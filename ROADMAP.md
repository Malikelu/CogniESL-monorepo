# CogniESL — Master Plan
**Last updated:** 2026-05-25 (session 2)
**Reference docs:** [IMPROVEMENT_IDEAS.md](IMPROVEMENT_IDEAS.md) · [docs/SELF_RUNNING_COGNIESL.md](docs/SELF_RUNNING_COGNIESL.md) · [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) · [docs/HERMES_AGENTS.md](docs/HERMES_AGENTS.md) · [forge plan](../forge/docs/DATA_DEEP_TREATMENT_PLAN.md)

---

## What's Built (code-complete)

- Full generation pipeline: chat → Content Brief → HTML slides (with watermark + closing brand slide) + **offline HTML bundle** (primary) + worksheet PDF (Sections A–F + Answer Key) + activity guide PDF + flashcard PDF + student progress tracker PDF. PPTX available on request only.
- **HTML-first presentation**: `BuildOfflineBundle` packages all slides into a single self-contained `.html` file — Google Fonts + Font Awesome + images all inlined as base64. Works offline. Fullscreen (F), speaker notes (N), arrow key navigation. Featured in delivery email with "how to open" tip. See [docs/HTML_FIRST_STRATEGY.md](docs/HTML_FIRST_STRATEGY.md)
- **CSS animations enabled**: `html_writer_instructions.md` PPTX constraints removed. Animations required on Hook, L1 Oracle, Wrap-up slides. Full Animation Guidelines section added with copy-paste patterns.
- **Hook slide with real images (V1)**: `ImageSearch` + `DownloadImage` fetches a contextual photo before A1 slide generation. Photo inlined into offline bundle. CSS-gradient fallback if fetch fails. `HOOK_IMAGE` field in A1 task_brief.
- **Decoupled PPTX planned**: future `BuildSimplePptx` generates PPTX from structured content (not from HTML). Spec in [docs/DECOUPLED_PPTX_SPEC.md](docs/DECOUPLED_PPTX_SPEC.md).
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
- **Brand consistency**: C-arc logo deployed everywhere — webui Navbar + logo.svg, email header (HTML text fallback), admin dashboard header, marketing website Navbar + favicon + PWA icons (192/512) + og-image.svg. Old `#0D7377` color replaced with `#0b7272` throughout all CSS/config files.

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
[✅] 5g  Daily digest email to Marcos — scheduler wired in server.py using stdlib threading.
        Fires at 07:00 daily: fetches /api/admin/daily-digest, calls send_daily_digest_email().
        Only starts if FOUNDER_EMAIL + RESEND_API_KEY are set. No APScheduler needed.

[✅] 3a  Lesson plan cover page — first slide of every deck (Section 0). Structured:
        objective (from YAML core_meaning), stage-by-stage plan with slide numbers + times,
        CCQ preview (all CCQs verbatim), anticipated L1 errors (top patterns from L1 YAML),
        differentiation tips. Implemented as slide type A0 in html_writer_instructions.md
        + task_brief format in instructions.md. Teacher-only, not shown to students.
        No watermark on this slide. Minimum deck size updated to 16 slides.

[✅] V1  Hook/visual slide — between cover page and content slide 1. A full-bleed thematic
        image or animated visual tied to the grammar point and age group. Uses grammar YAML
        `use` field to determine real-world context. Adults: workplace/daily life.
        Teenagers: pop culture/sports/social. Children: cartoons/games. No text-heavy content.
        `ImageSearch` + `DownloadImage` fetches a contextual photo (Step A.5 in instructions.md).
        Photo path passed as `HOOK_IMAGE` in A1 task_brief. Inlined into offline bundle by
        BuildOfflineBundle. Graceful CSS-gradient fallback if image fetch fails.

[✅] V2  Closing brand slide — last slide of every deck. Locked HTML template in
        html_writer_instructions.md. Agent calls ModifySlide with SLIDE_TYPE: CLOSING_BRAND.
        Logo centered, tagline "L1-aware teaching materials, made in minutes.", cogniesl.com.
        Teal accent strip at bottom. Not AI-generated — verbatim template output.

[✅] V3  Slide watermark — CogniESL symbol SVG on every content slide. Bottom-right corner.
        Free tier: 65% opacity. Pro/Founding: 35% opacity. WATERMARK field in every task_brief
        controls opacity. Geometry locked to brand symbol path. Added to html_writer_instructions.md
        as Technical Rule #12 + Mandatory Watermark section.

[✅] V4  Flashcard set as chat format option — "🃏 I need flashcards" button added to chat
        quick-start chips alongside Slides, Worksheet, Activity Guide. "✨ I need everything"
        covers all 4 formats. Welcome message updated with flashcard example. Download button
        labels in ChatInterface now correctly detect flashcard PDFs by filename.

[✅] 5d  Social share prompt — added to agent instructions.md (Part 5 post-delivery rules).
        3 pre-written templates (Twitter/X, LinkedIn, Teacher WhatsApp group) with @CogniESL
        and #ESLteacher tags. Appended after the Quick edits block on every delivery.

  [✅] 5f  Google review request — added to agent instructions (after 3rd generation, 7+ days, no frustration)

[✅] 3b  Homework section F in worksheet — added to agent instructions.md worksheet spec.
        4 exercise types (writing prompt, real-world observation, self-correction, translation
        trap). Dashed border, "HOMEWORK — Complete Before Next Class" header. Validation
        checklist updated to require Sections A-F + Answer Key.

[✅] 5e  Branded slide snapshot — `SnapSlideForEmail` tool: Playwright screenshots hook slide
        (slide 2) at 1280×720, crops center square 720×720, scales to 1080×1080, adds teal
        cogniesl.com brand pill watermark. Saves to snapshots/email_preview.png. Embedded as
        base64 inline image in delivery email via `_build_snapshot_html()`. Registered in
        cogniesl_agent.py, called before MarkJobComplete per updated instructions.md.

[✅] 3c  Pronunciation guidance slide — added as slide type A5b in html_writer_instructions.md
        and instructions.md. Soft cream background, 64px+ IPA symbols in teal, ≤3 sound
        groups, amber L1 phoneme callout. Conditional on phonetics data present in YAML.
        Inserted between formula slide (A5) and L1 Oracle (A6).

[✅] 3e  Flashcard set PDF — `GenerateFlashcardPdf` tool in `agent/slides_tools/`. Pulls
        10–15 error/correction pairs from grammar `common_errors` + L1 `interference_patterns`.
        Print-and-cut PDF: page 1 fronts (red error), page 2 backs (teal correction + why).
        Registered in cogniesl_agent.py, wired into instructions.md generation flow.
        MarkJobComplete extended with `flashcard_pdf_path` field.

[✅] 3d  Student progress tracker — `GenerateProgressTrackerPdf` tool: 1-page A4 PDF via
        weasyprint. "After this lesson I can..." with 4-6 skill statements + 4-star rating
        column + L1 error checklist (red strikethrough → teal correction) + example sentence
        lines. Registered in cogniesl_agent.py, call format + data sourcing added to
        instructions.md. MarkJobComplete extended with `progress_tracker_pdf_path`.

[ ] 1c  L1→English comparison box in Oracle slides  ← BLOCKED on forge Track 2 Phase 2
        Needs L1 sample sentences in YAML. Top 5 languages (Spanish, Mandarin, French,
        Arabic, Portuguese) have them. Others need forge enrichment first.
```

---

### Track 4 — Self-running system ↔ full vision in [docs/SELF_RUNNING_COGNIESL.md](docs/SELF_RUNNING_COGNIESL.md)

**Architecture:** Apex (your general assistant) → CogniESL Orchestrator (dedicated profile) → 4 Department Agents. One consolidated daily digest, not 6 separate reports.

**Implementation plan:** [docs/SELF_RUNNING_IMPLEMENTATION.md](docs/SELF_RUNNING_IMPLEMENTATION.md) — detailed phases, DB schema, API specs.

**Dashboard technical spec:** [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) — complete reference for all DB tables, API endpoints, dashboard UI, and debugging.

```
PHASE I-1 ✅ DONE — Feedback foundation
  [✅] Feedback widget on material cards (😍/👍/👎 + issue tags)
  [✅] feedback + events tables in DB, POST /api/feedback endpoint
  [✅] Frustration detection in agent instructions

PHASE I-2 ✅ DONE — Dashboard & agent infrastructure
  [✅] All 4 dashboard tabs (Digest, Details, Agents, Intelligence)
  [✅] 17 admin API endpoints
  [✅] agent_actions table + approve/reject workflow
  [✅] report_writer.py stub
  [✅] CEO Digest auto-refresh

PHASE I-3 — Orchestrator infrastructure (~8 hours)
  [✅] New DB tables: orchestrator_runs, agent_health, agent_messages, agent_costs, critical_alerts
  [✅] New DB functions: orchestrator/health/message/cost/alert operations (14 functions)
  [✅] agent/orchestrator.py — collect, correlate, synthesize, propose
  [✅] agent/monitor_agent.py — output sampler, error tracker, anomaly detector
  [✅] Orchestrator API endpoints (status, run, pause, history, health, alerts, costs)
  [✅] Orchestrator tab on dashboard (agent health matrix + quick actions)
  [✅] Inter-agent routing rules implemented
  [✅] One consolidated daily digest replaces individual agent reports

PHASE I-4 — Monitor Agent (~6 hours) — DONE
  [✅] agent/monitor_agent.py: output sampler, error tracker, anomaly detector
  [✅] Anomaly section in Intelligence tab
  [✅] Critical alert logic (error rate > 10% for 2+ hours triggers email via orchestrator)
  [✅] Wire to orchestrator (runs every 4 hours)

PHASE I-5 — Intel Agent + Cost Tracking (~6 hours) — DONE
  [✅] Intel logic in orchestrator (_run_intel): cost tracking, funnel analysis, suggestions
  [✅] Cost breakdown in Digest tab (daily + weekly trend via /api/admin/costs/daily, /weekly)
  [✅] Agent efficiency metrics in Intelligence tab (submitted vs. approved)
  [✅] Wire to orchestrator (runs daily)

PHASE I-6 — Growth Agent + Mobile (~8 hours) — DONE
  [✅] Growth logic in orchestrator (_run_growth): growth summary, churn risks, superfans, social drafts
  [✅] Google review solicitor (added to agent instructions, after 3rd gen, 7+ days, no frustration)
  [✅] Dashboard mobile optimization (responsive CSS, touch-friendly buttons, scrollable tabs)
  [✅] Wire to orchestrator (runs daily)

PHASE I-7 — Content intelligence (~6 hours) — DONE
  [✅] Content QA: agent/content_qa.py — detects forge updates, proposes sync (never auto-applies, Marcos approves via dashboard)
  [✅] Database curator: identifies grammar+L1 combos with poor feedback (>20% issue rate), flags for regeneration
  [✅] SEO content agent: agent/seo_agent.py — drafts blog posts from grammar+L1 database, queues for Marcos approval
  [✅] Content versioning: agent/content_versioning.py — Git commits for all YAML changes with audit trail

PHASE I-8 — Critical alerts + polish (~4 hours)
  [ ] Wire critical alert triggers into orchestrator (_run_monitor already detects anomalies)
  [ ] Alert acknowledgment flow in dashboard — DONE (ack/resolve buttons in Orchestrator tab)
  [ ] End-to-end testing of all alert types

DEFERRED (need users/revenue first):
  [ ] Secretary Agent (email classification) — needs meaningful email volume
  [ ] Support Agent (teacher questions) — needs active user base
  [ ] Reddit/TEFL monitor — needs brand mentions to exist
  [ ] Autonomous code fix + deploy — too risky without production data
```

**Total Track 4 effort: ~38 hours across 8 phases. Each phase delivers standalone value.**

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
