# CogniESL Pipeline Optimization Plan

**Date**: 2026-06-03
**Status**: Active — execution in progress
**Owner**: Marcos / Claude Code
**Target**: Complete generation (slides + worksheet + activity guide) in under 8 minutes wall-clock

---

## Problem Statement

The CogniESL pipeline takes 15-25 minutes to generate complete teaching materials from teacher request to delivery. This is too slow for a production SaaS product — teachers expect results in minutes, not half an hour.

## Diagnosis

### Current Pipeline (18-28 minutes)

| Phase | Steps | LLM Calls | Time |
|-------|-------|-----------|------|
| Chat interview | Requirements gathering | 2-4 | ~30s |
| Content Brief | DB searches + brief generation | 1 | ~30s |
| Approval → Queue | Server processing | 1 | ~6s |
| **Background: Slides** | Planner + 17× ModifySlide | 18 | **8-12 min** |
| Cooling period | Artificial wait | 0 | **3 min** |
| **Background: Documents** | Worksheet + Activity Guide | 2-4 | **3-6 min** |
| Final assembly | Bundle + validation + email | 1 | ~30s |

### True Bottlenecks (ranked by impact)

1. **17 sequential ModifySlide calls** — ~7-10 min of generation time. Each call: fresh sub-agent (48KB sys prompt) → LLM generates full HTML → validate → embed images → write file. No parallelism.
2. **SLIDE_GENERATION_DELAY=5** — 85s of pure waiting between slides. Legacy from OpenAI TPM limits; irrelevant on DeepSeek.
3. **3-minute cooling period** — 180s wait before document generation. Same legacy reason.
4. **Post-write retry loop** — up to 9 extra LLM calls per small slide. Rarely triggered, wasteful when it is.
5. **Main agent assembles task_briefs via LLM** — slow and fragile. The LLM reads 34K chars of DATABASE_CONTENT and writes 17 task_briefs. Python could do this directly.
6. **48KB html_writer_instructions sent every call** — no prompt caching on DeepSeek means every call processes the full instruction set.

### What's NOT the problem

- Chat interview speed (~4.9s first response, ~30s to brief — fine)
- Database search (local YAML reads — milliseconds)
- Image embedding (milliseconds per slide)
- Validation (file checks — 1-2s total)
- BuildOfflineBundle (single HTML assembly — 10-30s)
- "Wrong model" for chat — DeepSeek-V4-flash handles conversation well

---

## Strategy: Three Phases

### Phase 0 — Quick Wins (no architecture changes, minimal risk)

**Target: ~8-12 min → ~6-8 min**

| # | Change | File | Effort | Saves |
|---|--------|------|--------|-------|
| 0.1 | `SLIDE_GENERATION_DELAY=0` | `.env` | Trivial | ~85s |
| 0.2 | Remove "wait 3 minutes" from instructions | `instructions.md` | Trivial | ~180s |
| 0.3 | Skip ImageSearch/DownloadImage for hook | `instructions.md` | Trivial | ~10-15s |
| 0.4 | Set sub-agent model to fastest available | `.env` | Trivial | ~30-60s |

**Total Phase 0**: ~4-6 min saved

### Phase 1 — Code Optimizations (medium effort, medium risk)

**Target: ~6-8 min → ~3-5 min**

| # | Change | File | Effort | Saves |
|---|--------|------|--------|-------|
| 1.1 | Remove post-write retry loop (or reduce to 1 round) | `ModifySlide.py` | Low | ~0-90s |
| 1.2 | Parallelize independent slides using existing DAG | `ModifySlide` / orchestration | Medium | ~3-5 min |
| 1.3 | Generate slides + documents concurrently | `QueueGenerationJob.py` | Medium | ~2-5 min |
| 1.4 | Warm-start background agent (pass context from main thread) | `QueueGenerationJob.py` | Low | ~10-20s |
| 1.5 | YAML in-memory cache (load at startup) | `server.py` + `config.py` | Low | ~1-2s |

**Total Phase 1**: ~5-10 min saved

### Phase 2 — Architecture (significant effort, significant risk, biggest impact)

**Target: ~3-5 min → ~1-3 min**

| # | Change | Description | Risk | Saves |
|---|--------|-------------|------|-------|
| 2a | **Template-based HTML** | Pre-define HTML templates per slide type. LLM outputs only content JSON (CCQ text, wrong/correct pairs). Python injects into templates. | Medium — rewrites ModifySlide, but bottom half of generation | ~4-6 min |
| 2b | **Python constructs task_briefs** | Eliminate main-agent task_brief generation. Python maps YAML to 17 task_briefs deterministically from a slide plan. | Medium — complex refactor of `_run_generation()` | ~2-3 min + quality |
| 2c | **Warm generation on chat** | When teacher starts describing topic, kick off background generation immediately. If they approve, slides are ready in seconds. | Low — token waste on unapproved runs | Eliminates perceived wait |

**Recommended approach**: 2b → 2a → 2c in sequence. Python task_briefs fix the quality consistency problem AND speed. Template-based HTML is the biggest speed lever. Warm generation is a UX bonus on top.

---

## Infrastructure Fix (from Other Agent's Finding)

### Job Recovery on Server Startup

**Problem**: Railway auto-deploys kill background threads mid-generation. The SQLite job stays "running" forever even though files exist on the volume.

**Fix**: On server startup (`server.py`), scan for jobs with `status='running'` and check if their files exist on disk. If so, auto-complete them.

**Priority**: Medium — important for reliability, doesn't affect generation speed.

### Railway Deploy Management

**Problem**: Any git push triggers automatic redeploy, killing in-flight generations.

**Fix**: Use Railway's manual deploy mode during generation testing. Or separate the web process and the worker process into different Railway services.

---

## Execution Order

```
Week 1:
  Day 1: Phase 0 — quick wins (30 min of work)
         Test: single run with timing capture
  Day 2: Infrastructure — job recovery on startup
         Test: kill container mid-gen, restart, verify recovery
  Day 3: Phase 1 — parallel slides + document concurrency
         Test: run with timing capture, verify quality
  Day 4-5: Phase 2a or 2b — start template/Python refactor
         Test: compare output quality with current pipeline

Week 2:
  Day 1-2: Finish Phase 2, full integration test
  Day 3: Quality audit — examine actual slide HTML
  Day 4: Polish + deploy
  Day 5: Final timing verification with teacher-facing estimate
```

---

## Implementation Status (2026-06-03)

### ✅ Completed Changes

| # | Change | File | Status |
|---|--------|------|--------|
| 0.1 | `SLIDE_GENERATION_DELAY=0` | `.env` | ✅ |
| 0.2 | Remove "wait 3 minutes" from instructions | `instructions.md` | ✅ |
| 0.3 | Skip ImageSearch/DownloadImage for hook | `instructions.md` | ✅ (auto-fallback) |
| 0.4 | Set sub-agent model to fastest available | `.env` | ✅ (deepseek-v4-flash) |
| 1.1 | Remove post-write retry loop (9→2 attempts) | `ModifySlide.py` | ✅ |
| 1.5 | Python-driven task_brief construction | `slide_plan.py` (NEW) | ✅ |
| 1.2 | Parallel slides via DAG (3 at a time) | `QueueGenerationJob.py` | ✅ |
| 1.3 | Parallel documents + slides generation | `QueueGenerationJob.py` | ✅ (inline in flow) |
| — | Removed background agent dependency | `QueueGenerationJob.py` | ✅ |
| — | Job recovery on server startup | `server.py`, `jobs.py` | ✅ |
| — | Structured task_brief builder for A0-A8 | `slide_plan.py` | ✅ |
| — | Deterministic slide planner (no LLM) | `slide_plan.py` | ✅ |
| — | Programmatic worksheet/activity builder | `QueueGenerationJob.py` | ✅ |

### Architecture Change

**Before:** Background thread → create fresh agent → agent calls InsertNewSlides planner (LLM) → agent calls ModifySlide × 17 sequentially → agent calls Validate/Build/Docs → MarkJobComplete

**After:** Background thread → Python loads YAML dicts → slide_plan.compute_slide_plan() → Python creates placeholders → asyncio.gather(ModifySlide × 3 in parallel) → Python calls Validate/Build/Docs/Flashcards → MarkJobComplete

Zero LLM calls in the background thread. All generation is Python-driven BaseTool calls.

### Pending Work

| # | Change | Effort | Notes |
|---|--------|--------|-------|
| 2a | Template-based HTML (content JSON → injected into templates) | Medium | Would reduce ModifySlide LLM calls by ~80% |
| 2c | Warm generation on chat | Low | UX improvement — fires before approval |
| — | Hook image download via Python | Low | Currently skipped (graceful fallback) |

## Success Criteria

| Metric | Current | Target | Measure |
|--------|---------|--------|---------|
| First response | ~5s | < 3s | Server log |
| Content Brief visible | ~30s | < 20s | Server log |
| Approval → slides done | ~8-12 min | < 4 min | Background job timer |
| Full delivery (slides + docs) | ~15-25 min | < 8 min | Teacher timestamp |
| Slide content quality | Verbally correct | No thin slides | ValidateSlideSet |
| Teacher perception | "Too long" | "Fast enough" | N/A |

---

## Tools & Debugging Commands

```bash
# Run app locally for testing
python server.py

# Check logs for timing
grep "slide_01\|PROCEED_WITH_GENERATION\|MarkJobComplete" /app/logs/app.log

# Manual timing capture
# Add this to server.py's chat endpoint:
#   start = time.time()
#   ...
#   logging.info(f"[{session_id}] CHAT_TURN: {time.time() - start:.2f}s")
```
