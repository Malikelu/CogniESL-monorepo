"""Validate that teacher requirements are complete and confirmed."""

from typing import List, Optional
from agency_swarm.tools import BaseTool
from pydantic import BaseModel, Field


class TeacherRequirements(BaseModel):
    topic: Optional[str] = None
    l1_languages: List[str] = Field(default_factory=list)
    age_group: Optional[str] = None
    level: Optional[str] = None
    format: List[str] = Field(default_factory=list)  # ["slides", "worksheet", "activities"]


class ValidateRequirements(BaseTool):
    """
    Validate that all teacher requirements are specified and confirmed.
    """

    topic: str = Field(..., description="Grammar topic (e.g., 'present simple')")
    l1_languages: List[str] = Field(..., description="L1 languages (e.g., ['Spanish', 'Portuguese'])")
    age_group: str = Field(..., description="Age group (e.g., 'adults', 'teenagers', 'kids')")
    level: str = Field(..., description="Proficiency level (e.g., 'beginner', 'intermediate')")
    formats: List[str] = Field(..., description="Output formats (e.g., ['slides', 'worksheet'])")
    confirmed: bool = Field(
        default=False,
        description="Has the teacher explicitly confirmed all requirements?"
    )

    def run(self) -> str:
        """Validate requirements."""

        # Check all required fields
        missing = []
        if not self.topic:
            missing.append("Topic/grammar point")
        if not self.l1_languages:
            missing.append("L1 language(s)")
        if not self.age_group:
            missing.append("Age group")
        if not self.level:
            missing.append("Level")
        if not self.formats:
            missing.append("Output format(s)")

        if missing:
            return f"INCOMPLETE: Missing {', '.join(missing)}"

        if not self.confirmed:
            return "PENDING: Requirements specified but not confirmed by teacher"

        # All good
        summary = f"""
REQUIREMENTS CONFIRMED ✓

- **Topic**: {self.topic}
- **L1 Language(s)**: {', '.join(self.l1_languages)}
- **Age Group**: {self.age_group}
- **Level**: {self.level}
- **Format(s)**: {', '.join(self.formats)}

Ready to proceed with material generation.
"""
        return summary.strip()
