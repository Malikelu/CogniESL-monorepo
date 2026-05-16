import yaml
from pathlib import Path
from agency_swarm.tools import BaseTool
from pydantic import Field


class GetL1InterferenceTool(BaseTool):
    """
    Get L1 interference patterns for a specific grammar point and language.
    Returns all interference patterns with examples, explanations, and teacher tips.
    """

    grammar_point: str = Field(
        ...,
        description="The grammar point slug (e.g., 'present_simple', 'a_an_the', 'passive_voice'). Use the grammar_point field from SearchGrammarTool results."
    )
    language: str = Field(
        ...,
        description="The L1 language name (e.g., 'Portuguese', 'Spanish', 'Arabic', 'Japanese'). Case-insensitive."
    )

    def run(self):
        data_dir = Path(__file__).resolve().parents[3] / "data" / "l1-interference"
        if not data_dir.exists():
            return f"Error: L1 interference data directory not found at {data_dir}"

        language_lower = self.language.lower().strip()
        grammar_slug = self.grammar_point.lower().strip().replace(" ", "_").replace("-", "_")

        # Find the L1 file for this language
        l1_file = None

        # Strategy 1: Direct match (e.g., portuguese_interference.yaml)
        for f in data_dir.glob("*.yaml"):
            stem = f.stem.lower()
            if language_lower in stem:
                l1_file = f
                break

        if not l1_file:
            available = sorted([f.stem.replace("_interference", "").title() for f in data_dir.glob("*.yaml") if f.stem != "coverage"])
            return f"Error: No L1 interference data found for language '{self.language}'. Available languages: {', '.join(available)}"

        # Load the L1 file and find the grammar point
        try:
            l1_data = yaml.safe_load(l1_file.read_text(encoding="utf-8"))
        except Exception as e:
            return f"Error loading {l1_file.name}: {str(e)}"

        if not l1_data or "grammar_points" not in l1_data:
            return f"Error: Invalid format in {l1_file.name}"

        grammar_points = l1_data["grammar_points"]

        # Try exact slug match first
        if grammar_slug in grammar_points:
            return {
                "language": self.language.title(),
                "grammar_point": grammar_slug,
                "data": grammar_points[grammar_slug]
            }

        # Try case-insensitive match
        for gp_key in grammar_points:
            if gp_key.lower() == grammar_slug:
                return {
                    "language": self.language.title(),
                    "grammar_point": gp_key,
                    "data": grammar_points[gp_key]
                }

        # Try partial match (e.g., "present_simple" matches "present_simple_tense")
        for gp_key in grammar_points:
            if grammar_slug in gp_key.lower() or gp_key.lower() in grammar_slug:
                return {
                    "language": self.language.title(),
                    "grammar_point": gp_key,
                    "data": grammar_points[gp_key]
                }

        available_gps = sorted(grammar_points.keys())
        return {
            "language": self.language.title(),
            "grammar_point": grammar_slug,
            "error": f"No interference data for '{grammar_slug}' in {self.language}.",
            "available_grammar_points": available_gps[:30],
            "total_available": len(available_gps)
        }
