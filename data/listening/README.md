# Listening Skills Data

## Schema v1.0

```yaml
skill_area: str          # e.g., "listening_strategies", "connected_speech"
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
    - stage: str         # e.g., "pre-listening", "while-listening", "post-listening"
      activities: [str]
      teacher_tips: str
      source: str

phonological_features:  # Key phonological features for this listening skill
  - feature: str        # e.g., "elision", "assimilation", "weak forms"
    description: str
    examples: [str]
    l1_challenges:      # Which L1 speakers struggle most
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
        explanation: str
        example: str
        source: str

assessment:
  task_types: [str]
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
| extensive_listening.yaml | Extensive listening (podcasts, entertainment) | S04 Biber, S33 Underhill |
| listening_strategies.yaml | Gist, detail, inference listening | S04 Biber |
| listening_connected_speech.yaml | Elision, assimilation, linking, weak forms | S33 Underhill |
| listening_sub_skills.yaml | Note-taking, predicting, recognizing discourse markers | S04 Biber |
| listening_text_types.yaml | Lectures, conversations, announcements | S04 Biber |
| listening_assessment.yaml | Comprehension task types | S32 Peregoy & Boyle |
| listening_l1_interference.yaml | L1-specific listening difficulties | S08 Swan & Smith |
