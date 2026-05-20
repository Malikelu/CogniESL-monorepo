# CogniESL — Data Format Specification

> YAML data file schemas for grammar points, L1 interference patterns, and activities.

---

## 1. Grammar Points (`data/grammar/`)

Each file describes one English grammar point. File naming: `{slug}.yaml` (e.g., `present_simple.yaml`, `a_an_the.yaml`).

### Schema

```yaml
grammar_point: string          # Unique slug (e.g., "present_simple")
title: string                  # Human-readable name (e.g., "Present Simple")
description: string            # Brief description of the grammar point
level: string                  # CEFR level (A1, A2, B1, B2, C1, C2) — for internal use only
sources:                       # Academic references (optional)
  primary: string
  secondary: string
  validation: string
  pedagogical: string
  teaching_practice: string
meaning:
  core_meaning: string         # What this grammar point means
  timeline: string             # Visual timeline explanation (optional)
  contrast: string             # How to distinguish from similar grammar (optional)
  ccqs:                        # Concept Check Questions
    - question: string
      answer: string
  example_generator:
    contexts: [string]         # Example contexts (e.g., "daily routines")
    cultural_notes: [string]   # Cultural sensitivity notes
    min_examples: int
form:
  affirmative:
    structure: string          # Formation rule (e.g., "Subject + base verb + s/es")
    example_generator: [string] # Example sentences
    min_examples: int
  negative:
    structure: string
    example_generator: [string]
    min_examples: int
  questions:
    structure: string
    example_generator: [string]
    min_examples: int
sub_rules:                     # Spelling rules, irregulars, etc.
  - rule: string               # Rule name (e.g., "Third person singular spelling: add -s")
    type: string               # "spelling", "irregular", "exception"
    examples: [string]         # e.g., "work → works"
phonetics:                     # Pronunciation notes (optional)
  contractions: [string]       # e.g., "I'm, You're"
  notes: string
common_errors:                 # Known mistakes (optional)
  - error: string
    correction: string
    l1_specific: string        # Which L1 causes this (optional)
discourse_notes: string        # Real-world usage contexts (optional)
teaching:
  methodology: string          # e.g., "PPP" (Presentation, Practice, Production)
  tips: [string]               # Teacher guidance
  recommended_activities: [string]  # Activity names
register_notes: string         # Formal/informal usage (optional)
dialectal_variation: string    # BrE/AmE differences (optional)
```

### Example: `present_simple.yaml` (abbreviated)

```yaml
grammar_point: present_simple
title: Present Simple
description: Used for habits, routines, general truths, permanent situations...
level: A1
meaning:
  core_meaning: Describes actions that happen regularly (habits)...
  ccqs:
    - question: Is this happening right now, at this exact moment?
      answer: No — it happens regularly or is always true.
form:
  affirmative:
    structure: I/you/we/they + base verb (V1) / He/she/it + base verb + s/es
    example_generator:
      - I walk to school.
      - She walks to school.
sub_rules:
  - rule: "Third person singular spelling: add -s"
    type: spelling
    examples:
      - work → works
      - play → plays
  - rule: "Verbs ending in -s, -sh, -ch, -x, -o: add -es"
    type: spelling
    examples:
      - watch → watches
      - go → goes
```

### Key Fields for Material Generation

The agent extracts these specific fields when generating materials:

| Field | Used For |
|-------|----------|
| `meaning.core_meaning` | Slide content, worksheet instructions |
| `meaning.ccqs` | Concept Check Questions on slides |
| `form.*.structure` | Visual equations on slides |
| `form.*.example_generator` | Example sentences in materials |
| `sub_rules` | Dedicated slides for each rule |
| `phonetics` | Pronunciation guide slides |
| `common_errors` | Error correction exercises |
| `teaching.tips` | Speaker notes for teachers |
| `teaching.recommended_activities` | Activity selection |

---

## 2. L1 Interference (`data/l1-interference/`)

Each file contains interference patterns for one language across multiple grammar points. File naming: `{language}_interference.yaml` (e.g., `portuguese_interference.yaml`).

### Schema

```yaml
language: string               # Language name (e.g., "portuguese")
grammar_points:
  {grammar_point_slug}:        # Matches grammar_point field from grammar files
    interference_patterns:
      - pattern: string        # Error description
        example_portuguese: string  # Sentence in L1 (or L1-influenced English)
        example_gloss: string       # Word-by-word gloss
        example_wrong: string       # Incorrect English
        example_correct: string     # Correct English
        explanation: string         # Why the error happens
        frequency: int              # 1-5 scale (5 = very common)
        persistence: int            # 1-5 scale (5 = hard to eliminate)
        communicative_impact: int   # 1-5 scale (5 = severely impedes communication)
    examples:                       # Wrong → Correct pairs
      - string                      # e.g., "Wrong: 'I want the red.' Correct: 'I want the red one.'"
    why_it_happens: string          # Linguistic explanation
    teacher_tips:
      how_to_explain: string        # Pedagogical guidance
      where_to_start: string        # Teaching sequence start point
      sequencing: string            # Multi-week teaching plan
      exercises:
        - name: string              # Exercise name
          type: string              # Exercise type (fill-in-the-blank, matching, etc.)
          description: string       # What students do
          duration: int             # Minutes
    sources: [string]               # Academic references
```

### Example: `portuguese_interference.yaml` (abbreviated)

```yaml
language: portuguese
grammar_points:
  adjectives_without_nouns:
    interference_patterns:
      - pattern: Omission of 'one/ones' after adjectives
        example_portuguese: Eu quero o vermelho.
        example_gloss: I want the red.
        example_wrong: I want the red.
        example_correct: I want the red one.
        explanation: Portuguese allows adjectives to stand alone as nouns with an article...
        frequency: 4
        persistence: 3
        communicative_impact: 2
    examples:
      - "Wrong: 'I want the red.' Correct: 'I want the red one.'"
      - "Wrong: 'Which do you prefer? The big.' Correct: 'The big one.'"
    why_it_happens: "Portuguese allows adjectives to function as nouns..."
    teacher_tips:
      how_to_explain: "Write 'o vermelho' on the board. Ask: 'The red what? We need a word: ONE.'"
      where_to_start: "Begin with concrete objects. Hold up two pens: 'I want the blue one.'"
      sequencing: "Week 1: 'one' after adjectives (singular). Week 2: 'ones' (plural)..."
      exercises:
        - name: One Ones Insertion
          type: fill-in-the-blank
          description: Provide 15 sentences where students must insert 'one' or 'ones'...
          duration: 15
    sources:
      - "Swan, M. & Smith, B. (2001). Learner English (2nd ed.). Cambridge."
```

### Available Languages (34)

The `data/l1-interference/` directory contains files for: Arabic, Bengali, Czech, Danish, Dutch, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Mandarin, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Spanish, Swedish, Tagalog, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and others.

### Key Fields for Material Generation

| Field | Used For |
|-------|----------|
| `interference_patterns` | L1 Oracle slides, error correction exercises |
| `examples` | Wrong → Correct examples on slides/worksheets |
| `why_it_happens` | Teacher explanation in speaker notes |
| `teacher_tips.how_to_explain` | Teacher guidance |
| `teacher_tips.exercises` | Worksheet exercises |
| `frequency`, `persistence` | Prioritization (high scores = more prominent in materials) |

---

## 3. Activities (`data/activities/`)

Each file describes one classroom activity. File naming: `{slug}.yaml` (e.g., `3-2-1-exit.yaml`).

### Schema

```yaml
id: string                     # Unique slug (e.g., "3-2-1-exit")
name: string                   # Activity name (e.g., "3-2-1 Exit Ticket")
category: string               # Activity category (e.g., "review", "warm-up", "practice")
description: string            # Brief description
targetStructures: [string]     # Grammar structures this activity practices
bestForLevels: [string]        # CEFR levels (A1, A2, B1, B2, C1, C2)
duration: int                  # Duration in minutes
groupSize: string              # "individuals", "pairs", "small groups", "whole class"
energyRequired: string         # "low", "medium", "high"
prepTime: string               # "none", "minimal", "moderate", "extensive"
materials: [string]            # Required materials
format: [string]               # "in-person", "online"
requiresTech: boolean
digitalReady: boolean
hasAudioComponent: boolean
hasPrintableComponent: boolean
hasSlidesComponent: boolean
hasVisualComponent: boolean
adaptableToTopic: boolean      # Can this activity be adapted to any grammar topic?
instructions: [string]         # Step-by-step instructions
script: [string]               # Exact words for the teacher to say
setupInstructions: string      # How to prepare
differentiation:
  support: string              # Adaptations for weaker students
  extension: string            # Adaptations for stronger students
keywords: [string]             # Search keywords
l1Enhanced: boolean            # Whether this activity has L1-specific variants
```

### Example: `3-2-1-exit.yaml`

```yaml
id: 3-2-1-exit
name: 3-2-1 Exit Ticket
category: review
description: At the end of class, students write 3 things they learned, 2 things
  they found interesting, and 1 question they still have.
targetStructures:
  - sentence-structure
  - writing-accuracy
bestForLevels:
  - A1
  - A2
  - B1
  - B2
  - C1
duration: 5
groupSize: individuals
energyRequired: low
prepTime: none
materials:
  - Paper or index cards
format:
  - in-person
  - online
requiresTech: false
digitalReady: true
hasAudioComponent: false
hasPrintableComponent: false
hasSlidesComponent: false
hasVisualComponent: false
adaptableToTopic: true
instructions:
  - In the last 5 minutes of class, give each student a piece of paper or index card.
  - Ask them to write 3 things they learned today, 2 things they found interesting...
  - Collect the cards as students leave...
script:
  - "Before you leave, I want you to write me a quick note..."
  - "Thank you! I will read all of these and answer your questions next class."
setupInstructions: No setup needed. Have scrap paper or index cards available...
differentiation:
  support: "Provide sentence starters such as 'I learned that'..."
  extension: "Ask advanced students to also write how they would explain..."
keywords:
  - exit ticket
  - reflection
  - formative assessment
  - review
  - feedback
l1Enhanced: true
```

### Key Fields for Material Generation

| Field | Used For |
|-------|----------|
| `name`, `description` | Activity resource header |
| `targetStructures`, `bestForLevels` | Matching activities to requests |
| `instructions` | Step-by-step activity guide |
| `script` | Teacher script section |
| `materials`, `duration`, `groupSize` | Activity metadata |
| `differentiation` | Support + extension sections |
| `keywords` | Search matching in SearchActivitiesTool |

---

## 4. File Naming Conventions

| Directory | Pattern | Example |
|-----------|---------|---------|
| `data/grammar/` | `{slug}.yaml` | `present_simple.yaml`, `a_an_the.yaml` |
| `data/activities/` | `{slug}.yaml` | `3-2-1-exit.yaml`, `accent-detective.yaml` |
| `data/l1-interference/` | `{language}_interference.yaml` | `portuguese_interference.yaml` |

Slugs use lowercase with underscores. Multi-word grammar points use underscores (e.g., `present_simple`, `passive_voice`).

---

## 5. Adding New Data

### New Grammar Point
1. Create `data/grammar/{slug}.yaml`
2. Follow the schema above
3. At minimum, provide: `grammar_point`, `title`, `description`, `meaning`, `form`
4. SearchGrammarTool will find it automatically (5 matching strategies)

### New L1 Language
1. Create `data/l1-interference/{language}_interference.yaml`
2. Follow the schema above
3. `grammar_points` keys must match grammar_point slugs from `data/grammar/`
4. GetL1InterferenceTool will find it automatically

### New Activity
1. Create `data/activities/{slug}.yaml`
2. Follow the schema above
3. Include relevant `keywords` for search matching
4. SearchActivitiesTool will find it automatically
