"""
YAML schema validation and field normalization for CogniESL.

Validates grammar, L1 interference, and activity data at the load boundary
so field-name inconsistencies (error vs wrong vs example_wrong) are caught
and normalized BEFORE consumers see them.

This is the structural fix that makes F1/F2/F7-type bugs impossible to
reintroduce: once data passes through these normalizers, consumers always
see canonical field names.

Validation is advisory-only (warnings, never exceptions) — a malformed YAML
file should not crash generation.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Field-name canonicalization ────────────────────────────────────────────
# Grammar YAML: error / correction
# L1 YAML:      example_wrong / example_correct
# Some files:   wrong / correct
#
# Normalize all to: error / correction

_FIELD_MAP_WRONG = {
    "error": "error",
    "wrong": "error",
    "example_wrong": "error",
}

_FIELD_MAP_CORRECT = {
    "correction": "correction",
    "correct": "correction",
    "example_correct": "correction",
}


def normalize_common_errors(errors: list[dict]) -> list[dict]:
    """Normalize field names in common_errors/interference_patterns entries.

    Maps wrong/example_wrong → error and correct/example_correct → correction.
    Other fields are preserved unchanged. Returns a new list; does not mutate
    the input.
    """
    if not isinstance(errors, list):
        return []

    normalized: list[dict] = []
    for entry in errors:
        if not isinstance(entry, dict):
            continue
        norm: dict[str, Any] = dict(entry)  # shallow copy
        # Normalize wrong-field → error
        for src, dst in _FIELD_MAP_WRONG.items():
            if src in entry and src != dst:
                norm.setdefault("error", entry[src])
        # Normalize correct-field → correction
        for src, dst in _FIELD_MAP_CORRECT.items():
            if src in entry and src != dst:
                norm.setdefault("correction", entry[src])
        normalized.append(norm)

    return normalized


# ── Validation ─────────────────────────────────────────────────────────────


def validate_grammar_yaml(data: dict) -> list[str]:
    """Validate a grammar YAML dict and return human-readable warnings.

    Checks for missing required sections and empty fields that would cause
    downstream slide/worksheet builders to produce silent empty content.
    """
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Grammar data is not a dict — generation will fail."]

    gp = data.get("grammar_point", "unknown")

    # ── Required top-level sections ───────────────────────────────────────
    if not data.get("meaning"):
        warnings.append(f"[{gp}] Missing 'meaning' section — no CCQs, no core meaning for slides.")

    if not data.get("form"):
        warnings.append(f"[{gp}] Missing 'form' section — no formation rules for slides.")

    if "common_errors" not in data:
        warnings.append(f"[{gp}] Missing 'common_errors' — worksheet Sections A/B will be empty.")
    elif not isinstance(data["common_errors"], list) or not data["common_errors"]:
        warnings.append(f"[{gp}] 'common_errors' is empty — worksheet will have no error pairs.")

    if "sub_rules" not in data:
        warnings.append(f"[{gp}] Missing 'sub_rules' — spelling/irregular rule slides will be missing.")

    # ── meaning section ───────────────────────────────────────────────────
    meaning = data.get("meaning", {})
    if isinstance(meaning, dict):
        if not meaning.get("core_meaning"):
            warnings.append(f"[{gp}] 'meaning.core_meaning' is missing or empty.")
        ccqs = meaning.get("ccqs")
        if not ccqs or not isinstance(ccqs, list):
            warnings.append(f"[{gp}] 'meaning.ccqs' is missing or empty — no concept-check questions for Section 2.")

    # ── form section ──────────────────────────────────────────────────────
    form = data.get("form", {})
    if isinstance(form, dict):
        if not form.get("affirmative"):
            warnings.append(f"[{gp}] 'form.affirmative' is missing — no affirmative formation rule.")
        if not form.get("negative"):
            warnings.append(f"[{gp}] 'form.negative' is missing — no negative formation rule.")
        if not form.get("questions"):
            warnings.append(f"[{gp}] 'form.questions' is missing — no question formation rule.")

    # ── common_errors entries ─────────────────────────────────────────────
    common_errors = data.get("common_errors", [])
    if isinstance(common_errors, list):
        for i, err in enumerate(common_errors):
            if not isinstance(err, dict):
                warnings.append(f"[{gp}] common_errors[{i}] is not a dict — skipping.")
                continue
            has_wrong = err.get("error") or err.get("wrong") or err.get("example_wrong")
            has_correct = err.get("correction") or err.get("correct") or err.get("example_correct")
            if has_wrong and not has_correct:
                warnings.append(f"[{gp}] common_errors[{i}] has wrong but no correction — incomplete error pair.")
            if has_correct and not has_wrong:
                warnings.append(f"[{gp}] common_errors[{i}] has correction but no wrong — incomplete error pair.")
            if not has_wrong and not has_correct:
                warnings.append(f"[{gp}] common_errors[{i}] has no error/wrong/example_wrong AND no correction fields.")

    # ── sub_rules entries ─────────────────────────────────────────────────
    sub_rules = data.get("sub_rules", [])
    if isinstance(sub_rules, list):
        for i, sr in enumerate(sub_rules):
            if not isinstance(sr, dict):
                warnings.append(f"[{gp}] sub_rules[{i}] is not a dict.")
                continue
            if not sr.get("rule"):
                warnings.append(f"[{gp}] sub_rules[{i}] has no 'rule' text.")
            if not sr.get("examples"):
                warnings.append(f"[{gp}] sub_rules[{i}] has no 'examples'.")

    return warnings


def validate_l1_yaml(data: dict) -> list[str]:
    """Validate a single L1 interference entry (grammar_point + language) and
    return human-readable warnings.

    The L1 data passed here is the unwrapped, per-language-per-grammar-point
    dict already extracted by _load_yaml_data (i.e., with interference_patterns
    and why_it_happens at the top level).
    """
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["L1 data is not a dict — skipping validation."]

    lang = data.get("language", "unknown")
    gp = data.get("grammar_point", "unknown")

    patterns = data.get("interference_patterns")
    if not patterns or not isinstance(patterns, list):
        warnings.append(f"[{lang}/{gp}] No 'interference_patterns' — L1 Oracle slides will be empty.")
        return warnings

    # ── Pattern entries ───────────────────────────────────────────────────
    for i, p in enumerate(patterns):
        if not isinstance(p, dict):
            warnings.append(f"[{lang}/{gp}] interference_patterns[{i}] is not a dict.")
            continue
        has_wrong = p.get("example_wrong") or p.get("error") or p.get("wrong")
        has_correct = p.get("example_correct") or p.get("correction") or p.get("correct")
        has_explanation = p.get("explanation")
        if not has_wrong and not has_correct:
            warnings.append(f"[{lang}/{gp}] pattern[{i}] has no wrong/correct pair.")
        if not has_explanation:
            warnings.append(f"[{lang}/{gp}] pattern[{i}] '{p.get('pattern', '?')[:60]}' has no explanation.")

    # ── why_it_happens ────────────────────────────────────────────────────
    if not data.get("why_it_happens"):
        warnings.append(f"[{lang}/{gp}] Missing 'why_it_happens' — L1 Oracle explanation will be generic.")

    return warnings
