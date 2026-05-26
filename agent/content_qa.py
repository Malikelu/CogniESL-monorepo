"""Content QA Agent — detects forge updates and proposes syncs.

Compares forge/data/ against CogniESL/data/ to identify:
1. Grammar files that have been updated in forge but not synced to production
2. L1 interference files with new/updated interference patterns
3. Activity templates with new content

Never auto-applies. Creates agent_actions for Marcos to review and approve.
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from auth import db as auth_db

log = logging.getLogger("content_qa")

# Paths
FORGE_DATA_DIR = Path(_root).parent / "forge" / "data"
COGNIESL_DATA_DIR = Path(_root) / "data"

# Subdirectories to monitor
MONITORED_DIRS = {
    "grammar": "grammar",
    "l1_interference": "l1-interference",
    "activities": "activities",
}


def _get_file_hash(filepath: Path) -> str:
    """Get a simple hash of a file's content for change detection."""
    import hashlib
    if not filepath.exists():
        return ""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _load_yaml_safe(filepath: Path) -> dict:
    """Load a YAML file safely. Returns empty dict on failure."""
    try:
        import yaml
        with open(filepath) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _detect_grammar_updates() -> list:
    """Compare forge grammar files against production. Returns list of updates."""
    updates = []
    forge_grammar = FORGE_DATA_DIR / "grammar"
    prod_grammar = COGNIESL_DATA_DIR / "grammar"

    if not forge_grammar.exists():
        log.warning(f"Forge grammar dir not found: {forge_grammar}")
        return updates

    for forge_file in forge_grammar.glob("*.yaml"):
        prod_file = prod_grammar / forge_file.name
        if not prod_file.exists():
            updates.append({
                "type": "new_file",
                "file": forge_file.name,
                "category": "grammar",
                "description": f"New grammar file in forge: {forge_file.name}",
            })
            continue

        # Compare content hashes
        forge_hash = _get_file_hash(forge_file)
        prod_hash = _get_file_hash(prod_file)
        if forge_hash != prod_hash:
            # Check what changed
            forge_data = _load_yaml_safe(forge_file)
            prod_data = _load_yaml_safe(prod_file)

            changes = []
            for key in set(list(forge_data.keys()) + list(prod_data.keys())):
                if key not in prod_data:
                    changes.append(f"New section: {key}")
                elif key not in forge_data:
                    changes.append(f"Removed section: {key}")
                elif forge_data[key] != prod_data[key]:
                    changes.append(f"Updated: {key}")

            if changes:
                updates.append({
                    "type": "updated",
                    "file": forge_file.name,
                    "category": "grammar",
                    "description": f"Grammar update: {forge_file.name} — {', '.join(changes[:3])}",
                    "changes": changes,
                })

    return updates


def _detect_l1_updates() -> list:
    """Compare forge L1 files against production. Returns list of updates."""
    updates = []
    forge_l1 = FORGE_DATA_DIR / "l1_interference"
    prod_l1 = COGNIESL_DATA_DIR / "l1-interference"

    if not forge_l1.exists():
        log.warning(f"Forge L1 dir not found: {forge_l1}")
        return updates

    for forge_file in forge_l1.glob("*.yaml"):
        prod_file = prod_l1 / forge_file.name
        if not prod_file.exists():
            updates.append({
                "type": "new_file",
                "file": forge_file.name,
                "category": "l1_interference",
                "description": f"New L1 file in forge: {forge_file.name}",
            })
            continue

        forge_hash = _get_file_hash(forge_file)
        prod_hash = _get_file_hash(prod_file)
        if forge_hash != prod_hash:
            forge_data = _load_yaml_safe(forge_file)
            prod_data = _load_yaml_safe(prod_file)

            # Count interference patterns
            forge_patterns = len(forge_data.get("interference_patterns", []))
            prod_patterns = len(prod_data.get("interference_patterns", []))

            changes = []
            if forge_patterns != prod_patterns:
                changes.append(f"Patterns: {prod_patterns} → {forge_patterns}")

            for key in set(list(forge_data.keys()) + list(prod_data.keys())):
                if key == "interference_patterns":
                    continue
                if key not in prod_data:
                    changes.append(f"New: {key}")
                elif key not in forge_data:
                    changes.append(f"Removed: {key}")
                elif forge_data[key] != prod_data[key]:
                    changes.append(f"Updated: {key}")

            if changes:
                updates.append({
                    "type": "updated",
                    "file": forge_file.name,
                    "category": "l1_interference",
                    "description": f"L1 update: {forge_file.name} — {', '.join(changes[:3])}",
                    "changes": changes,
                })

    return updates


def _detect_activity_updates() -> list:
    """Compare forge activity files against production. Returns list of updates."""
    updates = []
    forge_activities = FORGE_DATA_DIR / "activities"
    prod_activities = COGNIESL_DATA_DIR / "activities"

    if not forge_activities.exists():
        return updates

    for forge_file in forge_activities.glob("*.yaml"):
        prod_file = prod_activities / forge_file.name
        if not prod_file.exists():
            updates.append({
                "type": "new_file",
                "file": forge_file.name,
                "category": "activities",
                "description": f"New activity file in forge: {forge_file.name}",
            })
            continue

        forge_hash = _get_file_hash(forge_file)
        prod_hash = _get_file_hash(prod_file)
        if forge_hash != prod_hash:
            updates.append({
                "type": "updated",
                "file": forge_file.name,
                "category": "activities",
                "description": f"Activity update: {forge_file.name}",
            })

    return updates


def _identify_poor_combinations() -> list:
    """Identify grammar+L1 combinations with poor feedback scores."""
    try:
        with auth_db._conn() as conn:
            # Get combinations with high issue rates
            rows = conn.execute("""
                SELECT m.grammar_point, m.l1_languages,
                       COUNT(f.id) as total_feedback,
                       SUM(CASE WHEN f.rating = 'issues' THEN 1 ELSE 0 END) as issue_count
                FROM feedback f
                JOIN materials m ON m.id = f.material_id
                WHERE m.grammar_point != '' AND m.l1_languages != ''
                GROUP BY m.grammar_point, m.l1_languages
                HAVING total_feedback >= 2
                ORDER BY (CAST(issue_count AS REAL) / total_feedback) DESC
                LIMIT 10
            """).fetchall()

        results = []
        for row in rows:
            issue_rate = row["issue_count"] / max(row["total_feedback"], 1) * 100
            if issue_rate > 20:  # More than 20% issues
                results.append({
                    "grammar": row["grammar_point"],
                    "l1": row["l1_languages"],
                    "total_feedback": row["total_feedback"],
                    "issue_count": row["issue_count"],
                    "issue_rate": round(issue_rate, 1),
                })
        return results
    except Exception:
        return []


def run_content_qa() -> dict:
    """Run Content QA check. Returns result dict with proposed syncs."""
    log.info("Content QA starting...")

    grammar_updates = _detect_grammar_updates()
    l1_updates = _detect_l1_updates()
    activity_updates = _detect_activity_updates()
    poor_combos = _identify_poor_combinations()

    all_updates = grammar_updates + l1_updates + activity_updates

    # Log each update as an agent_action for Marcos to review
    action_ids = []
    for update in all_updates:
        try:
            action_id = auth_db.log_agent_action(
                "ContentQA", "sync_proposed",
                f"[{update['category']}] {update['description']}"
            )
            action_ids.append(action_id)
        except Exception:
            pass

    # Log poor combinations
    for combo in poor_combos:
        try:
            auth_db.log_agent_action(
                "ContentQA", "poor_quality",
                f"Poor feedback: {combo['grammar']} + {combo['l1']} — "
                f"{combo['issue_rate']}% issue rate ({combo['issue_count']}/{combo['total_feedback']})"
            )
        except Exception:
            pass

    result = {
        "type": "content_qa_report",
        "updates_found": len(all_updates),
        "grammar_updates": grammar_updates,
        "l1_updates": l1_updates,
        "activity_updates": activity_updates,
        "poor_combinations": poor_combos,
        "action_ids": action_ids,
    }

    log.info(f"Content QA completed: {len(all_updates)} updates found, {len(poor_combos)} poor combos")
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
    result = run_content_qa()
    print(json.dumps(result, indent=2, default=str))
