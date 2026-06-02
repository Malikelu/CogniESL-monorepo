# Skills Mapping Data

## Schema v1.0

Cross-reference files that map grammar points, activities, and L1 patterns to the four skills (reading, listening, speaking, writing).

```yaml
# grammar_to_skills.yaml
mappings:
  - grammar_point: str       # e.g., "present_perfect"
    grammar_file: str        # e.g., "grammar/present_perfect.yaml"
    skills:
      reading:
        relevance: str       # How this grammar appears in reading
        text_types: [str]    # Where learners encounter this
        source: str
      listening:
        relevance: str
        challenges: [str]    # Listening-specific challenges
        source: str
      speaking:
        relevance: str
        functions: [str]     # Speaking functions this grammar serves
        source: str
      writing:
        relevance: str
        genres: [str]        # Writing genres where this is essential
        source: str
    l1_notes:
      - language: str
        skill_impact: str    # How L1 transfer affects this grammar in each skill
        source: str

# activities_to_skills.yaml
mappings:
  - activity_name: str
    activity_file: str
    primary_skill: str
    secondary_skills: [str]
    grammar_points: [str]
    l1_enhanced: bool
    source: str
```

## Files

| File | Purpose | Source |
|------|---------|--------|
| grammar_to_skills.yaml | Maps all 296 grammar points to 4 skills | All sources |
| activities_to_skills.yaml | Maps all 218 activities to skills | S32 Peregoy & Boyle |
