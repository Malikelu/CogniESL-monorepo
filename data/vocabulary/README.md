# Vocabulary Data

## Schema v1.0

```yaml
skill_area: str          # e.g., "academic_vocabulary", "collocations"
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
    source: str

word_lists:             # For academic/topic vocabulary
  - word: str
    part_of_speech: str
    definition: str
    example: str
    collocations: [str]
    word_family: [str]
    register: str
    source: str

collocations:           # For collocation-focused files
  - pattern: str        # e.g., "verb + noun", "adjective + noun"
    examples:
      - collocation: str
        example: str
        source: str

teaching_approach:
  stages:
    - stage: str
      activities: [str]
      teacher_tips: str
      source: str

common_difficulties:
  - difficulty: str
    affected_l1s: [str]
    explanation: str
    teaching_strategy: str
    source: str

l1_interference:        # False friends, L1 transfer in vocabulary
  - language: str
    patterns:
      - type: str       # "false_friend", "semantic_transfer", "cognate"
        l1_word: str
        l1_meaning: str
        english_false_friend: str
        english_actual_meaning: str
        example_wrong: str
        example_correct: str
        source: str

word_formation:         # For word formation focused files
  - type: str           # "prefix", "suffix", "compound", "conversion"
    pattern: str
    meaning: str
    examples: [str]
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
| academic_vocabulary.yaml | Academic word list, word families | S07 McCarthy & O'Dell |
| collocations_common.yaml | High-frequency collocations | S05 Swan |
| word_formation.yaml | Prefixes, suffixes, compounding, conversion | S01 H&P Ch.19 |
| vocabulary_learning_strategies.yaml | Memorization, context guessing, word cards | S32 Peregoy & Boyle |
| false_friends_by_l1.yaml | False friends organized by L1 | S08 Swan & Smith |
| vocabulary_l1_interference.yaml | L1-specific vocabulary transfer patterns | S08 Swan & Smith, S16 Nguyen Nhung |
