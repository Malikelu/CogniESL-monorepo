# CogniESL Testing Checkpoint
**Last updated:** 2026-05-22 (session 4)  
**Status:** Phase 1 ✅ | Phase 2 ✅ | Phase 4 ✅ PARTIALLY TESTED | Phase 5 ✅ IMPLEMENTED + CODE AUDITED (live test needed) | Phase 3 & Test 3 DEFERRED | Phase 6 📋 PLANNED | Phase 7 📋 PLANNED

---

## How to Resume

1. Start the server: `cd '/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL' && bash launch.sh`
2. Open Chrome at `http://localhost:8080`
3. Tell Claude: **"Read COGNIESL_TESTING_CHECKPOINT.md and continue from where testing left off."**

---

## All Bug Fixes Applied (cumulative)

1. ✅ `server.py` — `load_dotenv(override=True)` + `set_tracing_disabled(True)` + `asyncio` import + `_generation_lock`
2. ✅ `agent/slides_tools/html_writer_instructions.md` — Font Awesome CDN in every slide head
3. ✅ `agent/instructions.md` — Full YAML extraction rules + L1 Oracle mandatory + format confirmation + pushback handler + grammar mapping + activity fallback + natural question style + no-error-surfacing
4. ✅ `agent/slides_tools/html_writer_instructions.md` — Trimmed 23KB → 12KB; Icon Strategy section added (Unicode for semantic icons, FA only decorative); Rule 10 (explicit pixel widths for PPTX layout); A6 L1 Oracle uses Unicode ✗/✓ (120px) not Font Awesome
5. ✅ `agent/slides_tools/ModifySlide.py` — RateLimitError retry with 30s×attempt backoff
6. ✅ `.env` — `SLIDE_GENERATION_DELAY=30`, `OPENAI_AGENTS_DISABLE_TRACING=true`, `SUB_AGENT_MODEL=gpt-4.1`
7. ✅ LiteLLM routing fixed — OpenAI before OpenRouter in InsertNewSlides.py and ModifySlide.py
8. ✅ `ValidateSlideSet.py` — size threshold 4,500 bytes (was 6,000 — false positives on real title/CCQ slides)
9. ✅ `ValidateAndFixSlides` — requires YAML content in task_briefs on retry
10. ✅ `GetL1InterferenceTool.py` — `_LANGUAGE_ALIASES` dict (Chinese→mandarin, Brazil→portuguese, 20+ aliases)
11. ✅ `server.py` — `_generation_lock = asyncio.Lock()` to serialize concurrent generation requests
12. ✅ `agent/instructions.md` — L1 exception to pushback rule (never skipped)
13. ✅ `agent/instructions.md` — Activity options only shown when teacher explicitly requests activity guide
14. ✅ `agent/instructions.md` — Opening message (first turn) + upsell line for formats NOT requested
15. ✅ `agent/instructions.md` — Mandatory retry loop for thin slides (orchestrator-level instruction)
16. ✅ `ModifySlide.py` — Post-write size check + auto-retry: < 4,000B triggers 3 rounds × 3 attempts, 120s wait between rounds
17. ✅ `agent/instructions.md` — Inter-format cooling period (3 min after PPTX before worksheet/activity)
18. ✅ `agent/instructions.md` — Activity guide as separate document rule + CreateDocument/ConvertDocument sequence
19. ✅ `agent/instructions.md` — **Phase 4A**: Content Brief Preview (Part 2B) — verbatim YAML, "looks good" gate, change-handling table
20. ✅ `agent/instructions.md` — **Phase 4B**: Post-generation message template — always includes "Need to change something?" line + format upsell
21. ✅ `agent/instructions.md` — **Phase 4C**: Single-slide change flow (Part 6) — recognition triggers, slide identification, ModifySlide → ValidateSlideSet → BuildPptxFromHtmlSlides sequence, multi-slide batching, returning-user reconnect
22. ✅ `agent/instructions.md` — **Phase 4D**: Project memory — store project_name + slide_plan after every generation
23. ✅ `agent/instructions.md` — Fixed "Starting now!" UX conflict: kickoff message now sent AFTER Content Brief approval, not immediately after requirements confirmed
24. ✅ `agent/instructions.md` — Validation threshold updated to 4,500 bytes everywhere (was still 6,000 in two places)
25. ✅ `agent/instructions.md` — **Phase 4 live test session 2 fix**: "Starting now!" removed from ALL confirmation templates (was still appearing before Content Brief)
26. ✅ `agent/instructions.md` — **Phase 4 live test session 2 fix**: Email question combined with confirmation message (instead of separate turn that caused "Starting now! + One last thing?" confusion)
27. ✅ `agent/instructions.md` — **Phase 4 live test session 2 fix**: Generation UX flow step 1 updated to match Part 1B — both now say email appended to confirmation, not standalone
28. ✅ `agent/instructions.md` — Pushback handler example updated: no longer says "Starting now" — now correctly asks for email after defaulting

---

## Phase 1 — Chat Interview Live Testing ✅ COMPLETE

All 8 personas tested and verified:
- **Fatima** ("just make it"): asks L1 only, does not re-ask format ✅
- **Tom** (describes grammar): names "second conditional" before anything else ✅
- **Kenji** (vague): one warm combined question, not a bullet list ✅
- **Maria** (gives everything upfront): asks format only, proceeds ✅
- **Liu Wei, Sarah, Paulo, Anna**: all passed ✅

---

## Phase 2 — Generation Testing ✅ COMPLETE

### Test 1: Present Simple + Spanish Adults
- **Project**: `present_simple_spanish`
- **Slides**: 15/15 all > 6,000 bytes ✅ | PPTX: 33MB ✅

### Test 2: Third Conditional + Chinese + Japanese Teens
- **Project**: `third_conditional_teen_chinese_japanese`
- **Slides**: 15/15 all > 4,500 bytes (smallest: 4,973B) ✅ | PPTX: 12MB ✅
- **L1 Oracle**: Chinese + Japanese both present ✅

### Test 3: Present Perfect + French Adults — ALL 3 FORMATS ❌ DEFERRED
- **Reason**: 30k TPM rate limit — 3-format requests exhaust it; all slides become placeholders
- **Fix required**: Upgrade OpenAI to Tier 2 (450k TPM, ~$50 deposit)
- **Code is correct** — generation pipeline works. This is a billing constraint only.
- **Do NOT re-run Test 3** until OpenAI tier is upgraded.

---

## Phase 3 — Performance & Cost Monitoring (DEFERRED)

Target: < 5 min per 15 slides, < $0.50 per lesson set.
- Note: Test 2 took ~38 minutes (rate-limit retries with 120s waits). This is the current baseline.
- Phase 3 is not blocking anything. Defer until Tier 2 upgrade removes rate limit variability.

---

## Phase 4 — Content Brief + Single-Slide Edits ✅ PARTIALLY TESTED

All four components implemented in `agent/instructions.md`. See fixes #19–28 above.

### Phase 4 Live Test Results (session 3)

**Test session 1** — sent "I need slides for the present perfect. My students are adults from France."
- ✅ Content Brief appeared with verbatim YAML data (CCQs, formula, L1 Oracle)
- ❌ Email question was skipped — went straight to Content Brief → **FIXED (#26)**
- ❌ Activity section appeared in Content Brief for slides-only request → **FIXED (previous session)**
- ❌ Agent narrated "I couldn't find L1 data for Italian" instead of silently omitting → **FIXED (previous session)**

**Test session 2** — same message after fixes:
- ✅ Email question now appears
- ❌ "Starting now!" appeared BEFORE Content Brief (contradicting the flow) → **FIXED (#25)**
- ❌ Email question combined with "Starting now!" was confusing — consolidated into clean confirmation + email at end → **FIXED (#25, #26, #27)**

**What still needs testing (Phase 4):**

### Phase 4 Remaining Test Plan

**Test 4A — Full flow: confirmation + email + Content Brief + generation (PRIORITY):**
- Send: "I need slides for the third conditional, my students are adults from Spain"
- Expected: agent confirms + asks email (one message) → you reply with email → agent searches silently → shows Content Brief (no "Starting now!") → you say "looks good" → agent says "On it!" → generates
- Pass: Each step happens in the right order, "Starting now!" absent until after approval

**Test 4B — Brief change handling:**
- After seeing the Content Brief, say: "Can you change the L1 to French instead?"
- Expected: agent re-fetches French L1 data, shows UPDATED brief with French Oracle, waits for re-approval
- Pass: Updated brief appears before generation starts

**Test 4C — Post-generation message:**
- After generation, verify the closing message always includes "Need to change something? Just tell me which slide..."
- Pass: That line is present in every delivery message

**Test 4D — Single-slide change:**
- After delivery, say: "Change slide 5 to use travel examples instead of medicine"
- Expected: ModifySlide called on slide_05 only → ValidateSlideSet → BuildPptxFromHtmlSlides with all slides → "Done — updated slide 5, other 14 slides unchanged"
- Pass: Only slide 5 changes, PPTX is rebuilt, other slides not touched

**Test 4E — Project memory in same session:**
- After delivery, say: "Change the L1 Oracle slide" (ambiguous)
- Expected: agent asks "Do you mean slide 7 (L1 Oracle — Spanish)?" — without asking what project or grammar point
- Pass: Agent remembers the project from earlier in the conversation

---

## Phase 5 — Async Generation + Email Delivery ✅ IMPLEMENTED (NOT YET TESTED)

New files written:
- `agent/jobs.py` — SQLite job queue (create_job, mark_done, mark_error, get_job)
- `agent/email_sender.py` — Resend branded email with download buttons
- `agent/slides_tools/QueueGenerationJob.py` — tool the agent calls after Content Brief approval
- `agent/__init__.py` — makes agent/ a proper Python package (required for imports)

Changes to existing files:
- `server.py` — imports jobs, calls init_db() on startup, adds /api/jobs/{id} and /download/{id}/{filename} endpoints
- `cogniesl_agent.py` — registers QueueGenerationJob tool
- `agent/instructions.md` — Part 1B email collection step; QueueGenerationJob call after brief approval; mark_done call after delivery
- `.env` — RESEND_API_KEY, COGNIESL_FROM_EMAIL, COGNIESL_BASE_URL placeholders added
- `requirements.txt` — resend>=0.7.0 added

**To activate email delivery:**
1. `pip install resend` (or `pip install resend --break-system-packages`)
2. Sign up at resend.com → get API key → replace `YOUR_RESEND_API_KEY_HERE` in `.env`
3. For testing: `onboarding@resend.dev` as from-address works without domain setup
4. For production: verify your domain at resend.com/domains, update COGNIESL_FROM_EMAIL

**Verified in session 3 (syntax + import checks):**
- ✅ `agent/jobs.py` — imports correctly, `init_db()` runs, `jobs.db` created
- ✅ `agent/email_sender.py` — syntax clean
- ✅ `agent/slides_tools/QueueGenerationJob.py` — syntax clean
- ✅ `agent/slides_tools/MarkJobComplete.py` — syntax clean
- ✅ `server.py` — syntax clean

**Session 4 code audit findings (2026-05-22):**
- ✅ Tool registration confirmed (QueueGenerationJob + MarkJobComplete in cogniesl_agent.py)
- ✅ Download endpoint logic verified — reconstructs path from project_name, not stored paths
- ✅ Email button URLs verified — use `Path(fp).name` correctly
- 🔧 FIXED: `jobs.py` update_job — dict mutation during iteration → replaced with safe dict comprehension
- 🔧 FIXED: `email_sender.py` — brand colors were indigo/purple, now CogniESL teal #0D7377
- ⚠️ `QueueGenerationJob` docstring says "Phase 5 will add background threading" — generation still runs synchronously (inline). This is intentional for now — the job tracking works, background decoupling deferred.

**What still needs live testing (Phase 5 test checklist):**
1. Add RESEND_API_KEY to `.env`: sign up at resend.com → Settings → API Keys → create key
2. Restart server: `bash launch.sh`
3. Send a test request through the chat, approve the Content Brief, provide email
4. Verify: agent calls QueueGenerationJob → job appears at `/api/jobs/{id}` with status "pending"
5. After generation completes: verify agent calls MarkJobComplete → job status becomes "done"
6. Verify: email arrives at the provided address with teal-branded download buttons
7. Click a download link: verify file downloads successfully
8. Edge case: try `/api/jobs/nonexistent-id` → should return `{"error": "Job not found"}` not HTML

---

## Phase 6 — User Accounts + My Materials Library 📋 PLANNED

Full plan in `PHASE6_PLAN.md`. Summary:
- 6A: Email/password auth + JWT tokens
- 6B: Per-user file storage `/mnt/{user_id}/{project_name}/`
- 6C: Materials library (SQLite table + `/api/materials` endpoints)
- 6D: My Materials frontend page
- 6E: Agent ListMaterials tool for returning-teacher flow

**Not started. Start after Phase 5 is tested and stable.**

---

## Phase 7 — UI/Brand Identity 📋 PLANNED

Full plan in `PHASE7_PLAN.md`. Summary:
- 7A: Commission/generate CogniESL logo (primary, favicon, email, navbar sizes)
- 7B: Apply logo to product UI, website (Navbar + Footer), email template
- 7C: Align product chat UI colors to design system (teal #0D7377)
- 7D: Website final polish — real testimonials, real screenshots, OG image
- 7E: Domain setup, Plausible analytics, waitlist email wiring

**Not started. Can run in parallel with or after Phase 6.**

---

## Known Issues (not yet fixed)

1. **3-format requests fail at 30k TPM** — needs OpenAI Tier 2 upgrade
2. **HTTP timeout on long requests** — architectural fix in Phase 5 (async + email)
3. **PPTX layout overlap in complex slides** (slide 8 in Test 2) — mitigated by pixel-width rule in html_writer_instructions.md, not fully eliminated
4. **SLIDE_GENERATION_DELAY=30** — conservative for 1-format requests; could be 20s for slides-only to save time

---

## Cost Tracking

- Burned in testing (two sessions): ~$11
- Estimated per 3-format generation in production: $1.50–2.30
- $50 OpenAI credit ≈ 22–33 complete productions
- Tier 2 upgrade requires: $50 deposit → unlocks 450k TPM (from 30k)
