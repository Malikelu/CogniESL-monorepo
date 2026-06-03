"""
slide_plan.py — Deterministic slide planner + task_brief builder for CogniESL.

Replaces the LLM-driven task_brief construction and InsertNewSlides planner
with direct Python, enabling:
  1. Modular slide count estimation from grammar YAML structure
  2. Deterministic slide ordering (CCQs → Formulas → Sub-rules → Practice → L1 Oracle → Wrap-up)
  3. Full task_brief generation from verbatim YAML data (no LLM summarization)
  4. Parallel execution support (slides are independent)

Each slide type (A0–A8, CLOSING_BRAND) follows the exact task_brief format
from agent/instructions.md, with YAML fields pasted verbatim.

Usage:
    from agent.slides_tools.slide_plan import compute_slide_plan, build_all_task_briefs

    plan = compute_slide_plan(grammar_data, l1_languages, age_group)
    briefs = build_all_task_briefs(plan, grammar_data, l1_data_list, age_group, l1_languages)
"""

from __future__ import annotations

import os
from typing import Any

# ── Watermark ────────────────────────────────────────────────────────────────
_WATERMARK = os.getenv("COGNIESL_WATERMARK", "free")


# ── Slide Plan ───────────────────────────────────────────────────────────────

def compute_slide_plan(
    grammar_data: dict[str, Any],
    l1_languages: str,
    age_group: str,
) -> list[dict[str, Any]]:
    """Determine the slide order and types from YAML grammar data.

    Returns a list of slide metadata dicts, each with:
        - type: str (A0, A1, A2, A3, A5, A5_SUB, A5b, A6, A7_GAP_FILL, A8, CLOSING_BRAND)
        - label: str
        - Extra fields per type (e.g., ccq_index, form_key, sub_rule_index, l1_language)
    """
    meaning = grammar_data.get("meaning", {})
    form = grammar_data.get("form", {})
    sub_rules: list = grammar_data.get("sub_rules") or []
    common_errors: list = grammar_data.get("common_errors") or []
    phonetics = grammar_data.get("phonetics") or {}
    ccqs: list = meaning.get("ccqs") or []
    l1_list = [l.strip() for l in l1_languages.split(",") if l.strip()]

    slides: list[dict[str, Any]] = []

    # Slide 1: A0 Lesson Plan Cover
    slides.append({"type": "A0", "label": "Lesson Plan Cover"})

    # Slide 2: A0b Student Intro — beautiful class-opening slide
    slides.append({"type": "A0b", "label": "Student Intro"})

    # Slide 3: A1 Hook
    slides.append({"type": "A1", "label": "Hook"})

    # Slide 3: A2 Meaning Overview
    slides.append({"type": "A2", "label": "Meaning Overview"})

    # A3: CCQ Discovery (one per CCQ in the YAML)
    for i in range(len(ccqs)):
        slides.append({"type": "A3", "label": f"CCQ — {i+1}", "ccq_index": i})

    # A5: Grammar Formula slides (affirmative / negative / questions)
    for form_key in ("affirmative", "negative", "questions"):
        if isinstance(form.get(form_key), dict) and form[form_key].get("structure"):
            label_map = {"affirmative": "Affirmative", "negative": "Negative", "questions": "Questions"}
            slides.append({
                "type": "A5", "label": f"Formula — {label_map[form_key]}", "form_key": form_key,
            })

    # A5: Sub-rule slides (spelling rules, irregulars)
    for i in range(len(sub_rules)):
        slides.append({
            "type": "A5_SUB", "label": f"Sub-rule — {i+1}", "sub_rule_index": i,
        })

    # A5b: Pronunciation Guide (only if phonetics data exists)
    # phonetics can be a dict with 'groups'/'spelling_rule' or a list of sound groups
    if isinstance(phonetics, dict):
        has_phonetics = bool(phonetics.get("groups") or phonetics.get("spelling_rule"))
    else:
        has_phonetics = bool(phonetics)
    if has_phonetics:
        slides.append({"type": "A5b", "label": "Pronunciation Guide"})

    # A6: L1 Oracle (one per L1 language) — placed BEFORE practice so
    # students are warned about their specific errors before they practice.
    for l1 in l1_list:
        slides.append({
            "type": "A6", "label": f"L1 Oracle — {l1}", "l1_language": l1,
        })

    # A7: Practice slides (3 gap-fills from common_errors)
    # Only create as many as there are available error items (minimum 2, max 3)
    error_pool = [e for e in common_errors if isinstance(e, dict)]
    practice_count = min(3, max(2, len(error_pool)))
    practice_labels = ["Spot the Mistake", "Fill the Gap", "Fix the Error"]
    for i in range(practice_count):
        slides.append({
            "type": "A7_GAP_FILL", "label": f"Practice — {practice_labels[i]}",
            "practice_index": i,
        })

    # A8: Wrap-up
    slides.append({"type": "A8", "label": "Wrap-up"})

    # CLOSING_BRAND (always last)
    slides.append({"type": "CLOSING_BRAND", "label": "Closing Brand"})

    return slides


# ── Task Brief Builders ──────────────────────────────────────────────────────

def build_task_brief(
    slide_meta: dict[str, Any],
    grammar_data: dict[str, Any],
    l1_data_list: list[dict[str, Any]],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build a task_brief for a single slide from YAML data.

    Each builder produces a string matching the exact format in instructions.md.
    Returns the task_brief text exactly as the sub-agent expects it.
    """
    slide_type = slide_meta["type"]

    builders = {
        "A0": _build_a0_brief,
        "A0b": _build_a0b_brief,
        "A1": _build_a1_brief,
        "A2": _build_a2_brief,
        "A3": _build_a3_brief,
        "A5": _build_a5_brief,
        "A5_SUB": _build_a5_sub_brief,
        "A5b": _build_a5b_brief,
        "A6": _build_a6_brief,
        "A7_GAP_FILL": _build_a7_gap_fill_brief,
        "A8": _build_a8_brief,
        "CLOSING_BRAND": lambda *_: "SLIDE_TYPE: CLOSING_BRAND",
    }

    builder = builders.get(slide_type)
    if builder is None:
        return f"SLIDE_TYPE: {slide_type}\nSlide title: {slide_meta.get('label', '')}"

    return builder(slide_meta, grammar_data, l1_data_list, age_group, l1_languages)


def build_all_task_briefs(
    slide_plan: list[dict[str, Any]],
    grammar_data: dict[str, Any],
    l1_data_list: list[dict[str, Any]],
    age_group: str,
    l1_languages: str,
) -> dict[int, str]:
    """Build task_briefs for all slides in the plan.

    Returns {1: "task_brief for slide 01", 2: "..."} keyed by 1-based slide index.
    """
    return {
        i + 1: build_task_brief(s, grammar_data, l1_data_list, age_group, l1_languages)
        for i, s in enumerate(slide_plan)
    }


# ── Field Extraction Helpers ─────────────────────────────────────────────────

def _s(text: Any) -> str:
    """Safely convert a value to string, handling None."""
    if text is None:
        return ""
    return str(text)


def _fmt_label(title: str, subtitle: str = "") -> str:
    if subtitle:
        return f"{title}\nSubtitle: {subtitle}"
    return title


def _get_ccq(grammar_data: dict, index: int) -> dict:
    ccqs = grammar_data.get("meaning", {}).get("ccqs") or []
    if index < len(ccqs):
        c = ccqs[index]
        if isinstance(c, dict):
            return c
    return {"question": "", "answer": "", "purpose": ""}


def _get_sub_rule(grammar_data: dict, index: int) -> dict:
    rules = grammar_data.get("sub_rules") or []
    if index < len(rules) and isinstance(rules[index], dict):
        return rules[index]
    return {"rule": "", "examples": "", "explanation": ""}


def _get_form_data(grammar_data: dict, form_key: str) -> dict:
    form = grammar_data.get("form", {})
    section = form.get(form_key, {})
    if isinstance(section, dict):
        return section
    return {"structure": ""}


def _get_l1_data(l1_data_list: list[dict], language: str) -> dict:
    """Find the L1 data dict for a given language name."""
    lang_lower = language.lower().strip()
    for d in l1_data_list:
        d_name = _s(d.get("language", d.get("name", ""))).lower().strip()
        if lang_lower in d_name or d_name in lang_lower:
            return d
    return {}


def _get_teaching_tips(grammar_data: dict) -> list[str]:
    teaching = grammar_data.get("teaching", {})
    raw_tips = teaching.get("tips") or []
    # tips can be a list of strings or list of dicts
    return [_s(t.get("text", t) if isinstance(t, dict) else t) for t in raw_tips if t]


def _pick_tier1_2_patterns(l1_section: dict, max_count: int = 5) -> list[dict]:
    """Filter interference patterns to tier 1-2 with frequency >= 3 or persistence >= 3."""
    patterns = l1_section.get("interference_patterns") or l1_section.get("patterns") or []
    filtered = []
    for p in patterns:
        if not isinstance(p, dict):
            continue
        tier = p.get("tier")
        # Include if no tier field (legacy data — treat as tier 2)
        if tier is not None and tier not in (1, 2):
            continue
        freq = _as_int(p.get("frequency", 0))
        persist = _as_int(p.get("persistence", 0))
        if freq >= 3 or persist >= 3 or not filtered:
            # Always include first pattern even if low-rated (we need at least one)
            filtered.append(p)
            if len(filtered) >= max_count:
                break
    return filtered


def _as_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _pick_errors_for_gapfill(grammar_data: dict, l1_languages: str, count: int = 4) -> list[dict]:
    """Pick common_errors relevant to the specified L1 groups."""
    errors = grammar_data.get("common_errors") or []
    l1_list = [l.strip().lower() for l in l1_languages.split(",") if l.strip()]
    relevant = []
    for e in errors:
        if not isinstance(e, dict):
            continue
        # Check if this error targets one of the specified L1s
        l1_groups = e.get("l1_groups") or e.get("l1_languages") or []
        l1_groups_str = _s(l1_groups).lower() if not isinstance(l1_groups, list) else " ".join(l1_groups).lower()
        if any(l1 in l1_groups_str for l1 in l1_list) or not l1_list:
            relevant.append(e)
    return relevant[:count] if relevant else errors[:count]


def _get_differentiation(grammar_data: dict) -> tuple[str, str]:
    teaching = grammar_data.get("teaching", {})
    return (_s(teaching.get("support", "")), _s(teaching.get("extension", "")))


def _get_key_principles(grammar_data: dict) -> list[str]:
    kp = grammar_data.get("key_principles")
    if not isinstance(kp, list):
        return []
    result = []
    for p in kp:
        if isinstance(p, str):
            result.append(p)
        elif isinstance(p, dict):
            result.append(_s(p.get("text", "")))
    return result


def _build_plan_brief(
    grammar_point: str,
    age_group: str,
    l1_languages: str,
    slide_plan: list[dict],
) -> str:
    """Build a brief task_brief for InsertNewSlides (max 2000 chars)."""
    type_summary: dict[str, int] = {}
    for s in slide_plan:
        st = s["type"]
        type_summary[st] = type_summary.get(st, 0) + 1
    lines = [
        f"Grammar: {grammar_point} | Age: {age_group} | L1: {l1_languages}",
        f"Total slides: {len(slide_plan)}",
        f"Types: {', '.join(f'{k}={v}' for k, v in sorted(type_summary.items()))}",
    ]
    return "\n".join(lines)


# ── Individual Task Brief Builders ──────────────────────────────────────────

def _build_a0_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A0 Lesson Plan Cover task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    meaning = grammar_data.get("meaning", {})
    core_meaning = _s(meaning.get("core_meaning", meaning.get("short_meaning", "")))
    ccqs = meaning.get("ccqs") or []
    common_errors: list = grammar_data.get("common_errors") or []
    sub_rules: list = grammar_data.get("sub_rules") or []
    has_phonetics = bool(grammar_data.get("phonetics"))
    l1_list = [l.strip() for l in l1_languages.split(",") if l.strip()]
    form = grammar_data.get("form", {})

    # Count slide plan components for stage plan
    has_a2 = any(s["type"] == "A2" for s in [slide_meta])
    ccq_count = len(ccqs)
    formula_count = sum(
        1 for k in ("affirmative", "negative", "questions") if isinstance(form.get(k), dict) and form[k].get("structure")
    )
    sub_rule_count = len(sub_rules)
    l1_count = len(l1_list)

    support, extension = _get_differentiation(grammar_data)
    kp = _get_key_principles(grammar_data)

    # Pick top 3 anticipated errors
    errors = common_errors[:3] if common_errors else []

    lines = [
        f"Slide title: {grammar_point} — Lesson Plan",
        "Slide type: A0 Lesson Plan Cover",
        "Section: 0 of 8 (teacher briefing — first slide, not shown to students)",
        f"Grammar point: {grammar_point}",
        "Level: B1",
        f"Age group: {age_group}",
        f"L1 language(s): {l1_languages}",
        f"WATERMARK: {_WATERMARK}",
        "",
        "LESSON OBJECTIVE (from YAML meaning.core_meaning — paste verbatim):",
        f'"{core_meaning}"',
        "",
        "STAGE PLAN (estimate durations for a 45–50 min lesson):",
        "| Stage | Content | Slides | Time |",
        "|-------|---------|--------|------|",
        "| Warm-up / Hook | Contextual scene | 2–3 | 5 min |",
        "| Meaning | Core meaning + contrast | 1 | 5 min |",
        f"| CCQs | Concept check questions | {ccq_count} | 8 min |",
        f"| Formula | Affirmative / Negative / Questions | {formula_count} | 10 min |",
        f"| Practice | Gap-fill, error correction, L1 drill | 3 | 12 min |",
        f"| L1 Oracle | {l1_languages} error patterns | {l1_count} | 5 min |",
        "| Wrap-up | Key takeaway | 1 | 5 min |",
        "",
        "CCQ PREVIEW (paste ALL CCQs verbatim from YAML meaning.ccqs):",
    ]
    for i, ccq in enumerate(ccqs):
        q = _s(ccq.get("question") if isinstance(ccq, dict) else "")
        a = _s(ccq.get("answer") if isinstance(ccq, dict) else "")
        lines.append(f"  {i+1}. Q: {q} → A: {a}")

    lines.append("")
    lines.append("ANTICIPATED ERRORS — Top L1 patterns:")
    for i, err in enumerate(errors):
        wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
        correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
        lines.append(f"  Error {i+1}: Wrong: \"{wrong}\" → Correct: \"{correct}\"")

    lines.append("")
    lines.append("DIFFERENTIATION:")
    lines.append(f"  Support: {support}" if support else "  Support: Provide written examples and model the first item.")
    lines.append(f"  Extension: {extension}" if extension else "  Extension: Ask students to create their own examples.")

    if kp:
        lines.append("")
        lines.append("KEY PRINCIPLES:")
        for p in kp[:3]:
            lines.append(f"- {p}")

    lines.append("")
    lines.append("DESIGN:")
    lines.append("- Light background (#f8fafc). Dark teal (#0b7272) header bar. Two-column layout.")
    lines.append("- Left column: lesson objective + stage plan table.")
    lines.append("- Right column: CCQ preview + anticipated errors + differentiation.")
    lines.append("- Section labels in teal with 4px left border.")
    lines.append("- Error examples: wrong in red, correct in green.")
    lines.append("- Do NOT add a watermark to this slide (it is teacher-only).")

    return "\n".join(lines)


def _build_a0b_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A0b Student Intro — a visually stunning class opener.

    This is the FIRST slide students see when the lesson is projected.
    Minimal content: just the topic name + a tagline + visual impact.
    """
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    meaning = grammar_data.get("meaning", {})
    core_meaning = _s(meaning.get("core_meaning", meaning.get("short_meaning", "")))
    use_data = grammar_data.get("use") or []
    tagline = ""
    if isinstance(use_data, list) and use_data:
        first_use = use_data[0]
        if isinstance(first_use, dict):
            tagline = _s(first_use.get("context", first_use.get("description", first_use.get("use", ""))))
        else:
            tagline = _s(first_use)
    if not tagline:
        tagline = core_meaning

    lines = [
        f"Slide title: {grammar_point}",
        "Slide type: A0b Student Intro — class opening slide",
        "Section: 0b of 8 (student-facing opener — shown to class when lesson begins)",
        f"Grammar point: {grammar_point}",
        f"Age group: {age_group}",
        "WATERMARK: none",  # No watermark — this is the brand preview
        "",
        "TAGLINE (one line summarizing the grammar's purpose — paste verbatim below):",
        f'"{tagline}"',
        "",
        "CORE MEANING (from YAML meaning.core_meaning — paste verbatim):",
        f'"{core_meaning}"',
        "",
        "DESIGN GUIDELINES — THIS IS THE MOST IMPORTANT SLIDE FOR FIRST IMPRESSIONS:",
        "- FULL-BLEED design. The ENTIRE 1280×720 canvas. No border, no card.",
        "- Grammar point title: large, bold, elegant typography (60-80px)",
        "- Tagline: smaller, lighter, underneath the title (24-28px)",
        "- Minimal content — this is a VISUAL opener, not a teaching slide",
        "- Background: use the CSS variables from _theme.css (var(--bg), var(--primary), etc.)",
        "- Consider: gradient background, large geometric decoration, subtle pattern overlay",
        "- The mood/emotion should match the grammar:",
        "  * Present Simple → organized, routine-like (grid, lines, structured)",
        "  * Past tense → nostalgic (warm overlay, softer shapes)",
        "  * Future → forward-looking (arrows, upward motion, lighter at top)",
        "  * Conditionals → dreamy, hypothetical (overlapping circles, soft blur)",
        "  * Modals (can/should) → empowering (bold shapes, centered, confident)",
        "  * Questions → curious (question marks, playful arrangement)",
        "- Include a subtle CogniESL logo/brand mark in bottom-right at low opacity",
        "- SPEAKER NOTES: Brief teacher script: 'Today we're learning [topic]. [Tagline]. Let's get started.'",
        "- This slide sets the visual theme — all subsequent slides will use the same _theme.css",
    ]

    return "\n".join(lines)


def _build_a1_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A1 Hook slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    use_data = grammar_data.get("use", [])
    # use_data can be a list of context strings in the YAML
    if isinstance(use_data, list):
        use_contexts = use_data
    elif isinstance(use_data, dict):
        use_contexts = use_data.get("contexts") or use_data.get("examples") or []
    else:
        use_contexts = []
    teaching = grammar_data.get("teaching", {})
    tips = _get_teaching_tips(grammar_data)
    methodology = _s(teaching.get("methodology", ""))

    lines = [
        f"Slide title: Let's Explore {grammar_point}",
        "Slide type: A1 Contextual Hook",
        "Section: 1 of 8",
        f"Grammar point: {grammar_point}",
        f"Age group: {age_group}",
        "HOOK_IMAGE: ../images/hook.jpg",
        "",
        "YAML CONTEXT DATA — use these verbatim to build the scene:",
    ]
    for ctx in use_contexts[:2]:
        ctx_text = _s(ctx.get("context", ctx.get("text", ctx))) if isinstance(ctx, dict) else _s(ctx)
        lines.append(f"  Use context: {ctx_text}")

    if tips:
        lines.append("")
        lines.append("VISUAL TEACHING SUGGESTION (from teaching.tips):")
        lines.append(f"  {tips[0]}")

    lines.append("")
    lines.append("SCENE: Build a real-world scenario around the use context above. Show the grammar appearing naturally in dialogue or caption — without labeling it.")
    lines.append("")
    lines.append("SPEAKER NOTES: Teacher talk: Show this slide without explaining. Ask 'What do you notice? What's the person saying/doing?'")
    lines.append(f"  Teaching methodology: {methodology}")
    lines.append("  Watch for: Students trying to guess the rule — redirect to observation.")

    return "\n".join(lines)


def _build_a2_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A2 Meaning Overview slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    meaning = grammar_data.get("meaning", {})
    core = _s(meaning.get("core_meaning", meaning.get("short_meaning", "")))
    contrast = _s(meaning.get("contrast", meaning.get("long_meaning", "")))

    lines = [
        f"Slide title: What Is {grammar_point}?",
        "Slide type: A2 Meaning Overview",
        "Section: 2 of 8",
        f"Grammar point: {grammar_point}",
        "",
        "YAML MEANING DATA (use EXACTLY as written — this is what students need to understand):",
        f"  Core meaning: {core}",
        "",
        f"  Contrast: {contrast}",
        "",
        "DESIGN: Two-panel layout.",
        "Left panel (60%): large bold statement of core_meaning on a deep gradient background with a relevant FA icon (180px).",
        "Right panel (40%): contrast card showing the key distinctions — each item on its own colored row.",
        "No formulas yet. This slide answers: 'What IS this thing?'",
        "",
        "SPEAKER NOTES: Teacher talk: Read the core meaning aloud. Point to each contrast row and ask 'What's the difference?'",
        f"  CCQs: 'Can you give me one example of {grammar_point}?' 'Is it the same as [contrast item]?'",
        "  Watch for: Students confusing [grammar point] with the most common contrast item.",
    ]

    # Register notes if present
    register_notes = meaning.get("register_notes") or []
    if register_notes:
        lines.append("")
        lines.append("REGISTER NOTES DISPLAY (if register_notes data exists):")
        for rn in register_notes[:3]:
            text = _s(rn.get("text", rn)) if isinstance(rn, dict) else _s(rn)
            lines.append(f"  - {text}")

    return "\n".join(lines)


def _build_a3_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A3 CCQ Discovery slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    ccq_index = slide_meta.get("ccq_index", 0)
    ccq = _get_ccq(grammar_data, ccq_index)
    question = _s(ccq.get("question", ""))
    answer = _s(ccq.get("answer", ""))
    purpose = _s(ccq.get("purpose", ""))

    # Generate a short interesting title based on the first few words of the question
    short_q = question[:50].strip().rstrip("?.,")
    title = short_q if short_q else f"Check Your Understanding — {ccq_index + 1}"

    lines = [
        f"Slide title: {title}",
        "Slide type: A3 CCQ Discovery",
        "Section: 2 of 8",
        f"Grammar point: {grammar_point}",
        "",
        "YAML CCQ DATA (use EXACTLY as written):",
        f"  Question: {question}",
        f"  Answer: {answer}",
        f"  Purpose: {purpose}",
        "",
        "DESIGN: Hero layout. Large question card with the exact question text.",
        "Purple/indigo gradient background (signals 'thinking mode').",
        "Show the answer revealed below in a separate card with a checkmark icon.",
        "No formula yet — this is discovery only.",
        "",
        "SPEAKER NOTES: Teacher talk: Read the question aloud, give students 30 seconds to think.",
        f"  CCQs: {question}. Expected answer: {answer}.",
        "  Watch for: Students who jump to the formula — redirect to the question.",
    ]
    return "\n".join(lines)


def _build_a5_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A5 Grammar Formula slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    form_key = slide_meta.get("form_key", "affirmative")
    form_label = {"affirmative": "Affirmative", "negative": "Negative", "questions": "Questions"}
    form_data = _get_form_data(grammar_data, form_key)
    structure = _s(form_data.get("structure", ""))
    teaching = grammar_data.get("teaching", {})
    tips = _get_teaching_tips(grammar_data)
    common_errors: list = grammar_data.get("common_errors") or []
    l1_list = [l.strip().lower() for l in l1_languages.split(",") if l.strip()]

    # Filter common errors for this L1
    relevant_errors = []
    for e in common_errors:
        if not isinstance(e, dict):
            continue
        l1_groups = e.get("l1_groups") or e.get("l1_languages") or ""
        err_l1_str = _s(l1_groups).lower()
        if any(l1 in err_l1_str for l1 in l1_list) or not l1_list:
            relevant_errors.append(e)
        if len(relevant_errors) >= 2:
            break
    if not relevant_errors:
        relevant_errors = common_errors[:2]

    lines = [
        f"Slide title: The Formula — {form_label[form_key]}",
        f"Slide type: A5 Grammar Formula — {form_label[form_key]}",
        "Section: 4 of 8",
        f"Grammar point: {grammar_point}",
        "",
        "YAML FORM DATA (use EXACTLY as written — do NOT invent a formula):",
        f"  Structure: {structure}",
    ]

    if tips:
        lines.append("")
        lines.append("RELEVANT TEACHING TIP:")
        lines.append(f"  {tips[0]}")

    if relevant_errors:
        lines.append("")
        lines.append("COMMON ERRORS TO SHOW (filtered for specified L1 groups — paste verbatim):")
        for i, err in enumerate(relevant_errors):
            wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
            correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
            l1_g = err.get("l1_groups", "")
            lines.append(f"  Error {i+1}: {wrong} (wrong) → {correct} (correct)")
            if l1_g:
                lines.append(f"           L1 groups: {l1_g}")

    lines.extend([
        "",
        "SPEAKER NOTES: Teacher talk: Point to each formula part. Read aloud: '[exact structure]'.",
        "  Drill: give students a prompt, they produce the sentence.",
    ])
    if relevant_errors:
        lines.append(f"  Watch for: {_s(relevant_errors[0].get('wrong', relevant_errors[0].get('example_wrong', '')))}")

    return "\n".join(lines)


def _build_a5_sub_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A5 Sub-rule slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    sub_idx = slide_meta.get("sub_rule_index", 0)
    rule_data = _get_sub_rule(grammar_data, sub_idx)
    rule = _s(rule_data.get("rule", rule_data.get("text", "")))
    examples = rule_data.get("examples", [])
    if isinstance(examples, str):
        examples_text = examples
    else:
        examples_text = ", ".join(_s(e) for e in examples[:5]) if examples else ""
    explanation = _s(rule_data.get("explanation", ""))

    lines = [
        f"Slide title: {rule[:80]}" if rule else f"Rule {sub_idx + 1}",
        "Slide type: A5 Sub-rule",
        "Section: 3 of 8",
        f"Grammar point: {grammar_point}",
        "",
        "YAML SUB-RULE DATA (use EXACTLY as written):",
        f"  Rule: {rule}",
        f"  Examples: {examples_text}",
        f"  Explanation: {explanation}",
        "",
        "DESIGN: Visual contrast layout. Left: rule card. Right: examples in two columns.",
        "Use FA icons for pronunciation cues (fa-volume-up).",
        "",
        "SPEAKER NOTES: Teacher talk: [paste from YAML teaching.tips if relevant].",
        "  CCQs: Which sound does this word start with? Not which letter — which SOUND?",
        "  Watch for: Students looking at spelling instead of sound.",
    ]
    return "\n".join(lines)


def _build_a5b_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A5b Pronunciation Guide slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    phonetics = grammar_data.get("phonetics", {})
    # phonetics can be a dict with 'groups' or a list of sound strings
    groups = phonetics.get("groups") if isinstance(phonetics, dict) else (phonetics if isinstance(phonetics, list) else [])
    spelling_rule = _s(phonetics.get("spelling_rule", "")) if isinstance(phonetics, dict) else ""
    teacher_tip = _s(phonetics.get("teacher_tip", "")) if isinstance(phonetics, dict) else ""

    lines = [
        f"Slide title: How to Say It — {grammar_point}",
        "Slide type: A5b Pronunciation Guide",
        "Section: 5b of 8",
        f"Grammar point: {grammar_point}",
        f"WATERMARK: {_WATERMARK}",
        "",
        "SOUND GROUPS (from YAML phonetics):",
    ]
    for g in groups:
        if isinstance(g, dict):
            sound = _s(g.get("sound", g.get("phoneme", "")))
            words = g.get("words") or g.get("examples") or []
            words_str = ", ".join(_s(w) for w in words[:3])
            lines.append(f"  /{sound}/: {words_str}")
        elif isinstance(g, str):
            if "/" in g:
                parts = g.split(":", 1)
                if len(parts) == 2:
                    lines.append(f"  {parts[0].strip()}: {parts[1].strip()}")
                else:
                    lines.append(f"  {g}")

    if spelling_rule:
        lines.append(f"\n  SPELLING RULE: {spelling_rule}")
    if teacher_tip:
        lines.append(f"\n  TEACHER TIP: {teacher_tip}")

    # L1-specific phonology notes
    for l1_data in l1_data_list:
        l1_name = _s(l1_data.get("language", l1_data.get("name", "")))
        phonology = l1_data.get("phonology_interference") or l1_data.get("phonetics", {})
        if isinstance(phonology, dict) and phonology.get("notes"):
            lines.append(f"\n  L1 DIFFICULTY ({l1_name}): {_s(phonology.get('notes', ''))}")

    lines.append("")
    lines.append("SPEAKER NOTES: Model the sounds: 'Listen: /[sound]/ — [word1], [word2]. Now you...'")
    lines.append("  Drill technique: choral repetition. Watch for: L1-specific struggle from task_brief if present.")

    return "\n".join(lines)


def _build_a6_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A6 L1 Oracle slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    l1_language = slide_meta.get("l1_language", "")
    l1_data = _get_l1_data(l1_data_list, l1_language)

    patterns = _pick_tier1_2_patterns(l1_data)
    why_happens = _s(l1_data.get("why_it_happens", ""))
    teacher_tips = l1_data.get("teacher_tips", {})
    how_to_explain = _s(teacher_tips.get("how_to_explain", ""))
    sequencing = _s(teacher_tips.get("sequencing", ""))

    lines = [
        f"Slide title: {l1_language} Speakers: Watch Out!",
        f"Slide type: A6 L1 Oracle — {l1_language}",
        "Section: SECOND-TO-LAST (always placed just before the wrap-up section)",
        f"Grammar point: {grammar_point}",
        f"L1 language: {l1_language}",
        "",
        "QUALITY FILTER — MANDATORY:",
        "- ✅ Include: tier 1 (verified by 2+ sources) and tier 2 (verified by 1 source)",
        "- ❌ Exclude: tier 3 (LLM-only, unverified)",
        "",
        "YAML INTERFERENCE DATA — paste ALL tier 1 and tier 2 patterns with frequency ≥ 3 or persistence ≥ 3:",
        "",
    ]

    # WHY IT HAPPENS headline
    headline = why_happens[:120] if why_happens else f"Common errors {l1_language} speakers make with {grammar_point}"
    lines.append(f'WHY IT HAPPENS (HEADLINE): "{headline}"')
    if why_happens:
        lines.append(f'  Full explanation for speaker notes: "{why_happens}"')
    lines.append("")

    # Determine etiology for WHY explanation style
    etiology = _s(patterns[0].get("etiology", "unknown")) if patterns else "unknown"
    lines.append(f"  Etiology: {etiology} → Use this style for WHY headline")

    # Pattern cards
    for i, p in enumerate(patterns[:5]):
        wrong = _s(p.get("example_wrong", p.get("wrong", "")))
        correct = _s(p.get("example_correct", p.get("correct", "")))
        tier = p.get("tier", "legacy")
        freq = _as_int(p.get("frequency", 0))
        persist = _as_int(p.get("persistence", 0))
        impact = _as_int(p.get("communicative_impact", 0))
        l1_example = _s(p.get("example_l1", ""))

        lines.append(f"Pattern {i+1}:")
        lines.append(f'  Wrong: "{wrong}"')
        lines.append(f'  Correct: "{correct}"')
        lines.append(f"  Priority: Frequency {freq}/5, Persistence {persist}/5, Impact {impact}/5")
        lines.append(f"  Tier: {tier}")
        if l1_example:
            gloss = _s(p.get("example_gloss", ""))
            lines.append(f'  L1 example: "{l1_example}"' + (f' / Gloss: "{gloss}"' if gloss else ""))
        lines.append("")

    # Teacher script
    if how_to_explain:
        lines.append(f"Teacher script (paste COMPLETE text verbatim from teacher_tips.how_to_explain):")
        lines.append(f'  "{how_to_explain}"')
        lines.append("")

    if sequencing:
        lines.append(f"Teacher sequencing note (paste from teacher_tips.sequencing):")
        lines.append(f'  "{sequencing}"')
        lines.append("")

    lines.extend([
        "DESIGN:",
        "- TOP: Large teacher-readable headline = the WHY IT HAPPENS explanation. Big font, high contrast.",
        "- BELOW THE HEADLINE: 2x2 card grid (or vertical cards for 2 patterns) — each card shows:",
        '  LEFT side of card: ❌ "[wrong sentence]" in red',
        '  RIGHT side of card: ✅ "[correct sentence]" in green, with the corrected word highlighted yellow',
        "  Center between pairs: VS badge",
        "- BOTTOM STRIP: Dark card confirming the linguistic reason in brief (1 sentence from why_it_happens)",
        '- Make the contrast SHOCKING and MEMORABLE — this slide must make teachers feel "my students do exactly that"',
        "",
        "SPEAKER NOTES:",
    ])
    if why_happens:
        lines.append(f'  Full why_it_happens: "{why_happens}"')
    if how_to_explain:
        lines.append(f'  Suggested teacher script: "{how_to_explain}"')
    if sequencing:
        lines.append(f'  Sequencing: "{sequencing}"')
    lines.extend([
        '  Teacher talk: Show the headline first, read it aloud. Then reveal the card grid one row at a time.',
        "  Ask: 'Is this correct? No! Why not?' Then show the green card. Explain WHY using the headline.",
        "  CCQs: 'What is missing in the wrong sentence?' 'What word do we need to add?'",
        f"  Watch for: {wrong if patterns else 'common L1 error pattern in the next activity'}.",
    ])

    return "\n".join(lines)


def _build_a7_gap_fill_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A7 Practice slide (gap-fill from common_errors) task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    practice_index = slide_meta.get("practice_index", 0)
    labels = ["Spot the Mistake", "Fill the Gap", "Fix the Error"]
    title = labels[practice_index] if practice_index < len(labels) else "Practice"
    errors = _pick_errors_for_gapfill(grammar_data, l1_languages, 4)

    lines = [
        f"Slide title: {title}",
        "Slide type: A7 Controlled Practice — Gap Fill",
        "Section: 6 of 8",
        f"Grammar point: {grammar_point}",
        "",
        f"YAML SOURCE — common_errors filtered for L1 groups:",
    ]
    for i, err in enumerate(errors[:4]):
        wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
        correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
        explanation = _s(err.get("explanation", ""))
        lines.append(f"  Item {i+1}: wrong=\"{wrong}\" / correct=\"{correct}\" / explanation=\"{explanation}\"")

    lines.extend([
        "",
        "SPEAKER NOTES: Teacher talk: Students work alone for 2 minutes, then compare with a partner.",
    ])
    if errors:
        lines.append(f'  Watch for: {_s(errors[0].get("wrong", errors[0].get("example_wrong", "")))}')

    return "\n".join(lines)


def _build_a8_brief(
    slide_meta: dict,
    grammar_data: dict,
    l1_data_list: list[dict],
    age_group: str,
    l1_languages: str,
) -> str:
    """Build A8 Wrap-up slide task_brief."""
    grammar_point = _s(grammar_data.get("title", grammar_data.get("name", grammar_data.get("topic", ""))))
    meaning = grammar_data.get("meaning", {})
    core = _s(meaning.get("core_meaning", meaning.get("short_meaning", "")))
    common_errors: list = grammar_data.get("common_errors") or []
    l1_list = [l.strip().lower() for l in l1_languages.split(",") if l.strip()]
    kp = _get_key_principles(grammar_data)

    # Pick most relevant L1 error for the wrap-up
    l1_error = ""
    l1_correct = ""
    for err in common_errors:
        if not isinstance(err, dict):
            continue
        l1_groups = _s(err.get("l1_groups", "")).lower()
        if any(l1 in l1_groups for l1 in l1_list):
            l1_error = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
            l1_correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
            break
    if not l1_error and common_errors:
        err = common_errors[0]
        l1_error = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))) if isinstance(err, dict) else "")
        l1_correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))) if isinstance(err, dict) else "")

    lines = [
        f"Slide title: Key Takeaways",
        "Slide type: A8 Wrap-up",
        "Section: SECTION 7 (Always before closing brand slide)",
        f"Grammar point: {grammar_point}",
        "",
        "WRAP-UP CONTENT:",
        f"- Key takeaway: {core}",
    ]
    if l1_error:
        lines.append(f'- Most frequent L1 error: Wrong: "{l1_error}" → Correct: "{l1_correct}"')

    if kp:
        lines.append("")
        lines.append("KEY PRINCIPLE (if key_principles data exists):")
        lines.append(f"- {kp[0]}")

    lines.extend([
        "",
        "SPEAKER NOTES: Teacher talk: 'Let's review what we learned today. [Read key takeaway]. "
        "Remember, [L1] speakers often say [wrong example] — make sure you say [correct example].'",
        "  CCQs: [1-2 rapid-fire review questions matching the CCQ section]",
        "  Watch for: Students still making the same L1 error — redirect to the correct form.",
    ])

    return "\n".join(lines)
