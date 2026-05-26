"""
Master Repository Cache — CogniESL Phase C

Pre-generated decks are stored in master_repository/{key}/presentations/.
For "common" combinations, after generation the deck is copied here so
subsequent requests for the same combo are served in <10 seconds at $0 API cost.

Key format:  {grammar_slug}__{l1_slug}__{age}__{level}
Example:     present_simple__spanish__adult__b1
"""
import shutil
from pathlib import Path

# Root of the master repository (siblings of this file's parent)
MASTER_REPO = Path(__file__).parent.parent / "master_repository"

# Top 10 grammar points × top 5 L1s × 2 ages × 2 levels = up to 400 combos.
# Start with the most-requested 50 to control one-time pre-build cost (~$75).
COMMON_COMBINATIONS = [
    # Present Simple — the most-taught grammar point
    "present_simple__spanish__adult__a2",
    "present_simple__spanish__adult__b1",
    "present_simple__mandarin__adult__a2",
    "present_simple__mandarin__adult__b1",
    "present_simple__french__adult__b1",
    "present_simple__portuguese__adult__b1",
    "present_simple__arabic__adult__a2",
    "present_simple__japanese__adult__b1",
    "present_simple__spanish__teen__a2",
    "present_simple__mandarin__teen__a2",
    # Past Simple
    "past_simple__spanish__adult__b1",
    "past_simple__spanish__adult__a2",
    "past_simple__mandarin__adult__b1",
    "past_simple__french__adult__b1",
    "past_simple__portuguese__adult__b1",
    "past_simple__arabic__adult__a2",
    "past_simple__spanish__teen__b1",
    "past_simple__mandarin__teen__b1",
    # Present Continuous
    "present_continuous__spanish__adult__a2",
    "present_continuous__spanish__adult__b1",
    "present_continuous__mandarin__adult__a2",
    "present_continuous__mandarin__adult__b1",
    "present_continuous__french__adult__b1",
    "present_continuous__portuguese__adult__b1",
    # Present Perfect
    "present_perfect__spanish__adult__b1",
    "present_perfect__spanish__adult__b2",
    "present_perfect__mandarin__adult__b1",
    "present_perfect__french__adult__b1",
    "present_perfect__japanese__adult__b1",
    # Future Simple (will)
    "future_simple__spanish__adult__a2",
    "future_simple__spanish__adult__b1",
    "future_simple__mandarin__adult__b1",
    "future_simple__portuguese__adult__b1",
    # Going to (future)
    "going_to__spanish__adult__a2",
    "going_to__spanish__adult__b1",
    "going_to__mandarin__adult__b1",
    # Comparatives and Superlatives
    "comparatives__spanish__adult__a2",
    "comparatives__mandarin__adult__a2",
    "comparatives__spanish__teen__a2",
    # Conditionals
    "first_conditional__spanish__adult__b1",
    "first_conditional__mandarin__adult__b1",
    "second_conditional__spanish__adult__b2",
    "second_conditional__mandarin__adult__b2",
    # Modals
    "modals_can__spanish__adult__a2",
    "modals_can__mandarin__adult__a2",
    "modals_must__spanish__adult__b1",
    # Passive Voice
    "passive_voice__spanish__adult__b1",
    "passive_voice__mandarin__adult__b1",
    # Articles
    "articles__mandarin__adult__a2",
    "articles__japanese__adult__a2",
]


def get_combination_key(grammar: str, l1: str, age: str, level: str) -> str:
    """
    Build a cache key from the four parameters.
    All inputs are lowercased and spaces replaced with underscores.
    Only usable for single-L1 requests.
    """
    def _slug(s: str) -> str:
        return s.lower().strip().replace(" ", "_").replace("-", "_")
    return f"{_slug(grammar)}__{_slug(l1)}__{_slug(age)}__{_slug(level)}"


def check_cache(key: str) -> bool:
    """Return True if a pre-generated deck exists for this key."""
    return (MASTER_REPO / key / "presentations").exists()


def copy_from_cache(key: str, dest_path: Path) -> bool:
    """
    Copy pre-generated slides from the master repository to a teacher's project folder.
    Returns True on success, False if the cache entry doesn't exist.
    """
    src = MASTER_REPO / key / "presentations"
    if not src.exists():
        return False
    dest_path.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, dest_path / f.name)
    return True


def add_to_cache(key: str, source_path: Path) -> bool:
    """
    Copy a newly generated deck to the master repository.
    Only stores it if the key is in COMMON_COMBINATIONS.
    Returns True if stored, False if skipped.
    """
    if key not in COMMON_COMBINATIONS:
        return False
    dest = MASTER_REPO / key / "presentations"
    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in source_path.iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)
            copied += 1
    return copied > 0


def cache_stats() -> dict:
    """Return a summary of what's currently in the master repository."""
    if not MASTER_REPO.exists():
        return {"total_cached": 0, "common_cached": 0, "common_total": len(COMMON_COMBINATIONS)}
    cached_keys = [d.name for d in MASTER_REPO.iterdir() if d.is_dir() and (d / "presentations").exists()]
    common_cached = sum(1 for k in COMMON_COMBINATIONS if k in cached_keys)
    return {
        "total_cached": len(cached_keys),
        "common_cached": common_cached,
        "common_total": len(COMMON_COMBINATIONS),
        "cached_keys": sorted(cached_keys),
    }
