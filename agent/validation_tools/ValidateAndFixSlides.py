"""Automatically retry failed slides or regenerate them."""

import asyncio
from pathlib import Path
from typing import List
from agency_swarm.tools import BaseTool
from pydantic import Field

from slides_tools.slide_file_utils import get_project_dir
from slides_tools.ModifySlide import ModifySlide

# Minimum characters in a task_brief for us to trust it contains real YAML content.
# A generic fallback like "Create ESL teaching slide for slide_03" is ~44 chars.
# A YAML-rich brief should be at least 300 chars.
_MIN_BRIEF_LENGTH = 300

_YAML_SIGNALS = [
    "ccq",
    "interference",
    "example_wrong",
    "example_correct",
    "why_it_happens",
    "sub_rule",
    "teacher_tip",
    "speaker notes:",
    "yaml",
    "wrong:",
    "correct:",
    "frequency:",
    "persistence:",
]


def _brief_has_yaml_content(brief: str) -> bool:
    """Return True if the brief appears to contain actual YAML database content."""
    if len(brief) < _MIN_BRIEF_LENGTH:
        return False
    brief_lower = brief.lower()
    return any(sig in brief_lower for sig in _YAML_SIGNALS)


class ValidateAndFixSlides(BaseTool):
    """
    Re-validate slides and automatically fix empty/failed ones.

    CRITICAL: task_briefs MUST contain actual YAML excerpts for each slide.
    A brief like "Create ESL teaching slide for slide_03" produces output just
    as poor as the original failed slide. Include verbatim YAML content:
    - For CCQ slides: the exact question/answer from grammar YAML ccqs[]
    - For L1 Oracle slides: interference_patterns, example_wrong, example_correct,
      why_it_happens from L1 interference YAML
    - For formula slides: the exact structure string from form.affirmative/negative
    - For sub_rule slides: the exact rule, examples, and explanation from sub_rules[]

    Example of a good task_brief (L1 Oracle slide):
    ---
    Slide title: L1 Oracle — Portuguese Errors
    Slide type: L1 error correction (red/green contrast layout)
    Grammar point: articles (a, an, the)
    L1 language: Portuguese

    YAML INTERFERENCE DATA:
    Pattern: Omission of indefinite article before profession nouns
    Wrong: "She is doctor."
    Correct: "She is a doctor."
    Why it happens: Portuguese uses articles with professions differently — speakers
      transfer the L1 pattern where article omission is acceptable.
    Frequency: 4/5, Persistence: 4/5, Communicative Impact: 3/5

    Teacher tip: Drill "a/an + profession" using flashcards. Ask "What does she do?"
    and prompt "She is A doctor" with heavy stress on A.

    SPEAKER NOTES: Teacher talk: Show the wrong sentence and ask 'What's missing?'
    CCQs: Do we say 'She is doctor' or 'She is A doctor'? Why? Watch for: Students
    omitting A/AN before all singular countable nouns after professions.
    ---
    """

    project_name: str = Field(..., description="Project folder name")
    slide_names_to_fix: List[str] = Field(
        ...,
        description="List of slide names that failed validation (e.g., ['slide_03', 'slide_07'])"
    )
    task_briefs: dict = Field(
        default_factory=dict,
        description=(
            "Map of slide_name -> task_brief for regeneration. "
            "EACH task_brief MUST include verbatim YAML content (CCQs, interference patterns, "
            "examples, sub-rules, etc.). A generic description will produce equally thin output."
        )
    )

    def run(self) -> str:
        """Regenerate failed slides."""
        if not self.slide_names_to_fix:
            return "No slides to fix."

        results = []
        warnings = []

        for slide_name in self.slide_names_to_fix:
            task_brief = self.task_briefs.get(slide_name, "")

            # Warn loudly if the brief is missing or has no YAML content
            if not task_brief:
                warnings.append(
                    f"⚠️  {slide_name}: No task_brief provided. "
                    "Regeneration will produce thin, generic output. "
                    "Provide a YAML-rich task_brief with actual CCQs, interference patterns, "
                    "and examples from the database."
                )
                task_brief = (
                    f"Create an ESL teaching slide for {slide_name}. "
                    "WARNING: No YAML data was provided for this regeneration. "
                    "Make the slide as visually rich as possible given minimal context. "
                    "Include speaker notes with CCQs and watch-for errors."
                )
            elif not _brief_has_yaml_content(task_brief):
                warnings.append(
                    f"⚠️  {slide_name}: task_brief appears to lack YAML content "
                    f"({len(task_brief)} chars, no YAML signals detected). "
                    "Output quality will be poor without actual database excerpts."
                )

            modify_tool = ModifySlide(
                project_name=self.project_name,
                slide_name=slide_name,
                task_brief=task_brief,
            )

            try:
                result = asyncio.run(modify_tool.run())
                results.append(f"✓ {slide_name}: Regenerated successfully")
            except Exception as e:
                results.append(f"✗ {slide_name}: Failed — {e}")

        output_parts = []
        if warnings:
            output_parts.append("WARNINGS (address these for quality output):")
            output_parts.extend(warnings)
            output_parts.append("")
        output_parts.append("RESULTS:")
        output_parts.extend(results)

        return "\n".join(output_parts)
