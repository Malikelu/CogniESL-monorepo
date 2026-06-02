# Reading Skills Data

## Schema v1.0

Each file represents a reading skill area or sub-skill.

```yaml
skill_area: str          # e.g., "intensive_reading", "reading_strategies"
skill_name: str          # Human-readable name
cefr_range: str          # e.g., "A2-C1"
description: str         # What this skill involves

definition: str          # Detailed definition of the skill

key_principles:         # Core principles for teaching this skill
  - principle: str
    explanation: str
    source: str

sub_skills:             # Component sub-skills
  - name: str
    description: str
    examples: [str]
    source: str

teaching_approach:
  stages:
    - stage: str         # e.g., "pre-reading", "while-reading", "post-reading"
      activities: [str]
      teacher_tips: str
      source: str

common_difficulties:    # L1-specific and general difficulties
  - difficulty: str
    affected_l1s: [str]  # or "all"
    explanation: str
    teaching_strategy: str
    source: str

l1_interference:        # L1-specific reading interference patterns
  - language: str
    patterns:
      - pattern: str
        example_l1: str
        example_wrong: str
        example_correct: str
        explanation: str
        source: str

assessment:
  task_types: [str]
  rubric_criteria: [str]
  source: str

activities:             # Recommended activity types
  - name: str
    description: str
    level: str
    source: str

sources:                # Academic citations
  primary: str
  secondary: [str]
```

## Files

| File | Skill Area | Source |
|------|------------|--------|
| extensive_reading.yaml | Extensive reading (volume, pleasure) | S32 Peregoy & Boyle |
| intensive_reading.yaml | Intensive reading (detailed comprehension) | S32 Peregoy & Boyle |
| reading_strategies.yaml | Skimming, scanning, inference, prediction | S32 Peregoy & Boyle |
| reading_sub_skills.yaml | Vocabulary in context, text structure recognition | S32 Peregoy & Boyle |
| reading_text_types.yaml | News, academic, fiction, technical texts | S04 Biber |
| reading_assessment.yaml | Comprehension check types, rubrics | S32 Peregoy & Boyle |
| reading_l1_interference.yaml | L1-specific reading difficulties | S08 Swan & Smith |
