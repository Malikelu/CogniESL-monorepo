# CogniESL Pricing Research & Strategy Brief
**Prepared:** 2026-05-22 (session 4, autonomous work while Marcos away)  
**Purpose:** Data for the pricing discussion Marcos flagged as needing deep thought

---

## 1. What Competitors Charge (Individual Teachers)

| Tool | Free Tier | Paid Monthly | Paid Annual | Notes |
|------|-----------|-------------|-------------|-------|
| **MagicSchool AI** | Yes, unlimited tools | $12.99/mo | $8.33/mo ($99.96/yr) | Market leader, K-12 general |
| **Diffit** | Yes, limited | $14.99/mo | $12.49/mo ($149.99/yr) | Differentiation-focused |
| **Curipod** | Yes, limited | $9/mo | $7.50/mo (~$90/yr) | Interactive lessons, K-12 |
| **Class Companion** | Yes (basic) | Free (institutional pricing only) | — | Writing feedback, ESL-applicable |
| **Nearpod** | Yes (Silver) | — | Gold $159/yr / Platinum $397/yr | Engagement platform |
| **ESL Brains** | Yes (some lessons) | $12/mo | ~$10.56/mo (12% annual discount) | ESL-specific content library |
| **Reactored** | — | €20–40/mo | — | Language AI tool, Europe-focused |
| **ESL Video Plus** | — | $7.99/mo | — | AI quizzes for ESL video |

**The clear market range: $7.50–$15/mo for individual paid tier.** Most tools anchor around $9–12/mo when billed annually.

---

## 2. Key Patterns Across EdTech SaaS

1. **Free tier is non-negotiable.** 92% of teachers discover tools through free access. No free tier = no organic growth. MagicSchool, Diffit, and Curipod all have meaningful free tiers.

2. **Annual billing is the default.** Every major player leads with annual pricing and offers ~15–20% off monthly. Monthly is "available" but framed as the expensive option.

3. **School/district is where the real money is.** Every tool above has "Contact Us" for institutional pricing — typically $8–30/teacher/month at scale. This is CogniESL's Phase 6+ story.

4. **Freemium converts ~2–5% of free users to paid** in education tools. This means the free tier must be genuinely useful (not crippled) or teachers don't trust the paid version.

5. **Price anchoring matters.** Diffit at $14.99/mo makes CogniESL at $12/mo look like a bargain. MagicSchool at $8.33/mo (annual) sets the lower anchor.

---

## 3. CogniESL's Pricing Constraints (the honest math)

Current API cost per generation run:
- **1 format (slides only):** ~$0.80–1.20
- **2 formats (slides + worksheet):** ~$1.50–2.00
- **3 formats (all):** ~$1.50–2.30

At **$12/mo** with a Pro user generating **10 lesson sets/month (slides only):**
- Revenue: $12
- API cost: ~$10–12
- **Margin: near zero.** This is not viable.

At **$12/mo** with usage limits or with the Master Repository (Phase 8):
- Most requests become cache hits → ~$0 API cost
- Margin becomes viable

**Conclusion: the $12/mo price is fine IF:**
1. Free tier has a hard generation cap (5/month is right — generous enough to try, limited enough to feel it)
2. Pro tier has a soft limit (e.g., 30 generations/month), OR
3. Phase 8 Master Repository brings cost-per-request down to ~$0.10–0.20 for common requests

**Alternative: price higher.** $18/mo monthly / $14/mo annual would give real margin even at current API costs for moderate usage. At that price point, CogniESL is still cheaper than Diffit and positioned as premium/specialist.

---

## 4. What Makes CogniESL Worth More Than MagicSchool

MagicSchool is a general K-12 tool that does 60+ things adequately. CogniESL does one thing for ESL teachers at a level no general tool can match:

- **Validated academic database** — 302 grammar files from peer-reviewed sources. MagicSchool hallucinates grammar rules. CogniESL doesn't.
- **L1 interference intelligence** — 36 languages with specific error patterns, academic citations, and teacher tips. No competitor has this.
- **Complete materials, not stubs** — A full 15-slide PPTX deck + worksheet + activity guide, usable immediately. MagicSchool generates outlines.
- **Built by a teacher** — Not a VC-backed tool with a corporate feel.

This justifies being at or slightly above MagicSchool's price point, not below it.

---

## 5. ESL-Specific Market Context

ESL teachers are a distinct segment with specific purchasing behavior:
- Many work independently (private tutors, freelancers) — price-sensitive
- Many work in institutions (community colleges, language schools) — less price-sensitive, but purchasing goes through admin
- US market: ~300,000 ESL teachers (K-12 + adult ed + higher ed)
- International market (EFL): massive, but purchasing power varies

ESL Brains ($6–12/mo, ESL content library) is the closest analog for pricing psychology: ESL teachers are already paying $6–12/mo for content libraries. CogniESL is a generator, not just a library — that's worth more.

**Sweet spot: $12–15/mo monthly, $9–12/mo annual.** This is above ESL Brains, below Diffit, roughly at MagicSchool. Justifiable given the depth of the product.

---

## 6. Beta / Founding Member Pricing Options

Three models used by successful EdTech SaaS launches:

### Option A: "Founding Member" Price Lock
- First 100 teachers get Pro at **$7/mo billed annually ($84/yr) — locked forever**
- Full disclosure: "Regular price will be $12/mo. You get it at $7/mo for life."
- Reward for taking a risk on an unproven product
- Creates evangelical users who have financial stake in recommending it

### Option B: Free Beta + Delayed Billing
- Beta testers get **full Pro access free for 3–6 months** (no credit card)
- After the beta period, they're asked to subscribe or lose access
- Conversion rate: 40–60% of engaged beta users pay (from industry benchmarks)
- Risk: some users milk the free period and never convert

### Option C: Discounted First Year
- Waitlist members get **50% off first year** ($6/mo annual instead of $12)
- Framed as "early access pricing — locks in before prices go up"
- Creates urgency without a hard deadline
- Year 2 they pay full price — some churn, but you've built a base

**Recommendation:** Option A (Founding Member price lock) is the strongest for CogniESL. It:
- Signals confidence in long-term pricing
- Creates the most loyal early users (they saved money, they're invested)
- First 100 is a concrete, honest scarcity signal
- Aligns with "built by a teacher" brand voice — not a corporation running a "50% off SALE!!!" promotion

---

## 7. Plan Structure Recommendations

### Free
- **5 generations/month** (any format combination)
- **5 L1 languages** (the most popular: Spanish, Mandarin, French, Arabic, Portuguese)
- Slides format only (no worksheet or activity guide)
- Watermarked PPTX ("Made with CogniESL" on footer)
- Email delivery only (no in-browser preview)

### Pro — $12/mo monthly / $9/mo annual
- **Unlimited generations** (subject to fair use / 30/month soft cap)
- **All 36 L1 languages**
- **All 3 formats** (slides + worksheet + activity guide)
- No watermark
- Priority email delivery
- Single-slide editing via chat
- Access to full materials library (Phase 6)

### School — Custom pricing
- Everything in Pro
- Multiple teacher accounts (5, 10, 25+)
- Admin dashboard
- Usage reporting
- Dedicated support
- Invoice billing (not credit card)

---

## 8. Open Questions for the Discussion

1. **What's the actual usage limit on Pro?** Unlimited sounds good for marketing, but $12/mo can't sustain a teacher generating 20+ full 3-format sets per month. A soft cap of 20–30 generations/month (or a hard cap on 3-format) protects you.

2. **Do we watermark the Free PPTX?** Watermarks drive conversions ("I need to remove this") but can feel cheap. A subtle footer credit ("Created with CogniESL.com") is less aggressive.

3. **Annual vs. monthly as default?** Almost every SaaS leads with the annual price in the UI (shows the lower number) and makes monthly available but clearly more expensive. Recommend following this convention.

4. **What counts as a "generation"?** Is a 3-format generation (slides + worksheet + activity) 1 generation or 3? If it's 1, the 5/month free limit is very tight for teachers who want all formats. Recommend: count by session (one request = one generation regardless of formats).

5. **Beta commitment:** Are you willing to promise Founding Members lifetime pricing at the lower rate? This is a real commitment. Once made, you can't raise their price without breaking trust.

6. **Resend cost:** Resend's free tier is 3,000 emails/month. At 100 Pro users generating 10 sets each = 1,000 emails/month — comfortably within free tier. Doesn't become a cost until you have 300+ active Pro users.

---

## 9. Suggested Starting Point for the Discussion

**Launch pricing (Founding Member offer, first 100 users):**
- Free: 5 generations/month, 5 L1s, slides only
- Pro Founding Member: $7/mo billed annually ($84/yr), locked forever
- Pro regular: $12/mo / $9/mo annual (shown on pricing page, not yet available)
- School: Contact us

**After first 100:**
- Drop Founding Member offer, move to regular pricing
- Add testimonials from the 100 beta users
- Raise Free limit if conversion data shows it's not needed to drive upgrades

This gives Marcos a real data point (what do 100 teachers think it's worth?) before committing to permanent pricing.
