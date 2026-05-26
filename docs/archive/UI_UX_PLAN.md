# CogniESL UI/UX Plan
**Prepared:** 2026-05-23 (overnight sprint)  
**Scope:** Chat interface improvements, My Materials dashboard, onboarding, mobile, and wireframe descriptions  
**Based on:** Review of `webui/src/components/ChatInterface.tsx` and Phase 6/7 plans

---

## Overview: The Current State

The current app is a single-page chat interface (`ChatInterface.tsx`) sitting inside a full-screen Next.js shell. It works well for its purpose — collecting a generation request through conversation — but it has several meaningful gaps that limit both the user experience and the conversion funnel:

1. **No progress visibility during generation** — The teacher sends a request, sees "your materials are being prepared" after 15 seconds, and then... waits. There's no slide count, no phase indicator, nothing to show work is happening.
2. **No in-chat material preview** — When materials are done, the teacher gets an email link. They never see anything in the chat itself. The moment of "wow, this is what it can do" doesn't happen in the product.
3. **No conversation memory between sessions** — Each new window starts fresh. Teachers who return see the welcome message as if they've never used the tool.
4. **No quick-start prompts** — The welcome message gives examples in plain text, but there are no clickable starter buttons.
5. **No My Materials history** — After Phase 6 (auth), teachers should be able to log in and see all their past generations.

---

## Section 1: Chat Interface Improvements

### 1.1 Quick-Start Prompt Chips

**What:** Below the welcome message, display 3–4 tappable "starter" chips that pre-fill the input field.

**Design:** Small rounded chips in teal/coral/gold, horizontally scrollable on mobile.

**Suggested starters:**
- "📊 Slides for present simple (Spanish speakers)"
- "📝 Worksheet on articles (Korean teens)"
- "🎮 Activity guide for conditionals (Arabic adults)"
- "🔤 All formats: past simple (mixed class)"

**Why it matters:** Teachers who are new to the tool often freeze at an empty input. Pre-written examples lower the activation energy and demonstrate what a good request looks like. On the website demo, these examples convert skeptics — the same logic applies in the product.

**Implementation:** Add a `starterPrompts` array in `ChatInterface.tsx`. Render chips below the welcome message only when `messages.length === 1` (only the welcome message exists). On click, set the input value and optionally auto-submit.

---

### 1.2 Generation Progress Indicator

**What:** When generation starts (after the 15-second delay fires), replace the simple "preparing" message with a live progress component.

**Design:** A card in the chat stream with:
- A progress bar that fills across estimated time
- Phase labels that update: "🔍 Analyzing L1 patterns..." → "📖 Loading grammar database..." → "🎨 Writing slides (1 of 15)..." → "📝 Building worksheet..." → "✅ Done!"
- Estimated time remaining (rough: "About 6 minutes left")

**Why it matters:** The current dead-wait after "preparing" message feels like the tool crashed. A visible progress bar — even an approximate one — dramatically reduces the perceived wait time. Research: perceived wait time drops ~40% when progress is visible.

**Implementation options:**
- **Option A (Polling):** Add a `/api/job-status` endpoint to `server.py` that returns the current slide count and phase. Poll every 5 seconds from the frontend and update the progress card.
- **Option B (Fake progress):** Animate a progress bar that moves from 0→80% over 6 minutes, then jumps to 100% when the response arrives. Less accurate, zero backend work, still dramatically better than nothing.

**Recommendation:** Start with Option B for Phase 4 polish (no backend changes). Add Option A in Phase 6 when the jobs database is already being used for auth/history.

---

### 1.3 In-Chat Download Buttons

**What:** When the generation completes and the response includes file links, render them as styled download buttons — not as raw URLs embedded in text.

**Design:**
```
┌─────────────────────────────────────────────────────┐
│  ✅ Your materials are ready!                        │
│                                                     │
│  [📊 Download Slides (.pptx)]  [📝 Download Worksheet] │
│  [🎮 Download Activity Guide]                        │
│                                                     │
│  Also sent to your email: you@example.com            │
└─────────────────────────────────────────────────────┘
```

**Why it matters:** The current flow sends materials by email only. The teacher has to leave the app, find the email, and click there. Showing download buttons directly in the chat creates an "it's right here" moment that reinforces the product's quality and speed.

**Implementation:** Parse the assistant's final response for file URLs (they follow a consistent pattern from the email sender). Render matched URLs as `<a>` download buttons. Keep the email notification as backup, just add the in-chat buttons on top.

---

### 1.4 Conversation History in Sidebar (Phase 6)

**What:** After auth is added (Phase 6), the single-panel chat should expand to a two-panel layout:
- **Left sidebar (240px):** List of past conversations, newest first, labeled by grammar topic + date
- **Right panel (flex-1):** Current conversation

**Design — Sidebar item:**
```
┌──────────────────────────────┐
│ 📊 Present Simple            │
│ Spanish · B1 · 3 formats     │
│ May 21, 2026          →      │
└──────────────────────────────┘
```

**Mobile:** Sidebar hidden by default, accessible via hamburger menu or swipe-right gesture.

**Why it matters:** Teachers reuse materials. A teacher who created a great present-simple lesson in October wants to find it in January without digging through emails. Conversation history turns CogniESL from a one-shot generator into a materials library.

---

### 1.5 Typing Experience Improvements

**Current:** Single-line input, full message required before submit.

**Improvements:**
- **Multi-line input:** Change the input to a `<textarea>` that auto-expands up to 4 rows. Teachers often paste their own lesson description or student profile. Single-line truncates this.
- **Character count hint:** When the input exceeds 200 characters, show a faint "This looks good! You can send it." to reassure teachers they're not writing too much.
- **Send on Enter, Shift+Enter for newline:** Standard chat convention.

---

## Section 2: My Materials Dashboard

*This is a Phase 6 feature (after auth is live). Plan it now so Phase 6 can be built to spec.*

### 2.1 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  CogniESL  [Dashboard]  [New Material]  [Account]     👤 Marcos │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Your Materials                          [+ New Material]       │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  [Filter: All ▼]  [L1: Any ▼]  [Sort: Newest ▼]  [🔍 Search]  │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ 📊 Present Simple     │  │ 📊 Past Continuous    │            │
│  │ Spanish · B1         │  │ Korean · A2           │            │
│  │ Slides + Worksheet   │  │ All formats           │            │
│  │ May 21, 2026         │  │ May 19, 2026          │            │
│  │ [↓ Download] [Redo]  │  │ [↓ Download] [Redo]   │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ 📝 Articles          │  │ 🎮 Conditionals        │            │
│  │ Japanese · B2        │  │ Arabic · B1           │            │
│  │ Worksheet only       │  │ Activity guide only   │            │
│  │ May 18, 2026         │  │ May 15, 2026          │            │
│  │ [↓ Download] [Redo]  │  │ [↓ Download] [Redo]   │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                 │
│  [Load more...]                                                 │
│                                                                 │
│  Usage this month: 12/20 generations used  [████████░░░] 60%   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Material Card Details

Each card shows:
- Grammar topic (bold)
- L1 language + CEFR level + formats generated
- Generation date
- Download button (re-downloads from stored file)
- "Redo" button — re-opens the chat pre-filled with the same parameters (allows the teacher to regenerate with tweaks)

### 2.3 Filtering and Search

- **Filter by L1 language** — dropdown, multi-select
- **Filter by format** — Slides / Worksheet / Activity Guide / All
- **Sort by** — Newest, Oldest, Alphabetical (grammar topic)
- **Search** — Text search across grammar topic names

### 2.4 Usage Stats Panel (right sidebar or header)

For Pro users:
- Generations used this month: `12/20`
- Days until reset: `8 days`
- Favorite L1 language (inferred from history): "You generate the most Spanish content 🇪🇸"

For Free users:
- Generations used: `4/5`
- Upgrade CTA: "You have 1 free generation left. Upgrade to Pro for 20/month."

### 2.5 Empty State

When a teacher first logs in and has no materials:
```
┌─────────────────────────────────────────────────────┐
│           📚                                         │
│   Your materials will live here.                    │
│                                                     │
│   Start your first generation and it'll show        │
│   up here, ready to download anytime.               │
│                                                     │
│        [Create Your First Material →]               │
└─────────────────────────────────────────────────────┘
```

---

## Section 3: Onboarding Flow

*Triggered on first login after email verification (Phase 5/6).*

### 3.1 Onboarding Steps

The onboarding should be a 3-screen modal that runs once, then never again.

**Screen 1 — Welcome & Context**
```
┌──────────────────────────────────────────────────┐
│  👋 Welcome to CogniESL, [Name]!                  │
│                                                  │
│  You're about to generate your first set of      │
│  teaching materials. It takes about 5 minutes.   │
│                                                  │
│  Before you start, tell us a bit about yourself: │
│                                                  │
│  What do you mainly teach?                       │
│  ○ Adult ESL (community college / language school)│
│  ○ K-12 ESL (public school / private school)     │
│  ○ Private tutoring                              │
│  ○ University / EAP                              │
│                                                  │
│  [Continue →]                                    │
└──────────────────────────────────────────────────┘
```

**Screen 2 — Your Students**
```
┌──────────────────────────────────────────────────┐
│  What L1 languages do your students speak?        │
│  (Select all that apply — you can change this)    │
│                                                  │
│  [Spanish] [Mandarin] [French] [Arabic]          │
│  [Portuguese] [Korean] [Japanese] [Vietnamese]   │
│  [Russian] [Hindi] [Tagalog] [Other...]          │
│                                                  │
│  ← Back   [Continue →]                           │
└──────────────────────────────────────────────────┘
```

**Screen 3 — How it works (brief)**
```
┌──────────────────────────────────────────────────┐
│  Here's how CogniESL works:                       │
│                                                  │
│  1. Tell me what topic + who your students are   │
│  2. I'll generate materials (takes ~5–10 min)    │
│  3. Download your PPTX slides, worksheet,        │
│     and activity guide                           │
│                                                  │
│  Materials are sent to [email] too, so you       │
│  never lose them.                                │
│                                                  │
│  ← Back   [Start My First Generation →]          │
└──────────────────────────────────────────────────┘
```

### 3.2 What Onboarding Data Enables

The L1 languages selected in Screen 2 should be stored in the user profile and pre-populate suggestions in the chat. For example, if the teacher selected Spanish and Korean, the quick-start chips should default to Spanish and Korean examples.

The teaching context from Screen 1 (adult ESL vs. K-12) helps the orchestrator default to appropriate CEFR levels and activity types without the teacher having to specify each time.

### 3.3 Skipping Onboarding

Always provide a "Skip for now" link. Some teachers want to just dive in. Don't gate the experience on completing onboarding.

---

## Section 4: Mobile Considerations

### What Works on Mobile (Keep)
- The chat interface itself is fundamentally mobile-compatible (full-screen, bottom input)
- Waitlist email form on the website is simple and works on mobile
- The hero demo animation is a good mobile experience

### What Needs Mobile-Specific Attention

**Chat input:** A single-line input on mobile is fine, but the placeholder text "Describe what materials you need..." is too long for small screens. Shorten to "What materials do you need?" on mobile.

**Download buttons:** On mobile, file downloads trigger different behavior (iOS downloads to Files app; Android saves to Downloads). Add a note: "Materials will save to your Files app" for mobile users. Test on iOS Safari specifically.

**Generation wait:** On mobile, the risk is the teacher locking their phone screen while waiting. The "preparing" message should include: "Feel free to lock your phone — your materials will be in your email when ready." This prevents confused teachers who return to a blank screen.

**Sidebar (Phase 6):** On mobile, the My Materials sidebar must be a bottom sheet or a fullscreen modal, not an inline sidebar. A bottom drawer that slides up from 40% to fullscreen on swipe is the right pattern.

**Pricing page:** The 3-column pricing grid should collapse to a single column on mobile, with the Pro card first (most conversions happen on mobile browsing). Currently the grid may render as 3 tiny columns on small phones — verify and fix.

### Desktop-Only Features (for now)
- Side-by-side material preview (planned for Phase 7)
- The content brief review before generation (planned for Phase 5 enhancement)
- Admin dashboard (School tier, Phase 6+)

---

## Section 5: Wireframe Descriptions

*Detailed enough for a designer to build from.*

### Screen A: Chat Interface (Current State + Improvements)

```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 CogniESL                               [Generations: 4/5]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🤖 Hi! I'm CogniESL. Tell me what you need.             │   │
│  │                                                         │   │
│  │ [📊 Present Simple (Spanish)] [📝 Articles (Korean)]    │   │ ← Quick-start chips
│  │ [🎮 Conditionals (Arabic)] [✨ Try something custom]    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [User bubble, right-aligned, teal background]           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔍 Analyzing L1 patterns for Spanish speakers...        │   │
│  │ ████████████░░░░░░░░  Slide 8 of 15                     │   │ ← Progress card
│  │ Estimated: ~4 minutes left                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ✅ Ready! Present Simple for Spanish speakers (B1)       │   │
│  │                                                         │   │ ← Download buttons
│  │ [📊 Slides (.pptx)]  [📝 Worksheet]  [🎮 Activity Guide] │   │
│  │                                                         │   │
│  │ Also sent to you@email.com                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  [Input field — multi-line auto-expand]        [Send ▶]        │ ← Bottom input bar
└─────────────────────────────────────────────────────────────────┘
```

**Colors:** CogniESL teal (#0D7377) for user bubbles and send button, white/gray for assistant bubbles, progress bar in teal, download buttons in teal with coral/gold accent on hover.

---

### Screen B: My Materials Dashboard (Phase 6)

```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 CogniESL  [My Materials]  [New ✚]          👤 Marcos  [⚙️] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  My Materials (24 total)              [+ New Material]          │
│                                                                 │
│  [All Languages ▼]  [All Formats ▼]  [Newest ▼]  [🔍 Search]  │
│  ─────────────────────────────────────────────────────────     │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────┐ │
│  │ Present Simple     │  │ Past Continuous     │  │ Articles │ │
│  │ 🇪🇸 Spanish · B1   │  │ 🇰🇷 Korean · A2     │  │ 🇯🇵 Jpn  │ │
│  │ 📊📝🎮 All formats │  │ 📊📝 Slides+WS      │  │ B2 · 📝  │ │
│  │ May 21              │  │ May 19              │  │ May 18   │ │
│  │ [↓] [↺ Regenerate] │  │ [↓] [↺ Regenerate] │  │ [↓] [↺] │ │
│  └────────────────────┘  └────────────────────┘  └──────────┘ │
│                                                                 │
│  [Load more…]                                                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  📊 This month: 12 of 20 generations used  [██████░░░░] 60%    │
└─────────────────────────────────────────────────────────────────┘
```

**Card hover state:** Slight shadow lift, reveal "Regenerate" button. Clicking Regenerate opens the chat pre-filled with the same topic/L1/level parameters.

---

### Screen C: Onboarding Modal (Phase 5/6)

```
┌───────────────────────────────────────────────────────┐
│  Step 1 of 3   ●●○                          [Skip ×]  │
│                                                       │
│  What do you mainly teach?                            │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🏫  Adult ESL                                   │ │
│  │     Community college, language school, adult ed│ │
│  └─────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🏫  K-12 ESL                                    │ │
│  │     Public school, private school, middle/high  │ │
│  └─────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 👤  Private Tutoring                            │ │
│  │     1-on-1 or small group, independent          │ │
│  └─────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🎓  University / EAP                            │ │
│  │     Higher education, academic English          │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│                              [Continue →]             │
└───────────────────────────────────────────────────────┘
```

**Visual style:** Full-screen overlay with centered modal (600px max width), brand teal accent on selected option (left border highlight), pill-step indicator at top.

---

### Screen D: Mobile Chat (Specific Adjustments)

On screens < 640px:
- Remove sidebar entirely
- Input bar sticks to bottom of viewport with safe area insets
- Quick-start chips scroll horizontally (overflow-x: auto)
- Download buttons stack vertically (full-width)
- Usage counter moves from header to a small banner that appears only when at 80%+ usage
- "Materials are being prepared" message includes: "🔒 Safe to lock your phone — we'll email you"

---

## Implementation Priority

| Feature | Phase | Complexity | User Value |
|---------|-------|------------|------------|
| Quick-start chips | 4 polish | Low | High |
| Multi-line input | 4 polish | Low | Medium |
| Fake progress bar (Option B) | 4 polish | Low | Very High |
| In-chat download buttons | 4 polish | Medium | Very High |
| Real progress polling (Option A) | 6 | Medium | High |
| Conversation sidebar | 6 | High | High |
| My Materials dashboard | 6 | High | Very High |
| Onboarding modal | 6 | Medium | High |
| Mobile download guidance | 4 polish | Low | Medium |

---

*This plan should be reviewed alongside PHASE6_PLAN.md and PHASE7_PLAN.md before implementation begins.*
