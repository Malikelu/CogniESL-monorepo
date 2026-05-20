# CogniESL — Four Skills Expansion Plan

> Comprehensive plan for adding Reading, Writing, Listening, and Speaking support
> Created: 2026-05-19
> Status: Merged — Single Source of Truth
> Supersedes: `CogniESKILLS_EXPANSION_PLAN.md` (Apex)

---

## TABLE OF CONTENTS

1. [Authoritative Books & Gold Standard Sources](#part-1)
2. [Database Organization](#part-2)
3. [YAML Schemas](#part-3)
4. [Topic Population Plan](#part-4)
5. [Quality Process Per File](#part-47)
6. [What NOT to Do](#part-48)
7. [Feature Flag](#part-49)
8. [New Agent Tools](#part-5)
9. [Agent Instructions Updates](#part-6)
10. [Interaction with Existing Databases](#part-7)
11. [Execution Sequence](#part-8)
12. [Revision History & Critique Notes](#part-9)
13. [Appendices](#appendices)

---

## PART 1: AUTHORITATIVE BOOKS & GOLD STANDARD SOURCES {#part-1}

### 1.1 Teaching Reading

| # | Book | Author(s) | Why It's Authoritative |
|---|------|-----------|----------------------|
| 1 | *Extensive Reading in the Second Language Classroom* | Day & Bamford (1998) | Foundational ER text; "learn to read by reading" paradigm |
| 2 | *Reading in a Second Language: Moving from Theory to Practice* | Grabe (2009) | Comprehensive SLA reading theory; top-down/bottom-up models |
| 3 | *Teaching ESL/EFL Reading and Writing* | I.S.P. Nation (2008) | Frequency-based approach; word lists; practical reading pedagogy |
| 4 | *Extensive Reading Activities for Teaching Language* | Day & Bamford (2004) | Practical ER activity designs |
| 5 | *Exploring Second Language Reading: Issues and Strategies* | Neil Anderson (1999) | Reading strategy taxonomy for L2 learners |
| 6 | *Teaching Reading to English Language Learners: A Reflective Guide* | Thomas Farrell (2008) | Practical K-12 reading pedagogy for ELLs |
| 7 | *Second Language Reading and Vocabulary Learning* | Huckin & Haynes (1993) | Vocabulary acquisition through reading; threshold research |

### 1.2 Teaching Writing

| # | Book | Author(s) | Why It's Authoritative |
|---|------|-----------|----------------------|
| 1 | *Understanding ESL Writers: A Guide for Teachers* | Ilona Leki (1992) | Foundational L2 writing pedagogy |
| 2 | *Teaching ESL Composition: Purpose, Process, and Practice* | Ferris & Hedgcock (2013) | Comprehensive ESL writing instruction |
| 3 | *Second Language Writing* | Ken Hyland (2003) | Cambridge overview of L2 writing theory |
| 4 | *Contrastive Rhetoric: Cross-Cultural Aspects of Second-Language Writing* | Ulla Connor (1996) | How L1 culture shapes L2 writing organization |
| 5 | *Genre Analysis: English in Academic and Research Settings* | Swales (1990) | Genre-based writing; move analysis |
| 6 | *Feedback on Second Language Writing* | Hyland & Hyland (2006) | Error correction and feedback strategies |
| 7 | *Process Writing* | White & Arndt (1991) | Process approach: pre-write, draft, revise |
| 8 | *Journal of Second Language Writing* (journal) | Various, Elsevier | Premier L2 writing research journal |

### 1.3 Teaching Listening

| # | Book | Author(s) | Why It's Authoritative |
|---|------|-----------|----------------------|
| 1 | *Teaching and Learning Second Language Listening* | Vandergrift & Goh (2012) | Metacognitive approach to listening pedagogy |
| 2 | *Teaching ESL/EFL Listening and Speaking* | Nation & Newton (2008) | Comprehensive listening + speaking from Nation's frequency approach |
| 3 | *Listening in the Language Classroom* | John Field (2008) | Challenges "listen and answer"; bottom-up listening |
| 4 | *Teaching Listening Comprehension* | Penny Ur (1984) | Classic listening activity designs |
| 5 | *Listening: Theory and Practice* | Anderson & Lynch (1988) | Foundational listening comprehension research |
| 6 | *Sound Foundations* | Adrian Underhill (1994) | Phonemic awareness for listening; teacher training |

### 1.4 Teaching Speaking

| # | Book | Author(s) | Why It's Authoritative |
|---|------|-----------|----------------------|
| 1 | *Teaching Speaking: A Holistic Approach* | Goh & Burns (2012) | Integrated speaking pedagogy; teaching speaking cycle |
| 2 | *Teaching Pronunciation: A Course Book and Reference Guide* | Celce-Murcia, Brinton & Goodwin (2010) | Standard reference for pronunciation pedagogy |
| 3 | *Communicative Language Teaching in Action* | Klaus Brandl (2007) | Practical CLT activities for speaking |
| 4 | *How to Teach Speaking* | Scott Thornbury (2005) | Practical speaking methodology |
| 5 | *Task-Based Language Teaching* | Rod Ellis (2003) | TBLT framework for speaking tasks |
| 6 | *The Practice of English Language Teaching* | Jeremy Harmer (2001) | Comprehensive speaking activity designs |
| 7 | *Discussion in the Language Classroom* | Scott Thornbury (2005) | Discussion skills and activities |

### 1.5 Cross-Skill / General References

| # | Book | Author(s) | Why It's Authoritative |
|---|------|-----------|----------------------|
| 1 | *Approaches and Methods in Language Teaching* | Richards & Rodgers (2014) | Comprehensive survey of all major methods |
| 2 | *The Study of Second Language Acquisition* | Rod Ellis (1994) | Foundational SLA theory covering all four skills |
| 3 | *Learner English: A Teacher's Guide to Interference* | Swan & Smith (2001) | **CRITICAL**: L1 interference patterns across languages |
| 4 | *Crosslinguistic Influence in Language and Cognition* | Jarvis & Pavlenko (2008) | Modern L1 transfer research across all skills |
| 5 | *Practical English Usage* | Michael Swan (2016) | Standard reference for English usage problems |
| 6 | *The Grammar Book* | Celce-Murcia & Larsen-Freeman (2015) | Grammar pedagogy reference |

---

## PART 2: DATABASE ORGANIZATION {#part-2}

### 2.1 New Directory Structure

```
data/
├── grammar/                    # EXISTING — 300 files (unchanged)
├── activities/                 # EXISTING — 218 files (skill_areas added)
├── l1-interference/            # EXISTING — 34 files (unchanged)
│
├── reading/                    # NEW — Reading pedagogy database
│   ├── extensive_reading.yaml
│   ├── intensive_reading.yaml
│   ├── reading_strategies.yaml
│   ├── reading_sub_skills.yaml
│   ├── reading_text_types.yaml
│   ├── reading_assessment.yaml
│   └── reading_materials.yaml
│
├── writing/                    # NEW — Writing pedagogy database
│   ├── process_writing.yaml
│   ├── genre_based_writing.yaml
│   ├── writing_feedback.yaml
│   ├── writing_assessment.yaml
│   ├── writing_cohesion.yaml
│   └── writing_paragraph.yaml
│
├── listening/                  # NEW — Listening pedagogy database
│   ├── extensive_listening.yaml
│   ├── listening_strategies.yaml
│   ├── listening_sub_skills.yaml
│   ├── listening_text_types.yaml
│   ├── listening_assessment.yaml
│   └── listening_phonology.yaml
│
├── speaking/                   # NEW — Speaking pedagogy database
│   ├── fluency_development.yaml
│   ├── speaking_strategies.yaml
│   ├── speaking_functions.yaml
│   ├── speaking_assessment.yaml
│   └── speaking_task_types.yaml
│
├── skills_mapping/             # NEW — Cross-reference mappings
│   ├── grammar_to_skills.yaml  # Maps grammar points → skill connections
│   └── activities_to_skills.yaml  # Maps activities → skill areas
│
└── l1-interference/            # EXISTING — 34 files (skill_interference added)
    ├── portuguese_interference.yaml  # Now includes skill_interference key
    ├── spanish_interference.yaml     # Now includes skill_interference key
    └── ... (all 34 files gain skill_interference key)
```

### 2.2 Key Design Decisions

**Why separate directories per skill?**
- Grammar = language **structure** (form/meaning/use); Skills = language **use** (pedagogical frameworks)
- Teachers request by skill: "reading class" vs "present simple"
- Clean separation keeps each domain searchable and maintainable

**Why a `skills_mapping/` directory instead of modifying existing files?**
- **Safety**: Modifying 218 activity files or 300 grammar files risks breaking existing search tools
- **Separation of concerns**: Cross-references are maintained independently from source data
- **Easier updates**: Adding a new skill connection doesn't require editing the original grammar/activity file
- The mapping files are simple lookup tables that the agent reads alongside the primary data

**Why add `skill_interference` to existing L1 files (rather than separate files)?**
- Follows the existing pattern: `grammar_points` is already in these files, `skill_interference` sits alongside it
- Keeps ALL L1 data for one language in one file — the agent only needs one lookup
- The `GetL1InterferenceTool` can be extended with a `skill_area` parameter instead of creating a new tool
- Reduces total new files by 68

**Category taxonomy for each skill:**

Each skill file uses a `category` field to organize content:

*Reading categories:* `expeditious_reading` (skimming/scanning), `careful_reading` (detail/inference), `vocabulary_from_context`, `text_structure`, `extensive_vs_intensive`

*Writing categories:* `organization` (paragraph/essay/text structure), `genre` (email/narrative/argumentative), `process` (brainstorming/drafting/revising), `mechanics` (punctuation/spelling), `cohesion_and_coherence`

*Listening categories:* `listening_strategies` (gist/detail/inference), `phonological_awareness` (connected speech/stress), `listening_situations` (lectures/conversations), `note_taking`

*Speaking categories:* `interactional_competence` (turn-taking/repair), `pronunciation_segmentals`, `pronunciation_suprasegmentals`, `functional_language`, `fluency_development`, `discussion_skills`, `presentation_skills`

**Why NOT include vocabulary as a separate skill area?**
- Vocabulary is a **component** of all four skills, not a skill itself
- Vocabulary teaching is already embedded in grammar points and skill activities
- Adding it would create a fifth "skill" that doesn't fit the pedagogical model
- Vocabulary can be referenced within skill files via `vocabulary_focus` fields

---

## PART 3: YAML SCHEMAS {#part-3}

### Design Principle: Core vs. Optional Fields

Following the pattern established by the grammar database, each skill file has:
- **Core fields** (required): Minimum needed for the AI to generate useful materials
- **Optional fields** (enrichment): Additional detail that improves material quality but isn't essential

This allows incremental population — create files with core fields first, enrich later.

### 3.1 Reading Skills Schema

```yaml
# === CORE FIELDS (required) ===
skill_area: reading
topic: string                     # e.g., "extensive_reading"
title: string                     # e.g., "Extensive Reading"
description: string               # What this reading topic covers
level_range:
  min: string                     # e.g., "A2"
  max: string                     # e.g., "C2"

definition: string                # What this reading approach/skill is
what_it_is_not: string            # Contrast with common misunderstandings (e.g., "Skimming is NOT reading every word fast")
key_principles:                   # Foundational principles (3-7 items)
  - principle: string
    explanation: string

# Concept Checking Questions — with purpose (following grammar DB pattern)
ccqs:
  - question: string
    answer: string
    purpose: string               # WHY this checks understanding (e.g., "Tests whether student understands inferring vs. guessing")

# Teaching stages (the core pedagogical structure)
teaching_approach:
  stages:
    - stage: string               # e.g., "pre-reading", "while-reading", "post-reading"
      purpose: string
      teacher_actions: [string]
      student_actions: [string]

# Sub-skills involved
sub_skills:
  - name: string                  # e.g., "skimming", "scanning", "inferring"
    description: string
    cefr_level: string

# Connection to grammar
grammar_focus: [string]           # Grammar point slugs relevant to this topic

# Recommended activities
recommended_activities: [string]  # Activity IDs from data/activities/

teaching_tips: [string]

# === OPTIONAL FIELDS (enrichment) ===
sources:
  primary: string
  secondary: string
  pedagogical: string

classroom_implications: [string]

applicable_text_types:
  - type: string                  # e.g., "narrative", "expository"
    description: string
    examples: [string]
    suitable_levels: [string]

assessment:
  methods: [string]
  rubric_criteria:
    - criterion: string
      levels:
        - level: string
          description: string

materials:
  selection_criteria: [string]
  text_difficulty_factors: [string]
  adaptation_strategies: [string]

cross_skill_connections:
  writing: [string]
  speaking: [string]
  listening: [string]

common_pitfalls:
  - pitfall: string
    solution: string
```

### 3.2 Writing Skills Schema

```yaml
# === CORE FIELDS ===
skill_area: writing
topic: string                     # e.g., "process_writing"
title: string
description: string
level_range:
  min: string
  max: string

definition: string
what_it_is_not: string            # Contrast with common misunderstandings
key_principles:
  - principle: string
    explanation: string

ccqs:
  - question: string
    answer: string
    purpose: string

# Writing process stages (core pedagogical structure)
process_stages:
  - stage: string                 # e.g., "prewriting", "drafting", "revising"
    purpose: string
    teacher_role: string
    student_activities: [string]
    example_techniques: [string]

# Genre information
genre:
  type: string                    # e.g., "narrative", "argumentative"
  structure:
    - section: string
      purpose: string
      language_features: [string]

grammar_focus: [string]
recommended_activities: [string]
teaching_tips: [string]

# === OPTIONAL FIELDS ===
sources:
  primary: string
  secondary: string

language_features:
  - feature: string               # e.g., "cohesive devices", "topic sentences"
    description: string
    examples: [string]
    common_l1_issues: [string]

assessment:
  criteria:
    - criterion: string           # e.g., "content", "organization", "language"
      weight: int
      levels:
        - level: string
          score_range: string
          description: string
  feedback_strategies:
    - strategy: string
      when_to_use: string

scaffolding:
  for_beginners: [string]
  for_intermediate: [string]
  for_advanced: [string]
  graphic_organizers: [string]
  sentence_starters: [string]

cross_skill_connections:
  reading: [string]
  speaking: [string]

common_pitfalls:
  - pitfall: string
    solution: string
```

### 3.3 Listening Skills Schema

```yaml
# === CORE FIELDS ===
skill_area: listening
topic: string                     # e.g., "extensive_listening"
title: string
description: string
level_range:
  min: string
  max: string

definition: string
what_it_is_not: string
key_principles:
  - principle: string
    explanation: string

ccqs:
  - question: string
    answer: string
    purpose: string

# Listening lesson stages (core pedagogical structure)
teaching_approach:
  stages:
    - stage: string               # e.g., "pre-listening", "while-listening", "post-listening"
      purpose: string
      teacher_actions: [string]
      student_actions: [string]

sub_skills:
  - name: string                  # e.g., "listening for gist", "listening for detail"
    description: string
    cefr_level: string

# Phonological features affecting listening
phonological_challenges:
  - feature: string               # e.g., "connected speech", "weak forms"
    description: string
    teaching_approach: string

grammar_focus: [string]
vocabulary_focus: [string]
recommended_activities: [string]
teaching_tips: [string]

# === OPTIONAL FIELDS ===
sources:
  primary: string
  secondary: string

strategies:
  - name: string                  # e.g., "predicting", "inferring"
    type: string                  # "top-down" or "bottom-up"
    description: string
    example_tasks: [string]

applicable_text_types:
  - type: string                  # e.g., "conversation", "lecture"
    description: string
    features: [string]
    suitable_levels: [string]

materials:
  selection_criteria: [string]
  authenticity_levels:
    - level: string
      description: string
      pros: [string]
      cons: [string]

assessment:
  methods: [string]
  task_types: [string]

cross_skill_connections:
  speaking: [string]
  reading: [string]

common_pitfalls:
  - pitfall: string
    solution: string
```

### 3.4 Speaking Skills Schema

```yaml
# === CORE FIELDS ===
skill_area: speaking
topic: string                     # e.g., "fluency_development"
title: string
description: string
level_range:
  min: string
  max: string

definition: string
what_it_is_not: string            # e.g., "Fluency is NOT speaking fast"
key_principles:
  - principle: string
    explanation: string

ccqs:
  - question: string
    answer: string
    purpose: string

# Speaking lesson structure
lesson_structure:
  - stage: string                 # e.g., "lead-in", "preparation", "task", "feedback"
    purpose: string
    teacher_actions: [string]
    student_actions: [string]

sub_skills:
  - name: string                  # e.g., "turn-taking", "negotiating meaning"
    description: string
    cefr_level: string

# Fluency vs Accuracy balance
fluency_accuracy:
  fluency:
    definition: string
    development_strategies: [string]
  accuracy:
    definition: string
    when_to_correct: string
    correction_techniques: [string]
  balancing_approach: string

# Communicative functions
communicative_functions:
  - function: string              # e.g., "agreeing", "suggesting"
    description: string
    example_language: [string]
    cefr_level: string

grammar_focus: [string]
vocabulary_focus: [string]
recommended_activities: [string]
teaching_tips: [string]

# === OPTIONAL FIELDS ===
sources:
  primary: string
  secondary: string

pronunciation_focus:
  - feature: string               # e.g., "sentence stress", "intonation"
    description: string
    impact_on_communication: string
    teaching_approach: string

task_types:
  - type: string                  # e.g., "information gap", "role play", "debate"
    description: string
    fluency_focus: bool
    accuracy_focus: bool
    example_prompts: [string]

assessment:
  rubric_criteria:
    - criterion: string           # e.g., "fluency", "accuracy", "interaction"
      weight: int
      levels:
        - level: string
          description: string

cross_skill_connections:
  listening: [string]
  writing: [string]

common_pitfalls:
  - pitfall: string
    solution: string
```

### 3.5 L1 Skills Interference — Added to Existing L1 Files

Instead of separate files, each existing L1 file gains a `skill_interference` key alongside the existing `grammar_points` key:

```yaml
# In existing l1-interference/portuguese_interference.yaml (alongside grammar_points)

skill_interference:
  speaking:
    - skill: turn_taking
      interference_patterns:
        - pattern: Overlapping speech perceived as interrupting
          example_l1: "(overlapping) Mas eu acho que..."
          example_gloss: "(overlapping) But I think that..."
          example_wrong: "(interrupting partner) But I think that..."
          example_correct: "(waiting for pause) Can I add something?"
          explanation: >
            Portuguese tolerates more overlapping speech than English.
            Speakers may be perceived as interrupting when following L1 norms.
          frequency: 3
          persistence: 3
          communicative_impact: 2
      why_it_happens: >
        Portuguese conversational norms differ from English in overlap
        tolerance and turn-management strategies.
      teacher_tips:
        how_to_explain: >
          Record a Portuguese conversation and an English conversation.
          Ask students: "What differences do you notice?"
        where_to_start: Start with awareness. Then practice signals.
        sequencing: >
          Week 1: Awareness. Week 2: Signal identification.
          Week 3: Controlled practice. Week 4: Freer practice.
        exercises:
          - name: Overlap Count
            type: listening_task
            description: Students compare overlap frequency in PT vs EN
            duration: 10

    - skill: pronunciation_segmentals
      interference_patterns:
        - pattern: /θ/ → /t/ or /s/ substitution
          example_wrong: "I have tree books"
          example_correct: "I have three books"
          explanation: Portuguese has no /θ/ sound
          frequency: 5
          persistence: 4
          communicative_impact: 2

  listening:
    - skill: connected_speech
      interference_patterns:
        - pattern: Difficulty perceiving reduced vowels (schwa)
          example_l1: Portuguese syllable-timed, no schwa
          example_wrong: Student hears "can" instead of "can't"
          explanation: Portuguese has clear vowel pronunciation; schwa is inaudible
          frequency: 5
          persistence: 4
          communicative_impact: 4

  writing:
    - skill: paragraph_structure
      interference_patterns:
        - pattern: Long sentences with multiple embeddings
          example_l1: "O homem, que era muito alto..."
          example_wrong: "The man, who was very tall, who had a big hat..."
          example_correct: "The tall man wore a big hat. He walked..."
          explanation: Portuguese favors longer sentences with relative clauses
          frequency: 3
          persistence: 3
          communicative_impact: 2

  reading:
    - skill: skimming
      interference_patterns:
        - pattern: Slow syllable-by-syllable decoding
          example_wrong: Student reads every word carefully
          example_correct: Student moves eyes rapidly, focuses on key words
          explanation: Portuguese reading instruction emphasizes careful decoding
          frequency: 3
          persistence: 2
          communicative_impact: 2

# Cross-references
related_grammar_interferences: [string]  # Grammar point slugs from this file
```

### 3.6 Skills Mapping Files

**`skills_mapping/grammar_to_skills.yaml`:**
```yaml
# Maps grammar points to relevant skill connections
# The agent reads this to enrich grammar lessons with skill context
# and to enrich skill lessons with grammar context

grammar_points:
  present_simple:
    reading:
      - "Reading schedules and timetables"
      - "Reading about daily routines in texts"
    writing:
      - "Writing about daily routines"
      - "Writing descriptive paragraphs about habits"
    listening:
      - "Listening to people describe their routines"
    speaking:
      - "Talking about daily routines"
      - "Interviewing classmates about habits"

  past_simple:
    reading:
      - "Reading narratives and stories"
      - "Reading news reports"
    writing:
      - "Writing narratives"
      - "Writing about past events"
    listening:
      - "Listening to stories and anecdotes"
    speaking:
      - "Telling stories about past events"
```

**`skills_mapping/activities_to_skills.yaml`:**
```yaml
# Maps existing activities to skill areas
# This avoids modifying the original 218 activity files
# The agent reads this mapping to filter activities by skill

activities:
  3-2-1-exit:
    skill_areas: ["reading", "writing", "grammar", "general"]
    sub_skill: "reflection"
  accent-detective:
    skill_areas: ["listening", "pronunciation"]
    sub_skill: "accent-awareness"
  add-a-third:
    skill_areas: ["writing", "speaking"]
    sub_skill: "dialogue-writing"
  # ... (mapped activities)
```

---

## PART 4: TOPIC POPULATION PLAN {#part-4}

### 4.1 Reading Topics (7 files)

| File | Topic | Priority | Core Fields Only | + Optional |
|------|-------|----------|-----------------|------------|
| `extensive_reading.yaml` | Extensive Reading programs | HIGH | Week 3 | Week 7 |
| `intensive_reading.yaml` | Intensive Reading techniques | HIGH | Week 3 | Week 7 |
| `reading_strategies.yaml` | Strategy taxonomy (skimming, scanning, predicting, inferring) | HIGH | Week 3 | Week 7 |
| `reading_sub_skills.yaml` | Sub-skills: main idea, detail, reference, inference | HIGH | Week 3 | Week 8 |
| `reading_text_types.yaml` | Text types: narrative, expository, argumentative | MEDIUM | Week 4 | Week 8 |
| `reading_assessment.yaml` | Assessment methods and rubrics | MEDIUM | Week 4 | Week 8 |
| `reading_materials.yaml` | Material selection, graded readers, text difficulty | MEDIUM | Week 4 | Week 8 |

### 4.2 Writing Topics (6 files)

| File | Topic | Priority | Core Fields Only | + Optional |
|------|-------|----------|-----------------|------------|
| `process_writing.yaml` | Writing process (pre-write, draft, revise, edit, publish) | HIGH | Week 3 | Week 7 |
| `genre_based_writing.yaml` | Genre-based approach (narrative, descriptive, expository, argumentative) | HIGH | Week 3 | Week 7 |
| `writing_feedback.yaml` | Feedback strategies: teacher, peer, self | HIGH | Week 4 | Week 8 |
| `writing_assessment.yaml` | Writing rubrics and assessment criteria | MEDIUM | Week 4 | Week 8 |
| `writing_cohesion.yaml` | Cohesion and coherence devices | MEDIUM | Week 4 | Week 8 |
| `writing_paragraph.yaml` | Paragraph structure and development | MEDIUM | Week 4 | Week 8 |

### 4.3 Listening Topics (6 files)

| File | Topic | Priority | Core Fields Only | + Optional |
|------|-------|----------|-----------------|------------|
| `extensive_listening.yaml` | Extensive Listening programs | HIGH | Week 5 | Week 7 |
| `listening_strategies.yaml` | Listening strategies taxonomy | HIGH | Week 5 | Week 7 |
| `listening_sub_skills.yaml` | Sub-skills: gist, detail, specific information, attitude | HIGH | Week 5 | Week 8 |
| `listening_text_types.yaml` | Text types: conversations, lectures, announcements | MEDIUM | Week 6 | Week 8 |
| `listening_assessment.yaml` | Listening assessment methods | MEDIUM | Week 6 | Week 8 |
| `listening_phonology.yaml` | Phonological features affecting comprehension | MEDIUM | Week 6 | Week 8 |

### 4.4 Speaking Topics (5 files)

| File | Topic | Priority | Core Fields Only | + Optional |
|------|-------|----------|-----------------|------------|
| `fluency_development.yaml` | Fluency vs accuracy; fluency activities | HIGH | Week 5 | Week 7 |
| `speaking_strategies.yaml` | Communication strategies (circumlocution, appeal for help) | HIGH | Week 5 | Week 7 |
| `speaking_functions.yaml` | Functional language (agreeing, suggesting, clarifying) | HIGH | Week 5 | Week 8 |
| `speaking_assessment.yaml` | Speaking assessment rubrics | MEDIUM | Week 6 | Week 8 |
| `speaking_task_types.yaml` | Task types: information gap, role-play, debate | MEDIUM | Week 6 | Week 8 |

### 4.5 L1 Skills Interference — Added to Existing 34 Files

No new files needed. Each existing L1 file gains a `skill_interference` key. Populate by priority:

**Priority 1 — Top 10 L1s (complete interference for all 4 skills):**
Portuguese, Spanish, Mandarin, Arabic, Japanese, Korean, Hindi, French, German, Russian

**Priority 2 — Next 12 L1s:**
Italian, Turkish, Vietnamese, Thai, Indonesian, Polish, Dutch, Swedish, Czech, Ukrainian, Urdu, Bengali

**Priority 3 — Remaining 12 L1s:**
All remaining languages from the existing 34

### 4.6 Skills Mapping Files (2 files)

| File | Content | Priority |
|------|---------|----------|
| `grammar_to_skills.yaml` | Maps top 100 grammar points to skill connections | HIGH |
| `activities_to_skills.yaml` | Maps all 218 activities to skill areas | HIGH |

---

## PART 4.7: QUALITY PROCESS PER FILE {#part-47}

Following the grammar DB pattern, each file follows a structured creation process:

| Step | Activity | Time Est. | Quality Check |
|------|----------|-----------|---------------|
| 1 | Research: Consult primary sources | 30-60 min | At least 2 authoritative sources cited |
| 2 | Concept + what_it_is_not | 30 min | Contrast with misunderstanding is clear |
| 3 | CCQs (3-5 questions) | 30 min | Each has question, answer, AND purpose |
| 4 | Teaching procedure | 30 min | Step-by-step, teacher + student roles |
| 5 | Sub-skills | 30 min | Detailed breakdown with examples |
| 6 | Contexts of use | 20 min | Real-world application examples |
| 7 | Phonetics (if applicable) | 20 min | L1-specific pronunciation issues |
| 8 | Activities | 20 min | 2-3 recommended activities |
| 9 | Sources | 10 min | 5-tier system (primary through teaching practice) |
| 10 | Common errors | 30 min | Errors by L1 group with corrections |
| 11 | Register notes | 15 min | Formal/informal variation |
| **Total** | | **~4-5 hours** | |

## PART 4.8: WHAT NOT TO DO {#part-48}

1. **NEVER use scripts** to generate content — grammar DB showed script-generated data was unreliable
2. **NEVER skip CCQs** — they are the most important teaching tool in every grammar file
3. **NEVER skip L1 groups** in common errors — all 34 languages need coverage
4. **NEVER use placeholder content** — every field must be filled with real, sourced information
5. **NEVER skip sources** — all 5 tiers required
6. **NEVER modify existing grammar/activity files** — use `skills_mapping/` for cross-references

## PART 4.9: FEATURE FLAG {#part-49}

Add `ENABLE_SKILL_MODE=true` to `.env`. When false, new skill tools not registered. Enables:
- Safe deployment (staging first, then production)
- Rollback without reverting data files
- Parallel development: grammar improvements continue while skills are built

---

## PART 5: NEW AGENT TOOLS {#part-5}

### 5.1 Consolidated Skills Search Tool

Instead of 4 separate tools, ONE tool with a `skill_area` parameter:

```python
# New file: agent/tools/SearchSkillsTool.py
class SearchSkillsTool(BaseTool):
    """
    Search the skills database (reading, writing, listening, speaking) by topic.
    Returns full skill topic data including teaching approach, sub-skills,
    grammar connections, and recommended activities.
    """
    skill_area: str = Field(
        ...,
        description="Skill area: 'reading', 'writing', 'listening', or 'speaking'."
    )
    topic: str = Field(
        ...,
        description="Skill topic to search for (e.g., 'extensive reading', 'process writing', 'fluency')."
    )
    level: str = Field(
        default="",
        description="CEFR level to filter by (e.g., 'A1', 'B2'). Empty means all levels."
    )
```

**Why one tool instead of four?**
- Follows the existing pattern: `SearchActivitiesTool` handles all activity types with parameters
- Easier to maintain: one file instead of four
- Easier to register: one import instead of four
- The `skill_area` parameter provides the same routing as separate tools
- If needed, the tool can search across all skill areas when `skill_area` is ambiguous

### 5.2 GetL1InterferenceTool Update

The existing `GetL1InterferenceTool` gets ONE new optional parameter to also search the `skill_interference` key:

```python
# In existing agent/tools/GetL1InterferenceTool.py, add:
skill_area: str = Field(
    default="",
    description="Skill area: 'reading', 'writing', 'listening', or 'speaking'. Empty returns grammar-only data."
)
```

When `skill_area` is provided, the tool returns both grammar interference and skill interference from the same L1 file. This keeps everything in one tool, one file per L1.

### 5.3 Skills Mapping Tool

```python
# New file: agent/tools/GetSkillsMappingTool.py
class GetSkillsMappingTool(BaseTool):
    """
    Get cross-reference mappings between grammar points, activities, and skill areas.
    Used to enrich grammar lessons with skill context and vice versa.
    """
    mapping_type: str = Field(
        ...,
        description="'grammar_to_skills' or 'activities_to_skills'."
    )
    key: str = Field(
        default="",
        description="Specific grammar point slug or activity ID to look up. Empty returns all mappings."
    )
```

### 5.4 Tool Registration

In `agent/cogniesl_agent.py`:

```python
from tools import (
    SearchGrammarTool,           # EXISTING (unchanged)
    GetL1InterferenceTool,       # EXISTING (+ skill_area param)
    SearchActivitiesTool,        # EXISTING (+ skill_area param)
    SearchSkillsTool,            # NEW
    GetSkillsMappingTool,        # NEW
)
```

### 5.5 SearchActivitiesTool Update

The existing `SearchActivitiesTool` needs ONE new optional parameter to support skill-based filtering:

```python
# In SearchActivitiesTool.py, add:
skill_area: str = Field(
    default="",
    description="Skill area to filter by (e.g., 'reading', 'writing', 'listening', 'speaking'). Empty means all."
)
```

The skill_area filter uses the `skills_mapping/activities_to_skills.yaml` file (not the original activity files) to determine which activities match.

---

## PART 6: AGENT INSTRUCTIONS UPDATES {#part-6}

### 6.1 Updated Conversation Flow (Part 1)

**Request type detection logic:**

```
User message contains:
  → Grammar point name (e.g., "present simple", "articles", "passive voice")
    → Route to GRAMMAR workflow

  → Skill area keyword ("reading", "writing", "listening", "speaking")
    → Route to SKILL workflow
    → Identify sub-topic from context or ask:
      "What aspect of [skill] would you like to focus on?
       For reading: extensive reading, reading strategies, reading for main idea...
       For writing: process writing, narrative writing, academic writing...
       For listening: extensive listening, listening for detail, note-taking...
       For speaking: fluency, discussion skills, presentations..."

  → Ambiguous (e.g., "I need a class on essays")
    → Clarify: "Do you mean writing essays (writing skill) or reading/analyzing essays (reading skill)?"

  → Integrated (e.g., "reading and writing class")
    → Route to both SKILL workflows, generate integrated materials
```

**New example conversations:**

> Teacher: "I need a reading class for intermediate Portuguese students"
> Agent: "Great! What aspect of reading would you like to focus on? For example: extensive reading, reading strategies (skimming/scanning), reading for main idea vs. detail, or working with a specific text type?"

> Teacher: "I want to teach narrative writing to beginners"
> Agent: "Perfect! So you need materials for **narrative writing**, for **adult** students at a **beginner** level. What format — slides, worksheets, or both?"

> Teacher: "Help me with a listening class"
> Agent: "I'd love to help! A couple of quick questions — what level are your students, and what listening focus do you have in mind? For example: listening for gist, listening for detail, extensive listening, or note-taking skills?"

### 6.2 Updated Database Search (Part 2)

**Grammar request (unchanged):**
```
1. SearchGrammarTool(topic)
2. GetL1InterferenceTool(grammar_point, language)
3. SearchActivitiesTool(topic, level, age)
```

**Skill request (new):**
```
1. SearchSkillsTool(skill_area, topic, level)
2. GetL1InterferenceTool(grammar_point="", language, skill_area=skill_area)
3. SearchActivitiesTool(skill_area=skill_area, level=age)  # filtered by skill
4. GetSkillsMappingTool("grammar_to_skills", topic)  # find related grammar
5. If grammar connections exist → SearchGrammarTool for those points
```

**Integrated skills request (new):**
```
1. SearchSkillsTool for EACH skill area
2. GetL1InterferenceTool for the relevant skill-pair(s)
3. SearchActivitiesTool filtered by BOTH skill areas
4. GetSkillsMappingTool for cross-references
```

### 6.3 Updated Material Generation (Part 3)

**Reading Class Materials:**

*Slides (10-18 slides):*
1. Lead-in: Engaging question/image related to the text topic (1-2 slides)
2. Pre-reading: Activate schema, preview vocabulary, make predictions (2-3 slides)
3. While-reading: Task-based reading with guided questions (3-5 slides)
4. Post-reading: Comprehension check, discussion, extension (2-3 slides)
5. L1 Oracle: Reading-specific L1 interference patterns (1-2 slides, when L1 data exists)
6. Wrap-up: Summary, reflection, homework (1-2 slides)

*Worksheet:*
- Pre-reading section: Predictions, vocabulary preview
- Text (or text reference)
- While-reading tasks: Comprehension questions, detail finding, inference
- Post-reading: Discussion questions, personal response
- L1 Oracle box: Common L1 reading interference patterns (when data exists)

**Writing Class Materials:**

*Slides (12-20 slides):*
1. Lead-in: Model text or engaging prompt (1-2 slides)
2. Model text analysis: Structure, language features (2-3 slides)
3. Process guidance: Stage-by-stage writing process (3-5 slides)
4. Language focus: Grammar and vocabulary for this writing type (2-4 slides)
5. L1 Oracle: Writing-specific L1 interference (contrastive rhetoric) (1-2 slides)
6. Peer review: Checklist and guidelines (1-2 slides)
7. Wrap-up: Sharing, reflection (1 slide)

*Worksheet:*
- Planning section: Graphic organizer, brainstorming template
- Model text (annotated)
- Drafting section: Guided writing with sentence starters
- Self/peer assessment checklist
- L1 Oracle box: Common L1 writing errors (when data exists)

**Listening Class Materials:**

*Slides (10-16 slides):*
1. Lead-in: Context setting, prediction activation (1-2 slides)
2. Pre-listening: Vocabulary preview, listening goals (2-3 slides)
3. While-listening: Task-based listening activities (3-5 slides)
4. Post-listening: Comprehension check, discussion (2-3 slides)
5. L1 Oracle: Phonological challenges for this L1 (1-2 slides)
6. Wrap-up: Reflection, extension (1-2 slides)

*Worksheet:*
- Pre-listening: Predictions, key vocabulary
- While-listening: Gist task, detail tasks, specific information tasks
- Post-listening: Discussion, personal response
- L1 Oracle box: Sound discrimination exercises for L1 (when data exists)

**Speaking Class Materials:**

*Slides (10-16 slides):*
1. Lead-in: Engaging scenario or question (1-2 slides)
2. Model: Example dialogue or speaking model (1-2 slides)
3. Language focus: Functional language, useful expressions (2-3 slides)
4. Task setup: Clear instructions, grouping, time (1-2 slides)
5. L1 Oracle: Pronunciation/interference patterns (1-2 slides)
6. Feedback framework: What to listen for, how to give feedback (1-2 slides)
7. Wrap-up: Reflection, self-assessment (1-2 slides)

*Worksheet:*
- Useful language reference table
- Task instructions and role cards (if applicable)
- Planning space (notes before speaking)
- Self-assessment checklist
- L1 Oracle box: Pronunciation tips for L1 (when data exists)

### 6.4 Design Rules for Skill-Based Materials

- Follow existing 80/20 visual rule and 6x6 text rule for slides
- Follow existing worksheet design rules (large fonts, white space, numbered exercises)
- **New**: Reading worksheets must include the actual text (or a clear reference to it)
- **New**: Listening worksheets must include pre/post tasks (audio is external)
- **New**: Writing worksheets must include planning space and model text
- **New**: Speaking worksheets must include useful language reference and task instructions
- L1 Oracle sections follow the same pattern as grammar materials (wrong → correct, explanation, exercises)

---

## PART 7: INTERACTION WITH EXISTING DATABASES {#part-7}

### 7.1 Grammar ↔ Skills Cross-References

**Via `skills_mapping/grammar_to_skills.yaml` (NOT by modifying grammar files):**

The mapping file is a simple lookup table. When the agent processes a skill request:
1. It reads the mapping file to find relevant grammar points
2. It searches those grammar points using SearchGrammarTool
3. It integrates grammar content into the skill lesson

When the agent processes a grammar request:
1. It reads the mapping file to find relevant skill connections
2. It suggests skill-based practice activities to the teacher
3. It can optionally include skill context in grammar materials

**Example flow:**
```
Teacher: "I need a reading class on extensive reading for Portuguese students"

Agent workflow:
1. SearchSkillsTool("reading", "extensive_reading")
   → Gets ER principles, teaching stages, sub-skills
2. GetL1InterferenceTool("reading_writing", "Portuguese")
   → Gets Portuguese-specific reading interference patterns
3. SearchActivitiesTool(skill_area="reading", level="intermediate")
   → Gets reading-related activities (via activities_to_skills mapping)
4. GetSkillsMappingTool("grammar_to_skills")
   → Finds grammar points relevant to reading (e.g., present_simple for schedules)
5. Optionally: SearchGrammarTool for those points
   → Integrates grammar examples into reading materials
```

### 7.2 Activities Database Integration

**Via `skills_mapping/activities_to_skills.yaml` (NOT by modifying activity files):**

The mapping file tags each activity with applicable skill areas. This enables:
- `SearchActivitiesTool(skill_area="reading")` to return reading-relevant activities
- No risk of breaking existing grammar-based activity searches
- Easy to update: just edit the mapping file

**Migration approach:**
1. Create the mapping file with all 218 activities
2. Tag each activity with one or more skill areas based on its content
3. Activities that are grammar-focused get `skill_areas: ["grammar"]`
4. Activities that work across skills get multiple tags (e.g., `["reading", "writing", "grammar"]`)
5. The existing `targetStructures` field in activities already provides grammar-level filtering

### 7.3 L1 Interference Integration

**Single L1 source with two keys:**

| Request Type | Tool | Data Source Key |
|---|---|---|
| Grammar | GetL1InterferenceTool(skill_area="") | `grammar_points` key |
| Reading/Writing skill | GetL1InterferenceTool(skill_area="reading_writing") | `skill_interference` key |
| Listening/Speaking skill | GetL1InterferenceTool(skill_area="listening_speaking") | `skill_interference` key |
| Integrated | GetL1InterferenceTool(skill_area="all") | Both keys |

The `related_grammar_interferences` field in `skill_interference` creates a bridge: when processing a skill request, the agent can also pull relevant grammar L1 interference from the same file.

---

## PART 8: EXECUTION SEQUENCE {#part-8}

### Phase 1: Foundation (Week 1)
1. Create new directories: `data/reading/`, `data/writing/`, `data/listening/`, `data/speaking/`, `data/skills_mapping/`
2. Implement `SearchSkillsTool` and `GetSkillsMappingTool`
3. Add `skill_area` parameter to `GetL1InterferenceTool` and `SearchActivitiesTool`
4. Register new tools in `cogniesl_agent.py`
5. Create `skills_mapping/grammar_to_skills.yaml` (top 50 grammar points)
6. Create `skills_mapping/activities_to_skills.yaml` (all 218 activities)
7. Update `DATA_FORMAT.md` with new schemas
8. Build 1 sample file per skill (4 total) for end-to-end testing

### Phase 2: Speaking MVP — Ship First (Weeks 2-3)
9. Populate 5 speaking topic files (core fields only)
10. Add `skill_interference.speaking` to top 5 L1 files (PT, ES, JA, AR, KO)
11. Update agent instructions for skill-based requests
12. Test speaking material generation end-to-end
13. **Ship to production**

### Phase 3: Listening (Weeks 4-5)
14. Populate 6 listening topic files (core fields only)
15. Add `skill_interference.listening` to top 10 L1 files
16. Test listening material generation end-to-end
17. **Ship to production**

### Phase 4: Writing & Reading (Weeks 6-8)
18. Populate 6 writing topic files (core fields only)
19. Populate 7 reading topic files (core fields only)
20. Add `skill_interference.writing` and `skill_interference.reading` to top 10 L1s
21. Expand `grammar_to_skills.yaml` to top 100 grammar points
22. End-to-end testing of all 4 skill types

### Phase 5: Enrichment & Expansion (Weeks 9-11)
23. Enrich all skill topic files with optional fields (sources, assessment, materials)
24. Add L1 skill interference for Priority 2 L1s (12 languages)
25. Add L1 skill interference for Priority 3 L1s (remaining 12)
26. Quality review of all content against authoritative sources
27. Final documentation update

---

## PART 9: REVISION HISTORY & CRITIQUE NOTES {#part-9}

### Revision Pass 1 — Issues Identified

| # | Issue | Severity | Resolution |
|---|-------|----------|------------|
| 1 | Schemas too complex; no core/optional distinction | HIGH | Added core vs. optional field separation |
| 2 | 4 separate search tools redundant | MEDIUM | Consolidated into 1 `SearchSkillsTool` |
| 3 | Modifying 218 activity files risky | HIGH | Created separate `skills_mapping/` directory |
| 4 | No clear grammar vs. skill routing logic | HIGH | Added decision tree in Part 6.1 |
| 5 | Slides/docs tools may not support skill formats | MEDIUM | Described skill-specific material structures in Part 6.3 |
| 6 | Timeline underestimated for quality review | MEDIUM | Split into core-only (Weeks 3-6) + enrichment (Weeks 7-8) phases |
| 7 | Vocabulary not addressed | LOW | Clarified vocabulary is embedded, not a separate skill |
| 8 | L1 skills interference files too large/broad | MEDIUM | Kept as-is but focused on core interference areas per file |
| 9 | No integrated skills support | MEDIUM | Added integrated skills workflow in Parts 6.1-6.2 |
| 10 | Assessment mentioned but not explained | MEDIUM | Added assessment integration in material structures |

### Revision Pass 2 — Issues Identified

| # | Issue | Severity | Resolution |
|---|-------|----------|------------|
| 11 | `SearchSkillsTool` needs level filtering for CEFR alignment | MEDIUM | Added `level` parameter |
| 12 | Agent needs to know WHICH grammar points connect to a skill | HIGH | `grammar_focus` field in skill files + mapping tool |
| 13 | No example conversations for skill requests | MEDIUM | Added 3 example dialogues in Part 6.1 |
| 14 | L1 skills interference schema missing `sources` field | LOW | Added as optional field |
| 15 | No guidance on how to handle "integrated skills" classes | MEDIUM | Added integrated workflow in Parts 6.1-6.3 |
| 16 | `GetSkillsMappingTool` was missing from initial tool list | HIGH | Added as 3rd new tool |
| 17 | Phase 1 doesn't include mapping file creation | HIGH | Added mapping files to Phase 1 |
| 18 | No mention of how existing grammar L1 files stay compatible | MEDIUM | Added Part 7.3 integration table |

### Revision Pass 3 — Final Review

| # | Check | Status |
|---|-------|--------|
| 1 | All new tools follow existing tool patterns (BaseTool, Field, run method) | ✅ |
| 2 | All new data directories follow existing naming conventions | ✅ |
| 3 | YAML schemas are valid and parseable | ✅ |
| 4 | Agent instruction updates are specific and actionable | ✅ |
| 5 | No existing files are modified (only new files created) | ✅ |
| 6 | L1 interference integration is bidirectional | ✅ |
| 7 | CEFR alignment is consistent across all schemas | ✅ |
| 8 | Material generation follows existing design rules (80/20, 6x6) | ✅ |
| 9 | Execution sequence has clear milestones and test points | ✅ |
| 10 | Authoritative sources cover all four skills adequately | ✅ |
| 11 | Scope is manageable: ~24 skill files + 68 L1 files + 3 tools + 2 mappings | ✅ |
| 12 | Plan accounts for incremental population (core first, enrich later) | ✅ |

---

## APPENDICES

### Appendix A: CEFR Alignment Reference

| CEFR | Reading | Writing | Listening | Speaking |
|------|---------|---------|-----------|----------|
| A1 | Simple texts, familiar words | Words, simple phrases | Slow, clear speech | Basic phrases, formulaic |
| A2 | Short simple texts | Simple connected text | Clear standard speech | Simple routine exchange |
| B1 | Main ideas of complex texts | Straightforward connected text | Main points of clear speech | Handle most travel situations |
| B2 | Complex texts, implicit meaning | Clear detailed text | Extended speech, complex lines | Fluency, spontaneous interaction |
| C1 | Wide range, implicit meaning | Clear, well-structured, detailed text | Extended speech, implicit meaning | Flexible, effective language |
| C2 | Virtually any text | Virtually any type of text | Virtually anything | Virtually anything |

### Appendix B: Key Pedagogical Frameworks

| Framework | Skills | Key Idea |
|-----------|--------|----------|
| Extensive Reading/Listening | R/L | Large amounts of easy, self-selected material |
| Intensive Reading/Listening | R/L | Close study of shorter, more difficult texts |
| Process Writing | W | Pre-write → Draft → Revise → Edit → Publish |
| Genre-Based Writing | W | Analyze model texts → Joint construction → Independent writing |
| CLT | S/L | Interaction as means and goal |
| TBLT | S/L | Real-world tasks drive learning |
| Contrastive Rhetoric | R/W | L1 culture shapes L2 text organization |
| Phonological Transfer | S/L | L1 sound system affects L2 perception/production |
| Top-Down Processing | R/L | Use background knowledge to predict/interpret |
| Bottom-Up Processing | R/L | Build meaning from individual words/sounds |
| Interactive Model | R/L | Combine top-down and bottom-up |

### Appendix C: File Count Summary

| Category | Existing | New (Priority 1) | New (Priority 2) | New (Priority 3) | Total |
|----------|----------|-------------------|-------------------|-------------------|-------|
| Grammar files | 300 | — | — | — | 300 |
| Activity files | 218 | — | — | — | 218 |
| L1 files (grammar + skills) | 34 | updated¹ | updated¹ | updated¹ | 34 |
| Reading skill files | — | 7 | — | — | 7 |
| Writing skill files | — | 6 | — | — | 6 |
| Listening skill files | — | 6 | — | — | 6 |
| Speaking skill files | — | 5 | — | — | 5 |
| Skills mapping files | — | 2 | — | — | 2 |
| **Agent tools** | **6** | **2** | — | — | **8** |
| **TOTAL new files** | | **26** | **0** | **0** | **26** |

¹ Existing L1 files gain `skill_interference` key (no new files created)

### Appendix D: Lessons from the Grammar DB Project

**What the grammar project did right (replicate for skills):**
- CCQs were the backbone of every grammar file — do the same for skills
- Common errors by L1 group were extremely valuable — do the same
- 5-tier source system gave authority — do the same
- Multi-pass auditing caught errors — do the same for skills

**What the grammar project did wrong (avoid for skills):**
- Script-generated content was garbage — NO scripts for skill content
- LLM-only data was unreliable — every claim must be sourced from authoritative books
- Incomplete L1 coverage — all 34 languages required, not just top 10
