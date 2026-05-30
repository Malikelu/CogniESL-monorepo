"""
Targeted Update: Update a specific grammar or L1 interference YAML file in the DB.

Usage:
    python -m agent.update_content --type grammar --file ../data/grammar/present_simple.yaml
    python -m agent.update_content --type l1 --file ../data/l1-interference/spanish_interference.yaml

Matches existing records by title (grammar) or language (L1), then:
  - Replaces raw_yaml + metadata
  - Refreshes child rows (grammar_errors / l1_patterns)
  - Increments version
  - Rolls back on any error
"""
import argparse
import sqlite3
import uuid
import yaml
import sys
from pathlib import Path
from datetime import datetime, timezone


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


def update_grammar(conn: sqlite3.Connection, yaml_path: Path) -> bool:
    """Update a grammar point by title. Returns True on success."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or not isinstance(data, dict):
        print(f"  ✗ Invalid YAML: {yaml_path.name}")
        return False

    title = data.get("title", yaml_path.stem)
    print(f"  Title: {title}")

    # Find existing record
    row = conn.execute(
        "SELECT id, version FROM grammar_points WHERE title = ?", (title,)
    ).fetchone()

    if not row:
        print(f"  ✗ No existing grammar record found for '{title}'")
        return False

    grammar_id = row["id"]
    new_version = row["version"] + 1

    level = data.get("level", "")
    description = data.get("description", "")
    core_meaning = data.get("meaning", {}).get("core_meaning", "")
    raw_yaml = yaml_path.read_text(encoding="utf-8")
    imported_at = datetime.now(timezone.utc).isoformat()

    # Update main record
    conn.execute("""
        UPDATE grammar_points
        SET title = ?, level = ?, description = ?, core_meaning = ?,
            raw_yaml = ?, imported_at = ?, version = ?
        WHERE id = ?
    """, (title, level, description, core_meaning, raw_yaml, imported_at, new_version, grammar_id))

    # Delete old grammar_errors
    conn.execute("DELETE FROM grammar_errors WHERE grammar_id = ?", (grammar_id,))

    # Re-insert fresh errors
    common_errors = data.get("common_errors", [])
    for error_data in common_errors:
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

    print(f"  ✓ Updated → version {new_version}, {len(common_errors)} common errors")
    return True


def update_l1(conn: sqlite3.Connection, yaml_path: Path) -> bool:
    """Update an L1 interference record by language. Returns True on success."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or not isinstance(data, dict):
        print(f"  ✗ Invalid YAML: {yaml_path.name}")
        return False

    language = data.get("language", yaml_path.stem)
    l1_code = data.get("l1", "")
    print(f"  Language: {language} ({l1_code})")

    # Find existing record by language name (fallback to l1_code)
    row = conn.execute(
        "SELECT id, version FROM l1_interference WHERE language = ?", (language,)
    ).fetchone()

    if not row:
        row = conn.execute(
            "SELECT id, version FROM l1_interference WHERE l1_code = ?", (l1_code,)
        ).fetchone()

    if not row:
        print(f"  ✗ No existing L1 record found for '{language}'")
        return False

    l1_id = row["id"]
    new_version = row["version"] + 1

    total_grammar_points = data.get("total_grammar_points", 0)
    raw_yaml = yaml_path.read_text(encoding="utf-8")
    imported_at = datetime.now(timezone.utc).isoformat()

    # Update main record
    conn.execute("""
        UPDATE l1_interference
        SET language = ?, l1_code = ?, total_grammar_points = ?,
            raw_yaml = ?, imported_at = ?, version = ?
        WHERE id = ?
    """, (language, l1_code, total_grammar_points, raw_yaml, imported_at, new_version, l1_id))

    # Delete old l1_patterns
    conn.execute("DELETE FROM l1_patterns WHERE l1_id = ?", (l1_id,))

    # Re-insert fresh patterns
    grammar_points = data.get("grammar_points", {})
    total_patterns = 0
    for grammar_slug, grammar_data in grammar_points.items():
        if not isinstance(grammar_data, dict):
            continue

        interference_patterns = grammar_data.get("interference_patterns", [])
        for pattern_data in interference_patterns:
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
            total_patterns += 1

    print(f"  ✓ Updated → version {new_version}, {total_patterns} interference patterns across {len(grammar_points)} grammar points")
    return True


def main():
    parser = argparse.ArgumentParser(description="Update a specific YAML file in CogniESL DB")
    parser.add_argument("--type", required=True, choices=["grammar", "l1"],
                        help="Type of content: grammar or l1")
    parser.add_argument("--file", required=True,
                        help="Path to the YAML file")
    args = parser.parse_args()

    yaml_path = Path(args.file).resolve()
    if not yaml_path.exists():
        print(f"✗ File not found: {yaml_path}")
        sys.exit(1)

    print(f"= CogniESL Targeted Update =")
    print(f"  Type: {args.type}")
    print(f"  File: {yaml_path.name}")

    db_path = _get_db_path()
    print(f"  DB:   {db_path}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    try:
        if args.type == "grammar":
            success = update_grammar(conn, yaml_path)
        else:
            success = update_l1(conn, yaml_path)

        if success:
            conn.commit()
            print(f"\n✓ Update committed successfully")
        else:
            conn.rollback()
            print(f"\n✗ Update failed — rolled back")
            sys.exit(1)

    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
