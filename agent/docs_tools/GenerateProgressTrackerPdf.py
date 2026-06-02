"""Generate a one-page progress tracker PDF for student self-assessment."""

from agency_swarm.tools import BaseTool
from pydantic import Field

from .CreateDocument import CreateDocument
from .ConvertDocument import ConvertDocument


class GenerateProgressTrackerPdf(BaseTool):
    """Generate a one-page student self-assessment progress tracker PDF."""

    project_name: str = Field(
        ..., description="Project folder name"
    )
    grammar_point: str = Field(
        ..., description="Grammar point name"
    )
    l1_language: str = Field(
        default="",
        description="L1 language name or empty string",
    )
    sub_rules: str = Field(
        default="",
        description="Comma-separated list of sub-rule names (e.g. 'Third person -s, Negative formation')",
    )
    key_skills: str = Field(
        default="",
        description="Comma-separated list of skills to self-assess",
    )

    def run(self) -> str:
        title = self.grammar_point + " - Progress Tracker"
        if self.l1_language:
            title += " (" + self.l1_language + ")"

        skills_list = [s.strip() for s in self.key_skills.split(",") if s.strip()]
        if not skills_list:
            skills_list = [
                "I understand when to use " + self.grammar_point,
                "I can form affirmative sentences",
                "I can form negative sentences",
                "I can form questions",
                "I can use it in conversation",
            ]

        rules_list = [r.strip() for r in self.sub_rules.split(",") if r.strip()]
        rules_html = ""
        if rules_list:
            rules_html = "<h3>Key Rules to Review</h3><ul>"
            for r in rules_list:
                rules_html += "<li>" + r + "</li>"
            rules_html += "</ul>"

        rows_html = ""
        for skill in skills_list:
            rows_html += (
                '<tr>'
                '<td class="skill-cell">' + skill + '</td>'
                '<td class="radio-cell"><span class="circle">1</span></td>'
                '<td class="radio-cell"><span class="circle">2</span></td>'
                '<td class="radio-cell"><span class="circle">3</span></td>'
                '<td class="radio-cell"><span class="circle">4</span></td>'
                '</tr>'
            )

        html = (
            '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>' + title + '</title>'
            '<style>'
            '@page { size: A4; margin: 18pt; }'
            'body { font-family: Inter, Arial, sans-serif; margin: 0; padding: 18pt; color: #1f2937; }'
            'h1 { color: #0b7272; font-size: 18pt; margin-bottom: 4pt; }'
            '.subtitle { color: #6b7280; font-size: 11pt; margin-bottom: 16pt; }'
            'table { width: 100%; border-collapse: collapse; margin-bottom: 16pt; }'
            'th { background: #0b7272; color: #fff; padding: 8pt 6pt; font-size: 10pt; text-align: left; }'
            'th:first-child { width: 55%; }'
            'th:not(:first-child) { width: 11%; text-align: center; }'
            'td { padding: 8pt 6pt; border-bottom: 1px solid #e5e7eb; font-size: 10pt; }'
            '.skill-cell { font-weight: 500; }'
            '.radio-cell { text-align: center; }'
            '.circle { display: inline-block; width: 22px; height: 22px; border: 2px solid #d1d5db; border-radius: 50%; text-align: center; line-height: 22px; font-size: 10pt; color: #d1d5db; }'
            '.scale-label { font-size: 9pt; color: #6b7280; margin-top: 4pt; }'
            '.notes-box { border: 1px solid #d1d5db; padding: 8pt; min-height: 50pt; margin-top: 8pt; border-radius: 4pt; }'
            '.notes-box:before { content: "What I need more help with..."; color: #9ca3af; font-size: 10pt; }'
            '.footer { margin-top: 16pt; font-size: 9pt; color: #9ca3af; text-align: center; }'
            '</style></head><body>'
            '<h1>' + title + '</h1>'
            '<div class="subtitle">Rate your understanding: 1 = Need help  2 = Getting there  3 = Good  4 = Can teach others</div>'
            '<table>'
            '<tr><th>Skill</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>'
            + rows_html +
            '</table>'
            + rules_html +
            '<div class="notes-box"></div>'
            '<div class="footer">CogniESL Progress Tracker - Print one per student</div>'
            '</body></html>'
        )

        doc_name = (
            self.grammar_point.lower().replace(" ", "_")
            + "-"
            + (self.l1_language.lower() if self.l1_language else "general")
            + "-progress"
        )

        doc_result = CreateDocument(
            project_name=self.project_name,
            document_name=doc_name,
            content={"type": "html", "value": html},
        ).run()

        if doc_result.startswith("Error"):
            return doc_result

        pdf_result = ConvertDocument(
            project_name=self.project_name,
            document_name=doc_name,
            target_format="pdf",
        ).run()

        return pdf_result
