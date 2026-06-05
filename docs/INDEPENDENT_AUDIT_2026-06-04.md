# CogniESL — Independent Backend Audit

**Date:** 2026-06-04
**Scope:** Python backend + generation pipeline (`agent/`, `server.py`, data loaders). Website excluded by request.
**Method:** Static read of the actual source + targeted reproductions against the real YAML database. The prior `AUDIT_REPORT_2026-06-04.md` was treated as untrusted; every claim below was re-derived from code.
**Auditor stance:** Root cause over symptom. Confidence levels stated per finding.

---

## 0. TL;DR — what's actually wrong

The pipeline *runs* end-to-end, which is why prior testing looked "mostly fine." But three of the most important outputs are silently hollow, and the slowness is self-inflicted:

1. **The L1 Oracle slides — your entire value proposition — receive ZERO real interference data.** The data exists in the YAML, but a structural contract mismatch means the slide briefs get an empty list every time. The model then has to invent L1 content, which violates the "database is sacred / never AI-generate L1 content" rule in `CLAUDE.md`. **This is the single most damaging bug and the prior report missed it entirely** (it even marked L1 Oracle as passing).

2. **The worksheet is structurally empty** for the same root cause *plus* a second, independent key-name mismatch. Reproduced: Section A = 4 blank items, Sections B/C = 0 items, answer key = 0 items.

3. **Flashcards get no L1 patterns** — same root cause as #1/#2.

4. **"Parallel batch" generation is actually fully sequential.** `BATCH_SIZE=3` is dead code. This is the real reason a deck takes ~10 minutes. The prior report's claim of "parallel via `asyncio.gather`" is false.

5. **Proficiency level is silently dropped** across the entire pipeline; every deck is hardcoded "B1," and the cache key always uses `b1`.

6. **Fragile path resolution:** the `mnt` data directory is resolved three different ways across the codebase. They agree only while `COGNIESL_DATA_DIR` is explicitly set; if it's ever unset on Railway, every download / slide view 404s despite successful generation. The same class of bug is why the Master Repository cache has never populated (§1.7-C). (The email download *links* themselves are fine — see the §1.5 correction.)

7. **All delivered documents look identical in the email** — worksheet, activity guide, flashcards, and the deck all render as the same "Download Presentation" button (§1.7-B).

Findings 1–3 share a **single root cause** and can be fixed in ~3 lines. Findings 6 + the cache share another (path resolution) and collapse into one shared helper.

---

## 1. Root cause analysis

### 1.1 The shared root cause: L1 tool returns nested `data`, consumers expect it flattened

`GetL1InterferenceTool.run()` returns:

```python
{"language": "Spanish", "grammar_point": "present_perfect", "data": { ...the real entry... }}
```

The real interference content (`interference_patterns`, `why_it_happens`, `teacher_tips`, `phonology_interference`, …) lives **inside `data`**.

But every consumer reads those fields from the **top level** of that dict:

| Consumer | Code | Reads | Gets |
|---|---|---|---|
| L1 Oracle slide (`slide_plan._build_a6_brief`) | `_pick_tier1_2_patterns(l1_data)` → `l1_data.get("interference_patterns")` | top-level | `None` → 0 patterns |
| L1 Oracle WHY | `l1_data.get("why_it_happens")` | top-level | `""` |
| Phonics slide (`_build_*` ~L950) | `l1_data.get("phonology_interference")` | top-level | `None` |
| Worksheet Section C | `ld.get("interference_patterns")` | top-level | `None` → 0 items |
| Flashcards (QueueGenerationJob step 9) | `ld.get("interference_patterns")` | top-level | `None` → 0 patterns |

The consumers were written against a **flattened** shape `{language, interference_patterns, why_it_happens, ...}`. They even read `language` (a top-level wrapper field) **and** `interference_patterns` (a `data`-level field) from the same dict — the two are mutually incompatible, which is the fingerprint of the mismatch.

**Reproduced** against `data/l1-interference/spanish_interference.yaml`, present_perfect entry:

```
PATTERNS picked from wrapper (current code path): 0
PATTERNS if it unwrapped data[]:                  2   ← the data is right there
why_it_happens from wrapper: ''                       ← exists under data
```

**Confidence: VERY HIGH** (reproduced directly with the real database).

**Impact:** The L1 Oracle slide brief falls back to the generic line `"Common errors {L1} speakers make with {grammar}"` and zero pattern cards. The model fills the gap by inventing L1 errors — the exact behavior `CLAUDE.md` forbids ("never generate grammar/pedagogical content with AI"; "If an L1 is specified, L1 Oracle content MUST be generated"). The slides *look* populated (9–12 KB) so visual inspection and the prior report missed it.

**The fix (one place, fixes #1, #2-partial, #3 at once):** flatten in `_load_yaml_data` (`QueueGenerationJob.py`):

```python
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict) and "data" in result and isinstance(result["data"], dict):
    merged = {**result["data"], "language": result.get("language", l1),
              "grammar_point": result.get("grammar_point")}
    l1_data_list.append(merged)
elif isinstance(result, dict):
    l1_data_list.append(result)   # already-flat or error dict
```

Verify after: `len(_pick_tier1_2_patterns(_get_l1_data(l1_data_list, "Spanish")))` should be ≥ 1.

---

### 1.2 Worksheet: a *second*, independent key mismatch

Even after 1.1 is fixed, the worksheet's grammar-error sections stay empty because `_build_worksheet_html()` reads the wrong keys for `common_errors`:

```python
wrong   = err.get("wrong",   err.get("example_wrong",   ""))
correct = err.get("correct", err.get("example_correct", ""))
```

But the grammar YAML uses **`error`** and **`correction`**:

```yaml
common_errors:
  - error:       "Omitting the auxiliary 'have/has': *'I eaten lunch.'"
    correction:  "I have eaten lunch."
    explanation: "..."
```

**Reproduced** (present_perfect.yaml, 10 common_errors present):

```
Section A gap_text values: ["''", "''", "''", "''"]   # 4 empty <li>
Section B items:           0
Section C l1_patterns:     0   # the 1.1 nesting bug
Answer key items:          0
```

Note the slide builders (`slide_plan._build_a0_brief`, gap-fill, etc.) get this right — they use `err.get("error", err.get("wrong", err.get("example_wrong", "")))`. Only the worksheet builder omits the `error`/`correction` fallbacks. So **slides have real grammar errors; the worksheet does not.**

**Fix:** add the `error`/`correction` keys to the worksheet's `.get()` chains (and to the flashcard extraction), mirroring what the slide builders already do.

**Confidence: VERY HIGH** (reproduced).

Secondary worksheet defects (low severity, fix while you're in there): Section C prints the literal string `"[L1]"` instead of the language name; the doc is registered as `worksheet_pdf_path` but is actually `.source.html` (mislabeled as PDF in the email/materials row).

---

### 1.3 "Parallel" slide generation is sequential — the real speed bug

`QueueGenerationJob._run_slide_batches()` builds a list of coroutines, then awaits them **one at a time**:

```python
for filename in batch:
    tasks.append(ModifySlide(...).run())      # coroutine, NOT started
...
for t_idx, task in enumerate(tasks):
    await asyncio.wait_for(task, timeout=120) # ← awaited serially
```

A coroutine doesn't execute until awaited, and these are awaited in a sequential `for` loop. There is **no `asyncio.gather`** anywhere in the file (grep-confirmed). `BATCH_SIZE=3` therefore has **zero** effect on concurrency — it only changes how often the inter-batch `sleep(delay)` fires. The prior report's "Batch size: 3 slides per batch (parallel via asyncio.gather)" is **incorrect**.

This is why slides are 97–98% of runtime. With true batching of 3 (and DeepSeek's 2500 concurrency headroom), wall-clock for slide generation should drop roughly 3×.

**Compounding the slowness — forced sleeps everywhere:**
- `ModifySlide.run()` sleeps `SLIDE_GENERATION_DELAY` (default **3 s**) at the *start of every slide*.
- `_run_slide_batches()` sleeps `SLIDE_GENERATION_DELAY` (default **5 s**) between batches.
- Per-slide retry backoffs (`2*attempt`, `3*attempt`, plus rate-limit `15*attempt`).

For a 32-slide deck that's ~96 s of per-slide throttle + ~50 s of batch delay = **~150 s of pure sleeping** even before generation, all serialized.

**Fix:** run each batch with `await asyncio.gather(*[asyncio.wait_for(t, 120) for t in tasks], return_exceptions=True)`, and drop the per-slide `sleep` (keep a small inter-batch delay only if you actually hit TPM limits).

**Confidence: VERY HIGH** (code read; deterministic).

---

### 1.4 Proficiency level (A1–C1) is silently discarded

`QueueGenerationJob` has **no `level` field**. Yet it does:

```python
_level_val = getattr(self, "level", None) or "b1"   # always None → "b1"
```

`getattr(self, "level", ...)` can never find an attribute that isn't a declared Pydantic field, so the cache key is **always `b1`**. The level is also never threaded into the pipeline: `compute_slide_plan(grammar_data, l1_languages, age_group)` and `build_all_task_briefs(...)` take **no level argument**, and the briefs hardcode `"Level: B1"` (e.g. `slide_plan.py:431`).

Consequences:
- Every deck is built as if B1 regardless of the requested level — contradicts `CLAUDE.md` (level drives slide planning and `bestForLevels` activity filtering).
- The Master Repository cache will serve a B1 deck to an A1 request (and vice-versa) because the key ignores level.

**Fix:** add a `level` field to `QueueGenerationJob`, thread it through `_run_generation → compute_slide_plan / build_all_task_briefs`, and use it in the briefs and cache key.

**Confidence: VERY HIGH** (code read).

---

### 1.5 Production path mismatch (Railway) — broken downloads + dead cache

Files are written via `_get_mnt_path()`, which on Railway returns an **absolute** path under `$COGNIESL_DATA_DIR/mnt/<project>/...`. But the paths handed to `MarkJobComplete` (→ job DB, email links, materials table, and cache) are hardcoded **relative**:

```python
bundle_path     = f"./mnt/{project_name}/presentations/{project_name}.html"
worksheet_paths["source"] = f"./mnt/{project_name}/documents/..."
# activity, flashcards: same ./mnt/... pattern
```

Locally the process cwd is the repo root, so `./mnt/...` resolves correctly — which is exactly why every local test "passes." On Railway, the download/email resolver looks for `./mnt/...` relative to cwd (`/app`), but the files are at `/app/data/mnt/...`. Result: **broken download links / email attachments in production.**

Same bug kills the cache: `MarkJobComplete` does `Path(_primary_path).exists()` on the relative `./mnt/...` string; on Railway that's `False`, so `add_to_cache` never runs. This matches the standing note that the Master Repository / sync "has never run."

**Correction after tracing `server.py` (see §1.7):** the email download *links* are actually fine — `email_sender._build_buttons` uses only `Path(fp).name` (the basename) and the `/download/{job_id}/{filename}` endpoint rebuilds the absolute path from the env dir. So the relative `./mnt/...` strings do **not** by themselves break email downloads. The real exposure is (a) the cache never storing (§1.7-C) and (b) the deeper path-fallback inconsistency (§1.7-A). I've moved the substance of this finding into §1.7.

**Confidence: HIGH** on the code-level path inconsistency (§1.7-A); the download-link breakage I originally feared here is **downgraded** — see §1.7.

---

### 1.6 Other findings (medium / low)

- **Fallback slides bypass the validation they're held to.** When 3 attempts fail, `_generate_minimal_html_fallback()` writes a ~1.5 KB white slide with no Font Awesome and no visual content — i.e. it violates the very rules (`slide_html_utils` requires FA CDN + visual content) that real slides must pass. It's written straight to disk, unvalidated, and shipped. Acceptable as a *temporary* safety net, but it means "no blank slides" ≠ "no empty slides." **Confidence: HIGH.**
- **Email is in Resend sandbox.** `email_sender` defaults `from` to `onboarding@resend.dev`, which can only deliver to the account owner (`mitiro@gmail.com`). Confirmed; matches prior report. Needs a verified domain + `COGNIESL_FROM_EMAIL`. **Confidence: HIGH.**
- **`thin_briefs` guard is comparing the wrong things.** `if len(v) < 200 and k != slide_count` compares a slide *index* key to the *total* count to exempt the closing slide — works by accident for the last slide only, but it's fragile and not what the comment implies. **Confidence: MEDIUM** (logic smell, low impact).
- **Missing materials acknowledged in spec but not built:** no homework, no quiz; `GenerateProgressTrackerPdf` exists but is never called by the pipeline. **Confidence: HIGH** (consistent with prior report).

---

---

## 1.7 Delivery chain trace (`server.py` → email → cache)

Traced the full path from generated file to teacher download. The endpoint itself is more robust than the relative-path registration implied, but the trace surfaced three real bugs.

### 1.7-A — Three different `mnt` directory fallbacks (the headline bug here)

`COGNIESL_DATA_DIR` is read in ~18 places with **three different defaults** when it's unset:

| Behavior | Default chain | Used by (writers / readers) |
|---|---|---|
| **A. 3-tier** | env → `/app/data` (if dir exists) → repo root | `QueueGenerationJob._get_mnt_path`, `slide_file_utils.get_mnt_dir` — **writes slides, worksheet, activity** |
| **B. 2-tier** | env → repo root (no `/app/data`) | `server.py` `/download` (L311), `/slides` mount (L213-215), job slide viewer (L897), bundle (L945), material slides (L562) — **all web reads** |
| **C. /app/data only** | env → `/app/data` (no repo root) | `GenerateFlashcardPdf` (L28), `GenerateProgressTrackerPdf` (L25), `doc_file_utils` (L10) — **writes flashcards + docx/pdf** |

They only agree when `COGNIESL_DATA_DIR` is **explicitly set**. The moment it isn't:

- **Railway, var unset (volume `/app/data` exists, cwd `/app`):** writers (A, C) put files in `/app/data/mnt`, but every web read (B) looks in `/app/mnt`. **Result: every download, the `/slides` static mount, and the in-app slide viewer 404 — even though generation succeeded.**
- **Local, var unset (no `/app/data`):** slides (A) → `repo/mnt`; flashcards + docx/pdf (C) → `/app/data/mnt` (a path that doesn't exist on a Mac). Docs and slides land in different roots. The test scripts presumably set the var, which is why this never showed up in testing.

The underlying defect is that the same logic is reimplemented 3× instead of one shared `get_mnt_dir()`. **Fix:** export the 3-tier `slide_file_utils.get_mnt_dir()` and import it in `server.py`, `doc_file_utils`, and the flashcard/progress tools. Delete the other two variants.

**Confidence: VERY HIGH** (code). Whether it bites *today* depends solely on the Railway env var being set — confirm with the runtime check in §5.

### 1.7-B — Every generated document collides on one email label

All pipeline documents are written as `.source.html` (`CreateDocument` → `{name}.source.html`; worksheet, activity guide, flashcards). But `email_sender._label_for_file()` checks `name.endswith(".html")` **before** the worksheet/activity branches — and those branches require `.pdf`/`.docx`, which never match. So worksheet, activity guide, flashcards **and** the slide bundle all render as the same button:

> 🎬 Download Presentation (HTML — full animations, works offline)

The teacher sees 3–4 identical-looking buttons and can't tell the worksheet from the activity guide from the deck. The `.pdf`/`.docx` label branches are dead code for the current pipeline. **Fix:** match on the `worksheet`/`activity`/`flashcard` substrings before the generic `.html` fallback. **Confidence: VERY HIGH** (code).

### 1.7-C — Master Repository cache is never written (confirms the standing note)

`MarkJobComplete` sets `_primary_path = self.html_bundle_path` = the relative `./mnt/.../x.html`, then gates caching on `Path(_primary_path).exists()`. That resolves against the process cwd. On Railway (cwd `/app`, files at `/app/data/mnt`) it's always `False`, so `add_to_cache` never runs. This is the concrete reason the "sync to CogniESL / Master Repository has never run." **Fix:** resolve the bundle dir via `get_mnt_dir()` (absolute) before the existence check. **Confidence: HIGH** (code).

### 1.7-D / E — lower severity
- **Bundle is 113–126 MB** (every image base64-inlined into one HTML), served as an email download link. Real risk of Railway response timeouts / egress limits and email-client link issues. Concern, not a logic bug. **Confidence: MEDIUM.**
- **Download is allowed while `status == "running"`** (`/download`, `/bundle.html`, `/slides` viewer all accept `running`). A teacher can fetch a half-generated or not-yet-written bundle mid-run. **Confidence: HIGH** (code); **LOW-MEDIUM** impact.
- **Slide enumeration is inconsistent:** material-slides endpoint globs `slide_{i:02d}*.html` (handles label suffixes) but the job bundle/slides endpoints use exact `slide_{i:02d}.html`. Fine for the current flat naming; fragile if labeled filenames return. **LOW.**

---

## 2. Where the prior report was wrong or incomplete

Per your instruction not to trust its results:

- ❌ "Slides generated in parallel via `asyncio.gather` (batch 3)." — **False.** Fully sequential; no `gather`.
- ❌ Worksheet cause given as "data isn't being inserted… YAML loads correctly (verified by the activity guide which DOES contain content from the same data)." — **Misleading.** The activity guide reads `teaching.*` (different keys that *do* exist); the worksheet's emptiness is two specific key/shape mismatches. "Same data" is not the same keys.
- ❌ L1 Oracle marked as passing in the validation checklist. — **False.** L1 briefs receive 0 patterns; any L1 content on those slides is model-invented.
- ⚠️ Missed entirely: level being dropped (1.4), the Railway absolute/relative path mismatch (1.5), and the cache-never-stored consequence.
- ✅ Correct: worksheet is empty (symptom), email sandbox, fallback slides exist, generation too slow.

---

## 3. Recommended fix order (highest ROI first)

1. **Flatten the L1 tool result** in `_load_yaml_data` (§1.1). One change; restores L1 Oracle slides, worksheet Section C, and flashcards. *This is the value-prop fix — do it first.*
2. **Worksheet `error`/`correction` keys** (§1.2). Restores Sections A/B and answer key.
3. **True batching with `asyncio.gather` + drop per-slide sleep** (§1.3). ~3× faster.
4. **Thread `level` through** the tool, pipeline, briefs, and cache key (§1.4).
5. **Unify path resolution** (§1.7-A): one shared `get_mnt_dir()` imported everywhere; delete the 2 divergent copies. This also fixes the cache (§1.7-C). Highest-risk infra item.
6. **Fix email labels** (§1.7-B) — one-function change so the teacher can tell the files apart.
7. Verified email domain; validate fallback slides or flag them as degraded; gate downloads on `status == "done"` only (§1.7-E); reconsider the 124 MB bundle as a download link (§1.7-D); wire up progress tracker if in scope.

Each of 1–4 is independently verifiable with a tiny repro (the §1.1/§1.2 repros are already written and pasted above).

---

## 4. Confidence summary

| # | Finding | Severity | Confidence | Verified by |
|---|---|---|---|---|
| 1.1 | L1 Oracle / worksheet / flashcards get no L1 data (nested `data`) | Critical | Very High | Reproduced w/ real YAML |
| 1.2 | Worksheet `common_errors` key mismatch (`error`/`correction`) | Critical | Very High | Reproduced w/ real YAML |
| 1.3 | "Parallel" batch is sequential; forced sleeps | High (perf) | Very High | Code read, deterministic |
| 1.4 | Proficiency level discarded; hardcoded B1 | High | Very High | Code read |
| 1.7-A | 3 inconsistent `mnt` fallbacks → 404s if env unset | High | Very High | Code read; needs Railway check |
| 1.7-B | All docs collide on one email label ("Presentation") | Medium | Very High | Code read |
| 1.7-C | Master Repository cache never written | Medium-High | High | Code read |
| 1.7-D | 124 MB bundle as email download link | Medium | Medium | Code + prior sizes |
| 1.7-E | Downloads served while job still "running" | Low-Med | High | Code read |
| 1.6a | Fallback slides bypass validation, shipped empty | Medium | High | Code read |
| 1.6b | Email stuck in Resend sandbox | Medium | High | Code read |
| 1.6c | `thin_briefs` index-vs-count comparison | Low | Medium | Code read |
| 1.6d | Homework/quiz absent; progress tracker uncalled | Low | High | Code read |

---

## 5. Suggested runtime confirmations (to close the two open items)

- **§1.5 production:** on Railway, print `os.getcwd()`, `os.getenv("COGNIESL_DATA_DIR")`, and `_get_mnt_path("x")` from inside `_run_generation`; then confirm whether the download endpoint can open one registered `./mnt/...` path. If cwd ≠ the data dir, downloads are broken in prod.
- **§1.3 perf:** after switching to `gather`, time a 30-slide deck; expect a ~3× drop in the slide phase.
