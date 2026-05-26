#!/usr/bin/env python3
"""
Data Quality Integration Test — Verifies enhanced forge data is synced to CogniESL
and that the AI tools can load and return enriched content.

Tests:
1. Grammar files have per-claim citations (Ch./§/Entry in sources)
2. Grammar files have 3+ CCQs with specific purposes
3. Grammar files have non-generic discourse_notes and register_notes
4. L1 files have structured interference_patterns (dicts, not strings)
5. L1 patterns have example_wrong/example_correct pairs
6. SearchGrammarTool returns enhanced content
7. GetL1InterferenceTool returns structured patterns
"""
import sys
import os
import yaml
import re
from pathlib import Path

# Add agent directory to path for tool imports
AGENT_DIR = Path(__file__).parent.parent / "agent"
sys.path.insert(0, str(AGENT_DIR))

DATA_DIR = Path(__file__).parent.parent / "data"
GRAMMAR_DIR = DATA_DIR / "grammar"
L1_DIR = DATA_DIR / "l1-interference"

passed = 0
failed = 0
errors = []


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        errors.append(f"✗ {name}: {detail}")
        print(f"  ✗ {name}: {detail}")


# ─── TEST 1: Grammar file quality ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("TEST 1: Grammar File Quality")
print("=" * 70)

# Sample high-frequency files to check
SAMPLE_FILES = [
    "present_simple.yaml", "past_simple.yaml", "present_continuous.yaml",
    "articles.yaml", "a_an_the.yaml", "modals.yaml", "can_cant.yaml",
    "passive_voice.yaml", "relative_clauses.yaml", "comparatives_superlatives.yaml",
    "subject_pronouns.yaml", "there_is_are.yaml", "some_any.yaml",
    "future_will.yaml", "first_conditional.yaml", "reported_speech.yaml",
    "prepositions_of_place.yaml", "prepositions_of_time.yaml",
    "countable_uncountable.yaml", "question_forms.yaml",
]

for fname in SAMPLE_FILES:
    fpath = GRAMMAR_DIR / fname
    if not fpath.exists():
        check(fname, False, "file not found")
        continue
    with open(fpath) as f:
        data = yaml.safe_load(f)
    if not data:
        check(fname, False, "empty YAML")
        continue

    # Check sources have chapter/section
    sources = data.get("sources", {})
    primary = sources.get("primary", "")
    has_chapter = any(x in primary for x in ["Ch.", "Ch ", "§", "Entry"])
    check(f"{fname} — sources have chapter/section", has_chapter, f"primary: {primary[:60]}")

    # Check CCQs
    ccqs = data.get("meaning", {}).get("ccqs", [])
    check(f"{fname} — has 3+ CCQs", len(ccqs) >= 3, f"found {len(ccqs)}")

    # Check CCQ purposes are specific
    generic_purpose = re.compile(r"Tests (whether|that|if|understanding of) \w+$", re.IGNORECASE)
    for i, ccq in enumerate(ccqs):
        purpose = ccq.get("purpose", "")
        if generic_purpose.search(purpose):
            check(f"{fname} — CCQ[{i}] purpose specific", False, f"generic: {purpose[:60]}")

    # Check discourse_notes not generic
    discourse_generic = re.compile(r"used in both spoken and written discourse", re.IGNORECASE)
    for note in data.get("discourse_notes", []):
        text = note.get("note", "") if isinstance(note, dict) else str(note)
        if discourse_generic.search(text):
            check(f"{fname} — discourse_notes specific", False, f"generic: {text[:60]}")

    # Check register_notes not generic
    register_generic = re.compile(r"used in both formal and informal contexts", re.IGNORECASE)
    for note in data.get("register_notes", []):
        text = note.get("note", "") if isinstance(note, dict) else str(note)
        if register_generic.search(text):
            check(f"{fname} — register_notes specific", False, f"generic: {text[:60]}")


# ─── TEST 2: L1 file quality ─────────────────────────────────────────────────
print("\n" + "=" * 70)
print("TEST 2: L1 Interference File Quality")
print("=" * 70)

L1_LANGUAGES = [
    "spanish_interference.yaml", "arabic_interference.yaml",
    "mandarin_interference.yaml", "portuguese_interference.yaml",
]

for fname in L1_LANGUAGES:
    fpath = L1_DIR / fname
    if not fpath.exists():
        check(fname, False, "file not found")
        continue
    with open(fpath) as f:
        data = yaml.safe_load(f)
    if not data:
        check(fname, False, "empty YAML")
        continue

    gps = data.get("grammar_points", {})
    check(f"{fname} — has grammar_points", len(gps) > 0, f"found {len(gps)} GPs")

    # Check first 5 GPs for structured patterns
    string_count = 0
    struct_count = 0
    missing_examples = 0
    for gp_name, gp_data in list(gps.items())[:5]:
        patterns = gp_data.get("interference_patterns", [])
        for p in patterns[:3]:
            if isinstance(p, str):
                string_count += 1
            elif isinstance(p, dict):
                struct_count += 1
                if "example_wrong" not in p or "example_correct" not in p:
                    missing_examples += 1

    check(f"{fname} — no string patterns", string_count == 0, f"found {string_count} strings")
    check(f"{fname} — has structured patterns", struct_count > 0, f"found {struct_count} dicts")
    check(f"{fname} — patterns have examples", missing_examples == 0, f"{missing_examples} missing examples")


# ─── TEST 3: SearchGrammarTool integration ───────────────────────────────────
print("\n" + "=" * 70)
print("TEST 3: SearchGrammarTool Integration")
print("=" * 70)

try:
    from tools.SearchGrammarTool import SearchGrammarTool

    tool = SearchGrammarTool(topic="present_simple")
    result = tool.run()
    result_str = str(result)
    check("SearchGrammarTool — present_simple found", "present" in result_str.lower())
    check("SearchGrammarTool — has CCQs", "ccq" in result_str.lower() or "concept check" in result_str.lower() or "question" in result_str.lower())
    check("SearchGrammarTool — has sources", "Celce-Murcia" in result_str or "Grammar Book" in result_str or "Ch." in result_str)

except Exception as e:
    check("SearchGrammarTool — import/run", False, f"{type(e).__name__}: {e}")


# ─── TEST 4: GetL1InterferenceTool integration ───────────────────────────────
print("\n" + "=" * 70)
print("TEST 4: GetL1InterferenceTool Integration")
print("=" * 70)

try:
    from tools.GetL1InterferenceTool import GetL1InterferenceTool

    # Test Spanish + present_simple
    tool_es = GetL1InterferenceTool(language="Spanish", grammar_point="present_simple")
    result_es = tool_es.run()
    result_es_str = str(result_es)
    check("GetL1InterferenceTool — Spanish present_simple found", len(result_es_str) > 100)
    check("GetL1InterferenceTool — Spanish has structured patterns",
          "example_wrong" in result_es_str or "example_correct" in result_es_str or "interference" in result_es_str.lower())

    # Test Arabic + articles
    tool_ar = GetL1InterferenceTool(language="Arabic", grammar_point="articles")
    result_ar = tool_ar.run()
    result_ar_str = str(result_ar)
    check("GetL1InterferenceTool — Arabic articles found", len(result_ar_str) > 100)

    # Test Mandarin + articles
    tool_zh = GetL1InterferenceTool(language="Mandarin", grammar_point="articles")
    result_zh = tool_zh.run()
    result_zh_str = str(result_zh)
    check("GetL1InterferenceTool — Mandarin articles found", len(result_zh_str) > 100)

except Exception as e:
    check("GetL1InterferenceTool — import/run", False, f"{type(e).__name__}: {e}")


# ─── SUMMARY ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("INTEGRATION TEST SUMMARY")
print("=" * 70)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total:  {passed + failed}")

if errors:
    print(f"\nFailed checks:")
    for e in errors:
        print(f"  {e}")

print()
if failed == 0:
    print("✓ ALL TESTS PASSED — Data quality verified, tools load enhanced content")
    sys.exit(0)
else:
    print(f"✗ {failed} TESTS FAILED — See details above")
    sys.exit(1)
