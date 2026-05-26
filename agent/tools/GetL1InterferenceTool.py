import os
import yaml
from pathlib import Path
from agency_swarm.tools import BaseTool
from pydantic import Field


def _get_data_dir() -> Path:
    """Return the read-only static data directory (grammar/L1/activities).
    Uses COGNIESL_STATIC_DIR on Railway (points to /app/static-data, outside the
    Volume mount at /app/data). Falls back to source-relative path for local dev."""
    env_path = os.getenv("COGNIESL_STATIC_DIR")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[2] / "data"


class GetL1InterferenceTool(BaseTool):
    """
    Get L1 interference patterns for a specific grammar point and language.
    Returns all interference patterns with examples, explanations, and teacher tips.
    """

    grammar_point: str = Field(
        ...,
        description="The grammar point slug (e.g., 'present_simple', 'a_an_the', 'passive_voice')."
    )
    language: str = Field(
        ...,
        description="The L1 language name (e.g., 'Portuguese', 'Spanish', 'Arabic', 'Japanese')."
    )

    # Aliases map grammar point slugs that CogniESL uses internally to the
    # broader category keys used in L1 interference files.
    # Example: French file has no "past_simple" key — tense data lives under "verb_tenses".
    # This is a last-resort fallback applied only after all direct matching fails.
    _GRAMMAR_POINT_ALIASES: dict = {
        # Tenses — files differ: French uses "verb_tenses" umbrella, Arabic has granular keys.
        # Aliases are tried in order; first one found in the file wins (see run() logic).
        "past_simple": ["verb_tenses", "simple_past_vs_present_perfect", "time_tense_mismatch", "tense_aspect_combination_errors"],
        "present_simple": ["verb_tenses", "subject_verb_agreement"],
        "present_perfect": ["verb_tenses", "present_perfect_vs_past", "simple_past_vs_present_perfect"],
        "past_continuous": ["verb_tenses", "tense_aspect_combination_errors"],
        "present_continuous": ["verb_tenses", "tense_aspect_combination_errors"],
        "past_perfect": ["verb_tenses", "past_perfect_usage", "past_perfect_continuous"],
        "future_simple": ["verb_tenses", "future_expressions", "future_in_the_past"],
        "future_continuous": ["verb_tenses", "future_continuous", "future_expressions"],
        "past_perfect_continuous": ["verb_tenses", "past_perfect_continuous"],
        "present_perfect_continuous": ["verb_tenses", "present_perfect_continuous"],
        "future_perfect": ["verb_tenses", "future_perfect", "future_expressions"],
        "be_going_to": ["verb_tenses", "be_going_to", "future_expressions"],
        # Conditionals
        "first_conditional": "conditionals",
        "second_conditional": "conditionals",
        "third_conditional": "conditionals",
        "zero_conditional": "conditionals",
        "mixed_conditional": "conditionals",
        # Modals
        "can_could": "modal_verbs",
        "must_have_to": "modal_verbs",
        "should_ought_to": "modal_verbs",
        "will_would": "modal_verbs",
        "may_might": "modal_verbs",
        # Articles
        "a_an": "articles",
        "a_an_the": "articles",
        "definite_article": "articles",
        "indefinite_article": "articles",
        # Passive
        "passive_simple": "passive_voice",
        "passive_continuous": "passive_voice",
        "passive_perfect": "passive_voice",
        # Reported speech
        "indirect_speech": "reported_speech",
        "reporting_verbs": "reported_speech",
        # Gerund / infinitive
        "gerund": "gerund_infinitive",
        "infinitive": "gerund_infinitive",
        "verb_patterns": "gerund_infinitive",
    }

    # Aliases map common country names and alternative language names to the
    # canonical language name used in the interference file stems.
    _LANGUAGE_ALIASES: dict = {
        "chinese": "mandarin",
        "mandarin chinese": "mandarin",
        "simplified chinese": "mandarin",
        "traditional chinese": "mandarin",
        "cantonese": "mandarin",
        "brazilian": "portuguese",
        "brazilian portuguese": "portuguese",
        "brazil": "portuguese",
        "castilian": "spanish",
        "mexican": "spanish",
        "mexico": "spanish",
        "colombian": "spanish",
        "colombia": "spanish",
        "argentina": "spanish",
        "argentinian": "spanish",
        "spain": "spanish",
        "france": "french",
        "germany": "german",
        "deutschland": "german",
        "japan": "japanese",
        "korea": "korean",
        "south korea": "korean",
        "saudi": "arabic",
        "saudi arabia": "arabic",
        "egypt": "arabic",
        "russia": "russian",
        "russia": "russian",
        "turkey": "turkish",
        "vietnam": "vietnamese",
        "indonesia": "indonesian",
        "thailand": "thai",
        "netherlands": "dutch",
        "holland": "dutch",
        "poland": "polish",
        "czech republic": "czech",
        "czechia": "czech",
        "denmark": "danish",
        "greece": "greek",
        "sweden": "swedish",
        "norway": "norwegian",
        "finland": "finnish",
        "hungary": "hungarian",
        "romania": "romanian",
        "ukraine": "ukrainian",
        "bangladesh": "bengali",
    }

    def run(self):
        data_dir = _get_data_dir() / "l1-interference"
        if not data_dir.exists():
            return f"Error: L1 interference data directory not found at {data_dir}"

        language_lower = self.language.lower().strip()
        # Resolve aliases (e.g. "Chinese" → "mandarin", "Brazil" → "portuguese")
        language_lower = self._LANGUAGE_ALIASES.get(language_lower, language_lower)
        grammar_slug = self.grammar_point.lower().strip().replace(" ", "_").replace("-", "_")

        l1_file = None
        for f in data_dir.glob("*.yaml"):
            stem = f.stem.lower()
            if language_lower in stem:
                l1_file = f
                break

        if not l1_file:
            available = sorted([f.stem.replace("_interference", "").title() for f in data_dir.glob("*.yaml") if f.stem not in ("coverage", "enrichment_data", "hand_curated") and not f.stem.startswith("_")])
            return f"Error: No L1 interference data for '{self.language}'. Available: {', '.join(available)}"

        try:
            l1_data = yaml.safe_load(l1_file.read_text(encoding="utf-8"))
        except Exception as e:
            return f"Error loading {l1_file.name}: {str(e)}"

        if not l1_data or "grammar_points" not in l1_data:
            return f"Error: Invalid format in {l1_file.name}"

        grammar_points = l1_data["grammar_points"]

        if grammar_slug in grammar_points:
            return {"language": self.language.title(), "grammar_point": grammar_slug, "data": grammar_points[grammar_slug]}

        for gp_key in grammar_points:
            if gp_key.lower() == grammar_slug:
                return {"language": self.language.title(), "grammar_point": gp_key, "data": grammar_points[gp_key]}

        for gp_key in grammar_points:
            if grammar_slug in gp_key.lower() or gp_key.lower() in grammar_slug:
                return {"language": self.language.title(), "grammar_point": gp_key, "data": grammar_points[gp_key]}

        # Fallback 4: alias mapping — L1 files differ wildly in key names.
        # French uses umbrella "verb_tenses"; Arabic has granular keys like
        # "simple_past_vs_present_perfect". Try each alias in order, return first match.
        aliased = self._GRAMMAR_POINT_ALIASES.get(grammar_slug, [])
        if isinstance(aliased, str):
            aliased = [aliased]
        for candidate in aliased:
            if candidate in grammar_points:
                return {"language": self.language.title(), "grammar_point": candidate, "data": grammar_points[candidate]}

        available_gps = sorted(grammar_points.keys())
        return {
            "language": self.language.title(),
            "grammar_point": grammar_slug,
            "error": f"No interference data for '{grammar_slug}' in {self.language}.",
            "available_grammar_points": available_gps[:30],
            "total_available": len(available_gps)
        }
