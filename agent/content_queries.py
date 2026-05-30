"""
Query functions for Grammar & L1 Interference from database.

Provides read-only access to imported grammar and L1 content.
"""
import sqlite3
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List


def _get_db_path() -> Path:
    """Get database path."""
    preferred = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data"))
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        return preferred / "cogniesl.db"
    except (PermissionError, OSError):
        fallback = Path(__file__).parent.parent / "data" / "cogniesl.db"
        return fallback


def get_grammar_by_title(title: str) -> Optional[Dict[str, Any]]:
    """Get a grammar point by title."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM grammar_points WHERE LOWER(title) = LOWER(?)",
                (title,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
    except Exception as e:
        print(f"Error querying grammar: {e}")
    return None


def get_grammar_errors_for_point(grammar_id: str) -> List[Dict[str, Any]]:
    """Get all common errors for a grammar point."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM grammar_errors WHERE grammar_id = ?",
                (grammar_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error querying grammar errors: {e}")
    return []


def get_l1_by_language(language: str) -> Optional[Dict[str, Any]]:
    """Get L1 interference data by language name."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM l1_interference WHERE LOWER(language) = LOWER(?)",
                (language,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
    except Exception as e:
        print(f"Error querying L1: {e}")
    return None


def get_l1_patterns_for_grammar(l1_id: str, grammar_point: str) -> List[Dict[str, Any]]:
    """Get interference patterns for a specific L1 and grammar point."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM l1_patterns 
                   WHERE l1_id = ? AND LOWER(grammar_point) = LOWER(?)
                   ORDER BY frequency DESC, persistence DESC""",
                (l1_id, grammar_point)
            )
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error querying L1 patterns: {e}")
    return []


def get_all_l1_languages() -> List[str]:
    """Get list of all imported L1 languages."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.execute("SELECT language FROM l1_interference ORDER BY language")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error querying L1 languages: {e}")
    return []


def get_all_grammar_titles() -> List[str]:
    """Get list of all imported grammar titles."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.execute("SELECT title FROM grammar_points ORDER BY title")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error querying grammar titles: {e}")
    return []


def import_status() -> Dict[str, Any]:
    """Get import status (count of records)."""
    db_path = _get_db_path()
    try:
        with sqlite3.connect(str(db_path)) as conn:
            grammar_count = conn.execute("SELECT COUNT(*) FROM grammar_points").fetchone()[0]
            l1_count = conn.execute("SELECT COUNT(*) FROM l1_interference").fetchone()[0]
            error_count = conn.execute("SELECT COUNT(*) FROM grammar_errors").fetchone()[0]
            pattern_count = conn.execute("SELECT COUNT(*) FROM l1_patterns").fetchone()[0]

            return {
                "grammar_points": grammar_count,
                "l1_languages": l1_count,
                "grammar_errors": error_count,
                "l1_patterns": pattern_count,
                "db_path": str(db_path)
            }
    except Exception as e:
        return {"error": str(e)}
