# CogniESL — Testing Methodology

**Purpose:** Complete testing strategy for CogniESL's material generation pipeline.
Every test agent MUST follow this document. No exceptions.

**Last updated:** 2026-06-05
**Replaces:** The old "e2e" testing approach that was boring, repetitive, incomplete, and didn't let humans see results.

---

## 0. Before You Run ANY Test

1. **Read** `docs/COGNIESL_FULL_UNDERSTANDING.md` — you must understand what CogniESL is
2. **Read** `CLAUDE.md` — project principles and constraints
3. **Confirm** the Railway deployment is current (check `railway status`)
4. **Confirm** you know the base URL (check `railway domain` or env vars)

## 1. Testing Principles

### 1.1 One Test at a Time

**NEVER run concurrent tests.** Each test is a single job submitted to the pipeline. Wait for it to complete (status = "done") before starting the next one. Submitting multiple jobs simultaneously:
- Confuses the pipeline (it's designed for one-at-a-time per project)
- Makes debugging impossible (which job failed?)
- Is unrealistic (a single teacher doesn't request 3 generations simultaneously)

### 1.2 Vary EVERY Parameter

Each test must use a DIFFERENT combination. Never repeat the same grammar point, L1 language, or level twice in a session. Rotate through:

**Grammar points** (pick from the 302 available):
- Present Simple, Present Continuous, Present Perfect, Present Perfect Continuous
- Past Simple, Past Continuous, Past Perfect, Past Perfect Continuous
- Future Simple (will), Future (going to), Future Continuous, Future Perfect
- Conditionals (Zero, First, Second, Third, Mixed)
- Modals (can/could, must/have to, should, might/may, would)
- Passive Voice, Reported Speech, Relative Clauses
- Articles (a/an/the), Prepositions, Phrasal Verbs
- Gerunds vs Infinitives, Countable/Uncountable Nouns
- Question Formation, Tag Questions
- Comparatives/Superlatives, Used to/Would

**L1 languages** (pick from the 36 available):
- Never use Spanish or Portuguese twice in the same session
- Rotate: Spanish, Portuguese, Japanese, Korean, Chinese (Mandarin), Arabic, French, German, Italian, Russian, Turkish, Thai, Vietnamese, Hindi, Polish, Dutch, Swedish, etc.
- Vary the number of L1s: sometimes 1 language, sometimes 2, occasionally 0 (monolingual class)

**Levels:** A1, A2, B1, B2, C1 (rotate)

**Age groups:** children (6-9), young learners (10-12), teens (13-17), adults (18+), mixed

**Skill focus:** speaking, writing, reading, listening, grammar, mixed

### 1.3 Request ALL Materials

Every test must request ALL deliverable materials. The only exception is PPTX — request it in ~50% of tests to verify the opt-in mechanism works both ways.

**Standard request format:**
"I need [slides], [worksheet], [activity guide], [flashcards], [progress tracker] for [grammar] for [age] [L1] speakers at [level] level focusing on [skill]. [Add 'and PowerPoint' in ~50% of tests]"

**Example:**
"I need slides, a worksheet, an activity guide, flashcards, and a progress tracker for Second Conditional for teenage Japanese speakers at B1 level focusing on speaking. Also generate PowerPoint."

### 1.4 Make Results Viewable

After each test completes, produce:
1. **Download links** for every generated file (use the endpoints from COGNIESL_FULL_UNDERSTANDING.md Section 9)
2. **Slide content summary** — list each slide's title, content type, and file size
3. **Visual quality assessment** — describe the theme, layout density, and whether it meets the 80/20 visual rule
4. **File size verification** — every file must be non-trivial (>2500 bytes for slides, >10KB for documents)

## 2. Test Execution Protocol

### Step 1: Submit the Job

POST to the chat endpoint with the teacher's request. The chat agent will:
- Ask clarifying questions
- Present a Content Brief
- Wait for approval ("approved", "looks good", "go ahead", etc.)

Keep the conversation going until the agent confirms the job is submitted and returns a `job_id`.

### Step 2: Wait for Completion

Poll `GET /api/jobs/{job_id}` until `status == "done"`.
- Poll interval: 15 seconds
- Maximum wait: 10 minutes (40 polls)
- If still not done after 10 minutes, report the current status and last progress step

### Step 3: Download and Inspect EVERY File

For each file endpoint, download and inspect:

| File | Endpoint | Min Size | What to Check |
|------|----------|----------|---------------|
| Slide bundle | `/api/jobs/{job_id}/bundle.html` | 50KB | Contains all slides, has theme, speaker notes present |
| Worksheet DOCX | `/download/{job_id}/{project_name}_worksheet.docx` | 10KB | Has sections A-F, L1 content |
| Worksheet PDF | `/download/{job_id}/{project_name}_worksheet.pdf` | 20KB | Same content, properly formatted |
| Activity Guide DOCX | `/download/{job_id}/{project_name}_activity_guide.docx` | 10KB | Has activities, differentiation notes |
| Activity Guide PDF | `/download/{job_id}/{project_name}_activity_guide.pdf` | 20KB | Same content |
| Flashcards PDF | `/download/{job_id}/{project_name}_flashcards.pdf` | 20KB | Has error→correction pairs, L1-specific content |
| Progress Tracker PDF | `/download/{job_id}/{project_name}_progress-tracker.pdf` | 10KB | Has can-do statements, L1 checklist |
| PPTX (if requested) | `/download/{job_id}/{project_name}.pptx` | 100KB | Has slides, proper formatting |

Also fetch slide metadata: `GET /api/jobs/{job_id}/slides` — lists all slides with sizes.

### Step 4: Validate Content Quality

For slides (inspect the HTML bundle):
- [ ] Every slide > 2500 bytes (no blank/empty slides)
- [ ] Every slide has `data-speaker-notes` attribute with teacher notes
- [ ] CCQs appear BEFORE grammar formulas
- [ ] L1 Oracle slides exist for each specified L1 language
- [ ] L1 Oracle slides have specific error examples (red: wrong, green: correct)
- [ ] No two slides have identical content
- [ ] 80/20 visual rule: mostly visual elements, not walls of text
- [ ] Theme is applied (check for CSS variables, consistent colors)

For worksheet:
- [ ] Section A: Fill-in-the-gap exercises
- [ ] Section B: Error correction
- [ ] Section C: L1-specific drill (references the correct L1 language)
- [ ] Section D: Write your own (production)
- [ ] Section E: Answer key
- [ ] Section F: Homework suggestions

For activity guide:
- [ ] Multiple activities listed
- [ ] Each activity has instructions
- [ ] Differentiation notes (support + extension)
- [ ] Age-appropriate activities

For flashcards:
- [ ] At least 8-10 cards
- [ ] Front: error sentence (with indication it's wrong)
- [ ] Back: correction + explanation
- [ ] L1-specific content is present

For progress tracker:
- [ ] "After this lesson I can..." checklist
- [ ] Stars/rating system
- [ ] L1 error checklist
- [ ] Example sentences

### Step 5: Report Results

For each test, produce a structured report:

```markdown
## Test N: [Grammar] for [L1] speakers at [Level]

**Request:** [original teacher request]
**Job ID:** [id]
**Generation time:** [time from submit to done]
**Status:** PASS / FAIL

### Files Generated
| File | Size | Status |
|------|------|--------|
| Bundle | X KB | ✅/❌ |
| Worksheet DOCX | X KB | ✅/❌ |
| ... | ... | ... |

### Slide Summary
1. Slide 01 (XX KB): Title slide — "Present Simple"
2. Slide 02 (XX KB): CCQs — concept checking
...

### Quality Issues
- [List any problems found]

### Visual Assessment
- Theme used: [describe colors, fonts]
- Layout density: [too sparse / good / too dense]
- Would I pay a subscription? [yes / no, explain]
```

## 3. Test Suite

### Batch 1: Basic Validation (3 tests)
Verify the pipeline works end-to-end with varied parameters.

| Test | Grammar | L1 | Level | Age | Skill | PPTX? |
|------|---------|-----|-------|-----|-------|-------|
| 1 | Present Perfect | Japanese | A2 | Adults | Speaking | No |
| 2 | Second Conditional | Arabic | B1 | Teens | Writing | Yes |
| 3 | Passive Voice | French + German | B2 | Adults | Grammar | No |

### Batch 2: Edge Cases (3 tests)
Test unusual combinations and edge cases.

| Test | Grammar | L1 | Level | Age | Skill | PPTX? |
|------|---------|-----|-------|-----|-------|-------|
| 4 | Phrasal Verbs | Korean | B1 | Adults | Speaking | Yes |
| 5 | Articles (a/an/the) | Russian + Chinese | A1 | Children | Mixed | No |
| 6 | Reported Speech | Turkish | C1 | Adults | Writing | Yes |

### Batch 3: Stress & Variety (4 tests)
Maximum variety, maximum materials, different skill focuses.

| Test | Grammar | L1 | Level | Age | Skill | PPTX? |
|------|---------|-----|-------|-----|-------|-------|
| 7 | Gerunds vs Infinitives | Italian | B2 | Adults | Grammar | No |
| 8 | Question Formation | Thai | A2 | Young Learners | Speaking | Yes |
| 9 | Mixed Conditionals | Vietnamese + Polish | C1 | Adults | Writing | No |
| 10 | Future Perfect | Hindi + Swedish | B1 | Teens | Listening | Yes |

Notice: 10 tests, zero repeats. Every grammar point different. Every L1 combination different. Multiple levels and age groups.

## 4. Common Failure Modes

When a test fails, check these first:

1. **404 on download** → File wasn't generated. Check if `ConvertDocument` ran. Check Railway logs.
2. **Empty slide** → DeepSeek API call failed silently. Check ModifySlide logs.
3. **Missing L1 Oracle** → L1 data wasn't loaded properly. Check `_load_yaml_data()`.
4. **Stuck at "generating"** → Model is thinking (DeepSeek may still output thinking tokens despite setting). Wait longer.
5. **Small file sizes** → Content generation partially failed. Check if all slides passed validation.
6. **No DOCX/PDF** → `ConvertDocument` step failed. Check if `.source.html` exists.
7. **No PPTX** → Either wasn't requested (correct) or `BuildPptxFromHtmlSlides` failed (bug).

## 5. Railway Debug Commands

When something goes wrong, use these to inspect the Railway filesystem:

```bash
# Check if files exist
railway run ls -la /app/data/mnt/

# Find the project directory
railway run ls -la /app/data/mnt/*/presentations/
railway run ls -la /app/data/mnt/*/documents/

# Check slide content
railway run cat /app/data/mnt/{project}/presentations/slide_01.html

# Check checkpoint progress
railway run cat /app/data/mnt/{project}/presentations/_checkpoint.json

# Check logs for errors
railway logs --service cogniesl
```

## 6. Success Criteria for Phase 1

All tests in Batch 1 must pass. This means:
- All 10 pipeline steps complete without errors
- Every requested file exists and is non-trivial
- L1 Oracle content is present for every specified L1
- Speaker notes exist on every slide
- Visual quality passes the "would I pay?" test
- PPTX exists when requested, absent when not requested
- Worksheet has all 6 sections
- Progress tracker references correct L1

When Batch 1 passes, proceed to Batch 2. When Batch 2 passes, proceed to Batch 3.
When all 10 tests pass, CogniESL Phase 1 is complete.
