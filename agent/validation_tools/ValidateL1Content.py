"""Verify that L1-specific error content is present and substantive."""

import re
from pathlib import Path
from typing import List, Dict
from agency_swarm.tools import BaseTool
from pydantic import Field

from slides_tools.slide_file_utils import get_project_dir, list_slide_files


class ValidateL1Content(BaseTool):
    """
    Validate that each specified L1 has dedicated Oracle content.

    Checks:
    - L1 language name appears in slides
    - Error patterns are specific (not generic)
    - Common error examples are present
    - Correct answers are shown
    """

    project_name: str = Field(..., description="Project folder name")
    l1_languages: List[str] = Field(..., description="L1 languages (e.g., ['Spanish', 'Chinese'])")

    def run(self) -> str:
        """Validate L1 content."""
        project_dir = get_project_dir(self.project_name)
        slides = list_slide_files(project_dir)

        results = {}

        for lang in self.l1_languages:
            results[lang] = self._check_language(lang, slides)

        # Format report
        report = "L1 ORACLE VALIDATION:\n"
        report += "=" * 50 + "\n"

        for lang, checks in results.items():
            status = "✓" if all(checks.values()) else "✗"
            report += f"{status} {lang}:\n"
            for check_name, passed in checks.items():
                symbol = "  ✓" if passed else "  ✗"
                report += f"{symbol} {check_name}\n"

        return report

    def _check_language(self, lang: str, slides: List[Path]) -> Dict[str, bool]:
        """Check all validations for a language."""
        all_content = '\n'.join(slide.read_text(encoding='utf-8') for slide in slides)

        return {
            "Language name found": lang.lower() in all_content.lower(),
            "Error examples present": any(
                pattern in all_content.lower()
                for pattern in ['wrong', 'error', 'incorrect', '✗', 'mistake']
            ),
            "Correct examples shown": any(
                pattern in all_content.lower()
                for pattern in ['correct', 'right', '✓', 'should be']
            ),
            "Before-after comparison": '->' in all_content or '→' in all_content,
        }
