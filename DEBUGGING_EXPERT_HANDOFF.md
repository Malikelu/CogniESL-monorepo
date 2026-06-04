# CogniESL — Debugging Expert Handoff

## Overview

CogniESL is an AI-powered ESL teaching material generator. Teachers describe what they need (e.g., "slides for present simple for Portuguese adults"), and the system generates a full slide deck, worksheets, activity guides, etc.

**Architecture**: Single agent (Agency Swarm / OpenAI Agents SDK) → FastAPI backend on Railway → sub-agents for slide writing → output files on Railway Volume at `/app/data/mnt/{project_name}/`.

**Key repo**: `~/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/`
**GitHub**: `github.com/Malikelu/CogniESL-monorepo` (main branch)
**Live API**: `https://cogniesl-production.up.railway.app`
**Test account**: `test-e2e@test.com` / `test1234` (free tier)

---

## Problem 1: Thin Slides (Background Thread)

### What Happens

The **Slide HTML Writer sub-agent** produces ~2,100 bytes per slide — under the 4,000 byte minimum. Post-write validation retries (3 rounds × 3 attempts) produce the **same thin content**. This happens with both DeepSeek and Owl-Alpha.

### Symptoms in Logs

```
WARNING:slides_tools.ModifySlide:slide_17.html: written size 2101B < 4000B (placeholder detected). Waiting 10s then retrying HTML writer (round 1/3).
```

### Root Causes (Identified June 2)

1. **AUTOMATED GENERATION MODE said "call InsertNewSlides immediately"** — agent skipped database searches, task_briefs had no YAML data. **FIXED**: instructions.md now says run DB searches first. But fixing this alone did NOT solve thin slides (see P1 Latest Fix below).

2. **DeepSeek produces near-empty task_briefs** — 417 chars vs Owl-Alpha's 5,233 for Content Briefs. Summarizes instead of pasting verbatim YAML. **FIXED**: per-slide-type minimum character counts added to Golden Rule.

3. **Retry logic made slides thinner** — `if attempt >= 3` prepended "SIMPLIFIED REQUEST: Provide basic HTML structure only..." **FIXED**: block removed.

4. **Background agent forgets YAML data across 17 slides** — Even after running DB searches, DeepSeek doesn't paste the YAML verbatim into each task_brief. By slide 5 the tool-call output is far back in the context window and the model summarizes. **FIXED**: YAML pre-loaded in Python code and injected into the agent's first message (see P1 Latest Fix below).

---

## Problem 2: LiteLLM × Asyncio × Threading Conflict

DeepSeek via LiteLLM calls failed silently in `threading.Thread`. Owl-Alpha worked but was slower.

**FIXED June 2**: All `LitellmModel` creations for `deepseek/` models now pass `DEEPSEEK_API_KEY` explicitly. `create_cogniesl_agent()` accepts `bg_mode=True` which uses `get_bg_default_model()` (checks `BG_DEFAULT_MODEL` env var). `BG_SUB_AGENT_MODEL` env var controls background sub-agents.

**Railway env var options:**
| Scenario | BG_DEFAULT_MODEL | BG_SUB_AGENT_MODEL |
|----------|-----------------|-------------------|
| Free testing | `openrouter/owl-alpha` | `openrouter/owl-alpha` |
| Production (cheap) | `openrouter/deepseek/deepseek-v4-flash` | `openrouter/deepseek/deepseek-v4-flash` |
| Key fix enough | Don't set | Don't set |

---

## Problem 3: Output Guardrail Overwrites "done" Status

Agent calls MarkJobComplete (status → "done"), returns text, output guardrail trips on that text → `mark_error()` overwrites "done" with "error". Files exist on volume but endpoints refuse to serve them.

**FIXED June 2**: `mark_error()` in `agent/jobs.py` now uses:
```sql
UPDATE jobs SET status='error', error=? WHERE job_id=? AND status != 'done'
```
A job already marked done cannot be overwritten by a guardrail error.

---

## Problem 4: Double-`presentations/` Path Bug

`./mnt/.../presentations/presentations/file.html` — `presentations/` duplicated.

**FIXED June 2**: `BuildOfflineBundle.py` — `get_project_dir()` already returns `mnt/{name}/presentations`. The old code appended `/presentations` again. Fixed to `out_dir = project_dir`.

---

## Problem 5: New Kickoff Pattern

Agent sends 98-char "All ready for your review!" — not caught by `_is_kickoff_message()`.

**FIXED June 2**: `"all ready for your review"` added to `_kickoff_phrases` in `server.py`.

---

## P1 Latest Fix — YAML Pre-loading (June 2, late session)

### Root Cause Confirmed

The background agent runs DB searches (tool calls) but DeepSeek doesn't paste the YAML verbatim into task_briefs for slides 5–17. By then the tool output is far back in the context window. The model summarizes instead of quoting — producing 400-char task_briefs instead of the 800–1,200 chars the HTML Writer needs to build rich slides.

### Fix Applied

**`QueueGenerationJob.py` — `_preload_yaml_context()` function**

New function runs **before** the background agent is called. It directly instantiates `SearchGrammarTool`, `GetL1InterferenceTool`, and `SearchActivitiesTool` in Python (no LLM involved) and returns the full YAML data as formatted text.

This block is injected into the background agent's first message as `<DATABASE_CONTENT>...</DATABASE_CONTENT>`. Complete grammar YAML, L1 interference patterns, and activity templates are in the context window from the very first token — slide 1 through slide 17.

The agent no longer needs to "remember" tool-call outputs across 17 ModifySlide calls.

**`ModifySlide.py` — task_brief logging**

Each `ModifySlide.run()` logs the task_brief length and first 300 chars. Look for in Railway logs:
```
WARNING:[slide_01.html] THIN TASK_BRIEF (87 chars) — agent likely not pasting YAML.
INFO:[slide_01.html] task_brief=1243 chars. Preview: ...
```

### What to Monitor After Deployment

1. Railway logs: look for `task_brief=` lines — should see 800–1,200+ chars per slide
2. Slide sizes — should see 6,000–15,000 bytes (not 2,100B)
3. If thin briefs persist despite the DATABASE_CONTENT block: check `COGNIESL_STATIC_DIR` env var — the pre-loader uses the same path logic as the tools; if the YAML files aren't at the expected path, it will log `[Grammar data unavailable: ...]`

---

## Key Metrics

| Metric | DeepSeek (main thread) | DeepSeek (bg thread) |
|--------|------------------------|----------------------|
| Content Brief | 22-28s (98-417 chars) | N/A (bg starts after approval) |
| Approval | 4.6-6.0s | N/A |
| Total teacher wait | ~27-33s | N/A |
| BG slide generation | N/A | ~5 min (17 slides) |
| Slide size | N/A | ~2,100B (thin, target: 6,000+B) |

---

## Files Involved

| File | Path |
|------|------|
| InsertNewSlides.py | `agent/slides_tools/InsertNewSlides.py` |
| ModifySlide.py | `agent/slides_tools/ModifySlide.py` |
| html_writer_instructions.md | `agent/slides_tools/html_writer_instructions.md` |
| BuildOfflineBundle.py | `agent/slides_tools/BuildOfflineBundle.py` |
| QueueGenerationJob.py | `agent/slides_tools/QueueGenerationJob.py` |
| MarkJobComplete.py | `agent/slides_tools/MarkJobComplete.py` |
| instructions.md | `agent/instructions.md` |
| server.py | `server.py` |
| jobs.py | `agent/jobs.py` |
| config.py | `agent/config.py` |
| cogniesl_agent.py | `agent/cogniesl_agent.py` |

---

## Problem Status

| Problem | Status | Notes |
|---------|--------|-------|
| P1: Thin slides | **ALL FIXES APPLIED ✓** — awaiting prod test | YAML pre-load, instructions aligned, guardrail fixed |
| P2: LiteLLM threading | **FIXED ✓** | Explicit DEEPSEEK_API_KEY; DeepSeek works in bg thread |
| P3: Guardrail overwrites done | **FIXED ✓** | `mark_error` skips if status = done |
| P4: Double presentations/ path | **FIXED ✓** | `out_dir = project_dir` in BuildOfflineBundle.py |
| P5: "All ready for your review" | **FIXED ✓** | Added to `_kickoff_phrases` in server.py |

---

## All Changes Applied (June 2 full session)

1. Async generation via `threading.Thread`
2. PROCEED_WITH_GENERATION handshake
3. AUTOMATED GENERATION MODE in instructions.md
4. DB search instruction made conditional: use DATABASE_CONTENT if present, else run searches
5. Per-slide-type Golden Rule minimums in instructions.md
6. SIMPLIFIED REQUEST block removed from ModifySlide.py
7. Post-write sleep: 10s → 2s in ModifySlide.py
8. 8 new kickoff phrases in server.py + "all ready for your review"
9. Logging to stdout
10. `asyncio.run()` replaces manual loop
11. Content density requirement in retry prompt (rounds 2+)
12. Explicit DEEPSEEK_API_KEY in all LitellmModel creations (`config.py`, `ModifySlide.py`, `InsertNewSlides.py`)
13. `bg_mode` flag + `BG_DEFAULT_MODEL` / `BG_SUB_AGENT_MODEL` env vars (`config.py`, `cogniesl_agent.py`, `QueueGenerationJob.py`)
14. `mark_error` conditional update in `jobs.py` — won't overwrite done status
15. `out_dir = project_dir` in `BuildOfflineBundle.py` — fixes double path
16. `_preload_yaml_context()` in `QueueGenerationJob.py` — YAML pre-loaded in Python and injected into agent's first message
17. Task_brief size logging in `ModifySlide.py`
18. memory-context tag updated — references DATABASE_CONTENT, no longer contradicts instructions.md
19. `validate_l1_content` guardrail fixed — skips job completion messages so bg agent's final response never triggers a re-run

---

## Contact

- **Marcos**: Brazilian lawyer-entrepreneur, building CogniESL + CogniELA
- **Debugging expert**: You. Full codebase on GitHub main branch.
