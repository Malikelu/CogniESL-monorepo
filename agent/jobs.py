"""
CogniESL job queue — tracks background generation jobs in SQLite.

Each job is created when a teacher approves the Content Brief.
The background worker updates status and file paths when done.
Email is sent on completion via email_sender.py.
"""
import json
import logging
import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Store alongside cogniesl.db so Railway Volume covers both DBs at once.
def _resolve_db_dir() -> Path:
    preferred = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data"))
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        return preferred
    except (PermissionError, OSError):
        fallback = Path(__file__).parent.parent / "data"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

_MNT_DIR = _resolve_db_dir()
_DB_PATH = _MNT_DIR / "jobs.db"


def init_db() -> None:
    """Create the jobs table if it doesn't exist. Safe to call on every startup."""
    with sqlite3.connect(_DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id       TEXT PRIMARY KEY,
                status       TEXT NOT NULL DEFAULT 'pending',
                email        TEXT,
                user_id      TEXT,
                project_name TEXT,
                grammar_point TEXT,
                l1_languages TEXT,
                age_group    TEXT,
                formats      TEXT,
                file_paths   TEXT,
                created_at   TEXT NOT NULL,
                completed_at TEXT,
                error        TEXT
            )
        """)
        # Migrate existing databases that don't have user_id yet
        try:
            db.execute("ALTER TABLE jobs ADD COLUMN user_id TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
    logger.info(f"Jobs DB ready at {_DB_PATH}")


def create_job(
    email: str | None,
    project_name: str,
    grammar_point: str,
    l1_languages: str,
    age_group: str,
    formats: list[str],
    user_id: str | None = None,
) -> str:
    """Insert a new pending job. Returns the job_id."""
    job_id = str(uuid.uuid4())[:8]
    with sqlite3.connect(_DB_PATH) as db:
        db.execute(
            """INSERT INTO jobs
               (job_id, status, email, user_id, project_name, grammar_point,
                l1_languages, age_group, formats, created_at)
               VALUES (?, 'pending', ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                job_id,
                email,
                user_id,
                project_name,
                grammar_point,
                l1_languages,
                age_group,
                json.dumps(formats),
                datetime.utcnow().isoformat(),
            ),
        )
    logger.info(f"Job {job_id} created for project '{project_name}'")
    return job_id


def update_job(job_id: str, **kwargs) -> None:
    """Update arbitrary fields on a job. kwargs keys must match column names."""
    if not kwargs:
        return
    # Serialize lists/dicts to JSON (build new dict to avoid mutating during iteration)
    kwargs = {k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in kwargs.items()}
    cols = ", ".join(f"{k}=?" for k in kwargs)
    with sqlite3.connect(_DB_PATH) as db:
        db.execute(f"UPDATE jobs SET {cols} WHERE job_id=?", (*kwargs.values(), job_id))


def mark_done(job_id: str, file_paths: list[str]) -> None:
    """Mark job complete and record the generated file paths."""
    update_job(
        job_id,
        status="done",
        file_paths=json.dumps(file_paths),
        completed_at=datetime.utcnow().isoformat(),
    )
    logger.info(f"Job {job_id} marked done with {len(file_paths)} file(s)")


def mark_error(job_id: str, error: str) -> None:
    """Mark job as errored."""
    update_job(job_id, status="error", error=error)
    logger.error(f"Job {job_id} errored: {error}")


def get_job(job_id: str) -> dict | None:
    """Return a job dict or None if not found."""
    with sqlite3.connect(_DB_PATH) as db:
        db.row_factory = sqlite3.Row
        row = db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    # Deserialize JSON fields
    for field in ("file_paths", "formats"):
        if d.get(field):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                pass
    return d


def list_jobs(limit: int = 50) -> list[dict]:
    """Return the most recent jobs (for debugging/admin)."""
    with sqlite3.connect(_DB_PATH) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
