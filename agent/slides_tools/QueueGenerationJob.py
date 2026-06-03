"""
QueueGenerationJob — registers a generation job and spawns background generation.

This tool is called by the orchestrator AFTER the teacher approves the Content
Brief. It creates a job record, then spawns a background thread that runs the
full generation pipeline asynchronously (InsertNewSlides -> ModifySlide ->
BuildOfflineBundle -> MarkJobComplete). The teacher gets an email when done.

ASYNC FLOW:
  1. Main thread: agent calls QueueGenerationJob
  2. QueueGenerationJob creates job record, adds job_id to _background_jobs set
  3. QueueGenerationJob spawns background thread, returns "being generated" msg
  4. Main thread's agent returns the msg to teacher immediately (< 60s)
  5. Background thread: creates fresh agent, sends "Go ahead" + job_id
  6. Background agent calls QueueGenerationJob again — detects job_id is in
     _background_jobs set -> returns "PROCEED_WITH_GENERATION" instead
  7. Background agent continues with InsertNewSlides, ModifySlide, etc.
  8. MarkJobComplete sends the email when done (15-25 min later)
"""
import asyncio
import logging
import os
import threading
import sys
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

_cogniesl_root = str(Path(__file__).parent.parent.parent)
if _cogniesl_root not in sys.path:
    sys.path.insert(0, _cogniesl_root)
from agent import jobs as _jobs
from agent.master_repository import (
    get_combination_key,
    check_cache,
    copy_from_cache,
)

logger = logging.getLogger(__name__)

# Set of job_ids where background generation is in progress.
# When QueueGenerationJob is called with a job_id in this set, it returns
# "PROCEED_WITH_GENERATION" so the agent continues with generation tools
# instead of sending a "being generated" message.
_background_jobs: set[str] = set()
_background_jobs_lock = threading.Lock()


class QueueGenerationJob(BaseTool):
    """
    Register a new generation job and return a job_id.

    Call this AFTER the teacher approves the Content Brief and provides
    their email. Generation runs in a background thread — the teacher gets
    an email with download links when it completes.
    """

    project_name: str = Field(
        ...,
        description="Project folder name (e.g. 'present_perfect_french_adults')",
    )
    grammar_point: str = Field(
        ...,
        description="Grammar point being taught (e.g. 'Present Perfect')",
    )
    l1_languages: str = Field(
        ...,
        description="Teacher's students' L1 language(s) (e.g. 'French' or 'Chinese, Japanese')",
    )
    age_group: str = Field(
        ...,
        description="Student age group (e.g. 'adults', 'teenagers', 'kids')",
    )
    formats: list[str] = Field(
        ...,
        description="List of formats being generated (e.g. ['slides', 'worksheet', 'activity guide'])",
    )
    teacher_email: str | None = Field(
        default=None,
        description="Teacher's email address for completion notification. None if not provided.",
    )
    existing_job_id: str | None = Field(
        default=None,
        description="If set, reuse this job_id instead of creating a new one. Used by background thread.",
    )

    async def run(self) -> str:
        _user_id = None
        try:
            _user_id = self.context.get('user_id', None)
        except Exception:
            pass

        # ── If this is a background-thread call: return PROCEED token ────────
        if self.existing_job_id:
            with _background_jobs_lock:
                if self.existing_job_id in _background_jobs:
                    # Update job status to running
                    _jobs.update_job(self.existing_job_id, status="running")
                    logger.info(f"Background thread signaled to proceed for job {self.existing_job_id}")
                    return "PROCEED_WITH_GENERATION"

        # ── Master Repository cache check ──────────────────────────────────────
        _l1_list = [l.strip() for l in self.l1_languages.split(",") if l.strip()]
        _level_val = getattr(self, "level", None) or "b1"
        if len(_l1_list) == 1:
            _cache_key = get_combination_key(
                grammar=self.grammar_point,
                l1=_l1_list[0],
                age=self.age_group,
                level=_level_val,
            )
            if check_cache(_cache_key):
                _dest = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data")) / "mnt" / self.project_name / "presentations"
                if not (_dest.parent.parent).exists():
                    _dest = Path(__file__).parent.parent.parent / "mnt" / self.project_name / "presentations"
                copied = copy_from_cache(_cache_key, _dest)
                if copied:
                    job_id = _jobs.create_job(
                        email=self.teacher_email,
                        project_name=self.project_name,
                        grammar_point=self.grammar_point,
                        l1_languages=self.l1_languages,
                        age_group=self.age_group,
                        formats=self.formats,
                        user_id=_user_id,
                    )
                    return (
                        f"CACHE HIT ✅ job_id={job_id} — pre-generated slides found for "
                        f"'{_cache_key}'. Files copied to {_dest}. "
                        f"Skip generation — proceed directly to MarkJobComplete with the "
                        f"pptx_path pointing to the copied file."
                    )

        # ── Create job record ──────────────────────────────────────────────────
        job_id = _jobs.create_job(
            email=self.teacher_email,
            project_name=self.project_name,
            grammar_point=self.grammar_point,
            l1_languages=self.l1_languages,
            age_group=self.age_group,
            formats=self.formats,
            user_id=_user_id,
        )
        base_url = os.getenv("COGNIESL_BASE_URL", "http://localhost:8080")

        # ── Register as background job and spawn generation thread ────────────
        with _background_jobs_lock:
            _background_jobs.add(job_id)

        thread = threading.Thread(
            target=_run_background_generation,
            args=(
                job_id,
                self.project_name,
                self.grammar_point,
                self.l1_languages,
                self.age_group,
                self.formats,
                self.teacher_email,
                _user_id,
                self.context.get('format_hint', ''),
            ),
            daemon=True,
            name=f"bg-gen-{job_id}",
        )
        thread.start()
        logger.info(f"Background generation thread started for job {job_id}")

        # ── Return immediately to the teacher ─────────────────────────────────
        msg = f"QueueGenerationJob complete. job_id={job_id}. STOP. Do NOT call any more tools. The teacher has been notified."
        if self.teacher_email:
            msg += (
                f" Your materials are being generated in the background."
            )
        else:
            msg += (
                f" No email provided. The background will generate your materials."
            )
        
        # Set context flag so generation tools know to skip
        try:
            self.context.set('_generation_queued', True)
            self.context.set('_generation_job_id', job_id)
        except Exception:
            pass
        
        return msg


def _run_background_generation(
    job_id: str,
    project_name: str,
    grammar_point: str,
    l1_languages: str,
    age_group: str,
    formats: list[str],
    teacher_email: str | None,
    user_id: str | None,
    format_hint: str,
) -> None:
    """Run the full generation pipeline in a background thread."""
    try:
        _run_generation(
            job_id, project_name, grammar_point, l1_languages,
            age_group, formats, teacher_email, user_id, format_hint,
        )
    except Exception as e:
        logger.error(f"Background generation failed for job {job_id}: {e}", exc_info=True)
        try:
            _jobs.mark_error(job_id, str(e))
        except Exception:
            pass
    finally:
        # Cleanup: remove from background jobs set
        with _background_jobs_lock:
            _background_jobs.discard(job_id)


def _preload_yaml_context(
    grammar_point: str,
    l1_languages: str,
    age_group: str,
) -> str:
    """Pre-load YAML database content in Python and return it as formatted text.

    Why: The background agent reads YAML via tool calls, but DeepSeek doesn't paste
    the content verbatim when writing 17+ ModifySlide task_briefs — by slide 5 the
    tool output from slide 1's DB search is far back in the context window and the
    model summarizes instead. Injecting the data here puts it in the LLM's context
    from the very first token, every single slide call.

    The agent still runs DB searches (per instructions.md AUTOMATED GENERATION MODE)
    but this block acts as a safety net ensuring the raw data is always available.
    """
    try:
        import yaml as _yaml
    except ImportError:
        return ""

    sections: list[str] = [
        "=== PRE-LOADED DATABASE CONTENT ===",
        "The following data was loaded directly from the YAML database.",
        "Use it VERBATIM in every task_brief — do NOT summarize or paraphrase.",
        "Paste exact CCQ question/answer text, exact wrong→correct pairs, exact structure strings.",
        "",
    ]

    # ── Grammar YAML ──────────────────────────────────────────────────────────
    try:
        from agent.tools.SearchGrammarTool import SearchGrammarTool
        result = SearchGrammarTool(topic=grammar_point).run()
        if isinstance(result, dict):
            sections.append(f"--- GRAMMAR YAML: {grammar_point} ---")
            sections.append(_yaml.dump(result, default_flow_style=False, allow_unicode=True).strip())
            sections.append("")
        else:
            sections.append(f"[Grammar lookup: {str(result)[:120]}]")
    except Exception as exc:
        sections.append(f"[Grammar data unavailable: {exc}]")

    # ── L1 Interference YAMLs ─────────────────────────────────────────────────
    gram_slug = grammar_point.lower().strip().replace(" ", "_").replace("-", "_")
    for l1 in [l.strip() for l in l1_languages.split(",") if l.strip()]:
        try:
            from agent.tools.GetL1InterferenceTool import GetL1InterferenceTool
            result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
            if isinstance(result, dict):
                sections.append(f"--- L1 INTERFERENCE YAML: {l1} / {grammar_point} ---")
                sections.append(_yaml.dump(result, default_flow_style=False, allow_unicode=True).strip())
                sections.append("")
            else:
                sections.append(f"[L1 {l1}: {str(result)[:120]}]")
        except Exception as exc:
            sections.append(f"[L1 {l1} data unavailable: {exc}]")

    # ── Activities (top 3) ────────────────────────────────────────────────────
    try:
        from agent.tools.SearchActivitiesTool import SearchActivitiesTool
        result = SearchActivitiesTool(topic=grammar_point, age_group=age_group, max_results=3).run()
        if result and not isinstance(result, str):
            sections.append(f"--- ACTIVITY TEMPLATES: {grammar_point} / {age_group} ---")
            sections.append(_yaml.dump(result, default_flow_style=False, allow_unicode=True).strip())
            sections.append("")
    except Exception as exc:
        sections.append(f"[Activities data unavailable: {exc}]")

    return "\n".join(sections)


def _run_generation(
    job_id: str,
    project_name: str,
    grammar_point: str,
    l1_languages: str,
    age_group: str,
    formats: list[str],
    teacher_email: str | None,
    user_id: str | None,
    format_hint: str | None,
) -> None:
    """Core generation logic — runs in its own thread.

    Uses asyncio.run() to handle the event loop lifecycle (creates loop,
    runs coroutine, cancels pending tasks, closes loop).
    """

    try:
        from agent.cogniesl_agent import create_cogniesl_agent
        # bg_mode=True: uses BG_DEFAULT_MODEL env var if set, so background traffic
        # can be routed through OpenRouter when direct DeepSeek fails in threads.
        agent = create_cogniesl_agent(format_request=format_hint or "", bg_mode=True)

        from agency_swarm import ThreadManager
        from agency_swarm.agent.context_types import AgencyContext, AgentRuntimeState
        ctx = AgencyContext(
            agency_instance=None,
            thread_manager=ThreadManager(),
            runtime_state=AgentRuntimeState(agent._tool_concurrency_manager),
        )
        if user_id:
            ctx.user_id = user_id

        # Pre-load YAML data in Python and embed it in the agent's first message.
        # This ensures all grammar/L1/activities data is in the context window from
        # slide 1 through slide 17, instead of relying on DeepSeek to remember
        # tool-call outputs across 17+ subsequent ModifySlide calls.
        yaml_context = _preload_yaml_context(grammar_point, l1_languages, age_group)
        logger.info(f"Pre-loaded YAML context: {len(yaml_context)} chars for job {job_id}")

        formats_str = ", ".join(formats) if isinstance(formats, list) else formats
        l1_str = l1_languages or "English"
        email_part = f"My email is {teacher_email}." if teacher_email else ""

        db_block = (
            f"\n\n<DATABASE_CONTENT>\n{yaml_context}\n</DATABASE_CONTENT>\n\n"
            f"The DATABASE_CONTENT above contains the complete YAML data for this lesson. "
            f"When calling ModifySlide for each slide, paste the relevant fields VERBATIM "
            f"into the task_brief — exact CCQ text, exact wrong→correct pairs, exact "
            f"structure strings. The minimum task_brief sizes from the Golden Rule apply."
        ) if yaml_context.strip() else ""

        msg = (
            f"<memory-context>AUTOMATED GENERATION — teacher already approved. "
            f"Do NOT show a Content Brief. Do NOT ask for approval, email, or confirmation. "
            f"Skip directly to QueueGenerationJob with existing_job_id={job_id}. "
            f"After PROCEED_WITH_GENERATION: the DATABASE_CONTENT block below already "
            f"contains all YAML data — do NOT run DB searches again, just use the data "
            f"directly when writing task_briefs. Call InsertNewSlides immediately, then "
            f"ModifySlide for each slide pasting from DATABASE_CONTENT verbatim.</memory-context>\n"
            f"Generate {formats_str} for {grammar_point} for {l1_str} {age_group}. "
            f"{email_part}"
            f"{db_block}"
            f"\nGo ahead."
        )

        async def _run_async():
            response = await agent.get_response(message=msg, agency_context=ctx)
            text = str(getattr(response, 'final_output', response))
            return text

        # Use asyncio.run() instead of manual loop management — it properly
        # cleans up pending tasks (LiteLLM logging worker, etc.)
        result = asyncio.run(_run_async())
        logger.info(f"Background generation completed for job {job_id}")

        # Check if job was marked done by MarkJobComplete
        job = _jobs.get_job(job_id)
        if job and job.get("status") != "done":
            data_dir = Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent.parent.parent))
            presentations_dir = data_dir / "mnt" / project_name / "presentations"
            if presentations_dir.exists() and list(presentations_dir.glob("*.html")):
                files = [str(p) for p in presentations_dir.glob("*")]
                _jobs.mark_done(job_id, files)
                logger.info(f"Fallback: marked job {job_id} done with {len(files)} files")
            else:
                _jobs.mark_error(job_id, f"Generation completed but no files: {result[:300]}")
                logger.error(f"Background gen job {job_id}: no files. Agent said: {result[:300]}")

    except Exception as e:
        logger.error(f"Background generation error for job {job_id}: {e}", exc_info=True)
        try:
            _jobs.mark_error(job_id, str(e))
        except Exception:
            pass
