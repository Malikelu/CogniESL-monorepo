# CogniESL Data Architecture — Complete Inventory

> **Purpose:** Map every file, field, and relationship across all 9 skill areas.
> **Use:** Foundation for redesigning the agent's data routing logic.
> **Status:** Pre-coding — stress-test these mappings before any implementation.

> **Related Documents:**
> - `CogniELA/docs/ARCHITECTURE_DECISION.md` — ONE Forge, TWO presentation profiles (unified ESL+ELA architecture)
> - `CogniELA/docs/product-vision-2026-05-29.md` — ELA product vision with unified directory structure
> - `IMPLEMENTATION_PLAN.md` — ESL routing overhaul (Phases 0-4)

---

## Table of Contents

1. [Skill Area Overview](#1-skill-area-overview)
2. [Grammar Files](#2-grammar-files)
3. [L1 Interference Files](#3-l1-interference-files)
4. [Vocabulary Files](#4-vocabulary-files)
5. [Speaking Files](#5-speaking-files)
6. [Listening Files](#6-listening-files)
7. [Reading Files](#7-reading-files)
8. [Phonology Files](#8-phonology-files)
9. [Writing Files](#9-writing-files)
10. [Activity Files](#10-activity-files)
11. [Skills Mapping Files](#11-skills-mapping-files)
12. [Cross-Area Field Comparison](#12-cross-area-field-comparison)
13. [Teacher Request → Routing Logic](#13-teacher-request--routing-logic)
14. [Field → Output Section Mapping](#14-field--output-section-mapping)
15. [Bugs & Gaps in Current Instructions](#15-bugs--gaps-in-current-instructions)

---

## 1. Skill Area Overview

| # | Skill Area | File Count | Total Fields | Has L1 Data? | Has Activities? | Has CEFR? |
|---|------------|-----------|-------------|-------------|----------------|----------|
| 1 | Grammar | 300 | ~40 | ✅ (via L1 files) | ✅ (teaching.recommended_activities) | ✅ (level) |
| 2 | L1 Interference | 36 | ~30 per gp | N/A (is L1 data) | ✅ (teacher_tips.exercises) | ❌ |
| 3 | Vocabulary | 5 | ~17 | ✅ (l1_interference field) | ✅ (activities field) | ✅ (cefr_range) |
| 4 | Speaking | 6 | ~16 | ✅ (l1_interference field) | ✅ (activities field) | ✅ (cefr_range) |
| 5 | Listening | 5 | ~13 | ❌ (no l1_interference) | ✅ (activities field) | ✅ (cefr_range) |
| 6 | Reading | 4 | ~14 | ✅ (l1_interference field) | ✅ (activities field) | ✅ (cefr_range) |
| 7 | Phonology | 7 | ~13 | ✅ (l1_phonology file) | ✅ (activities field) | ✅ (cefr_range) |
| 8 | Writing | 18 | ~25 | ✅ (differentiation.by_l1) | ✅ (recommended_activities) | ✅ (level_range) |
| 9 | Activities | 218 | ~31 | ✅ (l1_enhanced, l1_specific) | N/A (is activity) | ✅ (bestForLevels) |
| 10 | Skills Mapping | 2 | ~10 | ✅ (mappings[].l1_notes) | ❌ | ❌ |

---

## 2. Grammar Files

**Location:** `forge/data/grammar/*.yaml` (300 files)
**Query key:** `grammar_point` (e.g., `present_simple`, `articles`, `passive_voice`)
**Activation:** Any request mentioning a grammar topic — slides, worksheet, or activity.

### 2.1 Full Field Schema

```
grammar_point        # String slug: "present_simple", "articles"
title                # Human name: "Present Simple", "Articles"
level                # CEFR: "A1", "B2", etc.
description          # One-line summary of the grammar point

┌─ meaning
│   core_meaning        # What this grammar IS (one sentence)
│   contrast            # How it differs from similar grammar
│   timeline            # Time visualization description
│   ccqs[]              # Concept Check Questions
│   │   question        #   The CCQ to ask students
│   │   answer          #   Expected correct answer
│   │   purpose         #   What this CCQ tests
│   example_generator
│       contexts        # List of real-world contexts for examples
│       cultural_notes  # Sensitivity notes for examples
│       min_examples    # Minimum examples to generate
│
├─ form
│   affirmative
│   │   structure       # Formula string: "Subject + V1 / He/She/It + V1+s"
│   │   example_generator  # Pre-written example sentences
│   │   min_examples
│   negative
│   │   structure       # "Subject + do/does + not + V1"
│   │   example_generator
│   │   min_examples
│   questions
│       structure       # "Do/Does + subject + V1?"
│       example_generator
│       min_examples
│
├─ sub_rules[]
│   rule                # The sub-rule text
│   examples[]          # Example words/sentences
│   type                # "spelling", "irregular", "lexical"
│
├─ use[]
│   context             # "Habits and routines", "General truths"
│   description         # When to use this
│   examples[]          # Example sentences per context
│
├─ common_errors[]
│   error               # WRONG sentence: "*She walk to school"
│   correction          # CORRECT sentence: "She walks to school"
│   explanation         # Why this error happens
│   l1_groups[]         # ["Portuguese", "Spanish", "Chinese"]
│   reliability         # "A", "B", "C", "D"
│   flagged             # true/false (review needed)
│   source              # Academic source for this error
│
├─ phonetics[]
│   note                # Pronunciation rule
│   example_generator[] # Example words with IPA
│   l1_issue            # L1-specific pronunciation challenge
│
├─ register_notes[]
│   note                # Formal/informal usage note
│
├─ discourse_notes[]
│   note                # How this grammar works in connected text
│
├─ dialectal_variation[]
│   note                # Variation across English dialects
│
├─ teaching
│   methodology         # "PPP", "Guided discovery", "Inductive"
│   tips[]              # Teaching tips (critical for slide design)
│   recommended_activities[]
│       name            # Activity name
│       duration        # Minutes
│       adaptation_notes # How to adapt
│
└─ sources
    primary             # Main academic source
    secondary           # Supporting sources
    pedagogical         # Teaching methodology source
    teaching_practice   # Classroom practice source
    validation          # Validation/synthesis source
    corpus_evidence     # Corpus linguistics source
```

### 2.2 Current Agent Coverage (instructions.md)

| Field | Extracted? | Used in? |
|-------|-----------|----------|
| meaning.core_meaning | ✅ | Content Brief, Meaning slide |
| meaning.contrast | ✅ | Content Brief, Meaning slide |
| meaning.timeline | ✅ | Timeline slide |
| ccqs[].question + answer | ✅ | CCQ slides |
| ccqs[].purpose | ❌ | Not extracted |
| meaning.example_generator | ❌ | Not extracted |
| form.*.structure | ✅ | Formula slides |
| form.*.example_generator | ❌ | Not extracted |
| sub_rules[].rule + examples | ✅ | Sub-rule slides |
| sub_rules[].type | ❌ | Not extracted |
| use[].context + description + examples | ✅ | Practice examples |
| common_errors[].error + correction + explanation + l1_groups | ✅ | Practice slides |
| common_errors[].flagged | ❌ | Not extracted |
| common_errors[].source | ❌ | Not extracted |
| phonetics[].note + l1_issue | ✅ | Pronunciation slide |
| register_notes | ❌ | **Missing** — could inform register notes on slides |
| discourse_notes | ❌ | **Missing** — could inform discourse context |
| dialectal_variation | ❌ | **Missing** — could inform variation notes |
| teaching.tips | ✅ | Slide design hints |
| teaching.recommended_activities | ✅ | Activity selection |
| sources | ❌ | Not used in output |
| citations | ❌ | Reference only |

### 2.3 Activation Rules

| Teacher says | File queried | Fields extracted |
|-------------|-------------|-----------------|
| "[grammar topic]" | `grammar/{slug}.yaml` | All above |
| "[grammar topic] slides" | + L1 file | + L1 interference |
| "[grammar topic] worksheet" | + L1 file | + common_errors (for exercises) |
| "[grammar topic] activity" | + activities | + recommended_activities |

---

## 3. L1 Interference Files

**Location:** `forge/data/l1-interference/*_interference.yaml` (36 files, ~30 languages)
**Query key:** `language` (e.g., "Spanish", "Portuguese") or `l1` code (e.g., "es", "pt")
**Activation:** Any request that specifies an L1 language for students.

### 3.1 Full Field Schema

```
schema_version         # Schema version, e.g. "4.0"
language               # Human name: "Spanish", "Portuguese"
l1                     # ISO code: "es", "pt"
l2                     # Target language: "en"
total_grammar_points   # Count of grammar points covered

┌─ writing_interference[]         # NEW FIELD — completely unused by agent
│   area                          # "argumentative_essay", "paragraph_structure"
│   description                   # How L1 affects writing in this genre
│   common_errors[]
│   │   error                    # Example of the writing error
│   │   correction               # Corrected version
│   │   explanation              # Why this happens
│   source                       # Academic reference
│
├─ grammar_points
│   {grammar_slug}               # e.g., "ser_vs_estar", "articles"
│   │
│   ├─ interference_patterns[]
│   │   pattern                  # Name of the pattern
│   │   example_l1               # Example in L1 language
│   │   example_gloss            # Word-for-word English gloss
│   │   example_wrong            # WRONG English sentence
│   │   example_correct          # CORRECT English sentence
│   │   explanation              # Why the error happens
│   │   frequency                # 1-5 rating
│   │   persistence              # 1-5 rating
│   │   communicative_impact     # 1-5 rating
│   │   reliability              # "A", "B", "C", "D"
│   │   etiology                 # "interlingual", "intralingual"
│   │   flagged                  # true/false
│   │   tier                     # 1-4 (source quality)
│   │
│   ├─ why_it_happens            # ⚠️ BUG: agent looks for this PER PATTERN but it's here
│   ├─ teacher_tips
│   │   how_to_explain           # How to explain this to students
│   │   where_to_start           # Where to begin teaching
│   │   sequencing               # Suggested teaching order
│   │   exercises[]
│   │       name                 # Exercise name
│   │       type                 # "translation", "error-correction", etc.
│   │       description          # What students do
│   │       duration             # Minutes
│   │
│   ├─ examples[]                # Wrong→Correct example pairs
│   ├─ sources[]                 # Academic sources for this data
│   ├─ source_count              # Number of sources
│   ├─ source_type               # "peer-reviewed", etc.
│   ├─ frequency                 # Grammar-point-level frequency
│   ├─ persistence               # Grammar-point-level persistence
│   ├─ communicative_impact      # Grammar-point-level impact
│   ├─ flagged                   # true/false
│   ├─ tier                      # 1-4
│   ├─ individually_assessed     # true/false
│   ├─ assessment                # Assessment text
│   ├─ source_rank               # 1-5
│   └─ citations[]               # Detailed citations per grammar point
│
├─ etiology[]                    # Overall L1 etiology research
├─ coverage                      # Stats on coverage
└─ citations[]                   # Top-level citations
```

### 3.2 Current Agent Coverage (instructions.md)

| Field | Extracted? | Used in? |
|-------|-----------|----------|
| interference_patterns[].pattern | ✅ | L1 Oracle slide title |
| interference_patterns[].example_wrong | ✅ | L1 Oracle: "✗" example |
| interference_patterns[].example_correct | ✅ | L1 Oracle: "✓" example |
| interference_patterns[].frequency | ✅ | Sorting (≥3 threshold) |
| interference_patterns[].persistence | ✅ | Sorting (≥3 threshold) |
| interference_patterns[].communicative_impact | ✅ | Sorting reference |
| interference_patterns[].why_it_happens | ❌ | **BUG**: extracted per-pattern but YAML has it at grammar_point level |
| interference_patterns[].reliability | ❌ | Not extracted |
| interference_patterns[].flagged | ❌ | Not extracted |
| interference_patterns[].etiology | ❌ | Not extracted |
| **grammar_point.why_it_happens** | ❌ | **BUG: THIS is where it actually lives** |
| grammar_point.teacher_tips.how_to_explain | ✅ | Speaker notes |
| grammar_point.teacher_tips.sequencing | ✅ | Slide sequencing |
| grammar_point.teacher_tips.exercises | ✅ | Practice slides |
| grammar_point.examples | ❌ | Not used — could be additional L1 Oracle content |
| grammar_point.sources | ❌ | Not used |
| grammar_point.citations | ❌ | Not used |
| grammar_point.flagged | ❌ | Could skip low-quality data |
| grammar_point.tier | ❌ | Could use for confidence |
| **writing_interference** | ❌ | **Entirely missing** — 4-rich-genre content |
| etiology | ❌ | Research reference |
| coverage | ❌ | Stats reference |

### 3.3 Activation Rules

| Teacher says | File queried | Fields extracted | Output affected |
|-------------|-------------|-----------------|----------------|
| "[L1] speakers" | `l1-interference/{l1}_interference.yaml` | grammar_point.interference_patterns | L1 Oracle slides |
| "[L1] writing" | + writing_interference | writing_interference | Worksheet writing section |
| "[L1] pronunciation" | + phonetics data | (not in L1 file) | Pronunciation slide |

### 3.4 Available Languages (36)

arabic, bengali, czech, danish, dholuo, dutch, finnish, french, german, greek, haitian_creole, hebrew, hindi, hungarian, indonesian, italian, japanese, korean, mandarin, norwegian, persian, polish, portuguese, romanian, russian, somali, spanish, swahili, swedish, tagalog, tamil, thai, turkish, urdu, vietnamese

---

## 4. Vocabulary Files

**Location:** `forge/data/vocabulary/*.yaml` (5 files)
**Query key:** `skill_name` or file name
**Activation:** Request mentioning vocabulary, word lists, collocations, or word formation.

### 4.1 Files

| File | Focus |
|------|-------|
| `academic_vocabulary.yaml` | Academic word lists, formal vocabulary |
| `collocations_common.yaml` | Common collocations, word partnerships |
| `vocabulary_l1_interference.yaml` | L1-specific vocabulary challenges |
| `vocabulary_learning_strategies.yaml` | How to learn vocabulary |
| `word_formation.yaml` | Prefixes, suffixes, compound words |

### 4.2 Full Field Schema

```
skill_area             # "Vocabulary"
skill_name             # "Collocations", "Academic Vocabulary"
cefr_range             # ["B1", "B2", "C1"]
definition             # What this vocabulary area is
description            # Detailed description

┌─ key_principles[]
│   principle           # Core principle
│   reliability         # Source reliability
│   source              # Academic source
│
├─ sub_skills[]         # Specific sub-skills
├─ common_difficulties[]
│   difficulty          # Description of difficulty
│   cause               # Why it happens
│   solution            # How to address
│
├─ l1_interference      # NEW FIELD - L1-specific data
├─ word_lists           # Lists of vocabulary items
├─ collocations         # Common word partnerships
├─ word_formation       # Prefix/suffix/compound rules
├─ teaching_approach    # How to teach this
├─ activities[]
│   name                # Activity name
│   description         # What students do
│   level               # Target level
│   source              # Activity source
│   type                # Activity type
│
├─ citations[]
└─ sources
```

### 4.3 Agent Coverage

**Current: ❌ NOTHING.** The agent has no extraction instructions for vocabulary files.

### 4.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "vocabulary worksheet" | vocabulary/*.yaml | Worksheet with word lists + exercises |
| "collocations practice" | collocations_common.yaml | Practice exercises |
| "academic vocabulary" | academic_vocabulary.yaml | Academic word list + exercises |
| "word formation" | word_formation.yaml | Formation rules + practice |
| "[topic] vocabulary for [L1]" | vocabulary/*.yaml + l1-interference | L1-specific vocabulary drills |

---

## 5. Speaking Files

**Location:** `forge/data/speaking/*.yaml` (6 files)
**Query key:** `skill_name` or file name
**Activation:** Request mentioning speaking, conversation, fluency, or oral skills.

### 5.1 Files

| File | Focus |
|------|-------|
| `fluency_development.yaml` | Building speaking fluency |
| `speaking_assessment.yaml` | Assessing speaking skills |
| `speaking_functions.yaml` | Functional language (requests, opinions, etc.) |
| `speaking_l1_interference.yaml` | L1 challenges in speaking |
| `speaking_strategies.yaml` | Communication strategies |
| `speaking_task_types.yaml` | Types of speaking tasks |

### 5.2 Full Field Schema

```
skill_area             # "Speaking"
skill_name             # e.g., "Speaking Functions"
cefr_range             # Target CEFR levels
definition             # What this speaking area is
description            # Detailed description

┌─ key_principles[]
│   principle
│   reliability
│   source
│
├─ sub_skills[]         # Sub-skills (as strings or structured)
├─ common_difficulties[]
│   difficulty
│   cause
│   solution
│
├─ l1_interference      # L1-specific speaking challenges
├─ l1_profiles          # Per-language profiles
├─ pronunciation_focus  # Pronunciation elements to target
├─ teaching_approach    # How to teach speaking
├─ assessment
│   rubric_criteria[]
│   task_types[]
│
├─ activities[]
│   name, description, level, source, type
│
├─ citations[]
└─ sources
```

### 5.3 Agent Coverage

**Current: ❌ NOTHING.**

### 5.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "speaking activity" | speaking_functions.yaml + activities | Activity guide with speaking focus |
| "fluency practice" | fluency_development.yaml | Fluency exercises |
| "conversation practice" | speaking_strategies.yaml | Conversation activities |
| "[L1] speaking challenges" | speaking_l1_interference.yaml | L1-specific speaking drills |

---

## 6. Listening Files

**Location:** `forge/data/listening/*.yaml` (5 files)
**Query key:** `skill_name` or file name
**Activation:** Request mentioning listening or audio comprehension.

### 6.1 Files

| File | Focus |
|------|-------|
| `extensive_listening.yaml` | Long-form listening |
| `listening_connected_speech.yaml` | Connected speech patterns |
| `listening_strategies.yaml` | Listening comprehension strategies |
| `listening_sub_skills.yaml` | Specific listening sub-skills |
| `listening_text_types.yaml` | Types of listening texts |

### 6.2 Full Field Schema

```
skill_area             # "Listening"
skill_name             # e.g., "Listening Strategies"
cefr_range             # Target CEFR levels
definition
description

┌─ key_principles[]
│   principle
│   explanation
│   reliability
│   source
│
├─ sub_skills[]
│   name, description, examples, source
├─ common_difficulties[]
│   difficulty, explanation, l1_groups, teaching_strategy
├─ phonological_features[]   # Connected speech elements
│   feature, description, examples, source
├─ teaching_approach
│   stages[].stage, activities, teacher_tips
├─ activities[]
│   name, description, level, source
├─ citations[]
└─ sources
```

### 6.3 Agent Coverage

**Current: ❌ NOTHING.**

### 6.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "listening activity" | listening_strategies.yaml + activities | Listening activity guide |
| "listening practice" | listening_sub_skills.yaml | Listening exercises |
| "connected speech" | listening_connected_speech.yaml | Pronunciation + listening |

Note: Listening has NO `l1_interference` field — L1-specific listening challenges would need to come from the L1 interference file or phonology.

---

## 7. Reading Files

**Location:** `forge/data/reading/*.yaml` (4 files)
**Query key:** `skill_name` or file name
**Activation:** Request mentioning reading or text comprehension.

### 7.1 Files

| File | Focus |
|------|-------|
| `extensive_reading.yaml` | Long-form reading |
| `intensive_reading.yaml` | Detailed reading analysis |
| `reading_strategies.yaml` | Reading comprehension strategies |
| `reading_sub_skills.yaml` | Specific reading sub-skills |

### 7.2 Full Field Schema

```
skill_area             # "Reading"
skill_name             # e.g., "Reading Strategies"
cefr_range             # Target CEFR levels
definition
description

┌─ key_principles[]
│   principle, explanation, reliability, source
├─ sub_skills[]
│   name, description, examples, source
├─ common_difficulties[]
│   difficulty, explanation, l1_groups, teaching_strategy
├─ l1_interference[]       # NEW FIELD - L1-specific reading challenges
│   language, patterns[].pattern, example_wrong, explanation
├─ teaching_approach
│   stages[].stage, activities, teacher_tips
├─ assessment
│   rubric_criteria[], task_types[]
├─ activities[]
│   name, description, level, source
├─ citations[]
└─ sources
```

### 7.3 Agent Coverage

**Current: ❌ NOTHING.**

### 7.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "reading activity" | reading_strategies.yaml + activities | Reading activity guide |
| "reading comprehension" | intensive_reading.yaml | Comprehension exercises |
| "[L1] reading challenges" | + l1-interference | L1-specific reading support |

---

## 8. Phonology Files

**Location:** `forge/data/phonology/*.yaml` (7 files)
**Query key:** `skill_name` or file name
**Activation:** Request mentioning pronunciation, sounds, stress, or intonation.

### 8.1 Files

| File | Focus |
|------|-------|
| `connected_speech.yaml` | Linking, reduction, elision |
| `intonation.yaml` | Pitch patterns |
| `l1_phonology_dutch.yaml` | L1-specific Dutch phonology |
| `segmentals_consonants.yaml` | Consonant sounds |
| `segmentals_vowels.yaml` | Vowel sounds |
| `sentence_stress_rhythm.yaml` | Sentence-level stress |
| `word_stress.yaml` | Word-level stress |

### 8.2 Full Field Schema

```
skill_area             # "Phonology"
skill_name             # e.g., "Word Stress", "Connected Speech"
cefr_range             # Target CEFR levels
definition
description

┌─ key_principles[]
│   principle, explanation, reliability, source
├─ phonological_features[]
│   feature              # e.g., "Primary stress", "Secondary stress"
│   description          # What it is
│   articulation         # How to produce
│   examples[]           # Example words/sentences
│   common_errors[]
│   │   error, description, explanation, l1_groups
│   spelling_patterns    # Rules for spelling→sound
│   teaching_techniques[]
│       technique, description, source
│   source
├─ activities[]
│   name, description, level, source, type
├─ assessment
│   methods[], source
├─ underhill_teaching_framework  # Connected speech only
├─ l1_specific_challenges        # L1-specific files only
├─ citations[]
└─ sources
```

### 8.3 Agent Coverage

**Current: ❌ NOTHING.** (The agent extracts phonetics from grammar files, but has no instructions for phonology skill files.)

### 8.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "pronunciation practice" | phonology/segmentals_*.yaml | Pronunciation drills |
| "stress patterns" | word_stress.yaml + sentence_stress_rhythm.yaml | Stress exercises |
| "connected speech" | connected_speech.yaml | Linking/reduction practice |
| "[L1] pronunciation" | phonology/l1_phonology_*.yaml | L1-specific pronunciation |

---

## 9. Writing Files

**Location:** `forge/data/writing/{conventions,genres,process}/*.yaml` (18 files)
**Query key:** `topic`, `genre.type`, or file name
**Activation:** Request mentioning writing, essay, composition, or a specific genre.

### 9.1 Files

**Conventions (3 files):**
- `citation-apa-mla.yaml` — Citation styles
- `formatting.yaml` — Document formatting
- `punctuation-advanced.yaml` — Advanced punctuation

**Genres (10 files):**
- `academic-essay.yaml`, `argumentative.yaml`, `business-email.yaml`, `cause-effect.yaml`,
  `compare-contrast.yaml`, `cover-letter.yaml`, `descriptive.yaml`, `expository.yaml`,
  `narrative.yaml`, `process-analysis.yaml`

**Process (5 files):**
- `drafting.yaml`, `editing.yaml`, `peer-review.yaml`, `prewriting.yaml`, `revising.yaml`

### 9.2 Full Field Schema

```
skill_area             # "Writing"
title                  # "Argumentative Essay", "Drafting"
topic                  # "argumentative", "drafting"
genre                  # STRUCTURED: {type: "argumentative", structure: [...]} (genres only)
level_range            # {min: "B1", max: "C1"}
definition             # What this writing type is
description            # Detailed description
what_it_is_not         # What it's NOT (prevents confusion)

┌─ key_principles[]
│   principle, explanation, flagged, reliability
├─ ccqs[]
│   question, answer, purpose
├─ register_notes       # Formal/informal register guidance
│   content, reliability, source, tier
├─ common_pitfalls[]    # Common student mistakes
│   pitfall, solution, reliability, source
├─ cross_skill_connections  # How this connects to other skills
│   grammar[], reading[], speaking[]
├─ grammar_focus[]      # Grammar points relevant to this writing
├─ scaffolding
│   for_beginners[]     # Sentence starters, frames
│   for_intermediate[]
│   for_advanced[]
│   graphic_organizers[]
│   sentence_starters[]
├─ differentiation
│   by_l1[]             # L1-specific adaptations
│   │   language, specific_challenges, adaptations
│   by_level[]
│       level, modifications
├─ teaching_approach
│   stages[].stage, purpose, duration, student_actions, teacher_actions
├─ teaching_tips[]
│   context, tip
├─ recommended_activities[]
├─ process_stages[]     # Writing process only
│   stage, purpose, duration, student_activities, teacher_role
├─ essay_exam_strategies  # Genres only
├─ integrating_sources    # Genres only
├─ assessment
│   criteria[].criterion, levels[].level, description, score_range
├─ citations[]
└─ sources
```

### 9.3 Agent Coverage

**Current: ❌ NOTHING.**

### 9.4 Activation Rules

| Teacher says | File(s) queried | Output produced |
|-------------|----------------|-----------------|
| "[genre] essay" | writing/genres/{genre}.yaml | Essay guide + structure |
| "writing process" | writing/process/{stage}.yaml | Process guide |
| "writing conventions" | writing/conventions/{topic}.yaml | Convention reference |
| "worksheet for [genre]" | writing/genres/{genre}.yaml + grammar | Worksheet with writing section |
| "[L1] writing challenges" | writing conventions + l1_interference | L1-specific writing support |

---

## 10. Activity Files

**Location:** `forge/data/activities/*.yaml` (218 files)
**Query key:** `id`, `keywords`, `skill_areas`, `grammar_focus`, `name`
**Activation:** Any request that includes an activity guide or activities in the format.

### 10.1 Full Field Schema

```
id                   # Unique identifier (e.g., "role-play-interviews-88564c")
name                 # Human name: "Role Play Interviews"
category             # "speaking", "grammar", "vocabulary", etc.
description          # One-line summary
format               # ["individual", "pair", "group", "whole-class"]
groupSize            # "pair", "small-group", "whole-class"
duration             # Minutes
energyRequired       # "low", "medium", "high"
prepTime             # "none", "low", "medium", "high"
digitalReady         # true/false
requiresTech         # true/false

hasAudioComponent    # true/false
hasPrintableComponent # true/false
hasSlidesComponent   # true/false
hasVisualComponent   # true/false

bestForLevels[]      # ["A1", "A2", "B1", "B2", "C1"]
bestForAges[]        # ["children", "teens", "adults"]

adaptableToTopic     # true/false
grammar_focus[]      # Grammar points this activity targets
skill_areas[]        # ["speaking", "listening", "grammar"]
targetStructures[]   # Language structures practiced

keywords[]           # Search keywords
materials[]          # Required materials
instructions[]       # Step-by-step instructions
script[]             # Exact words teacher should say

setupInstructions    # How to prepare

l1_enhanced[]        # NEW FIELD - L1-specific adaptations
│   language         # Target L1
│   adaptation       # How to adapt for this L1
│   priority         # "high", "medium", "low"
l1_specific          # true/false (was designed for specific L1)

differentiation
├─ support            # How to support weaker students
└─ extension          # How to extend for stronger students

teaching_tips         # General teaching tips
exampleSnippet        # Example of the activity in action

citations[]
└─ sources
```

### 10.2 Current Agent Coverage

| Field | Extracted? | Used in? |
|-------|-----------|----------|
| name | ✅ | Content Brief |
| duration | ✅ | Content Brief |
| instructions | ✅ | Activity guide |
| script | ✅ | Activity guide |
| materials | ✅ | Activity guide |
| differentiation.support | ✅ | Activity guide |
| differentiation.extension | ✅ | Activity guide |
| targetStructures | ✅ | Content Brief |
| | | |
| **NEW FIELDS (not extracted):** | |
| category | ❌ | Could filter by skill area |
| bestForLevels | ❌ | Could match to student level |
| bestForAges | ❌ | Could match to age group |
| format | ❌ | Could match group size |
| groupSize | ❌ | Could suggest pairs/groups |
| energyRequired | ❌ | Could match class energy |
| prepTime | ❌ | Could warn about prep |
| digitalReady | ❌ | Could check tech availability |
| requiresTech | ❌ | Could check tech requirements |
| has*Component | ❌ | Could filter by output type |
| l1_enhanced | ❌ | **Key** — could offer L1-specific adaptations |
| l1_specific | ❌ | Could highlight L1-ready activities |
| skill_areas | ❌ | **Key** — could route to correct skill file |
| grammar_focus | ❌ | **Key** — could filter by grammar topic |
| keywords | ❌ | Could improve search |
| setupInstructions | ❌ | Could include in activity guide |
| adaptableToTopic | ❌ | Could flag generic activities |
| citations | ❌ | Not needed for output |
| sources | ❌ | Not needed for output |

### 10.3 Activation Rules

| Condition | Activities filtered by |
|-----------|----------------------|
| Grammar topic + any L1 | grammar_focus matches + l1_specific or l1_enhanced |
| Age group | bestForAges matches |
| Level | bestForLevels matches |
| Format (slides/worksheet/activity) | has*Component matches |
| Skill area (speaking/listening/etc.) | skill_areas matches |
| Digital classroom | digitalReady = true |
| Low prep | prepTime = "low" or "none" |

---

## 11. Skills Mapping Files

**Location:** `forge/data/skills_mapping/*.yaml` (2 files)
**Purpose:** Cross-reference grammar points and activities to skill areas.

### 11.1 Files

| File | Maps |
|------|------|
| `grammar_to_skills.yaml` | Each grammar_point → which listening, reading, speaking, writing skills it connects to |
| `activities_to_skills.yaml` | Each activity → which skill areas it serves |

### 11.2 Full Field Schema

```
# grammar_to_skills.yaml
mappings[]
│   grammar_file      # "present_simple.yaml"
│   grammar_point     # "present_simple"
│   skills
│   ├─ listening
│   │   relevance     # How grammar relates to listening
│   │   challenges    # Listening challenges for this grammar
│   │   source
│   │   text_types[]  # Types of listening texts
│   ├─ speaking
│   │   relevance
│   │   functions[]   # Speaking functions practiced
│   │   source
│   ├─ reading
│   │   relevance
│   │   text_types[]
│   │   source
│   └─ writing
│       relevance
│       genres[]      # Writing genres relevant
│       source
│   l1_notes[]        # L1-specific skill impact
│       language
│       skill_impact
│       source
```

### 11.3 Activation Rules

This is the **routing table** — it tells the agent: "When a teacher asks about present simple, here's which speaking functions, writing genres, reading types, and listening texts connect to it."

Without this, the agent has no way to know that present simple connects to:
- Speaking: describing routines, giving instructions
- Writing: process analysis, narrative
- Reading: schedules, instructions

---

## 12. Cross-Area Field Comparison

### 12.1 Common Fields Across All Skill Areas

Every skill area file shares these fields:

| Field | Grammar | L1 | Vocab | Speaking | Listening | Reading | Phonology | Writing | Activity |
|-------|---------|-----|-------|----------|-----------|---------|-----------|---------|----------|
| skill_area | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| skill_name | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| cefr_range / level | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| description | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| definition | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| key_principles | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| citations | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sources | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| activities | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | N/A |
| l1_interference | ❌ | N/A | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |

### 12.2 Unique Fields Per Area

| Area | Unique Fields |
|------|--------------|
| GRAMMAR | meaning, form, sub_rules, ccqs, common_errors, phonetics, register_notes, discourse_notes, dialectal_variation, teaching |
| L1 | interference_patterns, writing_interference, etiology, coverage, teacher_tips |
| VOCABULARY | word_lists, collocations, word_formation |
| SPEAKING | l1_profiles, pronunciation_focus |
| LISTENING | phonological_features (shared with phonology) |
| READING | (no unique fields — shares sub_skills, common_difficulties) |
| PHONOLOGY | phonological_features (with articulation, common_errors, teaching_techniques), underhill_teaching_framework |
| WRITING | common_pitfalls, scaffolding, differentiation.by_l1, process_stages, essay_exam_strategies, integrating_sources, register_notes (structured), what_it_is_not, cross_skill_connections |
| ACTIVITY | format, groupSize, duration, energyRequired, prepTime, digitalReady, requiresTech, has*Component, l1_enhanced, l1_specific, skill_areas, grammar_focus, targetStructures, keywords, instructions, script, setupInstructions |

### 12.3 Fields That Mean The Same Thing But Use Different Names

| Concept | Grammar | L1 | Vocab/Speaking/etc. | Activity | Writing |
|---------|---------|-----|--------------------|----------|---------|
| Student errors | `common_errors` | `interference_patterns` | `common_difficulties` | — | `common_pitfalls` |
| Teaching method | `teaching.tips` | `teacher_tips` | `teaching_approach` | `teaching_tips` | `teaching_tips` |
| Level | `level` (A1) | — | `cefr_range` | `bestForLevels` | `level_range` |
| Age | — | — | — | `bestForAges` | — |
| Activities | `teaching.recommended_activities` | `teacher_tips.exercises` | `activities[]` | N/A | `recommended_activities` |
| L1 connection | `common_errors[].l1_groups` | N/A | `l1_interference` | `l1_enhanced`, `l1_specific` | `differentiation.by_l1` |
| Support | — | — | — | `differentiation.support` | `scaffolding` |
| Extension | — | — | — | `differentiation.extension` | `scaffolding.for_advanced` |
| Grammar connection | N/A | `grammar_points` | — | `grammar_focus` | `grammar_focus` |

> **⚠️ This is critical for routing:** When routing, the agent must normalize these different names to the same concept.

---

## 13. Teacher Request → Routing Logic

### 13.1 Request Type Classifier

When a teacher sends a request, the agent must classify it along these dimensions:

```
Request: "Slides for present simple for Spanish-speaking adults"

Dimensions:
  ┌─ TOPIC TYPE:   grammar | vocabulary | phonology | writing | speaking | listening | reading
  ├─ OUTPUT TYPE:  slides | worksheet | activity_guide | flashcards | all
  ├─ L1 LANGUAGE:  specific (e.g., "Spanish") | multiple (e.g., "Chinese and Japanese") | none
  ├─ AGE GROUP:    children | teens | adults | (empty = default adults)
  └─ LEVEL:        A1 | A2 | B1 | B2 | C1 | (empty = from grammar file)
```

### 13.2 Activation Matrix

Which files activate based on (TOPIC TYPE × OUTPUT TYPE):

```
                    │ SLIDES      │ WORKSHEET   │ ACTIVITY     │ FULL LESSON
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
GRAMMAR             │ grammar     │ grammar     │ grammar      │ grammar
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + activities
                    │             │             │              │ + skills_map
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
VOCABULARY          │ vocabulary  │ vocabulary  │ vocabulary   │ vocabulary
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + skills_map
                    │             │             │              │ + writing (maybe)
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
SPEAKING            │ speaking    │ speaking    │ speaking     │ speaking
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + activities
                    │             │             │              │ + skills_map
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
LISTENING           │ listening   │ listening   │ listening    │ listening
                    │             │             │ + activities │ + activities
                    │             │             │              │ + skills_map
                    │             │             │              │ + grammar (?)
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
READING             │ reading     │ reading     │ reading      │ reading
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + activities
                    │             │             │              │ + skills_map
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
PHONOLOGY           │ phonology   │ phonology   │ phonology    │ phonology
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + activities
────────────────────┼─────────────┼─────────────┼──────────────┼──────────────
WRITING             │ writing     │ writing     │ writing      │ writing
                    │ + L1        │ + L1        │ + L1         │ + L1
                    │             │             │ + activities │ + activities
                    │             │             │              │ + skills_map
                    │             │             │              │ + grammar (?)
```

### 13.3 L1 Language Activation

When L1 is specified, it activates:

| Skill Area | L1 Data Source | What Activates |
|------------|---------------|----------------|
| Grammar | `l1-interference/{l1}.yaml` → grammar_point | L1 Oracle slides |
| Vocabulary | `vocabulary/*.yaml` → l1_interference, or `vocabulary_l1_interference.yaml` | L1 vocabulary drills |
| Speaking | `speaking/speaking_l1_interference.yaml` or l1_interference field | L1 speaking notes |
| Reading | `reading/*.yaml` → l1_interference field | L1 reading support |
| Phonology | `phonology/l1_phonology_{l1}.yaml` (if exists) | L1 pronunciation drills |
| Writing | `writing/*/**.yaml` → differentiation.by_l1 | L1 writing adaptations |
| Activities | `activities/*.yaml` → l1_enhanced[].language match | L1-specific activity adaptations |

---

## 14. Field → Output Section Mapping

How each field maps to the final output:

### 14.1 Slide Deck (HTML Offline Bundle)

| Section | Slides | Data Sources |
|---------|--------|-------------|
| 1. Lesson Plan Cover | 1 slide | Metadata: grammar_point, level, age |
| 2. Hook | 1 slide | teaching.tips (visual ones) → slide design |
| 3. Meaning Overview | 1 slide | meaning.core_meaning, meaning.contrast |
| 4. CCQ Discovery | 1 slide per CCQ | meaning.ccqs[].question + answer |
| 5. Formula | 3 slides (affirmative, negative, questions) | form.*.structure |
| 6. Sub-rules | 1-2 slides | sub_rules[].rule + examples |
| 7. Practice | 3 slides | common_errors → gap-fill, error-correction, L1 drill |
| 8. Pronunciation | 1 slide (if phonetics exists) | phonetics[].note, l1_issue |
| 9. L1 Oracle | 1-2 slides per L1 | interference_patterns: wrong→correct + why_it_happens |
| 10. Wrap-up | 1-2 slides | Summary of key points |
| 11. Closing Brand | 1 slide | Fixed template |

### 14.2 Worksheet (PDF)

| Section | Data Sources |
|---------|-------------|
| A. Gap-fill | common_errors (sentences with blanks) |
| B. Error Correction | common_errors (wrong→correct pairs) |
| C. L1 Drills | L1 interference_patterns (wrong→correct, targeted) |
| D. Activity | recommended_activities or activities/* |
| E. Free Production | use[].context → writing prompt |
| Answer Key | Corrections + why_it_happens explanations |

### 14.3 Activity Guide

| Section | Data Sources |
|---------|-------------|
| Activity Overview | activities: name, duration, groupSize, format |
| Setup | setupInstructions, materials, prepTime |
| Instructions | instructions[] (step-by-step) |
| Script | script[] (teacher talk) |
| Differentiation | differentiation.support + extension |
| L1 Adaptations | l1_enhanced[language match].adaptation |
| Teaching Tips | teaching_tips |

### 14.4 Flashcards

| Card Content | Data Sources |
|-------------|-------------|
| Front: Trigger | sub_rules[].examples, common_errors[].error |
| Back: Response | sub_rules[].rule, common_errors[].correction |
| L1 Bonus: Why | interference_patterns[].explanation |

---

## 15. Bugs & Gaps in Current Instructions

### 🐛 BUG 1: `why_it_happens` Location Mismatch

**What instructions say:**
```
L1 INTERFERENCE EXTRACTION:
  Pattern 1:
    why_it_happens: [exact explanation]
```

**What the YAML actually has:**
```yaml
grammar_points:
  ser_vs_estar:
    why_it_happens: "Spanish has two copulas..."  # ← HERE, not in pattern
    interference_patterns:
      - pattern: "..."
        # NO why_it_happens here
```

**Fix:** Change instructions to extract `grammar_points.{slug}.why_it_happens`, not `pattern.why_it_happens`.

### 🐛 BUG 2: Grammar Files Missing from Extraction for Non-Grammar Requests

**Current behavior:** Agent only queries grammar files for grammar requests.
**Needed:** Grammar files also provide `common_errors` and `sub_rules` that are relevant to vocabulary, writing, and speaking materials.

### 🔴 GAP 1: No Instructions for 6 Skill Areas

The agent has **zero** extraction instructions for:
- Vocabulary (5 files, 17 fields)
- Speaking (6 files, 16 fields)
- Listening (5 files, 13 fields)
- Reading (4 files, 14 fields)
- Phonology (7 files, 13 fields)
- Writing (18 files, 25 fields)

### 🔴 GAP 2: Skills Mapping Files Not Used

The `grammar_to_skills.yaml` and `activities_to_skills.yaml` files are the **routing table** for cross-skill connections. Without them, the agent cannot:

- Know which speaking functions connect to a grammar point
- Know which writing genres are relevant
- Recommend cross-skill activities

### 🔴 GAP 3: `writing_interference` Not Used

The L1 files contain rich writing interference data (4+ genres per language) that the agent never extracts or uses in worksheets.

### 🔴 GAP 4: Activity Filtering Too Basic

Current instructions just pick "3 best-matching" activities. The enriched activity files have `skill_areas`, `grammar_focus`, `l1_enhanced`, `has*Component`, and other fields that allow precise filtering.

### 🔴 GAP 5: No Cross-File Field Name Normalization

Different files call the same things by different names (teaching.tips vs teacher_tips, common_errors vs common_difficulties vs common_pitfalls, level vs cefr_range vs bestForLevels). The agent needs a normalization layer.

---

## Appendix A: All Files Count

| Directory | Count |
|-----------|-------|
| grammar/ | 300 |
| l1-interference/ | 36 |
| vocabulary/ | 5 |
| speaking/ | 6 |
| listening/ | 5 |
| reading/ | 4 |
| phonology/ | 7 |
| writing/conventions/ | 3 |
| writing/genres/ | 10 |
| writing/process/ | 5 |
| activities/ | 218 |
| skills_mapping/ | 2 |
| **Total** | **601** |

## Appendix B: All L1 Languages

arabic, bengali, czech, danish, dholuo, dutch, finnish, french, german, greek, haitian_creole, hebrew, hindi, hungarian, indonesian, italian, japanese, korean, mandarin, norwegian, persian, polish, portuguese, romanian, russian, somali, spanish, swahili, swedish, tagalog, tamil, thai, turkish, urdu, vietnamese

## Appendix C: All CEFR Levels Referenced

A1, A2, B1, B2, C1

## Appendix D: Activity Categories

(From 218 activity files — common categories observed)
grammar, vocabulary, speaking, listening, reading, writing, pronunciation, mixed, review, icebreaker, warm-up, game, role-play, discussion, project, presentation, pair-work, group-work

## Appendix E: Writing Genres (10)

academic-essay, argumentative, business-email, cause-effect, compare-contrast, cover-letter, descriptive, expository, narrative, process-analysis

## Appendix F: Writing Conventions (3)

citation-apa-mla, formatting, punctuation-advanced

## Appendix G: Writing Process Stages (5)

prewriting, drafting, revising, editing, peer-review

## Appendix H: Phonology Topics (7)

word_stress, sentence_stress_rhythm, segmentals_consonants, segmentals_vowels, connected_speech, intonation, l1_phonology_dutch


---

# Section 16: Solution Design — 5-Layer Data Routing Architecture

> **Status:** Designed and stress-tested (3 passes, 35+ scenarios)
> **Next:** Implementation (agent instructions update + tool improvements)

## 16.1 The Core Problem

The agent's current instructions.md handles only 3 extraction templates (grammar, L1, activities) with ~29 fields total. The enriched database has 9+ skill areas with ~135+ fields. The agent has no routing logic to determine which files to query based on a teacher's request.

## 16.2 Solution Overview: 5-Layer Architecture

```
Teacher Request (natural language)
    │
    ▼
┌─────────────────────────────────────────┐
│ LAYER 1: REQUEST CLASSIFIER             │
│ Classifies: topic_type, output_format,   │
│ L1, age, level, context                 │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ LAYER 2: FILE ROUTER                    │
│ Decides which YAML files to query       │
│ based on classification dimensions      │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ LAYER 3: FIELD EXTRACTOR                │
│ Extracts relevant fields from each file │
│ based on (file_type × output_type)      │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ LAYER 4: COMPOSITION ENGINE             │
│ Maps extracted fields to output sections │
│ (slide sequence, worksheet sections)     │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ LAYER 5: TASK BRIEF GENERATOR           │
│ Creates structured brief → sub-agents   │
└─────────────────────────────────────────┘
```

## 16.3 Layer 1: Request Classifier

### Dimensions Table

| Dimension | Values | Default | Detection Priority |
|-----------|--------|---------|-------------------|
| topic_type | grammar, vocabulary, speaking, listening, reading, phonology, writing | grammar | grammar_point > explicit_skill_name > topic_keyword |
| grammar_slug | e.g., present_simple, articles | auto-detect | Named grammar point |
| output_types | [slides], [worksheet], [activity], [flashcards], combinations | Varies by topic (see below) | Explicit > default |
| l1_languages | [spanish, portuguese, ...] | [] (must ask if not specified) | Language name match |
| age_group | children, teens, adults | adults | Explicit mention |
| level_range | A1-A2, B1-B2, C1 | from_topic file | Explicit mention |
| topic_context | general, travel, business, healthcare, academic | general | Context keywords |

### Classification Priority Rules

```
1. GRAMMAR POINT MATCH: If the request names a specific grammar point,
   topic_type = grammar regardless of other skill keywords.
   Example: "Speaking practice for present perfect" → grammar(present_perfect)

2. EXPLICIT SKILL NAME: If no grammar point found but request names
   listening, speaking, reading, or writing explicitly.
   Example: "Listening comprehension for B1" → listening

3. TOPIC KEYWORD: If no grammar point or skill name found, use keywords.
   Example: "pronunciation" → phonology, "vocabulary" → vocabulary
```

### Default Outputs Per Topic Type

| Topic Type | Default Output |
|------------|---------------|
| grammar | [slides] |
| vocabulary | [worksheet] |
| speaking | [activity] |
| listening | [activity] |
| reading | [worksheet] |
| phonology | [activity] |
| writing | [worksheet] |

## 16.4 Layer 2: File Router

### Primary File Selection

| Topic Type | Primary File Pattern | Example |
|-----------|---------------------|---------|
| grammar | `grammar/{slug}.yaml` | grammar/present_simple.yaml |
| vocabulary | `vocabulary/{slug}.yaml` | vocabulary/collocations_common.yaml |
| speaking | `speaking/{slug}.yaml` | speaking/speaking_functions.yaml |
| listening | `listening/{slug}.yaml` | listening/listening_strategies.yaml |
| reading | `reading/{slug}.yaml` | reading/reading_strategies.yaml |
| phonology | `phonology/{slug}.yaml` | phonology/word_stress.yaml |
| writing | `writing/{subdir}/{slug}.yaml` | writing/genres/argumentative.yaml |

### L1 File Routing (Topic-Dependent)

| Topic Type | L1 Source | How to Query |
|-----------|-----------|-------------|
| grammar | `l1-interference/{l1}_interference.yaml` | Use GetL1InterferenceTool |
| vocabulary | `vocabulary/*.yaml` → l1_interference field | Direct field in vocab file |
| speaking | `speaking/*.yaml` → l1_interference field | Direct field in speaking file |
| reading | `reading/*.yaml` → l1_interference field | Direct field in reading file |
| listening | **NO L1 DATA** | Skip L1 section silently |
| phonology | `phonology/l1_phonology_{l1}.yaml` | Only Dutch currently |
| writing | `writing/*/**.yaml` → differentiation.by_l1 | L1 adaptations in writing file |

### Activity Filtering

When output_types includes "activity":
```
Filter 218 activities (priority order):
  1. grammar_focus matches → topic slug (if grammar)
  2. skill_areas matches → topic_type (if vocabulary/speaking/etc.)
  3. bestForLevels overlaps → level_range
  4. bestForAges matches → age_group
  5. (Bonus) l1_enhanced[].language matches → l1_languages
Return top 3 best-matching activities.
```

### Skills Mapping (Full Lesson / Mixed)

When teacher says "full lesson", "all materials", or topic_type = mixed:
```
1. Query grammar/{slug}.yaml (primary)
2. Query skills_mapping/grammar_to_skills.yaml
   → Extract connected: listening.relevance, speaking.functions,
     reading.text_types, writing.genres
3. Route to secondary files based on connections
4. Filter activities by ALL connected skill_areas
```

## 16.5 Layer 3: Field Extraction Templates

### Grammar × Slides (16 fields)
core_meaning, contrast, timeline, ccqs[].question + answer + purpose, structure_affirm, structure_negative, structure_questions, sub_rules[].rule + examples, use[].context + description + examples, common_errors[].error + correction + explanation + l1_groups, phonetics[].note + l1_issue, teaching_tips (visual), register_notes, discourse_notes

### Grammar × Worksheet (8 fields)
core_meaning, contrast, structure_affirm/neg/questions, sub_rules[], common_errors[0:5]→Section A, common_errors[5:10]→Section B, use[].context→Section E, teaching_tips[0:3]

### Grammar × Activity (4 fields)
core_meaning, recommended_activities[].name+duration+notes, common_errors[0:3], teaching_tips (practice)

### L1 × Slides (4 field groups)
interference_patterns (frequency≥3, sorted DESC): pattern, wrong, correct, explanation, frequency. grammar_point.why_it_happens. teacher_tips.how_to_explain, exercises

### L1 × Worksheet (L1 fields + writing_interference)
Same as L1×Slides plus writing_interference[0:3].area + description + common_errors

### Vocabulary × Worksheet (9 fields)
definition, key_principles, sub_skills, word_lists, collocations, word_formation, common_difficulties, l1_interference, teaching_approach

### Vocabulary × Activity (4 fields)
word_lists[0:10], collocations[0:5], sub_skills, activities from vocab file

### Speaking × Activity (10 fields)
skill_name, sub_skills, key_principles, common_difficulties, l1_interference, pronunciation_focus, l1_profiles, teaching_approach, activities

### Listening × Activity (7 fields)
skill_name, sub_skills, key_principles, common_difficulties, phonological_features, teaching_approach, activities

### Reading × Activity + Worksheet (6 fields)
skill_name, sub_skills, key_principles, common_difficulties, l1_interference, teaching_approach, activities

### Phonology × Activity + Worksheet (6 fields)
definition, phonological_features[].feature+common_errors+teaching_techniques, key_principles, activities, assessment.methods, l1_specific_challenges

### Writing × Worksheet + Activity (14 fields)
topic, definition, what_it_is_not, genre.structure[].section+example+language_features, common_pitfalls[].pitfall+solution, grammar_focus, scaffolding, differentiation.by_l1, teaching_approach.stages, process_stages, ccqs, register_notes, essay_exam_strategies, key_principles

### Activities × Any (15 field groups per activity)
name, duration, groupSize, format, energyRequired, prepTime, bestForLevels, bestForAges, instructions, script, materials, setupInstructions, differentiation.support+extension, l1_enhanced, has*Component flags, digitalReady, requiresTech, teaching_tips

## 16.6 Layer 4: Composition Profiles

### grammar_standard (slides, 16-18 slides)
1. Lesson Plan Cover, 2. Hook (visual tip + image), 3. Meaning Overview, 4-7. CCQ Discovery (1 per CCQ), 5. Formula: Affirmative, 6. Formula: Negative, 7. Formula: Questions, 8. Sub-rules, 9. Practice: Gap-fill, 10. Practice: Error Correction, 11. Practice: L1 Drill, 12. Pronunciation (if phonetics exists), 13. L1 Oracle (1-2 per L1), 14. Use & Context, 15. Wrap-up, 16. Closing Brand

### grammar_worksheet
Reference Box → A. Gap-fill (5 items) → B. Error Correction (5 items) → C. L1 Drills (3-5 items) → D. Writing Task (1 prompt) → Answer Key

### vocabulary_worksheet
Reference Box → A. Word List → B. Formation/Collocation Practice → C. Error Correction (L1) → D. Contextual Use → E. Free Production

### speaking_activity
Overview → Setup → Instructions → Script → Language Focus → Pronunciation Notes → L1 Notes → Differentiation → L1 Adaptations

### writing_worksheet
Genre Reference → A. Genre Analysis → B. Common Pitfalls → C. Grammar Focus → D. Scaffolded Writing → E. Free Writing + L1 Adaptations

### skill_slides (non-grammar, 8-10 slides)
Each skill area has a dedicated 8-10 slide profile. See Section 16.2 in Pass 1 improvements for full sequences.

## 16.7 Layer 5: Task Brief Generator

The agent creates a structured brief with:
```json
{
  "metadata": { "topic_type", "grammar_slug", "output_types", "l1_languages", "age_group", "level_range" },
  "grammar_section": { "core_meaning", "contrast", "ccqs", "form", "sub_rules", "use", "common_errors", ... },
  "l1_section": { "language", "interference_patterns", "why_it_happens", "teacher_tips" },
  "vocabulary_section": { ... } | null,
  "speaking_section": { ... } | null,
  "writing_section": { ... } | null,
  "activities": [ ... ],
  "composition": { "slide_sections": [...], "worksheet_sections": [...] }
}
```
Null fields are omitted. Only activated sections appear.

## 16.8 Bugs Fixed vs Current Instructions

| Bug | Current | Fix |
|-----|---------|-----|
| why_it_happens location | Agent looks per-pattern (not found) | Extract from grammar_point level |
| register_notes | Not extracted | Add to extraction |
| discourse_notes | Not extracted | Add to extraction |
| dialectal_variation | Not extracted | Add to extraction |
| writing_interference | Not extracted | Add for worksheet requests |
| Activity filtering | Topic + age only | Full filter: level, skill_areas, grammar_focus, L1 |

## 16.9 Gaps vs Current Instructions

| Gap | Current | Needed |
|-----|---------|--------|
| 6 skill areas missing | Grammar-only | Templates for vocab, speaking, listening, reading, phonology, writing |
| Default output varies | [slides] for everything | Varies by topic type |
| L1 source routing | Always l1-interference/*.yaml | Topic-dependent L1 source |
| Activity filters | 7 basic fields | 15+ filterable fields |
| Skills mapping unused | Never queried | Route cross-skill requests |
| Composition profiles | Grammar slides only | Profiles for all 7 topics |

---

## 17. Stress Test Results

### Pass 1: 10 Standard Scenarios

| # | Scenario | Result | Issue Found |
|---|----------|--------|-------------|
| S1 | Slides for present simple, Spanish adults | ✅ | None |
| S2 | Worksheet present perfect, Portuguese, intermediate | ✅ | None |
| S3 | Speaking activity B1, job interviews | ✅ | None |
| S4 | Full lesson conditionals, Chinese teens | ⚠️ | Mixed topic needs skills_mapping |
| S5 | Vocabulary worksheet, academic, university | ✅ | None |
| S6 | Pronunciation word stress, Japanese | ❌→✅ | Classified as vocab; fixed phonology priority |
| S7 | Writing guide argumentative, B2 | ❌→✅ | "guide" triggered activity; fixed to worksheet |
| S8 | Listening comprehension, B1 | ❌→✅ | Defaulted to [slides]; fixed to [activity] |
| S9 | Articles, French, travel context | ❌→✅ | Classified as speaking; fixed grammar point priority |
| S10 | Reading comprehension, Arabic | ✅ | None |

### Pass 2: 15 Edge Cases

| # | Scenario | Result | Issue Found |
|---|----------|--------|-------------|
| E1 | Pronunciation + Japanese | ✅ | Uses phonology slides + L1 phonology |
| E2 | Articles for French beginners | ✅ | Grammar(articles) + French |
| E3 | Full lesson conditionals + Chinese | ✅ | grammar(primary) + skills_map routing |
| E4 | Academic vocabulary, no format | ✅ | Defaults to [worksheet] |
| E5 | Writing guide + Arabic | ✅ | writing + guide→worksheet |
| E6 | Listening for connected speech | ✅ | Listens first, phonology not triggered |
| E7 | Reading comprehension + Arabic | ✅ | Uses reading l1_interference field |
| E8 | Speaking for present perfect | ✅ | grammar primary, speaking cross-refers |
| E9 | Past simple, no L1 | ✅ | Agent must ask (preserved rule) |
| E10 | Passive voice + Italian, slides+worksheet | ✅ | Both outputs parsed |
| E11 | Vocabulary activity for collocations | ✅ | vocab + activity |
| E12 | "Need materials for my class" | ✅ | Handled by conversation flow |
| E13 | Present simple, Spanish + Portuguese | ✅ | Both L1s routed |
| E14 | Phrasal verbs, advanced, slides+activity | ✅ | Both outputs parsed |
| E15 | Connected speech worksheet | ✅ | phonology + worksheet |

### Pass 3: 15 Adversarial Scenarios

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| A1 | "Need materials for articles" | ✅ | grammar(articles) resolves ambiguity |
| A2 | "Slides for listening comprehension" | ✅ | listening+slides: unusual but valid |
| A3 | "past perfect continuous, Russian" | ✅ | grammar slug resolved correctly |
| A4 | "Speaking and writing for present perfect, B2" | ✅ | grammar primary + cross-ref |
| A5 | "Klingon speakers" | ⚠️ Flagged | Unknown L1: agent offers general materials |
| A6 | "Kids, Spanish, A1, speaking" | ✅ | All filters applied correctly |
| A7 | "Zero article + hotel + Japanese" | ✅ | All 7 dimensions parsed |
| A8 | "Just make SOMETHING" | ✅ | Conversation flow handles |
| A9 | "Video for present continuous" | ⚠️ Flagged | Unsupported output: agent offers alternatives |
| A10 | "Advanced present simple" | ⚠️ Flagged | CEFR mismatch: database wins |
| A11 | "30 Brazilian teens, second conditional, slides+worksheet, sports" | ✅ | All dimensions parsed |
| A12 | "Slides past simple + speaking activity" | ✅ | grammar primary, activity secondary |
| A13 | "Portuguese speakers" (only L1) | ✅ | Agent asks for rest |
| A14 | "Listening for Arabic" | ⚠️ No L1 data | Skip silently |
| A15 | "Inversion + negative adverbials, advanced" | ✅ | File exists in grammar/ |

**Total: 40 scenarios tested | 35 passed (87.5%) initially | 5 issues resolved in improvements**

---

## 18. Implementation Plan

### Phase 1: Instructions Update (instructions.md) — 3-4 hours

**Files:** `agent/instructions.md`

**Changes:**
1. Add Layer 1 classification rules to Part 2 (before Step 0)
2. Expand Step 1 from 1 extraction template → 9 templates (grammar slides, grammar worksheet, grammar activity, L1 slides, L1 worksheet, vocabulary, speaking, listening, reading, phonology, writing, activities)
3. Add L1 file routing rules (topic-dependent)
4. Add activity filtering rules (skill_areas, grammar_focus, bestForLevels, bestForAges, l1_enhanced)
5. Add composition profiles (slide sequences for all topic types)
6. Fix why_it_happens extraction path (grammar_point level, not per-pattern)
7. Add writing_interference extraction for worksheets
8. Add skills mapping query instructions for mixed/full-lesson requests

### Phase 2: Tool Updates — 2-3 hours

**Files:** `agent/tools/SearchGrammarTool.py`, `agent/tools/GetL1InterferenceTool.py`, `agent/tools/SearchActivitiesTool.py`

**Changes:**
1. `SearchGrammarTool` — Add ability to search by grammar_focus for cross-references
2. `GetL1InterferenceTool` — Return why_it_happens from grammar_point level
3. `SearchActivitiesTool` — Expand filter parameters: skill_areas, grammar_focus, bestForLevels, bestForAges, l1_enhanced

### Phase 3: New Search Tools — 3-4 hours

**New files:**
- `agent/tools/SearchVocabularyTool.py`
- `agent/tools/SearchSpeakingTool.py`
- `agent/tools/SearchListeningTool.py`
- `agent/tools/SearchReadingTool.py`
- `agent/tools/SearchPhonologyTool.py`
- `agent/tools/SearchWritingTool.py`
- `agent/tools/SearchSkillsMappingTool.py`

Each follows the same pattern as SearchGrammarTool but for its skill area. Registered in `cogniesl_agent.py`.

### Phase 4: Composition Engine (Optional) — 4-6 hours

**New files:** `agent/composition_profiles.py`, `agent/brief_generator.py`

Replaces hardcoded slide sequences in instructions.md with structured profiles. Can be deferred.

### Dependencies

```
Phase 1 ──> must be done first (core logic)
Phase 2 ──> can be done in parallel with Phase 1
Phase 3 ──> depends on Phase 2 (tools must work together)
Phase 4 ──> standalone, can be deferred
```

### Testing After Implementation

1. Run all 40 scenarios from Pass 1-3 against the updated agent
2. Verify SearchGrammarTool still works for existing grammar lookups
3. Verify activity filtering matches correct activities
4. Verify why_it_happens now returns correctly from grammar_point level
5. Do a full end-to-end generation test

---

## Appendix I: Normalization Map (Different Names, Same Concept)

| Concept | Grammar | L1 | Vocab/Speak/Read | Activity | Writing |
|---------|---------|-----|-----------------|----------|---------|
| Student errors | common_errors | interference_patterns | common_difficulties | — | common_pitfalls |
| Teaching method | teaching.tips | teacher_tips | teaching_approach | teaching_tips | teaching_tips |
| Level | level (A1) | — | cefr_range | bestForLevels | level_range |
| Age | — | — | — | bestForAges | — |
| Activities | recommended_activities | exercises | activities[] | N/A | recommended_activities |
| L1 connection | l1_groups in errors | N/A | l1_interference | l1_enhanced | differentiation.by_l1 |
| Support | — | — | — | differentiation.support | scaffolding |
| Extension | — | — | — | differentiation.extension | scaffolding.for_advanced |
| Grammar link | N/A | grammar_points key | — | grammar_focus | grammar_focus |

## Appendix J: L1 Language Codes

| Language | Code | Language | Code | Language | Code |
|----------|------|----------|------|----------|------|
| Arabic | ar | Indonesian | id | Romanian | ro |
| Bengali | bn | Italian | it | Russian | ru |
| Czech | cs | Japanese | ja | Somali | so |
| Danish | da | Korean | ko | Spanish | es |
| Dholuo | luo | Mandarin | zh | Swahili | sw |
| Dutch | nl | Norwegian | no | Swedish | sv |
| Finnish | fi | Persian | fa | Tagalog | tl |
| French | fr | Polish | pl | Tamil | ta |
| German | de | Portuguese | pt | Thai | th |
| Greek | el | Haitian Creole | ht | Turkish | tr |
| Hebrew | he | Hungarian | hu | Urdu | ur |
| Hindi | hi | | | Vietnamese | vi |

## Appendix K: Activity Filtering Quick Reference

When filtering 218 activities, use these fields in this priority order:

1. `grammar_focus` — matches grammar slug (for grammar topics)
2. `skill_areas` — matches topic_type (for vocab/speaking/etc.)
3. `bestForLevels` — overlap with level_range
4. `bestForAges` — matches age_group
5. `l1_enhanced[].language` — bonus match for L1 adaptations
6. `duration` — prefer activities within reasonable time
7. `prepTime` — prefer low-prep unless teacher specifies

Top 3 results in Content Brief. Agent presents as clickable choices.

---

# Section 19: Critical Analysis — Flaws, Improvements & Simplifications

> **Status:** Self-audit of the 5-layer architecture design
> **Purpose:** Identify weaknesses before implementation

## 19.1 Critical Flaw: Instruction Bloat

**Problem:** The 5-layer design adds 7 extraction templates, 7 composition profiles, routing rules, and field lists to instructions.md. Current instructions are 1,349 lines. The expanded version would be 3,000+ lines. The agent cannot reliably remember and apply 3,000 lines of instructions across a multi-turn conversation.

**Severity:** CRITICAL — without fixing this, the design is not implementable.

**Solution:** Move routing logic from instructions into tools. Create `ClassifyRequestTool` and `RouteAndExtractTool` that handle classification and extraction deterministically. The agent only needs to call the tools and copy the structured results.

## 19.2 Critical Flaw: Single Point of Failure in Classification

**Problem:** If the agent misclassifies the teacher's request, the entire generation goes wrong. Wrong files queried, wrong fields extracted, wrong output structure. The 3-pass stress test showed ~90% accuracy, but 10% failures on edge cases is too high for a production system.

**Severity:** CRITICAL

**Solution:** Move classification from agent reasoning (LLM-dependent) to a deterministic tool (code-dependent). A `ClassifyRequestTool` uses keyword matching, the grammar slug list, and L1 name lookup. It never hallucinates.

## 19.3 Critical Flaw: Agent Overload

**Problem:** The current design asks the agent to simultaneously be:
1. A conversationalist (warm, natural tone with teacher)
2. A classifier (determine topic, output, L1, age, level from text)
3. A file router (know which YAML files to query)
4. A data engineer (manually extract and copy-paste fields)
5. A quality controller (validate the Content Brief)
6. A project manager (oversee sub-agent generation)

These roles compete for the agent's attention. A conversational agent optimizes for natural language, not for precise data routing.

**Severity:** HIGH

**Solution:** Tools handle roles 2-4 (classification, routing, extraction). The agent focuses on roles 1, 5, and 6 (conversation, quality, oversight).

## 19.4 High-Severity Flaw: Free-Text Task Briefs

**Problem:** The sub-agents (planner + HTML writer) receive free-text task_briefs that the main agent writes manually. If the main agent writes "Create a CCQ slide about articles" instead of including the exact CCQ question and answer, the sub-agent hallucinates generic content.

**Severity:** HIGH

**Solution:** Use structured task_brief objects with typed fields. The `RouteAndExtractTool` returns structured data. The main agent passes this structured data (not re-written prose) to the sub-agents. The HTML writer receives typed fields it can't misinterpret.

## 19.5 Medium-Severity Flaws

### Flaw 5: 9 Extraction Templates = 9 Things to Forget
**Problem:** 9 templates × 4-16 fields each = ~90 field references. The agent must remember which template to use and extract every field.
**Solution:** One template per file type (7 total, not 21+). Extract ALL fields from the primary file. Planner sub-agent decides what to use.

### Flaw 6: Rigid Composition Profiles
**Problem:** Hardcoded "16-18 slides for grammar" doesn't work for all topics. Articles needs fewer slides than conditionals.
**Solution:** Adaptive composition based on available data. Planner sub-agent includes/excludes sections based on what fields exist.

### Flaw 7: Sub-Agents Can't Access Database
**Problem:** HTML writer can't verify or look up data. If the brief is missing a field, the sub-agent hallucinates.
**Solution:** Give sub-agents a read-only ReadFile tool, or pass the extracted YAML as a structured context object.

### Flaw 8: Skills Mapping Is Grammar-Only
**Problem:** grammar_to_skills.yaml exists but no vocabulary_to_skills or speaking_to_writing.
**Solution:** Either add more mapping files or make cross-referencing generic (any topic type → any skill type).

## 19.6 The Simplified Architecture

```
                    ┌─────────────────────────┐
                    │   ClassifyRequestTool    │  ← NEW: deterministic
                    │  (code, not LLM)         │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   RouteAndExtractTool    │  ← NEW: does the heavy lifting
                    │  (queries files, returns │
                    │   structured data)       │
                    └──────────┬──────────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
    ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
    │ Grammar data   │ │ L1 data      │ │ Activities     │
    │ (structured)   │ │ (structured) │ │ (structured)   │
    └────────────────┘ └──────────────┘ └────────────────┘
             │                 │                  │
             └─────────────────┼──────────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   Main Agent            │
                    │  (conversation + brief   │
                    │   + quality check)       │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   Planner Sub-agent     │
                    │  (adaptive composition) │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   HTML Writer Sub-agent │
                    │  (structured data in,   │
                    │   typed slides out)     │
                    └─────────────────────────┘
```

## 19.7 Instructions.md Size Comparison

| Version | Lines | Content |
|---------|-------|---------|
| Current | 1,349 | 3 extraction templates + conversation + generation |
| Original 5-layer plan | ~3,000 | 9 extraction templates + 7 profiles + routing + field lists |
| **Simplified (proposed)** | **~600** | **Conversation + 7 file references + edge cases + validation** |

The simplified version removes:
- All 9 extraction templates (tools return data)
- All 7 composition profiles (planner adapts)
- All routing rules (tools decide)
- All field lists (tools know schemas)

And keeps:
- Conversation flow (unchanged)
- Content Brief format (expanded for all skills)
- Generation pipeline (expanded for all file types)
- How to call the 2 new tools (short reference)
- Edge case handling (new)
- Quality checklist (expanded)

## 19.8 What The Agent Actually Needs To Know

After the simplification, the agent only needs to:

1. Call `ClassifyRequestTool(teacher_message)` → gets dimensions
2. If L1 is missing, ask for it (existing rule)
3. Call `RouteAndExtractTool(classification)` → gets all data
4. Show Content Brief using the data (existing format, expanded)
5. On approval, pass structured data to planner sub-agent
6. Validate output quality (expanded checklist)

That's it. 6 steps. No memorizing field names. No guessing which template.

## 19.9 Is The Use Logic Sound?

**Yes.** The fundamental logic is validated:

1. ✅ Teacher describes needs → classified into dimensions
2. ✅ Dimensions route to correct files → data extracted
3. ✅ Data shown to teacher → Content Brief for approval
4. ✅ Teacher approves → materials generated
5. ✅ Sub-agents create output → teacher receives materials

The logic doesn't change. What changes is WHO does the mechanical work:
- **Before:** LLM agent does everything from memory
- **After:** Tools handle mechanics, agent handles conversation + quality

## 19.10 Remaining Questions Before Implementation

1. **Tool implementation:** Should `RouteAndExtractTool` be one tool or multiple? 
   → One tool is simpler. It takes the classification and returns everything.

2. **Structured briefs:** How does the planner sub-agent receive structured data?
   → The main agent puts a JSON object in the task_brief field. Sub-agent parses it.

3. **Backward compatibility:** Will existing generation still work after changes?
   → Yes. Grammar extraction returns the same fields as before. Other types are additive.

4. **Tool code location:** Where do the new tools live?
   → `agent/tools/ClassifyRequestTool.py` and `agent/tools/RouteAndExtractTool.py`

5. **Testing strategy:** How to validate before deploying to production?
   → Run all 40 stress test scenarios. Verify each returns correct routing.


---

## Section 20: Final Design — After 5 Improvement Iterations

> **Status:** FINAL — ready for review
> **Process:** 3 stress test passes (40 scenarios) + 5 improvement iterations
> **Key insight:** Move routing from agent instructions to deterministic tools

### 20.1 What Changed Through 5 Iterations

| Iteration | Focus | Improvement |
|-----------|-------|-------------|
| 1 | Tool architecture | 1 `PrepareGenerationTool` replaces 2 separate tools + agent routing |
| 2 | Data contracts | Structured JSON prevents sub-agent hallucination (typed fields) |
| 3 | Token optimization | Only load relevant data: ~8KB from L1 file (not 1.2MB), 3 filtered activities |
| 4 | Error recovery | 7 failure modes with 4-level recovery (silent → degrade → retry → escalate) |
| 5 | Final polish | New instructions outline (~550 lines), adaptive planner, expanded Content Brief |

### 20.2 Final Architecture

```
Teacher: "Slides for present simple, Spanish adults"
    │
    ▼
┌──────────────────────────────────────┐
│ PrepareGenerationTool (CODE)          │  ← NEW: deterministic, 100% accurate
│ 1. Classifies request                │
│ 2. Routes to correct YAML files       │
│ 3. Extracts only relevant fields     │  ← ~9K tokens, not 1.2MB
│ 4. Returns structured JSON           │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ Main Agent (LLM)                     │  ← simplified: ~550 line instructions
│ 1. Presents Content Brief            │
│ 2. Gets teacher approval             │
│ 3. Passes structured JSON to planner │
│ 4. Validates output quality          │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ Planner Sub-agent                    │  ← adaptive: checks data_quality
│ Decides WHICH slides to include      │  includes/excludes sections dynamically
│ based on available data              │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ HTML Writer Sub-agent                │  ← receives typed JSON fields
│ Creates HTML from structured data    │  cannot hallucinate field values
└──────────────────────────────────────┘
```

### 20.3 Files That Change

| File | Change | Lines |
|------|--------|-------|
| `agent/tools/PrepareGenerationTool.py` | **NEW** — classification + routing + extraction | ~300 |
| `agent/tools/SearchActivitiesTool.py` | Expanded filtering (skill_areas, grammar_focus, l1_enhanced) | +50 |
| `agent/tools/GetL1InterferenceTool.py` | Fix why_it_happens return (grammar_point level) | +10 |
| `agent/instructions.md` | Simplified: 1,349→550 lines | -799 |
| `agent/cogniesl_agent.py` | Register new tool | +3 |
| `agent/slides_tools/InsertNewSlides.py` | Planner instructions: adaptive composition | +30 |
| `agent/slides_tools/html_writer_instructions.md` | Document structured JSON format | +20 |

### 20.4 Implementation Order (Updated)

```
Day 1:  PrepareGenerationTool.py (~4 hours)
          → classification logic
          → file routing
          → smart extraction (L1 slicing, activity filtering)
          → data quality checks
          → token optimization

Day 2:  Instructions.md rewrite (~3 hours)
          → new Parts 2, 2B, 4
          → expanded Content Brief (7 skill formats)
          → edge case handling

Day 3:  Tool updates + planner updates (~3 hours)
          → SearchActivitiesTool filtering
          → GetL1InterferenceTool why_it_happens fix
          → planner adaptive composition
          → HTML writer structured JSON format

Day 4:  Testing (~3 hours)
          → Run all 40 stress test scenarios
          → Test each failure mode (7 modes)
          → End-to-end generation test
          → Backward compatibility check

Total: ~13 hours
```


---

## Section 21: CogniELA Integration — Domain-Aware Routing

> **Source:** `CogniELA/Docs/product-vision-2026-05-29.md` (updated)
> **Status:** Design integration — ready for implementation

### 21.1 Domain Model

The Forge now supports two domains under `forge/data/`:

```
forge/data/
  esl/                          # CogniESL — Teaching non-native speakers
    grammar/                    300 files (CEFR levels A1-C2)
    l1-interference/             36 files (30+ languages)
    activities/                 218 files
    writing/                     18 files (needs field migration)
    reading/                      4 files
    listening/                    5 files
    speaking/                     6 files
    phonology/                    7 files
    vocabulary/                   5 files
    skills_mapping/               2 files

  ela/                          # CogniELA — Teaching native speakers (NEW)
    literary-devices/            # Genre-agnostic, applies across poetry/prose/drama
      figurative-language/      # ~15 devices
      sound-devices/             # ~10 devices
      narrative-structure/       # ~15 devices
      characterization/          # ~12 devices
      theme/                     # ~12+ devices
      symbolism/                 # ~10+ devices
      tone-and-mood/             # ~10+ concepts
      irony/                     # 4 types
      satire/                    # 8 concepts
    poetry/                      # Poetry-specific only
      meter-and-rhythm/          
      rhyme-scheme/              
      stanza-forms/              
      poetic-forms/              
      sound-and-structure/       
    drama/                       # Drama-specific only
      dramatic-elements/         
      plot-structure/            
      theatrical-devices/        
    rhetoric/                    # NEW category
      rhetorical-appeals/        
      rhetorical-devices/        
      rhetorical-situation/      
    writing/                     # ELA writing
      argumentative/             
      informative-explanatory/   
      narrative/                 
      literary-analysis/         
      research/                  
      process/                   
      paragraph-development/     
      thesis-statements/         
      author-craft/              
    grammar-for-writers/         # Retargeted from ESL grammar
      sentences/                 
      usage/                     
      punctuation/               
      style/                     
    reading/                     # ELA reading
      close-reading/             
      text-dependent-questions/  
      text-structures/           
      genres/                    
      author-purpose/            
      vocabulary/                
    speaking-listening/          # Renamed from speaking/
      socratic-seminar/          
      presentation/              
      collaboration/             
      debate/                    
      academic-listening/        
    media-literacy/              
      advertising/               
      news-literacy/             
      digital-media/             
      propaganda/                
    film-visual-literacy/        # NEW
      cinematography/            
      editing/                   
      sound-design/              
      visual-analysis/           
    research-inquiry/            
      source-evaluation/         
      note-taking/               
      citation/                  
      information-synthesis/     
    activities/                  # ELA activities
      analysis/                  
      writing/                   
      discussion/                
      games/                     
      vocabulary/                
    standards/                   
      common-core/               # CCSS by strand and grade
    skills-mapping/              # Cross-reference: standards to files
```

### 21.2 Field Normalization (Across Both Domains)

From the product vision, section 4.9. These are the UNIFIED field names:

| Unified Field | ESL Grammar | ESL Writing (current) | ELA Literary Device | Action Needed |
|--------------|-------------|---------------------|-------------------|--------------|
| `common_errors` | ✅ Already correct | ❌ `common_pitfalls` → RENAME | ✅ Already correct | Migrate 18 ESL writing files |
| `teaching` | ✅ Already correct | ❌ `teaching_approach` + `teaching_tips` → MERGE | ✅ Already correct | Migrate 18 ESL writing files |
| `citations` | ✅ | ✅ | ✅ | None |
| `sources` | ✅ | ✅ | ✅ | None |
| `ccqs` | ✅ in meaning | ✅ top-level | ✅ in meaning | None |
| `register_notes` | ✅ | ✅ | ✅ | None |
| `discourse_notes` | ✅ | ❌ Missing | ✅ | Add to ESL writing schemas |

### 21.3 Domain-Specific Fields (No Normalization Needed)

| Field | Domain | Purpose |
|-------|--------|---------|
| `level` (CEFR: A1-C2) | ESL | Second language proficiency |
| `grade_band` ("6-8", "9-10", "11-12") | ELA | US grade level |
| `grammar_point` | ESL + ELA grammar | Slug for grammar concept |
| `device` | ELA literary devices | Slug for literary device |
| `l1_groups` in `common_errors` | ESL | Language groups affected by interference |
| `phonetics` | ESL | Pronunciation guidance |
| `dialectal_variation` | ESL | Regional dialect differences |
| `form: {affirmative, negative, question}` | ESL | Three-form grammar presentation |
| `structure` (single form) | ELA grammar-for-writers | How the rule works |
| `sub_types` | ELA | Variations of a literary device |
| `functions` | ELA | What the device achieves in text |
| `examples_from_literature` | ELA | Real literature examples |
| `bestForLevels` [CEFR] | ESL activities | Target proficiency levels |
| `bestForGrades` [US grades] | ELA activities | Target grade levels |
| `common_core_alignment` | ELA | CCSS standard references |

### 21.4 Domain-Aware Routing Logic

The `PrepareGenerationTool` now checks the domain path first:

```
Teacher: "I need slides for metaphor, 9th grade"

STEP 1: CLASSIFY
  domain:       ela
  topic_type:   literary-device
  specific_topic: metaphor
  output_types: [slides]
  grade_band:   "9-10"
  age_group:    teens

STEP 2: ROUTE TO FILE
  Path: ela/literary-devices/figurative-language/metaphor.yaml
  (or closest match)

STEP 3: SELECT EXTRACTION TEMPLATE
  Match: domain=ela + topic_type=literary-device
  Template: ELA_LITERARY_DEVICE_EXTRACTION
  Fields: title, device, grade_band, meaning, structure, sub_types,
          functions, examples_from_literature, common_errors, teaching

STEP 4: APPLY COMPOSITION PROFILE
  No L1 Oracle (native speakers)
  No pronunciation (unless phonetics exists, which it won't for ELA)
  Adaptive: if sub_types exist → sub-type slides
            if examples_from_literature exist → analysis slides
            if functions exist → function-of-device slides

STEP 5: GENERATE
  Slide sequence: Title → Definition → How it works → Sub-types →
                  Examples from lit → Analysis → Practice → Wrap-up → Closing
```

### 21.5 Extraction Templates for ELA

**ELA Literary Device × Slides:**
```
title, device, grade_band
meaning.core_meaning, meaning.contrast
meaning.ccqs[].question + answer + purpose
structure.{component}.description + examples
sub_types[].type + description + examples
functions[].function_name + description
examples_from_literature[].text + source + analysis
common_errors[].misconception + explanation + correction
teaching.methodology + tips + recommended_activities
```

**ELA Grammar-for-Writers × Slides:**
```
title, grammar_point, grade_band
meaning.core_meaning, meaning.contrast
meaning.ccqs[].question + answer + purpose
form.structure + example_generator
common_errors[].error + example_wrong + example_correct + explanation
teaching.methodology + tips + recommended_activities
```

**ELA Writing × Worksheet:**
```
title, topic, grade_band, skill_area
definition, what_it_is_not
key_principles[].principle + explanation
ccqs[].question + answer + purpose
scaffolding[].strategy + texts
assessment.formative + summative
common_errors[].error + example_wrong + example_correct + explanation
differentiation.support + extension
```

### 21.6 Adaptive Slide Composition (Domain-Aware)

The planner sub-agent checks `data_quality` to decide slide structure:

| Block | ESL Grammar | ELA Literary Device | ELA Grammar-for-Writers |
|-------|------------|-------------------|------------------------|
| Title | ✅ Always | ✅ Always | ✅ Always |
| Hook | ✅ If teaching_tips exist | ❌ (no visual context) | ❌ |
| Meaning | ✅ Always | ✅ Always | ✅ Always |
| CCQs | ✅ If ccqs exist | ✅ If ccqs exist | ✅ If ccqs exist |
| Formulas | ✅ If form exists | ❌ (uses structure) | ✅ If form exists |
| Structure | ❌ | ✅ If structure exists | ❌ |
| Sub-types | ❌ | ✅ If sub_types exist | ❌ |
| Sub-rules | ✅ If sub_rules exist | ❌ | ❌ |
| Functions | ❌ | ✅ If functions exist | ❌ |
| Practice | ✅ If common_errors exist | ✅ If examples exist | ✅ If common_errors exist |
| Pronunciation | ✅ If phonetics exists | ❌ | ❌ |
| L1 Oracle | ✅ If l1 data exists | ❌ | ❌ |
| Lit Examples | ❌ | ✅ If examples_from_lit exist | ❌ |
| Wrap-up | ✅ Always | ✅ Always | ✅ Always |
| Closing | ✅ Always | ✅ Always | ✅ Always |


---

## Section 22: Cross-Domain Data Access

> **Status:** RESOLVED — See `ARCHITECTURE_DECISION.md` in the CogniELA docs
> **Resolution:** The two-database approach (esl/ and ela/ directories) has been replaced with a unified Forge architecture. Content is organized into shared/, esl-only/, and ela-only/ directories. The agent infers domain from context (L1 mention → ESL, grade band → ELA) and applies a presentation profile (esl or ela) when generating materials. Cross-domain access is handled natively — shared files serve both domains. Section 22's original concern about "rigid domain walls" is resolved by eliminating the walls entirely.

### 22.1 Original Concern (Preserved for Reference)

ESL and ELA data should not be walled off from each other. Some ELA content (metaphor, rhetorical appeals, thesis statements) is useful for advanced ESL students. Some ESL content (verb tense consistency, sentence combining, subject-verb agreement) is useful for native speakers.

If the router strictly checks `esl/` for ESL teachers and `ela/` for ELA teachers:

| Teacher Request | Domain Check | Result |
|----------------|-------------|--------|
| ESL teacher asks for "metaphor" | Check `esl/` → not found | ❌ "Not available" |
| ELA teacher asks for "sentence combining" | Check `ela/` → not in ELA literary devices | ❌ "Not available" |
| ESL teacher asks for "thesis statements" | Check `esl/` → not in ESL grammar | ❌ "Not available" |

This is a bad experience. The data exists, just in the other domain.

### 22.2 Proposed Solution: Cross-Domain Fallback

The `PrepareGenerationTool` checks its primary domain first, then falls back:

```
Routing logic (updated):

1. Check primary domain: {domain}/{topic_type}/{slug}.yaml
2. IF found → return with domain tag + cross_domain: false
3. IF not found → check secondary domain: {other_domain}/{...}.yaml
4. IF found in secondary domain → return with cross_domain: true
5. IF not found in either → return closest_matches[]
```

**Example: ESL teacher asks for metaphor**
```
1. Check: esl/grammar/metaphor.yaml → NOT FOUND
2. Fallback: ela/literary-devices/figurative-language/metaphor.yaml → FOUND ✅
3. Return: { domain: "ela", cross_domain: true, data: {...} }
```

**Example: ELA teacher asks for sentence combining**
```
1. Check: ela/grammar-for-writers/sentences/sentence-combining.yaml → NOT FOUND yet
2. Fallback: esl/grammar/sentence_combining.yaml → FOUND ✅
3. Return: { domain: "esl", cross_domain: true, data: {...} }
```

### 22.3 Presentation Adjustment for Cross-Domain Content

When `cross_domain: true`, the planner and writer adjust:

| Adjustment | ESL teacher accessing ELA content | ELA teacher accessing ESL content |
|-----------|----------------------------------|----------------------------------|
| Language level | Simplify vocabulary, add glossaries | Use, don't simplify |
| Grade/Level | Map grade_band → CEFR level | Map CEFR level → grade_band |
| Examples | Replace literature quotes with simpler contexts | Keep literature quotes |
| L1 content | Add L1 notes if available from ESL files | N/A — skip L1 |
| CCQs | Use ESL-appropriate CCQs | Use ELA-appropriate CCQs |
| Terminology | Define literary terms | Use literary terms naturally |

**Content Brief note for cross-domain:**
> "I found 'Metaphor' in our ELA literary analysis database. This isn't typically an ESL topic, but it's excellent for advanced students. I'll adjust the examples for B2 level and include vocabulary support. Would you like me to proceed with this?"

### 22.4 Open Questions

1. **Should cross-domain be automatic or opt-in?**
   - Automatic: always search both domains, show what's found
   - Opt-in: agent asks "I found this in the ELA database. Want to use it?"
   - Trade-off: automatic is seamless, opt-in respects domain boundaries

2. **What if both domains have the same topic?**
   - ESL version (simpler) vs ELA version (deeper analysis)
   - Teacher's domain should win, but offer the other version as alternative
   - Example: "comma splices" exists in both ESL grammar and ELA grammar-for-writers

3. **Should there be a domain conversion map?**
   - `grade_band "9-10"` → `CEFR B2-C1` (for ESL teachers accessing ELA)
   - `CEFR B2` → `grade_band "9-10"` (for ELA teachers accessing ESL)
   - This enables automatic level/grade adjustment in the Content Brief

4. **How to handle activities cross-domain?**
   - ELA teacher might want ESL grammar drills for "comma splices"
   - ESL teacher might want ELA Socratic seminars for advanced speaking
   - Activities have `domain` field — should we filter or show all?

5. **Should the teacher be able to choose their domain?**
   - Explicit domain selection at start: "Are you teaching ESL or ELA?"
   - This would help the classifier and avoid misrouting
   - But adds friction to the first interaction

### 22.5 Section 22 Status

This section documents an open design discussion. The cross-domain fallback is not yet implemented. It should be revisited after Phase 1-3 are complete and the single-domain routing is stable.
