"""User and materials database operations for CogniESL."""
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from auth.models import User, UserPublic

# Store DB in COGNIESL_DATA_DIR (default: /app/data) so Railway Volume persists it.
# Falls back to a local ./data/ directory for dev/testing environments.
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
_DB_PATH = _MNT_DIR / "cogniesl.db"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_auth_db() -> None:
    """Create users, materials, generations, password_reset_tokens, and waitlist tables if they don't exist."""
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                subscription_tier TEXT NOT NULL DEFAULT 'free',
                name TEXT NOT NULL DEFAULT ''
            )
        """)
        # Migrate existing deployments that pre-date the name column
        try:
            conn.execute("ALTER TABLE users ADD COLUMN name TEXT NOT NULL DEFAULT ''")
            conn.commit()
        except Exception:
            pass  # Column already exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                job_id TEXT,
                project_name TEXT NOT NULL,
                grammar_point TEXT NOT NULL,
                l1_languages TEXT NOT NULL DEFAULT '',
                age_group TEXT NOT NULL DEFAULT 'adults',
                level TEXT NOT NULL DEFAULT '',
                formats TEXT NOT NULL DEFAULT '',
                slide_count INTEGER DEFAULT 0,
                html_bundle_path TEXT,
                pptx_path TEXT,
                worksheet_pdf_path TEXT,
                worksheet_docx_path TEXT,
                activity_pdf_path TEXT,
                activity_docx_path TEXT,
                flashcard_pdf_path TEXT,
                progress_tracker_pdf_path TEXT,
                created_at TEXT NOT NULL,
                model_version TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        # Migrate existing materials tables that pre-date html_bundle_path / flashcard columns
        for _col, _type in [
            ("html_bundle_path", "TEXT"),
            ("flashcard_pdf_path", "TEXT"),
            ("progress_tracker_pdf_path", "TEXT"),
        ]:
            try:
                conn.execute(f"ALTER TABLE materials ADD COLUMN {_col} {_type}")
                conn.commit()
            except Exception:
                pass  # Column already exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                grammar_point TEXT NOT NULL DEFAULT '',
                l1_languages TEXT NOT NULL DEFAULT '',
                formats TEXT NOT NULL DEFAULT '',
                level TEXT NOT NULL DEFAULT '',
                age_group TEXT NOT NULL DEFAULT '',
                cost_estimate REAL DEFAULT 0.0,
                model_version TEXT DEFAULT '',
                cache_hit INTEGER DEFAULT 0,
                job_id TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                used INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS waitlist (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                source TEXT DEFAULT 'homepage'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscription_events (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                stripe_event_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                subscription_status TEXT NOT NULL DEFAULT '',
                new_tier TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                raw_json TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL DEFAULT '',
                material_id TEXT DEFAULT '',
                job_id TEXT DEFAULT '',
                rating TEXT NOT NULL,
                tags TEXT DEFAULT '',
                comment TEXT DEFAULT '',
                source TEXT DEFAULT 'explicit',
                created_at TEXT NOT NULL,
                reviewed INTEGER DEFAULT 0,
                resolution TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL DEFAULT '',
                event_type TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_actions (
                id TEXT PRIMARY KEY,
                agent_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                marcos_notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                resolved_at TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_snapshots (
                id TEXT PRIMARY KEY,
                snapshot_date TEXT NOT NULL,
                total_users INTEGER DEFAULT 0,
                total_gens INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0,
                active_users_7d INTEGER DEFAULT 0,
                signups_today INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_digests (
                id TEXT PRIMARY KEY,
                digest_date TEXT NOT NULL,
                content_json TEXT NOT NULL,
                sent INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orchestrator_runs (
                id TEXT PRIMARY KEY,
                run_type TEXT NOT NULL DEFAULT 'scheduled',
                status TEXT NOT NULL DEFAULT 'running',
                started_at TEXT NOT NULL,
                completed_at TEXT,
                agents_run TEXT DEFAULT '[]',
                critical_alerts INTEGER DEFAULT 0,
                error_message TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_health (
                agent_name TEXT PRIMARY KEY,
                last_run_at TEXT,
                last_success_at TEXT,
                consecutive_failures INTEGER DEFAULT 0,
                avg_runtime_seconds REAL DEFAULT 0,
                total_runs INTEGER DEFAULT 0,
                status TEXT DEFAULT 'unknown'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_messages (
                id TEXT PRIMARY KEY,
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                message_type TEXT NOT NULL,
                payload TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                processed INTEGER DEFAULT 0,
                processed_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_costs (
                id TEXT PRIMARY KEY,
                agent_name TEXT NOT NULL,
                action_id TEXT,
                estimated_cost_usd REAL DEFAULT 0,
                tokens_input INTEGER DEFAULT 0,
                tokens_output INTEGER DEFAULT 0,
                model_used TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS critical_alerts (
                id TEXT PRIMARY KEY,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                details_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                acknowledged INTEGER DEFAULT 0,
                acknowledged_at TEXT,
                resolved INTEGER DEFAULT 0,
                resolved_at TEXT,
                marcos_notes TEXT DEFAULT ''
            )
        """)
        for col_sql in [
            "ALTER TABLE materials ADD COLUMN level TEXT NOT NULL DEFAULT ''",
            "ALTER TABLE users ADD COLUMN stripe_customer_id TEXT DEFAULT ''",
            "ALTER TABLE agent_actions ADD COLUMN routed_to TEXT DEFAULT ''",
            "ALTER TABLE agent_actions ADD COLUMN routed_at TEXT DEFAULT ''",
            "ALTER TABLE agent_actions ADD COLUMN estimated_cost_usd REAL DEFAULT 0",
        ]:
            try:
                conn.execute(col_sql)
            except Exception:
                pass
        try:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_generations_created ON generations(created_at)")
        except Exception:
            pass
        try:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at)")
        except Exception:
            pass
        try:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_snapshots_date ON daily_snapshots(snapshot_date)")
        except Exception:
            pass
        conn.commit()


# ─── User operations ─────────────────────────────────────────────────────────

def create_user(email: str, password_hash: str, name: str = "") -> User:
    user = User(
        id=str(uuid.uuid4()),
        email=email.lower().strip(),
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc).isoformat(),
        subscription_tier="free",
        name=name.strip(),
    )
    with _conn() as conn:
        conn.execute(
            "INSERT INTO users (id, email, password_hash, created_at, subscription_tier, name) VALUES (?,?,?,?,?,?)",
            (user.id, user.email, user.password_hash, user.created_at, user.subscription_tier, user.name),
        )
        conn.commit()
    return user


def get_user_by_email(email: str) -> Optional[User]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
    if not row:
        return None
    return User(**dict(row))


def get_user_by_id(user_id: str) -> Optional[User]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if not row:
        return None
    return User(**dict(row))


# ─── Materials operations ─────────────────────────────────────────────────────

def create_material(
    user_id: str,
    job_id: str,
    project_name: str,
    grammar_point: str,
    l1_languages: str,
    age_group: str,
    formats: str,
    slide_count: int = 0,
    html_bundle_path: Optional[str] = None,
    pptx_path: Optional[str] = None,
    worksheet_pdf_path: Optional[str] = None,
    worksheet_docx_path: Optional[str] = None,
    activity_pdf_path: Optional[str] = None,
    activity_docx_path: Optional[str] = None,
    flashcard_pdf_path: Optional[str] = None,
    progress_tracker_pdf_path: Optional[str] = None,
    model_version: str = "",
) -> str:
    """Insert a material row; returns the new material id."""
    material_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            """INSERT INTO materials (
                id, user_id, job_id, project_name, grammar_point, l1_languages,
                age_group, formats, slide_count, html_bundle_path, pptx_path,
                worksheet_pdf_path, worksheet_docx_path, activity_pdf_path,
                activity_docx_path, flashcard_pdf_path, progress_tracker_pdf_path,
                created_at, model_version
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                material_id, user_id, job_id, project_name, grammar_point,
                l1_languages, age_group, formats, slide_count, html_bundle_path,
                pptx_path, worksheet_pdf_path, worksheet_docx_path, activity_pdf_path,
                activity_docx_path, flashcard_pdf_path, progress_tracker_pdf_path,
                created_at, model_version,
            ),
        )
        conn.commit()
    return material_id


def list_materials(
    user_id: str,
    grammar_point: Optional[str] = None,
    l1: Optional[str] = None,
    limit: int = 50,
) -> list[dict]:
    query = "SELECT * FROM materials WHERE user_id = ?"
    params: list = [user_id]
    if grammar_point:
        query += " AND grammar_point LIKE ?"
        params.append(f"%{grammar_point}%")
    if l1:
        query += " AND l1_languages LIKE ?"
        params.append(f"%{l1}%")
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_material(material_id: str, user_id: str) -> Optional[dict]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM materials WHERE id = ? AND user_id = ?",
            (material_id, user_id),
        ).fetchone()
    return dict(row) if row else None


def delete_material(material_id: str, user_id: str) -> bool:
    with _conn() as conn:
        cur = conn.execute(
            "DELETE FROM materials WHERE id = ? AND user_id = ?",
            (material_id, user_id),
        )
        conn.commit()
    return cur.rowcount > 0


def count_materials(user_id: str) -> int:
    with _conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM materials WHERE user_id = ?", (user_id,)
        ).fetchone()
    return row[0] if row else 0


# ─── Generations operations ───────────────────────────────────────────────────

TIER_LIMITS = {"free": 5, "pro": 20, "founding_member": 20, "school": 9999}


def record_generation(
    user_id: str,
    job_id: str = "",
    grammar_point: str = "",
    l1_languages: str = "",
    formats: str = "",
    level: str = "",
    age_group: str = "",
    cost_estimate: float = 0.0,
    model_version: str = "",
    cache_hit: bool = False,
) -> str:
    """Record one generation event. Returns the new generation id."""
    gen_id = str(uuid.uuid4())
    with _conn() as conn:
        conn.execute(
            """INSERT INTO generations
               (id, user_id, created_at, grammar_point, l1_languages, formats,
                level, age_group, cost_estimate, model_version, cache_hit, job_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                gen_id, user_id, datetime.now(timezone.utc).isoformat(),
                grammar_point, l1_languages, formats, level, age_group,
                cost_estimate, model_version, int(cache_hit), job_id,
            ),
        )
        conn.commit()
    return gen_id


def count_monthly_generations(user_id: str) -> int:
    """Count completed generations for the current calendar month."""
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    with _conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM generations WHERE user_id = ? AND created_at >= ?",
            (user_id, month_start),
        ).fetchone()
    return row[0] if row else 0


def get_tier_limit(tier: str) -> int:
    return TIER_LIMITS.get(tier, 5)


# ─── Password reset operations ────────────────────────────────────────────────

import secrets as _secrets


def create_reset_token(user_id: str) -> str:
    """Generate a password-reset token valid for 2 hours."""
    from datetime import timedelta
    token = _secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO password_reset_tokens (token, user_id, expires_at) VALUES (?,?,?)",
            (token, user_id, expires),
        )
        conn.commit()
    return token


def use_reset_token(token: str) -> Optional[str]:
    """Validate a reset token; return user_id if valid, None if expired or already used."""
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM password_reset_tokens WHERE token=? AND used=0 AND expires_at>?",
            (token, now),
        ).fetchone()
        if not row:
            return None
        conn.execute(
            "UPDATE password_reset_tokens SET used=1 WHERE token=?", (token,)
        )
        conn.commit()
    return row["user_id"]


def update_password(user_id: str, new_password_hash: str) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (new_password_hash, user_id),
        )
        conn.commit()


# ─── Account deletion ─────────────────────────────────────────────────────────

def delete_user_account(user_id: str) -> None:
    """Permanently delete a user and all their associated data."""
    with _conn() as conn:
        conn.execute("DELETE FROM generations WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM materials WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()


# ─── Stripe / Subscription operations ────────────────────────────────────────

def update_subscription_tier(user_id: str, new_tier: str) -> None:
    """Update a user's subscription tier."""
    with _conn() as conn:
        conn.execute(
            "UPDATE users SET subscription_tier=? WHERE id=?",
            (new_tier, user_id),
        )
        conn.commit()


def set_stripe_customer_id(user_id: str, stripe_customer_id: str) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE users SET stripe_customer_id=? WHERE id=?",
            (stripe_customer_id, user_id),
        )
        conn.commit()


def get_user_by_stripe_customer_id(stripe_customer_id: str) -> Optional["User"]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE stripe_customer_id = ?", (stripe_customer_id,)
        ).fetchone()
    if not row:
        return None
    return User(**dict(row))


def record_subscription_event(
    user_id: str,
    stripe_event_id: str,
    event_type: str,
    subscription_status: str,
    new_tier: str,
    raw_json: str = "",
) -> None:
    with _conn() as conn:
        # Ignore duplicate events (Stripe may send the same event twice)
        conn.execute(
            """INSERT OR IGNORE INTO subscription_events
               (id, user_id, stripe_event_id, event_type, subscription_status,
                new_tier, created_at, raw_json)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                str(uuid.uuid4()), user_id, stripe_event_id, event_type,
                subscription_status, new_tier,
                datetime.now(timezone.utc).isoformat(), raw_json,
            ),
        )
        conn.commit()


def count_founding_members() -> int:
    """Count active founding_member subscriptions."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM users WHERE subscription_tier='founding_member'"
        ).fetchone()
    return row[0] if row else 0


# ─── Waitlist operations ──────────────────────────────────────────────────────

def add_to_waitlist(email: str, source: str = "homepage") -> bool:
    """Add email to waitlist. Returns True if added, False if already present."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO waitlist (id, email, created_at, source) VALUES (?,?,?,?)",
                (str(uuid.uuid4()), email.lower().strip(),
                 datetime.now(timezone.utc).isoformat(), source),
            )
            conn.commit()
            return conn.execute(
                "SELECT changes()"
            ).fetchone()[0] > 0
    except Exception:
        return False


def count_waitlist() -> int:
    with _conn() as conn:
        row = conn.execute("SELECT COUNT(*) FROM waitlist").fetchone()
    return row[0] if row else 0


# ─── Feedback operations ──────────────────────────────────────────────────────

def save_feedback(
    rating: str,
    user_id: str = "",
    material_id: str = "",
    job_id: str = "",
    tags: str = "",
    comment: str = "",
    source: str = "explicit",
) -> str:
    """Save a feedback record. Returns the new feedback ID."""
    fid = str(uuid.uuid4())
    with _conn() as conn:
        conn.execute(
            """INSERT INTO feedback
               (id, user_id, material_id, job_id, rating, tags, comment, source, created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (fid, user_id, material_id, job_id, rating, tags, comment, source,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    return fid


def list_feedback(limit: int = 100, unreviewed_only: bool = False) -> list[dict]:
    with _conn() as conn:
        where = "WHERE reviewed=0" if unreviewed_only else ""
        rows = conn.execute(
            f"SELECT * FROM feedback {where} ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_feedback_summary() -> dict:
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        by_rating = conn.execute(
            "SELECT rating, COUNT(*) FROM feedback GROUP BY rating"
        ).fetchall()
        unreviewed = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE reviewed=0"
        ).fetchone()[0]
    return {
        "total": total,
        "unreviewed": unreviewed,
        "by_rating": {r[0]: r[1] for r in by_rating},
    }


# ─── Event tracking operations ────────────────────────────────────────────────

def log_event(event_type: str, user_id: str = "", metadata: str = "{}") -> None:
    """Log a behavioral event. Fire-and-forget; never raises."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO events (id, user_id, event_type, metadata, created_at) VALUES (?,?,?,?,?)",
                (str(uuid.uuid4()), user_id, event_type, metadata,
                 datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
    except Exception:
        pass


# ─── Feedback resolution ──────────────────────────────────────────────────────

def resolve_feedback(feedback_id: str, resolution_text: str) -> bool:
    """Mark feedback as reviewed and set resolution. Returns True if found."""
    with _conn() as conn:
        cur = conn.execute(
            "UPDATE feedback SET reviewed=1, resolution=? WHERE id=?",
            (resolution_text, feedback_id),
        )
        conn.commit()
    return cur.rowcount > 0


# ─── User activity & engagement ────────────────────────────────────────────────

def get_user_activity(user_id: str) -> dict:
    """Get full activity profile for a user."""
    with _conn() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            return {}
        gens = conn.execute(
            "SELECT * FROM generations WHERE user_id=? ORDER BY created_at DESC LIMIT 100",
            (user_id,),
        ).fetchall()
        mats = conn.execute(
            "SELECT id, project_name, grammar_point, l1_languages, created_at FROM materials WHERE user_id=? ORDER BY created_at DESC LIMIT 50",
            (user_id,),
        ).fetchall()
        fb = conn.execute(
            "SELECT * FROM feedback WHERE user_id=? ORDER BY created_at DESC LIMIT 50",
            (user_id,),
        ).fetchall()
        evts = conn.execute(
            "SELECT * FROM events WHERE user_id=? ORDER BY created_at DESC LIMIT 100",
            (user_id,),
        ).fetchall()
        subs = conn.execute(
            "SELECT * FROM subscription_events WHERE user_id=? ORDER BY created_at DESC LIMIT 20",
            (user_id,),
        ).fetchall()
        total_cost = conn.execute(
            "SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE user_id=?",
            (user_id,),
        ).fetchone()[0]
    return {
        "user": dict(user),
        "stats": {
            "total_generations": len(gens),
            "total_materials": len(mats),
            "total_feedback": len(fb),
            "first_seen": user["created_at"],
            "last_seen": gens[0]["created_at"] if gens else user["created_at"],
            "total_cost": round(total_cost, 4),
        },
        "generations": [dict(r) for r in gens],
        "materials": [dict(r) for r in mats],
        "feedback": [dict(r) for r in fb],
        "events": [dict(r) for r in evts],
        "subscription_history": [dict(r) for r in subs],
    }


def get_events_timeline(event_type: str = None, limit: int = 200, offset: int = 0) -> list[dict]:
    """Get recent events across all users."""
    with _conn() as conn:
        if event_type:
            rows = conn.execute(
                "SELECT * FROM events WHERE event_type=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (event_type, limit, offset),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM events ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
    return [dict(r) for r in rows]


def count_events_by_type(days: int = 30) -> dict:
    """Count events by type over the last N days."""
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT event_type, COUNT(*) as cnt FROM events WHERE created_at>=? GROUP BY event_type ORDER BY cnt DESC",
            (cutoff,),
        ).fetchall()
    return {r["event_type"]: r["cnt"] for r in rows}


def get_engagement_stats() -> dict:
    """Compute DAU, WAU, MAU, avg gens/user, one-and-done."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    d1 = (now - timedelta(days=1)).isoformat()
    d7 = (now - timedelta(days=7)).isoformat()
    d30 = (now - timedelta(days=30)).isoformat()
    d14 = (now - timedelta(days=14)).isoformat()
    with _conn() as conn:
        dau = conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM generations WHERE created_at>=?", (d1,)
        ).fetchone()[0]
        wau = conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM generations WHERE created_at>=?", (d7,)
        ).fetchone()[0]
        mau = conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM generations WHERE created_at>=?", (d30,)
        ).fetchone()[0]
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_gens = conn.execute("SELECT COUNT(*) FROM generations").fetchone()[0]
        avg_gens = round(total_gens / max(total_users, 1), 1)
        zero_gens = conn.execute(
            """SELECT COUNT(*) FROM users u WHERE NOT EXISTS
               (SELECT 1 FROM generations g WHERE g.user_id=u.id)"""
        ).fetchone()[0]
        one_and_done = conn.execute(
            """SELECT COUNT(*) FROM users u
               WHERE (SELECT COUNT(*) FROM generations g WHERE g.user_id=u.id)=1
               AND u.created_at < ?""",
            (d14,),
        ).fetchone()[0]
    return {
        "dau": dau, "wau": wau, "mau": mau,
        "total_users": total_users,
        "total_gens": total_gens,
        "avg_gens_per_user": avg_gens,
        "users_with_zero_gens": zero_gens,
        "one_and_done_users": one_and_done,
    }


# ─── Agent actions ─────────────────────────────────────────────────────────────

def log_agent_action(agent_name: str, action_type: str, description: str) -> str:
    """Log an agent action. Returns the action ID."""
    aid = str(uuid.uuid4())
    with _conn() as conn:
        conn.execute(
            """INSERT INTO agent_actions (id, agent_name, action_type, description, status, created_at)
               VALUES (?,?,?,?,?,?)""",
            (aid, agent_name, action_type, description, "pending",
             datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    return aid


def list_agent_actions(status: str = None, agent_name: str = None, limit: int = 100) -> list[dict]:
    """List agent actions with optional filters."""
    query = "SELECT * FROM agent_actions WHERE 1=1"
    params: list = []
    if status:
        query += " AND status=?"
        params.append(status)
    if agent_name:
        query += " AND agent_name=?"
        params.append(agent_name)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def resolve_agent_action(action_id: str, status: str, marcos_notes: str = "") -> bool:
    """Approve or reject an agent action. Returns True if found."""
    with _conn() as conn:
        cur = conn.execute(
            "UPDATE agent_actions SET status=?, marcos_notes=?, resolved_at=? WHERE id=?",
            (status, marcos_notes, datetime.now(timezone.utc).isoformat(), action_id),
        )
        conn.commit()
    return cur.rowcount > 0


def get_agent_action_summary() -> dict:
    """Summary of agent actions by status and agent."""
    with _conn() as conn:
        pending = conn.execute("SELECT COUNT(*) FROM agent_actions WHERE status='pending'").fetchone()[0]
        approved_7d = conn.execute(
            "SELECT COUNT(*) FROM agent_actions WHERE status='approved' AND resolved_at>=?",
            ((datetime.now(timezone.utc) - __import__("datetime").timedelta(days=7)).isoformat(),),
        ).fetchone()[0]
        rejected_7d = conn.execute(
            "SELECT COUNT(*) FROM agent_actions WHERE status='rejected' AND resolved_at>=?",
            ((datetime.now(timezone.utc) - __import__("datetime").timedelta(days=7)).isoformat(),),
        ).fetchone()[0]
        by_agent = conn.execute(
            "SELECT agent_name, status, COUNT(*) as cnt FROM agent_actions GROUP BY agent_name, status"
        ).fetchall()
        pending_items = conn.execute(
            "SELECT * FROM agent_actions WHERE status='pending' ORDER BY created_at DESC LIMIT 20"
        ).fetchall()
    by_agent_dict: dict = {}
    for r in by_agent:
        name = r["agent_name"]
        if name not in by_agent_dict:
            by_agent_dict[name] = {}
        by_agent_dict[name][r["status"]] = r["cnt"]
    return {
        "pending": pending,
        "approved_last_7d": approved_7d,
        "rejected_last_7d": rejected_7d,
        "by_agent": by_agent_dict,
        "pending_actions": [dict(r) for r in pending_items],
    }


def has_pending_action(agent_name: str, action_type: str) -> bool:
    """Check if an agent already has a pending action of this type."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM agent_actions WHERE agent_name=? AND action_type=? AND status='pending'",
            (agent_name, action_type),
        ).fetchone()
    return row[0] > 0 if row else False


# ─── Intelligence: snapshots, churn, funnel, quality ──────────────────────────

def take_daily_snapshot() -> None:
    """Compute and store today's metrics snapshot."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    d7 = (now - timedelta(days=7)).isoformat()
    with _conn() as conn:
        existing = conn.execute("SELECT id FROM daily_snapshots WHERE snapshot_date=?", (today,)).fetchone()
        if existing:
            return
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_gens = conn.execute("SELECT COUNT(*) FROM generations").fetchone()[0]
        total_cost = conn.execute("SELECT COALESCE(SUM(cost_estimate),0) FROM generations").fetchone()[0]
        active_7d = conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM generations WHERE created_at>=?", (d7,)
        ).fetchone()[0]
        signups_today = conn.execute(
            "SELECT COUNT(*) FROM users WHERE created_at>=?", (today_start,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO daily_snapshots (id, snapshot_date, total_users, total_gens, total_cost, active_users_7d, signups_today, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (str(uuid.uuid4()), today, total_users, total_gens, total_cost, active_7d, signups_today, now.isoformat()),
        )
        conn.commit()


def get_daily_snapshots(days: int = 30) -> list[dict]:
    """Get last N days of snapshots."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM daily_snapshots ORDER BY snapshot_date DESC LIMIT ?", (days,),
        ).fetchall()
    return [dict(r) for r in rows]


def compute_churn_risk_scores() -> list[dict]:
    """Identify paying users at risk of churning. Returns sorted by risk score desc."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    d7 = (now - timedelta(days=7)).isoformat()
    d14 = (now - timedelta(days=14)).isoformat()
    d30 = (now - timedelta(days=30)).isoformat()
    with _conn() as conn:
        paying = conn.execute(
            "SELECT * FROM users WHERE subscription_tier IN ('pro','founding_member')"
        ).fetchall()
    at_risk = []
    for user in paying:
        uid = user["id"]
        with _conn() as conn:
            last_gen = conn.execute(
                "SELECT created_at FROM generations WHERE user_id=? ORDER BY created_at DESC LIMIT 1",
                (uid,),
            ).fetchone()
            gens_7d = conn.execute(
                "SELECT COUNT(*) FROM generations WHERE user_id=? AND created_at>=?",
                (uid, d7),
            ).fetchone()[0]
            gens_prev_7d = conn.execute(
                "SELECT COUNT(*) FROM generations WHERE user_id=? AND created_at>=? AND created_at<?",
                (uid, d14, d7),
            ).fetchone()[0]
            total_gens = conn.execute(
                "SELECT COUNT(*) FROM generations WHERE user_id=?", (uid,),
            ).fetchone()[0]
            has_issues = conn.execute(
                "SELECT COUNT(*) FROM feedback WHERE user_id=? AND rating='issues' AND reviewed=0",
                (uid,),
            ).fetchone()[0]
        score = 0
        reasons = []
        if last_gen:
            days_inactive = (now - datetime.fromisoformat(last_gen["created_at"])).days
            if days_inactive > 14:
                score += min(40, days_inactive)
                reasons.append(f"No activity in {days_inactive} days")
        else:
            days_since_signup = (now - datetime.fromisoformat(user["created_at"])).days
            score += 30
            reasons.append(f"Never generated ({days_since_signup} days since signup)")
        if gens_prev_7d > 0 and gens_7d < gens_prev_7d:
            score += 30
            reasons.append(f"Declining usage: {gens_prev_7d}→{gens_7d} gens/week")
        tier_limit = TIER_LIMITS.get(user["subscription_tier"], 20)
        if total_gens >= tier_limit * 0.8:
            score += 20
            reasons.append(f"Approaching tier limit ({total_gens}/{tier_limit})")
        if has_issues > 0:
            score += 10
            reasons.append(f"{has_issues} unresolved 'issues' feedback")
        if score >= 60:
            level = "critical"
        elif score >= 40:
            level = "high"
        elif score >= 20:
            level = "medium"
        else:
            level = "low"
        if score >= 20:
            at_risk.append({
                "user_id": uid,
                "email": user["email"],
                "tier": user["subscription_tier"],
                "risk_score": min(score, 100),
                "risk_level": level,
                "reasons": reasons,
                "last_generation": last_gen["created_at"] if last_gen else None,
                "total_gens": total_gens,
            })
    at_risk.sort(key=lambda x: x["risk_score"], reverse=True)
    return at_risk


def get_engagement_funnel() -> dict:
    """Compute signup → activation → engagement → power → paid funnel."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    d30 = (now - timedelta(days=30)).isoformat()
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        activated = conn.execute(
            """SELECT COUNT(DISTINCT u.id) FROM users u
               WHERE EXISTS (SELECT 1 FROM generations g WHERE g.user_id=u.id)"""
        ).fetchone()[0]
        engaged = conn.execute(
            """SELECT COUNT(*) FROM (
                   SELECT user_id FROM generations GROUP BY user_id HAVING COUNT(*)>=3
               )"""
        ).fetchone()[0]
        power = conn.execute(
            """SELECT COUNT(*) FROM (
                   SELECT user_id FROM generations GROUP BY user_id HAVING COUNT(*)>=10
               )"""
        ).fetchone()[0]
        paid = conn.execute(
            "SELECT COUNT(*) FROM users WHERE subscription_tier IN ('pro','founding_member','school')"
        ).fetchone()[0]
    def pct(n): return round(n / max(total, 1) * 100, 1)
    return {
        "stages": [
            {"name": "Signed Up", "count": total, "pct": 100.0},
            {"name": "Activated (1+ gen)", "count": activated, "pct": pct(activated)},
            {"name": "Engaged (3+ gens)", "count": engaged, "pct": pct(engaged)},
            {"name": "Power User (10+)", "count": power, "pct": pct(power)},
            {"name": "Paid Subscriber", "count": paid, "pct": pct(paid)},
        ]
    }


def get_content_quality_signals() -> dict:
    """Analyze feedback for content quality patterns."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    d30 = (now - timedelta(days=30)).isoformat()
    with _conn() as conn:
        recent_fb = conn.execute(
            "SELECT * FROM feedback WHERE created_at>=?", (d30,)
        ).fetchall()
        total = len(recent_fb)
        if total == 0:
            return {"period": "last_30_days", "total_feedback": 0, "issue_rate_pct": 0,
                    "rating_distribution": {}, "top_issue_tags": [],
                    "grammar_quality": [], "l1_quality": []}
        perfect = sum(1 for r in recent_fb if r["rating"] == "perfect")
        good = sum(1 for r in recent_fb if r["rating"] == "good")
        issues = sum(1 for r in recent_fb if r["rating"] == "issues")
        tag_counts: dict = {}
        for r in recent_fb:
            if r["rating"] == "issues" and r["tags"]:
                for t in r["tags"].split(","):
                    t = t.strip()
                    if t:
                        tag_counts[t] = tag_counts.get(t, 0) + 1
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        grammar_stats: dict = {}
        for r in recent_fb:
            if r["material_id"]:
                mat = conn.execute("SELECT grammar_point, l1_languages FROM materials WHERE id=?", (r["material_id"],)).fetchone()
                if mat:
                    gp = mat["grammar_point"]
                    if gp not in grammar_stats:
                        grammar_stats[gp] = {"gens": 0, "issues": 0}
                    grammar_stats[gp]["gens"] += 1
                    if r["rating"] == "issues":
                        grammar_stats[gp]["issues"] += 1
        grammar_quality = sorted(
            [{"grammar": k, "gens": v["gens"], "issues": v["issues"],
              "issue_rate": round(v["issues"] / max(v["gens"], 1) * 100, 1)}
             for k, v in grammar_stats.items()],
            key=lambda x: x["issue_rate"], reverse=True
        )[:10]
        l1_stats: dict = {}
        for r in recent_fb:
            if r["material_id"]:
                mat = conn.execute("SELECT l1_languages FROM materials WHERE id=?", (r["material_id"],)).fetchone()
                if mat and mat["l1_languages"]:
                    l1 = mat["l1_languages"]
                    if l1 not in l1_stats:
                        l1_stats[l1] = {"gens": 0, "issues": 0}
                    l1_stats[l1]["gens"] += 1
                    if r["rating"] == "issues":
                        l1_stats[l1]["issues"] += 1
        l1_quality = sorted(
            [{"l1": k, "gens": v["gens"], "issues": v["issues"],
              "issue_rate": round(v["issues"] / max(v["gens"], 1) * 100, 1)}
             for k, v in l1_stats.items()],
            key=lambda x: x["issue_rate"], reverse=True
        )[:10]
    return {
        "period": "last_30_days",
        "total_feedback": total,
        "rating_distribution": {"perfect": perfect, "good": good, "issues": issues},
        "issue_rate_pct": round(issues / total * 100, 1),
        "top_issue_tags": [{"tag": t, "count": c} for t, c in top_tags],
        "grammar_quality": grammar_quality,
        "l1_quality": l1_quality,
    }


# ─── Daily digest ──────────────────────────────────────────────────────────────

def save_daily_digest(content_json: str) -> None:
    """Store a generated digest."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO daily_digests (id, digest_date, content_json, created_at) VALUES (?,?,?,?)",
            (str(uuid.uuid4()), today, content_json, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()


def get_latest_digest() -> Optional[dict]:
    """Get the most recent digest."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM daily_digests ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


# ─── Orchestrator operations (Phase I-3) ───────────────────────────────────────

def create_orchestrator_run(run_type: str = "scheduled") -> str:
    """Create a new orchestrator run record. Returns the run ID."""
    run_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO orchestrator_runs (id, run_type, status, started_at) VALUES (?,?,?,?)",
            (run_id, run_type, "running", now),
        )
        conn.commit()
    return run_id


def complete_orchestrator_run(run_id: str, agents_run: str = "[]",
                              critical_alerts: int = 0, error_message: str = "") -> None:
    """Mark an orchestrator run as completed."""
    now = datetime.now(timezone.utc).isoformat()
    status = "failed" if error_message else "completed"
    with _conn() as conn:
        conn.execute(
            "UPDATE orchestrator_runs SET status=?, completed_at=?, agents_run=?, critical_alerts=?, error_message=? WHERE id=?",
            (status, now, agents_run, critical_alerts, error_message, run_id),
        )
        conn.commit()


def get_orchestrator_status() -> Optional[dict]:
    """Get the most recent orchestrator run."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM orchestrator_runs ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def get_orchestrator_history(limit: int = 30) -> list[dict]:
    """Get recent orchestrator runs."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM orchestrator_runs ORDER BY started_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


# ─── Agent health operations (Phase I-3) ───────────────────────────────────────

def init_agent_health(agent_name: str) -> None:
    """Initialize health record for an agent (idempotent)."""
    with _conn() as conn:
        existing = conn.execute("SELECT agent_name FROM agent_health WHERE agent_name=?", (agent_name,)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO agent_health (agent_name, status) VALUES (?, 'unknown')",
                (agent_name,),
            )
            conn.commit()


def update_agent_health(agent_name: str, success: bool, runtime_seconds: float = 0) -> None:
    """Update health record after an agent run."""
    now = datetime.now(timezone.utc).isoformat()
    init_agent_health(agent_name)
    with _conn() as conn:
        row = conn.execute("SELECT * FROM agent_health WHERE agent_name=?", (agent_name,)).fetchone()
        if row:
            consecutive = 0 if success else (row["consecutive_failures"] + 1)
            total = row["total_runs"] + 1
            avg_rt = ((row["avg_runtime_seconds"] * row["total_runs"]) + runtime_seconds) / total
            if consecutive == 0:
                status = "healthy"
            elif consecutive <= 2:
                status = "degraded"
            else:
                status = "failing"
            conn.execute(
                """UPDATE agent_health SET last_run_at=?, last_success_at=?,
                   consecutive_failures=?, avg_runtime_seconds=?, total_runs=?, status=?
                   WHERE agent_name=?""",
                (now, now if success else row["last_success_at"], consecutive,
                 round(avg_rt, 1), total, status, agent_name),
            )
            conn.commit()


def get_all_agent_health() -> list[dict]:
    """Get health status for all agents."""
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM agent_health ORDER BY agent_name").fetchall()
    return [dict(r) for r in rows]


# ─── Agent message operations (Phase I-3) ──────────────────────────────────────

def create_agent_message(from_agent: str, to_agent: str, message_type: str,
                          payload: str = "{}") -> str:
    """Create an inter-agent message. Returns message ID."""
    msg_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO agent_messages (id, from_agent, to_agent, message_type, payload, created_at) VALUES (?,?,?,?,?,?)",
            (msg_id, from_agent, to_agent, message_type, payload, now),
        )
        conn.commit()
    return msg_id


def get_pending_agent_messages(agent_name: str, limit: int = 20) -> list[dict]:
    """Get pending messages for a specific agent."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM agent_messages WHERE to_agent=? AND processed=0 ORDER BY created_at ASC LIMIT ?",
            (agent_name, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def ack_agent_message(msg_id: str) -> None:
    """Mark an inter-agent message as processed."""
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "UPDATE agent_messages SET processed=1, processed_at=? WHERE id=?",
            (now, msg_id),
        )
        conn.commit()


# ─── Agent cost operations (Phase I-3) ────────────────────────────────────────

def log_agent_cost(agent_name: str, estimated_cost_usd: float = 0,
                    tokens_input: int = 0, tokens_output: int = 0,
                    model_used: str = "", action_id: str = "") -> str:
    """Log the cost of an agent action. Returns cost record ID."""
    cost_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO agent_costs (id, agent_name, action_id, estimated_cost_usd, tokens_input, tokens_output, model_used, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (cost_id, agent_name, action_id, estimated_cost_usd, tokens_input, tokens_output, model_used, now),
        )
        conn.commit()
    return cost_id


def get_daily_agent_costs() -> list[dict]:
    """Get today's costs broken down by agent."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with _conn() as conn:
        rows = conn.execute(
            """SELECT agent_name,
                      COALESCE(SUM(estimated_cost_usd), 0) as total_cost,
                      COALESCE(SUM(tokens_input), 0) as total_input_tokens,
                      COALESCE(SUM(tokens_output), 0) as total_output_tokens,
                      COUNT(*) as action_count
               FROM agent_costs
               WHERE created_at >= ?
               GROUP BY agent_name
               ORDER BY total_cost DESC""",
            (today,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_weekly_agent_costs() -> list[dict]:
    """Get 7-day cost trend."""
    from datetime import timedelta
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    with _conn() as conn:
        rows = conn.execute(
            """SELECT DATE(created_at) as day,
                      COALESCE(SUM(estimated_cost_usd), 0) as total_cost,
                      COUNT(*) as action_count
               FROM agent_costs
               WHERE created_at >= ?
               GROUP BY DATE(created_at)
               ORDER BY day DESC""",
            (week_ago,),
        ).fetchall()
    return [dict(r) for r in rows]


# ─── Critical alert operations (Phase I-8) ─────────────────────────────────────

def create_critical_alert(alert_type: str, severity: str, description: str,
                           details_json: str = "{}") -> str:
    """Create a critical alert. Returns alert ID."""
    alert_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO critical_alerts (id, alert_type, severity, description, details_json, created_at) VALUES (?,?,?,?,?,?)",
            (alert_id, alert_type, severity, description, details_json, now),
        )
        conn.commit()
    return alert_id


def get_active_alerts() -> list[dict]:
    """Get all unresolved critical alerts."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM critical_alerts WHERE resolved=0 ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def acknowledge_alert(alert_id: str) -> None:
    """Marcos acknowledges an alert."""
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "UPDATE critical_alerts SET acknowledged=1, acknowledged_at=? WHERE id=?",
            (now, alert_id),
        )
        conn.commit()


def resolve_alert(alert_id: str, marcos_notes: str = "") -> None:
    """Marcos resolves an alert."""
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            "UPDATE critical_alerts SET resolved=1, resolved_at=?, marcos_notes=? WHERE id=?",
            (now, marcos_notes, alert_id),
        )
        conn.commit()
