"""
Curator Agent — CogniESL Phase E

Runs on a schedule (weekly) to pre-populate the Master Repository with the most
commonly requested combinations. Once a combination is cached, future requests
for that combination are served in <10 seconds at $0 LLM cost.

Usage:
    python -m agent.curator_agent                    # run all missing common combos
    python -m agent.curator_agent --status           # show what's cached vs missing
    python -m agent.curator_agent --key present_simple__spanish__adult__b1  # single key
    python -m agent.curator_agent --max 5            # cap at 5 generations per run

Railway Cron usage (set CRON_SCHEDULE in Railway):
    The server.py calls curator_agent.run_scheduled() on startup and re-schedules it weekly.

Cost estimate:
    ~$1.50 per generation × 50 combinations = ~$75 one-time to fully populate.
    After cache is warm, marginal API cost drops by ~70%.
"""
import argparse
import asyncio
import logging
import os
import sys
import time
from pathlib import Path

# Ensure project root is on sys.path when run as a module
_root = Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from agent.master_repository import (
    COMMON_COMBINATIONS,
    check_cache,
    cache_stats,
    get_combination_key,
    add_to_cache,
    MASTER_REPO,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Curator] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("curator")


# ─── Demand analysis ─────────────────────────────────────────────────────────

def get_top_uncached_from_db(limit: int = 20) -> list[str]:
    """
    Query the generations table and return uncached combinations ordered by request frequency.
    Falls back to COMMON_COMBINATIONS if the DB is empty or not available.
    """
    try:
        from agent.jobs import _MNT_DIR
        data_dir = _MNT_DIR.parent if _MNT_DIR.name == "data" else _MNT_DIR
        db_path = data_dir / "cogniesl.db"
        if not db_path.exists():
            db_path = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data")) / "cogniesl.db"

        if not db_path.exists():
            log.info("No generations DB found — using COMMON_COMBINATIONS list")
            return [k for k in COMMON_COMBINATIONS if not check_cache(k)]

        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT grammar_point, l1_languages, age_group, level, COUNT(*) as cnt
            FROM generations
            WHERE grammar_point != ''
              AND l1_languages NOT LIKE '%,%'  -- single L1 only
            GROUP BY grammar_point, l1_languages, age_group, level
            ORDER BY cnt DESC
            LIMIT ?
        """, (limit * 3,)).fetchall()
        conn.close()

        demanded = []
        for row in rows:
            level = row["level"] or "b1"
            key = get_combination_key(
                grammar=row["grammar_point"],
                l1=row["l1_languages"],
                age=row["age_group"] or "adult",
                level=level,
            )
            if not check_cache(key):
                demanded.append(key)
            if len(demanded) >= limit:
                break

        if demanded:
            log.info(f"Found {len(demanded)} high-demand uncached combinations from DB")
            return demanded

        # Fall back to COMMON_COMBINATIONS if DB has no useful data
        return [k for k in COMMON_COMBINATIONS if not check_cache(k)]

    except Exception as e:
        log.warning(f"DB demand analysis failed ({e}) — using COMMON_COMBINATIONS")
        return [k for k in COMMON_COMBINATIONS if not check_cache(k)]


# ─── Generation ──────────────────────────────────────────────────────────────

def _parse_key(key: str) -> tuple[str, str, str, str]:
    """Split a cache key into (grammar, l1, age, level)."""
    parts = key.split("__")
    if len(parts) != 4:
        raise ValueError(f"Invalid cache key: {key} (expected grammar__l1__age__level)")
    return parts[0], parts[1], parts[2], parts[3]


def _grammar_slug_to_name(slug: str) -> str:
    """Convert a slug like 'present_simple' to 'Present Simple'."""
    return slug.replace("_", " ").title()


def _l1_slug_to_name(slug: str) -> str:
    """Convert a slug like 'spanish' to 'Spanish'."""
    return slug.title()


async def _generate_one(key: str) -> bool:
    """
    Synthesise one combination and store in Master Repository.
    Returns True on success.
    """
    grammar_slug, l1_slug, age, level = _parse_key(key)
    grammar = _grammar_slug_to_name(grammar_slug)
    l1 = _l1_slug_to_name(l1_slug)

    log.info(f"Generating: {grammar} | {l1} | {age} | {level.upper()}")

    # Build a synthetic teacher request and run through the full agent
    from agent.cogniesl_agent import create_cogniesl_agent
    from agency_swarm import set_openai_client
    import openai

    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not openai_key:
        log.error("No OPENAI_API_KEY or OPENROUTER_API_KEY — cannot generate")
        return False

    # Configure client (use OpenRouter if specified)
    base_url = os.getenv("OPENROUTER_BASE_URL", None)
    client = openai.AsyncOpenAI(
        api_key=openai_key,
        base_url=base_url,
    ) if base_url else openai.AsyncOpenAI(api_key=openai_key)
    set_openai_client(client)

    project_name = f"curator_{key}"
    agent, ctx = create_cogniesl_agent()

    # Synthetic request that specifies all parameters clearly
    request = (
        f"I need slides for {grammar} for {l1} {age} students at {level.upper()} level. "
        f"Please generate slides only (no worksheet or activity guide). "
        f"This is a pre-generation for the Master Repository — skip email delivery."
    )

    try:
        response = await agent.get_response(message=request, agency_context=ctx)
        response_text = str(getattr(response, "final_output", response))
        log.info(f"Agent response (first 200 chars): {response_text[:200]}")

        # Check if PPTX was generated
        pptx_candidates = list(
            (Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent.parent)) / "mnt" / project_name / "presentations").glob("*.pptx")
        )
        if not pptx_candidates:
            log.warning(f"No PPTX found for {key} after generation")
            return False

        pptx_file = pptx_candidates[0]
        stored = add_to_cache(key, pptx_file.parent)
        if stored:
            log.info(f"✅ Cached: {key} ({pptx_file.stat().st_size:,} bytes)")
        else:
            log.warning(f"Skipped cache store for {key} (not in COMMON_COMBINATIONS?)")
        return stored

    except Exception as e:
        log.error(f"Generation failed for {key}: {e}", exc_info=True)
        return False


# ─── CLI / scheduler entry points ────────────────────────────────────────────

def show_status() -> None:
    stats = cache_stats()
    print(f"\n{'═'*60}")
    print(f"  Master Repository Status")
    print(f"{'═'*60}")
    print(f"  Common combinations: {stats['common_total']}")
    print(f"  Cached:              {stats['common_cached']} ({100*stats['common_cached']//max(stats['common_total'],1)}%)")
    print(f"  Total in repo:       {stats['total_cached']}")
    print(f"{'─'*60}")

    missing = [k for k in COMMON_COMBINATIONS if not check_cache(k)]
    if missing:
        print(f"  Missing ({len(missing)}):")
        for k in missing[:15]:
            print(f"    - {k}")
        if len(missing) > 15:
            print(f"    … and {len(missing)-15} more")
    else:
        print("  ✅ All common combinations cached!")
    print()


async def run_batch(keys: list[str], delay_between: float = 30.0) -> dict:
    """Generate a list of keys sequentially with a delay between each."""
    results = {"success": 0, "failed": 0, "skipped": 0}
    for i, key in enumerate(keys, 1):
        if check_cache(key):
            log.info(f"[{i}/{len(keys)}] Already cached: {key}")
            results["skipped"] += 1
            continue
        log.info(f"[{i}/{len(keys)}] Starting generation for: {key}")
        ok = await _generate_one(key)
        if ok:
            results["success"] += 1
        else:
            results["failed"] += 1
        if i < len(keys):
            log.info(f"Waiting {delay_between}s before next generation...")
            await asyncio.sleep(delay_between)
    return results


def run_scheduled(max_per_run: int = 3) -> None:
    """
    Entry point called by the server's startup scheduler.
    Generates up to max_per_run uncached common combinations.
    Runs in a background thread (non-blocking).
    """
    import threading

    def _bg():
        keys = get_top_uncached_from_db(limit=max_per_run)
        if not keys:
            log.info("Curator: All common combinations are cached — nothing to do")
            return
        log.info(f"Curator: Scheduling {len(keys)} generation(s)")
        asyncio.run(run_batch(keys[:max_per_run], delay_between=60.0))

    thread = threading.Thread(target=_bg, daemon=True, name="curator-agent")
    thread.start()


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="CogniESL Curator Agent")
    parser.add_argument("--status", action="store_true", help="Show cache status and exit")
    parser.add_argument("--key", help="Generate a single specific key")
    parser.add_argument("--max", type=int, default=5, help="Max combinations to generate (default 5)")
    parser.add_argument("--delay", type=float, default=30.0, help="Seconds between generations (default 30)")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.key:
        keys = [args.key]
    else:
        keys = get_top_uncached_from_db(limit=args.max)

    if not keys:
        print("✅ Nothing to generate — all common combinations are already cached.")
        show_status()
        return

    print(f"\nGenerating {len(keys)} combination(s) with {args.delay}s delay between:\n")
    for k in keys:
        print(f"  {k}")
    print()

    results = asyncio.run(run_batch(keys, delay_between=args.delay))
    print(f"\n{'═'*60}")
    print(f"  Done: {results['success']} succeeded · {results['failed']} failed · {results['skipped']} already cached")
    show_status()


if __name__ == "__main__":
    main()
