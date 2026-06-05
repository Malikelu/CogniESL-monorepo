# CogniESL — Full Audit Report

**Date:** 2026-06-04
**Author:** Claude Opus 4.8 (independent code audit)
**Scope:** Full codebase — architecture, pipeline, data layer, validation, infrastructure

This report identifies bugs, structural problems, and design issues found by direct source code inspection. Findings are verified against the actual YAML data files and source code — not based on previous reports or observed test output.

---

## Audit Methodology

For each finding, I provide:
- **Confidence**: HIGH (verified against code + data), MEDIUM (code path verified but behavior untested), LOW (suspected but not fully traced)
- **Impact**: CRITICAL (silent data loss / broken output), HIGH (degraded output), MEDIUM (performance waste), LOW (code quality)
- **Debug Plan**: How to reproduce and verify
- **Fix**: The minimal change needed

---

## Finding 1: Worksheet Content Is Always Empty

**Severity:** CRITICAL — produces broken deliverables
**Confidence:** HIGH — verified against source YAML data
**Impact:** All worksheets have empty `Section A`, `Section B`, and `Section C`

### Root Cause

The worksheet builder (`QueueGenerationJob.py:322-426`, `_build_worksheet_html`) uses different field names to access `common_errors` than what the YAML data actually contains.

**What the worksheet builder looks for** (line 371-375):
```python
wrong = _s(err.get("wrong", err.get("example_wrong", "")))      #  ← never matches
correct = _s(err.get("correct", err.get("example_correct", "")))  # ← never matches
```

**What the grammar YAML actually contains** (verified in `present_simple.yaml`, `present_perfect.yaml`):
```yaml
common_errors:
- error: 'Omitting third person -s: *''She walk to school.'''     # ← field is "error"
  correction: She walks to school.                                  # ← field is "correction"
```

**The field names are `error`/`correction`, not `wrong`/`correct`.**

The task brief builder (`slide_plan.py:1088-1089`) correctly handles both naming conventions:
```python
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

But the worksheet builder only checks `wrong`/`correct`/`example_wrong`/`example_correct`. Since the YAML uses `error`/`correction`, all fallback chains resolve to `""`, producing empty `<li>` elements.

### Debug Plan
1. Generate a worksheet for Present Simple + Spanish
2. Inspect `Section A` — all 4 `<li>` items will be empty
3. Add `print()` debug before line 371 to confirm `err` dict has `error`/`correction` keys
4. Apply fix, regenerate, verify content appears

### Fix

In `_build_worksheet_html()` (QueueGenerationJob.py), lines 371 and 375, add `error`/`correction` to the fallback chain:

```python
# Line 371 (Section A fill-the-gap)
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))

# Line 383 (Section B error correction)
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))

# Line 413 (Answer Key)
correct = _s(err.get("correction", err.get("correct", err.get("example_correct", ""))))
```

Also affects L1 patterns in Section C (line 395-396) — but L1 YAML uses `example_wrong`/`example_correct` which is already handled correctly. Add `error`/`correction` as the first fallback anyway for consistency.

---

## Finding 2: Slide Batches Are Sequential, Not Parallel

**Severity:** MEDIUM — performance waste, not a correctness bug
**Confidence:** HIGH — the code is unambiguous
**Impact:** Generation is ~3x slower than it should be for slide generation

### Root Cause

`QueueGenerationJob.py:596-648` processes slides in "batches" of 3, but `_run_slide_batches()` awaits each task sequentially using individual `await asyncio.wait_for()` calls:

```python
for t_idx, task in enumerate(tasks):        # tasks has 3 items
    await asyncio.wait_for(task, timeout=120)  # ← blocks sequentially
```

The docstring at line 12 says "parallel batches (3 at a time)" but the implementation is sequential within each batch. Each slide is generated one at a time, waiting for completion before starting the next.

### Debug Plan
1. Add timing logs around the batch loop
2. Run with 3 slides and observe: total batch time ≈ sum of individual slide times
3. Change to `asyncio.gather()`  and observe: total batch time ≈ max individual slide time
4. Expected improvement: ~2.5-3x faster slide generation

### Fix

Replace lines 623-645 with:

```python
if tasks:
    results = await asyncio.gather(*tasks, return_exceptions=True)
    batch_ok = True
    for t_idx, result in enumerate(results):
        filename = batch[t_idx]
        if isinstance(result, asyncio.TimeoutError):
            logger.error(f"Batch {batch_num}/{total_batches}: TIMEOUT for {filename}")
            batch_ok = False
        elif isinstance(result, Exception):
            logger.error(f"Batch {batch_num}/{total_batches}: ERROR on {filename}: {result}")
            batch_ok = False
```

**Caveat:** ModifySlide already has a built-in 3-second throttle (`ModifySlide.py:562`). With parallel execution, 3 slides would hit the API simultaneously — monitor for rate limiting. If hitting limits, add a small stagger (0.5s) between concurrent task starts.

---

## Finding 3: Duplicate Model Client Code

**Severity:** LOW — code quality, not a functional bug
**Confidence:** HIGH
**Impact:** 56 lines of duplicated code between two files

### Root Cause

`ModifySlide.py` (lines 233-263) and `InsertNewSlides.py` (lines 48-72) contain identical implementations of:
- `_make_deepseek_client()` — 14 lines
- `_call_deepseek()` — 15 lines
- `_get_*_model_id()` — 8 lines each (nearly identical)

### Fix

Extract to `agent/slides_tools/deepseek_client.py`:
```python
def make_deepseek_client(): ...
async def call_deepseek(client, model_id, system_prompt, user_prompt): ...
def get_model_id(env_var="BG_SUB_AGENT_MODEL", fallback="deepseek-v4-flash"): ...
```

Import in both files. One source of truth for DeepSeek client creation.

---

## Finding 4: Two Incompatible Model Routing Systems

**Severity:** MEDIUM — architectural confusion
**Confidence:** HIGH
**Impact:** Main agent uses `LitellmModel` wrapper; sub-agents use direct `AsyncOpenAI`. Different error handling, different retry logic, different base URL configuration.

### Root Cause

- **Main agent** (`config.py`): Wraps model IDs in `LitellmModel` for the agency-swarm Agent constructor. DeepSeek is accessed via LiteLLM's multi-provider routing.
- **Sub-agents** (`ModifySlide.py`, `InsertNewSlides.py`): Bypass LiteLLM entirely with direct `AsyncOpenAI(api_key=..., base_url="https://api.deepseek.com")`.

This means the main agent and sub-agents have:
- Different error/retry behavior (LiteLLM retries internally vs. explicit retry loops)
- Different thinking mode handling (main agent doesn't disable it)
- Different API key resolution paths

### Debug Plan
1. Check if the main agent's DeepSeek calls use thinking mode (not disabled in `config.py`)
2. Compare latency of main agent calls vs. sub-agent calls
3. Verify neither path is secretly routing through a different provider

### Fix

Decide on one approach:
- **Option A:** Use direct `AsyncOpenAI` everywhere, rip out LiteLLM from `config.py`
- **Option B:** Use `LitellmModel` everywhere, remove direct client code from sub-agents

Option A is likely better — the project only uses DeepSeek, so multi-provider routing adds complexity without value.

---

## Finding 5: Daemon Threads Lose Mid-Generation Work on Restart

**Severity:** MEDIUM — affects reliability
**Confidence:** HIGH
**Impact:** When Railway auto-deploys or the server restarts, any in-progress generation is terminated without cleanup. Partially-written slide files remain on disk. The job status stays "running" until recovery logic on restart either marks it "done" (if slide files exist) or "error" (if not).

### Root Cause

`QueueGenerationJob.py:146-162` — background generation thread is created with `daemon=True`:
```python
thread = threading.Thread(
    target=_run_background_generation, ...
    daemon=True,   # ← killed without warning on process exit
)
```

The recovery logic in `server.py:110-149` handles this reasonably well — but it can only mark jobs as done/error. It can't resume mid-generation. A job that had 28/32 slides complete will either be "done" (partial deck) or "error" (teacher gets nothing).

### Debug Plan
1. Start a generation job
2. Mid-way through, send SIGTERM to the server
3. Observe which slides exist on disk
4. Check how recovery logic classifies the job

### Fix

The current recovery is "best effort" and probably sufficient for now. However, consider:

1. **Checkpointing**: After each batch completes, write a manifest of completed slides to disk (already partially done via `_write_progress()`)
2. **Resume**: On restart, if a "running" job has partial slides, resume from where it left off
3. **At minimum**: Log which slides were completed so the recovery can distinguish "28/32 slides done" from "0/32 done"

---

## Finding 6: Font Pairing Selects Unmatched Combinations

**Severity:** LOW — visual quality
**Confidence:** HIGH
**Impact:** Heading and body fonts may clash, degrading the "premium" visual quality the product targets.

### Root Cause

`theme_generator.py:296-297` selects heading and body fonts independently from `_FONT_PAIRS`:
```python
"font_heading": random.choice(_FONT_PAIRS)[0],
"font_body": random.choice(_FONT_PAIRS)[1],
```

`_FONT_PAIRS` contains 8 **curated pairs** meant to be used together:
```python
("Space Grotesk", "Inter"),
("Inter", "Merriweather"),
("Urbanist", "Lora"),
...
```

But `random.choice(_FONT_PAIRS)[0]` and `random.choice(_FONT_PAIRS)[1]` are independent calls — the heading might come from pair 7 (`Playfair Display`) and the body from pair 3 (`Lora`), which may not pair well.

### Fix

```python
pair = random.choice(_FONT_PAIRS)
"font_heading": pair[0],
"font_body": pair[1],
```

---

## Finding 7: Post-Write Retry Discards Validation Context

**Severity:** MEDIUM — reduces retry effectiveness
**Confidence:** HIGH
**Impact:** When a slide passes validation but is too thin (<4000 bytes), the retry round discards the validation error context that could help the model fix specific problems.

### Root Cause

`ModifySlide.py:713-775` — the post-write size check retry:
```python
_pw_prompt = _build_sub_run_prompt(
    ...
    retry_validation_error=_pw_err,     # ← starts empty, may get filled
    previous_failed_html=None,           # ← NEVER shows the model its own output
)
```

The `previous_failed_html` is explicitly set to `None`, meaning the model doesn't see what it previously generated. It has to regenerate from scratch, likely making the same mistakes. The validation error (`_pw_err`) is only populated when the retry itself fails validation — not when the original slide passed validation but was too small.

### Fix

Set `previous_failed_html=final_html` (the slide that passed validation but was too thin) so the model can see what it needs to expand:

```python
_pw_prompt = _build_sub_run_prompt(
    ...
    retry_validation_error="Slide content is too thin. Add more examples, visual elements, and detailed speaker notes.",
    previous_failed_html=final_html,    # ← show what needs improvement
)
```

---

## Finding 8: Substring Matching in L1 Error Filtering

**Severity:** LOW — unlikely to cause visible bugs with current data
**Confidence:** MEDIUM
**Impact:** Potential false positives when L1 language names are substrings of each other.

### Root Cause

`slide_plan.py:348-349`:
```python
l1_groups_str = _s(l1_groups).lower() if not isinstance(l1_groups, list) else " ".join(l1_groups).lower()
if any(l1 in l1_groups_str for l1 in l1_list) or not l1_list:
```

If requesting "Russian" and the `l1_groups` contains "Prussian", `"russian" in "prussian"` is `True` — a false positive match. Similarly, "Mandarin" partially matches "Mandarin Chinese" (correct) but "Chinese" isn't in "Mandarin" (missed match).

With the current 36-language dataset this is unlikely to cause visible problems, but it's fragile.

### Fix

Use word-boundary matching or normalize to canonical language identifiers:
```python
l1_set = set(l1_list)
err_l1_set = set(l.strip().lower() for l in l1_groups_str.replace(",", " ").split())
if l1_set & err_l1_set:
```

Or, better: standardize on ISO language codes or canonical names throughout the data.

---

## Finding 9: No YAML Schema Validation

**Severity:** HIGH — silent data loss across the pipeline
**Confidence:** MEDIUM
**Impact:** The pipeline accesses YAML fields with multi-level fallback chains (`err.get("error", err.get("wrong", err.get("example_wrong", "")))`) to handle inconsistent naming. If all fallbacks miss (as in Finding 1), output is silently empty. There's no warning that data was expected but not found.

### Root Cause

No schema validation exists anywhere in the pipeline. The YAML data has inconsistent field naming conventions:
- Grammar `common_errors`: uses `error`/`correction`  
- L1 `interference_patterns`: uses `example_wrong`/`example_correct`
- Some files may use `wrong`/`correct`

The multi-level fallback is a symptom — the root cause is no enforced contract between data producers (YAML files) and data consumers (task brief builders, worksheet builders).

### Fix

1. **Define a Pydantic model** for each YAML structure (grammar data, L1 data, activities)
2. **Validate at load time** in `_load_yaml_data()` — log warnings if fields are missing
3. **Standardize field names** — pick one convention (`error`/`correction` or `wrong`/`correct`) and normalize at import time

---

## Finding 10: Theme Generation Failure Is Silently Ignored

**Severity:** LOW — slides still work, just less visually cohesive
**Confidence:** HIGH
**Impact:** If `theme_generator.py` raises (e.g., due to missing mood mapping for a new grammar point), slides proceed without theme CSS. Each slide then falls back to its own embedded styles, losing visual cohesion.

### Root Cause

`QueueGenerationJob.py:584-593`:
```python
try:
    from agent.slides_tools.theme_generator import generate_theme, write_theme_css
    ...
    theme = generate_theme(grammar_point, age_group)
    theme_path = write_theme_css(presentations_dir, theme)
except Exception as exc:
    logger.warning(f"Theme generation skipped: {exc}")   # ← just a warning
```

The pipeline continues without `_theme.css`. Slides still get written with individual styles, but they won't share the cohesive palette and font pair the theme provides.

### Fix

This is a reasonable design choice (don't block on non-critical failure). However, the `_read_theme_css()` fallback (line 292-298) returns `""` when `_theme.css` is missing. Consider:

```python
# In ModifySlide._build_sub_run_prompt, when theme_css is empty:
if not theme_css:
    theme_css = _generate_fallback_theme_css()  # deterministic fallback palette
```

---

## Finding 11: Missing Progress Tracker Generation

**Severity:** LOW — feature gap, not a bug
**Confidence:** HIGH
**Impact:** `GenerateProgressTrackerPdf.py` exists and is imported by the agent, but is never called from the background pipeline.

### Root Cause

`QueueGenerationJob.py` has no code path that calls `GenerateProgressTrackerPdf`. The tool exists, the agent has access to it, but the background pipeline's 10-step flow doesn't include it. MarkJobComplete has a `progress_tracker_pdf_path` parameter that's always `None` because nothing generates the file.

### Fix

Add a Step 9b in the pipeline (or integrate into MarkJobComplete) to generate the progress tracker. The `GenerateProgressTrackerPdf` tool appears to be designed for use by the main agent (via chat), not the background pipeline — decide whether to add it to the background flow or keep it as a post-generation request the teacher can make.

---

## Finding 12: Slide File Listing May Mismatch Task Brief Indices

**Severity:** LOW — unlikely but possible
**Confidence:** MEDIUM
**Impact:** `_list_slide_filenames()` lists all `slide_*.html` files in the presentations directory. In `_run_slide_batches()`, the slide index is extracted from the filename regex `slide_(\d+)`. If files have unexpected names (e.g., `slide_01_cover.html` from a previous coding session), the regex would match `01` and map to `task_briefs[1]`. But the file listing might include files the pipeline didn't create (leftovers from a previous run).

### Debug Plan
1. Check if the presentation directory is cleaned before each generation
2. If not, add a cleanup step before creating blank placeholders

### Fix

In `_create_blank_slides()` (line 304), delete all existing `slide_*.html` files before creating new ones:
```python
def _create_blank_slides(project_name: str, count: int) -> None:
    presentations_dir = _get_mnt_path(project_name) / "presentations"
    presentations_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean up any leftover files from a previous run
    for old in presentations_dir.glob("slide_*.html"):
        old.unlink()
    
    # Create fresh blank placeholders
    ...
```

---

## Finding 13: Literal "[L1]" Text Appears in Worksheet Output

**Severity:** MEDIUM — degrades worksheet quality
**Confidence:** HIGH — verified in source code
**Impact:** Every worksheet's Section C header says "Fix these sentences that [L1] speakers often get wrong." — with the literal text `[L1]`, not the actual language name.

### Root Cause

`QueueGenerationJob.py:393`:
```python
html_parts.append("<p>Fix these sentences that [L1] speakers often get wrong.</p>")
```

The placeholder `[L1]` is hardcoded as literal text. The function has access to `l1_languages` (a comma-separated string like "Spanish, Portuguese") but never performs string replacement on this line. Compare with how `l1_languages` IS used elsewhere — only in line 330 to create `l1_list` for pattern filtering.

### Fix

```python
l1_display = l1_languages if l1_languages else "some"
html_parts.append(f"<p>Fix these sentences that {l1_display} speakers often get wrong.</p>")
```

---

## Finding 14: "error" Field Contains Verbose Descriptions, Not Clean Sentences

**Severity:** MEDIUM — data contamination degrades slide quality
**Confidence:** HIGH — verified against actual YAML data
**Impact:** When task brief builders fall back to `err.get("error")`, they get descriptive strings like `"Omitting third person -s: *'She walk to school.'"` instead of clean wrong sentences like `"She walk to school."` The HTML writer model must parse out the actual sentence from a verbose label — some models will succeed, others will produce garbled output or include the label text on the slide.

### Root Cause

The grammar YAML files use the `error` field to store both a descriptive label AND the wrong example, formatted as a single string:

```yaml
common_errors:
- error: 'Omitting third person -s: *''She walk to school.'''
  correction: She walks to school.
```

The task brief builders (`slide_plan.py`) correctly include `error` in their fallback chains (unlike the worksheet builder — Finding 1), so they DO extract data. But the extracted value is contaminated: it's not a clean wrong sentence, it's a descriptive label that happens to contain the wrong sentence.

Affected task brief builders:
- `_build_a5_brief()` line 738: `wrong = _s(err.get("error", ...))`
- `_build_a7_gap_fill_brief()` line 1089: `wrong = _s(err.get("error", ...))`  
- `_build_a8_brief()` lines 1127, 1132: `l1_error = _s(err.get("error", ...))`

### Fix

Two options:

**Option A (quick):** Parse the wrong sentence out of the `error` string:
```python
def _extract_wrong_sentence(error_str: str) -> str:
    """Extract just the wrong sentence from error descriptions like 
    'Omitting third person -s: *''She walk to school.'''"""
    import re
    match = re.search(r"\*'([^']+)'|\*"([^"]+)"", error_str)
    return match.group(1) if match else error_str
```

**Option B (better):** Add explicit `wrong`/`correct` fields to the YAML data or normalize at load time. This is the same root cause as Finding 9 (no schema validation).

---

## Finding 15: "Watch For" Lines Are Empty Due to Missing `error` Fallback

**Severity:** MEDIUM — speaker notes lose error-awareness
**Confidence:** HIGH — verified against code + YAML field names
**Impact:** The "Watch for:" speaker notes in A5, A7, and A8 task briefs are empty when the YAML only has `error`/`correction` fields (which is all grammar YAML files). The teacher loses the "what to watch for" guidance.

### Root Cause

Three task brief builders have "Watch for" lines that don't include `error` in their fallback chain:

**`_build_a5_brief()` line 751:**
```python
lines.append(f"  Watch for: {_s(relevant_errors[0].get('wrong', relevant_errors[0].get('example_wrong', '')))}")
```

**`_build_a7_gap_fill_brief()` line 1099:**
```python
lines.append(f'  Watch for: {_s(errors[0].get("wrong", errors[0].get("example_wrong", "")))}')
```

**`_build_a8_brief()` — same pattern.**

All three fallback chains are `wrong` → `example_wrong` → `""`. The YAML uses `error`, which is not in the chain. Result: empty string.

Contrast with the A5 builder's main error extraction (line 738) which DOES include `error`:
```python
wrong = _s(err.get("error", err.get("wrong", err.get("example_wrong", ""))))
```

The "Watch for" lines were written with a different (older?) fallback chain that was never updated to include `error`.

### Fix

Add `error` to the fallback chain in all three "Watch for" lines:
```python
# _build_a5_brief line 751
lines.append(f"  Watch for: {_s(relevant_errors[0].get('error', relevant_errors[0].get('wrong', relevant_errors[0].get('example_wrong', ''))))}")

# _build_a7_gap_fill_brief line 1099
lines.append(f'  Watch for: {_s(errors[0].get("error", errors[0].get("wrong", errors[0].get("example_wrong", ""))))}')
```

This will at least surface the `error` value, even though it contains descriptive text (see Finding 14).

---

## Finding 16: Kickoff Detection Is Fragile (30 Hardcoded Strings)

**Severity:** LOW — maintenance burden, not a correctness bug
**Confidence:** HIGH
**Impact:** `server.py:717-748` uses 30 hardcoded keyword phrases to detect when the agent sends a "holding message" instead of calling tools. If the agent uses a phrase not in this list, the kickoff goes undetected and the teacher sees an unhelpful message. If a phrase is too generic, it produces false positives.

### Root Cause

```python
_kickoff_phrases = (
    "stay tuned", "coming right up",
    "putting together", "will be ready", "brief is coming",
    "getting your brief", "preparing your brief",
    # ... 30 total phrases
)
```

This is a blacklist approach to an LLM behavioral problem. The LLM can generate infinite variations — no blacklist will ever be complete. The current list was built reactively (phrases added after they were observed failing), which guarantees new phrases will be missed.

### Fix

Consider alternative approaches:
1. **Structural detection**: If the agent's response is < 200 chars and contains NO tool calls, treat as kickoff
2. **Tool-call enforcement**: Modify the agent's system prompt to require a tool call in every response during generation flow
3. **Timeout-based**: If no tool call within N seconds, force-retry

The length-based check already exists (`len(text.strip()) > 700`) but 700 chars is generous — a kickoff message is typically < 200 chars.

---

## Finding 17: Duplicate Field-Name Fallback Chains Across Codebase

**Severity:** LOW — code quality, but directly caused Finding 1 and Finding 15
**Confidence:** HIGH
**Impact:** The field-name fallback pattern (`err.get("error", err.get("wrong", err.get("example_wrong", ""))`) is copy-pasted across ~8 locations in 3 files with inconsistent variations. Some locations include `error`/`correction`, some don't. This duplication made Finding 1 inevitable — the worksheet builder was copied without the updated fallback chain.

### Affected Locations

| File | Lines | Has `error`/`correction`? |
|------|-------|--------------------------|
| `slide_plan.py:_build_a5_brief` | 738-739 | ✅ Yes |
| `slide_plan.py:_build_a5_brief` (Watch for) | 751 | ❌ Missing |
| `slide_plan.py:_build_a7_gap_fill_brief` | 1089-1090 | ✅ Yes |
| `slide_plan.py:_build_a7_gap_fill_brief` (Watch for) | 1099 | ❌ Missing |
| `slide_plan.py:_build_a8_brief` | 1127-1128 | ✅ Yes |
| `slide_plan.py:_build_a8_brief` (Watch for) | 1150 | ❌ Missing |
| `QueueGenerationJob.py:_build_worksheet_html` Section A | 371-372 | ❌ Missing |
| `QueueGenerationJob.py:_build_worksheet_html` Section B | 383-384 | ❌ Missing |
| `QueueGenerationJob.py:_build_worksheet_html` Answer Key | 413 | ❌ Missing |
| `QueueGenerationJob.py:_build_worksheet_html` Section C | 395-396 | N/A (L1 patterns use `example_wrong`) |

### Fix

Create a single utility function and use it everywhere:

```python
def _get_error_pair(err: dict) -> tuple[str, str]:
    """Extract (wrong, correct) from a common_errors entry regardless of field naming convention."""
    wrong = str(err.get("error") or err.get("wrong") or err.get("example_wrong") or "")
    correct = str(err.get("correction") or err.get("correct") or err.get("example_correct") or "")
    return wrong, correct
```

This is the same root cause as Finding 9 — without schema validation, field name conventions diverge and consumers handle them inconsistently.

---

## Summary

| # | Finding | Confidence | Severity |
|---|---------|-----------|----------|
| 1 | **Worksheet content always empty** — field name mismatch (`error`/`correction` vs `wrong`/`correct`) | HIGH | CRITICAL |
| 2 | **Slide batches are sequential, not parallel** — individual `await` instead of `gather` | HIGH | MEDIUM |
| 3 | **Duplicate model client code** — identical functions in two files | HIGH | LOW |
| 4 | **Two model routing systems** — LiteLLM + direct AsyncOpenAI | HIGH | MEDIUM |
| 5 | **Daemon threads lose work on restart** — no checkpointing | HIGH | MEDIUM |
| 6 | **Font pairing broken** — independent selection from curated pairs | HIGH | LOW |
| 7 | **Post-write retry discards context** — `previous_failed_html=None` | HIGH | MEDIUM |
| 8 | **Substring matching in L1 filter** — fragile language matching | MEDIUM | LOW |
| 9 | **No YAML schema validation** — silent data loss across pipeline | MEDIUM | HIGH |
| 10 | **Theme failure silently ignored** — cohesive style lost | HIGH | LOW |
| 11 | **Missing progress tracker generation** — tool exists, not called | HIGH | LOW |
| 12 | **Stale slide files from previous runs** — leftover files may interfere | MEDIUM | LOW |
| 13 | **Literal "[L1]" in worksheet** — placeholder never replaced with language name | HIGH | MEDIUM |
| 14 | **"error" field values are verbose descriptions** — contaminated data in task briefs | HIGH | MEDIUM |
| 15 | **"Watch for" lines are empty** — missing `error` in fallback chains for A5/A7/A8 | HIGH | MEDIUM |
| 16 | **Kickoff detection fragility** — 30 hardcoded keyword strings | HIGH | LOW |
| 17 | **Duplicate fallback chains** — 10 locations, 3 inconsistent variations | HIGH | LOW |

### Root Cause Analysis

Findings 1, 9, 13, 14, 15, and 17 share a common root cause: **the YAML data has no enforced schema contract**. Field names vary (`error`/`correction` vs `wrong`/`correct`), field value formats vary (descriptive labels vs clean sentences), and consumers handle this inconsistently. Every new consumer of the YAML data risks introducing the same class of bug.

The fix that would prevent ALL of these: **validate and normalize YAML data at load time** (Finding 9), then extract a single utility for field access (Finding 17).

### Recommended Fix Priority

1. **Fix Finding 1 first** — CRITICAL bug producing broken worksheets. Affects every worksheet generated.
2. **Fix Finding 9 + 17 together** — add Pydantic validation at YAML load time + single utility function. This prevents Findings 1, 13, 14, 15 from recurring and catches data issues at import time.
3. **Fix Finding 13** — literal "[L1]" text is visible to every teacher using worksheets.
4. **Fix Finding 2** — 2-3x speedup with `asyncio.gather()`.
5. **Fix Finding 15** — restore "Watch for" guidance that teachers rely on.
6. **Fix Findings 6, 7** — trivial fixes for visual quality and retry effectiveness.

### What the Pipeline Gets Right

Despite these issues, the architecture is well-designed:
- **10-step pipeline** is logically sound and covers all deliverable types
- **Crash recovery** correctly handles restarts (best effort)
- **Theme system** (when it works) provides visual cohesion without LLM calls
- **Validation** is thorough (Playwright-based, checks dimensions, overflow, text wrapping, speaker notes)
- **Post-write size check** catches thin slides that pass validation
- **Progress logging** (`_write_progress`) provides crash debugging
- **Master Repository cache** avoids redundant generation

The core problems are data contract mismatches (Findings 1, 9) and performance (Finding 2) — not architectural. The system is closer to production-ready than the previous report suggests.
