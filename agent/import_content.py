"""
Import Grammar & L1 Interference YAML files into CogniESL Database

Usage:
    python -m agent.import_content
    
Imports all YAML files from /data/grammar/ and /data/l1-interference/
into the SQLite database tables created by db_schema.init_content_db().
"""
import sqlite3
import yaml
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def _get_db_path() -> Path:
    """Get database path."""
    import os
    preferred = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data"))
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        return preferred / "cogniesl.db"
    except (PermissionError, OSError):
        fallback = Path(__file__).parent.parent / "data" / "cogniesl.db"
        return fallback


def _get_data_dir() -> Path:
    """Get static data directory."""
    import os
    env_path = os.getenv("COGNIESL_STATIC_DIR")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[2] / "data"


def import_grammar_files(conn: sqlite3.Connection, data_dir: Path) -> int:
    """Import all grammar YAML files. Returns count imported."""
    grammar_dir = data_dir / "grammar"
    if not grammar_dir.exists():
        print(f"✗ Grammar directory not found: {grammar_dir}")
        return 0

    yaml_files = sorted(grammar_dir.glob("*.yaml"))
    print(f"Found {len(yaml_files)} grammar files")

    imported = 0
    skipped = 0

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or not isinstance(data, dict):
                print(f"  ⚠ Skipping {yaml_file.name} (empty or invalid)")
                skipped += 1
                continue

            grammar_id = str(uuid.uuid4())
            title = data.get("title", yaml_file.stem)
            level = data.get("level", "")
            description = data.get("description", "")
            core_meaning = data.get("meaning", {}).get("core_meaning", "")

            # Store raw YAML for reference
            raw_yaml = yaml_file.read_text(encoding="utf-8")
            imported_at = datetime.now(timezone.utc).isoformat()

            conn.execute("""
                INSERT OR REPLACE INTO grammar_points
                (id, title, level, description, core_meaning, raw_yaml, imported_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (grammar_id, title, level, description, core_meaning, raw_yaml, imported_at))

            # Import common errors
            common_errors = data.get("common_errors", [])
            for idx, error_data in enumerate(common_errors):
                error_id = str(uuid.uuid4())
                l1_groups = ", ".join(error_data.get("l1_groups", []))
                conn.execute("""
                    INSERT INTO grammar_errors
                    (id, grammar_id, error, correction, explanation, l1_groups, reliability)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    error_id,
                    grammar_id,
                    error_data.get("error", ""),
                    error_data.get("correction", ""),
                    error_data.get("explanation", ""),
                    l1_groups,
                    error_data.get("reliability", "")
                ))

            imported += 1
            if imported % 50 == 0:
                print(f"  ✓ Imported {imported} grammar files...")

        except Exception as e:
            print(f"  ✗ Error importing {yaml_file.name}: {str(e)}")
            skipped += 1

    conn.commit()
    print(f"✓ Grammar import complete: {imported} imported, {skipped} skipped")
    return imported


def import_l1_interference_files(conn: sqlite3.Connection, data_dir: Path) -> int:
    """Import all L1 interference YAML files. Returns count imported."""
    l1_dir = data_dir / "l1-interference"
    if not l1_dir.exists():
        print(f"✗ L1 interference directory not found: {l1_dir}")
        return 0

    yaml_files = sorted(l1_dir.glob("*.yaml"))
    print(f"Found {len(yaml_files)} L1 interference files")

    imported = 0
    skipped = 0

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or not isinstance(data, dict):
                print(f"  ⚠ Skipping {yaml_file.name} (empty or invalid)")
                skipped += 1
                continue

            l1_id = str(uuid.uuid4())
            language = data.get("language", yaml_file.stem)
            l1_code = data.get("l1", "")
            total_grammar_points = data.get("total_grammar_points", 0)

            raw_yaml = yaml_file.read_text(encoding="utf-8")
            imported_at = datetime.now(timezone.utc).isoformat()

            conn.execute("""
                INSERT OR REPLACE INTO l1_interference
                (id, language, l1_code, total_grammar_points, raw_yaml, imported_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (l1_id, language, l1_code, total_grammar_points, raw_yaml, imported_at))

            # Import grammar points with interference patterns
            grammar_points = data.get("grammar_points", {})
            for grammar_slug, grammar_data in grammar_points.items():
                if not isinstance(grammar_data, dict):
                    continue

                interference_patterns = grammar_data.get("interference_patterns", [])
                for idx, pattern_data in enumerate(interference_patterns):
                    pattern_id = str(uuid.uuid4())
                    conn.execute("""
                        INSERT INTO l1_patterns
                        (id, l1_id, grammar_point, pattern, frequency, persistence,
                         communicative_impact, example_wrong, example_correct, explanation)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pattern_id,
                        l1_id,
                        grammar_slug,
                        pattern_data.get("pattern", ""),
                        pattern_data.get("frequency"),
                        pattern_data.get("persistence"),
                        pattern_data.get("communicative_impact"),
                        pattern_data.get("example_wrong", ""),
                        pattern_data.get("example_correct", ""),
                        pattern_data.get("explanation", "")
                    ))

            imported += 1
            if imported % 10 == 0:
                print(f"  ✓ Imported {imported} L1 files...")

        except Exception as e:
            print(f"  ✗ Error importing {yaml_file.name}: {str(e)}")
            skipped += 1

    conn.commit()
    print(f"✓ L1 interference import complete: {imported} imported, {skipped} skipped")
    return imported


def run_import() -> None:
    """Main import function."""
    print("=" * 60)
    print("CogniESL Content Import")
    print("=" * 60)

    db_path = _get_db_path()
    data_dir = _get_data_dir()

    print(f"Database: {db_path}")
    print(f"Data dir: {data_dir}")
    print()

    # Initialize schema first
    from agent.db_schema import init_content_db
    init_content_db()

    # Open connection and import
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        print("\n--- IMPORTING GRAMMAR ---")
        grammar_count = import_grammar_files(conn, data_dir)

        print("\n--- IMPORTING L1 INTERFERENCE ---")
        l1_count = import_l1_interference_files(conn, data_dir)

    print("\n" + "=" * 60)
    print(f"Import Summary: {grammar_count} grammar + {l1_count} L1 files")
    print("=" * 60)


if __name__ == "__main__":
    run_import()
