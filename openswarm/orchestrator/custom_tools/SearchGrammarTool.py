import os
import yaml
from pathlib import Path
from agency_swarm.tools import BaseTool
from pydantic import Field


class SearchGrammarTool(BaseTool):
    """
    Search the CogniESL grammar database by topic name.
    Handles variations like 'Simple Present' -> present_simple.yaml.
    Returns the full grammar point data as a dictionary.
    """

    topic: str = Field(
        ...,
        description="The grammar topic to search for (e.g., 'present simple', 'passive voice', 'articles')."
    )

    def run(self):
        data_dir = Path(__file__).resolve().parents[3] / "data" / "grammar"
        if not data_dir.exists():
            return f"Error: Grammar data directory not found at {data_dir}"

        topic_lower = self.topic.lower().strip()
        topic_normalized = topic_lower.replace(" ", "_").replace("-", "_")

        # Strategy 1: Exact slug match
        exact_path = data_dir / f"{topic_normalized}.yaml"
        if exact_path.exists():
            return self._load_yaml(exact_path)

        # Strategy 2: Case-insensitive filename match
        for f in data_dir.glob("*.yaml"):
            if f.stem.lower() == topic_normalized:
                return self._load_yaml(f)

        # Strategy 3: Title match (search inside files)
        for f in data_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
                if data and "title" in data and data["title"].lower() == topic_lower:
                    return data
            except Exception:
                continue

        # Strategy 4: Fuzzy match - check if topic words appear in filename or title
        topic_words = set(topic_lower.split())
        best_match = None
        best_score = 0

        for f in data_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
                if not data:
                    continue

                # Score by filename word overlap
                stem_words = set(f.stem.lower().replace("_", " ").replace("-", " ").split())
                score = len(topic_words & stem_words)

                # Score by title word overlap
                title = data.get("title", "")
                if title:
                    title_words = set(title.lower().split())
                    score = max(score, len(topic_words & title_words))

                if score > best_score:
                    best_score = score
                    best_match = data
            except Exception:
                continue

        if best_match and best_score >= 1:
            return best_match

        # Strategy 5: Partial match - topic appears anywhere in title
        for f in data_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
                if data and "title" in data and topic_lower in data["title"].lower():
                    return data
            except Exception:
                continue

        available = sorted([f.stem for f in data_dir.glob("*.yaml")])
        return f"Error: No grammar point found for '{self.topic}'. Available grammar points: {', '.join(available[:20])}..."

    def _load_yaml(self, path: Path):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return data if data else f"Error: Empty file {path.name}"
        except Exception as e:
            return f"Error loading {path.name}: {str(e)}"
