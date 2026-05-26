# CogniESL: The Self-Running App
**Vision:** CogniESL as an AI-run organization — every department staffed by agents, the product improving itself 24/7, and you as the CEO steering the ship.
**Last updated:** 2026-05-24
**Status:** Brainstorm → Design document

---

## Table of Contents

1. [The Big Picture](#1-the-big-picture)
2. [Feedback Loops — The Nervous System](#2-feedback-loops--the-nervous-system)
3. [The Self-Healing Pipeline](#3-the-self-healing-pipeline)
4. [AI Agents as Departments](#4-ai-agents-as-departments)
5. [Social Sharing & Growth Engine](#5-social-sharing--growth-engine)
6. [The Intelligent Dashboard](#6-the-intelligent-dashboard)
7. [Email Intelligence Layer](#7-email-intelligence-layer)
8. [Self-Improving Content Database](#8-self-improving-content-database)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Risks, Limits & Honest Tradeoffs](#10-risks-limits--honest-tradeoffs)

---

## 1. The Big Picture

### The Vision

You don't just want a product that teachers use. You want a product that **runs itself**:

- Teachers report issues → AI classifies, routes, and resolves them overnight
- Marketing writes itself → AI drafts posts, monitors social media, suggests campaigns
- Quality controls itself → AI samples outputs, detects degradation, triggers regeneration
- Business metrics watch themselves → AI flags anomalies, predicts churn, optimizes pricing
- Bugs fix themselves → AI reads audit logs, identifies root causes, proposes code fixes
- Content improves itself → AI identifies enrichment opportunities in the YAML database
- Emails organize themselves → AI reads, classifies, prioritizes, and drafts responses

You wake up. The AI team has been working all night. A digest tells you what happened, what needs your decision, and what was already handled. You approve, adjust, or override. Then you go teach.

### What Already Exists (Foundation)

You're not starting from scratch. The infrastructure for self-improvement is surprisingly close:

| Component | Status | Role in Self-Running System |
|---|---|---|
| Agency Swarm agent framework | ✅ Built | Foundation for all AI agents |
| Audit logger (`audit_logger.py`) | ✅ Built | Eyes and ears — logs every tool call |
| Job tracking (`jobs.py`) | ✅ Built | Tracks successes and failures |
| Admin dashboard API (`/api/admin/overview`) | ✅ Built | Business metrics — fuel for AI decisions |
| SQLite databases (auth, materials, generations) | ✅ Built | Structured data agents can query |
| Email delivery (Resend) | ✅ Built | Outbound communication channel |
| Stripe integration | ✅ Built | Revenue data, subscription state |
| Claude / LiteLLM integration | ✅ Built | Brain for all agents |
| FastAPI server | ✅ Built | API layer for agent endpoints |

**What doesn't exist yet:** The feedback collection layer, the classification agents, the social sharing engine, the automated review system, and the "AI department" orchestration. This document designs all of it.

### Core Architecture Principle

Every self-improving system needs three components:

```
INPUT → PROCESSING → OUTPUT
  ↓                      ↑
  └──── FEEDBACK ────────┘
```

1. **Input:** How information enters the system (teacher reports, usage data, social signals, emails)
2. **Processing:** How AI agents analyze, classify, decide, and act
3. **Output:** What changes (bug fix deployed, review requested, post published, content updated)
4. **Feedback:** How the system measures whether the output worked

The goal is to close every loop — outputs generate new inputs, and the system gets better every cycle.

---

## 2. Feedback Loops — The Nervous System

### 2.1 The Problem with Feedback

Teachers are busy. Reporting bugs through a form, sending an email, or filing a ticket takes effort they won't spend. **If reporting is frictionless, you get feedback. If it's hard, you fly blind.**

The key insight: **feedback should be captured in the flow of the existing experience**, not as a separate action the teacher has to think about.

### 2.2 Explicit Feedback Channels

#### A. Material-Level Micro-Feedback (Highest Priority)

**What:** After a teacher downloads or views generated materials, show a tiny, non-intrusive feedback widget.

**Where:** In the materials library panel (the "My Materials" UI), on each material card.

**Design:**
```
┌─────────────────────────────────────────┐
│  📊 Present Simple — Spanish Adults B1  │
│  Generated May 24 · 15 slides           │
│                                         │
│  [📥 Slides] [📥 Worksheet] [📥 Guide]  │
│                                         │
│  How were these materials?              │
│  [😍 Perfect] [👍 Good] [👎 Issues]    │
└─────────────────────────────────────────┘
```

**If "Issues" is tapped, expand inline (no navigation):**
```
  What went wrong?
  [Wrong level] [L1 errors] [Missing content]
  [Not what I asked for] [Formatting] [Other: ___]
```

**Why this works:**
- One tap, no navigation
- Takes < 5 seconds
- Teachers are most opinionated right after seeing the material
- You already have the material ID and context — no need for the teacher to explain what they're reporting about

**Database:** New `feedback` table:
```sql
CREATE TABLE feedback (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    material_id TEXT NOT NULL,
    rating TEXT NOT NULL,          -- 'perfect' | 'good' | 'issues'
    tags TEXT DEFAULT '',          -- comma-separated: 'wrong_level,l1_errors'
    comment TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    reviewed INTEGER DEFAULT 0,    -- has an agent/human reviewed this?
    resolution TEXT DEFAULT ''     -- what was done about it
);
```

**API endpoint:** `POST /api/feedback` — no auth friction, just material_id + rating.

#### B. Chat-Embedded Frustration Detection

**What:** The agent should detect frustration, confusion, or rejection in the teacher's chat messages and **implicitly** log it as feedback without asking.

**How:** Add a lightweight classification step after each teacher message. Not a separate AI call — just a system prompt instruction to the existing agent:

> "If the teacher's message expresses dissatisfaction, frustration, or rejection of generated output (e.g., 'this is wrong', 'that's not what I meant', 'the level is too easy', 'you missed the L1'), log it as implicit feedback by calling the `log_feedback` tool. Include the specific issue they mentioned."

**Why this works:** Teachers already complain in chat. You're just capturing what's free. The teacher doesn't have to do anything extra.

**Edge case:**
- A teacher saying "can you make this harder?" is not frustration — it's a feature request
- A teacher saying "this is completely wrong" is frustration — log it
- The distinction matters for classification (see §3)

#### C. Post-Generation Satisfaction Check (Delayed)

**What:** 24 hours after material delivery, send a brief email:

```
Subject: How were your Present Simple materials?

Hi [Name],

Yesterday you generated materials for Present Simple (Spanish Adults, B1).
How did they work in class?

[😍 Loved them] [👍 Decent] [👎 Had issues]

One click. Helps us improve.
— CogniESL
```

**Pros:** Captures classroom-quality feedback (the real test), catches issues that only appear when teaching.
**Cons:** Email open rates are ~30%, click rates lower. Works best for active users only.
**Verdict:** Implement, but don't rely on it as the primary channel. See §2.2A as the main channel.

#### D. Grammar/L1-Specific Bug Reporting

**This is the hardest feedback type** and the most valuable. A teacher saying "the L1 interference pattern for Portuguese is wrong" requires domain expertise to triage.

**Design:** Add a "Report content error" link specifically on L1-generated content (the Oracle slides in the PPTX). This could be:
- A QR code on the last slide of generated PPTX files linking to a pre-filled feedback form
- An inline button on the material detail page: "Report a content error"

When a content bug is reported:
1. Auto-identify which YAML file is implicated (grammar + L1 + grammar_point)
2. Cross-reference against the actual file
3. Route to the Content QA Agent (see §4)

**Critical rule:** Content errors should NEVER be auto-fixed. They require your review because they affect pedagogical correctness. The agent's job is to identify, flag, and propose — you approve.

### 2.3 Implicit Behavioral Feedback (No Teacher Action Needed)

Teachers don't just tell you about problems — their behavior reveals them.

**Signals to track:**

| Signal | What it means | How to detect |
|---|---|---|
| Downloads the material but never returns | Tried it, didn't like it | Material downloaded, no subsequent generation within 14 days |
| Regenerates same grammar point quickly | Wasn't satisfied with first result | Same grammar + L1 + level, second generation within 48 hours |
| Downgrades subscription | Not seeing value | Stripe webhook: `customer.subscription.updated` (pro → free) |
| Stops generating after N uses | Churned | No generation activity for 30+ days after initial use |
| Generates same type repeatedly | Core use case, high value | Clustering analysis on generation patterns |
| Opens email but doesn't generate | Interested but not activated | Resend webhook: email opened, no API call within 24h |

**Implementation:** A new `events` table logging all user actions with timestamps. The dashboard already tracks generations; this extends it to a full event stream.

```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,   -- 'generation_started', 'generation_completed',
                                -- 'material_downloaded', 'feedback_submitted',
                                -- 'email_opened', 'login', 'signup'
    metadata TEXT DEFAULT '{}', -- JSON blob with event-specific data
    created_at TEXT NOT NULL
);
```

### 2.4 Feedback from the Wider Ecosystem

**Google Reviews / App Store reviews:** Monitor and respond automatically (with approval).

**Social mentions:** Track when CogniESL is mentioned on X, Instagram, Reddit, Facebook groups (ESL teacher communities).

**Email replies:** When teachers reply to the completion email, classify the sentiment and content (see §7).

**Website analytics (already have Plausible):** Track where teachers drop off (signup → first generation funnel).

---

## 3. The Self-Healing Pipeline

### 3.1 The Full Pipeline

This is the core feedback-to-resolution engine:

```
                    ┌──────────────┐
                    │   FEEDBACK   │
                    │  (all types) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  CLASSIFIER   │
                    │    AGENT      │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────────┐
            │              │                  │
     ┌──────▼──────┐ ┌────▼─────┐    ┌──────▼──────┐
     │  BUG        │ │ QUALITY  │    │ SUGGESTION  │
     │  (content/  │ │ ISSUE    │    │ / PRAISE    │
     │   code)     │ │          │    │             │
     └──────┬──────┘ └────┬─────┘    └──────┬──────┘
            │              │                  │
     ┌──────▼──────┐ ┌────▼─────┐    ┌──────▼──────┐
     │   TRIAGE    │ │ MATERIAL │    │   ROUTE     │
     │   AGENT     │ │ QA AGENT │    │   AGENT     │
     └──────┬──────┘ └────┬─────┘    └──────┬──────┘
            │              │                  │
     ┌──────▼──────┐ ┌────▼─────┐    ┌──────▼──────┐
     │ AUTO-FIX?   │ │ FLAG FOR │    │ REVIEW?     │
     │ (code only) │ │ CONTENT  │    │ TESTIMONIAL?│
     │             │ │ REVIEW   │    │ BACKLOG?    │
     └──────┬──────┘ └──────────┘    └─────────────┘
            │
     ┌──────▼──────┐
     │ CREATE FIX  │
     │ TEST        │
     │ DEPLOY      │
     └─────────────┘
```

### 3.2 The Classification Agent

This is the front door of the entire self-healing system. Every piece of feedback goes here first.

**Input:** Any text from any feedback channel + context (which material, which user, what grammar point)

**Output:** A structured classification:

```json
{
  "type": "content_bug",
  "severity": "high",
  "category": "l1_interference",
  "file": "data/l1-interference/portuguese_interference.yaml",
  "grammar_point": "present_simple",
  "language": "portuguese",
  "summary": "Teacher reports that the L1 interference pattern for Portuguese speakers and Present Simple is incorrect — the 'yo' form doesn't map the way it's described",
  "teacher_text": "The Spanish comparison is wrong. In Portuguese it's different...",
  "auto_fixable": false,
  "requires_human": true
}
```

**Taxonomies for classification:**

**Type:**
- `content_bug` — Wrong information in grammar/L1/activity databases
- `code_bug` — Generation pipeline error (empty slides, formatting, crashes)
- `ux_issue` — Confusing interface, chat flow problem
- `feature_request` — Teacher wants something new
- `testimonial` — Positive feedback, potential marketing material
- `question` — Teacher doesn't understand how to use something

**Severity:**
- `critical` — Content error that misleads students; crash affecting many users
- `high` — Bug that wastes teacher time; repeated occurrences
- `medium` — Minor issue, workable
- `low` — Cosmetic, nice-to-have

**Implementation:** This agent runs as a lightweight background job (Claude Haiku is cheap and fast for classification). Classify each new feedback item within 5 minutes of submission.

### 3.3 Routing Rules

| Type | Severity | Action |
|---|---|---|
| Code bug | Critical | Immediate alert to Marcos + auto-create GitHub issue + QA agent investigates |
| Code bug | High/Med | Queue for next development cycle, agent proposes fix |
| Content bug | Any | Always requires human review. Agent proposes fix to YAML, Marcos approves |
| UX issue | High | Agent analyzes session logs, proposes redesign |
| Feature request | Any | Add to backlog with vote count (if multiple teachers request same thing, priority increases) |
| Testimonial | Positive sentiment > threshold | Trigger review request (see §5) |
| Testimonial | Strong positive | Agent drafts testimonial request email |

### 3.4 The Auto-Fix Pipeline (Code Only)

For code bugs only — NEVER for content:

1. QA Agent reads the audit logs + error trace
2. Identifies the failing tool/function
3. Proposes a code fix
4. Runs existing tests
5. If tests pass, creates a deployment-ready change
6. Sends Marcos a summary: "Fixed issue in ModifySlide tool (edge case where HTML contains emoji). Tested with 3 test cases. Ready to deploy."
7. Marcos approves (or auto-approve if you configure it)

**Implementation:** Essentially Claude Code running on your repo, triggered by the pipeline. You already have Claude Code as your development tool — the difference is that the trigger comes from real teacher reports instead of your manual instructions.

**Risk:** Auto-fix can break things. **Mitigation:** Always require Marcos approval for production deploys. Let the agent propose, prepare, and test — but you press the button.

---

## 4. AI Agents as Departments

### 4.0 The Missing Piece: Orchestrator Layer

**The original design had 6 independent agents reporting to Marcos. This was the biggest gap.** Independent agents with no coordination means Marcos becomes the integrator — reading 6 separate reports and figuring out how they relate. That defeats the purpose of a self-running system.

**The fix: An Orchestrator layer** that sits between Marcos and the department agents:

```
Marcos (CEO)
  └── Orchestrator (runs on schedule, synthesizes everything)
        ├── Monitor Agent — quality self-monitoring, anomaly detection
        ├── Curator Agent — master repo management
        ├── Growth Agent — marketing, social, churn prevention
        └── Intel Agent — business intelligence, costs, funnel
```

**What the Orchestrator does:**
1. **COLLECT:** Runs each department agent on schedule
2. **CORRELATE:** Cross-references findings across agents (see §4.3)
3. **SYNTHESIZE:** Produces ONE consolidated daily digest (not 6 separate ones)
4. **PROPOSE:** Writes agent_actions to the database for Marcos' approval
5. **ALERT:** Sends immediate notification for critical issues (see §4.4)

**Why 4 agents instead of 6:**
- **Secretary (email classification)** and **Support (teacher questions)** are deferred. They're only useful when you have meaningful email volume and an active user base. Building them now means maintaining code that processes zero messages.
- **Content QA** is folded into the Curator Agent (content-related quality issues are Curator's domain)
- **QA (code bugs)** and **Quality monitoring** are folded into one Monitor Agent

### 4.1 Organizational Chart

```
                        ┌──────────┐
                        │  MARCOS  │
                        │  (CEO)   │
                        └────┬─────┘
                             │
                    ┌────────▼────────┐
                    │   ORCHESTRATOR  │
                    │  (synthesizer)  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   ┌──────▼──────┐   ┌──────▼──────┐   ┌───────▼───────┐
  ┌▼───────────┐ │  ┌▼───────────┐ │  ┌▼─────────────┐ │
  │  MONITOR   │ │  │  CURATOR   │ │  │   GROWTH     │ │
  │  (Quality) │ │  │  (Content) │ │  │  (Marketing) │ │
  └────────────┘ │  └────────────┘ │  └──────────────┘ │
                  │                  │                   │
                  │          ┌───────▼──────┐            │
                  │          │    INTEL     │            │
                  │          │  (Business)  │            │
                  │          └──────────────┘            │
                  └──────────────────────────────────────┘
```

Note: Apex (Marcos' general Hermes assistant) is NOT in this chart. Apex is Marcos' right hand for everything — CogniESL, personal, other businesses. Apex checks the orchestrator's status when Marcos asks, but doesn't run CogniESL agent loops. This keeps Apex's context clean.

### 4.2 Agent Specifications

#### Monitor Agent ("Quality")

**Mission:** Automated quality self-monitoring. Catches degradation before teachers do.

**Inputs:**
- `failed_jobs` from the job tracking system
- `audit.json` logs
- Sampled generation outputs (1 in 10)
- Anomaly detection metrics (7-day rolling averages)

**Actions:**
- **Output sampler:** Randomly checks 1 in 10 generations against quality checklist (slide count, L1 Oracle present, CCQs present, file sizes)
- **Error tracker:** Correlates failures ("3 generations failed on emoji encoding today")
- **Anomaly detector:** Compares current metrics to 7-day average, flags deviations > 50%
- **Quality drift alert:** "Present Perfect output quality dropped 15% this week"

**Output format:**
```
MONITOR REPORT — May 26, 2026 (2:00 PM run)

Quality Score: 94% (down from 97% last week)
Sampled Outputs: 3/3 passed checklist

Anomalies Detected: 1
- Error spike at 10:42 AM (3 failures in 15 min) → emoji encoding issue
  Fix proposed → routed to agent_actions for Marcos' approval

System Health: 96.2% success rate (4-hour rolling)
Model: Claude Haiku for monitoring, Claude Sonnet for fix proposals
Schedule: Every 4 hours
```

#### Curator Agent ("Content")

**Mission:** Manage the Master Repository — pre-generate, prune, regenerate, and keep content fresh.

**Inputs:**
- Master Repository cache status
- Generation demand data (from generations table)
- Feedback data (prioritize combinations with poor feedback)
- Forge update notifications (new content available for sync)

**Actions:**
- Pre-generate high-demand uncached combinations
- Prune unused combinations (12+ months without requests)
- Flag decks for regeneration when YAML content is updated
- Identify gap: content combinations that don't exist yet but are likely to be requested

**Output format:**
```
CURATOR REPORT — Night of May 26

New master decks generated: 3
- present_perfect__korean__adult__b1 (3 teacher requests this week)
- past_continuous__spanish__teen__a2 (2 requests + gap analysis)
- articles__portuguese__adult__a2 (forge content update)

Flagged for regeneration: 5 decks
- All affected by Portuguese L1 file sync (content enrichment)

Pruned: 2 decks (0 requests in 6+ months)

Repository coverage: 76% of historical requests now served from cache (up from 74%)

New gaps identified: "conditionals__arabic__teen__b1" — not in COMMON_COMBINATIONS but 2 requests this month

Schedule: Nightly
```

#### Growth Agent ("Marketing")

**Mission:** Turn happy teachers into marketers and keep churning users engaged.

**Inputs:**
- Dashboard metrics (signups, generations, conversion rates)
- Testimonials from feedback system
- Churn risk scores (from Intel Agent)
- Email engagement data (open/click rates)
- Social share events

**Actions:**
- Identify superfans (top generation users with positive feedback) → draft testimonial requests
- Identify churn-risk users → draft re-engagement emails
- Draft social media posts (queued for Marcos approval)
- Trigger Google review requests (after 3rd generation, no frustration, 7+ days)
- Track referral link usage
- Generate weekly growth report

**Output format:**
```
GROWTH REPORT — May 26

SIGNUPS & CONVERSION:
- 2 new signups today (1 from referral, 1 from homepage)
- Free→Pro conversion: 3.2% (up from 2.8%)

CHURN PREVENTION:
- 3 Pro users at risk (14+ days inactive)
- Re-engagement emails drafted [pending Marcos approval]

SUPERFANS:
- user_abc (32 generations, 5 positive feedback) → testimonial request drafted
- user_xyz (28 generations, Google review solicitation ready)

SOCIAL QUEUE:
- 3 posts drafted for X, 2 for Instagram [pending Marcos approval]
- 1 testimonial queued for Google review request

Schedule: Daily
Model: Claude Sonnet (creative writing quality matters)
```

#### Intel Agent ("Business")

**Mission:** Business intelligence, cost monitoring, and prescriptive suggestions.

**Inputs:**
- Stripe data (revenue, subscriptions, churn events)
- Generation costs (API spend per agent, per generation)
- Funnel metrics (signup → activation → engagement → power → paid)
- Agent performance data (from Monitor Agent)

**Actions:**
- Daily cost tracking (API spend vs. revenue, broken down by agent)
- Funnel analysis (where do users drop off?)
- Agent efficiency reporting (cost per agent vs. value delivered)
- Prescriptive suggestions (rule-based for now)
- Budget alerts (projected monthly overspend)

**Output format:**
```
INTEL REPORT — May 26

TODAY:
- API cost: $4.20 (14 generations × ~$0.30 avg)
- Revenue: $0 (no new subscriptions)
- MRR: $84.00 (7 Pro + 4 Founding)

THIS MONTH:
- Total API cost: $62.40
- Revenue: $84.00
- Gross margin: +$21.60 ✅

AGENT COSTS:
- Monitor: $0.40/day (Haiku, 4 runs)
- Curator: $2.10/night (generation costs)
- Growth: $0.15/day (Haiku, analysis only)
- Intel: $0.10/day (Haiku, analysis only)
- Total agent cost: ~$8.50/month

FUNNEL:
- Signup → First Gen: 45% (industry avg: 40%) ✅
- First Gen → Second Gen: 62% ✅
- Free → Pro: 3.2% (target: 5%)

SUGGESTION:
- Cost per gen is 40% higher on Fridays. Investigate: longer prompts or more complex requests?
- Free tier users who generate 6+ are 4× more likely to convert. Consider raising from 5 to 8.

Schedule: Daily
Model: Claude Sonnet (analysis quality matters)
```

### 4.3 Inter-Agent Routing Rules

This is the lateral communication that was missing from the original design. The Orchestrator manages these routes:

```
Monitor detects content quality issue (e.g., L1 Oracle slides empty)
  → Curator: "Regenerate top 3 affected combinations"
  → Growth: "Don't ask these users for testimonials"

Monitor detects error spike (error rate > 10%)
  → Intel: "Include cost impact in next digest"
  → (Critical alert sent to Marcos immediately)

Intel detects cost spike per generation
  → Monitor: "Investigate error rate correlation"
  → Curator: "Pause non-essential pre-generation"

Intel detects funnel drop-off (signup → first gen below 30%)
  → Growth: "Draft onboarding improvement suggestions"

Growth identifies churn-risk user who's also a superfan
  → Intel: "Calculate LTV before sending re-engagement"
  → Monitor: "Check their recent output quality"

Curator completes regeneration batch
  → Monitor: "Verify quality of new outputs"
  → Intel: "Update cost tracking"

Curator detects forge content update available
  → Monitor: "Watch for quality changes after sync"
  → Intel: "Estimate cost of regeneration batch"
```

### 4.4 Critical Alert System

The daily digest is for normal operations. Critical issues need immediate attention — Marcos shouldn't wait until 7 AM to find out the system is broken.

**Alert conditions and actions:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Error rate spike | > 10% for 2+ hours | Immediate email to Marcos |
| Zero generations | 24+ hours (when users exist) | Immediate email to Marcos |
| Content bug cluster | 3+ teachers report same bug in 24h | Immediate email + auto-flag content |
| Single gen cost spike | > $1.00 | Flag in next digest (not urgent) |
| Founding Member churning | Any Founding Member at risk | Immediate email to Marcos |
| Funnel anomaly | Signup → Gen drops below 20% | Flag in next digest |

**Alert format:**
```
🚨 COGNIESL CRITICAL ALERT
━━━━━━━━━━━━━━━━━━━━━━
Error rate: 14.2% (normal: < 5%)
Duration: 2.5 hours
Affected: 5 of 7 generations failed
Root cause: ModifySlide emoji encoding
Fix proposed: [link to agent_action]
━━━━━━━━━━━━━━━━━━━━━━
Acknowledge: [link]
Approve fix: [link]
```

### 4.5 The Daily Digest (Consolidated)

Every morning, Marcos receives ONE message that consolidates all agent reports:

```
═══════════════════════════════════════
  COGNIESL DAILY DIGEST — May 26, 2026
  Orchestrator run: 7:00 AM ✅ All agents healthy
═══════════════════════════════════════

📊 AT A GLANCE
   Generations today: 0 (just started) | Active users (7d): 4
   API cost today: $0.00 | MRR: $84.00
   System health: 96.2% ✅

🔧 MONITOR
   Quality score: 94% (down from 97%)
   1 anomaly: emoji encoding spike (fix proposed)
   0 critical issues

📦 CURATOR
   3 new decks | 2 pruned | Coverage: 76%
   5 decks flagged for regeneration (Portuguese L1 update)

📣 GROWTH
   2 new signups | 3 churn risks | 1 testimonial ready
   3 social posts drafted [review →]

💰 INTEL
   Monthly cost: $62.40 | Revenue: $84.00 | Margin: +$21.60 ✅
   Agent costs: $8.50/month total
   Suggestion: investigate Friday cost spike

📋 ACTIONS NEEDED FROM YOU:
   [ ] Approve emoji encoding fix [→]
   [ ] Approve 3 social media posts [→]
   [ ] Review 3 re-engagement emails [→]
   [ ] Approve Portuguese L1 sync [→]

═══════════════════════════════════════
```

---

## 4A. Dashboard Improvements for Self-Running

### 4A.1 New Tab: Orchestrator (Tab 5)

The current 4 tabs are passive (show data). The Orchestrator tab is active (Marcos commands the system):

- **Agent Health Matrix:** Last run, status, next run, manual trigger buttons
- **Orchestrator Queue:** What's currently running, progress indicator
- **Quick Actions:** [Run Full Check Now] [Send Test Digest] [Pause All Agents] [Regenerate Digest]

### 4A.2 Improvements to Existing Tabs

**Digest Tab:** Add agent health summary (4 green/yellow/red dots)

**Agents Tab:** Add cost tracking per agent action + agent efficiency metric (submitted vs. approved)

**Intelligence Tab:** Add anomaly feed (last 10 anomalies with timestamp and resolution)

### 4A.3 Mobile Optimization

- Digest tab loads by default on mobile (skip tab bar)
- Touch-friendly buttons (min 44px)
- No horizontal scrolling
- Modal close button reachable on small screens

---

## 5. Social Sharing & Growth Engine

### 5.1 Why This Matters More Than Any Ad Campaign

Teacher-to-teacher word-of-mouth is the **highest-converting growth channel** for education tools. A teacher posting "my secret weapon for lesson planning" is worth more than any Facebook ad.

### 5.2 The Trigger System

The key insight is: **ask for the share at the moment of maximum satisfaction.**

The best time to ask a teacher for a share, review, or testimonial is right after they've successfully generated materials and reacted positively.

```
Generation completes
       │
       ▼
Agent detects: positive outcome (no errors, no frustration signals)
       │
       ▼
Agent includes in the delivery message:
"Your materials are ready! 🎉 
 Quick question — if CogniESL saved you time today, 
 would you share one sentence about your experience? 
 It helps other teachers like you. Yes! / Not today"
       │
       ▼ (If "Yes!")
Agent opens a one-line input:
"What would you say? (or pick one below)
 • 'Made my lesson planning so much easier'
 • 'Finally, materials that match my students' needs'
 • 'More time for what matters — teaching'"
       │
       ▼
Agent asks: "Where would you like to share?"
 • [Post to X] [Post to Instagram] [Post to Facebook] 
 • [Leave a Google review] [Just send it to us for the website]
```

### 5.3 Pre-Written Social Templates

Offer teachers ready-made posts they can customize:

**Template 1 — Casual:**
> Just generated a full ESL lesson in 2 minutes with @CogniESL. Slides, worksheet, activity guide — all tailored to my students' native language. Work done, now play time with the kids! 🏀✏️

**Template 2 — Confident:**
> Why am I the teacher everyone asks for materials? 🤫 My secret weapon just got an upgrade. @CogniESL generates complete, professional ESL materials in minutes. Can't tell you my secret but... 👀

**Template 3 — Relatable:**
> Sunday night lesson prep: 2 minutes, not 2 hours. @CogniESL knows my students' native language and builds everything around the specific errors they make. Game changer for ESL teachers. 🔥

**Template 4 — Testimonial-style:**
> I've tried a lot of teaching tools. @CogniESL is the only one that gets L1 interference right — it actually knows WHY my Spanish speakers keep dropping the -s. This is real ESL expertise, automated.

### 5.4 Branded Snapshots (Shareable Images)

**What:** After generation, the system automatically creates a beautiful, branded preview image of:
- Slide 1 (title slide) with the CogniESL watermark
- A worksheet snippet
- A "generated in X minutes" stamp

**Format:** Instagram-post sized (1080×1080) with CogniESL branding at the bottom.

**Why:** Teachers are more likely to share an image than write text. A pretty picture of professional materials with a subtle "Generated with CogniESL" is powerful ambient marketing.

**Implementation:** Use Playwright (already in the codebase) to render slide HTML → PNG. Overlay with branding template. Include in the delivery email with: "Love your materials? Share this image!"

### 5.5 Google Review Automation

**When:** After 3+ successful generations (proven value delivered), trigger the review request.

**How (in the chat):**
> "Looks like CogniESL is working well for you! 🎉 Other teachers would love to hear about your experience. Would you leave a quick Google review? It takes 30 seconds: [link]"

**How (in the email):**
The 3rd material delivery email includes: "If you have 30 seconds, a Google review helps us reach more teachers like you: [link]"

**Scheduling logic:**
- Never ask a user who reported a bug or issues
- Never ask more than once per user
- Wait at least 7 days after signup
- Always ask after a positive signal (repeated generation, explicit positive feedback)

### 5.6 Viral Mechanics

**Referral links:** Every user gets a unique referral code. When a teacher signs up through their link:
- Referrer gets +5 generations (or 1 week free Pro)
- New user gets +3 bonus generations

**Shareable material links:** Teachers can generate a "view-only" link to their materials. A colleague clicks it, sees beautiful materials, sees "Generated with CogniESL", signs up. Requires a `/share/{share_id}` endpoint.

**School-level virality:** When one teacher in a school starts raving about CogniESL, the adoption spreads within the school. This is the School tier's growth engine.

---

## 6. The Intelligent Dashboard

### 6.1 Current Dashboard → Future Dashboard

The dashboard already exists (FOUNDER_DASHBOARD.md describes it fully, and `/api/admin/overview` is built). The self-running layer adds:

**From:** Marcos checks the dashboard → Marcos interprets the data → Marcos acts
**To:** AI agents watch the dashboard → AI agents interpret → AI agents report and propose → Marcos decides

### 6.2 AI Dashboard Layers

**Layer 1 — Anomaly Detection (Always On)**

Agents monitor these metrics continuously and alert when something unusual happens:

| Metric | Normal Range | Alert Trigger |
|---|---|---|
| Daily generations | Based on 7-day average | Deviation > 50% from average |
| Error rate | < 5% | > 10% for 2+ hours |
| New signups | Based on 7-day average | 0 for 3+ consecutive days |
| API cost per generation | ~$0.30 | > $0.50 (model issue or inefficiency) |
| Free→Pro conversion | 2-5% | Drops below 1% for 2+ weeks |
| Churn | < 5% monthly | Any single-day spike |

**Layer 2 — Predictive Analytics**

- **Churn prediction:** "These 5 Pro users are likely to churn in the next 14 days based on declining usage patterns. Suggested action: send a 'we miss you' email with a free generation bonus."
- **Demand forecasting:** "Present Perfect requests are trending up 30% week-over-week. Pre-generate the top 5 L1 combinations."
- **Revenue projection:** "At current growth rate, MRR will reach $500 by August."

**Layer 3 — Prescriptive Suggestions**

- "Teachers who generate materials on Sunday evening have 2× higher retention. Consider sending a 'Sunday planning' email."
- "The most common first-generation grammar point is Present Simple. Optimize the onboarding flow to start with this."
- "Your cost per generation is 40% higher on Fridays. Investigate: is the model being less efficient, or are Friday requests more complex?"

### 6.3 Dashboard API Extensions

New endpoints for the AI agents to consume:

```
GET /api/admin/feedback-summary    — Aggregated feedback data
GET /api/admin/churn-risk          — Users at risk of churning
GET /api/admin/growth-signals      — Anomalies and trends
GET /api/admin/agent-reports        — All agent reports in one feed
POST /api/admin/agent-action        — Marcos approves/rejects agent proposals
```

---

## 7. Email Intelligence Layer

### 7.1 Inbound Email Processing

**Setup:** Resend inbound webhook → FastAPI endpoint at `/api/inbound-email`

**Flow:**
```
Teacher replies to completion email
       │
       ▼
Resend webhook → /api/inbound-email
       │
       ▼
Secretary Agent classifies:
  ├── Bug report → QA Agent
  ├── Content issue → Content QA Agent
  ├── Question → Support Agent drafts response
  ├── Testimonial → CMO Agent
  ├── Feature request → Backlog
  └── Spam → Archive
       │
       ▼
Marcos gets classified summary with draft responses
       │
       ▼
Marcos approves → Resend sends response
```

### 7.2 Outbound Email Intelligence

**Track everything:**
- Open rates (Resend webhook)
- Click rates (track download link clicks)
- Reply rates
- Unsubscribe/bounce

**Use the data:**
- If completion emails have low open rates → test different subject lines
- If download links aren't being clicked → the materials might not be what teachers expected (quality issue)
- If a teacher opens every email but never generates → they're interested but something is blocking activation

### 7.3 Automated Email Sequences

**Onboarding sequence (for new signups who haven't generated yet):**
- Day 0: Welcome + "Generate your first lesson in 2 minutes"
- Day 3: "Still thinking about it? Here's what other teachers made"
- Day 7: "Your free generations are waiting — here's a tip for getting the best results"

**Re-engagement sequence (for churn-risk users):**
- Day 14 inactive: "We miss you! Here's what's new"
- Day 21 inactive: "Your students are waiting — generate a lesson in 2 minutes"
- Day 30 inactive: "Last chance to lock in your Pro pricing" (if applicable)

**Post-generation sequence:**
- Day 0: Materials ready (already exists)
- Day 1: "How were the materials?" (satisfaction check)
- Day 3: "Ready for next week's lesson?" (re-engagement)
- Day 7: "Did you know you can also generate..." (feature discovery)

---

## 8. Self-Improving Content Database

### 8.1 The Content Improvement Loop

The YAML database (grammar, L1, activities) is CogniESL's crown jewel. It should get better over time, automatically.

**How content improves:**

```
Teacher reports content issue
       │
       ▼
Content QA Agent reads the report + the implicated YAML file
       │
       ▼
Agent proposes a specific change to the YAML file
       │
       ▼
Marcos reviews and approves (or rejects)
       │
       ▼
Change is applied to the YAML file
       │
       ▼
All future generations using this content are improved
       │
       ▼
Master Repository decks using this content are flagged for regeneration
```

### 8.2 Proactive Content Enrichment

Beyond reactive fixes, agents can proactively identify enrichment opportunities:

**Gap detection:**
- "The Portuguese L1 file has 3 example sentences for Present Simple. The Spanish file has 8. Consider adding 5 more to Portuguese."
- "The grammar file for Third Conditional has no `student_quotes` field. 12 other grammar files have this. Adding it would improve L1 Oracle slides."

**Quality scoring:**
- Score each YAML file on completeness (all fields filled, enough examples, sources cited)
- Generate a prioritized list: "These 10 files would benefit most from enrichment"

**Teacher-sourced enrichment:**
- When a teacher provides a particularly good example in feedback, flag it: "Teacher suggested this example for Present Perfect: 'I have been waiting since 8 AM.' Consider adding to the grammar file."

### 8.3 Content Versioning

**Critical requirement:** Every change to the YAML database must be versioned.

**Implementation:** Simple Git-based versioning:
- The `data/` directory is in Git
- Every content change is a commit with message: "Content QA: Added 3 Portuguese L1 examples for Present Simple (teacher-reported)"
- Marcos can review the Git log to see all content changes
- Rollback is `git revert`

**Never let agents modify content without a commit trail.**

---

## 9. Implementation Roadmap

### Phase 1 — Feedback Foundation (Weeks 1-2)

**Goal:** Capture teacher feedback in the flow of the existing experience.

| Task | Effort | Impact |
|---|---|---|
| Add `feedback` table to database | 2 hours | Required for everything below |
| Add `👍/👎/Issues` widget to material cards | 4 hours | Primary feedback channel |
| Add `POST /api/feedback` endpoint | 1 hour | API for widget |
| Add frustration detection to agent instructions | 1 hour | Implicit feedback capture |
| Add `events` table for behavioral tracking | 2 hours | Implicit behavioral feedback |
| Log key events (download, generation, login) | 2 hours | Populate events table |

**Total: ~12 hours of development**

**What you get:** A feedback system that captures both explicit and implicit signals. Data starts accumulating immediately.

### Phase 2 — Classification & Routing (Weeks 3-4)

**Goal:** AI reads feedback and routes it to the right place.

| Task | Effort | Impact |
|---|---|---|
| Build Classification Agent | 4 hours | Front door of self-healing |
| Build routing logic | 2 hours | Right feedback → right agent |
| Add feedback summary to admin dashboard | 2 hours | Marcos can see all feedback |
| Add daily feedback digest email | 2 hours | Marcos stays informed |

**Total: ~10 hours**

**What you get:** Feedback is automatically classified and routed. Marcos sees a daily summary instead of raw feedback.

### Phase 3 — QA Agent (Weeks 5-6)

**Goal:** Automated code bug detection and fix proposals.

| Task | Effort | Impact |
|---|---|---|
| Build QA Agent (reads audit logs + failed jobs) | 6 hours | Automated bug detection |
| Build fix proposal pipeline | 4 hours | Code fixes proposed automatically |
| Add QA report to daily digest | 2 hours | Marcos sees QA status |

**Total: ~12 hours**

**What you get:** Code bugs are detected and fixed without Marcos having to investigate. Marcos approves the fix, agent prepares it.

### Phase 4 — Social Sharing & Growth (Weeks 7-8)

**Goal:** Turn happy teachers into marketers.

| Task | Effort | Impact |
|---|---|---|
| Post-generation share prompt in chat | 2 hours | Trigger at peak satisfaction |
| Pre-written social media templates | 2 hours | Easy sharing for teachers |
| Branded snapshot image generation | 6 hours | Visual shareable content |
| Google review request logic | 2 hours | Automated review collection |
| Referral link system | 4 hours | Viral growth mechanic |

**Total: ~16 hours**

**What you get:** A growth engine powered by teacher satisfaction. Every happy teacher becomes a potential marketer.

### Phase 5 — Full AI Organization (Weeks 9-14)

**Goal:** All department agents operational.

| Task | Effort | Impact |
|---|---|---|
| Curator Agent (extends existing design) | 8 hours | Master repo self-management |
| CMO Agent | 8 hours | Automated marketing |
| CFO Agent | 6 hours | Financial monitoring |
| Secretary Agent | 8 hours | Email intelligence |
| Support Agent | 4 hours | Second-line teacher support |
| Daily Digest system | 4 hours | Consolidated morning report |

**Total: ~38 hours**

**What you get:** The full AI organization. Marcos receives one daily digest, reviews agent proposals, and steers the ship.

### Phase 6 — Content Self-Improvement (Weeks 15-16)

**Goal:** The YAML database gets better over time.

| Task | Effort | Impact |
|---|---|---|
| Content QA Agent | 6 hours | Content bug triage + fix proposals |
| Content gap detection | 4 hours | Proactive enrichment identification |
| Content versioning (Git-based) | 2 hours | Audit trail for all changes |
| Teacher-sourced enrichment pipeline | 4 hours | Good teacher examples → database |

**Total: ~16 hours**

**What you get:** The database that powers CogniESL improves continuously, with full version control.

### Total Estimated Effort

**~104 hours** of development, spread across ~16 weeks. At a pace of 6-8 hours/week (realistic for a solo founder), this is **4 months** to a fully self-running CogniESL.

**But the key is:** each phase delivers value independently. You don't need to build everything to get benefits. Phase 1 alone (feedback collection) transforms your ability to improve the product.

---

## 10. Risks, Limits & Honest Tradeoffs

### 10.1 What Can Go Wrong

**Over-automation risk:** If agents make too many decisions without Marcos' review, quality can drift. A wrong content change propagated to the master repository affects every future teacher.

**Mitigation:** Content changes always require human approval. Code changes always require human approval. Agents propose, Marcos decides.

**Feedback noise:** Not all teacher feedback is useful. "I don't like the colors" is subjective. "The L1 pattern is wrong" is critical. The classifier must distinguish signal from noise.

**Mitigation:** Weight feedback by user expertise (Pro users who generate frequently are more reliable signal). Aggregate: one teacher reporting something is an anecdote; five teachers reporting the same thing is a pattern.

**Cost of agents:** Running multiple AI agents continuously adds API costs. The CMO Agent drafting social posts, the CFO Agent analyzing finances, the QA Agent monitoring logs — each costs tokens.

**Mitigation:** Use the cheapest model that's good enough for each task. Classification → Haiku. Code fixes → Sonnet. Marketing copy → Sonnet. Most agents run on schedules (not continuously), keeping costs manageable. Estimate: $20-50/month in additional API costs for the full agent team.

**Teacher trust:** If teachers find out an AI is running everything, some may feel uneasy. "Who's checking the AI?"

**Mitigation:** Be transparent. "CogniESL uses AI to improve itself, but every content change is reviewed by our founder, Marcos." This is actually a selling point — it shows commitment to quality.

### 10.2 What Should NOT Be Automated

| What | Why not | What to do instead |
|---|---|---|
| Content (grammar/L1) changes | Pedagogical correctness is non-negotiable. A wrong L1 pattern harms students. | Agent proposes, Marcos approves |
| Pricing changes | Strategic business decision | Agent suggests, Marcos decides |
| Teacher communication (final) | Teachers deserve a human touch for important matters | Agent drafts, Marcos sends |
| New feature development | Requires product vision and teacher understanding | Agent implements, Marcos designs |
| Master repo pruning (aggressive) | Rare combinations might become popular later | Conservative pruning (12+ months unused) |

### 10.3 Honest Assessment

**What's realistic in 3 months:**
- Feedback collection system ✅
- Classification and routing ✅
- QA Agent for code bugs ✅
- Social sharing prompts ✅
- Daily digest ✅

**What's realistic in 6 months:**
- Full AI organization (all department agents) ✅
- Content self-improvement pipeline ✅
- Email intelligence layer ✅
- Predictive analytics ✅

**What's aspirational (requires more infrastructure):**
- Fully autonomous code fix + deploy (without Marcos approving each one)
- AI-generated marketing campaigns that run without review
- Real-time social media engagement (AI responding to mentions)
- Autonomous content enrichment (AI adding to YAML files without review)

**The bottom line:** The self-running CogniESL is not about replacing Marcos. It's about Marcos spending 30 minutes a day reviewing an AI team's work instead of 8 hours doing everything himself. The AI handles the monitoring, analysis, drafting, and proposing. Marcos provides the judgment, vision, and approval.

That's the real promise: **you go from being the entire company to being the CEO of a company that never sleeps.**

---

## Appendix A: New Database Tables

```sql
-- Explicit and implicit feedback
CREATE TABLE feedback (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    material_id TEXT,
    rating TEXT NOT NULL,          -- 'perfect' | 'good' | 'issues'
    tags TEXT DEFAULT '',          -- comma-separated
    comment TEXT DEFAULT '',
    source TEXT DEFAULT 'explicit', -- 'explicit' | 'implicit_chat' | 'email' | 'delayed_email'
    created_at TEXT NOT NULL,
    reviewed INTEGER DEFAULT 0,
    resolution TEXT DEFAULT ''
);

-- Behavioral event stream
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    metadata TEXT DEFAULT '{}',
    created_at TEXT NOT NULL
);

-- Agent action log (audit trail for everything agents do)
CREATE TABLE agent_actions (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    action_type TEXT NOT NULL,     -- 'fix_proposed' | 'content_flagged' | 'post_drafted' | 'email_classified'
    description TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending' | 'approved' | 'rejected' | 'auto_approved'
    marcos_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    resolved_at TEXT
);

-- Social shares and referrals
CREATE TABLE social_shares (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    platform TEXT NOT NULL,        -- 'x' | 'instagram' | 'facebook' | 'google_review' | 'referral'
    testimonial_text TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
```

## Appendix B: New API Endpoints

```
# Feedback
POST   /api/feedback                    — Submit feedback (auth optional)
GET    /api/admin/feedback              — List feedback (admin only)
GET    /api/admin/feedback/summary      — Aggregated stats (admin only)

# Events
POST   /api/events                      — Log an event (internal)

# Social
POST   /api/share                       — Record a share event
GET    /api/referral/{code}             — Referral landing page

# Agent management
GET    /api/admin/agent-reports         — All agent reports
POST   /api/admin/agent-action          — Approve/reject agent proposal

# Email
POST   /api/inbound-email               — Resend inbound webhook

# Dashboard extensions
GET    /api/admin/churn-risk            — Users at risk
GET    /api/admin/growth-signals        — Anomalies and trends
```

---

*This document is a living strategy. As CogniESL grows, the self-running systems should grow with it. Start with Phase 1, learn from the data, and build toward the full vision incrementally.*
