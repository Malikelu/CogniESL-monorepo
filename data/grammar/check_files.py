#!/usr/bin/env python3
"""Fill empty fields in grammar YAML files for CogniESL."""

import yaml
import os

GRAMMAR_DIR = "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar"

# The 40 files to process (first 40 from the list)
FILES = [
    "deduction_speculation.yaml",
    "definitely_probably.yaml",
    "degree_adverbs.yaml",
    "dependent_prepositions.yaml",
    "ed_clauses.yaml",
    "ed_vs_ing_adjectives.yaml",
    "even_if.yaml",
    "few.yaml",
    "first_conditional.yaml",
    "frequency_adverbs.yaml",
    "future_continuous.yaml",
    "future_going_to.yaml",
    "future_in_the_past.yaml",
    "future_perfect.yaml",
    "future_perfect_continuous.yaml",
    "future_perfect_simple.yaml",
    "future_will.yaml",
    "generic_pronouns.yaml",
    "gerunds_infinitives.yaml",
    "had_better.yaml",
    "have_get_something_done.yaml",
    "however.yaml",
    "i_wish_if_only.yaml",
    "in_case.yaml",
    "indirect_questions.yaml",
    "infinitive_of_purpose.yaml",
    "ing_clauses.yaml",
    "inversion_negative.yaml",
    "inversion_with_negative_adverbials.yaml",
    "its_time.yaml",
    "likely.yaml",
    "linking_words.yaml",
    "look_sound_feel_smell_taste.yaml",
    "manner_adverbs.yaml",
    "may_might_probability.yaml",
    "might.yaml",
    "mixed_conditionals.yaml",
    "modals.yaml",
    "modals_overview.yaml",
    "modals_possibility.yaml",
]


def needs_filling(data):
    """Check which fields need filling."""
    issues = []
    meaning = data.get("meaning", {})
    if isinstance(meaning, dict):
        if not meaning.get("ccqs", []):
            issues.append("ccqs")
    if not data.get("sub_rules", []):
        issues.append("sub_rules")
    if not data.get("phonetics", []):
        issues.append("phonetics")
    teaching = data.get("teaching", {})
    if isinstance(teaching, dict):
        if not teaching.get("tips", []):
            issues.append("tips")
        if not teaching.get("recommended_activities", []):
            issues.append("activities")
    if not data.get("use", []):
        issues.append("use")
    return issues


def process_file(filename):
    """Read, check, and report on a file. Returns True if file needs filling."""
    filepath = os.path.join(GRAMMAR_DIR, filename)
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        return False

    if not data:
        print(f"SKIP {filename}: empty or invalid")
        return False

    issues = needs_filling(data)
    if issues:
        print(f"NEEDS: {filename} -> {', '.join(issues)}")
        return True
    else:
        print(f"OK: {filename}")
        return False


def main():
    needs_work = []
    for f in FILES:
        if process_file(f):
            needs_work.append(f)

    print(f"\n{len(needs_work)} files need filling out of {len(FILES)}")
    for f in needs_work:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
