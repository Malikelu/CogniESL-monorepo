# CogniESL Testing Brief — Instructions for Test Agent

**Read `docs/COGNIESL_FULL_UNDERSTANDING.md`, `docs/Final Audit Report.md`, and `CLAUDE.md` first.**

**Critical context:** This document was rewritten 2026-06-05 because the old version described an ideal system. The pipeline has 34 verified findings (documented in `Final Audit Report.md`), several of which break every test. If you encounter a failure, it's probably a known bug — don't retry blindly. Report it and move on.

---

## Known Issues That Affect Testing (Read This First)

These are verified bugs from the Final Audit Report. Every test will hit at least some of them. Don't troubleshoot — just report.

| Issue | Affects | What Happens |
|-------|---------|-------------|
| **Chat agent context loss** (F32) | All chat sessions | Agent forgets your parameters and reverts to "Present Simple, Spanish, adults" defaults. May create duplicate jobs. |
| **Flashcard generation crash** (F35) | Flashcards | `GenerateFlashcardPdf` crashes with TypeError (`'list' object has no attribute 'startswith'`). **FIXED 2026-06-05** — but fix is not yet deployed. |
| **Progress tracker filename mismatch** (F24a) | Progress tracker PDF | Progress tracker IS generated but saved with wrong filename (grammar-L1 based instead of project_name based). **FIXED 2026-06-05** — but fix is not yet deployed. |
| **L1 Oracle empty** (F1) | L1 content | L1 Oracle slides get zero real interference data from the database. The model invents content. |
| **Worksheet sections missing** (F2, F13) | Worksheet | Sections A/B/Answer Key empty due to YAML field name mismatch. Section C header says literal "[L1]". Sections E/F missing. |
| **Content hallucination** (F27) | Output accuracy | With concurrent jobs, the LLM mixes grammar points and L1 languages across threads (e.g., requests Past Simple but generates Unreal Past). Single-thread jobs produce correct content. |
| **Level always B1** (F4) | Materials | Proficiency level is silently discarded. Every deck is generated at B1 regardless of request. |
| **Download endpoint status gate** (F28) | Downloads | `/download/{job_id}/{filename}` returns 404 for ALL files until status reaches "done". Only affects flashcards and progress tracker for completed jobs — **worksheet and activity guide downloads work** for "done" jobs. |
| **Jobs stuck "pending"** (F29) | Reliability | ONLY happens with concurrent jobs. Single-threaded jobs complete reliably in ~9 min. Do NOT run parallel tests. |

---

## What the Pipeline Can Produce (Ideal vs. Current Reality)

| # | Material | Files | Status |
|---|----------|-------|--------|
| 1 | Slides | `{project}.html` (offline bundle) | ✅ Works — download via `/api/jobs/{job_id}/bundle.html` |
| 2 | Worksheet | `{project}_worksheet.docx` + `.pdf` | ✅ Works for completed jobs — both DOCX and PDF downloadable (HTTP 200). Sections A-F incomplete due to F2/F13. |
| 3 | Activity Guide | `{project}_activity_guide.docx` + `.pdf` | ✅ Works for completed jobs — both DOCX and PDF downloadable (HTTP 200). |
| 4 | Flashcards | `{project}_flashcards.pdf` | ❌ Crashes with TypeError (F35 — **FIXED**, deploy pending). Always 404. |
| 5 | Progress Tracker | `{project}_progress-tracker.pdf` | ⚠️ Generated with wrong filename (F24a — **FIXED**, deploy pending). PDF exists on volume but at wrong path → 404. |
| 6 | PowerPoint | `{project}.pptx` | ⚠️ Only if teacher says "PowerPoint." Not tested in diagnostic run. |

**For completed jobs, bundle, worksheet (DOCX+PDF), and activity guide (DOCX+PDF) all download reliably.** Only flashcards (F35 — fixed) and progress tracker (F24a — fixed) 404. If those still 404, the fixes need deploying. See Debugging section for volume inspection via Railway commands.

---

## Step 0: Read First

```
docs/COGNIESL_FULL_UNDERSTANDING.md   ← what CogniESL is, all materials, pipeline steps
docs/Final Audit Report.md             ← 34 verified findings — know what's broken before testing
docs/TESTING_METHODOLOGY.md            ← testing philosophy (vary everything, one at a time)
CLAUDE.md                              ← core principles: database is sacred, L1-aware, 80/20 visual
```

---

## Step 1: Check Deployment

```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
railway status
```

Base URL: `https://cogniesl-production.up.railway.app`

---

## Step 2: Register Test Account

```
POST https://cogniesl-production.up.railway.app/api/auth/register
Content-Type: application/json
{"email": "test-<unique>@cogniesl.com", "password": "TestPass123!", "name": "Test Agent"}
```

Save the token. All subsequent requests need header: `Authorization: Bearer <token>`

---

## Step 3: Test Plan — 5 Tests

**ONE AT A TIME. Wait for `status: "done"` before starting next. Never run concurrent tests — F27 (content hallucination) and F29 (stuck jobs) are amplified by concurrency.**

| # | Grammar | L1 | Level | Age | Skill | PPTX? |
|---|---------|----|-------|-----|-------|-------|
| 1 | Past Continuous | Korean | B1 | teens | writing | No |
| 2 | First Conditional | Turkish | A2 | adults | speaking | **Yes** |
| 3 | Passive Voice | French, Chinese | B2 | adults | grammar | No |
| 4 | Phrasal Verbs (travel) | Russian | B1 | adults | speaking | **Yes** |
| 5 | Gerunds vs Infinitives | Japanese | B2 | teens | writing | No |

---

## Step 4: For Each Test

### 4a. Start Chat and Submit Request

```
POST https://cogniesl-production.up.railway.app/cogniesl/get_response
Authorization: Bearer <token>
X-Session-ID: test-<N>-<timestamp>
Content-Type: application/json
```

**Request message for tests WITHOUT PowerPoint (1, 3, 5):**
```
I need slides, a worksheet, an activity guide, flashcards, and a progress tracker for <Grammar> for <age> <L1> speakers at <Level> level focusing on <Skill>.
```

**Request message for tests WITH PowerPoint (2, 4):**
```
I need slides, a worksheet, an activity guide, flashcards, a progress tracker, and PowerPoint for <Grammar> for <age> <L1> speakers at <Level> level focusing on <Skill>.
```

### 4b. Handle Agent Conversation (Watch for Context Loss!)

The chat agent has a **known context loss bug** (F32). It may:
- Respond with "Present Simple, Spanish" regardless of your request
- Forget parameters mid-conversation
- Create duplicate jobs

**If the agent ignores your parameters:**
1. Note it in the report (important data point)
2. Try re-prompting with the full request again
3. If it still reverts to wrong defaults after 2-3 attempts, stop and report
4. Do NOT create duplicate jobs — this triggers F31 (concurrent degradation) and F27 (content hallucination)

**Normal conversation flow:**
- Answer clarifying questions using the test plan parameters
- When agent presents Content Brief → reply "Approved, please generate everything now"
- Chat until agent returns a message containing "STOP" or "job_id=" or "background"
- Extract `job_id` (hex string like `a1b2c3d4`)

### 4c. Poll Until Done

```
GET https://cogniesl-production.up.railway.app/api/jobs/<job_id>
Authorization: Bearer <token>
```

Poll every 15 seconds. **Known issue:** status will show "pending" throughout generation (even when logs show active work). Only flips to "done" at the end. Wait max 15 minutes (60 polls).

Save the `project_name` from the response. Also save `file_paths` if present — this tells you what the pipeline *intended* to generate.

### 4d. Download What You Can — Use Railway Commands for the Rest

**The download endpoint returns 404 for all non-bundle files** (known bug F28). Don't waste time retrying 404s — switch to Railway volume inspection.

| # | File | How to Verify | Expected Min Size |
|---|------|--------------|-------------------|
| 1 | Slides bundle | `GET /api/jobs/<job_id>/bundle.html` | 50 KB — Works reliably |
| 2 | Worksheet DOCX | `GET /download/<job_id>/<project>_worksheet.docx` | 10 KB — Works for done jobs |
| 3 | Worksheet PDF | `GET /download/<job_id>/<project>_worksheet.pdf` | 10 KB — Works for done jobs |
| 4 | Activity Guide DOCX | `GET /download/<job_id>/<project>_activity_guide.docx` | 10 KB — Works for done jobs |
| 5 | Activity Guide PDF | `GET /download/<job_id>/<project>_activity_guide.pdf` | 10 KB — Works for done jobs |
| 6 | Flashcards PDF | `GET /download/<job_id>/<project>_flashcards.pdf` | Likely 404 (F35 — fixed, deploy pending) |
| 7 | Progress Tracker PDF | `GET /download/<job_id>/<project>_progress-tracker.pdf` | Likely 404 (F24a — fixed, deploy pending) |
| 8 | PowerPoint | `railway run wc -c /app/data/mnt/<project>/presentations/*.pptx` | 100 KB (if requested) |

Also fetch `GET /api/jobs/<job_id>/slides` — list of all slides with sizes.

### 4e. Verify Slide Content Quality

Save the bundle HTML and check:
1. Every slide > 2500 bytes (use the `/slides` endpoint)
2. Every slide has `data-speaker-notes` attribute with content
3. L1 Oracle slides exist — but note they may have **invented content** (F1 — no real database data reaches them)
4. No two slides have identical visible content
5. Theme is applied (CSS variables like `--primary`, `--bg` present)
6. CCQs appear before grammar formulas (check slide order/content)
7. **Check if the grammar point is correct** — F27 (content hallucination) may swap it for something unrelated

### 4f. Verify Worksheet Content (via Railway Volume Inspection)

Worksheet files live on Railway volume but downloads 404. Inspect via:
```bash
railway run cat /app/data/mnt/<project>/documents/<project>_worksheet.source.html
```

Check:
1. **Section A** — Fill-in-the-gap: are the `<li>` items empty or real? (F2: likely empty)
2. **Section B** — Error correction: wrong→correct pairs in red/green? (F2: likely empty)
3. **Section C** — L1 Drill: does it say "[L1]" or the actual language? (F13: likely "[L1]")
4. **Section D** — Write Your Own: blank lines present?
5. **Section E** — Answer Key: real answers or empty? (F2: likely empty)
6. **Section F** — Homework: present or missing? (likely missing — F2)

### 4g. Verify Flashcards Content

Flashcards crash in `GenerateFlashcardPdf` with TypeError (F35). Check via:
```bash
railway run ls -la /app/data/mnt/<project>/documents/
```
If no flashcard files exist, report "flashcard generation crashed — known bug F35 (fixed, deploy pending)."

### 4h. Verify Progress Tracker Content

Progress tracker IS generated but saved with wrong filename (F24a — naming mismatch). Check via:
```bash
railway run ls -la /app/data/mnt/<project>/documents/
railway run ls -la /app/data/mnt/<project>/documents/*progress*
```
If files exist but have grammar-L1 based names (e.g., `present_simple-spanish-progress-tracker.pdf`), that's F24a — **fixed but deploy pending.** Report "progress tracker generated at wrong path — known bug F24a (fixed)."

---

## Step 5: Report Format

After each test, produce:

```markdown
## Test N: <Grammar> for <L1> | Level <Level> | Age <Age> | <Skill>

**Job ID:** <id> | **Project:** <project_name> | **Duration:** <time to done>
**PPTX requested:** Yes/No
**Agent context loss observed:** Yes/No (this is a key diagnostic signal)

### Downloads
| # | File | Size | Method | Status |
|---|------|------|--------|--------|
| 1 | Slides bundle | X KB | HTTP download | ✅/❌ |
| 2 | Worksheet DOCX | X KB / 404 | Railway volume | ✅/❌ |
| 3 | Worksheet PDF | X KB / 404 | Railway volume | ✅/❌ |
| 4 | Activity Guide DOCX | X KB / 404 | Railway volume | ✅/❌ |
| 5 | Activity Guide PDF | X KB / 404 | Railway volume | ✅/❌ |
| 6 | Flashcards PDF | 404 / missing | Railway volume | ✅/❌/known bug |
| 7 | Progress Tracker PDF | 404 / missing | Railway volume | ✅/❌/known bug |
| 8 | PowerPoint (.pptx) | X KB / 404 | Railway volume | ✅/❌ (expected: <yes/no>) |

### Slide Summary
N slides. Size range: X-Y KB.
Speaker notes: present on N/N slides.
L1 Oracle: present/missing/invented content (known bug F1).
Grammar point correct: yes/no (watch for F27 hallucination).

### Quality
- Worksheet Section A: <has real content / empty — known bug F2>
- Worksheet Section C: <uses real L1 name / literal "[L1]" — known bug F13>
- Flashcards: <crash in GenerateFlashcardPdf with TypeError / missing — known bug F35 (fixed, deploy pending)>
- Progress Tracker: <generated but wrong filename / missing — known bug F24a (fixed, deploy pending)>
- Visual quality: <passable/not passable — would teacher pay?>

### New Issues (not in the 34 known findings)
- <Describe anything unexpected that doesn't match the known bug list>

### Bundle
[Bundle URL](https://cogniesl-production.up.railway.app/api/jobs/<job_id>/bundle.html)
```

---

## Step 6: Final Summary Matrix

Use rows with known-bug annotations (e.g., "404 (F28)" instead of just "404"):

| # | Grammar | L1 | Bundle | Wks DOCX | Wks PDF | Act DOCX | Act PDF | Flash | Tracker | PPTX | Overall |
|---|---------|----|--------|----------|---------|----------|---------|-------|---------|------|---------|
| 1 | Past Cont. | Korean | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ❌ F35* | ❌ F24a* | N/A | |
| 2 | 1st Cond. | Turkish | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ❌ F35* | ❌ F24a* | Exp. | |
| 3 | Passive V. | Fr, Zh | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ❌ F35* | ❌ F24a* | N/A | |
| 4 | Phrasal V. | Russian | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ❌ F35* | ❌ F24a* | Exp. | |
| 5 | Gerunds/Inf | Japanese | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ✅ exp. | ❌ F35* | ❌ F24a* | N/A | |

*Expected to 404 until fixes are deployed. Mark as ✅ once deployed and verified.

---

## Debugging (these actually work)

```bash
# Watch logs (filter for errors)
railway logs --service cogniesl --lines 300 | grep -iE "error|fail|warn|exception"

# Check what files actually exist on the volume
railway run ls -la /app/data/mnt/
railway run find /app/data/mnt -type f | head -50

# Check specific project's files
railway run ls -laR /app/data/mnt/<project_name>/

# Read pipeline progress
railway run cat /app/data/mnt/<project_name>/presentations/_checkpoint.json

# Check slide content on disk
railway run wc -c /app/data/mnt/<project_name>/presentations/slide_*.html

# Check worksheet source HTML
railway run cat /app/data/mnt/<project_name>/documents/*.source.html | head -200

# Search for L1-specific content in documents
railway run grep -rl "Spanish\|Korean\|Turkish\|Arabic\|Japanese" /app/data/mnt/<project_name>/documents/

# Check job status directly (to verify API vs reality)
railway run curl -s http://localhost:8000/api/jobs/<job_id> | python3 -m json.tool
```

---

## Hard Rules

1. **One test at a time.** Never concurrent — known bug F27 (content hallucination across threads) and F29 (stuck jobs) get worse with parallel runs.
2. **Know the known bugs before testing.** Read `Final Audit Report.md` §1 (findings F1-F36) before starting.
3. **Retry 404s selectively.** If worksheet or activity guide 404 on a "done" job, that's a new bug. If flashcards 404, that's known bug F35 (fixed, deploy pending). If progress tracker 404, that's known bug F24a (fixed, deploy pending). Use Railway volume inspection to confirm files exist on disk.
4. **If the agent reverts to defaults, note it.** Agent context loss (F32) is a key diagnostic signal — document how many attempts it took, what it said, and what the final job was.
5. **Don't fix code.** Just report what passes, what fails, and whether it's a known bug or a new issue.
6. **Provide clickable download link for at least the bundle** in the report so Marcos can view slides (bundle downloads work).
7. **If stuck, duplicate, or ambiguous — stop and report.** Don't submit duplicate jobs (amplifies F31).

---

## Appendix A: Current System State (2026-06-05)

### What Works Reliably
- Bundle HTML generation and download ✅
- Slide count > 2500 bytes ✅
- Speaker notes on all slides ✅
- Theme CSS applied ✅
- Slide metadata endpoint (`/api/jobs/{id}/slides`) ✅
- Job polling for status ✅
- Project directory created on volume ✅
- Worksheet DOCX + PDF downloads (for completed jobs) ✅
- Activity guide DOCX + PDF downloads (for completed jobs) ✅

### What Works with Known Bugs
- Single-threaded jobs complete reliably (~9 min) — F29 only manifests with concurrent jobs
- Correct grammar point generated in single-thread mode — F27 is a concurrency artifact
- Slide content matches task briefs — no drift in single-thread mode
- Progress tracker generated but at wrong filename — F24a (fixed, deploy pending)
- L1 Oracle slide exists in plan but content is AI-invented — F1 still open

### What Never Works (based on diagnostic run)
- Worksheet Sections C, E, F — always missing (F2)
- L1-specific content in slides — always invented (F1)
- Flashcards — crash in GenerateFlashcardPdf (F35 — fixed, deploy pending)
- Proficiency level filtering — always B1 (F4)

### Fixes Applied (2026-06-05, deploy pending)
1. **F24a** — `GenerateProgressTrackerPdf` now uses `project_name` for filename stem
2. **F35** — `GenerateFlashcardPdf` fixed: list return-type check, `output_format` param, project-based naming

### Priority Fixes Still Open
1. F1 — Fix L1 Oracle data flow (without this, the core value prop is broken)
2. F2 — Fix worksheet content (without this, worksheets are unusable)
3. F4 — Thread proficiency level through pipeline (without this, level is silently B1)
4. F5 — Unify path resolution (without this, cache and edge cases break)

### Test Results Archive

See `Final Audit Report.md` §7 for full results of these prior test runs:
- Job ee194a68: Narrative Tenses / Korean / teens (3 of 5 formats generated)
- Job d9d467ef: Present Simple / Spanish / adults (5 of 5 formats listed but downloads all 404)
- Job b39fd63a: Present Simple / Spanish / adults (3 formats, same 404 pattern)
- Job ade45ef9: Present Continuous / Japanese / adults (stuck in "pending" at 7/8 batches)
- Job d2512cfc: Past Simple Irregular Verbs / Arabic / teens (hallucinated "Unreal Past"; all downloads 404)
- Job ff45716c: First Conditional / Korean / kids (stuck in "pending" at 3/8 batches)
