"""
GenerateProgressTrackerPdf — generate a 1-page student self-assessment PDF.

Creates a "After this lesson I can..." tracker with:
- 4-6 "I can..." statements derived from CCQs + YAML core_meaning
- L1-specific error awareness checklist (from interference patterns)
- Self-rating scale (1–4 stars) next to each statement
- Space for personal notes / examples

Saves as a print-ready A4 PDF alongside other documents.
"""

import json
import logging
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

log = logging.getLogger(__name__)


def _get_project_dir(project_name: str) -> Path:
    import os
    base = Path(os.getenv("COGNIESL_DATA_DIR", "/app/data")) / "mnt"
    if not base.parent.exists():
        base = Path(__file__).parent.parent.parent / "mnt"
    doc_dir = base / project_name / "documents"
    doc_dir.mkdir(parents=True, exist_ok=True)
    return doc_dir


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


_STARS = '<span style="color:#f59e0b;font-size:18px;">☆☆☆☆</span>'
_STARS_LABEL = "1 = not yet &nbsp; 2 = getting there &nbsp; 3 = mostly &nbsp; 4 = confident"


def _build_html(
    grammar_point: str,
    l1_language: str,
    core_meaning: str,
    can_do_statements: list[str],
    l1_checks: list[dict],
) -> str:
    safe_gp = _esc(grammar_point)
    safe_l1 = _esc(l1_language) if l1_language else ""
    safe_cm = _esc(core_meaning) if core_meaning else ""

    # Build "I can..." rows
    can_do_rows = ""
    for stmt in can_do_statements:
        can_do_rows += f"""
        <tr>
          <td style="padding:10px 12px;font-size:14px;color:#1f2937;line-height:1.4;width:65%;">
            ✅ {_esc(stmt)}
          </td>
          <td style="padding:10px 12px;text-align:center;width:20%;">{_STARS}</td>
          <td style="padding:10px 12px;width:15%;border-left:1px solid #e5e7eb;">
            <div style="border-bottom:1px solid #d1d5db;margin-bottom:8px;">&nbsp;</div>
            <div style="border-bottom:1px solid #d1d5db;">&nbsp;</div>
          </td>
        </tr>"""

    # Build L1 error awareness section
    l1_section = ""
    if l1_checks and l1_language:
        rows = ""
        for item in l1_checks[:5]:
            wrong = _esc(item.get("wrong", ""))
            correct = _esc(item.get("correct", ""))
            rows += f"""
          <tr>
            <td style="padding:8px 12px;font-size:13px;">
              <span style="color:#dc2626;text-decoration:line-through;">{wrong}</span>
              &nbsp;→&nbsp;
              <span style="color:#0b7272;font-weight:700;">{correct}</span>
            </td>
            <td style="padding:8px 12px;text-align:center;font-size:20px;color:#9ca3af;">☐</td>
          </tr>"""
        l1_section = f"""
      <div style="margin-top:20px;border:1.5px solid #1baa6e;border-radius:8px;overflow:hidden;">
        <div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;">
          <span style="font-size:13px;font-weight:700;color:#0b7272;text-transform:uppercase;letter-spacing:0.5px;">
            ⚠ {safe_l1} Speakers — Watch These Errors
          </span>
        </div>
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <th style="padding:8px 12px;font-size:12px;color:#6b7280;text-align:left;border-bottom:1px solid #e5e7eb;">Common mistake → Correct form</th>
            <th style="padding:8px 12px;font-size:12px;color:#6b7280;text-align:center;border-bottom:1px solid #e5e7eb;width:60px;">✓ Done</th>
          </tr>
          {rows}
        </table>
      </div>"""

    # Personal example box
    l1_label_line = f" &nbsp;|&nbsp; <span style='color:#1baa6e;font-weight:700;'>{safe_l1} Speakers: check the error list!</span>" if l1_language else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  @page {{ size: A4; margin: 14mm 14mm 12mm; }}
  @media print {{
    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
  body {{ font-family: 'Nunito', Arial, sans-serif; background: #fff; color: #1f2937; }}
</style>
</head>
<body>

<!-- Header -->
<div style="background:#0b7272;color:white;padding:14px 18px;border-radius:8px 8px 0 0;margin-bottom:0;">
  <div style="font-size:11px;font-weight:700;letter-spacing:1.5px;opacity:0.75;text-transform:uppercase;">Student Progress Tracker</div>
  <div style="font-size:22px;font-weight:800;margin-top:2px;">{safe_gp}</div>
  {f'<div style="font-size:12px;opacity:0.8;margin-top:2px;">Prepared for {safe_l1} speakers</div>' if safe_l1 else ''}
</div>

<!-- Core meaning strip -->
{f'<div style="background:#e0f2f1;padding:10px 18px;font-size:13px;color:#065f46;line-height:1.4;border:1.5px solid #0b7272;border-top:none;margin-bottom:16px;"><strong>What this grammar means:</strong> {safe_cm}</div>' if safe_cm else '<div style="margin-bottom:16px;"></div>'}

<!-- Self-assessment table -->
<div style="border:1.5px solid #0b7272;border-radius:0 0 8px 8px;overflow:hidden;margin-bottom:16px;">
  <div style="background:#f0f9f9;padding:10px 14px;border-bottom:1px solid #b2dfdb;">
    <span style="font-size:13px;font-weight:700;color:#0b7272;text-transform:uppercase;letter-spacing:0.5px;">After this lesson, I can…</span>
    <span style="font-size:11px;color:#6b7280;margin-left:10px;">Rate yourself: {_STARS_LABEL}</span>
  </div>
  <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
    <tr style="background:#f8fafc;border-bottom:1px solid #e5e7eb;">
      <th style="padding:8px 12px;font-size:11px;color:#9ca3af;text-align:left;">Skill</th>
      <th style="padding:8px 12px;font-size:11px;color:#9ca3af;text-align:center;width:20%;">My rating ★</th>
      <th style="padding:8px 12px;font-size:11px;color:#9ca3af;text-align:left;width:15%;border-left:1px solid #e5e7eb;">My example</th>
    </tr>
    {can_do_rows}
  </table>
</div>

{l1_section}

<!-- My example sentence box -->
<div style="margin-top:16px;border:1.5px dashed #d1d5db;border-radius:8px;padding:12px 16px;">
  <div style="font-size:12px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">
    📝 My own example sentence{l1_label_line}
  </div>
  <div style="border-bottom:1px solid #e5e7eb;padding-bottom:18px;margin-bottom:10px;">&nbsp;</div>
  <div style="border-bottom:1px solid #e5e7eb;padding-bottom:18px;">&nbsp;</div>
</div>

<!-- Footer -->
<div style="text-align:center;margin-top:14px;font-size:9px;color:#9ca3af;letter-spacing:0.3px;">
  <strong style="color:#0b7272;">cogniesl.com</strong> · L1-aware teaching materials, made in minutes.
</div>

</body>
</html>
"""
    return html


class GenerateProgressTrackerPdf(BaseTool):
    """
    Generate a 1-page student self-assessment PDF (progress tracker).

    Creates "After this lesson I can..." with 4-6 skill statements + L1 error
    checklist + self-rating stars + example sentence space.

    Call this after slides (and other formats) are generated — it takes very little time.
    """

    project_name: str = Field(
        ...,
        description="Project folder name (e.g. 'present_perfect_french_adults')",
    )
    grammar_point: str = Field(
        ...,
        description="Grammar point name (e.g. 'Present Perfect')",
    )
    core_meaning: str = Field(
        default="",
        description="One-sentence core meaning from grammar YAML (shown at top of tracker).",
    )
    can_do_statements_json: str = Field(
        default="[]",
        description=(
            "JSON array of 4-6 'I can...' strings derived from CCQs and YAML form examples. "
            "E.g. '[\"use present perfect to talk about life experiences\", "
            "\"form the negative: I haven't + past participle\"]'"
        ),
    )
    l1_language: str = Field(
        default="",
        description="Student L1 language name (e.g. 'Spanish'). Leave blank if no L1.",
    )
    l1_error_pairs_json: str = Field(
        default="[]",
        description=(
            "JSON array of {wrong, correct} dicts from L1 interference YAML. "
            "E.g. '[{\"wrong\": \"*I have seen him yesterday\", \"correct\": \"I saw him yesterday\"}]'"
        ),
    )

    def run(self) -> str:
        try:
            doc_dir = _get_project_dir(self.project_name)
        except Exception as e:
            return f"Error: Could not create project directory: {e}"

        # Parse inputs
        try:
            can_do = json.loads(self.can_do_statements_json)
            if not isinstance(can_do, list):
                can_do = []
        except (json.JSONDecodeError, TypeError):
            can_do = []

        try:
            l1_pairs = json.loads(self.l1_error_pairs_json)
            if not isinstance(l1_pairs, list):
                l1_pairs = []
        except (json.JSONDecodeError, TypeError):
            l1_pairs = []

        if not can_do:
            return (
                "Error: can_do_statements_json is empty. Provide 4-6 'I can...' statements "
                "derived from the grammar YAML CCQs and form examples."
            )

        # Build HTML
        html = _build_html(
            grammar_point=self.grammar_point,
            l1_language=self.l1_language,
            core_meaning=self.core_meaning,
            can_do_statements=can_do[:6],
            l1_checks=l1_pairs[:5],
        )

        # Determine file stem
        safe_grammar = self.grammar_point.lower().replace(" ", "_").replace("/", "_")
        safe_l1 = self.l1_language.lower().replace(" ", "_") if self.l1_language else "general"
        stem = f"{safe_grammar}-{safe_l1}-progress-tracker"

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
                f"Error: weasyprint not installed. HTML source saved at: {html_path}"
            )
        except Exception as e:
            return f"Error generating PDF: {e}. HTML saved at: {html_path}"

        if not pdf_path.exists():
            return f"Error: PDF was not created. HTML source at: {html_path}"

        pdf_size = pdf_path.stat().st_size
        return (
            f"Progress tracker PDF generated!\n"
            f"Statements: {len(can_do[:6])} 'I can...' items"
            f"{f' + {len(l1_pairs[:5])} L1 error checks' if l1_pairs else ''}\n"
            f"HTML source: {html_path}\n"
            f"PDF: {pdf_path} ({pdf_size:,} bytes)\n"
            f"Path for MarkJobComplete: {pdf_path}"
        )
