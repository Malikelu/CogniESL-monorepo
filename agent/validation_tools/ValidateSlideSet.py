"""Automated validation of all generated slides before PPTX build."""

import re
from pathlib import Path
from typing import List, Dict, Any
from agency_swarm.tools import BaseTool
from pydantic import Field

from slides_tools.slide_file_utils import get_project_dir, list_slide_files

# Minimum bytes for a slide to be considered populated.
# Placeholder (fallback) HTML is ~1,452 bytes. Real slides with CSS boilerplate
# start around 4,500–5,000 bytes. 4,500 separates real from placeholder
# while avoiding false positives on simpler slides (title, transition, CCQ).
_MIN_SLIDE_BYTES = 4500

# Signals that a slide contains CCQ/discovery content (before formulas)
_CCQ_SIGNALS = [
    "concept check",
    "ccq",
    "is this",
    "why do we",
    "was it",
    "first mention",
    "already known",
    "specific",
]

# Signals that a slide shows the grammar formula / structure
_FORMULA_SIGNALS = [
    "structure:",
    "subject +",
    "s + v",
    "affirmative",
    "formula",
    "formation",
    "equation",
    "verb +",
    "+ ing",
    "+ ed",
    "a + ",
    "an + ",
]

_FONT_AWESOME_CDN = "font-awesome"


class ValidationResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "all_pass": len(self.failed) == 0,
        }


class ValidateSlideSet(BaseTool):
    """
    Validate all slides before building PPTX.

    Checks:
    1. All slides have content (file size > 6000 bytes)
    2. Speaker notes exist on every slide
    3. L1 Oracle sections for each specified language
    4. CCQs appear BEFORE formula slides (deck ordering)
    5. No duplicate slides
    6. All slides have proper HTML structure
    7. Font Awesome CDN is loaded (for icons to render)
    8. Minimum visual content present (gradients / SVG / icons)
    """

    project_name: str = Field(..., description="Project folder name")
    slide_count: int = Field(
        ...,
        description="Expected number of slides from the generation plan"
    )
    l1_languages: List[str] = Field(
        default_factory=list,
        description="L1 languages that should have Oracle sections (e.g., ['Spanish', 'Chinese'])"
    )

    def run(self) -> str:
        """Run all validations and return detailed report."""
        project_dir = get_project_dir(self.project_name)
        slides = list_slide_files(project_dir)
        result = ValidationResult()

        # 1. Check slide count
        if len(slides) != self.slide_count:
            result.failed.append(
                f"Slide count mismatch: expected {self.slide_count}, got {len(slides)}"
            )
        else:
            result.passed.append(f"✓ Slide count correct ({len(slides)} slides)")

        # 2. Check each slide individually
        for slide_file in sorted(slides, key=lambda s: s.index):
            self._validate_slide(slide_file.path, result)

        # 3. Check CCQ ordering (CCQs must appear before formulas in the deck)
        self._validate_ccq_ordering(slides, result)

        # 4. Check L1 Oracle sections
        if self.l1_languages:
            self._validate_l1_sections([s.path for s in slides], result)

        # 5. Check for duplicate content
        self._validate_no_duplicates([s.path for s in slides], result)

        # 6. Summary
        status = "✓ PASSED" if result.to_dict()["all_pass"] else "✗ FAILED"

        report = f"""
VALIDATION REPORT: {status}

PASSED ({len(result.passed)}):
{self._format_list(result.passed)}

FAILED ({len(result.failed)}):
{self._format_list(result.failed)}

WARNINGS ({len(result.warnings)}):
{self._format_list(result.warnings)}

NEXT STEPS:
{self._next_steps(result.to_dict())}
"""
        return report.strip()

    def _validate_slide(self, slide_path: Path, result: ValidationResult):
        """Validate a single slide file."""
        slide_name = slide_path.stem

        # Check file size
        size = slide_path.stat().st_size
        if size < _MIN_SLIDE_BYTES:
            result.failed.append(
                f"{slide_name}: File too small ({size} bytes, minimum {_MIN_SLIDE_BYTES}) — "
                "thin content. Regenerate with full YAML data in the task_brief."
            )
            return

        # Read content
        try:
            content = slide_path.read_text(encoding="utf-8")
        except Exception as e:
            result.failed.append(f"{slide_name}: Cannot read file ({e})")
            return

        # Check HTML structure
        if not self._has_valid_html(content):
            result.failed.append(f"{slide_name}: Invalid HTML structure")
            return

        result.passed.append(f"✓ {slide_name}: Size OK ({size:,} bytes)")

        # Check Font Awesome CDN
        if _FONT_AWESOME_CDN not in content.lower():
            result.failed.append(
                f"{slide_name}: Missing Font Awesome CDN — icons will not render. "
                'Add: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'
            )
        else:
            result.passed.append(f"✓ {slide_name}: Font Awesome CDN present")

        # Check speaker notes
        if "data-speaker-notes" not in content:
            result.failed.append(f"{slide_name}: Missing speaker notes (data-speaker-notes attribute)")
        else:
            notes = self._extract_speaker_notes(content)
            if notes and len(notes.strip()) > 30:
                result.passed.append(f"✓ {slide_name}: Speaker notes present")
            else:
                result.warnings.append(
                    f"{slide_name}: Speaker notes attribute exists but content is very short"
                )

        # Check for meaningful visual content
        has_gradient = "gradient" in content.lower()
        has_fa_icon = "fa-" in content
        has_svg = "<svg" in content.lower()
        has_img = "<img" in content.lower()
        has_visual = has_gradient or has_fa_icon or has_svg or has_img

        if not has_visual:
            result.warnings.append(
                f"{slide_name}: No visual elements detected (no gradients, icons, SVG, or images) — "
                "violates 80/20 visual rule"
            )
        else:
            result.passed.append(f"✓ {slide_name}: Visual content present")

    def _validate_ccq_ordering(self, slides, result: ValidationResult):
        """Verify CCQs appear before formula slides in the deck."""
        first_ccq_index = None
        first_formula_index = None

        for i, slide_file in enumerate(sorted(slides, key=lambda s: s.index)):
            try:
                content = slide_file.path.read_text(encoding="utf-8").lower()
            except Exception:
                continue

            if first_ccq_index is None and any(sig in content for sig in _CCQ_SIGNALS):
                first_ccq_index = i

            if first_formula_index is None and any(sig in content for sig in _FORMULA_SIGNALS):
                first_formula_index = i

        if first_ccq_index is not None and first_formula_index is not None:
            if first_ccq_index < first_formula_index:
                result.passed.append(
                    f"✓ CCQ ordering correct: discovery (slide {first_ccq_index + 1}) "
                    f"appears before formula (slide {first_formula_index + 1})"
                )
            else:
                result.failed.append(
                    f"CCQ ordering WRONG: formula appears at slide {first_formula_index + 1} "
                    f"before CCQ at slide {first_ccq_index + 1}. "
                    "CCQs MUST come first — pedagogical rule A3 before A5."
                )
        elif first_ccq_index is None:
            result.warnings.append(
                "No CCQ signals found in any slide — verify that concept check questions "
                "appear in Section 2 before formulas."
            )
        elif first_formula_index is None:
            result.warnings.append(
                "No formula/structure signals found — verify formation rules appear in Section 2-3."
            )

    def _validate_l1_sections(self, slide_paths: List[Path], result: ValidationResult):
        """Check that L1 Oracle sections exist for each language."""
        all_content = ""
        for path in slide_paths:
            try:
                all_content += path.read_text(encoding="utf-8").lower()
            except Exception:
                pass

        for lang in self.l1_languages:
            lang_lower = lang.lower()
            lang_first_word = lang_lower.split()[0]  # e.g. "portuguese" from "Brazilian Portuguese"

            found = lang_lower in all_content or lang_first_word in all_content

            # Check for wrong→correct contrast markers alongside language mention
            has_contrast = found and (
                "→" in all_content
                or "-&gt;" in all_content
                or "wrong" in all_content
                or "correct" in all_content
                or "example_wrong" in all_content
            )

            if has_contrast:
                result.passed.append(f"✓ L1 Oracle content with error contrasts found for {lang}")
            elif found:
                result.warnings.append(
                    f"{lang} name appears in slides but no error contrast detected — "
                    "verify L1 Oracle slide has Wrong→Correct examples from YAML"
                )
            else:
                result.failed.append(
                    f"Missing L1 Oracle content for {lang} — "
                    "at least 1-2 dedicated slides with specific error examples REQUIRED"
                )

    def _validate_no_duplicates(self, slide_paths: List[Path], result: ValidationResult):
        """Check for slides with identical or near-identical text content."""
        seen_texts: dict[str, str] = {}
        duplicates_found = False
        for path in slide_paths:
            try:
                content = path.read_text(encoding="utf-8")
                # Strip all HTML tags and collapse whitespace
                text = re.sub(r"<[^>]+>", " ", content)
                text = re.sub(r"\s+", " ", text).strip()
                # Use a longer fingerprint (1500 chars) to catch near-duplicates
                fingerprint = text[:1500]
            except Exception:
                continue
            if fingerprint in seen_texts:
                result.failed.append(
                    f"DUPLICATE SLIDES: {path.stem} and {seen_texts[fingerprint]} have identical content. "
                    "Delete one and create a distinct slide for the missing section."
                )
                duplicates_found = True
            else:
                seen_texts[fingerprint] = path.stem

        if not duplicates_found:
            result.passed.append("✓ No duplicate slide content detected")

    def _has_valid_html(self, content: str) -> bool:
        return bool(re.search(r"<html|<!doctype", content, re.IGNORECASE))

    def _extract_speaker_notes(self, content: str) -> str:
        match = re.search(r'data-speaker-notes="([^"]*)"', content)
        return match.group(1) if match else ""

    def _format_list(self, items: List[str]) -> str:
        if not items:
            return "  (none)"
        return "\n".join(f"  • {item}" for item in items)

    def _next_steps(self, summary: dict) -> str:
        failed = summary.get("failed", [])
        if not failed:
            return "All checks passed! Call BuildPptxFromHtmlSlides to create the PPTX."

        size_fails = [f for f in failed if "too small" in f]
        fa_fails = [f for f in failed if "Font Awesome" in f]
        l1_fails = [f for f in failed if "L1 Oracle" in f]
        ccq_fails = [f for f in failed if "CCQ ordering" in f]

        steps = []
        if size_fails:
            steps.append(
                f"• {len(size_fails)} slide(s) too small: call ModifySlide with full YAML "
                "excerpts in task_brief (CCQs, interference patterns, examples verbatim from YAML)"
            )
        if fa_fails:
            steps.append(
                f"• {len(fa_fails)} slide(s) missing Font Awesome CDN: regenerate those slides"
            )
        if l1_fails:
            steps.append(
                "• Missing L1 Oracle: call ModifySlide with interference_patterns, "
                "example_wrong/correct, and why_it_happens from the L1 YAML"
            )
        if ccq_fails:
            steps.append(
                "• CCQ ordering wrong: CCQ/discovery slides must appear before formula slides"
            )

        return (
            "\n".join(steps)
            if steps
            else "Use ValidateAndFixSlides with YAML-rich task_briefs to regenerate failed slides."
        )
