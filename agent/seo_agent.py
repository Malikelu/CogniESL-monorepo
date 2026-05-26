"""SEO Content Agent — drafts blog posts from the CogniESL YAML database.

Reads grammar and L1 interference data to draft SEO-optimized blog posts
that help teachers understand common ESL errors. Queues drafts for Marcos approval.

Output: Creates agent_actions with draft content for review.
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

log = logging.getLogger("seo_agent")

DATA_DIR = Path(_root) / "data"


def _load_yaml_safe(filepath: Path) -> dict:
    """Load a YAML file safely. Returns empty dict on failure."""
    try:
        import yaml
        with open(filepath) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _get_top_grammar_points(limit: int = 5) -> list:
    """Get the most commonly requested grammar points from the database."""
    try:
        with auth_db._conn() as conn:
            rows = conn.execute("""
                SELECT grammar_point, COUNT(*) as cnt
                FROM generations
                WHERE grammar_point != ''
                GROUP BY grammar_point
                ORDER BY cnt DESC LIMIT ?
            """, (limit,)).fetchall()
        return [{"grammar": r["grammar_point"], "requests": r["cnt"]} for r in rows]
    except Exception:
        return []


def _get_top_l1_languages(limit: int = 5) -> list:
    """Get the most commonly requested L1 languages."""
    try:
        with auth_db._conn() as conn:
            rows = conn.execute("""
                SELECT l1_languages, COUNT(*) as cnt
                FROM generations
                WHERE l1_languages != ''
                GROUP BY l1_languages
                ORDER BY cnt DESC LIMIT ?
            """, (limit,)).fetchall()
        return [{"language": r["l1_languages"], "requests": r["cnt"]} for r in rows]
    except Exception:
        return []


def _get_grammar_data(grammar_point: str) -> dict:
    """Load grammar file data for a specific grammar point."""
    grammar_dir = DATA_DIR / "grammar"
    if not grammar_dir.exists():
        return {}

    # Try to find the file by name
    for f in grammar_dir.glob("*.yaml"):
        data = _load_yaml_safe(f)
        name = data.get("name", "") or data.get("grammar_point", "")
        if name.lower() == grammar_point.lower() or f.stem.lower() == grammar_point.lower().replace(" ", "_"):
            return data

    return {}


def _get_l1_data(language: str) -> dict:
    """Load L1 interference data for a specific language."""
    l1_dir = DATA_DIR / "l1-interference"
    if not l1_dir.exists():
        return {}

    for f in l1_dir.glob("*.yaml"):
        if language.lower() in f.stem.lower():
            return _load_yaml_safe(f)

    return {}


def _draft_blog_post(grammar_point: str, language: str, grammar_data: dict, l1_data: dict) -> dict:
    """Draft an SEO blog post for a grammar point + L1 combination."""
    title = f"Most Common {grammar_point} Errors for {language} ESL Students"

    # Extract key data
    meaning = grammar_data.get("meaning", {})
    core_meaning = meaning.get("core_meaning", "")
    ccqs = meaning.get("ccqs", [])

    form = grammar_data.get("form", {})
    affirmative = form.get("affirmative", "")
    negative = form.get("negative", "")
    questions = form.get("questions", "")

    common_errors = grammar_data.get("common_errors", [])

    # L1-specific patterns
    interference_patterns = l1_data.get("interference_patterns", [])
    teacher_tips = l1_data.get("teacher_tips", [])
    why_it_happens = l1_data.get("why_it_happens", "")

    # Build the draft
    sections = []

    sections.append(f"# {title}")
    sections.append("")
    sections.append(f"Teaching {grammar_point} to {language} speakers? Here are the most common errors your students will make — and exactly how to address them.")
    sections.append("")

    if core_meaning:
        sections.append(f"## What is {grammar_point}?")
        sections.append("")
        sections.append(core_meaning)
        sections.append("")

    if why_it_happens:
        sections.append(f"## Why {language} Students Struggle with {grammar_point}")
        sections.append("")
        sections.append(why_it_happens)
        sections.append("")

    if common_errors:
        sections.append("## Common Errors and How to Fix Them")
        sections.append("")
        for i, error in enumerate(common_errors[:5], 1):
            wrong = error.get("wrong", error) if isinstance(error, dict) else str(error)
            correct = error.get("correct", "") if isinstance(error, dict) else ""
            explanation = error.get("explanation", "") if isinstance(error, dict) else ""
            sections.append(f"### Error {i}")
            if wrong:
                sections.append(f"**Incorrect:** {wrong}")
            if correct:
                sections.append(f"**Correct:** {correct}")
            if explanation:
                sections.append(f"**Why:** {explanation}")
            sections.append("")

    if interference_patterns:
        sections.append(f"## {language}-Specific Interference Patterns")
        sections.append("")
        for pattern in interference_patterns[:5]:
            if isinstance(pattern, dict):
                desc = pattern.get("description", pattern.get("pattern", str(pattern)))
                freq = pattern.get("frequency", "")
                sections.append(f"- {desc}" + (f" (Frequency: {freq}/5)" if freq else ""))
            else:
                sections.append(f"- {pattern}")
        sections.append("")

    if teacher_tips:
        sections.append("## Teacher Tips")
        sections.append("")
        for tip in teacher_tips[:5]:
            if isinstance(tip, dict):
                sections.append(f"- {tip.get('tip', tip.get('description', str(tip)))}")
            else:
                sections.append(f"- {tip}")
        sections.append("")

    if ccqs:
        sections.append("## Concept Check Questions (CCQs)")
        sections.append("")
        for ccq in ccqs[:5]:
            if isinstance(ccq, dict):
                q = ccq.get("question", ccq.get("q", str(ccq)))
                sections.append(f"- {q}")
            else:
                sections.append(f"- {ccq}")
        sections.append("")

    sections.append("## Generate L1-Aware Materials Instantly")
    sections.append("")
    sections.append(
        f"With CogniESL, you can generate complete {grammar_point} teaching materials "
        f"specifically tailored for {language} speakers — slides with L1 Oracle, "
        f"worksheets with targeted practice, and activity guides. "
        f"[Try it free at cogniesl.com](https://cogniesl.com)"
    )

    content = "\n".join(sections)

    return {
        "title": title,
        "slug": f"{grammar_point.lower().replace(' ', '-')}-errors-{language.lower()}-esl-students",
        "grammar_point": grammar_point,
        "language": language,
        "content": content,
        "word_count": len(content.split()),
    }


def run_seo_agent(max_posts: int = 3) -> dict:
    """Run SEO Content Agent. Returns result dict with drafted posts."""
    log.info("SEO Content Agent starting...")

    top_grammar = _get_top_grammar_points(limit=5)
    top_l1 = _get_top_l1_languages(limit=5)

    if not top_grammar or not top_l1:
        log.info("No generation data yet — skipping SEO drafts")
        return {"type": "seo_report", "posts_drafted": 0, "reason": "No generation data yet"}

    # Draft posts for top combinations
    drafts = []
    for g in top_grammar[:max_posts]:
        for l in top_l1[:1]:  # Top L1 for each grammar point
            grammar_data = _get_grammar_data(g["grammar"])
            l1_data = _get_l1_data(l["language"])

            if grammar_data or l1_data:
                draft = _draft_blog_post(g["grammar"], l["language"], grammar_data, l1_data)
                if draft["word_count"] > 100:  # Only include substantial drafts
                    drafts.append(draft)

    # Queue drafts as agent_actions
    action_ids = []
    for draft in drafts:
        try:
            action_id = auth_db.log_agent_action(
                "SEO", "draft_ready",
                f"Blog draft: {draft['title']} ({draft['word_count']} words) — "
                f"Grammar: {draft['grammar_point']}, L1: {draft['language']}"
            )
            action_ids.append(action_id)
        except Exception:
            pass

    result = {
        "type": "seo_report",
        "posts_drafted": len(drafts),
        "drafts": drafts,
        "top_grammar": top_grammar,
        "top_l1": top_l1,
        "action_ids": action_ids,
    }

    log.info(f"SEO Agent completed: {len(drafts)} posts drafted")
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
    result = run_seo_agent()
    print(json.dumps(result, indent=2, default=str))
