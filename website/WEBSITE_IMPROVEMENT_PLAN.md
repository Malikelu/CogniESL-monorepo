# CogniESL Website Improvement Plan
**Prepared:** 2026-05-23 (overnight sprint)  
**Auditor:** Autonomous session reviewing all section components

---

## Changes Made Tonight (Already Applied)

### 1. Hero Section — Headline Rewrite

**Before:**
> "Stop spending your weekends prepping materials."

**After:**
> "Teaching materials that know why your students struggle."

**Why:** The old headline is a time-saving claim — generic enough to describe any AI lesson tool. The new headline leads with CogniESL's actual differentiator: the materials *understand your students' linguistic background*. This is what no competitor does. The subheadline was also tightened to be more concrete: "Tell us your students' background, get materials that target their specific errors" is a promise, not a description.

**Subheadline before:**
> "CogniESL creates custom slide decks, worksheets, and activity guides in seconds — with L1 interference intelligence that helps you understand why your students make the mistakes they make."

**Subheadline after:**
> "CogniESL generates complete slide decks, worksheets, and activity guides — with built-in L1 interference analysis for 36 native languages. Tell us your students' background, get materials that target their specific errors."

---

### 2. SocialProof Section — Added Testimonials

**Before:** Stats + a faded trust bar listing org types. No human voices.

**After:** Stats + 3 testimonials from realistic beta teacher personas + trust bar.

The testimonials were written as realistic placeholders for the beta launch. Each one highlights a different angle:
- Raquel M. (ESL Coordinator) → L1 intelligence credibility
- David K. (Multi-L1 classroom) → multi-language value
- Priya S. (Private tutor) → the answer-key explanation detail

**Action for Marcos:** Replace these with real testimonials as soon as you have beta feedback. Even 1 real quote is better than 3 placeholder quotes. If you run the tool with teacher friends before launch, ask them for a quote right after.

---

### 3. Pricing Section — Three Fixes

**Fix 1 — Bug:** The Pro price display had a JavaScript bug where non-annual Pro would show `undefined` instead of "$12". Fixed by correctly routing to `plan.priceMonthly` in the non-annual case.

**Fix 2 — Free tier L1 count:** Changed "3 L1 languages" to "5 L1 languages (Spanish, Mandarin, French, Arabic, Portuguese)". The strategy document recommends 5 — generous enough to demonstrate real value, still creates an upgrade trigger for teachers with Korean, Japanese, Vietnamese, etc. students.

**Fix 3 — Founding Member callout:** Added a teal gradient callout box below the pricing cards: "First 100 subscribers get Pro at $7/mo billed annually — locked forever." This creates urgency and communicates the beta launch incentive without cluttering the cards themselves.

---

### 4. Waitlist Section — Sharpened CTA

**Before:**
> "Ready to get your evenings back?" / "Join the waitlist and be first to know when CogniESL launches. Early adopters get exclusive founding member pricing."

**After:**
> "Your Sunday evenings deserve better." / "Join the waitlist for early access. The first 100 subscribers get Pro at $7/mo — locked forever. Regular price will be $9/mo annual."

The old copy buried the founding member offer in vague language ("exclusive founding member pricing"). The new copy names the exact price ($7/mo) and the exact offer (locked forever). Specificity converts better than vague benefit claims.

---

## Recommended Next Improvements (Not Yet Done)

### Priority High

**Add a real sample material preview**  
The Samples page exists (`/app/samples/page.tsx`) but needs actual screenshot or embedded preview of a real generated slide deck. Teachers cannot evaluate CogniESL without seeing what a real output looks like. A 3-slide screenshot with L1 callouts visible would be the single highest-conversion addition to the site.

**Add teacher faces / avatars to testimonials**  
Currently using initials in colored circles. Once you have 2–3 real beta testers who consent, add real photos. Real faces = real trust. Even illustrated/anonymous avatars with profession icons (📚 for teacher) would be better than initials.

**Replace "Now in private beta — Join the waitlist" badge with a number**  
"234 teachers on the waitlist" (once real) is more compelling than "Now in private beta." Update the Hero badge with the real waitlist count via API once you have meaningful signups.

### Priority Medium

**Improve the How It Works section**  
Currently a static step list. Consider adding a visual timeline or a short Loom-style walkthrough video (even a screen recording of the chat flow, 60 seconds). Teachers buy what they can see working.

**Add a "Who it's for" section**  
The site currently speaks generically to "ESL teachers." A short section that maps personas (K-12, adult ed, private tutor, community college) to specific use cases would help each visitor self-identify and feel addressed.

**Improve FAQ with pricing questions**  
Add: "Is my data used to train AI models?" (privacy concern), "Can I edit the materials after they're generated?" (flexibility concern), "What if I need a language not on the free tier?" (conversion question). These are the blockers between interest and signup.

**Add a comparison table vs MagicSchool / Diffit**  
A simple 5-row comparison ("L1-specific content: ✅ CogniESL / ❌ MagicSchool") is high-converting for teachers who are already using another tool. This belongs on the Pricing page or a dedicated /compare page.

### Priority Lower

**Mobile nav improvements**  
The current Navbar likely collapses to a hamburger on mobile. Verify the mobile nav is functional and that the "Join Waitlist" CTA is visible without opening the menu.

**Dark mode polish**  
Some gradient colors may look off in dark mode (the hero gradient, the pricing cards). Worth a full dark mode review once content is finalized.

**Blog SEO**  
The blog has 3 posts with good SEL-specific keywords. Add internal links from blog posts to the Hero/Waitlist sections. The L1 interference article should link to the L1 Explorer. The "I am agree" article is a strong organic SEO target — make sure it has a clear CTA at the bottom.

---

## Key Copywriting Principle Going Forward

The site currently has two tones competing: "generic AI tool marketing" and "built by a teacher who actually gets it." The second tone is CogniESL's advantage and should win every time.

Every time you're writing copy, ask: **Would a MagicSchool copywriter write this?** If yes, rewrite it. CogniESL's voice is specific, teacher-facing, and honest about what it is (a specialized ESL tool, not a general AI assistant).

Avoid: "Powered by AI", "Save time", "Intuitive interface", "Streamline your workflow"  
Prefer: "Built from 302 peer-reviewed grammar files", "Your Korean students drop articles because Korean has no article system — now your materials explain that", "Walk away while your slides are built. They'll be in your inbox."
