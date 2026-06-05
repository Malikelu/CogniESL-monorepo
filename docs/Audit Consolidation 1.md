# CogniESL — Audit Consolidation 1

**Date:** 2026-06-04
**Sources consolidated:** `AUDIT_REPORT_2026-06-04.md` (Report A) + `INDEPENDENT_AUDIT_2026-06-04.md` (Report B)
**Method:** Both reports were written as independent source-code-level audits. This consolidation cross-references every finding, verifies agreements/disagreements against the actual source code and YAML data, and produces a single unified report with a sequenced execution plan.

---

## Part 1: Cross-Reference Matrix

Every finding from both reports, verified against source code and YAML data.

### Critical (broken deliverables, zero data reaches output)

| ID | Finding | Report A | Report B | Verdict |
|----|---------|----------|----------|---------|
| C1 | **L1 data never reaches any consumer** — `GetL1InterferenceTool.run()` wraps all interference data inside a `data` key (`{"language":..., "data": {interference_patterns, why_it_happens, ...}}`), but every consumer reads `interference_patterns`, `why_it_happens`, `teacher_tips` from the top level. **L1 Oracle slides receive zero interference data.** | ❌ Missed | ✅ Found (§1.1) | **Confirmed.** Reproduced by direct code trace: `_load_yaml_data` appends the raw tool result to `l1_data_list` without unwrapping `data`. All consumers (`_pick_tier1_2_patterns` line 312, `_build_a6_brief` lines 975-977, `_build_worksheet_html` line 343, `QueueGenerationJob` step 9 line 747) read from top level and get `None`/`""`/`[]`. The L1 Oracle — the product's stated unique value proposition — is silently hollow. |
| C2 | **Worksheet `common_errors` key mismatch** — `_build_worksheet_html` reads `err.get("wrong")` / `err.get("correct")` but YAML uses `error` / `correction`. Sections A, B, and Answer Key are empty. | ✅ Found (F1) | ✅ Found (§1.2) | **Confirmed.** Both reports independently verified against `present_simple.yaml` and `present_perfect.yaml`. Reproduced: Section A = 4 empty `<li>`, Section B = 0 items, Answer Key = 0 items. Slide builders (`slide_plan.py`) handle this correctly; only the worksheet builder omits the `error`/`correction` fallbacks. |

### High (degraded output, architectural defects, production risks)

| ID | Finding | Report A | Report B | Verdict |
|----|---------|----------|----------|---------|
| H1 | **Proficiency level discarded** — `QueueGenerationJob` has no `level` Pydantic field. `getattr(self, "level", None)` always returns `None` → hardcoded `"b1"`. Level is never threaded into `compute_slide_plan` or `build_all_task_briefs`. Cache key always uses `"b1"`. | ❌ Missed | ✅ Found (§1.4) | **Confirmed.** A1 student gets B1 materials. Cache serves wrong level to wrong request. Contradicts CLAUDE.md requirement that level drives slide planning. |
| H2 | **3 inconsistent `mnt` path resolutions** — `COGNIESL_DATA_DIR` fallback chains differ across writers and readers. If the env var is unset on Railway: writers put files in `/app/data/mnt` (because `/app/data` exists as a dir), web readers look in `/app/mnt` (fallback to `Path(__file__).parent`) → all downloads/slides 404. Also blocks Master Repository cache writes. | ❌ Missed | ✅ Found (§1.7-A, §1.7-C) | **Confirmed.** Three resolution patterns verified in source: (1) `slide_file_utils.get_mnt_dir()` = 3-tier (env → `/app/data` if exists → repo root), (2) `server.py` web endpoints = 2-tier (env → repo root, NO `/app/data`), (3) `server.py` DB/recovery = 2-tier (env → `/app/data`, NO repo root). They diverge when env var unset. |
| H3 | **"Watch for" speaker notes empty in A5/A7/A8 task briefs** — three task brief builders have "Watch for:" lines that use `err.get("wrong", err.get("example_wrong", ""))` without `error` in the chain. YAML uses `error` → empty strings. | ✅ Found (F15) | ❌ Not mentioned | **Confirmed.** Code-verified at `_build_a5_brief` line 751, `_build_a7_gap_fill_brief` line 1099, `_build_a8_brief` line 1157. |
| H4 | **"error" field contains verbose descriptions** — grammar YAML `error` values like `"Omitting third person -s: *'She walk to school.'"` are descriptive labels, not clean wrong sentences. Task brief builders that include `error` in their fallback chain pass these contaminated strings to the HTML writer model. | ✅ Found (F14) | ❌ Not mentioned | **Confirmed** against `present_simple.yaml`. The `error` field is a label, not a sentence. |

### Medium (degraded experience, fix-soon)

| ID | Finding | Report A | Report B | Verdict |
|----|---------|----------|----------|---------|
| M1 | **Slide batches are sequential** — `_run_slide_batches` awaits each coroutine individually in a `for` loop. No `asyncio.gather`. `BATCH_SIZE=3` is cosmetic. ~3× slowdown. | ✅ Found (F2) | ✅ Found (§1.3) | **Confirmed.** Both reports independently verified. Additionally: per-slide 3s sleep + inter-batch 5s sleep = ~150s of pure sleeping for a 32-slide deck. |
| M2 | **Post-write retry discards context** — when a slide is too thin (<4000 bytes), retry sets `previous_failed_html=None`, so the model never sees what it generated and likely repeats mistakes. | ✅ Found (F7) | ❌ Not mentioned | **Confirmed.** `ModifySlide.py:713-775`. |
| M3 | **Literal "[L1]" in worksheet** — Section C header hardcodes the text `[L1]` instead of substituting the actual language name. | ✅ Found (F13) | ✅ Mentioned (§1.2 secondary) | **Confirmed.** `QueueGenerationJob.py:393`. |
| M4 | **Email labels collision** — all pipeline docs are `.source.html` files. `email_sender._label_for_file` checks `.pdf`/`.docx` before `.html`, but worksheet/activity/flashcard HTML files don't match the `.pdf`/`.docx` branches. All render as "Download Presentation." Teacher can't tell files apart. | ❌ Missed | ✅ Found (§1.7-B) | **Confirmed.** `_label_for_file` lines 175-189: `.pdf`/`.docx` branches match "worksheet"/"activity" substrings but require `.pdf`/`.docx` extension. All pipeline files end in `.source.html` → fall through to generic HTML label. |
| M5 | **Fallback slides bypass validation** — `_generate_minimal_html_fallback()` writes ~1.5KB white slides directly to disk, unvalidated, skipping Playwright checks that real slides must pass. Acceptable as safety net, but "no blank slides" ≠ "no empty slides." | ✅ Mentioned (F7 context) | ✅ Found (§1.6a) | **Confirmed.** Both agree on the finding; Report B states it more forcefully. |
| M6 | **Two model routing systems** — main agent uses `LitellmModel` wrapper; sub-agents use direct `AsyncOpenAI`. Different error handling, retry logic, thinking-mode configuration. | ✅ Found (F4) | ❌ Not mentioned | **Confirmed.** `config.py` vs `ModifySlide.py`/`InsertNewSlides.py`. |
| M7 | **No YAML schema validation** — no enforced contract between data producers and consumers. Multi-level fallback chains are the symptom. | ✅ Found (F9) | ❌ Separate finding but addressed via fixes | **Confirmed.** Root cause behind C2, H3, H4, and the duplicate fallback chains finding. |
| M8 | **Duplicate field-name fallback chains** — the `err.get("error", err.get("wrong", ...)` pattern is copy-pasted to 10 locations with 3 inconsistent variations. | ✅ Found (F17) | ❌ Not mentioned | **Confirmed.** Mapped in detail in Report A. |
| M9 | **Email in Resend sandbox** — `from` defaults to `onboarding@resend.dev`, only delivers to account owner. | ❌ Not listed as finding | ✅ Found (§1.6b) | **Confirmed.** Needs verified domain + `COGNIESL_FROM_EMAIL`. |

### Low (code quality, maintenance, unlikely-to-bite)

| ID | Finding | Report A | Report B | Verdict |
|----|---------|----------|----------|---------|
| L1 | **Font pairing selects unmatched combinations** — `random.choice(_FONT_PAIRS)[0]` and `random.choice(_FONT_PAIRS)[1]` are independent calls. | ✅ Found (F6) | ❌ Not mentioned | **Confirmed.** |
| L2 | **Duplicate model client code** — `_make_deepseek_client` and `_call_deepseek` in both `ModifySlide.py` and `InsertNewSlides.py`. | ✅ Found (F3) | ❌ Not mentioned | **Confirmed.** |
| L3 | **Substring matching in L1 filter** — `any(l1 in l1_groups_str for l1 in l1_list)` could match "Russian" in "Prussian". | ✅ Found (F8) | ❌ Not mentioned | **Confirmed** but unlikely to bite with 36-language dataset. |
| L4 | **Theme failure silently ignored** — pipeline continues without theme CSS if `theme_generator` raises. | ✅ Found (F10) | ❌ Not mentioned | **Confirmed.** Design choice is reasonable (don't block on non-critical), but fallback is empty string. |
| L5 | **Daemon threads lose mid-generation work** — `daemon=True` on generation thread. No checkpointing for resume. | ✅ Found (F5) | ❌ Not mentioned | **Confirmed.** Recovery logic handles it "best effort" but can't resume. |
| L6 | **Kickoff detection fragility** — 30 hardcoded keyword strings to detect when the agent sends a "holding message" instead of calling tools. | ✅ Found (F16) | ❌ Not mentioned | **Confirmed.** Blacklist approach to LLM behavioral problem. |
| L7 | **Stale slide files from previous runs** — `_list_slide_filenames` may include leftover files. | ✅ Found (F12) | ❌ Not mentioned | **Confirmed.** Presentation dir not cleaned before generation. |
| L8 | **Missing deliverables** — progress tracker PDF generator exists but is never called by pipeline. Homework/quiz absent from pipeline. | ✅ Found (F11) | ✅ Found (§1.6d) | **Confirmed.** Both agree. |
| L9 | **Downloads allowed while job "running"** — `/download`, `/bundle.html`, `/slides` viewer accept `status == "running"`. Teacher can fetch half-generated materials. | ❌ Not mentioned | ✅ Found (§1.7-E) | **Confirmed.** |
| L10 | **`thin_briefs` index-vs-count comparison** — `k != slide_count` works by accident for last slide only. Fragile. | ❌ Not mentioned | ✅ Found (§1.6c) | **Confirmed** but low impact. |
| L11 | **Bundle is 113–126 MB** — all images base64-inlined into one HTML. Risk of Railway response timeouts / egress limits. | ❌ Not mentioned | ✅ Found (§1.7-D) | **Confirmed** (concern, not logic bug). |

---

## Part 2: Where the Reports Disagreed

### Claim: "Report A said slides are parallel"

**Report B §2:** "❌ 'Slides generated in parallel via `asyncio.gather` (batch 3).' — **False.**"

**Verdict:** Report B is criticizing a **prior version** of `AUDIT_REPORT_2026-06-04.md`, not Report A. Report A Finding 2 explicitly states: **"Slide Batches Are Sequential, Not Parallel"** and identifies the individual `await` loop as the root cause. Both reports agree slides are sequential. No conflict.

### Claim: "Report A said worksheet data loads correctly"

**Report B §2:** "❌ Worksheet cause given as 'data isn't being inserted… YAML loads correctly (verified by the activity guide which DOES contain content from the same data).'"

**Verdict:** Same as above — this criticism targets a prior report, not Report A. Report A Finding 1 identifies the exact key mismatch (`error`/`correction` vs `wrong`/`correct`). Both reports agree on the root cause. No conflict.

### Claim: "Report A marked L1 Oracle as passing"

**Report B §2:** "❌ L1 Oracle marked as passing in the validation checklist."

**Verdict:** Report A's "What the Pipeline Gets Right" section never mentions L1 Oracle as passing. Report A did not include a validation checklist. This criticism targets the prior report. **However**, Report A did miss the L1 data nesting bug (C1), which means Report A's analysis of L1 Oracle content was incomplete. Report B correctly identified the structural defect. **Report B is right that the L1 Oracle was broken; Report A is the one that missed it.**

---

## Part 3: Root Cause Map

Findings C1, C2, H3, H4, M8 all trace to a single structural defect:

```
                    ┌──────────────────────────────────┐
                    │  No enforced YAML data contract   │
                    │  (no Pydantic schema, no normalize │
                    │   at load time, no shared accessor) │
                    └──────────┬───────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
  ┌───────────────┐   ┌──────────────┐   ┌──────────────────┐
  │ Field name    │   │ Nested shape │   │ Value format     │
  │ mismatch      │   │ mismatch     │   │ mismatch         │
  │ (error/wrong) │   │ (data{} key) │   │ (labels vs clean │
  └───┬───────────┘   └──┬───────────┘   │ sentences)       │
      │                  │               └──┬───────────────┘
      ▼                  ▼                  ▼
  C2: Worksheet      C1: L1 Oracle      H4: Contaminated
  empty Sections     gets 0 patterns    task brief values
  A, B, Answer Key   (value prop is
                      silently hollow)
      │                  │
      ▼                  ▼
  H3: "Watch for"    M3: Literal "[L1]"
  lines empty        in worksheet output
```

Findings H1, H2 are independent structural defects (missing field, divergent path resolution).

---

## Part 4: Verified Execution Plan

Ordered by impact × ease-of-fix. Each step is independently verifiable.

### Phase 1: Restore Broken Outputs (estimated: 2-3 hours)

**Step 1 — Fix C1: Unwrap L1 `data` in `_load_yaml_data`**

File: `agent/slides_tools/QueueGenerationJob.py`, function `_load_yaml_data` (line 296)

```python
# BEFORE (line 295-297):
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict):
    l1_data_list.append(result)

# AFTER:
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict) and "data" in result and isinstance(result["data"], dict):
    # Unwrap: GetL1InterferenceTool returns {language, grammar_point, data: {...}}
    # Consumers expect flattened shape with interference_patterns at top level.
    merged = {**result["data"], "language": result.get("language", l1),
              "grammar_point": result.get("grammar_point", gram_slug)}
    l1_data_list.append(merged)
elif isinstance(result, dict):
    l1_data_list.append(result)  # already-flat or error dict
```

**Verify:** Generate Present Simple + Spanish. Inspect L1 Oracle slide — should contain specific Spanish interference patterns (e.g., "She walk" → "She walks") from the YAML, not generic LLM-invented content. Worksheet Section C should have L1 patterns (once C2 is also fixed).

**Step 2 — Fix C2: Add `error`/`correction` to worksheet fallback chains**

File: `agent/slides_tools/QueueGenerationJob.py`, function `_build_worksheet_html`

Lines 371-372 (Section A):
```python
# BEFORE:
wrong = _s(err.get("wrong", err.get("example_wrong", "")))
correct = _s(err.get("correct", err.get("example_correct", "")))
# AFTER:
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

Lines 383-384 (Section B): same change.

Line 413 (Answer Key):
```python
# BEFORE:
correct = _s(err.get("correct", err.get("example_correct", "")))
# AFTER:
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

**Verify:** Regenerate worksheet. Section A should show 4 gap-fill items with real sentences. Section B should show 4 error-correction pairs. Answer Key should list 8 correct answers.

**Step 3 — Fix M3: Replace literal `[L1]` with actual language name**

File: `agent/slides_tools/QueueGenerationJob.py`, line 393

```python
# BEFORE:
html_parts.append("<p>Fix these sentences that [L1] speakers often get wrong.</p>")
# AFTER:
l1_display = l1_languages if l1_languages else "some"
html_parts.append(f"<p>Fix these sentences that {l1_display} speakers often get wrong.</p>")
```

**Verify:** Worksheet Section C header should say "Fix these sentences that Spanish speakers often get wrong."

### Phase 2: Fix Structural Defects (estimated: 3-4 hours)

**Step 4 — Add YAML schema validation + shared accessor**

Create `agent/data_schema.py`:
```python
from pydantic import BaseModel

class CommonError(BaseModel):
    error: str = ""
    correction: str = ""
    wrong: str = ""   # normalize to this after load
    correct: str = "" # normalize to this after load
    explanation: str = ""
    l1_groups: list[str] = []

    @classmethod
    def from_yaml_entry(cls, entry: dict) -> "CommonError":
        """Normalize regardless of source field naming convention."""
        wrong = str(entry.get("error") or entry.get("wrong") or entry.get("example_wrong") or "")
        correct = str(entry.get("correction") or entry.get("correct") or entry.get("example_correct") or "")
        return cls(
            error=wrong,
            correction=correct,
            wrong=wrong,
            correct=correct,
            explanation=str(entry.get("explanation", "")),
            l1_groups=entry.get("l1_groups") or [],
        )
```

Add a shared accessor function that every consumer imports:
```python
def get_error_pair(err: dict) -> tuple[str, str]:
    """Extract (wrong, correct) from a common_errors entry.
    Works regardless of whether the YAML used error/correction or wrong/correct."""
    wrong = str(err.get("error") or err.get("wrong") or err.get("example_wrong") or "")
    correct = str(err.get("correction") or err.get("correct") or err.get("example_correct") or "")
    return wrong, correct
```

Replace ALL 10 fallback chain sites in `slide_plan.py` and `QueueGenerationJob.py` with calls to `get_error_pair()`. This eliminates Findings M8, H3, and prevents future C2-class bugs.

**Verify:** Run existing tests. All task brief builders and worksheet builder should produce identical or better output. No regressions.

**Step 5 — Fix H1: Thread `level` through pipeline**

a) Add `level` field to `QueueGenerationJob`:
```python
level: str = Field(
    default="B1",
    description="Proficiency level (A1, A2, B1, B2, C1)",
)
```

b) Replace `getattr(self, "level", None) or "b1"` with `self.level.lower()`.

c) Pass `level` to `compute_slide_plan(grammar_data, l1_languages, age_group, level)` and `build_all_task_briefs(...)`. Update those function signatures.

d) Replace hardcoded `"Level: B1"` in task briefs with the actual level.

**Verify:** Generate a deck with level="A1". Cache key should contain "a1". Task briefs should contain "Level: A1".

**Step 6 — Fix H2: Unify `mnt` path resolution**

a) Export `slide_file_utils.get_mnt_dir()` as the single source of truth.

b) In `server.py`: replace all 5 direct `COGNIESL_DATA_DIR` → Path constructions with `get_mnt_dir()`.

c) In `doc_file_utils` and flashcard/progress tracker tools: replace local path resolution with `get_mnt_dir()`.

d) Delete the 2 divergent copies of the resolution logic.

e) In `MarkJobComplete`: resolve the bundle path via `get_mnt_dir()` (absolute) before the existence check for cache writes.

**Verify:** On Railway, run generation. Confirm `get_mnt_dir()` returns the same path from writers and readers. Confirm cache `add_to_cache` executes. Confirm downloads work.

### Phase 3: Performance + Quality (estimated: 2-3 hours)

**Step 7 — Fix M1: True parallel batches**

File: `agent/slides_tools/QueueGenerationJob.py`, `_run_slide_batches`

```python
# BEFORE:
for t_idx, task in enumerate(tasks):
    await asyncio.wait_for(task, timeout=120)

# AFTER:
results = await asyncio.gather(
    *[asyncio.wait_for(t, timeout=120) for t in tasks],
    return_exceptions=True
)
for t_idx, result in enumerate(results):
    filename = batch[t_idx]
    if isinstance(result, asyncio.TimeoutError):
        logger.error(f"TIMEOUT for {filename}")
    elif isinstance(result, Exception):
        logger.error(f"ERROR on {filename}: {result}")
```

Consider dropping or reducing the per-slide 3s throttle (`SLIDE_GENERATION_DELAY`). DeepSeek has 2500 RPM concurrency headroom. Keep a small inter-batch delay (1-2s) only if rate limits are hit.

**Verify:** Time a 30-slide deck before and after. Slide phase should drop ~3×.

**Step 8 — Fix M2: Show model its own failed output on retry**

File: `agent/slides_tools/ModifySlide.py`, post-write size check retry (line ~720)

```python
_pw_prompt = _build_sub_run_prompt(
    ...
    retry_validation_error="Slide content is too thin. Add more examples, visual elements, and detailed speaker notes.",
    previous_failed_html=final_html,  # ← was None
)
```

**Step 9 — Fix M4: Email labels**

File: `agent/email_sender.py`, `_label_for_file`

Add checks for `.source.html` files with content-type substrings before the generic `.html` fallback:
```python
if "worksheet" in name:
    return ("Download Worksheet", "📝")
if "activity" in name:
    return ("Download Activity Guide", "📋")
if "flashcard" in name:
    return ("Download Flashcards", "🃏")
if name.endswith(".html"):
    return ("Download Presentation", "🎬")
```

**Verify:** Email notification for a full generation should show distinct labels for worksheet, activity guide, flashcards, and presentation.

### Phase 4: Polish (estimated: 1-2 hours)

**Step 10 — Fix L1:** Font pairing — change `theme_generator.py:296-297` to select from a single pair.

**Step 11 — Fix L3:** Use set intersection for L1 language matching instead of substring.

**Step 12 — Fix L7:** Clean `slide_*.html` files in presentation dir before creating blank placeholders.

**Step 13 — Fix M9:** Configure verified domain for Resend (`COGNIESL_FROM_EMAIL`).

**Step 14 — Fix L9:** Gate downloads on `status == "done"` only.

### Deferred / Monitor

| Item | Reason |
|------|--------|
| L2: Duplicate model client code | Code quality, no functional impact. Refactor when touching those files. |
| L4: Theme failure silently ignored | Design choice. Add fallback palette if visual cohesion issues observed. |
| L5: Daemon thread checkpointing | Current best-effort recovery works. Add checkpointing after Phase 4. |
| L6: Kickoff detection fragility | Use structural detection (response length + tool call check) instead of blacklist. Do during next round of prompt tuning. |
| L8: Progress tracker / homework / quiz | Feature gap, not a bug. Prioritize with product roadmap. |
| L10: `thin_briefs` comparison | Harmless but fragile. Fix alongside next refactor. |
| L11: 124 MB bundle | Consider splitting or serving as zip. Monitor for Railway timeout/e ingress issues. |
| M6: Dual model routing | Standardize on direct AsyncOpenAI. Do alongside L2 refactor. |

---

## Part 5: Confidence Summary

| ID | Finding | Confidence | How Verified |
|----|---------|-----------|--------------|
| C1 | L1 data nesting — zero interference data reaches consumers | **Very High** | Source code trace: GetL1InterferenceTool return shape → _load_yaml_data append → consumer .get() calls. Reproduced against real YAML. |
| C2 | Worksheet key mismatch — empty Sections A/B/Answer Key | **Very High** | Source code trace + grep of YAML field names. Reproduced with present_simple.yaml. |
| H1 | Proficiency level discarded — hardcoded B1 | **Very High** | Pydantic model has no `level` field → `getattr` always None → `"b1"`. Deterministic. |
| H2 | 3-way path resolution mismatch | **Very High** | Source code trace in 3 files. Determined by env var state. |
| H3 | "Watch for" lines empty | **Very High** | Missing `error` in 3 specific fallback chains. YAML grep confirmed. |
| H4 | "error" field is verbose descriptions | **Very High** | YAML inspection of present_simple.yaml. |
| M1 | Sequential slide batches | **Very High** | Source code: for-loop await. No `gather` anywhere in file. Deterministic. |
| M2 | Post-write retry discards context | **Very High** | `previous_failed_html=None` in retry prompt construction. |
| M3 | Literal "[L1]" in worksheet | **Very High** | Hardcoded string, no replacement logic. |
| M4 | Email labels collision | **Very High** | `_label_for_file` branch order: `.pdf`/`.docx` before `.html`, but all pipeline files are `.source.html`. |
| Remaining low-severity items | All | **High** | Source code read, deterministic. |

---

## Part 6: What the Pipeline Gets Right

Despite the findings above, the architecture has strong fundamentals:

- **10-step pipeline** covers all deliverable types end-to-end
- **Crash recovery** best-effort handles restarts (partial slide detection)
- **Theme system** provides visual cohesion without LLM calls
- **Playwright validation** is thorough (dimensions, overflow, text wrapping, speaker notes, descender clipping)
- **Post-write size check** catches thin slides that pass structural validation
- **Progress logging** (`_write_progress`) provides crash debugging
- **Master Repository cache** structure exists (just needs path fix to populate)
- **302 grammar + 36 L1 + 220 activity YAML files** — rich, pre-validated database

The findings are concentrated in the glue code between data and consumers — not in the architecture. The system is closer to production-ready than the bug count suggests, because the fixes are surgical and share common root causes.
