# Phonology & Pronunciation Data

## Schema v1.0

```yaml
skill_area: str          # e.g., "segmentals", "suprasegmentals", "connected_speech"
skill_name: str
cefr_range: str
description: str

definition: str

key_principles:
  - principle: str
    explanation: str
    source: str

phonological_features:
  - feature: str        # e.g., "θ/ð distinction", "word stress", "sentence intonation"
    description: str
    articulation: str   # How to produce the sound (physical/motor description)
    examples: [str]     # Minimal pairs, example words/sentences
    spelling_patterns: [str]  # Common spellings for this sound/pattern
    common_errors:
      - error: str
        correction: str
        affected_l1s: [str]
        explanation: str
    teaching_techniques:
      - technique: str
        description: str
        source: str
    source: str

l1_specific_challenges:
  - language: str
    challenges:
      - sound_or_feature: str
        l1_equivalent: str    # What exists in L1
        problem: str          # Why it's difficult
        teaching_strategy: str
        source: str

connected_speech:       # For connected speech features
  - feature: str        # e.g., "elision", "assimilation", "linking", "weak forms"
    description: str
    examples:
      - full_form: str
        reduced_form: str
        context: str
    l1_challenges:
      - language: str
        explanation: str
    source: str

activities:
  - name: str
    description: str
    type: str           # e.g., "discrimination", "production", "awareness"
    level: str
    source: str

assessment:
  methods: [str]
  source: str

sources:
  primary: str          # S33 Underhill is primary for all phonology
  secondary: [str]
```

## Files

| File | Skill Area | Source |
|------|------------|--------|
| segmentals_vowels.yaml | English vowel system, monophthongs, diphthongs | S33 Underhill |
| segmentals_consonants.yaml | English consonant system, place/manner of articulation | S33 Underhill |
| consonant_clusters.yaml | Initial and final clusters, simplification strategies | S33 Underhill |
| word_stress.yaml | Primary/secondary stress, stress patterns, compound stress | S33 Underhill |
| sentence_stress_rhythm.yaml | Stress-timed rhythm, content vs function words | S33 Underhill |
| intonation.yaml | Rising, falling, fall-rise patterns, meaning | S33 Underhill |
| connected_speech.yaml | Elision, assimilation, linking, weak forms, juncture | S33 Underhill |
| l1_phonology_arabic.yaml | Arabic-English phonological contrasts | S10 Khalil, S15 Valencia |
| l1_phonology_mandarin.yaml | Mandarin-English phonological contrasts | S11 Li & Luk |
| l1_phonology_japanese.yaml | Japanese-English phonological contrasts | S12 Kuno, S13 Oxford Handbook |
| l1_phonology_spanish.yaml | Spanish-English phonological contrasts | S14 Whitley, S15 Valencia |
| l1_phonology_french.yaml | French-English phonological contrasts | S08 Swan & Smith Ch.2 |
| l1_phonology_german.yaml | German-English phonological contrasts | S08 Swan & Smith Ch.3 |
| l1_phonology_korean.yaml | Korean-English phonological contrasts | S08 Swan & Smith Ch.15 |
| l1_phonology_thai.yaml | Thai-English phonological contrasts | S08 Swan & Smith Ch.16 |
| l1_phonology_vietnamese.yaml | Vietnamese-English phonological contrasts | S08 Swan & Smith Ch.18 |
| l1_phonology_hindi.yaml | Hindi-English phonological contrasts | S08 Swan & Smith Ch.19 |
| l1_phonology_urdu.yaml | Urdu-English phonological contrasts | S08 Swan & Smith Ch.20 |
| l1_phonology_bengali.yaml | Bengali-English phonological contrasts | S08 Swan & Smith Ch.21 |
| l1_phonology_persian.yaml | Persian-English phonological contrasts | S08 Swan & Smith Ch.22 |
| l1_phonology_generic.yaml | Phonological contrasts for remaining L1s | S08 Swan & Smith |
