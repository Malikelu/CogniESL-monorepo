"""Output guardrails: Validate agent responses before they reach the teacher."""
import re
from agency_swarm import Agent, GuardrailFunctionOutput, RunContextWrapper, output_guardrail


@output_guardrail
async def validate_l1_content(
    context: RunContextWrapper,
    agent: Agent,
    response_text: str,
) -> GuardrailFunctionOutput:
    """Validate that L1 interference data is included when relevant.

    This guardrail is intentionally narrow: it only fires on Content Brief
    responses, never on background generation completion messages.
    """
    # Skip short responses (confirmations, one-liners)
    if len(response_text.strip()) <= 500:
        return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)

    # Skip background generation completion messages.
    # After the background thread finishes, the agent returns something like
    # "Job XXXXXXXX marked complete. 17 file(s) registered." — which is long
    # but has no ✗/✓ symbols. Without this guard, the guardrail fires, causes
    # validation_attempts=2 retry, and can trigger a second generation run.
    text_lower = response_text.lower()
    is_job_completion = (
        "marked complete" in text_lower
        or "file(s) registered" in text_lower
        or "proceed_with_generation" in text_lower
        or "job_id=" in text_lower
        or ("generating" in text_lower and "background" in text_lower)
    )
    if is_job_completion:
        return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)

    # Only check responses that look like a Content Brief
    is_content_brief = "Content Brief" in response_text or "Slide Plan" in response_text
    if not is_content_brief:
        return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)

    has_l1_section = "L1" in response_text

    # Accept error pairs in either format:
    # - Slide/Oracle format: ✗ / ✓ symbols (used in HTML slides)
    # - Content Brief format: Wrong: "..." → Correct: "..." (used in teacher-facing briefs)
    has_error_pairs = (
        ("✗" in response_text and "✓" in response_text)
        or ("Wrong:" in response_text and "Correct:" in response_text)
        or ("wrong" in response_text.lower() and "correct" in response_text.lower() and "→" in response_text)
    )

    tripwire = not (has_l1_section and has_error_pairs)

    return GuardrailFunctionOutput(
        output_info=(
            "The teacher requested materials for specific L1 speakers. Your output "
            "must include an L1 Oracle section with wrong/correct error pairs (✗ → ✓) "
            "from the interference_patterns data. Place it before the exercises section."
        ) if tripwire else "",
        tripwire_triggered=tripwire,
    )


@output_guardrail
async def validate_citations(
    context: RunContextWrapper,
    agent: Agent,
    response_text: str,
) -> GuardrailFunctionOutput:
    """Flag vague attribution language that might indicate fabrication."""
    text_lower = response_text.lower()
    fabrication_indicators = [
        "according to research", "studies show", "experts say",
        "it is widely believed", "commonly thought", "some linguists argue",
        "research indicates", "studies suggest",
    ]
    # Only flag vague attribution if it is NOT followed by a specific citation
    # e.g., "According to research by Swan (2016)" has a citation and is OK
    import re as _re
    has_vague = False
    for indicator in fabrication_indicators:
        idx = text_lower.find(indicator)
        if idx == -1:
            continue
        # Look ahead for a citation pattern (year in parens, "by Author", etc.)
        # Use original case so [A-Z] patterns work
        after_original = response_text[idx + len(indicator):idx + len(indicator) + 80]
        if _re.search(r'(?i)\bby\s+[A-Za-z]+|\(\d{4}\)', after_original):
            continue  # Has a legitimate citation following the phrase
        has_vague = True
        break

    return GuardrailFunctionOutput(
        output_info=(
            "You used vague attribution like 'studies show' or 'experts say'. "
            "The YAML database has verified citations for every claim. Use the exact "
            "citation from the citations[] field, or omit the claim entirely."
        ) if has_vague else "",
        tripwire_triggered=has_vague,
    )


@output_guardrail
async def validate_slide_count(
    context: RunContextWrapper,
    agent: Agent,
    response_text: str,
) -> GuardrailFunctionOutput:
    """Validate standard grammar decks have at least 16 slides."""
    slide_count_match = re.search(r'Slide Plan\s*[—–-]+\s*(\d+)', response_text)

    if slide_count_match:
        count = int(slide_count_match.group(1))
        if count < 14:
            return GuardrailFunctionOutput(
                output_info=(
                    f"Your Slide Plan has {count} slides but standard grammar topics "
                    f"need minimum 16. Vocabulary or usage topics need minimum 14. "
                    f"You are missing at least {16 - count} slides. "
                    f"Add the missing sections: 1 cover + 1 hook + 1 meaning + "
                    f"2-3 CCQs + Affirmative + Negative + Question formulas + "
                    f"1-2 sub-rules + Pronunciation (if data exists) + "
                    f"3 practice + 1-2 L1 Oracle + 1 wrap-up + 1 closing brand."
                ),
                tripwire_triggered=True,
            )

    return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)