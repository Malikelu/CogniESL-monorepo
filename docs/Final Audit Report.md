# CogniESL — Final Audit Report & Execution Plan

**Date:** 2026-06-04
**Sources:** Three-layer consolidation.

| Layer | Documents | Role |
|-------|-----------|------|
| 1 | `AUDIT_REPORT_2026-06-04.md`, `INDEPENDENT_AUDIT_2026-06-04.md` | Independent source-code audits |
| 2 | `Audit Consolidation 1.md`, `Audit Consolidation 2.md` | Independent consolidations of Layer 1 |
| 3 | This document | Final reconciliation of Layer 2 |

**Method:** Every finding was verified against actual source code and YAML data. No finding is included here that wasn't traced to a specific line number.

---

## 1. Complete Finding Inventory

26 verified findings, deduplicated and renumbered.

### CRITICAL (broken deliverables — fix immediately)

| ID | Finding | Root Cause | Source |
|----|---------|-----------|--------|
| **F1** | **L1 Oracle slides contain zero real interference data.** `GetL1InterferenceTool.run()` returns `{language, grammar_point, data: {interference_patterns, why_it_happens, ...}}` but `_load_yaml_data` appends the raw result to `l1_data_list` without unwrapping `data`. All consumers read `interference_patterns`, `why_it_happens`, `teacher_tips` from the top level — where they don't exist. The model silently invents L1 content, violating CLAUDE.md's "database is sacred" rule. Affects L1 Oracle slides, worksheet Section C, and flashcards. | Nested dict not unwrapped at load boundary | Independent |
| **F2** | **Worksheet Sections A, B, and Answer Key are always empty.** `_build_worksheet_html()` reads `err.get("wrong")` / `err.get("correct")` but grammar YAML uses `error` / `correction`. Slide builders handle this correctly with multi-level fallback; only the worksheet builder omits `error`/`correction`. Reproduced: Section A = 4 empty `<li>`, Section B = 0 items, Answer Key = 0 items. | Missing keys in `.get()` fallback chain | Both |

### HIGH (degraded output, architectural defects, production risk)

| ID | Finding | Root Cause | Source |
|----|---------|-----------|--------|
| **F3** | **Slide generation is fully sequential, not parallel.** `_run_slide_batches()` builds coroutines then awaits each individually in a `for` loop. No `asyncio.gather` anywhere in the file. `BATCH_SIZE=3` is cosmetic — it only changes how often the inter-batch `sleep` fires. Plus per-slide 3s sleep + inter-batch 5s sleep = ~150s of pure idle time for a 32-slide deck. ~3× slower than it should be. | Individual `await` loop instead of `asyncio.gather` | Both |
| **F4** | **Proficiency level silently discarded — every deck is B1.** `QueueGenerationJob` has no `level` Pydantic field. `getattr(self, "level", None)` always returns `None` → hardcoded `"b1"`. Level is never threaded into `compute_slide_plan`, `build_all_task_briefs`, or the cache key. Task briefs hardcode `"Level: B1"`. A1 student gets B1 materials. Cache serves wrong level to wrong request. | Missing Pydantic field + no parameter threading | Independent |
| **F5** | **Three inconsistent `mnt` path resolution fallbacks.** Writers use 3-tier (env → `/app/data` if exists → repo root). Web readers use 2-tier (env → repo root, no `/app/data`). DB/recovery uses 2-tier (env → `/app/data`, no repo root). If `COGNIESL_DATA_DIR` is unset on Railway: writers put files in `/app/data/mnt`, web readers look in `/app/mnt` → all downloads/slides 404. Also silently blocks Master Repository cache writes (`Path.exists()` on relative path always False on Railway). | 3 divergent implementations of same logic | Independent |
| **F6** | **No YAML schema validation — silent data loss is structural.** Field names vary across YAML files (`error`/`correction` vs `wrong`/`correct` vs `example_wrong`/`example_correct`). Consumers use multi-level fallback chains, but not all chains include all variants. No warning when expected data is not found. This is the root cause behind F2, F14, F15, and the duplicate fallback chains. | No enforced data contract | Prior |
| **F7** | **"Watch for" speaker notes empty in A5/A7/A8 task briefs.** Three builders have "Watch for:" lines that use `err.get("wrong", err.get("example_wrong", ""))` without `error` in the chain. The "Watch for" chain was written before `error` was added to the main extraction chain. | Inconsistent fallback: main extraction has `error`, "Watch for" doesn't | Prior |
| **F8** | **"error" field values are verbose descriptions, not clean sentences.** YAML `error` values like `"Omitting third person -s: *'She walk to school.'"` are labels, not clean wrong sentences. Slide builders that include `error` in their fallback pass these contaminated strings to the HTML writer model. The model must parse out the actual sentence — some will succeed, others will produce garbled output. | YAML field stores label + example in one string | Prior |
| **F9** | **Post-write retry discards validation context.** When a slide passes structural validation but is too thin (<4000 bytes), the retry prompt sets `previous_failed_html=None`. The model never sees what it generated, so it can't fix specific problems — it regenerates blind and likely repeats the same mistakes. | `None` instead of `final_html` in retry prompt | Prior |
| **F10** | **Two incompatible model routing systems.** Main agent uses `LitellmModel` wrapper (via `config.py`); sub-agents use direct `AsyncOpenAI`. Different error handling, retry logic, and thinking-mode configuration. No shared client factory. | Two separate code paths for same API | Prior |
| **F11** | **Daemon threads lose mid-generation work on restart.** Generation thread created with `daemon=True`. On Railway auto-deploy or server restart, the thread is killed without warning. Recovery logic can only classify jobs as "done" or "error" — it can't resume. A job with 28/32 slides complete is either shipped partial or reported as error (teacher gets nothing). | No checkpointing; `daemon=True` | Prior |
| **F12** | **Master Repository cache never populated.** `MarkJobComplete` sets `_primary_path` to a relative `./mnt/...` string. `Path(_primary_path).exists()` resolves against cwd. On Railway (cwd `/app`, files at `/app/data/mnt`) it's always `False` → `add_to_cache` never runs. This matches the standing note that "sync to Master Repository has never run." | Relative path vs. absolute expectation (same root as F5) | Independent |

### MEDIUM (degraded experience — fix soon)

| ID | Finding | Root Cause | Source |
|----|---------|-----------|--------|
| **F13** | **Literal "[L1]" in worksheet output.** Section C header hardcodes the string `[L1]` instead of substituting the actual language name. Every worksheet says "Fix these sentences that [L1] speakers often get wrong." | Hardcoded placeholder with no replacement logic | Both |
| **F14** | **All email deliverables labeled identically.** All pipeline docs are `.source.html` files. `email_sender._label_for_file` checks `.pdf`/`.docx` before `.html` — but the `.pdf`/`.docx` branches require those extensions, which never match. All files fall to the generic `.html` label: "Download Presentation." Teacher sees 3-4 identical buttons. | Branch order: `.pdf`/`.docx` before `.html` but files are `.source.html` | Independent |
| **F15** | **Fallback slides bypass validation.** `_generate_minimal_html_fallback()` writes ~1.5KB white slides directly to disk, unvalidated. They lack Font Awesome, visual content, and the structure that real slides must pass. Acceptable as a safety net, but "no blank slides" ≠ "no empty slides." | Fallback bypasses Playwright validation | Both |
| **F16** | **Email in Resend sandbox.** `from` defaults to `onboarding@resend.dev`, which can only deliver to the account owner. Non-Marcos teachers never receive completion emails. | Resend sandbox mode; no verified domain | Both |
| **F17** | **Duplicate field-name fallback chains.** The `err.get("error", err.get("wrong", err.get("example_wrong", ""))` pattern is copy-pasted to 10 locations in 3 files with 3 inconsistent variations. This duplication made F2 inevitable — the worksheet builder was copied without the updated fallback that includes `error`. | Copy-paste without shared utility function | Prior |

### LOW (code quality, maintenance, unlikely-to-bite immediately)

| ID | Finding | Source |
|----|---------|--------|
| **F18** | **Font pairing selects unmatched combinations.** `random.choice(_FONT_PAIRS)[0]` and `random.choice(_FONT_PAIRS)[1]` are independent calls — heading and body fonts come from different curated pairs. | Prior |
| **F19** | **Duplicate DeepSeek client code.** `_make_deepseek_client()` and `_call_deepseek()` are copied verbatim in `ModifySlide.py` and `InsertNewSlides.py`. | Prior |
| **F20** | **Substring matching in L1 filter.** `any(l1 in l1_groups_str for l1 in l1_list)` matches "Russian" in "Prussian". Unlikely to bite with 36-language dataset but fragile. | Prior |
| **F21** | **Theme failure silently ignored.** Pipeline continues without theme CSS if `theme_generator` raises. No deterministic fallback palette. | Prior |
| **F22** | **Kickoff detection fragility.** 30 hardcoded keyword strings to detect when the agent sends a "holding message." Blacklist approach to an LLM behavioral problem — infinite variation can't be blacklisted. | Prior |
| **F23** | **Stale slide files from previous runs.** Presentation directory is not cleaned before generation. Leftover `slide_*.html` files may interfere with filename-based task brief mapping. | Prior |
| **F24** | **Missing deliverables.** `GenerateProgressTrackerPdf` exists and is imported but never called by the pipeline. Homework and quiz generation are absent. | Both |
| **F25** | **Downloads allowed while job "running".** `/download`, `/bundle.html`, `/slides` endpoints accept `status == "running"`. Teacher can fetch a half-generated or not-yet-written bundle mid-run. | Independent |
| **F26** | **HTML bundle is 113-126 MB.** All images base64-inlined into one file. Risk of Railway response timeouts and egress cost. Concern, not a logic bug. | Independent |

---

## 2. Root Cause Map

F1, F2, F6, F7, F8, F13, F17 all share a common origin:

```
                    ┌──────────────────────────────────┐
                    │  No enforced YAML data contract    │
                    │  (no schema, no normalize at load, │
                    │   no shared accessor, no validation)│
                    └──────────┬───────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
  ┌───────────────┐   ┌──────────────┐   ┌──────────────────┐
  │ Field name    │   │ Nested shape │   │ Value format     │
  │ mismatch      │   │ mismatch     │   │ mismatch         │
  │ (error/wrong/ │   │ (data{} key  │   │ (labels vs clean │
  │  example_wrong)│  │ not unwrapped)│   │ sentences)       │
  └───┬───────────┘   └──┬───────────┘   └──┬───────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
  F2: Worksheet      F1: L1 Oracle      F8: Contaminated
  Sections A/B       gets 0 patterns    task brief values
  /Answer Key empty  (value prop is     (verbose labels)
      │               silently hollow)
      ▼                  │
  F7: "Watch for"       ▼
  lines empty        F13: Literal "[L1]"
                     in worksheet output
      │
      ▼
  F17: 10 inconsistent
  fallback chains across
  3 files
```

F4 (level discarded) and F5 (divergent path resolution) are independent structural defects.

F12 (cache never populated) is a direct consequence of F5 (the relative path resolves wrong in the cache check).

---

## 3. Clarification: Consolidation 2 Disagreement Analysis

Consolidation 2 re-litigated claims from `INDEPENDENT_AUDIT_2026-06-04.md` §2 stating that `AUDIT_REPORT_2026-06-04.md` claimed "parallel via asyncio.gather" and "L1 Oracle marked as passing." These claims do **not** appear in the current `AUDIT_REPORT_2026-06-04.md`. That report's Finding 2 explicitly states slides are sequential. It never mentions L1 Oracle as passing.

The git history confirms: an earlier version of `AUDIT_REPORT_2026-06-04.md` was deleted and rewritten. `INDEPENDENT_AUDIT` correctly critiqued the deleted version. The current version already incorporates those corrections. **There is no remaining disagreement between the current versions of both Layer 1 reports on these points.** The consolidation documents are in agreement about what needs to be fixed; they differ only in organization.

---

## 4. Execution Plan

Ordered by impact × ease-of-fix. Each step is independently verifiable.

### Sprint 1 — Restore Broken Outputs (2–3 hours)

**Goal:** L1 Oracle, worksheet, and flashcards contain real database content — not empty or AI-invented.

---

**Step 1.1 — Fix F1: Unwrap L1 `data` in `_load_yaml_data`**

File: `agent/slides_tools/QueueGenerationJob.py`, function `_load_yaml_data`, line 295-297.

```python
# BEFORE:
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict):
    l1_data_list.append(result)

# AFTER:
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict) and "data" in result and isinstance(result["data"], dict):
    # Unwrap: GetL1InterferenceTool returns {language, grammar_point, data: {...}}
    # All consumers expect flattened shape with interference_patterns at top level.
    merged = {**result["data"], "language": result.get("language", l1),
              "grammar_point": result.get("grammar_point", gram_slug)}
    l1_data_list.append(merged)
elif isinstance(result, dict):
    l1_data_list.append(result)  # already-flat or error dict
```

**Verify:** Generate Present Simple + Spanish. In the resulting `task_briefs`, L1 Oracle slide brief should reference specific Spanish interference patterns (e.g., "She walk" → "She walks") from the YAML database, not generic text. Worksheet Section C should contain L1-specific examples.

**Step 1.2 — Fix F2: Add `error`/`correction` to worksheet fallback chains**

File: `agent/slides_tools/QueueGenerationJob.py`, function `_build_worksheet_html`.

Lines 371-372 (Section A):
```python
# BEFORE:
wrong = _s(err.get("wrong", err.get("example_wrong", "")))
correct = _s(err.get("correct", err.get("example_correct", "")))
# AFTER:
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

Lines 383-384 (Section B): identical change.

Line 413 (Answer Key):
```python
# BEFORE:
correct = _s(err.get("correct", err.get("example_correct", "")))
# AFTER:
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

**Verify:** Generate a worksheet. Section A should show 4 gap-fill items with real sentences from the YAML. Section B should show 4 error-correction pairs with red/green formatting. Answer Key should list correct answers.

**Step 1.3 — Fix F13: Replace literal `[L1]` with language name**

File: `agent/slides_tools/QueueGenerationJob.py`, line 393.

```python
# BEFORE:
html_parts.append("<p>Fix these sentences that [L1] speakers often get wrong.</p>")
# AFTER:
l1_display = l1_languages if l1_languages else "some"
html_parts.append(f"<p>Fix these sentences that {l1_display} speakers often get wrong.</p>")
```

**Verify:** Worksheet Section C header should display the actual language name (e.g., "Fix these sentences that Spanish speakers often get wrong.").

**Step 1.4 — Fix F7: Add `error` to "Watch for" fallback chains**

Three locations in `agent/slides_tools/slide_plan.py`:

`_build_a5_brief` line 751:
```python
# BEFORE:
lines.append(f"  Watch for: {_s(relevant_errors[0].get('wrong', relevant_errors[0].get('example_wrong', '')))}")
# AFTER:
lines.append(f"  Watch for: {_s(relevant_errors[0].get('error', relevant_errors[0].get('wrong', relevant_errors[0].get('example_wrong', ''))))}")
```

`_build_a7_gap_fill_brief` line 1099: same pattern.

`_build_a8_brief` line 1157: same pattern.

**Verify:** Task briefs for A5, A7, A8 slides should have non-empty "Watch for:" lines in speaker notes.

---

### Sprint 2 — Performance (1 day)

**Goal:** ~3× faster slide generation.

---

**Step 2.1 — Fix F3: True parallel batches with `asyncio.gather`**

File: `agent/slides_tools/QueueGenerationJob.py`, `_run_slide_batches` (lines 623-645).

```python
# BEFORE:
for t_idx, task in enumerate(tasks):
    await asyncio.wait_for(task, timeout=120)

# AFTER:
results = await asyncio.gather(
    *[asyncio.wait_for(t, timeout=120) for t in tasks],
    return_exceptions=True
)
batch_ok = True
for t_idx, result in enumerate(results):
    filename = batch[t_idx]
    if isinstance(result, asyncio.TimeoutError):
        logger.error(f"Batch {batch_num}/{total_batches}: TIMEOUT for {filename}")
        batch_ok = False
    elif isinstance(result, Exception):
        logger.error(f"Batch {batch_num}/{total_batches}: ERROR on {filename}: {result}")
        batch_ok = False
# rest of batch_ok handling stays the same
```

Drop or reduce the per-slide 3s throttle (`SLIDE_GENERATION_DELAY` env var). DeepSeek's concurrency headroom is 2500 RPM — 3 concurrent calls are negligible. Keep a small inter-batch delay (1-2s) only if rate limiting is observed.

**Verify:** Time a 30-slide deck before and after. Slide generation phase should drop from ~10 minutes to ~3-4 minutes.

---

### Sprint 3 — Correctness (1 day)

**Goal:** Decks reflect requested proficiency level. Error data is clean.

---

**Step 3.1 — Fix F4: Thread `level` through the pipeline**

a) Add `level` field to `QueueGenerationJob` (file: `agent/slides_tools/QueueGenerationJob.py`, line ~73):
```python
level: str = Field(
    default="B1",
    description="Proficiency level (A1, A2, B1, B2, C1)",
)
```

b) Replace `getattr(self, "level", None) or "b1"` (line 103) with `self.level.lower()`.

c) Pass `level` through `_run_generation` → `compute_slide_plan` → `build_all_task_briefs`. Update function signatures.

d) In the brief builders (`slide_plan.py`), replace all hardcoded `"Level: B1"` with the dynamic value. The hardcoded string appears at line 431 and similar positions in `_build_a0_brief`.

**Verify:** Generate decks at A1, B1, and C1 levels. Cache keys should differ. Task briefs should reflect the correct level. Activity filtering (`bestForLevels`) should now work correctly.

**Step 3.2 — Fix F8: Extract clean sentences from verbose `error` field**

Create a helper in `agent/slides_tools/slide_plan.py`:
```python
def _extract_wrong_sentence(error_str: str) -> str:
    """Extract the wrong sentence from verbose error labels.
    YAML 'error' values are formatted like:
      "Omitting third person -s: *'She walk to school.'"
    This strips the label and returns just the wrong sentence."""
    import re
    # Match text between *'...' or *"..."
    match = re.search(r"\*'([^']+)'|\*\"([^\"]+)\"", error_str)
    return match.group(1) or match.group(2) if match else error_str
```

Use this helper in `_build_a5_brief`, `_build_a7_gap_fill_brief`, and `_build_a8_brief` whenever extracting from the `error` field. The fallback chain becomes:
```python
raw = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
wrong = _extract_wrong_sentence(raw) if err.get("error") else raw
```

**Verify:** Task briefs for A5/A7/A8 should contain clean wrong sentences like `"She walk to school."` instead of verbose labels like `"Omitting third person -s: *'She walk to school.'"`.

---

### Sprint 4 — Infrastructure Reliability (1–2 days)

**Goal:** Railway deployment is reliable. Downloads work. Cache populates. Teachers receive correctly labeled emails.

---

**Step 4.1 — Fix F5: Unify `mnt` path resolution**

File `agent/slides_tools/slide_file_utils.py` already has the correct 3-tier logic in `get_mnt_dir()` (line 47):
```python
def get_mnt_dir() -> Path:
    data_dir = os.getenv("COGNIESL_DATA_DIR")
    if data_dir:
        return Path(data_dir) / "mnt"
    if Path("/app/data").is_dir():
        return Path("/app/data") / "mnt"
    return Path(__file__).parents[2] / "mnt"
```

Make this the single source of truth:
- Import `get_mnt_dir` into `server.py`. Replace all 5 direct `COGNIESL_DATA_DIR` → `Path` constructions (lines 111, 213, 246, 311, 562, 897, 945) with `get_mnt_dir()`.
- Import into `GenerateFlashcardPdf.py`, `GenerateProgressTrackerPdf.py`, and `doc_file_utils.py`. Replace local path resolution.
- Delete the 2 divergent copies.

**Step 4.2 — Fix F12: Enable Master Repository cache writes**

File: `agent/slides_tools/MarkJobComplete.py`. The cache gate currently does:
```python
if Path(_primary_path).exists():
    add_to_cache(...)
```

Change to use `get_mnt_dir()`:
```python
from agent.slides_tools.slide_file_utils import get_mnt_dir
absolute_primary = get_mnt_dir() / project_name / "presentations" / Path(_primary_path).name
if absolute_primary.exists():
    add_to_cache(...)
```

**Step 4.3 — Fix F14: Email document labels**

File: `agent/email_sender.py`, `_label_for_file`. Add substring checks before the generic `.html` fallback:

```python
def _label_for_file(filename: str) -> tuple[str, str]:
    name = filename.lower()
    # Check content-type substrings first (pipeline files are .source.html)
    if "worksheet" in name:
        return ("Download Worksheet", "\U0001F4DD")
    if "activity" in name:
        return ("Download Activity Guide", "\U0001F4CB")
    if "flashcard" in name:
        return ("Download Flashcards", "\U0001F0CF")
    if "progress-tracker" in name:
        return ("Download Progress Tracker", "\U0001F4CA")
    # Original extension-based branches follow...
    if name.endswith(".html"):
        return ("Download Presentation", "\U0001F3AC")
    if name.endswith(".pdf"):
        return ("Download PDF", "\U0001F4C4")
    if name.endswith(".docx"):
        return ("Download DOCX", "\U0001F4C4")
    return ("Download File", "\U0001F4C1")
```

**Verify Sprint 4:** On Railway (or simulating with `COGNIESL_DATA_DIR` unset): (a) generation succeeds, (b) downloads resolve correctly, (c) a second identical request is served from cache, (d) email has 4 distinctly labeled buttons.

---

### Sprint 5 — Polish & Resilience (1–2 days)

Lower-severity items. Order is flexible based on capacity.

| Step | ID | Fix | Effort |
|------|----|-----|--------|
| 5.1 | F6 | **Add YAML schema validation.** Create Pydantic models for grammar, L1, and activity YAML structures. Validate at load time in `_load_yaml_data`. Normalize field names to a single convention. Log warnings when expected fields are missing. This makes F1/F2/F7 structurally impossible to reintroduce. | 3-4 hrs |
| 5.2 | F17 | **Extract shared `get_error_pair()` utility.** Replace all 10 fallback chain sites across `slide_plan.py` and `QueueGenerationJob.py` with a single imported function. This is the code-quality companion to F6. | 1 hr |
| 5.3 | F9 | **Show model its failed output on retry.** In `ModifySlide.py` post-write retry: set `previous_failed_html=final_html` and add a specific error message. | 15 min |
| 5.4 | F16 | **Configure Resend verified domain.** Set `COGNIESL_FROM_EMAIL` to a verified domain so non-Marcos teachers receive email. Verify domain in Resend dashboard. | 30 min |
| 5.5 | F18 | **Fix font pairing.** Change `theme_generator.py:296-297` to select heading and body from a single `random.choice(_FONT_PAIRS)` pair. | 5 min |
| 5.6 | F15 | **Validate fallback slides.** Run `slide_html_utils.validate_html()` on fallback-generated slides before writing to disk. Flag as degraded if they fail. | 1 hr |
| 5.7 | F22 | **Replace kickoff blacklist with structural detection.** If agent response is < 300 chars and contains no tool calls, treat as kickoff. Remove the 30 hardcoded phrases from `server.py`. | 1 hr |
| 5.8 | F23 | **Clean presentation directory before generation.** In `_create_blank_slides`, delete existing `slide_*.html` files before creating new placeholders. | 10 min |
| 5.9 | F25 | **Gate downloads on `status == "done"`.** In `/download`, `/bundle.html`, and `/slides` endpoints, reject requests for jobs still `"running"`. | 15 min |
| 5.10 | F24 | **Wire progress tracker into pipeline.** Add `GenerateProgressTrackerPdf` call as a post-generation step in `_run_generation`. | 1 hr |
| 5.11 | F11 | **Add batch-level checkpointing.** After each slide batch completes, write a manifest of completed slide indices. Recovery on restart can report "28/32 done" instead of all-or-nothing. | 2 hrs |

### Deferred

| ID | Item | Reason |
|----|------|--------|
| F19 | Duplicate DeepSeek client code | Refactor when touching both `ModifySlide.py` and `InsertNewSlides.py` for other changes. |
| F20 | Substring L1 matching | Fix alongside F6 (YAML schema — normalize to canonical language identifiers). |
| F21 | Theme failure fallback | Current behavior is a valid design choice (don't block on non-critical). Add fallback only if visual issues observed. |
| F26 | 124 MB bundle | Monitor for Railway timeout issues. Consider splitting or zip compression. |

---

## 5. Confidence Summary

All findings were verified by direct source code inspection against actual YAML data files.

| ID | Finding | Confidence | Verification Method |
|----|---------|-----------|---------------------|
| F1 | L1 Oracle receives zero real data | **Very High** | Full code trace: tool return → append → consumer .get(). Reproduced against `spanish_interference.yaml`. |
| F2 | Worksheet Sections A/B/Answer Key empty | **Very High** | Code trace + YAML grep for `error:` vs `wrong:`. Reproduced with `present_simple.yaml`. |
| F3 | Sequential batches | **Very High** | Source code: `for` loop `await`. No `gather` in file. Deterministic. |
| F4 | Level discarded | **Very High** | Pydantic field inspection: no `level`. `getattr` always `None`. Deterministic. |
| F5 | Inconsistent path resolution | **Very High** | Code trace across 7 files. 3 resolution patterns confirmed. |
| F6 | No YAML schema validation | **High** | Code inspection: no validation anywhere. Field names confirmed divergent in YAML. |
| F7 | "Watch for" empty | **Very High** | Missing `error` in 3 fallback chains. YAML grep confirmed. |
| F8 | Verbose `error` field | **Very High** | YAML inspection of `present_simple.yaml` and `present_perfect.yaml`. |
| F9 | Retry discards context | **Very High** | `previous_failed_html=None` at `ModifySlide.py:720`. |
| F10 | Two model routing systems | **Very High** | Code read: `config.py` LiteLLM vs. `ModifySlide.py` direct AsyncOpenAI. |
| F11 | Daemon thread work loss | **Very High** | `threading.Thread(daemon=True)`. No signal handler. |
| F12 | Cache never populated | **High** | Path resolution trace: relative × absolute mismatch. |
| F13-F26 | All remaining | **High** | Source code read, deterministic or traceable. |

---

## 6. What the Pipeline Gets Right

Despite 26 findings, the architecture has strong fundamentals:

- **10-step pipeline** is logically sound and covers all deliverable types
- **Crash recovery** detects partial state on restart (best-effort, can be improved — F11)
- **Theme system** provides visual cohesion without LLM calls (protect it — F21)
- **Playwright validation** is thorough: dimensions, overflow, text wrapping, speaker notes, descender clipping
- **Post-write size check** catches thin slides that pass structural validation
- **Progress logging** (`_write_progress`) provides per-step crash debugging
- **Master Repository cache** structure exists — just needs a path fix (F12)
- **302 grammar + 36 L1 + 220 activity YAML files** — rich, pre-validated database

The findings concentrate in the glue code between data and consumers — not in the core architecture. F1 and F2 are the only bugs that produce broken output. The remaining 24 findings are about performance, correctness at edges (level/paths), resilience, and code quality. **Sprints 1–3 will take the system from "runs but ships wrong content" to "ships correct, differentiated, fast materials."**
