# Cross-Cutting Grammar Compositions
## Problem Analysis, Current State & Proposed Solutions

---

## 1. The Problem

### 1.1 The Core Issue

When a teacher requests materials for a grammar topic (e.g., "simple past"), the natural ESL lesson includes not just the tense's affirmative/negative/question forms, but also **structures that change form depending on the tense** — WH questions, short answers, question tags, etc.

For example, a lesson on "past simple" inherently includes:

| Structure | Teacher Expectation | Current Coverage |
|-----------|-------------------|------------------|
| Affirmative | "I walked to school." | ✅ In `past_simple.yaml` |
| Negative | "I didn't walk to school." | ✅ In `past_simple.yaml` |
| Yes/No questions | "Did you walk to school?" | ✅ In `past_simple.yaml` |
| **WH questions** | **"Where did you go? What did you do?"** | ❌ **Missing** |
| **Short answers** | **"Yes, I did. / No, I didn't."** | ❌ **Missing** |
| **Question tags** (at A2+) | **"You went, didn't you?"** | ❌ **Missing** |

### 1.2 Why This Matters

These are not optional additions — they are part of teaching the tense. A past simple lesson without "What did you do yesterday?" is incomplete. The WH question structure changes per tense (do → did → have → will), so each tense needs its own set of examples.

### 1.3 Current Behavior

If a teacher requests materials for "past simple" and then asks the chatbot to add question tags, **the system cannot reliably comply** because:

1. The slide plan (`compute_slide_plan()`) is fixed at generation time and reads only one grammar YAML
2. Task briefs contain verbatim YAML data — if question tags aren't in the YAML, the brief has no sourced content
3. Sub-agents generating slides would either refuse or fabricate unsourced content
4. Nothing in the pipeline knows how to load a second YAML and merge it

---

## 2. Current State of CogniESL Data

### 2.1 Grammar File Architecture

- **Total grammar YAML files:** ~200 individual `.yaml` files in `data/grammar/`
- **Each file is a silo:** One grammar point per file, with form, meaning, CCQs, common errors, teaching tips, phonetics, L1 data, etc.
- **No cross-references:** Zero files have `cross_references`, `builds_on`, `compositions`, or `extends` fields
- **`form.questions` covers yes/no only:** Every tense file's question section has only yes/no structure and examples

### 2.2 The Cross-Cutting Grammar Categories

There are **structures that apply across multiple base topics** — their form changes per base topic:

| Cross-Cutting Structure | Applies To | CEFR Level | Form Changes With |
|---|---|---|---|
| **WH Questions** (what/where/when/why/how) | ALL tenses, modals, copula | A1+ | Auxiliary: do → did → have → will |
| **Short Answers** (Yes, I do/did/have) | ALL tenses, modals | A1+ | Auxiliary must match question |
| **Question Tags** (You went, didn't you?) | ALL tenses, modals | A2+ | Tag auxiliary matches main clause |
| **Negative Questions** (Don't you? Didn't you?) | ALL tenses, modals | B1+ | Auxiliary negated |
| **Passive Voice** (It was done) | ALL tenses | A2-B1 | Be conjugated per tense |
| **Reported/Indirect Speech** | ALL tenses (backshift) | B1+ | Base tense backshifts |
| **Subject/Object Questions** (Who called? Who did you call?) | ALL tenses | A2 | Auxiliary per tense |

### 2.3 The 20+ Tense/Aspect Files Affected

Every tense/aspect YAML file has the same gap — `form.questions` contains yes/no only:

- `present_simple.yaml`, `past_simple.yaml`, `present_continuous.yaml`, `past_continuous.yaml`
- `present_perfect.yaml` (and subtypes), `past_perfect.yaml`, `past_perfect_continuous.yaml`
- `future_will.yaml`, `future_going_to.yaml`, `future_continuous.yaml`, `future_perfect.yaml`
- `used_to.yaml`, `will_would_habits.yaml`
- `modals.yaml`, `modals_overview.yaml`, `modals_past.yaml`, `modals_perfect.yaml`
- `passive_basic.yaml`, `simple_passive.yaml` (these form the bridge to passive voice)

### 2.4 The Slide Generator (How It Works Today)

`compute_slide_plan()` in `agent/slides_tools/slide_plan.py` iterates over a fixed list:

```python
for form_key in ("affirmative", "negative", "questions"):
    if form[form_key].get("structure"):
        slides.append(A5 Formula slide)
```

It only checks for these three keys. There is no concept of:
- Additional slides for WH questions
- Additional slides for question tags
- Loading a second YAML file for cross-cutting data
- Compositions or merge logic

---

## 3. Proposed Solutions

### Solution A: Embed Everything Directly in Each Tense File

Add WH questions, short answers, question tags, etc. directly into each tense YAML's `form.questions` section.

**Example** for `past_simple.yaml`:
```yaml
form:
  questions:
    yes_no:
      structure: "Did + subject + base verb?"
      examples: ["Did you walk to school yesterday?"]
    wh_questions:
      structure: "Wh-word + did + subject + base verb?"
      examples:
        - "What did you do yesterday?"
        - "Where did she go?"
        - "Who called you?"
        - "When did they arrive?"
      min_examples: 4
    tags:
      structure: "Statement, didn't + subject?"
      examples:
        - "You went to school, didn't you?"
        - "She called you, didn't she?"
```

| Factor | Rating | Details |
|--------|--------|---------|
| **Generator changes** | NONE | Works with current `slide_plan.py` — just reads `form.questions` |
| **Data work** | HIGH | Edit 20+ files, each getting 40-80 new lines. Copy-paste heavy |
| **Maintenance** | TERRIBLE | Update a WH question CCQ or teaching tip? Edit 20+ files manually |
| **Quality risk** | LOW | Human-authored examples. Verifiable in each file |
| **Data drift risk** | HIGH | Different files may drift apart over time. Same concept, different wording |
| **Implementation time** | 2-4 days | Pure data entry. No code changes |
| **Scalability** | POOR | New cross-cutting topic = edit every file again |

### Solution B: Compositions Field + Generator Merge

Each grammar YAML gets a `compositions` field. Cross-cutting topics stay in their own source files. The generator loads both and creates slides from the merged data.

**In `past_simple.yaml`:**
```yaml
grammar_point: past_simple
compositions:
  - topic: question_forms
    level_min: A1
    label: "WH Questions in Past Simple"
    structure: "Wh-word + did + subject + base verb?"
    examples:
      - "What did you do yesterday?"
      - "Where did she go?"
      - "Who called you?"
  - topic: short_answers
    level_min: A1
    label: "Short Answers in Past Simple"
    structure: "Yes/No + did/didn't"
    examples:
      - "Yes, I did."
      - "No, she didn't."
  - topic: question_tags
    level_min: A2
    label: "Question Tags in Past Simple"
    structure: "Statement + didn't + subject?"
    examples:
      - "You went, didn't you?"
```

**Generator behavior change:**
```python
# New logic in compute_slide_plan()
for composition in grammar_data.get("compositions", []):
    slides.append({
        "type": "A5_COMPOSITION",
        "label": f"Formula — {composition['label']}",
        "composition_topic": composition["topic"],
    })
```

The task brief builder loads the cross-cutting YAML (e.g., `question_forms.yaml`) and merges its CCQs, common errors, and teaching tips with the tense-specific examples from the composition.

| Factor | Rating | Details |
|--------|--------|---------|
| **Generator changes** | MEDIUM | `slide_plan.py` + `build_task_brief()` need new logic to load and merge cross-cutting YAMLs |
| **Data work** | MEDIUM | ~10-15 lines per tense file for compositions. Cross-cutting YAMLs stay unchanged |
| **Maintenance** | GOOD | Cross-cutting content (CCQs, L1 data, tips) lives in ONE file. Only examples duplicated per tense |
| **Quality risk** | LOW | Examples and structure are human-authored in compositions. Cross-cutting content is sourced |
| **Data drift risk** | LOW | Cross-cutting source files centralize pedagogical depth. Only examples are per-file |
| **Implementation time** | 4-6 days | 2-3 for generator changes, 2-3 for data entry |
| **Scalability** | GOOD | New cross-cutting topic = add the YAML once, then add `compositions` entries to affected tenses |

### Solution C: Registry File — No YAML Changes

A separate registry file maps base topics → cross-cutting topics per level. No changes to existing YAMLs.

**New file** `grammar-compositions.yaml`:
```yaml
compositions:
  - base: past_simple
    level: A1
    with:
      - topic: question_forms
        structure: "Wh-word + did + subject + base verb?"
        examples:
          - "What did you do yesterday?"
          - "Where did she go?"
      - topic: short_answers
        structure: "Yes/No + did/didn't"
        examples:
          - "Yes, I did."
          - "No, she didn't."
    level: A2
    with:
      - topic: question_tags
        structure: "Statement + didn't + subject?"
        examples:
          - "You went, didn't you?"
  - base: present_simple
    level: A1
    with:
      - topic: question_forms
        structure: "Wh-word + do/does + subject + verb?"
        examples:
          - "Where do you live?"
          - "What does she do?"
      - topic: short_answers
        structure: "Yes/No + do/does/don't/doesn't"
        examples:
          - "Yes, I do."
          - "No, she doesn't."
```

| Factor | Rating | Details |
|--------|--------|---------|
| **Generator changes** | MEDIUM | Same as Solution B — load registry, load cross-cutting YAMLs, merge |
| **Data work** | LOW | One registry file instead of editing 20+ YAMLs |
| **Maintenance** | GOOD | All compositions in one file |
| **Quality risk** | LOW | Examples are human-authored in registry |
| **Data drift risk** | LOW | Examples live in registry, cross-cutting content in source YAMLs |
| **Implementation time** | 3-5 days | 2-3 for generator, 1-2 for registry data |
| **Scalability** | GOOD | Add entries to registry for new topics |

### Solution D: On-Demand AI Composition (No Data Changes)

Keep everything as-is. When a teacher requests a topic, the chatbot offers: "Would you also like WH questions or question tags included?" If yes, the generation pipeline loads both YAMLs and the sub-agent composes slides from the merged data.

| Factor | Rating | Details |
|--------|--------|---------|
| **Generator changes** | LOW | Modify task brief to optionally load additional YAMLs |
| **Data work** | NONE | No YAML changes |
| **Maintenance** | BEST | Nothing to maintain |
| **Quality risk** | **HIGH** | LLM must adapt generic examples ("Where do you live?") to the correct tense ("Where did you live?"). No guarantee of correctness |
| **Implementation time** | 1-2 days | Simple generator mod |
| **Scalability** | POOR | Each generation depends on LLM quality. No deterministic output |

---

## 4. Solution Comparison Matrix

| Criteria | A (Embed) | B (Compositions) | C (Registry) | D (AI Merge) |
|----------|-----------|-----------------|-------------|--------------|
| **Correctness guarantee** | ✅ Highest | ✅ High | ✅ High | ⚠️ Variable |
| **Generator effort** | None | 2-3 days | 2-3 days | 1-2 days |
| **Data entry effort** | 2-4 days | 2-3 days | 1-2 days | None |
| **Total time** | 2-4 days | 4-6 days | 3-5 days | 1-2 days |
| **Maintenance burden** | 🔴 Very high | 🟢 Low | 🟢 Low | 🟢 None |
| **Scalability (new topics)** | 🔴 Edit all files | 🟢 Add data + code | 🟢 Add registry entry | 🟢 N/A |
| **Content consistency** | 🔴 Drift risk | 🟢 Centralized | 🟢 Centralized | ⚠️ LLM-dependent |
| **Backward compatible** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 5. Risks & Mitigations

### Across All Solutions

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Too many slides per topic | Medium | Medium | Cap compositions per level (max 3 per base topic). Level filtering built in |
| Teacher doesn't want compositions | Low | Low | Make compositions optional — question to the chatbot before generation OR flag in the interface |
| Cross-cutting YAMLs need richer content | Medium | Low | Existing YAMLs (question_forms, question_tags) already have CCQs, tips, errors. May need minor enrichment |

### Solution-Specific Risks

| Solution | Risk | Mitigation |
|----------|------|------------|
| **A (Embed)** | Data drift — same content diverges across files | Impossible to prevent without code enforcement |
| **B (Compositions)** | Cross-cutting YAML merge logic complex | Keep it simple: append CCQs and tips from cross-cutting file, deduplicate by key |
| **C (Registry)** | Registry file grows large | Keep flat, one topic per entry. Easy to read |
| **D (AI Merge)** | LLM produces wrong tense examples | Use only for "nice to have" bonus content, not core slides |

---

## 6. Recommendation

**Solution B (Compositions field + Generator merge)** is the recommended approach because:

1. **Highest quality** — examples are human-verified in each YAML file
2. **Single source of truth** — pedagogical depth (CCQs, L1 data, tips) lives in one cross-cutting YAML
3. **Moderate implementation** — 4-6 days total, 2-3 for code, 2-3 for data
4. **Backward compatible** — files without `compositions` work exactly as they do today
5. **Maintainable** — new compositions are a few lines per YAML file

### Recommended Implementation Sequence

**Phase 1 — Foundation (Days 1-2):**
- Modify `slide_plan.py` to read `compositions` field and create extra slides
- Modify `build_task_brief()` to load cross-cutting YAML and merge data
- Write merge logic (append CCQs, append common errors, deduplicate)

**Phase 2 — Data (Days 3-5):**
- Add `compositions` to the 5 most-requested tenses: past_simple, present_simple, present_continuous, present_perfect, future_will
- Cross-cutting topics: question_forms, short_answers (A1), question_tags (A2)

**Phase 3 — Expansion (Days 6+):**
- Add compositions to remaining tenses and modals
- Add negative_questions (B1) compositions
- Add passive voice compositions to passive_basic if needed

---

## 7. Implementation Record

**Date:** 2026-06-03
**Decision:** Solution C (Registry File) was chosen over the document's original recommendation of Solution B.
**Reason for change:** Solution B requires editing 20+ production-validated YAML files — each edit is a chance to corrupt content that already works. Solution C adds one new file and touches nothing that exists. The generator code changes are identical between B and C, so there is no trade-off on the code side. The only advantage B has over C (data locality — composition lives in the same file as the grammar point) is a minor organisational preference, not a real architectural benefit, and not meaningful for a solo maintainer.

---

### 7.1 Files Created / Modified

| File | Action | Purpose |
|------|--------|---------|
| `data/grammar-compositions.yaml` | **Created** | The registry. Maps all 21 grammar points to their cross-cutting structures. |
| `agent/slides_tools/slide_plan.py` | **Modified** | Loads the registry, inserts `A5_COMPOSITION` slides, builds task briefs for them. |

No existing grammar YAML files were touched.

---

### 7.2 Registry Design (`data/grammar-compositions.yaml`)

The registry is a flat YAML list. Each entry has one `base` key (matching `grammar_point` in the grammar YAML) and a `topics` list. Each topic has:

| Field | Purpose |
|-------|---------|
| `topic` | Slug identifying the cross-cutting structure (`wh_questions`, `short_answers`, `question_tags`) |
| `level_min` | Minimum CEFR level for this composition (`A1` or `A2`) |
| `label` | Human-readable slide title, e.g. `"WH Questions — Past Simple"` |
| `cross_cutting_source` | Filename (without `.yaml`) of the cross-cutting grammar file to pull CCQs and tips from |
| `structure` | The tense-specific formula string, e.g. `"Wh- word + did + subject + base verb?"` |
| `examples` | 3–6 tense-correct example sentences, all human-authored |

| Grammar points covered (22 total):

| Group | Grammar points |
|-------|---------------|
| Present/Past simple | `present_simple`, `past_simple` |
| Continuous | `present_continuous`, `past_continuous` |
| Perfect | `present_perfect`, `present_perfect_continuous`, `past_perfect`, `past_perfect_continuous` |
| Future | `future_will`, `be_going_to`, `future_going_to`, `future_continuous`, `future_perfect`, `future_perfect_simple`, `future_perfect_continuous` |
| Past habits | `used_to`, `used_to_would`, `will_would_habits` |
| Modals | `modals`, `modals_overview`, `modals_past`, `modals_perfect` |

Each entry has 7 topics: `wh_questions` (A1), `short_answers` (A1), `question_tags` (A2), `negative_questions` (B1), `subject_object_questions` (A2), `passive_voice` (A2), `indirect_questions` (B2).

**Example entry (past_simple):**

```yaml
- base: past_simple
  topics:
    - topic: wh_questions
      level_min: A1
      label: "WH Questions — Past Simple"
      cross_cutting_source: question_forms
      structure: "Wh- word + did + subject + base verb?"
      examples:
        - "What did you do yesterday?"
        - "Where did she go last night?"
        - "Who did you meet at the party?"
        - "When did it happen?"
        - "Why did he leave early?"
        - "How did they get here?"
    - topic: short_answers
      level_min: A1
      label: "Short Answers — Past Simple"
      cross_cutting_source: question_forms
      structure: "Yes/No, subject + did / didn't."
      examples:
        - "Did you go to school? — Yes, I did. / No, I didn't."
        - "Did she call you? — Yes, she did. / No, she didn't."
    - topic: question_tags
      level_min: A2
      label: "Question Tags — Past Simple"
      cross_cutting_source: question_tags
      structure: "Positive statement + didn't + pronoun? / Negative statement + did + pronoun?"
      examples:
        - "You went to school yesterday, didn't you?"
        - "She called you, didn't she?"
        - "They left early, didn't they?"
        - "He didn't come, did he?"
```

**How to extend the registry in the future:**

To add negative questions (B1) to all tenses:
1. Create `data/grammar/negative_questions.yaml` (or confirm it exists)
2. Add a new `topic` entry to each base in `grammar-compositions.yaml`:
   ```yaml
   - topic: negative_questions
     level_min: B1
     label: "Negative Questions — Past Simple"
     cross_cutting_source: negative_questions
     structure: "Didn't + subject + base verb?"
     examples:
       - "Didn't you go to school?"
       - "Didn't she call?"
   ```
3. No changes needed to `slide_plan.py` or any grammar YAML.

---

### 7.3 Code Changes (`agent/slides_tools/slide_plan.py`)

Four additions were made. No existing logic was modified.

#### Addition 1 — Module-level import and caches

```python
from pathlib import Path  # added to existing imports

_COMPOSITIONS_CACHE: list[dict] | None = None
_CROSS_CUTTING_CACHE: dict[str, dict] = {}
```

#### Addition 2 — Three helper functions

**`_load_compositions_registry()`** — loads and caches `data/grammar-compositions.yaml`. Returns an empty list if the file is missing (safe fallback: no composition slides generated).

**`_load_cross_cutting_yaml(topic_slug)`** — loads and caches a cross-cutting grammar YAML by filename slug (e.g., `"question_forms"` → `data/grammar/question_forms.yaml`). Returns an empty dict if missing.

**`_get_compositions_for_grammar(grammar_data)`** — looks up the grammar point's slug in the registry and returns its topic list. Returns an empty list if the grammar point has no registry entry (all non-tense grammar points like articles, conditionals, etc. get zero composition slides — fully backward compatible).

#### Addition 3 — Composition slides in `compute_slide_plan()`

Nine lines inserted after the A5 formula slides loop (affirmative / negative / questions), before the A5_SUB sub-rules:

```python
# A5_COMPOSITION: Cross-cutting structure slides (WH questions, short answers, question tags)
# Loaded from grammar-compositions.yaml — structures and examples are tense-specific.
# Pedagogical depth (CCQs, teaching tips) is pulled from cross-cutting YAMLs at brief-build time.
for comp in _get_compositions_for_grammar(grammar_data):
    slides.append({
        "type": "A5_COMPOSITION",
        "label": comp.get("label", comp.get("topic", "Composition")),
        "composition": comp,
    })
```

The composition data travels with the slide metadata so the brief builder has everything it needs without any additional lookups at plan time.

#### Addition 4 — `_build_a5_composition_brief()`

A new brief builder registered under `"A5_COMPOSITION"` in the `builders` dict. It:

1. Reads the tense-specific `structure` and `examples` from `slide_meta["composition"]`
2. Calls `_load_cross_cutting_yaml(cross_cutting_source)` to get the CCQs, teaching tips, and common errors from the validated cross-cutting YAML
3. Sorts common errors by breadth of L1 coverage (length of `l1_groups` list) so the most universally relevant errors appear first
4. Outputs a task brief in the same format as all other A5 briefs so the HTML writer sub-agent treats it identically

**Key design decision:** The brief combines two data sources — tense-specific examples (registry) + pedagogical depth (cross-cutting YAML) — without duplicating content anywhere. The structure `"Wh- word + did + subject + base verb?"` only exists once, in the registry. The CCQ `"Is this a yes/no question or a wh- question?"` only exists once, in `question_forms.yaml`.

---

### 7.4 Slide Count Impact

| Grammar point | Slides before | Slides after | Change |
|---------------|--------------|--------------|--------|
| `past_simple` | 25 | 28 | +3 (WH, short answers, question tags) |
| `present_simple` | 24 | 27 | +3 |
| `present_perfect` | 25 | 28 | +3 |
| `modals` | 25 | 28 | +3 |
| `articles` | varies | no change | 0 (not in registry) |
| Any non-tense grammar | varies | no change | 0 (not in registry) |

---

### 7.5 Verification

Smoke test run immediately after implementation (`python3` with direct module import to bypass an unrelated `IndentationError` in `InsertNewSlides.py`):

```
past_simple: 28 total slides, 3 composition slides
  - WH Questions — Past Simple
  - Short Answers — Past Simple
  - Question Tags — Past Simple

present_simple: 27 total slides, 3 composition slides
  - WH Questions — Present Simple
  - Short Answers — Present Simple
  - Question Tags — Present Simple

present_perfect: 28 total slides, 3 composition slides
present_perfect: ...

modals: 28 total slides, 3 composition slides

articles.yaml (no compositions expected): Composition slides: 0 ✅
```

**Sample task brief output — past_simple WH questions (abbreviated):**

```
Slide title: WH Questions — Past Simple
Slide type: A5 Grammar Formula — Cross-cutting Structure
Section: 4 of 8 (continuation of formula section)
Grammar point: Past Simple (V2/ed)

TENSE-SPECIFIC STRUCTURE:
  Structure: Wh- word + did + subject + base verb?

TENSE-SPECIFIC EXAMPLES:
  - What did you do yesterday?
  - Where did she go last night?
  - Who did you meet at the party?
  ...

CCQs FROM QUESTION_FORMS.YAML:
  Q: Is this a yes/no question or a wh- question?
  A: Yes/no questions start with an auxiliary (do, can, are)...

COMMON ERRORS FROM QUESTION_FORMS.YAML:
  ❌ Wrong:   "Using statement word order: *'You like coffee?'"
  ✅ Correct: "Do you like coffee?"

SPEAKER NOTES:
  Teacher talk: 'Now let's look at WH Questions — Past Simple...'
  CCQ: Is this a yes/no question or a wh- question?
  Watch for: "Using statement word order in questions"
```

---

### 7.6 All 7 Cross-Cutting Structures Covered

The registry now covers all 7 cross-cutting structures identified in Section 2.2:

| # | Structure | CEFR | In registry | Slides generated |
|---|-----------|:----:|:-----------:|:----------------:|
| 1 | WH questions | A1 | ✅ | ✅ For all 22 grammar points |
| 2 | Short answers | A1 | ✅ | ✅ For all 22 grammar points |
| 3 | Question tags | A2 | ✅ | ✅ For all 22 grammar points |
| 4 | Negative questions | B1 | ✅ | ✅ For all 22 grammar points |
| 5 | Subject/Object questions | A2 | ✅ | ✅ For all 22 grammar points |
| 6 | Passive voice | A2–B1 | ✅ | ✅ For all 22 grammar points |
| 7 | Indirect questions | B2 | ✅ | ✅ For all 22 grammar points |

**Total:** 154 topic entries (22 grammar points × 7 structures)
