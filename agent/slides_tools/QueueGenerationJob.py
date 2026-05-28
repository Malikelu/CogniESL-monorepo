"""
QueueGenerationJob — registers a generation job in the jobs database.

This tool is called by the orchestrator AFTER the teacher approves the Content
Brief and provides their email address. It creates a job record so the server
can track progress and serve download links when generation finishes.

NOTE (Phase 5 wiring):
    Currently this tool just creates the job record and returns the job_id.
    The actual generation still runs inline (via InsertNewSlides / ModifySlide).
    In Phase 5, this tool will also trigger a background thread so generation
    is fully decoupled from the HTTP connection. See PHASE5_PLAN.md.
"""
import os
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

# Import jobs module — works whether run from CogniESL root or agent/ subdir
import sys
_cogniesl_root = str(Path(__file__).parent.parent.parent)
if _cogniesl_root not in sys.path:
    sys.path.insert(0, _cogniesl_root)
from agent import jobs as _jobs
from agent.master_repository import (
    get_combination_key,
    check_cache,
    copy_from_cache,
    MASTER_REPO,
)


class QueueGenerationJob(BaseTool):
    """
    Register a new generation job and return a job_id.

    Call this AFTER the teacher approves the Content Brief and provides
    their email. The job_id appears in the completion email's download links.

    Returns a confirmation string with the job_id.
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

    def run(self) -> str:
        # Get user_id from agent context (set by server.py from JWT)
        _user_id = None
        try:
            _ctx = getattr(self, '_shared_state', None)
            if _ctx:
                _user_id = getattr(_ctx, 'user_id', None)
        except Exception:
            pass

        # ── Master Repository cache check ──────────────────────────────────────
        # For single-L1, single-level requests, check whether a pre-generated
        # deck already exists. If so, copy it to the project folder and instruct
        # the agent to skip straight to MarkJobComplete.
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
                # Copy cached slides into the project's presentations/ folder
                _dest = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data")) / "mnt" / self.project_name / "presentations"
                # Fallback to ./mnt/ for local dev
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

        # ── Normal job creation (no cache hit) ────────────────────────────────
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
        msg = f"Job registered. job_id={job_id}"
        if self.teacher_email:
            msg += (
                f" A completion email will be sent to {self.teacher_email} "
                f"with download links at {base_url}/download/{job_id}/<filename> "
                f"once generation finishes."
            )
        return msg
