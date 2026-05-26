# CogniESL Pricing Strategy
**Prepared:** 2026-05-23 (overnight sprint)  
**Builds on:** PRICING_RESEARCH.md (session 4, 2026-05-22)  
**Purpose:** Final, actionable pricing decisions with competitive data, cost math, and revenue projections

---

## 1. Updated Competitor Landscape (May 2026)

| Tool | Free Tier | Monthly | Annual (per mo) | Target | Differentiator |
|------|-----------|---------|-----------------|--------|----------------|
| **MagicSchool AI** | Yes — all tools, usage-limited | $12.99 | $8.33 ($99.96/yr) | K-12 general | 60+ tools, market leader |
| **Curipod** | Yes — 5 lessons | $9.00 | $7.50 (~$90/yr) | K-12, interactive | Interactive lessons, student engagement |
| **Diffit** | Yes — 60-day trial then limited | $14.99 | $12.49 ($149.99/yr) | Differentiation | Reading-level adaptation |
| **TeacherMade** | Yes — core features | $6.58/mo | $79/yr ($6.58) | Worksheets | PDF digitization, auto-grading |
| **Eduaide.ai** | Yes — 20 gen/month | $5.99 | $4.17 ($49.99/yr) | General lesson planning | Cheapest credible option |
| **Khanmigo** | Free for teachers | $4/mo | $3.67 ($44/yr) | Students/families | AI tutoring, not content creation |
| **Twee** | Yes — limited | $6.50 | $6.50 | Language teachers | ESL/EFL specific, vocab/grammar games |
| **ESL Brains** | Yes — some lessons | $12/mo | ~$10.56 | ESL content library | Human-curated ESL content |

**Key takeaway:** The market clusters around two groups:
- **Budget-general tools:** $5–8/mo (Eduaide, Twee, TeacherMade) — generic, high-volume
- **Premium-specialist tools:** $9–15/mo (MagicSchool, Diffit, ESL Brains) — domain-specific value

CogniESL belongs in the premium-specialist group. ESL Brains is the closest analog ($10–12/mo for ESL-specific content), but CogniESL is a generator — it creates custom materials, not just a library to browse.

---

## 2. CogniESL Cost Per Generation (Updated Math)

**API stack:** gpt-4.1 orchestrator + gpt-4.1 HTML writer via OpenRouter  
**OpenRouter gpt-4.1 pricing (May 2026):** $2.00/M input tokens · $8.00/M output tokens

### Token estimate per full 3-format generation:
| Component | Input tokens | Output tokens | Cost |
|-----------|-------------|---------------|------|
| Orchestrator (planning, database reads, coordination) | ~80k | ~20k | $0.16 + $0.16 = **$0.32** |
| HTML writer — 15 slides (avg 2k tokens/slide output) | ~120k | ~180k | $0.24 + $1.44 = **$1.68** |
| Worksheet generation | ~40k | ~30k | $0.08 + $0.24 = **$0.32** |
| Activity guide generation | ~30k | ~20k | $0.06 + $0.16 = **$0.22** |
| **Total — 3 formats** | ~270k | ~250k | **~$2.54** |
| **Total — slides only** | ~200k | ~200k | **~$2.00** |

> **Note:** These estimates assume worst-case (all 15 slides, full L1 oracle, complex grammar). Real-world average with caching and simpler requests likely 40–50% lower: **~$1.20–1.50 for slides only, ~$1.50–2.00 for all 3 formats.**

### What this means for margin at different price points:

| Monthly Price | Generations/mo (break-even) | Margin at 10 gen/mo | Margin at 20 gen/mo |
|--------------|---------------------------|---------------------|---------------------|
| $9/mo (annual) | ~4.5 (slides only) | **-$6** (unviable) | **-$21** (disaster) |
| $12/mo (monthly) | ~6 (slides only) | **-$8** (unviable) | **-$28** (disaster) |
| $18/mo | ~9 (slides only) | **+$3** (break-even) | **-$12** (still bad) |
| $24/mo | ~12 (slides only) | **+$9** (viable) | **-$6** (marginal) |

**Hard truth: At current API costs, no per-generation model is profitable without usage limits.**

### The three paths to profitability:

**Path A — Usage limits (now available)**  
Cap Free at 5 gen/month, Pro at 20–25 gen/month. At 15 gen/month average, $12/mo gives ~$0 margin — you're building market share, not making money yet. Viable for beta/launch phase only.

**Path B — Higher pricing ($18–24/mo)**  
$18/mo with a 15 gen/month soft cap gives $18 - (~$22.50 at $1.50/gen) = still negative. Requires Path C to work long-term.

**Path C — Phase 8 Master Repository (pre-cached slides)**  
When common grammar topics have pre-built slides (~$0 marginal cost), cost per generation drops to ~$0.20–0.40 for cache hits. This is the only path to real margins at consumer pricing. Phase 8 is the business-model unlock.

**Recommendation for launch:** Price for growth, not profit. $12/mo with a 20 gen/month soft cap. Accept near-zero margins for the first 200–300 subscribers while building toward Phase 8. This is standard SaaS CAC amortization — you're paying acquisition cost via API costs during beta.

---

## 3. Recommended Pricing Tiers

### Free
- **5 generations/month** (count by session, not format — one request with slides+worksheet = 1 generation)
- **5 L1 languages** (Spanish, Mandarin, French, Arabic, Portuguese — the top 5 most common in US ESL)
- Slides format only
- Subtle footer watermark: "Created with CogniESL.com"
- Email delivery only

*Why 5 languages not all 36:* The most common request pattern is Spanish speakers (60%+ of US ESL). Giving 5 languages is generous enough to demonstrate real value and let teachers discover the L1 intelligence, without giving away the differentiator entirely.

### Pro — $12/mo · $9/mo billed annually
- **20 generations/month** (soft cap — teachers who legitimately need more can contact us)
- **All 36 L1 languages**
- **All 3 formats** (slides + worksheet + activity guide)
- All proficiency levels (A1–C1)
- No watermark
- Priority email delivery (queue priority over free users)
- Access to My Materials library (Phase 6)

*Why $12/mo:* Positions CogniESL above generic tools (Eduaide $5.99, TeacherMade $6.58) and at parity with MagicSchool ($8.33 annual). Monthly $12 creates annual urgency — teachers see "$3/month savings" as meaningful.

*Why 20 gen/month cap vs "unlimited":* Unlimited is a liability at current API costs. 20 gen/month = one full lesson set per school day, which is more than any teacher realistically generates. "20 generations" sounds like abundance, not a restriction.

### Pro Founding Member — $7/mo billed annually ($84/yr, locked forever)
- Available to first 100 subscribers only
- Everything in Pro
- Lifetime lock — price never goes up for them
- Clear scarcity signal: "First 100 teachers. After that, regular pricing."

*Why $7 not $9:* At $7/mo annual ($84/yr), you're below ESL Brains and well below Diffit. The founding member price is a *thank you for taking a risk* signal, not just a discount. It should feel meaningfully below what later users pay.

### School — Contact Us
- Everything in Pro
- Multi-teacher accounts (starting at 5 teachers)
- Admin dashboard with usage reporting
- Invoice billing (purchase orders accepted)
- Dedicated onboarding call
- Priority support (24-hour response guarantee)
- Custom L1 language packs on request
- SSO integration (Phase 6+)

*Suggested school pricing (for reference in sales conversations):*
- 5 teachers: $50/mo ($10/teacher, 17% discount)
- 10 teachers: $90/mo ($9/teacher, 25% discount)
- 25+ teachers: Contact for quote (likely $6–7/teacher)

---

## 4. Freemium Strategy

### What to give away free (and why)
The goal of the free tier is **demonstrating the L1 intelligence**, not generating revenue. A teacher needs to experience the moment where they see "Oh — this is why my Spanish students say 'I am agree'" to understand why CogniESL is worth paying for. That moment doesn't happen without at least one real generation with L1 content.

**Give generously on L1 quality, restrict on quantity and scope:**
- Free tier should show ALL the L1 intelligence features on the 5 included languages
- The free slide deck should look identical in quality to Pro — no visual degradation
- The watermark is subtle (footer credit), not intrusive
- Worksheet and activity guide are Pro-only — this creates the upgrade trigger ("I want the worksheet too")

### The upgrade trigger hierarchy
Based on SaaS freemium conversion research, teachers upgrade when they hit a specific limit they care about:

1. **Format limit** (slides-only → want worksheet) — estimated 60% of upgrades
2. **Language limit** (5 L1s → need Korean, Japanese, etc.) — estimated 25% of upgrades  
3. **Generation limit** (5/month cap) — estimated 15% of upgrades

This means the worksheet/activity guide gate is the most important conversion driver. The language gate catches the rest. The generation cap is a safety net, not the primary conversion mechanism.

### What NOT to gate
- Quality of L1 intelligence (don't give worse L1 analysis to free users)
- Response time (acceptable slowdown fine, but don't make free feel broken)
- Grammar topic coverage (all 302 grammar files available to free users)
- Email delivery reliability

---

## 5. Revenue Projections

### Assumptions
- Monthly churn: 5% (industry benchmark for solo EdTech tools)
- Free → Pro conversion: 3% (conservative; industry EdTech average 2–5%)
- Average revenue per subscriber: $10.50/mo blended (mix of monthly $12 and annual $9)
- API cost per subscriber: ~$18/mo (assumes 15 gen/month at $1.20/gen average — generous estimate)

> **Important caveat:** Until Phase 8 (Master Repository), API costs likely exceed revenue per subscriber at high usage. The model below assumes Phase 8 is live within 12 months and costs drop to ~$0.30/gen for cache hits.

### Pre-Phase 8 (current API costs, ~$1.20–1.50/gen)
At 15 gen/month average: **~$19.50/mo API cost per Pro subscriber** — this means every Pro subscriber costs money at launch. This is intentional: you're investing in user acquisition and market validation, not building revenue.

### Post-Phase 8 (cached slides, ~$0.30/gen average)
At 15 gen/month average: **~$4.50/mo API cost per Pro subscriber** — healthy margins restored.

### Projection table (post-Phase 8 economics)

| Subscribers | MRR (blended $10.50) | API Costs ($4.50/sub) | Gross Profit | Gross Margin |
|-------------|---------------------|-----------------------|--------------|--------------|
| 100 | $1,050 | $450 | **$600** | **57%** |
| 500 | $5,250 | $2,250 | **$3,000** | **57%** |
| 1,000 | $10,500 | $4,500 | **$6,000** | **57%** |
| 2,500 | $26,250 | $11,250 | **$15,000** | **57%** |

Note: Does not include hosting (~$50–200/mo), Resend email (~free under 3k emails, then $20/mo), or Marcos's time. At 1,000 subscribers the business is generating ~$72k/year gross profit — viable for a solo founder.

### Pre-Phase 8 launch reality check

| Subscribers | MRR | API Costs (high) | Gross Profit | Notes |
|-------------|-----|-----------------|--------------|-------|
| 100 | $1,050 | $1,950 | **-$900** | Investing phase |
| 300 | $3,150 | $5,850 | **-$2,700** | Still investing |
| 500 | $5,250 | $9,750 | **-$4,500** | Phase 8 must arrive before here |

**This confirms:** Phase 8 (Master Repository) isn't just a nice-to-have feature — it's the financial viability switch. Target shipping Phase 8 before reaching 300 paid subscribers.

---

## 6. Why CogniESL's L1 Content Justifies a Premium

Generic tools (MagicSchool, Eduaide) compete on breadth — 60+ tools, anything a teacher might want. CogniESL competes on depth in one specific, high-value area. Here's how to articulate the premium:

### The specificity argument
MagicSchool generates: "Practice exercise for present simple."  
CogniESL generates: "Practice exercise for present simple, specifically targeting Spanish-speaker errors: third-person -s omission ('He walk'), false cognate confusion with 'estar', and 'ser vs. be' interference — with three wrong/correct example pairs from peer-reviewed research."

One of these saves 30 minutes. The other saves 2 hours *and* teaches you something about your students.

### The validation argument
Every grammar rule in CogniESL comes from a peer-reviewed source. MagicSchool, Curipod, and Eduaide are all LLM outputs — they hallucinate grammar rules and invent "common errors." CogniESL cannot invent a grammar rule because it doesn't generate grammar content from the LLM; it reads from validated YAML files.

For ESL teachers who are accountable to students' real language development, this is the difference between a tool they can trust and one they have to fact-check.

### The time math argument
At $12/mo, CogniESL costs $0.60 per generation (20/month).  
If a teacher spends 2 hours creating one good L1-aware lesson set manually, and their time is worth $25/hour, that's $50 of time per lesson set.  
CogniESL at $0.60 per generation = **99% cost reduction** on material prep time.  
Even at $24/mo, it's a clear ROI for any teacher with paying students.

---

## 7. Launch Pricing Recommendation

**Phase 1 (Waitlist → First 100 subscribers):**
- Free: 5 gen/month, 5 L1 languages, slides only
- **Founding Member Pro: $7/mo billed annually ($84/yr) — locked forever**
- Show regular pricing ($12/$9) crossed out to create anchor
- Hard cap at 100 founding members — then door closes

**Phase 2 (100–500 subscribers):**  
- Regular pricing live: $12/mo monthly, $9/mo annual
- Keep founding member badge visible on pricing page ("Founding Member slots are full — join at regular pricing")
- Add testimonials from founding members

**Phase 3 (500+ subscribers):**  
- Consider raising monthly to $14 or $15 (matches Diffit, still below)
- Annual stays at $9 or raises to $10
- School tier active with real pricing

---

## 8. Open Questions Marcos Should Decide

1. **The API cost problem:** Are you comfortable losing ~$900–4,500/month on API costs while building to Phase 8? Or do you want to price higher ($18–20/mo) and slow growth to preserve cash? Both are valid strategies.

2. **Founding Member commitment:** $7/mo locked forever is a real promise. 100 teachers at $84/year = $8,400/year that never inflates. Comfortable with that?

3. **Soft vs. hard gen cap:** A soft cap (20/month, contactable for more) is friendlier but requires monitoring. A hard cap is cleaner but risks annoying the most engaged teachers. Recommend: soft cap with an easy "I need more" button.

4. **Worksheet on free tier?** The current plan says no worksheet on free. Could test giving 1 worksheet/month on free to show teachers what they're missing. Higher conversion risk but also higher conversion payoff.

5. **Annual default:** Should the pricing toggle default to Annual (showing $9, more conversions) or Monthly (showing $12, more honest)? Most SaaS defaults to Annual. Test both.

---

*This document supersedes the relevant sections of PRICING_RESEARCH.md. PRICING_RESEARCH.md remains for reference on the beta/founding member strategy detail.*
