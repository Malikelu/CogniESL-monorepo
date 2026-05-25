# CogniESL — Master Plan
**Last updated:** 2026-05-25 (evening)
**Reference docs:** [IMPROVEMENT_IDEAS.md](IMPROVEMENT_IDEAS.md) · [docs/SELF_RUNNING_COGNIESL.md](docs/SELF_RUNNING_COGNIESL.md) · [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) · [docs/HERMES_AGENTS.md](docs/HERMES_AGENTS.md) · [forge plan](../forge/docs/DATA_DEEP_TREATMENT_PLAN.md)

---

## What's Built (code-complete)

- Full generation pipeline: chat → Content Brief → HTML slides + PPTX + worksheet PDF + activity guide PDF
- HTML presenter (`/present/[jobId]`): keyboard nav, speaker notes, fullscreen, bundle download. PPTX is secondary optional export.
- L1 Oracle slides for all 36 native languages. CCQs before formulas. CSS freedom (PPTX constraints removed).
- User accounts: register, login, JWT, My Materials library, Present button, download buttons
- Feedback widget on every material card (😍/👍/👎 + issue tags → `feedback` + `events` DB tables → `POST /api/feedback`)
- Frustration detection instruction in agent (Part 8 of `agent/instructions.md`)
- Password reset, account deletion (GDPR), usage counter, free tier enforcement
- Privacy Policy, Terms of Service, Pricing page with Founding Member counter
- Stripe: checkout, webhook, tier upgrade (needs price ID fix before going live)
- Founder Dashboard (`/admin`): **CEO Command Center** — 4 tabs (Digest, Details, Agents, Intelligence), 13 new API endpoints, churn risk scoring, content quality heatmap, agent approval queue, engagement funnel, user drill-down modal, 30-day sparklines, daily digest. Full spec: [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md)
- Master Repository cache: `QueueGenerationJob` checks cache on hit, `MarkJobComplete` stores on success
- Curator Agent (`agent/curator_agent.py`): CLI + scheduler, pre-populates top combinations
- Auth DB persistence fix: `COGNIESL_DATA_DIR` env var — survives Railway deploys once Volume attached
- Marketing website: L1-specific hero, slide mockup, founding progress bar, waitlist wired
- **Brand identity** (`brand/`): logo finalized — C-arc integrated wordmark. 8 SVG files (wordmark + symbol, 4 variants each: light, dark, white, mono). Full brand guidelines in `brand/BRAND_GUIDELINES.md`.

**What's waiting to be deployed:** All of the above. Nothing has been deployed since the auth fixes. See Track 1.

---

## Track 0 — Logo ✅ DONE

C-arc integrated wordmark. The arc is the letter C in CogniESL — mark and type are one element. Bold stroke teal (#0b7272) with green uptick (#1baa6e). All files in `brand/logos/`. Guidelines in `brand/BRAND_GUIDELINES.md`. V2, V3, and 5e are now unblocked.

---

## Active Work — 4 Parallel Tracks

All four tracks run at the same time. Track 1 needs Marcos. Tracks 2, 3, 4 are Claude's work.

---

### Track 1 — Marcos manual steps ← unblocks everything

```
[ ] Attach Railway Volume: cogniesl service → Volumes → Add → mount path /app/data
[ ] Run: railway up  (deploys all code from last 3 sessions)
[ ] Fix Stripe price IDs in Railway env vars: replace prod_... with price_... (Stripe Dashboard → Products → copy price_... ID)
[ ] Test generation end-to-end on Railway (Present Simple, Spanish, Adults, B1)
[ ] Test Stripe checkout: card 4242 4242 4242 4242
[ ] Open /admin, verify Founder Dashboard shows real data
```

---

### Track 2 — forge database ← blocks quality testing (Phase E)

The `forge/` folder enriches YAML files with deep academic content before syncing to CogniESL.
CogniESL currently has the initial-enriched data (all files have structure, but shallow content).
Forge has deeper versions but **nothing is synced yet**. Full plan: [forge/docs/DATA_DEEP_TREATMENT_PLAN.md](../forge/docs/DATA_DEEP_TREATMENT_PLAN.md)

**CRITICAL ISSUE**: Arabic/Spanish/Mandarin L1 files (3 of top 5 US ESL languages) have ALL
interference_patterns as bare strings — completely unusable for L1 Oracle slides. These must
be fixed first before any L1 work can be synced.

```
[ ] CRITICAL: Fix 1,510 L1 string patterns (AR 719 + ES 289 + ZH 502) → structured dicts
[ ] Phase 1: Complete grammar deep treatment (296 files with per-claim citations)
    — 128 files have CCQ purposes but need sources + discourse + register upgrades
    — 166 files need full rewrite to deep standard
[ ] Phase 2: Complete L1 interference expansion (31 languages to Portuguese gold standard)
[ ] Phase 3: Create writing database (18 files across genres/process/conventions)
[ ] Phase 4: Add skill_area tags + L1-aware differentiation to activities (218 files)
[ ] QA: Full validation — automated + spot-check + AI flow integration test
[ ] SYNC: copy forge/data/ → CogniESL/data/ (only after QA passes)
[ ] Smoke test: verify L1 Oracle slides from structured patterns
```

---

### Track 3 — App features (Claude builds, no deploy needed to build)

Priority order from [IMPROVEMENT_IDEAS.md](IMPROVEMENT_IDEAS.md). All unblocked except where noted.
Logo (Track 0) is a dependency for items marked ← NEEDS LOGO.

```
[~] 5g  Daily digest email to Marcos — email function built, needs scheduler wiring
        (Phase I-3). Daily digest API + CEO Digest dashboard tab done.

[ ] 3a  Lesson plan cover page — added to every generation. Structured: objective, duration,
        stage-by-stage plan with slide numbers, CCQs, anticipated L1 difficulties, differentiation.
        Data all comes from grammar + L1 YAML already loaded.

[ ] V1  Hook/visual slide — between cover page and content slide 1. A full-bleed thematic
        image or animated visual tied to the grammar point and age group. Uses grammar YAML
        `use` field to determine real-world context. Adults: workplace/daily life.
        Teenagers: pop culture/sports/social. Children: cartoons/games. No text-heavy content.
        Pre-generated as a static HTML slide template with dynamic background image/color scheme.

[✅] V2  Closing brand slide — last slide of every deck. Pre-generated HTML template:
        logo centered, tagline, cogniesl.com. Inserted at position -1 in every deck.

[✅] V3  Slide watermark — CogniESL symbol SVG embedded in slide base template.
        Bottom-right corner. Free tier: 50% opacity. Pro/Founding: 25% opacity.
        Implemented as inline SVG + CSS in html_writer_instructions.md base template.

[ ] V4  Flashcard set as chat format option — add "🃏 Flashcard set" to the format buttons
        shown at chat open (alongside Slides, Worksheet, Activity Guide). Keep "All of them."
        Teachers who skip the button still learn the option exists. The flashcard generation
        itself (3e) is built alongside this UI change.

[ ] 5d  Social share prompt — after clean delivery (no frustration signals): 4 pre-written
        templates + platform buttons. All templates must include @cogniesl or #cogniesl.
        Agent adds one line to completion message.

[ ] 5f  Google review request — after teacher's 3rd successful generation. One-time only,
        requires: no frustration detected, 7+ days since signup.

[ ] 3b  Homework section F in worksheet — 2–3 harder exercises using production context from
        grammar YAML, designed for outside-class completion. Same pipeline, small addition.

[ ] 5e  Branded slide snapshot — Playwright screenshots slide 1 → 1080×1080 PNG → CogniESL
        watermark → attached to delivery email. Strongest viral mechanic. ← NEEDS LOGO

[ ] 3c  Pronunciation guidance slide — phonetics data already in grammar YAML (/s/ /z/ /ɪz/
        groupings + L1-specific phoneme difficulties). One new slide per deck.

[ ] 3e  Flashcard set PDF — 10–15 cards from common_errors + use context. Print-and-cut format.
        No new data needed. ~$0.05 added to generation cost. Built together with V4 UI change.

[ ] 3d  Student progress tracker — 1-page self-assessment: "After this lesson I can..." matching
        the specific lesson objectives and L1 errors from the generation.

[ ] 1c  L1→English comparison box in Oracle slides  ← BLOCKED on forge Track 2 Phase 2
        Needs L1 sample sentences in YAML. Top 5 languages (Spanish, Mandarin, French,
        Arabic, Portuguese) have them. Others need forge enrichment first.
```

---

### Track 4 — Self-running system ← full vision in [docs/SELF_RUNNING_COGNIESL.md](docs/SELF_RUNNING_COGNIESL.md)

Build in phases. Each phase delivers standalone value.

**Dashboard technical spec:** [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) — complete reference for all DB tables, API endpoints, dashboard UI, and debugging.

```
PHASE I-1 ✅ DONE
  [✅] Feedback widget on material cards (😍/👍/👎 + issue tags)
  [✅] feedback + events tables in DB, POST /api/feedback endpoint
  [✅] Frustration detection in agent instructions

PHASE I-2 ✅ DONE — Marcos visibility
  [✅] Feedback view in Founder Dashboard (Feedback Center with tags + rating + resolve)
  [✅] Engagement Pulse cards (DAU/WAU/MAU, one-and-done)
  [✅] User drill-down modal (click email → generations/materials/feedback/events tabs)
  [✅] User detail API endpoint (GET /api/admin/users/{id})
  [✅] Event timeline API endpoint (GET /api/admin/events)
  [✅] Engagement stats API endpoint (GET /api/admin/engagement)
  [✅] Agent infrastructure — agent_actions table + log/list/resolve functions + API endpoints
  [✅] Agent Command Center tab (pending queue with approve/reject, activity feed)
  [✅] report_writer.py stub (extension point for future agent reports)
  [✅] Intelligence layer — churn risk scoring, engagement funnel, content quality heatmap
  [✅] Daily digest API endpoint (GET /api/admin/daily-digest) — aggregates all metrics
  [✅] CEO Digest tab (default view — at-a-glance + actions needed + system health)
  [✅] 30-day trend sparklines
  [✅] Tab navigation (Digest / Details / Agents / Intelligence)
  [✅] Tab badges (action count, agent pending count)
  [✅] Auto-refresh every 5 minutes
  [✅] Daily digest email function (FOUNDER_EMAIL env var; not yet scheduled)

PHASE I-3 — Quality self-monitoring (~2 sessions)
  [ ] Wire daily digest email to scheduler (7am daily — needs FOUNDER_EMAIL env var on Railway)
  [ ] Output sampler: randomly samples 1 in 10 generations, checks quality checklist, flags
      degradation in Marcos digest
  [ ] Feedback classifier: groups "issues" feedback by type weekly, adds summary to digest
  [ ] Bug triage: reads Railway logs daily, classifies errors by severity

PHASE I-4 — Growth engine (~2 sessions)
  [ ] Social share prompt after delivery (same as Track 3 5d)
  [ ] Google review solicitor after 3rd generation (same as Track 3 5f)
  [ ] Branded snapshot in delivery email (same as Track 3 5e)
  [ ] Reddit/TEFL monitor: detect mentions, flag to Marcos for response

PHASE I-5 — Content intelligence (~3 sessions)
  [ ] Content QA agent: detects forge updates, proposes sync — never auto-applies, Marcos approves
  [ ] Database curator: identifies which grammar+L1 combinations get poor feedback, prioritizes in forge
  [ ] SEO content agent: drafts blog posts from grammar+L1 database, queues for Marcos approval

PHASE I-6 — Email intelligence (later)
  [ ] Email classifier: reads teacher replies, classifies bug/praise/feature/content error
  [ ] Draft responder: drafts replies for common types, Marcos sends
  [ ] Analytics reviewer: weekly Plausible digest — signup funnel, drop-off, top pages
```

---

## Quality Testing & Launch (after Track 1 + Track 2)

These can only happen once the deploy is live and the forge sync is done.

```
QUALITY (Phase E) — blocked on Track 2 sync + Track 1 deploy
  [ ] Generate: Present Simple, Spanish, Adults, B1, all 3 formats
  [ ] Inspect every slide in HTML presenter — visual checklist in CLAUDE.md
  [ ] Download PPTX + worksheet PDF + activity guide, open each
  [ ] Fix any layout issues in agent/slides_tools/html_writer_instructions.md
  [ ] "Would I show these to a paying teacher and feel proud?" ← done when yes

LAUNCH (Phase F) — blocked on Phase E sign-off
  [ ] Record 90-second demo video (QuickTime, screen recording, script in Phase F section below)
  [ ] Write 3 SEO articles using CogniESL database as source material
  [ ] Email waitlist: personal note from Marcos, Founding Member offer, link to demo
  [ ] Run Curator Agent overnight to pre-populate top 50 combinations (~$75 one-time)
  [ ] Hook curator_agent.run_scheduled() into server.py startup
```

---

## Dependency Map

| Item | Blocked by |
|------|-----------|
| Phase E quality testing | Track 1 deploy + Track 2 forge sync |
| Phase F launch | Phase E sign-off |
| Track 3 item 1c (L1 comparison box) | Track 2 Phase 2 (L1 expansion) |
| Curator Agent overnight run | Track 1 Railway Volume attached |
| Stripe working | Track 1 price ID fix + deploy |
| Founder Dashboard verified | Track 1 deploy | Full dashboard spec: [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) |
| **Everything in Track 3 and Track 4 I-2 through I-6** | **Nothing — build now** |

---

## Phase F Detail — Launch Preparation

### Demo Video Script (90 seconds, QuickTime screen recording)
- 0:00–0:20 "I spent hours making grammar slides. Then I built this."
- 0:20–0:50 Type the request → show Content Brief → approve → wait
- 0:50–1:20 Open email → open HTML presenter → click through slides → pause on L1 Oracle slide
- 1:20–1:30 "CogniESL. Try free at cogniesl.com."
Post: marketing homepage (autoplay muted), YouTube (unlisted), Reddit r/TEFL

### SEO Articles (publish at /blog/{slug})
1. "Most common Present Simple errors for Spanish ESL students"
2. "Why Chinese ESL students struggle with articles (and how to teach it)"
3. "Past Simple: the top mistakes by native language"

### Waitlist Email
Personal note from Marcos. Under 200 words. Founding Member offer ($7/month locked, first 100 only). Link to demo video + pricing page.
