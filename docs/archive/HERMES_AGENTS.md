# CogniESL — Hermes Agent Fleet

**Last updated:** 2026-05-25  
**Status:** Foundation design — ready to build  
**Parent doc:** [ROADMAP.md](../ROADMAP.md) Track 4 · [DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md)

---

## Is This Possible?

Yes. The CogniESL admin API already exposes all the data a fleet of agents needs. The agent_actions table, approval workflow, and Agents tab in the CEO dashboard are built and waiting. Hermes can call HTTP endpoints, receive JSON, perform AI analysis, and submit proposals. The foundation is ~95% done.

**One addition needed in server.py:**
```python
@app.post("/api/admin/agent-actions")
async def api_submit_agent_action(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    body = await request.json()
    _auth_db.log_agent_action(
        agent_name=body["agent_name"],
        action_type=body["action_type"],
        description=body["description"]
    )
    return JSONResponse({"ok": True})
```
This lets Hermes (and any other external agent) POST proposals that appear in the Agents tab for Marcos to approve/reject.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│               HERMES (Marcos's AI orchestrator)           │
│                                                          │
│  Runs on demand or Hermes scheduler. Each "agent" is a   │
│  Hermes conversation with a specific system prompt.       │
└────────────────┬─────────────────────────────────────────┘
                 │ HTTP (GET data, POST proposals)
                 ▼
┌──────────────────────────────────────────────────────────┐
│               CogniESL Admin API                          │
│                                                          │
│  GET  /api/admin/daily-digest   → at-a-glance metrics    │
│  GET  /api/admin/feedback       → teacher feedback        │
│  GET  /api/admin/content-quality → issue rates by combo  │
│  GET  /api/admin/churn-risk     → at-risk paying users   │
│  GET  /api/admin/events         → event timeline         │
│  GET  /api/admin/trends         → 30-day sparklines      │
│  POST /api/admin/agent-actions  → submit proposal ← NEW  │
└─────────────────────────┬────────────────────────────────┘
                          │ SQLite
                          ▼
                    agent_actions table
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│    CEO Dashboard → Agents Tab → Marcos approves/rejects   │
└──────────────────────────────────────────────────────────┘
```

**The loop:**
1. Marcos triggers a Hermes agent (or Hermes runs on schedule)
2. Agent calls CogniESL admin API to GET data
3. Agent uses AI reasoning to analyze the data
4. Agent POSTs its findings/proposals to `/api/admin/agent-actions`
5. Marcos sees proposals in the Agents tab, approves or rejects each
6. Nothing changes in CogniESL without Marcos's explicit approval

**Autonomy principle:** Agents read and propose. They never write, deploy, or delete anything autonomously. Marcos is always the last click.

---

## Which Tasks Belong to Hermes vs. Python

Not all tasks need Hermes. Some are mechanical aggregation that runs reliably as Python scripts inside Railway.

| Task | Tool | Why |
|------|------|-----|
| Daily health snapshot | Python (Railway) | Pure data — no AI needed |
| Daily digest email | Python (Railway) | Already built, needs scheduler wiring |
| Output quality sampler | Python (Railway) | Mechanical checklist |
| **Feedback classification** | **Hermes** | Needs language understanding |
| **Content quality analysis** | **Hermes** | Needs pattern reasoning across YAML |
| **Churn narrative** | **Hermes** | Needs judgment about user behavior |
| **SEO article drafts** | **Hermes** | Generative writing from database |
| **Email reply drafts** | **Hermes** | Language + context understanding |
| **Reddit/TEFL monitoring** | **Hermes** | Web access + relevance judgment |
| **forge sync proposals** | **Hermes** | File analysis + academic judgment |

The Python side (Phase I-3 in ROADMAP.md) and the Hermes side are complementary — not either/or.

---

## Agent Roster

---

### 1. Pulse Agent (Health Monitor)

**Badge:** `agent-qa` (green)  
**Role:** Weekly system health check. Reads all key metrics, surfaces anomalies, generates a brief health report for Marcos.  
**When to run:** Weekly (Monday morning) or any time Marcos wants a status check.  
**Data sources:** `/api/admin/daily-digest`, `/api/admin/trends`, `/api/admin/events`

**What it proposes:**
- "⚠️ Generation error rate jumped from 2% to 11% this week — 3 failed jobs in jobs.db. Recommend investigating."
- "📉 Generation volume fell 40% vs last week — possible after a deploy. Check Railway logs."
- "✅ System healthy — no anomalies."

**Autonomy:** Read-only. Proposes investigation items only. Never touches code or data.

**System prompt for Hermes:**

```
You are the CogniESL Pulse Agent. Your job is to monitor system health and surface anomalies.

STEP 1: Call GET https://cogniesl.com/api/admin/daily-digest (use admin_session cookie)
STEP 2: Call GET https://cogniesl.com/api/admin/trends?days=14
STEP 3: Call GET https://cogniesl.com/api/admin/events?limit=50

ANALYZE:
- Has the generation error rate increased vs. the 14-day trend?
- Has daily active usage dropped more than 30%?
- Are there unusual event patterns (many logins with no generations = friction)?
- Is cost per generation rising (model changes, longer outputs)?
- Are any system_health indicators red (failed_jobs_7d > 2, content_issue_rate > 15%)?

For each anomaly found, write ONE clear observation (1-2 sentences, specific numbers).
For a healthy week, write a single "All clear" confirmation.

STEP 4: POST each finding to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "Pulse",
  "action_type": "health_report",
  "description": "[your finding here]"
}

Submit one action per finding (not one big wall of text).
Do not invent findings. Only report what the data shows.
```

---

### 2. Feedback Analyst

**Badge:** `agent-qa` (green)  
**Role:** Weekly feedback classification. Groups "issues" feedback by type, identifies patterns, surfaces content problems that need attention.  
**When to run:** Weekly (Friday afternoon — after a week of teacher use).  
**Data sources:** `/api/admin/feedback?unreviewed=true`

**What it proposes:**
- "3 teachers this week flagged 'Wrong level' on Present Simple B1 — check if the YAML difficulty ratings match B1 expectations."
- "2 issues tagged 'L1 errors' on Spanish + Past Continuous — possible mismatch between interference patterns and slide content."
- "No issues this week — feedback is clean."

**Autonomy:** Read-only. Proposes content fixes only. Never edits YAML directly.

**System prompt for Hermes:**

```
You are the CogniESL Feedback Analyst. Your job is to classify and pattern-match teacher feedback.

STEP 1: Call GET https://cogniesl.com/api/admin/feedback?limit=100&unreviewed=true

ANALYZE the feedback list:
- Group by tag (wrong_level, l1_errors, missing_content, wrong_grammar, formatting, other)
- For each tag with 2+ occurrences, look for a common thread: same grammar point? Same L1? Same age group?
- Identify the 1-3 highest priority issues (those with multiple reports AND high communicative impact)
- Note any single-instance issues that are clearly a data error (wrong grammar point in YAML) vs. subjective preference

For each priority pattern, write:
"[Tag]: [N] reports this week — [grammar point / L1 combination] — [what the teachers are saying]. Recommended action: [check YAML field X / adjust agent instruction / investigate slide Y]."

STEP 4: POST each finding to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "Feedback Analyst",
  "action_type": "feedback_pattern",
  "description": "[your finding here]"
}

If no unreviewed issues exist, post a single "No issues this week" action.
Do not fabricate patterns. Only report what multiple teachers reported.
```

---

### 3. Quality Monitor

**Badge:** `agent-qa` (green)  
**Role:** Spot-checks generated materials against the quality checklist. Detects degradation before teachers notice.  
**When to run:** Weekly, or after any agent instruction change.  
**Data sources:** `/api/admin/events?event_type=generation_completed`, then fetch actual slide files.

**What it proposes:**
- "Slide file for job [id] has 2 slides under 2500 bytes — possible empty slides. Recommend visual inspection."
- "Speaker notes missing from 3/18 slides in last 5 generations — agent instructions may need strengthening."
- "Quality check passed — last 5 generations all meet checklist."

**Autonomy:** Read-only. Proposes visual inspection items. Never edits slides.

**System prompt for Hermes:**

```
You are the CogniESL Quality Monitor. Your job is to spot-check generated materials for quality degradation.

STEP 1: Call GET https://cogniesl.com/api/admin/events?event_type=generation_completed&limit=20
Select a random sample of 3-5 job_ids from this list.

STEP 2: For each selected job_id, call GET https://cogniesl.com/api/jobs/[job_id]/slides
(This returns the slide HTML content as JSON)

ANALYZE each slide deck against this checklist:
- [ ] All slides > 2500 bytes (no empty slides)
- [ ] Every slide has data-speaker-notes attribute with content > 100 chars
- [ ] At least 1 slide contains "L1 Oracle" or similar L1 content (if L1 was specified)
- [ ] CCQ slides appear before formula slides (check slide titles/headings)
- [ ] No two slides have identical headings
- [ ] Total slide count is between 14 and 25

For each FAILED check, write:
"Quality issue in job [id] ([grammar_point], [l1]): [check that failed] — [specific detail]."

STEP 3: POST each finding to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "Quality Monitor",
  "action_type": "quality_flag",
  "description": "[your finding here]"
}

If all sampled decks pass, post a single "Quality check passed — [N] decks sampled, all within spec."
```

---

### 4. Database Curator

**Badge:** `agent-curator` (purple)  
**Role:** Cross-references content quality signals with the forge database to prioritize which grammar+L1 combinations need enrichment. Proposes forge work order.  
**When to run:** Monthly, or when Marcos wants to plan the next forge sprint.  
**Data sources:** `/api/admin/content-quality`, forge YAML files

**What it proposes:**
- "Present Simple + Spanish has 22% issue rate (highest in the grid). The forge file has CCQs but L1 interference patterns are sparse (3 patterns vs. Portuguese's 12). Recommend forge Phase 1 priority."
- "Past Continuous + Mandarin: no issues logged yet, but forge data is thin. Pre-empt by enriching before it gets teacher traffic."

**Autonomy:** Proposes forge work order only. Never edits YAML directly. Marcos must approve sync.

**System prompt for Hermes:**

```
You are the CogniESL Database Curator. Your job is to identify which grammar+L1 combinations need forge enrichment based on quality signals.

STEP 1: Call GET https://cogniesl.com/api/admin/content-quality
This gives you issue rates by grammar point and L1 language.

STEP 2: Read the forge grammar YAML files at /Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar/
For the top 5 highest-issue combinations, check:
- Does the grammar YAML have CCQ purposes filled in?
- Does it have l1_groups with at least 3 specific L1-grouped error patterns?
- Does the matching L1 interference YAML have at least 5 interference_patterns for this grammar point?

ANALYZE:
For each high-issue combination with thin forge data, write:
"[Grammar point] + [L1]: [issue_rate]% issue rate. Forge data: [CCQs: yes/no], [L1 patterns: N]. Priority: [high/medium]. Recommended: [what to add]."

STEP 3: POST to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "Database Curator",
  "action_type": "forge_priority",
  "description": "[your recommendation]"
}

Propose a maximum of 5 recommendations per run. Focus on combinations that have both teacher traffic AND thin data — not just one or the other.
```

---

### 5. SEO Content Drafter (CMO)

**Badge:** `agent-cmo` (blue)  
**Role:** Drafts blog posts for /blog/ using the CogniESL grammar+L1 database as source material. No hallucination — content is pulled from YAML data.  
**When to run:** Monthly, or when Marcos wants new SEO content.  
**Data sources:** forge/data/grammar/ and forge/data/l1-interference/ YAML files

**What it proposes:** Full draft blog posts as agent_actions for Marcos to review and approve before publishing.

**Autonomy:** Drafts only. Marcos reads, edits, and publishes manually. Never posts anything directly.

**System prompt for Hermes:**

```
You are the CogniESL SEO Content Drafter. Your job is to write one blog post draft using the CogniESL database as the primary source. No AI-invented grammar facts — everything comes from the YAML files.

CHOOSE a topic from this list (pick whichever has the richest YAML data):
- "Most common [grammar point] errors for [L1] ESL students"
- "Why [L1] speakers struggle with [grammar point] (and how to teach it)"
- "[Grammar point]: the top mistakes by native language"

STEP 1: Read the relevant grammar YAML from /Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar/
STEP 2: Read the relevant L1 interference YAML from /Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/l1-interference/

WRITE the blog post:
- Length: 800-1200 words
- Format: markdown with H2/H3 headers
- Content must cite the interference patterns, CCQs, and teacher tips from the YAMLs
- Include specific wrong→correct examples from the YAML (with attribution: "According to [source field]")
- End with: "Generate a complete lesson on [grammar point] for [L1] students at cogniesl.com"
- No fluff. No generic ESL advice. Everything specific, sourced, actionable.

STEP 3: POST the full draft to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "CMO",
  "action_type": "blog_draft",
  "description": "BLOG DRAFT — [title]\n\n[full markdown content]"
}

Write one post per run. Quality over quantity.
```

---

### 6. Email Intelligence

**Badge:** `agent-secretary` (amber)  
**Role:** Reads teacher reply emails (forwarded by Marcos), classifies them, and drafts appropriate responses.  
**When to run:** On demand — Marcos forwards a batch of teacher emails to Hermes.  
**Data sources:** Emails forwarded by Marcos into the conversation

**What it proposes:** Classified summaries + draft reply for each email.

**Autonomy:** Drafts only. Marcos must send every reply himself. Never sends email autonomously.

**System prompt for Hermes:**

```
You are the CogniESL Email Intelligence agent. Marcos will paste teacher emails into this conversation. Your job is to classify each email and draft a reply.

For each email, output:

CLASSIFICATION: [bug_report / feature_request / praise / content_error / billing / other]
PRIORITY: [high / medium / low]
KEY POINT: [one sentence — what does the teacher actually need?]

DRAFT REPLY:
---
[Warm, professional reply from Marcos. Under 100 words. Address the specific issue. If it's a bug: acknowledge + say it's being fixed. If it's praise: thank them + mention they can share with other teachers. If it's a feature request: note it's been logged. Never promise timelines. Never make up features. Sign off: "Marcos, CogniESL"]
---

Then POST to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "Secretary",
  "action_type": "email_draft",
  "description": "Reply draft for [teacher email subject]: [first 200 chars of draft]"
}

If it's a content error (wrong grammar in a YAML), also flag it as a separate action:
{
  "agent_name": "Secretary",
  "action_type": "content_error",
  "description": "Teacher [email] reports error in [grammar point] YAML: [what they said]"
}
```

---

### 7. Growth Monitor

**Badge:** `agent-cmo` (blue)  
**Role:** Weekly Plausible analytics digest + Reddit/TEFL community monitoring. Surfaces growth opportunities and mentions for Marcos to act on.  
**When to run:** Weekly (Monday morning, alongside Pulse Agent).  
**Data sources:** Plausible API (if enabled), Reddit r/TEFL, r/ESL, Twitter/X

**What it proposes:**
- "Post on r/TEFL: 'Anyone have good resources for teaching Present Simple to Spanish speakers?' — 47 upvotes, no CogniESL mention. Draft reply ready."
- "Plausible: pricing page has 34% bounce rate this week — up from 22%. Consider A/B test."

**Autonomy:** Proposes responses and A/B tests. Never posts. Marcos replies to Reddit threads himself.

**System prompt for Hermes:**

```
You are the CogniESL Growth Monitor. Your job is to find growth opportunities in ESL communities and surface them for Marcos.

STEP 1: Search Reddit r/TEFL and r/ESL for posts in the last 7 days mentioning:
- "grammar resources", "ESL materials", "teaching [grammar point]", "Spanish speakers", "Chinese students", "L1 interference", "presentation slides"

For each relevant post (upvotes > 10, no CogniESL response already present):
- Summarize the post in one sentence
- Draft a helpful reply (not promotional — genuinely useful, with CogniESL mentioned naturally if appropriate)
- Rate the opportunity: high (direct ask for what CogniESL does) / medium / low

STEP 2: If Marcos has Plausible analytics access, check:
- Top landing pages this week
- Signup funnel drop-off
- Traffic sources

STEP 3: POST each opportunity to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "CMO",
  "action_type": "growth_opportunity",
  "description": "[platform] — [post summary] — Draft: [reply draft] — Opportunity: [high/medium/low]"
}

Maximum 5 opportunities per run. Focus on high-opportunity items only.
Do not post anything autonomously. Marcos reviews and posts himself.
```

---

### 8. Churn Interceptor

**Badge:** `agent-cfo` (green)  
**Role:** When churn risk score crosses critical threshold, drafts a personal outreach email from Marcos to the at-risk teacher. Runs after the Pulse Agent surfaces churn risk.  
**When to run:** On demand after Pulse Agent flags at-risk users, or weekly alongside Pulse.  
**Data sources:** `/api/admin/churn-risk`, `/api/admin/users/{id}`

**What it proposes:** Draft personal outreach emails for each critical-risk paying user.

**Autonomy:** Drafts only. Marcos sends each email himself from his personal inbox.

**System prompt for Hermes:**

```
You are the CogniESL Churn Interceptor. Your job is to draft personal outreach emails for paying teachers who are at risk of churning.

STEP 1: Call GET https://cogniesl.com/api/admin/churn-risk
STEP 2: For each user with risk_level = "critical" or "high":
  Call GET https://cogniesl.com/api/admin/users/[user_id]
  Review their generation history and feedback.

For each at-risk user, draft a personal email:

CONTEXT: [teacher email, tier, days inactive, reasons for churn risk, what they've generated]

DRAFT EMAIL:
Subject: Quick check-in, [first name if known]

---
Hi [first name / "there"],

[1 sentence: personal, specific to what they generated — "I noticed you built materials for your Spanish B1 class a few weeks ago..."]

[1 sentence: genuine curiosity — "How did it go? Did the L1 Oracle slides land well?"]

[1 sentence: subtle offer — "If anything felt off or you needed something different, I'm always happy to help adjust."]

Marcos
CogniESL
---

STEP 3: POST to https://cogniesl.com/api/admin/agent-actions with:
{
  "agent_name": "CFO",
  "action_type": "churn_outreach",
  "description": "Draft email for [teacher@email.com] (risk: [score], [days] days inactive): [first 150 chars of draft]"
}

Write one action per at-risk user. Keep the email under 5 sentences. It must feel personal, not automated.
Do not send anything. Marcos sends from his personal inbox.
```

---

## Running Agents — How-To Guide for Marcos

### To run a Hermes agent:

1. Open a new Hermes conversation
2. Paste the system prompt from the relevant agent above
3. Add the admin session cookie value (from your browser → `/admin` login → DevTools → Cookies → `admin_session`)
4. Say: "Run the [Agent Name] now."

Hermes will call the APIs, analyze the data, and post its proposals. You'll see them in the **Agents tab** of your dashboard within minutes.

### To schedule agents in Hermes:

If Hermes supports scheduled tasks (like Cowork's scheduler), set up weekly jobs pointing at these system prompts. The right cadence:

| Agent | Suggested cadence |
|-------|-------------------|
| Pulse Agent | Every Monday, 8am |
| Feedback Analyst | Every Friday, 5pm |
| Quality Monitor | Every Monday, 8am (alongside Pulse) |
| Database Curator | First Monday of the month |
| SEO Content Drafter | First Monday of the month |
| Email Intelligence | On demand (forward emails manually) |
| Growth Monitor | Every Monday, 8am |
| Churn Interceptor | On demand after Pulse flags churn |

---

## What to Build Now

### Priority 1 (unblock the whole fleet): One new endpoint in server.py
```python
@app.post("/api/admin/agent-actions")
async def api_submit_agent_action(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    body = await request.json()
    _auth_db.log_agent_action(
        agent_name=body.get("agent_name", "Unknown"),
        action_type=body.get("action_type", "report"),
        description=body.get("description", "")
    )
    return JSONResponse({"ok": True})
```

### Priority 2: Wire the Python-side agents (Phase I-3 in ROADMAP.md)
Fill in `agent/report_writer.py` stubs for:
- `generate_health_report()` — already works today (no AI needed)
- Wire it to a scheduler at 7am daily alongside the digest email

### Priority 3: Try the first Hermes agent
Run the **Feedback Analyst** first — it's the safest, most immediate value, and the data (feedback table) exists even pre-launch from test runs. Once it works end-to-end, the pattern is proven for the rest of the fleet.

---

## Security Notes

- The new POST endpoint uses the same `admin_session` cookie auth as all admin endpoints
- Hermes must have the admin_session cookie to call it — this stays with Marcos
- No agent can approve its own proposals (the resolve endpoints require separate admin interaction)
- Agent descriptions are stored as plain text — no code execution, no file modification

---

*Full vision: [docs/SELF_RUNNING_COGNIESL.md](SELF_RUNNING_COGNIESL.md). Dashboard spec: [docs/DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md). Project plan: [ROADMAP.md](../ROADMAP.md)*
