"""Output guardrails: Validate agent responses before they reach the teacher."""
import re
from agency_swarm import Agent, GuardrailFunctionOutput, RunContextWrapper, output_guardrail


@output_guardrail
async def validate_l1_content(
    context: RunContextWrapper,
    agent: Agent,
    response_text: str,
) -> GuardrailFunctionOutput:
    """Validate that L1 interference data is included when relevant."""
    has_l1_section = "L1" in response_text
    has_error_pairs = "✗" in response_text and "✓" in response_text

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
        if count < 16:
            return GuardrailFunctionOutput(
                output_info=(
                    f"Your Slide Plan has {count} slides but standard grammar topics "
                    f"need minimum 16 (1 lesson plan cover + 1 hook + 1 meaning + "
                    f"2-3 CCQs + 1 affirmative + 1 negative + 1 question + "
                    f"1-2 sub-rules + 3 practice + 1-2 L1 Oracle + 1 wrap-up + "
                    f"1 closing brand). You're missing at least {16 - count} slides. "
                    f"Add the missing sections."
                ),
                tripwire_triggered=True,
            )

    return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)