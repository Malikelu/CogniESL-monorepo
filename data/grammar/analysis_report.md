# CogniESL Grammar YAML Analysis: Form Section Coverage

## Summary of ALL Files Analyzed

| # | Grammar File | form.affirmative | form.negative | form.questions | WH Q's in questions? | Passive in form? | cross_refs/builds_on |
|---|-------------|:-:|:-:|:-:|:-:|:-:|:-:|
| | **TENSE FILES** | | | | | | |
| 1 | present_simple | YES | YES | YES | No (yes/no only) | No | No |
| 2 | present_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 3 | past_simple | YES | YES | YES | No (yes/no only) | No | No |
| 4 | past_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 5 | present_perfect | YES | YES | YES | No (yes/no only) | No | No |
| 6 | present_perfect_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 7 | present_perfect_experiential | YES | YES | YES | "Have you ever..." format (still yes/no) | No | No |
| 8 | present_perfect_resultative | YES | YES | YES | No (yes/no only) | No | No |
| 9 | present_perfect_recent | YES | YES | YES | No (yes/no only) | No | No |
| 10 | present_perfect_baseline | YES | YES | YES | No (yes/no only) | No | No |
| 11 | past_perfect | YES | YES | YES | No (yes/no only) | No | No |
| 12 | past_perfect_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 13 | future_will | YES | YES | YES | No (yes/no only) | No | No |
| 14 | future_going_to | YES | YES | YES | No (yes/no only) | No | No |
| 15 | future_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 16 | future_perfect | YES | YES | YES | No (yes/no only) | No | No |
| 17 | future_perfect_continuous | YES | YES | YES | No (yes/no only) | No | No |
| 18 | used_to | YES | YES | YES | No (yes/no only) | No | No |
| 19 | will_vs_going_to | YES | YES | YES | No (yes/no only) | No | No |
| 20 | will_would_habits | YES | YES | NO (explicitly excluded) | N/A | No | No |
| | **QUESTION FILES** | | | | | | |
| 21 | question_tags | YES | YES | YES (tags are questions) | N/A (tags use polar form) | No | No |
| 22 | short_answers | YES | YES | YES (responds to questions) | N/A | No | No |
| 23 | negative_questions | YES | YES | YES | YES - "Why don't you...?" | No | No |
| 24 | indirect_questions | YES | YES | YES | YES - "where the station is" | No | No |
| 25 | subject_questions | YES | YES | YES | YES - "Who called you?" | No | No |
| 26 | object_questions | YES | YES | YES | YES - "Who did you call?" | No | No |
| 27 | question_forms | YES | YES | YES | YES - "Where do you live?" | No | No |
| 28 | interrogative_word_order | YES | YES | YES | YES - "Who lives here?" | No | No |
| 29 | word_order_questions | YES | YES | YES | YES - "Where do you live?" | No | No |

## Key Findings

### 1. Question Forms in Tense Files
**NONE of the 20 tense files contain WH question examples (like "Where do you live?", "What did you eat?") in their `form.questions` section.** They all only provide **yes/no question examples** (e.g., "Do you speak English?", "Did you walk to school?", "Have you eaten lunch?").

The question form structures use the appropriate auxiliary inversion for each tense:
- Present Simple: `Do/Does + subject + base verb?`
- Past Simple: `Did + subject + base verb?`
- Present Continuous: `Am/Is/Are + subject + verb-ing?`
- Present Perfect: `Have/Has + subject + past participle?`
- etc.

But they never demonstrate WH-question patterns like:
- "What do you eat for breakfast?" (Present Simple WH)
- "Where did she go?" (Past Simple WH)
- "How long have you lived here?" (Present Perfect WH)

### 2. Files with WH Question Content
Only these 8 files include WH question examples (what, where, who, why, how):
- **negative_questions** (line 119): "Why don't you like coffee?"
- **indirect_questions** (line 78): "Can you tell me where the station is?"
- **subject_questions** (lines 173-177): "Who called you?", "What happened?"
- **object_questions** (lines 142-144): "Who did you call?", "What did she buy?"
- **question_forms** (lines 189-191): "Where do you live?", "Who likes coffee?"
- **interrogative_word_order** (lines 88-94): "Who lives here?", "Where do you work?"
- **word_order_questions** (lines 57-58): "Where do you live?", "Who called?"

### 3. Negative Form Coverage
**ALL 29 files** have a `form.negative` section — except `will_would_habits` which has it, and all others have it. This is universal.

### 4. Passive Voice
**NONE of the tense files have a `form.passive` section.** Passive voice is handled exclusively in separate dedicated files:
- passive_basic.yaml
- passive_voice.yaml
- passive_voice_all_tenses.yaml
- passive_voice_complex.yaml
- simple_passive.yaml
- passive_with_two_objects.yaml
- passive_with_reporting_verbs.yaml
- modal_perfect_passive.yaml

The word "passive" appears in some tense YAML files, but only in `discourse_notes` or `register_notes` sections (e.g., present_perfect.yaml mentions it in discourse notes), never in the `form` section.

### 5. Cross References / Builds On
**ZERO files** in the entire grammar directory have `cross_references` or `builds_on` fields. This is a gap — there is no explicit linking between related grammar points.

### 6. `will_would_habits` is Unique
This is the **only** file that explicitly states questions are not used:
> "This structure is not typically used in questions for habitual meaning. Questions about habits use present simple or past simple."

And its `form.questions.example_generator.min_examples` is `0`.

## Structural Pattern

All tense files follow a consistent pattern:
```
form:
  affirmative:
    structure: ...
    example_generator: [...]
  negative:
    structure: ...
    example_generator: [...]
  questions:
    structure: ...
    example_generator: [...]
```

The `questions` section in every tense file only provides the **yes/no inversion pattern** — no WH-question forms are ever included in the tense files themselves.
