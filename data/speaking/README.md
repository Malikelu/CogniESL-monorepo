# Speaking Skills Data

## Schema v1.0

```yaml
skill_area: str          # e.g., "fluency_development", "speaking_functions"
skill_name: str
cefr_range: str
description: str

definition: str

key_principles:
  - principle: str
    explanation: str
    source: str

sub_skills:
  - name: str
    description: str
    examples: [str]
    source: str

teaching_approach:
  stages:
    - stage: str
      activities: [str]
      teacher_tips: str
      source: str

pronunciation_focus:    # Key pronunciation features for this speaking skill
  - feature: str        # e.g., "sentence stress", "intonation patterns"
    description: str
    examples: [str]
    l1_challenges:
      - language: str
        explanation: str
    source: str

common_difficulties:
  - difficulty: str
    affected_l1s: [str]
    explanation: str
    teaching_strategy: str
    source: str

l1_interference:
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

activities:
  - name: str
    description: str
    level: str
    source: str

sources:
  primary: str
  secondary: [str]
```

## Files

| File | Skill Area | Source |
|------|------------|--------|
| fluency_development.yaml | Speaking speed, confidence, hesitation management | S04 Biber |
| speaking_strategies.yaml | Turn-taking, repair, circumlocution, hedging | S04 Biber, S08 Swan & Smith |
| speaking_functions.yaml | Greeting, requesting, arguing, negotiating | S04 Biber |
| speaking_task_types.yaml | Presentations, discussions, role plays | S08 Swan & Smith |
| speaking_assessment.yaml | Rubrics, pronunciation assessment | S33 Underhill |
| speaking_l1_interference.yaml | L1-specific speaking/pragmatic difficulties | S08 Swan & Smith |
