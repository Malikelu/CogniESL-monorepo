"""Generate a print-and-cut flashcard PDF from grammar and L1 data."""

import json
import hashlib
import random
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

from .CreateDocument import CreateDocument
from .ConvertDocument import ConvertDocument


class GenerateFlashcardPdf(BaseTool):
    """Generate a print-and-cut flashcard PDF combining grammar common_errors and L1 interference patterns."""

    project_name: str = Field(
        ..., description="Project folder name"
    )
    grammar_point: str = Field(
        ..., description="Grammar point name"
    )
    common_errors_json: str = Field(
        ..., description="JSON string of common_errors array from grammar YAML"
    )
    l1_language: str = Field(
        default="",
        description="L1 language name or empty string if no L1 data",
    )
    l1_patterns_json: str = Field(
        default="[]",
        description="JSON string of interference_patterns array from L1 YAML",
    )

    def run(self) -> str:
        common_errors = json.loads(self.common_errors_json) if self.common_errors_json else []
        l1_patterns = json.loads(self.l1_patterns_json) if self.l1_patterns_json else []

        cards = []

        for err in common_errors[:8]:
            wrong = err.get("error", err.get("wrong", ""))
            correct = err.get("correction", err.get("correct", ""))
            explanation = err.get("explanation", err.get("why", ""))
            if wrong and correct:
                front = wrong.replace("*", "").strip()
                back = correct.strip()
                if explanation:
                    back += " - " + explanation
                cards.append((front, back))

        for pat in l1_patterns[:6]:
            examples = pat.get("examples", [])
            why = pat.get("why_it_happens", "")
            for ex in examples[:2]:
                w = ex.get("wrong", "").replace("*", "").strip()
                c = ex.get("correct", "").strip()
                if w and c:
                    back_text = c
                    if why:
                        back_text += " - " + why[:80]
                    cards.append((w, back_text))

        if len(cards) > 15:
            seed = hashlib.md5(self.grammar_point.encode()).hexdigest()
            rng = random.Random(seed)
            rng.shuffle(cards)
            cards = cards[:15]

        if not cards:
            return "Error: No card pairs could be generated from the provided data"

        title = self.grammar_point + " Flashcards"
        if self.l1_language:
            title += " - " + self.l1_language

        fronts_rows = ""
        backs_rows = ""
        for i, (front, back) in enumerate(cards):
            num = str(i + 1)
            fronts_rows += (
                '<td class="card">'
                '<div class="card-num">' + num + '.</div>'
                '<div class="card-front">' + front + '</div>'
                '</td>'
            )
            backs_rows += (
                '<td class="card back-card">'
                '<div class="card-num">' + num + '.</div>'
                '<div class="card-back">' + back + '</div>'
                '</td>'
            )
            if (i + 1) % 2 == 0 or i == len(cards) - 1:
                if fronts_rows:
                    fronts_html += '<tr>' + fronts_rows + '</tr>'
                    fronts_rows = ""
                if backs_rows:
                    backs_html += '<tr>' + backs_rows + '</tr>'
                    backs_rows = ""

        html = (
            '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>' + title + '</title>'
            '<style>'
            '@page { size: A4; margin: 12pt; }'
            'body { font-family: Inter, Arial, sans-serif; margin: 0; padding: 12pt; }'
            '.page-title { text-align: center; font-size: 14pt; font-weight: 700; color: #0b7272; margin-bottom: 12pt; }'
            '.page-label { text-align: center; font-size: 10pt; color: #6b7280; margin-bottom: 8pt; font-style: italic; }'
            'table.grid { width: 100%; border-collapse: separate; border-spacing: 8pt; }'
            '.card { border: 1px solid #d1d5db; padding: 12pt 8pt; min-height: 90pt; vertical-align: middle; text-align: center; page-break-inside: avoid; width: 50%; }'
            '.back-card { background: #f8fafc; }'
            '.card-num { font-size: 8pt; color: #9ca3af; text-align: left; }'
            '.card-front { font-size: 13pt; font-weight: 600; color: #1f2937; padding-top: 6pt; }'
            '.card-back { font-size: 12pt; font-weight: 500; color: #0b7272; padding-top: 6pt; }'
            '</style></head><body>'
            '<div class="page-title">' + title + '</div>'
            '<div class="page-label">Front — Look at the prompt. Try to say the correct answer.</div>'
            '<table class="grid"><tbody>' + fronts_html + '</tbody></table>'
            '<div style="page-break-before: always;"></div>'
            '<div class="page-title">' + title + '</div>'
            '<div class="page-label">Back — Check your answers.</div>'
            '<table class="grid"><tbody>' + backs_html + '</tbody></table>'
            '</body></html>'
        )

        doc_name = (
            self.grammar_point.lower().replace(" ", "_")
            + "-"
            + (self.l1_language.lower() if self.l1_language else "general")
            + "-flashcards"
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
