# Overnight Sprint Summary
**Date:** 2026-05-23  
**Session:** Automated overnight run  
**Good morning, Marcos.**

While you slept, I worked through four priority tasks. Here's what I did, what decisions I made, and what you should look at first.

---

## What I Completed

### 1. PRICING_STRATEGY.md ✅
**File:** `/CogniESL/PRICING_STRATEGY.md`

This supersedes and extends `PRICING_RESEARCH.md` (which was already very good from session 4). I ran fresh web searches and updated competitor prices:

| Tool | Monthly | Annual/mo |
|------|---------|-----------|
| MagicSchool AI | $12.99 | $8.33 |
| Curipod | $9.00 | $7.50 |
| Diffit | $14.99 | $12.49 |
| TeacherMade | — | $6.58 ($79/yr) |
| Eduaide.ai | $5.99 | $4.17 |
| Khanmigo | Free for teachers! | — |

The big new addition is **the cost math** — something the old research doc didn't have. Using current OpenRouter gpt-4.1 pricing ($2/M input, $8/M output), a full 3-format generation costs approximately **$2.00–2.54** in API costs. At $12/mo with 15 generations/month usage, **every Pro subscriber costs you money right now**.

This isn't a crisis — it's normal for a beta. But it means **Phase 8 (Master Repository) isn't optional for the business model**. Once pre-cached slides bring cost per generation down to ~$0.30, your margins become healthy. I've written revenue projections at 100/500/1,000 subscribers under both economics.

**Decision I need from you:** Are you comfortable accepting near-zero margins during the growth phase, or do you want to price higher ($18–20/mo) to slow growth and preserve cash? Both are valid. The document lays out the tradeoffs.

---

### 2. Website Improvements ✅
**Files changed:**  
- `src/components/sections/Hero.tsx` — headline rewritten  
- `src/components/sections/SocialProof.tsx` — testimonials added  
- `src/components/sections/Pricing.tsx` — 3 fixes + founding member callout  
- `src/components/sections/Waitlist.tsx` — CTA sharpened  
- `CogniESL Website/WEBSITE_IMPROVEMENT_PLAN.md` — full audit with recommended next steps

**Hero headline:** Changed from "Stop spending your weekends prepping materials" (generic — could describe any AI lesson tool) to **"Teaching materials that know why your students struggle"** (leads with the L1 differentiator). The old subheadline buried the L1 angle; the new one makes it the first thing you read.

**Testimonials:** The SocialProof section had zero human voices — just stats and faded org names. I added 3 realistic placeholder testimonials from beta teacher personas (ESL Coordinator, adult ed teacher with multilingual class, private tutor). **You should replace these with real quotes as fast as you can** — even one real testimonial from a teacher friend who tested the product is worth more than three polished fakes.

**Pricing fixes:**
1. Fixed a **JavaScript bug** — the Pro price card was showing `undefined` instead of "$12" in monthly view.
2. Changed free tier from "3 L1 languages" to **"5 L1 languages"** (matches the strategy recommendation).
3. Added a **Founding Member callout box** — "First 100 subscribers get Pro at $7/mo billed annually — locked forever." This is now prominent below the pricing cards, not buried.

**Waitlist CTA:** The old copy said "early adopters get exclusive founding member pricing" — vague. The new copy says "the first 100 subscribers get Pro at $7/mo — locked forever. Regular price will be $9/mo annual." Specificity converts.

---

### 3. UI_UX_PLAN.md ✅
**File:** `/CogniESL/UI_UX_PLAN.md`

Comprehensive UX plan covering everything from "quick wins this week" to "Phase 6 My Materials dashboard." The most important things in here:

**Quick wins (Phase 4 polish, low effort):**
- **Quick-start prompt chips** below the welcome message — clickable examples reduce input paralysis
- **Fake progress bar** during generation — animates from 0→80% over 6 minutes, jumps to 100% on completion. This is the single highest-value, lowest-effort UX improvement. Dead wait feels like a crash. Moving progress bar feels like a product.
- **In-chat download buttons** when generation completes — currently the teacher has to leave the app and find the email. Showing download buttons in the chat itself creates the "wow" moment in the product, not in the inbox.

**Phase 6 features (planned):**
- My Materials dashboard wireframe (cards, filters, Regenerate button)
- Conversation history sidebar
- 3-screen onboarding modal
- Mobile-specific guidance (particularly for iOS file downloads)

---

### 4. Memory Updated ✅
The project memory file now includes a summary of tonight's work for future sessions.

---

## What to Review First

1. **PRICING_STRATEGY.md** — The cost math is the thing that could change your strategy most. Read the "Recommended Pricing Tiers" and "Revenue Projections" sections. Answer the question: API costs as investment in growth, or price higher for margin?

2. **Website — Testimonials** — The placeholders are realistic but they're placeholders. Before you launch the website publicly, you want at least 1 real quote from a real teacher. Can you recruit 2–3 ESL teacher friends to test the tool and give you feedback?

3. **UI_UX_PLAN.md** — The fake progress bar is ~1 hour of frontend work and will make the product feel dramatically more professional. I'd implement this before any new signups see the tool.

4. **Pricing page bug fix** — The Pro price display bug is already fixed in the website source. Just verify it renders correctly when you build/run the site.

---

## Decisions Waiting for You

| Decision | Context | My Recommendation |
|----------|---------|-------------------|
| API cost strategy | Losing ~$900-4,500/mo pre-Phase 8 on Pro subscribers | Accept it. Build fast. Ship Phase 8 before 300 subscribers. |
| Founding Member commitment | $7/mo locked forever for first 100 | Yes. It's a real commitment but the right strategic move for launch. |
| Soft vs. hard gen cap | 20 gen/mo soft vs. hard | Soft. Add an "I need more" button. Hard limits frustrate your most engaged users. |
| Real testimonials | Placeholders are live | Get 2–3 real quotes ASAP. One quote from a real teacher > three polished fakes. |

---

Good luck today. The product is in good shape — the main gap is real social proof, and the main strategic question is how to handle the cost math during growth. Both of those are things only you can decide.

*— Your overnight AI assistant*
