"""
Pre-build Master Repository Cache — CogniESL Phase C

One-time script that generates the 50 most common combinations and stores them
in master_repository/. Run this locally (NOT on Railway) overnight.

Cost estimate: ~50 generations × $1.50 each ≈ $75 one-time cost.
After this, each cached combo is served in <10 seconds at $0 API cost.

Usage:
    cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
    python scripts/prebuild_cache.py

Options:
    --dry-run       Print what would be generated without making API calls
    --only "key"    Generate only the specified key (for testing one combo)
    --skip-existing Skip keys that already have a cached deck (default: True)
"""
import argparse
import sys
import time
from pathlib import Path

# Add the project root to sys.path so we can import agent modules
_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from agent.master_repository import COMMON_COMBINATIONS, check_cache, add_to_cache


def main():
    parser = argparse.ArgumentParser(description="Pre-build CogniESL Master Repository cache")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without running")
    parser.add_argument("--only", type=str, default="", help="Generate only this key")
    parser.add_argument("--no-skip", action="store_true", help="Regenerate even if cached")
    args = parser.parse_args()

    targets = COMMON_COMBINATIONS
    if args.only:
        targets = [k for k in COMMON_COMBINATIONS if args.only in k]
        if not targets:
            print(f"No combination matches '{args.only}'. Valid keys:")
            for k in COMMON_COMBINATIONS:
                print(f"  {k}")
            sys.exit(1)

    skip_existing = not args.no_skip
    to_generate = []
    for key in targets:
        if skip_existing and check_cache(key):
            print(f"  [SKIP] {key} — already cached")
        else:
            to_generate.append(key)

    print(f"\nPlan: generate {len(to_generate)} combinations")
    print(f"Estimated cost: ~${len(to_generate) * 1.5:.0f}")
    print(f"Estimated time: ~{len(to_generate) * 5} minutes\n")

    if args.dry_run:
        print("DRY RUN — not calling API. Keys that would be generated:")
        for key in to_generate:
            print(f"  {key}")
        return

    if not to_generate:
        print("Nothing to generate. All common combinations are already cached.")
        return

    # ── Actual generation ────────────────────────────────────────────────────
    # This section calls the CogniESL generation pipeline programmatically.
    # TODO: Wire this to the agent once the generation API is stable.
    # For now it prints the steps so Marcos can run them manually or via the chat UI.
    print("=" * 60)
    print("GENERATION STEPS (run via CogniESL chat or API):")
    print("=" * 60)
    for i, key in enumerate(to_generate, 1):
        parts = key.split("__")
        if len(parts) == 4:
            grammar, l1, age, level = parts
        else:
            print(f"  [{i}] SKIPPED — bad key format: {key}")
            continue

        grammar_display = grammar.replace("_", " ").title()
        l1_display = l1.replace("_", " ").title()
        age_display = age.title()
        level_display = level.upper()

        print(f"\n[{i}/{len(to_generate)}] {key}")
        print(f"  Grammar:  {grammar_display}")
        print(f"  L1:       {l1_display} speakers")
        print(f"  Age:      {age_display}")
        print(f"  Level:    {level_display}")
        print(f"  Chat prompt: Generate {grammar_display} for {age_display} {l1_display} speakers at {level_display} level, all formats")

    print("\n" + "=" * 60)
    print("After each generation, the agent will automatically add the")
    print("deck to the master_repository/ cache if the key is in COMMON_COMBINATIONS.")
    print("=" * 60)


if __name__ == "__main__":
    main()
