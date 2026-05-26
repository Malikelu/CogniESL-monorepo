"""
ListMaterials — let the agent show a returning teacher their saved materials.

Returns a formatted summary of previously generated materials for the current user.
The agent should offer to regenerate any listed set, or suggest improvements.
"""
import sys
from pathlib import Path
from typing import Optional

from agency_swarm.tools import BaseTool
from pydantic import Field

_cogniesl_root = str(Path(__file__).parent.parent.parent)
if _cogniesl_root not in sys.path:
    sys.path.insert(0, _cogniesl_root)


class ListMaterials(BaseTool):
    """
    List previously generated materials for the current authenticated user.

    Use this when a returning teacher says things like:
    - "Show me my materials"
    - "What have I generated before?"
    - "I want to use a past lesson"
    - "Can I download my slides again?"
    - "What did I make for Spanish students?"

    Returns a formatted list of their materials with download links.
    """

    grammar_point: Optional[str] = Field(
        default=None,
        description="Optional: filter by grammar point (e.g., 'present simple'). Leave blank to show all.",
    )
    l1_language: Optional[str] = Field(
        default=None,
        description="Optional: filter by L1 language (e.g., 'Spanish'). Leave blank to show all.",
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results to return (default 10).",
    )

    def run(self) -> str:
        # Try to get user_id from the agent context (set by server.py from JWT)
        user_id = None
        try:
            # agency_swarm agents can access context via _shared_state
            ctx = getattr(self, '_shared_state', None)
            if ctx:
                user_id = getattr(ctx, 'user_id', None)
        except Exception:
            pass

        if not user_id:
            return (
                "I can see your past materials if you're signed in. "
                "Please sign in or create an account using the button in the top-right corner, "
                "and then ask me again — I'll be able to show you everything you've made!"
            )

        try:
            from auth.db import list_materials
            materials = list_materials(
                user_id=user_id,
                grammar_point=self.grammar_point,
                l1=self.l1_language,
                limit=self.limit,
            )
        except Exception as e:
            return f"Sorry, I couldn't retrieve your materials right now: {e}"

        if not materials:
            filters = []
            if self.grammar_point:
                filters.append(f"grammar point '{self.grammar_point}'")
            if self.l1_language:
                filters.append(f"L1 language '{self.l1_language}'")
            filter_text = " and ".join(filters)
            if filter_text:
                return f"You don't have any saved materials for {filter_text} yet. Would you like me to generate some?"
            return (
                "You haven't generated any materials yet. "
                "Tell me what you need — a grammar point, your students' native language, "
                "and their age group — and I'll create slides, worksheets, or activities for you!"
            )

        # Format the results
        lines = [f"Here are your {len(materials)} most recent material set(s):\n"]
        for mat in materials:
            grammar = mat["grammar_point"].replace("_", " ").title()
            l1s = mat["l1_languages"] or "any language"
            age = mat["age_group"]
            date = mat["created_at"][:10]  # YYYY-MM-DD
            slides = f"{mat['slide_count']} slides" if mat.get("slide_count") else ""
            files = []
            if mat.get("pptx_path") and mat.get("job_id"):
                fname = mat["pptx_path"].split("/")[-1]
                files.append(f"[Slides](/download/{mat['job_id']}/{fname})")
            if mat.get("worksheet_pdf_path") and mat.get("job_id"):
                fname = mat["worksheet_pdf_path"].split("/")[-1]
                files.append(f"[Worksheet PDF](/download/{mat['job_id']}/{fname})")
            if mat.get("worksheet_docx_path") and mat.get("job_id"):
                fname = mat["worksheet_docx_path"].split("/")[-1]
                files.append(f"[Worksheet DOCX](/download/{mat['job_id']}/{fname})")
            if mat.get("activity_pdf_path") and mat.get("job_id"):
                fname = mat["activity_pdf_path"].split("/")[-1]
                files.append(f"[Activity](/download/{mat['job_id']}/{fname})")

            parts = [f"**{grammar}** — {l1s} — {age}s — {date}"]
            if slides:
                parts.append(f"({slides})")
            lines.append(" ".join(parts))
            if files:
                lines.append("  Downloads: " + " · ".join(files))
            lines.append("")

        lines.append("Would you like to regenerate any of these, or shall I create something new?")
        return "\n".join(lines)
