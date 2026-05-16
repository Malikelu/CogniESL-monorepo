import yaml
from pathlib import Path
from agency_swarm.tools import BaseTool
from pydantic import Field


class SearchActivitiesTool(BaseTool):
    """
    Search the CogniESL activities database by topic, level, age group, or L1 language.
    Returns matching activities with full details (instructions, scripts, materials, duration).
    """

    topic: str = Field(
        default="",
        description="Grammar topic or keyword to search for (e.g., 'present simple', 'articles'). Searches in activity name, description, and target structures."
    )
    level: str = Field(
        default="",
        description="CEFR level to filter by (e.g., 'A1', 'A2', 'B1', 'B2', 'C1'). Empty means all levels."
    )
    age_group: str = Field(
        default="",
        description="Age group to filter by (e.g., 'kids', 'teens', 'adults'). Empty means all ages."
    )
    l1_language: str = Field(
        default="",
        description="L1 language to filter by (e.g., 'Portuguese', 'Spanish'). Checks l1Enhanced flag and keyword matches. Empty means all languages."
    )
    max_results: int = Field(
        default=5,
        description="Maximum number of activities to return. Default is 5."
    )

    def run(self):
        data_dir = Path(__file__).resolve().parents[3] / "data" / "activities"
        if not data_dir.exists():
            return f"Error: Activities data directory not found at {data_dir}"

        results = []
        topic_lower = self.topic.lower().strip() if self.topic else ""
        level_upper = self.level.upper().strip() if self.level else ""
        age_lower = self.age_group.lower().strip() if self.age_group else ""
        l1_lower = self.l1_language.lower().strip() if self.l1_language else ""

        for f in sorted(data_dir.glob("*.yaml")):
            try:
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
                if not data:
                    continue

                # Score/relevance check
                match = True

                # Topic match: check name, description, targetStructures, keywords
                if topic_lower:
                    searchable = " ".join([
                        data.get("name", ""),
                        data.get("description", ""),
                        " ".join(data.get("targetStructures", [])),
                        " ".join(data.get("keywords", [])),
                    ]).lower()
                    if topic_lower not in searchable:
                        match = False

                # Level match
                if level_upper and match:
                    levels = [l.upper() for l in data.get("bestForLevels", [])]
                    if level_upper not in levels:
                        match = False

                # Age group match
                if age_lower and match:
                    # Check groupSize and description for age clues
                    group_size = data.get("groupSize", "").lower()
                    desc = data.get("description", "").lower()
                    # If activity specifies individuals/pairs/groups, it works for all ages
                    # Only filter out if there's a clear age mismatch
                    age_indicators = {
                        "kids": ["kids", "children", "young learners", "elementary"],
                        "teens": ["teens", "teenagers", "adolescents", "middle school", "high school"],
                        "adults": ["adults", "adult", "business", "professional"],
                    }
                    if age_lower in age_indicators:
                        indicators = age_indicators[age_lower]
                        if not any(ind in desc or ind in group_size for ind in indicators):
                            # Not a hard fail — many activities work for all ages
                            # Only skip if the activity explicitly targets a different age
                            other_ages = [a for a in age_indicators if a != age_lower]
                            for other in other_ages:
                                if any(ind in desc for ind in age_indicators[other]):
                                    match = False
                                    break

                # L1 match
                if l1_lower and match:
                    l1_enhanced = data.get("l1Enhanced", False)
                    keywords = " ".join(data.get("keywords", [])).lower()
                    if not l1_enhanced and l1_lower not in keywords:
                        match = False

                if match:
                    results.append(data)
                    if len(results) >= self.max_results:
                        break

            except Exception:
                continue

        if not results:
            return f"No activities found for topic='{self.topic}', level='{self.level}', age='{self.age_group}', L1='{self.l1_language}'. Try broadening your search."

        if len(results) == 1:
            return results[0]

        return {
            "count": len(results),
            "activities": results
        }
