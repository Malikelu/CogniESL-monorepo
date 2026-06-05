# CogniESL — Audit Consolidation 2

**Date:** 2026-06-04  
**Sources:** `AUDIT_REPORT_2026-06-04.md` (prior report) + `INDEPENDENT_AUDIT_2026-06-04.md` (independent re-audit)  
**Purpose:** Single source of truth — reconciling both reports, resolving disagreements, and producing a final execution plan.

---

## Where Both Reports Agree

These findings are confirmed by both audits with high confidence. No dispute.

| Finding | Severity | Both reports say |
|---|---|---|
| Worksheet content is empty | CRITICAL | Yes — empty Sections A, B |
| Slide batches are sequential (not parallel) | HIGH | Yes — awaited one at a time, ~3× slower |
| Email stuck in Resend sandbox | MEDIUM | Yes — can only deliver to `mitiro@gmail.com` |
| Literal `[L1]` never replaced in worksheet Section C | MEDIUM | Yes — hardcoded string, not the language name |
| Progress tracker tool exists but is never called | LOW | Yes — `GenerateProgressTrackerPdf` is dead code in the pipeline |

---

## Where They Disagreed — And Who Was Right

### Disagreement 1: L1 Oracle — PASSING or BROKEN?

**Prior report:** Marked L1 Oracle as passing in its validation checklist.

**Independent audit:** L1 Oracle slides receive **zero real interference data**. The L1 tool returns `{"language": "...", "grammar_point": "...", "data": {...real content...}}` but every consumer reads interference fields from the **top level** of that dict, where they don't exist. The model is then forced to invent L1 content — exactly what `CLAUDE.md` forbids. Independently reproduced: 0 patterns extracted vs. 2 patterns available.

**Verdict: Independent audit is correct.** This is the most critical bug in the system. The prior report missed it because the slides look visually populated — they have content, it's just AI-invented rather than database-sourced. This silently violates the product's core promise.

---

### Disagreement 2: "Parallel via asyncio.gather" — True or False?

**Prior report:** Stated slide generation runs "parallel via `asyncio.gather` (batch 3)."

**Independent audit:** There is no `asyncio.gather` anywhere in the file (grep-confirmed). Each slide is awaited sequentially in a `for` loop. `BATCH_SIZE=3` affects only how often the inter-batch `sleep` fires, not concurrency.

**Verdict: Independent audit is correct.** The prior report's claim was false. Sequential execution plus forced per-slide sleeps account for the 10-minute generation times.

---

### Disagreement 3: Worksheet root cause — one bug or two?

**Prior report:** Attributed empty worksheet to a single root cause — wrong field names (`wrong`/`correct` instead of `error`/`correction`).

**Independent audit:** Found **two independent root causes**: (1) the L1 data nesting bug (`data` wrapper not unwrapped) which empties Section C; (2) the same key-name mismatch for grammar errors which empties Sections A/B and the answer key.

**Verdict: Independent audit is more complete.** Both bugs need to be fixed. The prior report correctly identified bug #2 but missed bug #1 (because bug #1 is the same root cause as the L1 Oracle failure — fixing §1.1 fixes both at once).

---

### Disagreement 4: Email download links — broken or fine?

**Prior report:** Did not specifically analyze download links.

**Independent audit:** Initially flagged relative `./mnt/...` paths as breaking email downloads, then **self-corrected** after tracing `server.py`: `email_sender._build_buttons` uses only `Path(fp).name` and the `/download/{job_id}/{filename}` endpoint reconstructs the absolute path. Email download links are fine.

**Verdict: Download links themselves are not broken.** The real exposure is the cache never storing (§1.7-C) and the three inconsistent `mnt` fallback paths (§1.7-A) which break everything else on Railway if `COGNIESL_DATA_DIR` is unset.

---

## What Each Report Uniquely Contributed

### Independent audit found — missed entirely by prior report

| Finding | Severity |
|---|---|
| L1 Oracle gets zero real data (nested `data` unwrap) | CRITICAL |
| Proficiency level silently discarded — hardcoded B1 everywhere | HIGH |
| Three inconsistent `mnt` directory fallbacks → Railway 404s if env unset | HIGH |
| All email deliverables render as the same "Download Presentation" button | MEDIUM |
| Master Repository cache never written (concrete path confirmed) | MEDIUM-HIGH |

### Prior report found — missed by independent audit

| Finding | Severity |
|---|---|
| Empty "Watch for" lines in A5/A7/A8 speaker notes | MEDIUM |
| Verbose `error` field descriptions contaminate task briefs | MEDIUM |
| Post-write retry discards `previous_failed_html` (regenerates blind) | MEDIUM |
| Font pairing broken — heading/body selected independently from curated pairs | LOW |
| Two incompatible model routing systems (LiteLLM vs direct AsyncOpenAI) | MEDIUM |
| Duplicate DeepSeek client code in ModifySlide + InsertNewSlides | LOW |
| Daemon threads lose in-progress work on Railway redeploy | MEDIUM |
| No YAML schema validation — silent data loss is structural, not just cosmetic | HIGH |
| Stale slide files from previous runs may interfere | LOW |
| Kickoff detection uses 30 hardcoded phrases — fragile | LOW |
| Substring L1 matching ("Russian" matches "Prussian") | LOW |
| Theme failure silently ignored without deterministic fallback | LOW |

---

## Final Finding Inventory

Consolidated list, deduplicated, with agreed severity and confidence.

| # | Finding | Severity | Confidence | Source |
|---|---|---|---|---|
| **F1** | L1 Oracle gets zero real data — `data` nesting not unwrapped | CRITICAL | Very High | Independent |
| **F2** | Worksheet Sections A/B/Answer Key empty — `error`/`correction` key mismatch | CRITICAL | Very High | Both |
| **F3** | Slide generation is sequential, not parallel; forced sleeps add ~150 s overhead | HIGH | Very High | Both |
| **F4** | Proficiency level discarded; every deck hardcoded B1 in plan + cache key | HIGH | Very High | Independent |
| **F5** | Three inconsistent `mnt` fallback paths → 404s on Railway if env var unset | HIGH | Very High | Independent |
| **F6** | No YAML schema validation — field-name mismatches cause silent empty output | HIGH | Medium | Prior |
| **F7** | Master Repository cache never written (relative path check fails on Railway) | MEDIUM-HIGH | High | Independent |
| **F8** | All email deliverables labeled identically — teacher can't distinguish worksheet from deck | MEDIUM | Very High | Independent |
| **F9** | Two model routing systems (LiteLLM vs. direct AsyncOpenAI) — inconsistent retry/error handling | MEDIUM | High | Prior |
| **F10** | Post-write retry discards `previous_failed_html=None` — model regenerates blind | MEDIUM | High | Prior |
| **F11** | Daemon threads lose in-progress work on Railway redeploy | MEDIUM | High | Prior |
| **F13** | Literal `[L1]` never replaced in worksheet Section C | MEDIUM | High | Both |
| **F14** | Empty "Watch for" lines in A5/A7/A8 — missing `error` in fallback chain | MEDIUM | High | Prior |
| **F15** | `error` field values are verbose descriptions, not clean sentences | MEDIUM | High | Prior |
| **F16** | Email stuck in Resend sandbox — can only deliver to `mitiro@gmail.com` | MEDIUM | High | Both |
| **F17** | Fallback slides bypass validation and are shipped (empty visual content) | MEDIUM | High | Independent |
| **F18** | Duplicate DeepSeek client code (ModifySlide + InsertNewSlides) | LOW | High | Prior |
| **F19** | Font pairing broken — heading/body selected from different random pairs | LOW | High | Prior |
| **F20** | Stale slide files from previous runs may map to wrong task briefs | LOW | Medium | Prior |
| **F21** | Kickoff detection: 30 hardcoded phrases — any new phrase escapes undetected | LOW | High | Prior |
| **F22** | Substring L1 matching ("Russian" in "Prussian") — fragile with current 36-language set | LOW | Medium | Prior |
| **F23** | Theme failure silently ignored — no deterministic fallback CSS | LOW | High | Prior |
| **F24** | Progress tracker tool exists but is never called by pipeline | LOW | High | Both |
| **F25** | 124 MB HTML bundle served as email download — Railway timeout / egress risk | LOW-MED | Medium | Independent |
| **F26** | Downloads served while `status == "running"` — teacher may fetch partial deck | LOW | High | Independent |

---

## Proposed Execution Plan

Grouped by root cause to minimize total changes. Each group has a verification step.

---

### Sprint 1 — Restore the value proposition (1–2 days)

**Goal:** Real database content in L1 Oracle, worksheet, and flashcards. This is the product's core promise.

**F1 — Unwrap L1 tool result** (`QueueGenerationJob._load_yaml_data`)

```python
result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
if isinstance(result, dict) and "data" in result and isinstance(result["data"], dict):
    merged = {**result["data"], "language": result.get("language", l1),
              "grammar_point": result.get("grammar_point")}
    l1_data_list.append(merged)
elif isinstance(result, dict):
    l1_data_list.append(result)
```

**F2 — Fix worksheet key names** (`_build_worksheet_html`, lines 371, 383, 413)

Mirror what `slide_plan.py` already does: add `error`/`correction` as first fallbacks before `wrong`/`correct`.

**F13 — Fix literal `[L1]`** in Section C header (one-line f-string fix).

**F14 — Fix empty "Watch for" lines** in A5/A7/A8 (add `error` to 3 fallback chains).

**Verify Sprint 1:** Generate Present Simple + Spanish. Confirm: (a) L1 Oracle slide brief shows ≥ 1 pattern from the database (not generic text), (b) Worksheet Section A has real sentences, (c) "Watch for" line in speaker notes is non-empty.

---

### Sprint 2 — Speed (1 day)

**Goal:** ~3× faster generation.

**F3 — True parallel batching** (`_run_slide_batches`)

Replace the sequential `for t_idx, task in enumerate(tasks): await asyncio.wait_for(task, 120)` loop with:

```python
results = await asyncio.gather(
    *[asyncio.wait_for(t, 120) for t in tasks],
    return_exceptions=True
)
```

Drop the per-slide `SLIDE_GENERATION_DELAY` sleep; keep a small inter-batch delay (1–2 s) only if rate limits appear.

**Verify Sprint 2:** Time a 30-slide deck before and after. Expect slide phase to drop from ~10 min to ~3–4 min.

---

### Sprint 3 — Level + content quality (1 day)

**Goal:** Decks reflect the requested proficiency level.

**F4 — Thread `level` through the pipeline**

1. Add `level: str = "b1"` field to `QueueGenerationJob`
2. Pass it into `compute_slide_plan` and `build_all_task_briefs`
3. Use it in the cache key (replace hardcoded `b1`)
4. In the brief builders, replace hardcoded `"Level: B1"` with the dynamic value

**F15 — Verbose `error` field in task briefs**

Add `_extract_wrong_sentence(error_str)` helper that strips the descriptive prefix before the `*'...'` pattern. Use in A5/A7/A8 brief builders. (This is a quality improvement — do not block Sprint 3 on it.)

**Verify Sprint 3:** Generate A1 deck. Confirm cache key differs from B1 run, and slide briefs reflect A1 vocabulary/complexity.

---

### Sprint 4 — Infrastructure (1–2 days)

**Goal:** Railway deployment is reliable; cache actually works; teacher gets labeled downloads.

**F5 — Unify mnt path resolution**

Export `slide_file_utils.get_mnt_dir()` (the 3-tier logic). Replace all other variants in `server.py`, `doc_file_utils`, flashcard/progress tools. Delete the 2 divergent copies.

**F7 — Fix cache existence check**

In `MarkJobComplete`, resolve `_primary_path` via `get_mnt_dir()` (absolute) before the `Path.exists()` gate that guards `add_to_cache`.

**F8 — Fix email document labels**

In `email_sender._label_for_file()`, check `worksheet`/`activity`/`flashcard` substrings before the generic `.html` fallback. Teachers will finally see correctly labeled buttons.

**Verify Sprint 4:** On Railway (or simulating Railway env without `COGNIESL_DATA_DIR` set), confirm: (a) downloads resolve correctly, (b) a second identical generation request is served from cache, (c) email has 4 distinctly labeled buttons.

---

### Sprint 5 — Polish and resilience (as capacity allows)

Lower-severity items. No strict order.

- **F6 (YAML schema):** Add Pydantic models for grammar/L1/activity YAML. Validate at load time. This makes F1/F2/F14 structurally impossible to reintroduce. High long-term value.
- **F16 (email domain):** Set `COGNIESL_FROM_EMAIL` to a verified domain so non-Marcos teachers receive email.
- **F19 (font pairing):** One-line fix — `pair = random.choice(_FONT_PAIRS)`, then use `pair[0]` and `pair[1]` together.
- **F10 (retry context):** Pass `previous_failed_html=final_html` in the post-write retry so the model sees what it generated.
- **F9 (model routing):** Consolidate on direct `AsyncOpenAI` — extract shared `deepseek_client.py`, remove LiteLLM from `config.py`.
- **F17 (fallback slides):** Run `slide_html_utils` validation on fallback-generated slides before shipping; flag as degraded if they fail.
- **F11 (daemon threads):** Add slide-count checkpoint to manifest after each batch so recovery can report "28/32 done" instead of all-or-nothing.
- **F21 (kickoff detection):** Replace 30-phrase blacklist with: `if len(text.strip()) < 300 and no tool calls → treat as kickoff`.
- **F24 (progress tracker):** Wire `GenerateProgressTrackerPdf` into the background pipeline as a final step.
- **F25/F26:** Gate `/download` on `status == "done"` only. Evaluate HTML bundle size; consider splitting images.

---

## Summary Assessment

The pipeline is architecturally sound. The 10-step structure is logical, crash recovery is reasonable, validation is thorough. The problems are concentrated in three areas:

**Data contract mismatches** (F1, F2, F6, F13, F14, F15) — one shared root: no enforced schema between YAML producers and consumers. The L1 nesting mismatch is the most damaging because it silently strips the product's entire differentiator from every output.

**Performance** (F3) — one-line fix; ~3× gain.

**Infrastructure** (F4, F5, F7, F8) — scattered path-resolution variants and a dropped `level` field. Fixable in one focused infra sprint.

**Sprints 1–4 will take the system from "runs but ships wrong content" to "ships correct, differentiated, fast, deployable materials."**
