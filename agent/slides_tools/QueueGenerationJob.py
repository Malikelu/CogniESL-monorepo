"""
QueueGenerationJob — registers a generation job and spawns background generation.

ASYNC FLOW:
  1. Main thread: agent calls QueueGenerationJob
  2. QueueGenerationJob creates job record, adds job_id to _background_jobs set
  3. QueueGenerationJob spawns background thread, returns "being generated" msg
  4. Main thread's agent returns the msg to teacher immediately (< 60s)
  5. Background thread runs the FULL PIPELINE in pure Python (no agent):
     - Load YAML data → compute slide plan → build task_briefs
     - Insert blank slide placeholders
     - Call ModifySlide in parallel batches (3 at a time)
     - ValidateSlideSet → BuildOfflineBundle
     - CreateDocument for worksheet/activity (if requested)
     - GenerateFlashcardPdf (if requested)
     - MarkJobComplete
"""

import asyncio
import json
import logging
import os
import re
import sys
import threading
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
        description="Teacher's email address for completion notification.",
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
                _dest = _get_mnt_path(self.project_name) / "presentations"
                _dest.mkdir(parents=True, exist_ok=True)
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
                        f"Skip generation — proceed directly to MarkJobComplete."
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
            msg += f" Your materials are being generated in the background."
        else:
            msg += f" No email provided. The background will generate your materials."

        try:
            self.context.set('_generation_queued', True)
            self.context.set('_generation_job_id', job_id)
        except Exception:
            pass

        return msg


# ═══════════════════════════════════════════════════════════════════════════
# Background Generation Pipeline
# ═══════════════════════════════════════════════════════════════════════════

BATCH_SIZE = 3  # Parallel slide generation — 3 slides at a time


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
        with _background_jobs_lock:
            _background_jobs.discard(job_id)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_mnt_path(project_name: str) -> Path:
    """Return the mnt directory path for this project.

    Precedence:
    1. COGNIESL_DATA_DIR env var (set on Railway by nixpacks)
    2. /app/data (Railway persistent volume — detect by dir existence)
    3. Project root (local dev fallback)
    """
    data_dir = os.getenv("COGNIESL_DATA_DIR")
    if data_dir:
        return Path(data_dir) / "mnt" / project_name
    if Path("/app/data").is_dir():
        return Path("/app/data") / "mnt" / project_name
    return Path(__file__).parent.parent.parent / "mnt" / project_name


# ── Crash-proof progress tracking ──────────────────────────────────────────

_progress_lock = threading.Lock()


def _write_progress(project_name: str, step: str, details: str = "") -> None:
    """Write a persistent progress marker to disk.

    Even if the process is killed immediately after, the last-written line
    survives on the Railway volume so we can identify exactly where it died.
    """
    try:
        import datetime
        mnt = _get_mnt_path(project_name)
        ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
        line = f"[{ts}] {step}  {details}\n"
        path = mnt / ".pipeline_progress"
        with _progress_lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a") as f:
                f.write(line)
    except Exception:
        pass  # progress logging must never crash the pipeline


def _list_slide_filenames(project_name: str, file_prefix: str = "slide") -> list[str]:
    """Return sorted list of slide filenames (e.g. ['slide_01.html', ...])."""
    presentations_dir = _get_mnt_path(project_name) / "presentations"
    if not presentations_dir.exists():
        return []
    pattern = re.compile(rf"^{re.escape(file_prefix)}_(\d+).*\.html$", re.IGNORECASE)
    files = []
    for path in sorted(presentations_dir.iterdir()):
        if pattern.match(path.name):
            files.append(path.name)
    return sorted(files)


def _load_yaml_data(
    grammar_point: str,
    l1_languages: str,
    age_group: str,
) -> tuple[dict | None, list[dict]]:
    """Load grammar and L1 YAML data as Python dicts for programmatic use."""
    grammar_data = None
    l1_data_list: list[dict] = []

    # Grammar YAML
    try:
        from agent.tools.SearchGrammarTool import SearchGrammarTool
        result = SearchGrammarTool(topic=grammar_point).run()
        if isinstance(result, dict):
            grammar_data = result
    except Exception as exc:
        logger.warning(f"Could not load grammar YAML: {exc}")

    # L1 Interference YAMLs
    gram_slug = grammar_point.lower().strip().replace(" ", "_").replace("-", "_")
    for l1 in [l.strip() for l in l1_languages.split(",") if l.strip()]:
        try:
            from agent.tools.GetL1InterferenceTool import GetL1InterferenceTool
            result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
            if isinstance(result, dict):
                l1_data_list.append(result)
        except Exception as exc:
            logger.warning(f"Could not load L1 YAML for {l1}: {exc}")

    return grammar_data, l1_data_list


def _create_blank_slides(project_name: str, count: int) -> None:
    """Create blank HTML placeholder files for all slides."""
    presentations_dir = _get_mnt_path(project_name) / "presentations"
    presentations_dir.mkdir(parents=True, exist_ok=True)

    blank_html = (
        "<!DOCTYPE html><html lang=\"en\"><head>"
        "<meta charset=\"utf-8\">"
        "<title>Slide</title>"
        "</head><body></body></html>"
    )
    pad_width = max(2, len(str(count)))
    for i in range(count):
        name = f"slide_{i + 1:0{pad_width}d}.html"
        path = presentations_dir / name
        path.write_text(blank_html, encoding="utf-8")


def _build_worksheet_html(
    grammar_data: dict,
    l1_data_list: list[dict],
    grammar_point: str,
    l1_languages: str,
) -> str:
    """Build worksheet HTML from YAML data."""
    common_errors = grammar_data.get("common_errors") or []
    l1_list = [l.strip().lower() for l in l1_languages.split(",") if l.strip()]
    meaning = grammar_data.get("meaning", {})
    core = meaning.get("core_meaning", meaning.get("short_meaning", ""))

    def _s(v):
        if v is None:
            return ""
        return str(v)

    # Collect relevant errors
    errors = [e for e in common_errors if isinstance(e, dict)][:8]
    l1_patterns = []
    for ld in l1_data_list:
        patterns = ld.get("interference_patterns") or ld.get("patterns") or []
        for p in patterns:
            if isinstance(p, dict):
                l1_patterns.append(p)

    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head>',
        '<meta charset="utf-8">',
        f"<title>Worksheet — {grammar_point}</title>",
        '<style>',
        'body { font-family: "Segoe UI", Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }',
        'h1 { color: #0b7272; border-bottom: 3px solid #0b7272; padding-bottom: 8px; }',
        'h2 { color: #333; margin-top: 30px; }',
        '.error { color: #dc2626; } .correct { color: #16a34a; }',
        '.section { background: #f8fafc; padding: 20px; margin: 15px 0; }',
        'ol li { margin: 10px 0; }',
        '.answer-key { background: #f0fdf4; padding: 20px; margin: 15px 0; }',
        '</style></head><body>',
        f'<h1>{grammar_point} — Worksheet</h1>',
        f'<p><strong>Core meaning:</strong> {_s(core)}</p>',
    ]

    # Section A: Fill the Gap
    html_parts.append('<div class="section">')
    html_parts.append("<h2>Section A: Fill the Gap</h2>")
    html_parts.append("<p>Complete the sentences with the correct form.</p><ol>")
    for i, err in enumerate(errors[:4]):
        wrong = _s(err.get("wrong", err.get("example_wrong", "")))
        correct = _s(err.get("correct", err.get("example_correct", "")))
        explanation = _s(err.get("explanation", ""))
        gap_text = correct if correct else wrong
        html_parts.append(f"<li>{gap_text}</li>")
    html_parts.append("</ol></div>")

    # Section B: Error Correction
    html_parts.append('<div class="section">')
    html_parts.append("<h2>Section B: Error Correction</h2>")
    html_parts.append("<p>Each sentence has ONE error. Correct it.</p><ol>")
    for i, err in enumerate(errors[4:8], start=1):
        wrong = _s(err.get("wrong", err.get("example_wrong", "")))
        correct = _s(err.get("correct", err.get("example_correct", "")))
        if wrong:
            html_parts.append(f'<li><span class="error">{wrong}</span> → <span class="correct">{correct}</span></li>')
    html_parts.append("</ol></div>")

    # Section C: L1 Drill
    if l1_patterns:
        html_parts.append('<div class="section">')
        html_parts.append("<h2>Section C: L1 Drill — Watch Your Language!</h2>")
        html_parts.append("<p>Fix these sentences that [L1] speakers often get wrong.</p><ol>")
        for i, p in enumerate(l1_patterns[:4]):
            wrong = _s(p.get("example_wrong", p.get("wrong", "")))
            correct = _s(p.get("example_correct", p.get("correct", "")))
            if wrong:
                html_parts.append(f'<li><span class="error">{wrong}</span> → <span class="correct">{correct}</span></li>')
        html_parts.append("</ol></div>")

    # Section D: Create Your Own
    html_parts.append('<div class="section">')
    html_parts.append("<h2>Section D: Write Your Own</h2>")
    html_parts.append(f"<p>Write 3 original sentences using {grammar_point}.</p><ol>")
    for i in range(3):
        html_parts.append(f"<li>_____________________________</li>")
    html_parts.append("</ol></div>")

    # Answer Key
    html_parts.append('<div class="answer-key">')
    html_parts.append("<h2>Answer Key</h2><ol>")
    for err in errors[:8]:
        correct = _s(err.get("correct", err.get("example_correct", "")))
        if correct:
            html_parts.append(f"<li>{correct}</li>")
    html_parts.append("</ol>")
    html_parts.append("<p><em>Note: L1-specific errors benefit from teacher-led discussion.</em></p>")
    html_parts.append("</div>")

    # L1 Highlights
    for ld in l1_data_list:
        lang = _s(ld.get("language", ld.get("name", "")))
        html_parts.append(f'<p><strong>{lang} learners:</strong> Review the L1 Oracle slides for language-specific patterns.</p>')

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _build_activity_guide_html(
    grammar_data: dict,
    grammar_point: str,
    age_group: str,
) -> str:
    """Build activity guide HTML from YAML data."""
    teaching = grammar_data.get("teaching", {})
    recommended = teaching.get("recommended_activities") or []
    methodology = teaching.get("methodology", "")
    tips = teaching.get("tips") or []

    def _s(v):
        if v is None:
            return ""
        return str(v)

    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head>',
        '<meta charset="utf-8">',
        f"<title>Activity Guide — {grammar_point}</title>",
        '<style>',
        'body { font-family: "Segoe UI", Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }',
        'h1 { color: #0b7272; border-bottom: 3px solid #0b7272; padding-bottom: 8px; }',
        'h2 { color: #333; margin-top: 30px; }',
        '.activity { background: #f8fafc; padding: 20px; margin: 15px 0; border-left: 4px solid #0b7272; }',
        '</style></head><body>',
        f'<h1>{grammar_point} — Activity Guide</h1>',
        f"<h2>Recommended Methodology</h2>",
        f"<p>{_s(methodology)}</p>",
    ]

    if tips:
        html_parts.append("<h2>Teaching Tips</h2><ul>")
        for t in tips[:5]:
            text = _s(t.get("text", t)) if isinstance(t, dict) else _s(t)
            html_parts.append(f"<li>{text}</li>")
        html_parts.append("</ul>")

    for i, act in enumerate(recommended[:3]):
        name = _s(act.get("name", act.get("title", f"Activity {i+1}")))
        duration = _s(act.get("duration", "15"))
        instructions = _s(act.get("instructions", act.get("description", "")))
        html_parts.append(f'<div class="activity">')
        html_parts.append(f"<h3>{name}</h3>")
        html_parts.append(f"<p><strong>Duration:</strong> {duration} minutes</p>")
        html_parts.append(f"<p><strong>Instructions:</strong> {instructions}</p>")

        support = _s(act.get("differentiation", {}).get("support", ""))
        extension = _s(act.get("differentiation", {}).get("extension", ""))
        if support:
            html_parts.append(f"<p><strong>Support:</strong> {support}</p>")
        if extension:
            html_parts.append(f"<p><strong>Extension:</strong> {extension}</p>")

        l1_enhanced = act.get("l1Enhanced", "")
        if l1_enhanced:
            html_parts.append(f"<p><em>L1 enhanced activity</em></p>")

        html_parts.append("</div>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _get_slide_files_list(project_name: str) -> list[str]:
    """Return list of absolute paths to generated files for MarkJobComplete."""
    mnt = _get_mnt_path(project_name)
    files = []
    presentations = mnt / "presentations"
    if presentations.exists():
        for f in presentations.iterdir():
            if f.is_file():
                files.append(str(f))
    documents = mnt / "documents"
    if documents.exists():
        for f in documents.iterdir():
            if f.is_file():
                files.append(str(f))
    return files


# ── Main Generation Pipeline ─────────────────────────────────────────────────

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

    FULL PYTHON PIPELINE (no agent):
      1. Load YAML data as dicts
      2. Compute slide plan → build task_briefs from YAML verbatim
      3. Create blank slide placeholders
      4. Call ModifySlide in parallel batches (BATCH_SIZE at a time)
      5. ValidateSlideSet
      6. BuildOfflineBundle
      7. CreateDocument for worksheet (if requested)
      8. CreateDocument for activity guide (if requested)
      9. GenerateFlashcardPdf (if requested)
     10. MarkJobComplete
    """
    all_formats = [f.strip().lower() for f in formats] if isinstance(formats, list) else [formats.strip().lower()]
    has_slides = "slides" in all_formats or not all_formats
    has_worksheet = "worksheet" in all_formats
    has_activity = "activity" in all_formats or "activity guide" in all_formats
    has_flashcards = "flashcards" in all_formats or "flash card" in all_formats

    try:
        # ── Step 1: Load YAML data ─────────────────────────────────────────────
        _write_progress(project_name, "1:load-yaml", "start")
        grammar_data, l1_data_list = _load_yaml_data(grammar_point, l1_languages, age_group)
        if grammar_data is None:
            grammar_data = {}
        logger.info(f"Loaded YAML: grammar={'yes' if grammar_data else 'no'}, l1_files={len(l1_data_list)}")
        _write_progress(project_name, "1:load-yaml", f"grammar={bool(grammar_data)}, l1={len(l1_data_list)}")

        # ── Step 2: Compute slide plan + build task_briefs ──────────────────────
        _write_progress(project_name, "2:slide-plan", "start")
        from agent.slides_tools.slide_plan import compute_slide_plan, build_all_task_briefs

        slide_plan = compute_slide_plan(grammar_data, l1_languages, age_group)
        slide_count = len(slide_plan)
        task_briefs = build_all_task_briefs(
            slide_plan, grammar_data, l1_data_list, age_group, l1_languages
        )

        # Log task_brief sizes
        total_brief_chars = sum(len(b) for b in task_briefs.values())
        logger.info(
            f"Slide plan: {slide_count} slides, "
            f"{total_brief_chars} total task_brief chars "
            f"({total_brief_chars // max(slide_count, 1)} avg) for job {job_id}"
        )
        _write_progress(project_name, "2:slide-plan", f"{slide_count} slides, {total_brief_chars} chars")

        # Verify no thin task_briefs
        thin_briefs = [k for k, v in task_briefs.items() if len(v) < 200 and k != slide_count]
        if thin_briefs:
            logger.warning(f"Thin task_briefs detected: {thin_briefs}. "
                           f"These slides will likely have poor quality.")

        # ── Step 3: Create blank slide placeholders ─────────────────────────────
        _create_blank_slides(project_name, slide_count)

        # ── Step 3b: Generate Theme DNA ─────────────────────────────────────────
        # Before any slides, generate and write a cohesive visual theme (_theme.css)
        # so every ModifySlide call shares the same color palette, fonts, and style.
        try:
            from agent.slides_tools.theme_generator import generate_theme, write_theme_css
            from agent.slides_tools.slide_file_utils import get_project_dir
            presentations_dir = get_project_dir(project_name)
            theme = generate_theme(grammar_point, age_group)
            theme_path = write_theme_css(presentations_dir, theme)
            logger.info(f"Theme DNA: {theme_path.name} ({theme.get('mood', '?')}/{theme.get('font_heading', '?')})")
            _write_progress(project_name, "3:theme", f"{theme_path.name}")
        except Exception as exc:
            logger.warning(f"Theme generation skipped: {exc}")

        # ── Step 4: Run ModifySlide sequentially (one slide at a time) ──────────
        async def _run_slide_batches():
            from agent.slides_tools.ModifySlide import ModifySlide

            # Get slide file names (may be 'slide_01.html', 'slide_02.html', ...)
            slide_files = _list_slide_filenames(project_name)
            delay = int(os.getenv("SLIDE_GENERATION_DELAY", "5"))  # seconds between batches
            total_batches = (len(slide_files) + BATCH_SIZE - 1) // BATCH_SIZE

            for i in range(0, len(slide_files), BATCH_SIZE):
                batch = slide_files[i:i + BATCH_SIZE]
                tasks = []
                batch_num = i // BATCH_SIZE + 1
                for filename in batch:
                    # Extract slide index from filename
                    m = re.search(r'slide_(\d+)', filename)
                    if not m:
                        continue
                    slide_idx = int(m.group(1))
                    brief = task_briefs.get(slide_idx, "")
                    tasks.append(
                        ModifySlide(
                            project_name=project_name,
                            slide_name=filename,
                            task_brief=brief,
                        ).run()
                    )

                if tasks:
                    batch_ok = True
                    for t_idx, task in enumerate(tasks):
                        # Individual task timeout — one slow slide doesn't block others
                        filename = batch[t_idx]
                        try:
                            await asyncio.wait_for(task, timeout=120)
                        except asyncio.TimeoutError:
                            logger.error(
                                f"Batch {batch_num}/{total_batches}: TIMEOUT after 120s for "
                                f"{filename} (job {job_id}). Slide will be blank."
                            )
                            batch_ok = False
                        except Exception as exc:
                            logger.error(
                                f"Batch {batch_num}/{total_batches}: ERROR on {filename}: {exc}"
                            )
                            batch_ok = False
                    logger.info(
                        f"Batch {batch_num}/{total_batches}: "
                        f"{'ok' if batch_ok else 'partial fail'} "
                        f"({len(tasks)} slides) for job {job_id}"
                    )

                if delay > 0 and i + BATCH_SIZE < len(slide_files):
                    await asyncio.sleep(delay)

        if has_slides and slide_count > 0:
            asyncio.run(_run_slide_batches())
            logger.info(f"All {slide_count} slides generated for job {job_id}")
            _write_progress(project_name, "4:slides", f"{slide_count} slides done")
        elif not has_slides:
            logger.info(f"No slides requested for job {job_id}")
        else:
            logger.warning(f"No slides in plan for job {job_id}")
            slide_count = 0

        # ── Step 5: Validate slides ─────────────────────────────────────────────
        if has_slides and slide_count > 0:
            try:
                from agent.validation_tools.ValidateSlideSet import ValidateSlideSet
                l1_list = [l.strip() for l in l1_languages.split(",") if l.strip()]
                validation_result = ValidateSlideSet(
                    project_name=project_name,
                    slide_count=slide_count,
                    l1_languages=l1_list,
                ).run()
                logger.info(f"Validation: {validation_result[:300]}")
                _write_progress(project_name, "5:validation", "ok")
            except Exception as exc:
                logger.warning(f"Slide validation skipped: {exc}")

        # ── Step 6: Build offline bundle ────────────────────────────────────────
        bundle_path = None
        if has_slides and slide_count > 0:
            _write_progress(project_name, "6:bundle", "start")
            try:
                from agent.slides_tools.BuildOfflineBundle import BuildOfflineBundle
                bundle_result = BuildOfflineBundle(
                    project_name=project_name,
                    grammar_point=grammar_point,
                ).run()
                logger.info(f"Bundle: {bundle_result[:200]}")
                _write_progress(project_name, "6:bundle", "done")
                # Extract the bundle path from the result
                bundle_path = f"./mnt/{project_name}/presentations/{project_name}.html"
            except Exception as exc:
                _write_progress(project_name, "6:bundle", f"FAILED: {exc}")
                logger.warning(f"Bundle build skipped: {exc}")

        # ── Step 7: Worksheet ───────────────────────────────────────────────────
        worksheet_paths = {}
        if has_worksheet:
            _write_progress(project_name, "7:worksheet", "start")
            try:
                from agent.docs_tools.CreateDocument import CreateDocument
                html_content = _build_worksheet_html(
                    grammar_data, l1_data_list, grammar_point, l1_languages,
                )
                doc_result = CreateDocument(
                    project_name=project_name,
                    document_name=f"{project_name}_worksheet",
                    content={"type": "html", "value": html_content},
                    overwrite=True,
                ).run()
                logger.info(f"Worksheet: {str(doc_result)[:200]}")
                _write_progress(project_name, "7:worksheet", "done")
                worksheet_paths["source"] = f"./mnt/{project_name}/documents/{project_name}_worksheet.source.html"
            except Exception as exc:
                _write_progress(project_name, "7:worksheet", f"FAILED: {exc}")
                logger.warning(f"Worksheet generation skipped: {exc}")

        # ── Step 8: Activity Guide ──────────────────────────────────────────────
        activity_paths = {}
        if has_activity:
            _write_progress(project_name, "8:activity", "start")
            try:
                from agent.docs_tools.CreateDocument import CreateDocument
                html_content = _build_activity_guide_html(
                    grammar_data, grammar_point, age_group,
                )
                doc_result = CreateDocument(
                    project_name=project_name,
                    document_name=f"{project_name}_activity_guide",
                    content={"type": "html", "value": html_content},
                    overwrite=True,
                ).run()
                logger.info(f"Activity guide: {str(doc_result)[:200]}")
                _write_progress(project_name, "8:activity", "done")
                activity_paths["source"] = f"./mnt/{project_name}/documents/{project_name}_activity_guide.source.html"
            except Exception as exc:
                _write_progress(project_name, "8:activity", f"FAILED: {exc}")
                logger.warning(f"Activity guide generation skipped: {exc}")

        # ── Step 9: Flashcards ──────────────────────────────────────────────────
        flashcard_path = None
        if has_flashcards:
            _write_progress(project_name, "9:flashcards", "start")
            try:
                from agent.docs_tools.GenerateFlashcardPdf import GenerateFlashcardPdf
                common_errors = grammar_data.get("common_errors") or []
                l1_patterns = []
                l1_lang_single = ""
                for ld in l1_data_list:
                    patterns = ld.get("interference_patterns") or ld.get("patterns") or []
                    l1_patterns.extend(patterns)
                    l1_lang_single = ld.get("language", ld.get("name", ""))
                flash_result = GenerateFlashcardPdf(
                    project_name=project_name,
                    grammar_point=grammar_point,
                    common_errors_json=json.dumps(common_errors[:15]),
                    l1_language=l1_lang_single,
                    l1_patterns_json=json.dumps(l1_patterns[:10]),
                ).run()
                logger.info(f"Flashcards: {flash_result[:200]}")
                _write_progress(project_name, "9:flashcards", "done")
                flashcard_path = f"./mnt/{project_name}/documents/{project_name}_flashcards.source.html"
            except Exception as exc:
                _write_progress(project_name, "9:flashcards", f"FAILED: {exc}")
                logger.warning(f"Flashcard generation skipped: {exc}")

        # ── Step 10: Mark job complete ──────────────────────────────────────────
        _write_progress(project_name, "10:mark-complete", "start")
        from agent.slides_tools.MarkJobComplete import MarkJobComplete
        mark_result = MarkJobComplete(
            job_id=job_id,
            project_name=project_name,
            html_bundle_path=bundle_path,
            slide_count=slide_count,
            worksheet_pdf_path=worksheet_paths.get("source"),
            activity_pdf_path=activity_paths.get("source"),
            flashcard_pdf_path=flashcard_path,
        ).run()
        logger.info(f"Job {job_id} complete: {mark_result[:200]}")
        _write_progress(project_name, "10:mark-complete", "done")
        _write_progress(project_name, "PIPELINE", "COMPLETE SUCCESS")

    except Exception as e:
        logger.error(f"Generation error for job {job_id}: {e}", exc_info=True)
        _write_progress(project_name, "PIPELINE", f"FAILED: {e}")
        try:
            _jobs.mark_error(job_id, str(e))
        except Exception:
            pass
