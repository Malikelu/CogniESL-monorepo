# CogniESL: Scaling, Storage & Master Repository Vision
**Status:** Strategic planning — not yet implemented  
**Last updated:** 2026-05-22

---

## The Core Questions This Document Answers

1. Will storing files for every teacher cost a lot of money?
2. Will teachers have their own personal space?
3. Can teachers access past materials?
4. Can we pre-generate common combinations to avoid regenerating the same thing over and over?

---

## 1. Storage Reality Check

### What each project costs in storage
Every time a teacher generates a set of slides, this is what gets saved:
- 15 HTML slide files × ~8KB average = ~120KB
- 1 PPTX file = ~15–35MB (the dominant cost)
- 15 HTML snapshot files (the `.pptx.slides` folder) = ~120KB

**Total per project: ~15–35MB, dominated by the PPTX.**

### At scale
| Teachers | Projects per teacher | Total projects | Storage |
|---|---|---|---|
| 100 | 5 | 500 | ~12GB |
| 1,000 | 10 | 10,000 | ~250GB |
| 10,000 | 10 | 100,000 | ~2.5TB |

On Railway (current deployment target), storage is relatively expensive. On AWS S3 or similar object storage, 2.5TB costs ~$57/month — acceptable at scale but not trivial.

### The optimization: PPTX is the main cost, HTML is almost free
HTML slides are ~8KB each. Keeping HTML files forever costs almost nothing. The PPTX is 2,000× bigger. **One option: store HTML forever, regenerate PPTX on-demand when the teacher downloads.** PPTX rebuild from existing HTML takes ~30 seconds. This alone cuts storage cost by ~99%.

---

## 2. Per-User Personal Spaces

### Current state (no accounts)
Right now all files sit in one flat folder: `mnt/{project_name}/`. There is no concept of "this project belongs to this teacher." If two teachers both generate "present simple for Spanish adults," their projects would collide.

### What needs to exist for production
Each teacher needs their own namespace:
```
mnt/
  {user_id}/
    present_simple_spanish_adults/
      presentations/
        slide_01.html ... slide_15.html
        deck.pptx
    third_conditional_chinese_teens/
      ...
```

This requires:
- **User authentication** — email/password or Google OAuth
- **Session → user mapping** — every API call includes a user token
- **Storage isolation** — each user's files are in their own folder (or S3 bucket prefix)
- **A simple database** — maps user_id → list of project_names, created_at, grammar_point, etc.

### What teachers see: "My Materials" library
A panel in the CogniESL UI showing each teacher's past projects:
- Thumbnail of slide 1
- Grammar point + L1 + Level tag
- Date created
- Buttons: Download PPTX | Edit in chat | Delete

Clicking "Edit in chat" opens a conversation pre-loaded with that project's context, so the teacher can immediately request single-slide changes without having to explain what they were working on.

---

## 3. Past Materials Access

### What teachers need to be able to do with past materials
- **Re-download** a PPTX they generated 3 months ago
- **Update** a deck they generated before (e.g., "add a worksheet to my present simple deck")
- **Fork** a deck (e.g., "make a version of this for B2 instead of A2")
- **Share** a deck with a colleague (future — requires sharing permissions)

### Re-download
If we store HTML files permanently (cheap) and regenerate PPTX on demand (30 seconds), re-download is simple. The system finds the HTML files, runs `BuildPptxFromHtmlSlides`, returns the PPTX. Teacher doesn't notice the difference.

### Update
This is the single-slide change flow from Phase 4C. Works as long as the HTML files still exist.

### Fork
Teacher says "make a B2 version of my present simple deck." Agent creates a new project folder, copies the original HTML files as a starting point, then modifies the relevant slides for B2 level. Faster than generating from scratch.

---

## 4. The Master Repository — The Big Idea

### The problem with generating everything fresh
Right now every teacher who asks for "Present Simple for adult Spanish speakers at B1" triggers:
- ~3–5 API calls to read the database
- 15 sub-agent calls to generate slides
- ~38 minutes of generation time
- ~$2–3 in API costs

If 50 teachers ask for the same combination this week, that's $100–150 in costs for generating identical content 50 times.

### The insight: most requests cluster around a small set of combinations
The grammar combinations that ESL teachers actually teach are not random. There's a clear power law:
- Present Simple, Present Continuous, Past Simple, Present Perfect = 40%+ of all ESL lessons
- Spanish, Chinese/Mandarin, Brazilian Portuguese, French, Arabic = 60%+ of all L1s
- Adults (B1) + Teens (A2) = 70%+ of contexts

**If you map the top 20 grammar points × top 5 L1s × 2 age groups × 3 levels = 600 combinations.** Those 600 combinations likely cover 70–80% of all real teacher requests.

### The Master Repository concept
A pre-generated library of the most common combinations, built once, served many times.

```
master_repository/
  present_simple__spanish__adult__b1/
    slide_01.html ... slide_15.html   ← source HTML (the canonical version)
    deck.pptx                          ← pre-built PPTX
    metadata.json                      ← {grammar_point, l1, level, generated_at, version}
  present_simple__chinese__teen__a2/
    ...
  past_simple__spanish__adult__b1/
    ...
```

**When a teacher requests a combination that exists in the master repository:**
1. Check → cache hit
2. Copy the master files to the teacher's personal space (instantaneous)
3. Return the PPTX immediately — **no generation, no API cost, no wait**
4. Teacher gets their materials in seconds instead of 38 minutes

**When a teacher requests a combination not in the repository:**
1. Generate fresh (current flow)
2. If it's a "common" combination (e.g., top 5 grammar × top 5 L1 → 25 combos), automatically add it to the master repository for future teachers
3. If it's rare, store only in teacher's personal space

### Cache hit economics
| Scenario | Cost per request | Time |
|---|---|---|
| Cache miss (generate fresh) | ~$2–3 | 20–40 min |
| Cache hit (serve from repo) | ~$0.00 (storage bandwidth) | <5 seconds |
| Cache hit + single-slide customization | ~$0.15 (1 slide) | ~1 min |

If 70% of requests are cache hits, the average cost per request drops from $2.50 to ~$0.75. At 1,000 requests/month, that's saving ~$1,750/month in API costs. At 10,000 requests/month, savings are ~$17,500/month.

### Personalization on top of cached content
A cached deck is a starting point, not a final product. Teachers often want small customizations:
- "Add an example about technology instead of medicine"
- "Make the hook slide about my city"
- "Add my school's name somewhere"

These become single-slide modifications on a **fork** of the cached deck. The master repository is never modified — each teacher gets their own copy that they can customize.

```
teacher_A/
  present_simple__spanish__adult__b1/      ← forked from master, modified slide_06
    slide_01.html ... slide_05.html        ← identical to master
    slide_06.html                          ← teacher_A's custom version
    slide_07.html ... slide_15.html        ← identical to master
    deck.pptx                              ← rebuilt with teacher_A's slide_06
```

This gives teachers the feeling of a fully personalized deck while the system does minimal work.

---

## 5. The AI Curator Agent

This is the most forward-looking idea. Instead of manually deciding which combinations to pre-generate, an AI agent monitors usage patterns and manages the repository automatically.

### What the Curator Agent does

**Demand prediction:** Tracks which combinations are requested most. Notices when "Present Perfect for Brazilian Portuguese adults" is being requested 3× per week and proactively generates it before the next request comes in.

**Quality control:** Periodically re-validates master repository decks. If the YAML database is updated (new CCQs, better examples), flags affected decks for regeneration.

**Repository pruning:** Removes master decks that haven't been used in 6+ months to save storage. Keeps a "has been requested" counter per combination.

**Gap analysis:** Identifies combinations that are frequently requested but missing from the repository. Generates a priority list for the next batch of pre-generation.

**Seasonal awareness:** Knows that "Present Simple" requests spike in September (new school year) and pre-generates the most common variants in August.

**Model upgrade evaluation + regeneration:** When a new LLM is being considered, the Curator Agent runs an automatic benchmark evaluation and produces a scored report so Marcos can make an informed decision — without having to guess whether the new model is actually better for CogniESL's specific task.

### The Benchmark Suite (10 fixed slides)
The Curator maintains a permanent set of 10 fixed task briefs — always the same grammar points, L1s, and slide types. When evaluating a new model, BOTH models generate these exact same 10 slides:

| # | Slide type | Grammar | L1 |
|---|---|---|---|
| 1–2 | Hook (A1) | Present Simple / Present Perfect | — |
| 3–4 | CCQ (A3) | Present Simple / Past Simple | — |
| 5–6 | Formula (A5) | Third Conditional / Passive Voice | — |
| 7–8 | L1 Oracle (A6) | Present Simple / Present Perfect | Spanish / Chinese |
| 9–10 | Practice (A7) | Articles / Present Perfect | — |

### The Judge LLM
A separate, capable LLM (whichever is NOT being evaluated — e.g., Claude Opus if testing GPT-5, or GPT-4o if testing Claude) scores each slide against a fixed rubric:

| Criterion | What it measures | Weight |
|---|---|---|
| Visual richness | Gradients, color usage, layout density, visual hierarchy | 20% |
| YAML accuracy | CCQ wording verbatim, exact examples, exact formula | 30% |
| L1 Oracle quality | Wrong→Correct clarity, why_it_happens present, L1 specificity | 30% |
| Speaker notes | Specific teacher actions, real CCQs with answers, L1 watch-for | 20% |

### The Report Format
After running the benchmark, the Curator produces:

```
BENCHMARK REPORT — [current model] vs [candidate model]
Evaluated: 10 slides × 4 criteria

                         Current    Candidate    Δ
Visual richness            6.8        8.1       +19%  ✅
YAML accuracy              8.2        8.5       +4%   ✅
L1 Oracle quality          7.1        8.9       +25%  ✅ (biggest gain)
Speaker notes              6.3        7.0       +11%  ✅
──────────────────────────────────────────────────────
Overall (weighted)         7.3        8.2       +12%

Recommendation: UPGRADE — consistent improvement across all criteria.
Estimated repository regeneration cost: ~$48 (96 decks × ~$0.50)
Suggested regeneration order: L1 Oracle slides first (largest quality gap),
then Hook slides, then Formula slides.

[Links to side-by-side HTML previews for each benchmark slide pair]
```

**If the new model scores WORSE on YAML accuracy or L1 Oracle quality** (even if overall score is higher), the report flags a hard warning: *"New model shows regression on critical criteria — DO NOT upgrade without further investigation."* These two criteria are non-negotiable: a model that invents CCQs or L1 examples is worse, full stop, regardless of how pretty the slides look.

**If scores are within 5%** either way: *"Inconclusive — recommend running a teacher preview panel before deciding. Cost difference does not justify regeneration at this margin."*

### Triggering an evaluation
Marcos says to the Curator Agent: *"We're testing [new model] for slide generation."*
The Curator runs overnight and delivers the report next morning. Cost: ~$2 total (10 slides × $0.15 + judge calls × $0.05).

### After approval: staged regeneration
- Every master deck's `metadata.json` stores `model_id` (e.g., `"gpt-4.1"`) and `model_score` (the benchmark score at time of generation)
- Approved new model replaces current production model
- Curator queues all master decks whose `model_id` ≠ current production model for regeneration
- Regeneration runs in batches overnight, sorted by popularity (most-requested first)
- Suggested batch size: 25 decks/night — balances speed with API cost control

**What stays the same for teachers:**
- Teachers who already received a deck are NOT affected — their personal copy stays as-is
- Only the master repository is updated
- Next time any teacher requests that combination (cache hit), they automatically get the upgraded version
- Teachers who want their old deck upgraded can ask the agent: *"Re-generate my present simple slides with the latest model"* → triggers a fresh fork from the new master

### How the Curator Agent runs
- Scheduled task (daily or weekly) — uses the existing `mcp__scheduled-tasks` infrastructure
- Reads the request log from the server
- Makes generation decisions based on frequency thresholds
- Checks `MODEL_TIER_REGISTRY` for pending upgrade regeneration queue
- Runs overnight when API rate limits are cheaper/less contested
- Reports: "Generated 12 new master decks this week. Pruned 3 unused decks. Upgraded 47 decks to gpt-5 tier. Repository now covers 78% of historical requests."

---

## 6. The Full Architecture Vision

```
[Teacher opens CogniESL]
        ↓
[Chat interview: grammar, L1, level, age, format]
        ↓
[Content Brief Preview — teacher approves]
        ↓
[Cache check: does master_repository have this combination?]
        ↓                           ↓
   YES (cache hit)              NO (cache miss)
        ↓                           ↓
[Copy to teacher's space]    [Generate fresh — 20–40 min]
        ↓                           ↓
[Optional: 1–2 slide       [If common combination:
 customizations via chat]    add to master_repository]
        ↓                           ↓
[Deliver PPTX]              [Store in teacher's space]
        ↓                           ↓
[Teacher's "My Materials"   [Deliver PPTX]
 library updated]
        ↓
[Future: teacher returns, requests single-slide edit]
        ↓
[ModifySlide on teacher's fork → rebuild PPTX → re-deliver]
```

---

## 7. Implementation Roadmap (rough phases)

### Phases 1–5 ✅ Complete
- Phase 1–3: Chat interview, generation pipeline, performance baseline
- Phase 4: Content Brief Preview + post-generation message + single-slide edits + project memory
- Phase 5: Async generation + email delivery (implemented, pending live test)

### Phase 5 — Async Generation + Email Delivery ✅ Implemented

This is a **prerequisite for production**. Without it, teachers see "request timed out" errors on any generation over ~90 seconds — which is every real request.

**The problem:** The current architecture holds an HTTP connection open for the entire 20–40 minute generation run. Browsers and servers close connections after 60–120 seconds. Teacher sees an error even though the server is still working.

**The solution:** Decouple generation from the chat connection entirely.

**How it works:**
1. Teacher sends message and selects preferences → agent immediately returns: *"Your materials are being generated! I'll email you when they're ready — usually 15–25 minutes."*
2. Generation runs as a **background job** (separate process/queue), completely independent of the browser session
3. When the job finishes, the system sends a **branded email** with:
   - Download buttons for PPTX, worksheet PDF, activity guide PDF (big, clear, clickable)
   - A summary of what was generated (grammar point, L1, slide count)
   - A preview thumbnail of slide 1 (optional but nice)
   - A link back to the CogniESL chat if they want to request changes
4. Links are direct download URLs — no login required to download (for MVP)

**What the email looks like:**
```
Subject: Your Present Perfect materials are ready!

[CogniESL logo]

Hi Maria,
Your materials for Present Perfect — French Adults — B1 are ready.

[📥 Download Slides (15 slides, PPTX)]    ← big button
[📥 Download Worksheet (PDF)]             ← big button  
[📥 Download Activity Guide (PDF)]        ← big button

Need to change something? Reply to this email or go back to your CogniESL chat.

— The CogniESL Team
```

**Technical components needed:**
- **Job queue**: Redis + a worker process (e.g. Celery, or a simple Python subprocess queue). The FastAPI server enqueues the job and returns immediately; the worker runs the agent.
- **Email service**: Resend or SendGrid (both have generous free tiers — Resend: 3,000 emails/month free). Simple transactional email with HTML template.
- **File serving**: A `/download/{job_id}/{filename}` endpoint on the server that streams the file. The email links point here.
- **Job status tracking**: A simple SQLite table (job_id, status, created_at, completed_at, email, file_paths). The worker updates it; the download endpoint checks it.

**Why email and not in-chat notification:**
- Email works even if the teacher closes the tab
- Email is a marketing touchpoint — every delivery email reinforces the brand
- Teachers expect to wait; email is the natural medium for "it's ready"
- In-chat notifications require WebSockets and persistent connections — more complex

**Why not a progress bar:**
- Progress bars require polling, which requires WebSockets or SSE
- Progress is inherently nonlinear (slide 8 might take 3× longer than slide 7)
- A progress bar that lies is worse than no progress bar
- Better UX: "You'll get an email in ~20 minutes. Go teach your class."

### Phase 6 — User Accounts & Personal Spaces (~2–4 weeks dev)
- Add email authentication (simplest: passwordless magic link)
- Add `user_id` to all project paths: `mnt/{user_id}/{project_name}/`
- Build "My Materials" library UI panel (list of past projects, download buttons)
- Add project metadata database (SQLite or Postgres — start simple)
- Full plan in `PHASE6_PLAN.md`

### Phase 7 — UI/Brand Identity (~1–2 weeks)
- Design and commission a CogniESL logo (primary + favicon versions)
- Apply logo to the product chat UI (Navbar), website, and all email templates
- Align product UI colors/fonts with the website design system (teal #0D7377 + coral #FF6B6B palette)
- Review and refine marketing website copy, testimonials (real), and pricing
- Add real screenshots/demos of generated materials to the website Samples page
- Soft-launch preparation: domain setup, analytics (Plausible), Stripe account

### Phase 8 — Master Repository (~2–4 weeks dev)
- Design the combination key format (grammar_slug + l1_slug + age + level)
- Build the cache check at the start of the generation flow
- Build the "copy from master to teacher space" logic
- Pre-generate the top 50 most common combinations manually (one-time batch job)
- Add automatic "add to master if common" logic after each cache miss

### Phase 9 — Curator Agent (~2–4 weeks dev)
- Build the usage logging infrastructure
- Build the Curator Agent (runs as a scheduled task)
- Add demand prediction and gap analysis
- Add quality control checks against YAML database versions

### Phase 10 — Scale & Optimize
- Move from local disk to S3/R2 for storage
- CDN for PPTX delivery (fast downloads globally)
- HTML-only storage + on-demand PPTX rebuild to cut storage costs
- Usage analytics dashboard for Marcos

---

## 8. Open Questions

1. **Privacy:** Are teachers' materials private to them, or can the master repository use their generated content? (Need consent — probably say "your materials help improve the shared library" in ToS)

2. **Staleness:** If a teacher generated a deck 1 year ago and the YAML database has been updated since, should they get a notification? Or auto-update silently?

3. **Sharing between teachers:** Should a teacher be able to share a link to their deck with a colleague? This is a viral growth vector — free word-of-mouth. Probably yes, but requires permissions design.

4. **White-labeling:** Some schools will want materials branded with their logo. How does this interact with the master repository? (Answer: it's a post-generation modification — add a logo watermark to the PPTX. Doesn't affect the cache system.)

5. **How common is "common enough"?** What threshold of requests triggers adding a combination to the master repository? Suggested starting point: 3+ requests for the same combination within 30 days.

6. **Who pays for pre-generating the master repository?** The initial batch of 600 pre-generated decks costs ~$300–1,500 in API calls. This is a one-time infrastructure investment that pays back quickly.
