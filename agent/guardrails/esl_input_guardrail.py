"""Input guardrail: Keeps the agent focused on ESL topics."""
from agency_swarm import Agent, GuardrailFunctionOutput, RunContextWrapper, input_guardrail


@input_guardrail
async def require_esl_topic(
    context: RunContextWrapper,
    agent: Agent,
    user_input: str | list[str],
) -> GuardrailFunctionOutput:
    """Validate that user input is ESL-related before it reaches the agent."""
    text = user_input if isinstance(user_input, str) else " ".join(user_input)
    text_lower = text.lower()

    # Broad ESL indicator list — covers grammar terms, teaching terms, CEFR levels
    esl_indicators = [
        "grammar", "english", "esl", "efl", "worksheet", "slide", "lesson",
        "activity", "exercise", "practice", "vocabulary", "pronunciation",
        "tense", "verb", "noun", "article", "preposition", "conditional",
        "present", "past", "future", "perfect", "continuous",
        "homework", "flashcard", "quiz", "test", "assessment",
        "teaching", "class", "student", "learner", "beginner", "teacher",
        "a1", "a2", "b1", "b2", "c1", "cefr",
        "l1", "interference", "error", "mistake", "correction",
        "a and an", "make do", "collocation", "phrasal", "idiom",
        "handout", "printable", "pdf", "exercise sheet",
        "curriculum", "syllabus", "lesson plan", "unit plan",
        "warm-up", "icebreaker", "drill", "game",
        # Common ESL question patterns
        "correct", "incorrect", "right or wrong",
        "difference between", "how do i", "when do i",
        "can i say", "what does", "which one",
        "much", "many", "say in english", "how to say",
        "mean?", "synonym", "antonym", "spell",
        "pronounce", "pronunciation of",
    ]

    is_esl = any(indicator in text_lower for indicator in esl_indicators)

    # Always allow follow-ups (short messages, clarifications)
    is_short_followup = len(text.split()) <= 5

    if is_esl or is_short_followup:
        return GuardrailFunctionOutput(
            output_info="",
            tripwire_triggered=False,
        )

    return GuardrailFunctionOutput(
        output_info=(
            "I'm here to create ESL teaching materials! Tell me what grammar "
            "point you'd like to cover and I'll build slides, worksheets, or "
            "activities for your students. For example: 'I need a lesson on "
            "present simple for Portuguese speakers.'"
        ),
        tripwire_triggered=True,
    )
