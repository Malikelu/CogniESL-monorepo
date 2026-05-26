# CogniESL — Status & Morning Checklist
**Last updated:** 2026-05-26

Reference: [ROADMAP.md](ROADMAP.md) · [IMPROVEMENT_IDEAS.md](IMPROVEMENT_IDEAS.md) · [docs/HTML_FIRST_STRATEGY.md](docs/HTML_FIRST_STRATEGY.md) · [docs/DECOUPLED_PPTX_SPEC.md](docs/DECOUPLED_PPTX_SPEC.md)

---

## 🤖 Morning check — 2026-05-26 (updated after build failure)

**Build failure root cause found and fixed.**
Railway's `railway up` respects `.gitignore` when uploading files. `data/` was in `.gitignore`,
so the grammar/L1/activities YAML files were never uploaded → Dockerfile `cp` failed at step 9/11.

**Fix applied:** Removed `data/` from `.gitignore`. The YAML files were always committed to git
(tracked before the ignore rule was added), so they're safe to include. SQLite DBs are still
excluded via the `*.db` rule. `data/writing/` is still excluded.

**Ready to deploy:** YES — run the commands below.

**Marcos: do this now →**
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
git add -A && git commit -m "fix: include data/ YAML files in Railway build (remove from gitignore); 6 pipeline bugs"
railway up
```

After deploy succeeds:
```bash
curl https://cogniesl-production.up.railway.app/api/healthcheck
# Expect: {"status":"ok"} with yaml_count ~302 grammar, ~36 L1, ~220 activities
python test_cogniesl.py
```

---

## What's Built (Code Complete — Waiting to Deploy)

| Feature | Status |
|---------|--------|
| Full generation pipeline: chat → HTML slides + offline bundle + worksheet + activity guide + flashcards + progress tracker | ✅ Built |
| **HTML-first deliverable** — `BuildOfflineBundle` packages all slides into a single self-contained `.html` file (fonts + images inlined as base64, works offline, F=fullscreen, arrow keys nav) | ✅ Built |
| **CSS animations on slides** — hook, L1 Oracle, wrap-up slides have mandatory entrance animations | ✅ Built |
| **Hook slide with real images** — `ImageSearch` + `DownloadImage` fetches a contextual photo before generating A1; inlined into offline bundle | ✅ Built |
| Lesson plan cover slide (A0) — teacher briefing, not shown to students | ✅ Built |
| Pronunciation guidance slide (A5b) | ✅ Built |
| L1 Oracle slides — one per specified native language | ✅ Built |
| Closing brand slide (V2) + slide watermark (V3) | ✅ Built |
| Flashcard PDF (`GenerateFlashcardPdf`) — print-and-cut, fronts + backs | ✅ Built |
| Progress tracker PDF (`GenerateProgressTrackerPdf`) — self-assessment checklist | ✅ Built |
| Branded email snapshot (`SnapSlideForEmail`) — hook slide cropped + watermarked, embedded in delivery email | ✅ Built |
| Worksheet Sections A–F + Answer Key (Section F = homework) | ✅ Built |
| Social share prompt in delivery message | ✅ Built |
| PPTX — opt-in only, generated only when teacher explicitly asks | ✅ Built (spec in [docs/DECOUPLED_PPTX_SPEC.md](docs/DECOUPLED_PPTX_SPEC.md)) |
| User accounts (register, login, JWT, My Materials library) | ✅ Built |
| Password reset + account deletion (GDPR) | ✅ Built |
| Usage counter + free tier enforcement (5 gen/month) | ✅ Built |
| Privacy Policy + Terms of Service pages | ✅ Built |
| Pricing page (/pricing) | ✅ Built |
| Stripe backend (checkout, webhook, founding member counter) | ✅ Built |
| Founder Dashboard (/admin) — CEO Command Center, 4 tabs, 13 API endpoints, churn risk, content quality heatmap | ✅ Built |
| Feedback widget on material cards (😍/👍/👎 + issue tags → DB) | ✅ Built |
| Frustration detection in agent | ✅ Built |
| Master Repository cache (generation deduplication) | ✅ Built |
| Curator Agent (`agent/curator_agent.py`) — CLI + scheduler | ✅ Built |
| Daily digest email scheduler (07:00 daily, threading daemon in server.py) | ✅ Built |
| Brand identity — C-arc integrated wordmark, all logo variants, brand guidelines | ✅ Built |
| Marketing website — L1-specific hero, founding counter, waitlist | ✅ Built |
| Auth DB persistence fix (`COGNIESL_DATA_DIR` env var, Railway Volume ready) | ✅ Built |

**CRITICAL FIXES APPLIED LAST NIGHT (not yet deployed) — see "Deploy First" section below.**

---

## 🚨 Deploy First — Critical Fixes Waiting

These fixes were made overnight and are **not yet on Railway**. Run `railway up` before testing anything.

### What was fixed:
1. **Grammar database broken on Railway** — Root cause found and fixed. Railway's Volume mount at `/app/data` was hiding all the YAML files (grammar, L1, activities). The Dockerfile now copies them to `/app/static-data/` (outside the Volume path) before the Volume overlays. The three search tools now use `COGNIESL_STATIC_DIR=/app/static-data` instead. Without this deploy, the agent always says "I'm unable to access the grammar database."

2. **Agent not starting generation after approval** — Kickoff detection improved. When the agent sends a short "I'll start now" text instead of calling tools, the server detects it and force-retries with a direct tool call instruction. Pre-brief kickoffs and post-approval kickoffs are handled separately.

3. **Security** — Agent was revealing server internals when someone claimed to be the CEO. Fixed in instructions.md.

4. **`/api/healthcheck` endpoint added** — Lets you verify grammar file counts without a full chat test.

5. **`test_cogniesl.py` written** — Automated end-to-end test script (stdlib only, no installs needed).

### To deploy:
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
railway up
```

### To verify deploy worked (run after `railway up` completes):
```bash
# Check grammar files are accessible (should show ~302 grammar, ~36 L1, ~220 activities):
curl https://cogniesl-production.up.railway.app/api/healthcheck

# Run full end-to-end test (takes ~5 min — tests healthcheck + chat + generation):
python test_cogniesl.py
```

If healthcheck shows `"status": "ok"` and all yaml_counts > 0, the grammar database fix worked.

---

## Things Only Marcos Can Do (Track 1)

Do these in order. Each one unblocks the next.

```
[ ] 0. Deploy tonight's fixes (see above — REQUIRED before any testing)

[ ] 1. Attach Railway Volume
        cogniesl service → Volumes → Add → mount path /app/data
        (This makes the user database survive redeploys — do before deploy)

[ ] 2. Deploy: railway up
        Run from: /Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL
        Watch logs — server should start cleanly.

[ ] 3. Fix Stripe price IDs in Railway env vars
        Stripe Dashboard → Products → copy price_... IDs (NOT prod_...)
        Update: NEXT_PUBLIC_STRIPE_PRO_MONTHLY_PRICE_ID
                NEXT_PUBLIC_STRIPE_PRO_ANNUAL_PRICE_ID
                NEXT_PUBLIC_STRIPE_FOUNDING_PRICE_ID
                STRIPE_FOUNDING_PRICE_ID (backend)

[ ] 4. Set email env vars on Railway (if not already set)
        RESEND_API_KEY   = your Resend key
        COGNIESL_FROM_EMAIL = CogniESL <hello@cogniesl.com>
        FOUNDER_EMAIL    = your email (enables daily 7am digest)
        ADMIN_TOKEN      = any secure token (optional — digest auth)

[ ] 5. Test generation end-to-end
        Register at cogniesl-production.up.railway.app
        Chat: "Slides for Present Simple, Spanish speakers, adults, B1"
        Follow interview → approve Content Brief → wait for email
        Open the .html bundle: double-click → F for fullscreen → arrow keys

[ ] 6. Test Stripe checkout
        /pricing → Start Pro → card 4242 4242 4242 4242, any future date, any CVC
        Check Railway logs: [Stripe] Updated user ... → pro

[ ] 7. Open /admin — verify Founder Dashboard shows real data
```

---

## Morning Checks (Once Deployed)

Run these every morning after Railway is live:

```
[ ] Check Founder Dashboard (/admin → Digest tab) — any actions needed?
[ ] Check Railway logs for errors (especially generation failures)
[ ] Open daily digest email — arrived at 7am? Any red flags?
[ ] New signups or generations overnight? Note in a running log.
```

---

## Quick Generation Test (Visual Quality Check)

Use this script every time you want to verify quality:

1. In chat: "Slides + worksheet + flashcards for Present Simple for Spanish-speaking adults, B1"
2. Approve Content Brief after review
3. Wait for email (~5–10 min)
4. Open `.html` bundle — check:
   - Hook slide: does it have a real photo background?
   - Hook slide: does it animate on open?
   - L1 Oracle slide: red error vs green correction present?
   - L1 Oracle slide: slide-in animation works?
   - Closing brand slide: cogniesl.com visible, C-arc logo present?
   - Watermark: bottom-right corner every content slide?
   - All slides > 1 screen of content (no empty slides)?
   - Speaker notes: visible when pressing N?
   - Keyboard nav: left/right arrows work?
   - Fullscreen: F key works?
5. Open worksheet PDF — Sections A–F + Answer Key present?
6. Open flashcard PDF — fronts page (red errors) + backs page (teal corrections)?
7. Check delivery email: branded snapshot image visible? HTML "how to open" tip visible? Download buttons for all files?

---

## Env Vars Required on Railway

| Variable | Value | Notes |
|----------|-------|-------|
| `RESEND_API_KEY` | from resend.com | Required for email delivery |
| `COGNIESL_FROM_EMAIL` | `CogniESL <hello@cogniesl.com>` | Sender address |
| `COGNIESL_BASE_URL` | `https://cogniesl-production.up.railway.app` | For download links in emails |
| `FOUNDER_EMAIL` | your email | Enables daily 7am digest |
| `COGNIESL_DATA_DIR` | `/app/data` | User DB persistence (needs Volume) |
| `ADMIN_PASSWORD` | any secure password | Founder Dashboard login |
| `JWT_SECRET` | any random string | Auth token signing |
| `STRIPE_SECRET_KEY` | from Stripe Dashboard | Payments |
| `STRIPE_WEBHOOK_SECRET` | from Stripe Dashboard | Webhook validation |
| `NEXT_PUBLIC_STRIPE_PRO_MONTHLY_PRICE_ID` | `price_...` | NOT `prod_...` |
| `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` | your key | Generation model |

---

## What's NOT Done Yet

| Item | Blocker | Priority |
|------|---------|----------|
| Phase E quality testing (full inspect on Railway) | Track 1 deploy | High — must before launch |
| Phase F launch (demo video, SEO articles, waitlist email) | Phase E sign-off | High |
| forge database sync (deep YAML → CogniESL data/) | Track 2 (see ROADMAP) | High — blocks L1 quality |
| Fix 1,510 L1 string patterns (AR/ES/ZH — bare strings, unusable) | Track 2 | Critical |
| V1 Hook slide with images — fully wired in generation | None | Done in code, needs quality test |
| BuildSimplePptx — decoupled PPTX from structured JSON | None (spec written) | Low — only if teachers ask |
| 5f Google review request (after 3rd generation) | Usage data needed | Low |
| Phase I-3: Output sampler, feedback classifier, bug triage | None | Medium |
| Phase I-4: Reddit/TEFL monitor | None | Low |
| Phase I-5: Content QA agent, database curator, SEO agent | Phase E | Later |
| Stripe live mode | Track 1 price ID fix + Phase E | Before charging real money |
| Railway Volume | Marcos (Track 1) | Before first paid user |

---

## Architecture Quick Reference

**Primary deliverable:** `.html` offline bundle (fonts + images inlined, works without internet)
**Secondary/opt-in:** `.pptx` — only built when teacher explicitly asks ("can I get a PowerPoint?")
**Email:** delivery email contains branded snapshot image + HTML "how to open" tip + download buttons for all files

**Generation flow:**
```
chat interview → Content Brief → approval
  → QueueGenerationJob
  → ImageSearch + DownloadImage (hook image)
  → InsertNewSlides
  → ModifySlide × N (one per slide, sequential)
  → ValidateSlideSet (retry failures up to 3x)
  → BuildOfflineBundle → [3 min pause] → worksheet → activity guide → flashcards → progress tracker
  → SnapSlideForEmail
  → MarkJobComplete → send_completion_email
```

**Key files:**
- `agent/instructions.md` — agent behavior + full task_brief formats
- `agent/slides_tools/html_writer_instructions.md` — HTML slide design rules + animation guidelines
- `agent/slides_tools/BuildOfflineBundle.py` — packages all slides into one .html file
- `agent/slides_tools/SnapSlideForEmail.py` — Playwright screenshot → branded 1080×1080 PNG
- `agent/email_sender.py` — delivery + daily digest emails
- `server.py` — FastAPI server + daily digest scheduler (07:00 daemon thread)
- `webui/src/components/ChatInterface.tsx` — chat UI with progress phases + download buttons
- `docs/HTML_FIRST_STRATEGY.md` — why HTML-first, what changed
- `docs/DECOUPLED_PPTX_SPEC.md` — future BuildSimplePptx spec
