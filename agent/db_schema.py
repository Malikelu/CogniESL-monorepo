"""
CogniESL Database Schema — Grammar & L1 Interference Tables

Creates tables for grammar points and L1 interference patterns.
Part of Phase 1: Database integration for curated content.
"""
import sqlite3
import os
from pathlib import Path


def _get_db_path() -> Path:
    """Get database path (same as auth/db.py)."""
    preferred = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data"))
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        return preferred / "cogniesl.db"
    except (PermissionError, OSError):
        fallback = Path(__file__).parent.parent / "data" / "cogniesl.db"
        return fallback


def init_content_db() -> None:
    """Create grammar, l1_interference, and related tables."""
    db_path = _get_db_path()
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        # Grammar Points Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grammar_points (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                level TEXT NOT NULL,
                description TEXT,
                core_meaning TEXT,
                raw_yaml TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                version INTEGER DEFAULT 1
            )
        """)

        # L1 Interference Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS l1_interference (
                id TEXT PRIMARY KEY,
                language TEXT NOT NULL,
                l1_code TEXT NOT NULL,
                total_grammar_points INTEGER,
                raw_yaml TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                version INTEGER DEFAULT 1
            )
        """)

        # L1 Interference Patterns (flattened for easy querying)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS l1_patterns (
                id TEXT PRIMARY KEY,
                l1_id TEXT NOT NULL,
                grammar_point TEXT NOT NULL,
                pattern TEXT NOT NULL,
                frequency INTEGER,
                persistence INTEGER,
                communicative_impact INTEGER,
                example_wrong TEXT,
                example_correct TEXT,
                explanation TEXT,
                FOREIGN KEY (l1_id) REFERENCES l1_interference(id)
            )
        """)

        # Grammar Common Errors (flattened for easy querying)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grammar_errors (
                id TEXT PRIMARY KEY,
                grammar_id TEXT NOT NULL,
                error TEXT NOT NULL,
                correction TEXT NOT NULL,
                explanation TEXT,
                l1_groups TEXT,
                reliability TEXT,
                FOREIGN KEY (grammar_id) REFERENCES grammar_points(id)
            )
        """)

        # Create indexes for fast lookup
        conn.execute("CREATE INDEX IF NOT EXISTS idx_grammar_title ON grammar_points(title)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_grammar_level ON grammar_points(level)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_l1_language ON l1_interference(language)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_l1_code ON l1_interference(l1_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_l1_patterns_grammar ON l1_patterns(grammar_point)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_grammar_errors_grammar ON grammar_errors(grammar_id)")

        conn.commit()
        print(f"✓ Database schema initialized at {db_path}")
