# CogniESL — Handover Document

> Written 2026-06-04 for handoff to a fresh agent.  
> Purpose: Document all known bugs, failed fixes, architecture decisions, and test results so a new agent can pick up without repeating mistakes.

---

## 1. The Core Problem

**A full generation run (Present Simple, Spanish adults, all materials) takes 44 minutes and produces incomplete materials.**

- 24 slides planned → 23 generated, 1 blank (timeout)
- Worksheet and Activity Guide created as local `.source.html` files but never registered in the downloadable file list
- No email sent (Resend sandbox limitation)
- `/api/materials` returns empty — no materials are registered

At this speed, no teacher would use the product. The system is not production-ready.

---

## 2. Architecture Overview

```
Teacher sends request → FastAPI /cogniesl/get_response
  → Agent (OpenAI Agents SDK + agency_swarm) generates Content Brief
    → Teacher approves → QueueGenerationJob tool is called
      → Background thread spawns _run_generation()
        → Steps 1-10 pure Python pipeline (NO agent after step 4)
```

### Slide Generation Pipeline (the 44-minute path)

```
Step 1: Load YAML data          (fast, <1s)
Step 2: Compute slide plan      (fast, <1s)
Step 3: Create blank placeholders (fast, <1s)
Step 3b: Generate theme DNA     (fast, <1s)
Step 4: Generate 24 slides via ModifySlide (the 44-minute part)
  → For EACH slide:
    → _make_html_writer_agent() creates a new Agent object
      → Agent wraps model in LitellmModel("deepseek/deepseek-v4-flash")
        → get_response() → agents SDK loop → LiteLLM Python library
          → POST to api.deepseek.com/v1/chat/completions
    → Up to 5 retries with validation
    → Post-write size check (< 4000B triggers another 3 retry round)
Step 5: ValidateSlideSet
Step 6: BuildOfflineBundle       (writes ~90MB HTML file)
Step 7-9: Documents (worksheet + activity guide)
Step 10: MarkJobComplete
```

### Model Routing

```
_modifySlide.py:_make_html_writer_agent()
  → LitellmModel(model="deepseek/deepseek-v4-flash", api_key=DEEPSEEK_API_KEY)
    → LiteLLM Python library parses the "deepseek/" prefix
      → POST to https://api.deepseek.com/v1/chat/completions
```

DeepSeek's API is OpenAI-compatible. The `deepseek/` prefix is a LiteLLM convention.  
LiteLLM is not needed — we could call `AsyncOpenAI(api_key=..., base_url="https://api.deepseek.com/v1")` directly.  
But LiteLLM overhead is negligible (<100ms). The real slowdown is DeepSeek API response time per slide.

`config.py` also uses LitellmModel via `_resolve()` for the main agent's model. Not needed for OpenAI-compatible APIs.

---

## 3. Known Bugs

### BUG-1: Blank slides due to batch timeout (FIXED but root cause remains)

**Discovery**: Run 4 (job 73f7ff0b) produced 7 blank slides (slides 04, 14, 15, 16, 17, 18, 21), each 106 bytes.

**Root cause**: `asyncio.wait_for(asyncio.gather(*tasks), timeout=120)` with BATCH_SIZE=2. When 120s timeout fired, it caught TimeoutError but all results from that batch were lost. Two slow slides could corrupt up to 4 slides.

**Fix applied**: Changed to BATCH_SIZE=1 with per-slide `asyncio.wait_for(task, timeout=300)` and individual try/except. One slow slide now only corrupts itself.

**Result after fix**: Test run d6396171 produced 1 blank slide (slide 15) instead of 7. Improvement but still broken — every blank slide makes the product unusable.

### BUG-2: Process crash during bundle build (FIXED — memory issue)

**Discovery**: Run 4 generated all 24 slides, bundle step processed all 24, then container restarted. No Python traceback — process was killed externally.

**Root cause**: Two possibilities:
1. **OOM**: Railway hobby tier has 1 GB memory limit. The old `BuildOfflineBundle.py` built one giant in-memory string (slide HTML + inlined Google Fonts WOFF2 + Font Awesome data URIs). A 90MB bundle file means several MB in memory at once.
2. **Railway health check timeout**: If health check runs and the process doesn't respond quickly enough, Railway restarts it.

**Fix applied**: Rewrote `BuildOfflineBundle.py` to write progressively to a temp file, avoiding giant in-memory string allocation. Uses `os.rename(tmp_path, out_path)` for atomic write. Added `_font_cache` module-level dict to avoid re-fetching fonts across slides.

**Result**: Test run d6396171 completed bundle successfully (90MB HTML file written).

### BUG-3: Pipeline progress tracking not working correctly (FIXED)

**Discovery**: After Run 4 crash, had no way to determine where the pipeline died.

**Fix applied**: Added `_write_progress()` function with threading lock that writes timestamped lines to `{mnt}/{project}/.pipeline_progress`. Inserted at all 10 pipeline steps and at PIPELINE FAILED/COMPLETE.

**Remaining issue**: The progress file writes to the same directory as the project. If the directory path changes between the job record creation and the pipeline execution (see BUG-6), the progress file is written to the wrong path.

### BUG-4: Project name mismatch between job record and filesystem (UNRESOLVED)

**Discovery**: Test run d6396171 creates a project folder `present_simple_spanish_adults_activity` on disk, but the job record might use a different name. The API returns `project_name: "present_simple_spanish_adults_activity"` which works for the bundle but is not the same as what QueueGenerationJob was called with.

**Impact**: Unclear. The project name is generated by the Content Brief agent, not by QueueGenerationJob consistently. If they diverge, MarkJobComplete can't find the files.

### BUG-5: Documents created but not downloadable (UNRESOLVED)

**Discovery**: `CreateDocument` saves `.source.html` files to `{mnt}/{project}/documents/`, but these paths are never passed to `MarkJobComplete` or added to the job's `file_paths` list. The pipeline code builds paths like:
```python
worksheet_paths["source"] = f"./mnt/{project}/documents/{project_name}_worksheet.source.html"
activity_paths["source"] = f"./mnt/{project}/documents/{project_name}_activity_guide.source.html"
```
But these dicts are never used — the code path to include them in `_get_slide_files_list()` or the final file list does not exist.

**Result**: `/api/materials` returns `{"materials": [], "total": 0}`. The teacher cannot download worksheet or activity guide.

### BUG-6: Email delivery broken (UNRESOLVED — sandbox limitation)

**Discovery**: Resend API key in use is in sandbox mode. Only emails to the verified sender (mitiro@gmail.com) are delivered. Emails to test@cogniesl.com fail silently.

**Impact**: In production, teachers would never receive their download links. Need to verify sender domain in Resend or use a different email provider.

### BUG-7: Validation passes but reports failure (MINOR)

**Discovery**: ValidateSlideSet logs "90 validation checks passed" but overall validation result reports failure. This is likely because:
- 23/24 slides have speaker notes (slide 15 blank, missing notes)
- Slide size checks fail on the blank slide

**Impact**: The error message is confusing but doesn't block pipeline completion. It's logged and ignored.

---

## 4. Failed Fix Attempts

### Attempt 1: asyncio batch timeout (partial fix)
- **Goal**: Prevent one slow slide from corrupting batch mates
- **Change**: BATCH_SIZE=2 → BATCH_SIZE=1, 120s → 300s per-slide timeout
- **Result**: Blank slides reduced from 7 to 1. But 300s timeout means a single failed slide adds 5 minutes of waiting.
- **Verdict**: Treats symptom, not cause. The model should complete a slide in 10-30s, not 300s.

### Attempt 2: Progressive memory write for bundle builder (successful)
- **Goal**: Prevent OOM during bundle construction
- **Change**: Rewrote BuildOfflineBundle.py to write incrementally via temp file
- **Result**: Bundle builds successfully now. Previously it crashed the container.
- **Verdict**: Fix works. Required change.

### Attempt 3: Pipeline progress tracking (partially helpful)
- **Goal**: See where pipeline crashes
- **Change**: Added _write_progress() at all pipeline steps
- **Result**: Worked for determining how far the pipeline got. But doesn't survive container restarts if the progress file was never flushed.
- **Verdict**: Helpful for debugging, not essential.

### Attempt 4: Model switch to DeepSeek v4 flash (THE PROBLEM)
- **History**: Originally used DeepSeek via OpenRouter. Then was switched to DeepSeek v4 flash via LiteLLM.
- What the user is angry about: The session burned credits on OpenRouter/other APIs without authorization.
- **Current state**: Using `deepseek/deepseek-v4-flash` via `LitellmModel` with `DEEPSEEK_API_KEY`. Each slide takes 60+ seconds.

---

## 5. Test Results Summary

| Run | Job ID | Model | Slides | Blank | Bundle | Docs | Duration |
|-----|--------|-------|--------|-------|--------|------|----------|
| 4 | 73f7ff0b | DeepSeek v4 flash | 24 planned, 17 real, 7 blank | 7 | No (crash) | No | ~21min visible, crash at end |
| 5 | d6396171 | DeepSeek v4 flash | 24 planned, 23 real, 1 blank | 1 | Yes (90MB) | .source.html only | 44 min |

---

## 6. Root Cause Analysis: Why 44 Minutes?

The pipeline has a **chain of sequential bottlenecks**:

| Step | Time | Why |
|------|------|-----|
| 24 ModifySlide calls | ~42 min | Average ~105s per slide, 24 slides sequential (BATCH_SIZE=1) |
| BuildOfflineBundle | ~30s | Reading 24 files, fetching fonts, writing 90MB |
| CreateDocument ×2 | ~10s | Writing two .source.html files |
| Validate + MarkComplete | ~5s | File operations |

**Why 105s per slide?**
1. `Agent` object creation overhead (~2s)
2. `get_response()` call to DeepSeek API (~60-90s response time)
3. Validation and post-write size check (~5-10s)
4. Up to 5 retries on failure means some slides take much longer

**Why does DeepSeek v4 flash take 60-90s per request?**
The prompts are large (theme CSS + task brief + HTML context = ~5000-10000 tokens). DeepSeek v4 flash is a small/fast model, but via LiteLLM it's being asked to produce complex HTML with specific visual constraints. The model may be struggling with:
- Long context windows
- Complex output format requirements
- Rate limiting at DeepSeek's API

---

## 7. Strategic Problems

### 7.1 Architecture Overhead
Each slide generation creates a full `Agent` object with:
- System prompt loaded from file
- Tool setup (no tools used, but framework overhead still runs)
- agents SDK response loop with event streaming
- LiteLLM model wrapper

A simpler approach: Use `AsyncOpenAI(api_key=KEY, base_url=DEEPSEEK_URL)` directly with a `chat.completions.create()` call. No agents SDK, no LiteLLM, no tool setup. The HTML writer uses zero tools — it just generates HTML text. All the framework overhead is wasted.

### 7.2 No Caching Between Runs
The Master Repository cache check exists in QueueGenerationJob, but it never hit during testing. The cache key is built from (grammar, L1, age, level) and checks for pre-generated slides. Either:
- The cache was never populated
- The cache key didn't match
- The cache directory doesn't exist on Railway's volume

A cache hit would return instantly. Two runs of the same request should have been served from cache on the second attempt.

### 7.3 No Model Fallback
If DeepSeek v4 flash is slow or times out on a slide, there's no fallback to a different model. The slide just stays blank. Options: retry with Haiku via OpenRouter, retry with a simpler prompt, or have a fast "always works" model as backup.

### 7.4 Documents Not Integrated
The CreateDocument tool was designed for the main agent (not the background pipeline). Its output (`.source.html` in `documents/` directory) is never collected by the background pipeline's file registration logic. The pipeline constructs `worksheet_paths` and `activity_paths` dicts but never reads from them.

---

## 8. What to Do Next

### Priority 1: Fix slide generation speed
This is the make-or-break issue. 44 minutes = dead product.

Options (in order of likely impact):
1. **Use AsyncOpenAI directly** — skip LiteLLM + agents SDK for the HTML writer sub-agent. This eliminates ~80% of framework overhead per slide. The sub-agent generates HTML from a prompt — it doesn't need tools, streaming, or the agents SDK.
2. **Switch model** — DeepSeek v4 flash may not be the right model for this task. Consider: Claude Haiku via OpenRouter (fast, good HTML), GPT-4o mini (fast, reliable), or DeepSeek's own chat endpoint directly.
3. **Parallelize** — BATCH_SIZE=1 was a safety fix. After fixing per-slide speed, increase BATCH_SIZE safely by using per-task timeouts that don't cascade.

### Priority 2: Fix document registration
The `_get_slide_files_list()` function needs to also check the `documents/` directory and include `.source.html` files in the file_paths list passed to MarkJobComplete.

### Priority 3: Fix email delivery
Verify the sender domain in Resend or switch to SendGrid / SMTP.

### Priority 4: Seed the cache
After a successful run, copy the generated files to the Master Repository cache so identical requests return instantly.

---

## 9. Key Files

| File | Purpose |
|------|---------|
| `agent/slides_tools/QueueGenerationJob.py` | Background pipeline orchestration (all 10 steps) |
| `agent/slides_tools/ModifySlide.py` | Per-slide HTML generation via sub-agent |
| `agent/slides_tools/BuildOfflineBundle.py` | Builds self-contained HTML bundle |
| `agent/slides_tools/InsertNewSlides.py` | Creates blank slide placeholders |
| `agent/config.py` | Model routing config |
| `agent/docs_tools/CreateDocument.py` | Creates .source.html document files |
| `agent/jobs.py` | SQLite job queue |
| `server.py` | FastAPI server + endpoints |
| `agent/slides_tools/slide_plan.py` | Determines how many slides and their order |
| `agent/slides_tools/theme_generator.py` | Generates visual theme CSS |
| `agent/master_repository.py` | Cache check + copy functions |
| `.env.example` | Environment variable documentation |

---

## 10. Environment

- **Railway**: cogniesl service, hobby tier, 1 GB RAM, 2 vCPU
- **Volume**: `cogniesl-volume` at `/app/data`, 500 MB (0 used)
- **Current deployment**: `fd7a444a` (healthy)
- **Test user**: test@cogniesl.com (free tier)
- **API key**: DEEPSEEK_API_KEY is set in Railway env

---

## 11. API Endpoints for Testing

| Endpoint | Purpose |
|----------|---------|
| `POST /api/auth/register` | Register test user |
| `POST /api/auth/login` | Get auth token |
| `POST /cogniesl/get_response` | Send message to agent (triggers generation) |
| `GET /api/jobs/{job_id}` | Check job status |
| `GET /api/jobs/{job_id}/slides` | Get slide metadata + speaker notes |
| `GET /api/jobs/{job_id}/bundle.html` | Download HTML bundle |
| `GET /download/{job_id}/{filename}` | Download specific file |
| `GET /api/materials` | List user's materials |
| `GET /api/healthcheck` | Verify static data accessibility |
