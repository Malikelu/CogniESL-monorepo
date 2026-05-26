"""
GenerateFlashcardPdf — generate a print-and-cut flashcard PDF from YAML data.

Creates 10–15 flashcards:
  - Front: error sentence (in red, struck through) + L1 label
  - Back: correction (in teal) + brief 'why it happens' explanation

Two-page PDF: page 1 = all fronts, page 2 = all backs.
Print double-sided, flip on short edge, then cut along dashed lines.

Source: common_errors from grammar YAML + interference_patterns from L1 YAML.
"""

import json
import logging
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

log = logging.getLogger(__name__)

# ── Path helper ───────────────────────────────────────────────────────────────

def _get_project_dir(project_name: str) -> Path:
    """Return (and create) ./mnt/{project_name}/documents/."""
    import os
    base = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data")) / "mnt"
    if not base.parent.exists():
        # Local dev fallback
        base = Path(__file__).parent.parent.parent / "mnt"
    doc_dir = base / project_name / "documents"
    doc_dir.mkdir(parents=True, exist_ok=True)
    return doc_dir


# ── HTML template helpers ────────────────────────────────────────────────────

_HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  @page {{ size: A4; margin: 12mm 12mm 10mm; }}
  @media print {{
    .page-break {{ page-break-before: always; }}
    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}

  body {{
    font-family: 'Nunito', Arial, sans-serif;
    background: #fff;
    color: #1f2937;
  }}

  .page-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 2.5px solid {header_color};
    padding-bottom: 5px;
    margin-bottom: 8px;
  }}

  .page-header .badge {{
    background: {header_color};
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }}

  .page-header .meta {{
    font-size: 11px;
    color: #6b7280;
    flex: 1;
  }}

  .card-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5mm;
  }}

  .card {{
    border: 1.5px dashed #0b7272;
    border-radius: 7px;
    padding: 7px 10px;
    min-height: 48mm;
    max-height: 52mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
  }}

  .card-num {{
    position: absolute;
    top: 4px;
    right: 7px;
    font-size: 9px;
    color: #d1d5db;
    font-weight: 700;
  }}

  /* FRONT */
  .front .card {{ background: #fff8f8; }}
  .front .card-label {{
    font-size: 8.5px;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
  }}
  .front .error {{
    font-size: 15px;
    font-weight: 700;
    color: #dc2626;
    text-decoration: line-through;
    text-decoration-color: #fca5a5;
    line-height: 1.3;
    margin-bottom: 4px;
  }}
  .front .prompt {{
    font-size: 11px;
    color: #374151;
    line-height: 1.4;
    font-style: italic;
  }}
  .front .l1-tag {{
    display: inline-block;
    background: #fef2f2;
    color: #dc2626;
    font-size: 9px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 10px;
    border: 1px solid #fecaca;
    margin-top: 5px;
    align-self: flex-start;
  }}

  /* BACK */
  .back .card {{ background: #f0fdf4; }}
  .back .correct {{
    font-size: 16px;
    font-weight: 800;
    color: #0b7272;
    line-height: 1.3;
    margin-bottom: 5px;
  }}
  .back .why-label {{
    font-size: 8.5px;
    font-weight: 700;
    color: #1baa6e;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
  }}
  .back .why {{
    font-size: 10.5px;
    color: #374151;
    line-height: 1.45;
  }}

  .footer {{
    text-align: center;
    font-size: 8.5px;
    color: #9ca3af;
    margin-top: 7px;
    letter-spacing: 0.3px;
  }}
  .footer strong {{
    color: #0b7272;
  }}
</style>
</head>
<body>
"""

_HTML_FOOTER = "</body></html>\n"


def _card_front(num: int, error: str, context: str, l1_label: str) -> str:
    context_html = f'<div class="prompt">{_esc(context)}</div>' if context else ""
    l1_html = f'<span class="l1-tag">{_esc(l1_label)}</span>' if l1_label else ""
    return f"""
<div class="card">
  <span class="card-num">#{num}</span>
  <div>
    <div class="card-label">✗ Find the mistake</div>
    <div class="error">{_esc(error)}</div>
    {context_html}
  </div>
  <div>{l1_html}</div>
</div>"""


def _card_back(num: int, correct: str, why: str) -> str:
    why_html = ""
    if why:
        why_html = f'<div><div class="why-label">Why?</div><div class="why">{_esc(why)}</div></div>'
    return f"""
<div class="card">
  <span class="card-num">#{num}</span>
  <div class="correct">✓ {_esc(correct)}</div>
  {why_html}
</div>"""


def _esc(s: str) -> str:
    """Minimal HTML escape."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


# ── Card extraction ──────────────────────────────────────────────────────────

def _extract_cards(
    common_errors_json: str,
    l1_patterns_json: str,
    l1_language: str,
) -> list[dict]:
    """
    Build a list of card dicts from YAML data strings.

    Each dict: {error, correct, why, l1_label}
    """
    cards: list[dict] = []

    # 1. Grammar common_errors
    if common_errors_json:
        try:
            errors = json.loads(common_errors_json)
            if isinstance(errors, dict):
                errors = [errors]
            for item in errors[:7]:  # max 7 from grammar
                error = (
                    item.get("error") or item.get("wrong") or item.get("incorrect") or ""
                ).strip()
                correct = (
                    item.get("correction") or item.get("correct") or item.get("corrected") or ""
                ).strip()
                why = (item.get("explanation") or item.get("why") or "").strip()
                context = (item.get("context") or item.get("note") or "").strip()
                if error and correct:
                    cards.append({
                        "error": error,
                        "correct": correct,
                        "why": why or context,
                        "l1_label": "",
                    })
        except (json.JSONDecodeError, TypeError):
            log.warning("Could not parse common_errors_json")

    # 2. L1 interference patterns
    if l1_patterns_json and l1_language:
        try:
            patterns = json.loads(l1_patterns_json)
            if isinstance(patterns, dict):
                patterns = [patterns]
            added = 0
            for pattern in patterns:
                if added >= 8:
                    break
                # Each pattern may have examples list
                examples = pattern.get("examples") or []
                if isinstance(examples, str):
                    examples = [{"wrong": examples, "correct": ""}]
                why = (
                    pattern.get("why_it_happens")
                    or pattern.get("why")
                    or pattern.get("explanation")
                    or ""
                ).strip()
                # Use first example from the pattern
                if examples:
                    ex = examples[0] if isinstance(examples[0], dict) else {}
                    error = (
                        ex.get("wrong") or ex.get("incorrect") or ex.get("error") or ""
                    ).strip()
                    correct = (
                        ex.get("correct") or ex.get("correction") or ex.get("corrected") or ""
                    ).strip()
                    if error and correct:
                        cards.append({
                            "error": error,
                            "correct": correct,
                            "why": why,
                            "l1_label": f"{l1_language} error",
                        })
                        added += 1
                elif why:
                    # Pattern without examples — use pattern description as a hint card
                    interference = (
                        pattern.get("interference_pattern")
                        or pattern.get("pattern")
                        or pattern.get("description")
                        or ""
                    ).strip()
                    if interference:
                        cards.append({
                            "error": interference,
                            "correct": why,
                            "why": "",
                            "l1_label": f"{l1_language} pattern",
                        })
                        added += 1
        except (json.JSONDecodeError, TypeError):
            log.warning("Could not parse l1_patterns_json")

    # Deduplicate and cap
    seen: set[str] = set()
    unique: list[dict] = []
    for c in cards:
        key = c["error"].lower()[:40]
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique[:15]


# ── HTML builder ─────────────────────────────────────────────────────────────

def _build_html(
    grammar_point: str,
    l1_language: str,
    cards: list[dict],
) -> str:
    l1_label = l1_language or "General"
    meta = f"{grammar_point}  ·  L1: {l1_label}  ·  {len(cards)} cards"

    html = _HTML_HEADER.format(header_color="#dc2626")

    # — Page 1: Fronts —
    html += f"""
<div class="page-header">
  <span class="badge">✗ FRONT</span>
  <span class="meta">{_esc(meta)}</span>
</div>
<div class="card-grid front">
"""
    for i, c in enumerate(cards, 1):
        html += _card_front(i, c["error"], c["why"][:60] if not c["l1_label"] else "", c["l1_label"])
    html += "\n</div>\n"
    html += f'<div class="footer">Print double-sided (flip on short edge) · Cut along dashed lines · <strong>cogniesl.com</strong></div>\n'

    # — Page 2: Backs —
    html += '\n<div class="page-break"></div>\n'
    html += f"""
<div class="page-header">
  <span class="badge" style="background:#0b7272;">✓ BACK</span>
  <span class="meta">{_esc(meta)}</span>
</div>
<div class="card-grid back">
"""
    for i, c in enumerate(cards, 1):
        html += _card_back(i, c["correct"], c["why"])
    html += "\n</div>\n"
    html += f'<div class="footer"><strong>cogniesl.com</strong> · L1-aware teaching materials, made in minutes.</div>\n'

    html += _HTML_FOOTER
    return html


# ── Tool ─────────────────────────────────────────────────────────────────────

class GenerateFlashcardPdf(BaseTool):
    """
    Generate a print-and-cut flashcard PDF for a grammar point.

    Sources 10–15 error/correction pairs from:
    1. common_errors_json — grammar YAML common_errors array (JSON string)
    2. l1_patterns_json  — L1 interference YAML patterns array (JSON string, optional)

    Output: saves both the .source.html and .pdf files, returns both paths.
    Call this AFTER slides (and worksheet if requested) are complete.
    """

    project_name: str = Field(
        ...,
        description="Project folder name (e.g. 'present_perfect_french_adults')",
    )
    grammar_point: str = Field(
        ...,
        description="Grammar point name (e.g. 'Present Perfect')",
    )
    common_errors_json: str = Field(
        default="[]",
        description=(
            "JSON string of the common_errors array from the grammar YAML. "
            "Each item must have: error/wrong, correction/correct, and optionally explanation/why. "
            "Example: [{\"error\": \"*He walk\", \"correction\": \"He walks\", \"explanation\": \"Missing 3rd-person -s\"}]"
        ),
    )
    l1_language: str = Field(
        default="",
        description="Student L1 language name (e.g. 'Spanish'). Leave blank if no L1 specified.",
    )
    l1_patterns_json: str = Field(
        default="[]",
        description=(
            "JSON string of the interference_patterns array from the L1 YAML. "
            "Each item should have: examples (list of {wrong, correct}), why_it_happens. "
            "Leave as '[]' if no L1 specified or data unavailable."
        ),
    )

    def run(self) -> str:
        try:
            doc_dir = _get_project_dir(self.project_name)
        except Exception as e:
            return f"Error: Could not create project directory: {e}"

        # Build card list from YAML data
        cards = _extract_cards(
            self.common_errors_json,
            self.l1_patterns_json,
            self.l1_language,
        )

        if not cards:
            return (
                "Error: No flashcard content could be extracted from the provided YAML data. "
                "Ensure common_errors_json contains items with 'error'/'wrong' and 'correction'/'correct' keys."
            )

        # Build HTML
        html = _build_html(self.grammar_point, self.l1_language, cards)

        # Determine file stem
        safe_grammar = self.grammar_point.lower().replace(" ", "_").replace("/", "_")
        safe_l1 = self.l1_language.lower().replace(" ", "_") if self.l1_language else "general"
        stem = f"{safe_grammar}-{safe_l1}-flashcards"

        # Write .source.html
        html_path = doc_dir / f"{stem}.source.html"
        html_path.write_text(html, encoding="utf-8")

        # Convert to PDF via weasyprint
        pdf_path = doc_dir / f"{stem}.pdf"
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(pdf_path)
        except ImportError:
            return (
                f"Error: weasyprint is not installed. Cannot generate PDF. "
                f"HTML source saved at: {html_path}"
            )
        except Exception as e:
            return f"Error generating PDF: {e}. HTML saved at: {html_path}"

        if not pdf_path.exists():
            return f"Error: PDF was not created. HTML source at: {html_path}"

        pdf_size = pdf_path.stat().st_size
        return (
            f"Flashcard PDF generated successfully!\n"
            f"Cards: {len(cards)} pairs (fronts page 1 · backs page 2)\n"
            f"HTML source: {html_path}\n"
            f"PDF: {pdf_path} ({pdf_size:,} bytes)\n"
            f"Path for MarkJobComplete: {pdf_path}"
        )
