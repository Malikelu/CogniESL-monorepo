# CogniESL Self-Running System — Implementation Plan

**Version:** 2.0.0
**Created:** 2026-05-26
**Author:** Apex (audit) + Marcos (direction)
**Status:** Ready to build
**Based on:** docs/SELF_RUNNING_COGNIESL.md + docs/DASHBOARD_ARCHITECTURE.md

---

## 1. Architecture Overview

### 1.1 The Three-Layer Model

```
LAYER 3: MARCOS (CEO)
  - Reads dashboard, approves/rejects agent proposals
  - Sets priorities via Apex
  - One daily digest, not 6 separate reports

LAYER 2: APEX (Your Right Hand — default Hermes profile)
  - General assistant for everything (CogniESL + personal + other businesses)
  - Checks on orchestrator status when you ask
  - Does NOT run CogniESL agent loops (avoids context split)

LAYER 1: COGNIESL ORCHESTRATOR (dedicated Hermes profile)
  - Runs department agents on schedule
  - Synthesizes all agent outputs into ONE daily digest
  - Manages inter-agent routing
  - Writes to dashboard via API
```

### 1.2 Why This Structure

- **Apex stays clean.** Your general assistant isn't buried in CogniESL operational loops. When you ask "what's the status of CogniESL?", Apex checks the orchestrator's latest report and tells you in 30 seconds. No context pollution.

- **Orchestrator is specialized.** It knows CogniESL inside out. It has skills specific to monitoring, quality, finance, growth. It doesn't know about your legal work or other businesses.

- **One digest, not six.** Instead of Marcos reading 6 separate agent reports, the orchestrator produces ONE consolidated daily digest. Each agent feeds into the orchestrator, the orchestrator feeds into Marcos.

### 1.3 Department Agents (Simplified)

The original plan had 6 agents + sub-agents. We're consolidating to 4 core functions that feed into the orchestrator:

| Agent | Purpose | Schedule | Model |
|-------|---------|----------|-------|
| **Monitor Agent** | Quality self-monitoring: output sampling, error tracking, anomaly detection | Every 4 hours | Haiku (cheap, fast) |
| **Curator Agent** | Master repo management: pre-generate, prune, flag for regeneration | Nightly | Sonnet (generation quality) |
| **Growth Agent** | Marketing: social posts, churn prevention, review collection, referrals | Daily | Sonnet (creative writing) |
| **Intel Agent** | Business intelligence: costs, funnel, anomalies, suggestions | Daily | Sonnet (analysis) |

The "Secretary" (email classification) and "Support" (teacher questions) are deferred — they're only useful when you have meaningful email volume and active users.

---

## 2. What The Orchestrator Does

### 2.1 Core Loop (Runs Daily)

```
1. COLLECT: Run each department agent, gather their outputs
2. CORRELATE: Cross-reference findings across agents
   - Monitor flagged quality issue on "Present Perfect + Korean"?
     → Tell Curator to regenerate those decks
   - Intel detected cost spike on Friday?
     → Include in digest with Monitor's error data
   - Growth identified a superfan?
     → Check Monitor for their quality score before asking for testimonial
3. SYNTHESIZE: Produce ONE consolidated daily digest
4. PROPOSE: Write agent_actions to DB for Marcos' approval
5. ALERT: If critical issue detected, send immediate notification
```

### 2.2 Inter-Agent Routing Rules

These are the lateral communication paths that the original design was missing:

```
Monitor detects content quality issue
  → Curator: "Regenerate top 3 affected combinations"
  → Growth: "Don't ask these users for testimonials"

Intel detects cost spike per generation
  → Monitor: "Investigate error rate correlation"
  → Curator: "Pause non-essential pre-generation"

Growth identifies churn-risk user who's also a superfan
  → Intel: "Calculate LTV before sending re-engagement"
  → Monitor: "Check their recent output quality"

Curator completes regeneration batch
  → Monitor: "Verify quality of new outputs"
  → Intel: "Update cost tracking"
```

### 2.3 Critical Alert System

The daily digest is for normal operations. Critical issues need immediate attention:

| Condition | Action |
|-----------|--------|
| Error rate > 10% for 2+ hours | Immediate dashboard alert + email to Marcos |
| Zero generations for 24+ hours (when users exist) | Immediate alert |
| Single generation cost > $1.00 | Flag in next digest (not urgent) |
| 3+ teachers report same content bug within 24h | Immediate alert + auto-flag content for review |
| Churning user was a Founding Member | Immediate alert |

---

## 3. Dashboard Improvements

### 3.1 New Tab: 🟣 Orchestrator (Tab 5)

The current 4 tabs (Digest, Details, Agents, Intelligence) are passive — they show data. The Orchestrator tab is active — it lets Marcos command the system.

**Sections:**

**A. Agent Health Matrix**
```
┌──────────────┬──────────┬─────────────┬───────────┬──────────┐
│ Agent        │ Last Run │ Status      │ Next Run  │ Actions  │
├──────────────┼──────────┼─────────────┼───────────┼──────────┤
│ Monitor      │ 2h ago   │ ✅ Healthy  │ In 2h     │ [Run Now]│
│ Curator      │ 14h ago  │ ✅ Done     │ In 10h    │ [Status] │
│ Growth       │ 1d ago   │ ✅ Done     │ In 23h    │ [Posts]  │
│ Intel        │ 1d ago   │ ⚠️ Delayed  │ Overdue   │ [Run Now]│
└──────────────┴──────────┴─────────────┴───────────┴──────────┘
```

**B. Orchestrator Queue**
- Shows what the orchestrator is currently doing
- "Running Monitor Agent... (step 2/4)"
- "Synthesizing daily digest..."
- Allows Marcos to pause/resume the orchestrator

**C. Quick Actions (Buttons)**
- [Run Full Check Now] — triggers orchestrator immediately
- [Send Test Digest] — sends the digest to Marcos right now
- [Pause All Agents] — stops all scheduled runs
- [Regenerate Digest] — re-runs synthesis without re-running agents

### 3.2 Improvements to Existing Tabs

**Digest Tab — Add Agent Health Summary**
- Current: At a Glance + Actions Needed + System Health
- Add: "Agent Team Status" — 4 green/yellow/red dots, one per department agent
- If Intel Agent hasn't run in 25 hours: yellow dot + "Intel Agent overdue"

**Agents Tab — Add Cost Tracking per Agent**
- Current: Agent actions with approve/reject
- Add: Estimated API cost per agent action
- Add: "Agent Efficiency" metric — proposals submitted vs. approved (if Marcos rejects 80% of Growth posts, the Growth agent needs tuning)

**Intelligence Tab — Add Anomaly Feed**
- Current: Funnel, churn risk, content quality heatmap
- Add: "Recent Anomalies" — last 10 anomalies detected, with timestamp and resolution status
- Example: "May 26, 14:32 — Error rate spiked to 12% (resolved: emoji encoding fix)"

### 3.3 Mobile Optimization

The current dashboard works on desktop. For Marcos checking on his phone:

- Digest tab should be the ONLY tab that loads by default on mobile (skip the tab bar, go straight to digest)
- Metric cards stack vertically (already handled by CSS grid)
- Agent action buttons need to be thumb-friendly (min 44px touch targets)
- Modal needs a close button that's reachable (not just Escape key)
- No horizontal scrolling anywhere

---

## 4. Database Additions

### 4.1 New Tables

```sql
-- Orchestrator runs (tracks orchestrator execution)
CREATE TABLE IF NOT EXISTS orchestrator_runs (
    id TEXT PRIMARY KEY,
    run_type TEXT NOT NULL,         -- 'scheduled' | 'manual' | 'retry'
    status TEXT DEFAULT 'running',  -- 'running' | 'completed' | 'failed' | 'paused'
    started_at TEXT NOT NULL,
    completed_at TEXT,
    agents_run TEXT DEFAULT '[]',   -- JSON array of agent names run
    critical_alerts INTEGER DEFAULT 0,
    error_message TEXT DEFAULT ''
);

-- Agent health (tracks each agent's operational status)
CREATE TABLE IF NOT EXISTS agent_health (
    agent_name TEXT PRIMARY KEY,
    last_run_at TEXT,
    last_success_at TEXT,
    consecutive_failures INTEGER DEFAULT 0,
    avg_runtime_seconds REAL DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    status TEXT DEFAULT 'unknown'  -- 'healthy' | 'degraded' | 'failing' | 'paused'
);

-- Inter-agent messages (lateral communication log)
CREATE TABLE IF NOT EXISTS agent_messages (
    id TEXT PRIMARY KEY,
    from_agent TEXT NOT NULL,
    to_agent TEXT NOT NULL,
    message_type TEXT NOT NULL,     -- 'regenerate' | 'flag_content' | 'pause' | 'alert'
    payload TEXT DEFAULT '{}',      -- JSON blob with details
    created_at TEXT NOT NULL,
    processed INTEGER DEFAULT 0,
    processed_at TEXT
);

-- Agent cost tracking (per-action API cost)
CREATE TABLE IF NOT EXISTS agent_costs (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    action_id TEXT,                 -- links to agent_actions.id
    estimated_cost_usd REAL DEFAULT 0,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    model_used TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
```

### 4.2 Modified Tables

```sql
-- Add cascade routing to agent_actions
ALTER TABLE agent_actions ADD COLUMN routed_to TEXT DEFAULT '';
ALTER TABLE agent_actions ADD COLUMN routed_at TEXT DEFAULT '';
ALTER TABLE agent_actions ADD COLUMN estimated_cost_usd REAL DEFAULT 0;
```

---

## 5. API Addpoints to Add

```
# Orchestrator
GET    /api/admin/orchestrator/status       — Current orchestrator state, last run, next run
POST   /api/admin/orchestrator/run          — Trigger manual orchestrator run
POST   /api/admin/orchestrator/pause        — Pause all agents
POST   /api/admin/orchestrator/resume       — Resume all agents
GET    /api/admin/orchestrator/history      — Last 30 orchestrator runs

# Agent health
GET    /api/admin/agent-health              — Status of all 4 department agents
POST   /api/admin/agents/{name}/run         — Trigger a specific agent manually
POST   /api/admin/agents/{name}/pause       — Pause a specific agent

# Inter-agent
GET    /api/admin/agent-messages            — Pending inter-agent messages
POST   /api/admin/agent-messages/{id}/ack   — Mark message as processed

# Cost tracking
GET    /api/admin/costs/daily              — Today's costs broken down by agent
GET    /api/admin/costs/weekly             — 7-day cost trend

# Critical alerts
GET    /api/admin/alerts                   — Active critical alerts
POST   /api/admin/alerts/{id}/acknowledge  — Marcos acknowledges alert
POST   /api/admin/alerts/{id}/resolve      — Marcos marks alert resolved
```

---

## 6. Implementation Phases

### Phase 1: Orchestrator Infrastructure (Week 1-2, ~8 hours)

**Goal:** The orchestrator can collect, correlate, synthesize, and produce one digest.

Tasks:
1. Add new database tables (orchestrator_runs, agent_health, agent_messages, agent_costs)
2. Create orchestrator module (`agent/orchestrator.py`) — the loop that runs agents and synthesizes
3. Add orchestrator API endpoints to server.py
4. Add Orchestrator tab to dashboard (agent health matrix + quick actions)
5. Wire the 4 existing report_writer functions to be called by orchestrator
6. Test: trigger orchestrator manually, verify digest is produced

**Verification:**
- Orchestrator runs all 4 agents in sequence
- One consolidated digest appears in the dashboard
- Agent health shows correct status for each agent
- Inter-agent messages are logged when one agent triggers another

---

### Phase 2: Monitor Agent MVP (Week 2-3, ~6 hours)

**Goal:** Automated quality self-monitoring catches degradation before teachers do.

Tasks:
1. Implement Monitor Agent (`agent/monitor_agent.py`):
   - Output sampler: randomly samples 1 in 10 generations, runs quality checklist
   - Error tracker: reads failed_jobs, correlates by error type
   - Anomaly detector: compares current metrics to 7-day rolling average
2. Add anomaly dashboard section to Intelligence tab
3. Add critical alert logic (immediate notification for error rate > 10%)
4. Wire Monitor to orchestrator (runs every 4 hours)

**Verification:**
- Monitor runs every 4 hours via orchestrator
- Sampled outputs are checked against quality checklist
- Anomalies appear in Intelligence tab
- Critical alerts trigger immediate email

---

### Phase 3: Intel Agent + Cost Tracking (Week 3-4, ~6 hours)

**Goal:** Financial monitoring and business intelligence automated.

Tasks:
1. Implement Intel Agent (`agent/intel_agent.py`):
   - Cost tracking: daily and weekly API spend by agent
   - Funnel analysis: signup → activation → engagement → power → paid
   - Prescriptive suggestions: simple rule-based for now ("cost per gen up 40% on Fridays")
2. Add cost tracking to agent_costs table
3. Add costs section to Digest tab (daily cost, weekly trend)
4. Add agent efficiency metric to Agents tab
5. Wire Intel to orchestrator (runs daily)

**Verification:**
- Daily digest includes cost breakdown by agent
- Dashboard shows 7-day cost trend sparkline
- Agent efficiency metrics are tracked (submitted vs. approved)

---

### Phase 4: Growth Agent MVP + Mobile (Week 4-5, ~8 hours)

**Goal:** Growth engine operational + dashboard works on phone.

Tasks:
1. Implement Growth Agent (`agent/growth_agent.py`):
   - Daily signup/generation metrics summary
   - Churn risk user identification (checks with Intel Agent)
   - Superfan identification (top Generation users, positive feedback)
   - Draft social post queue (3 templates, queued for Marcos approval)
2. Add Google review solicitor logic (after 3rd generation, no frustration, 7+ days old)
3. Dashboard mobile optimization:
   - Digest tab loads by default on mobile
   - Touch-friendly buttons
   - No horizontal scroll
4. Wire Growth to orchestrator (runs daily)

**Verification:**
- Growth agent produces daily summary with churn risks and superfans
- Social posts are drafted and queued for Marcos' approval
- Google review request triggers correctly (test with 3rd generation)
- Dashboard is usable on 375px screen

---

### Phase 5: Content Intelligence (Week 5-6, ~6 hours)

**Goal:** The content databaseself-improves.

Tasks:
1. Content QA extension in Curator:
   - Detects when forge has updates compared to production data
   - Proposes sync (never auto-applies, Marcos approves via dashboard)
   - Identifies grammar+L1 combinations with poor feedback → prioritizes in forge
2. SEO content agent: drafts blog posts from grammar+L1 database (1 per week, queued)
3. Content versioning: ensure all YAML changes are Git commits with audit trail

**Verification:**
- Curator detects content gap and flags it
- SEO blog post is drafted and queued for Marcos
- Every content change has a Git commit

---

### Phase 6: Critical Alerts + Polish (Week 6-7, ~4 hours)

**Goal:** Real-time alerting for critical issues + final polish.

Tasks:
1. Implement critical alert system:
   - Error rate > 10% for 2+ hours → immediate email
   - Zero generations for 24h (when users exist) → immediate email
   - 3+ teachers report same content bug → immediate email + auto-flag
2. Add alerts tab/section to dashboard
3. Add alert acknowledgment flow (Marcos marks alert as seen/resolved)
4. End-to-end testing: trigger each alert type, verify notification arrives

**Verification:**
- Each alert type triggers correctly
- Alerts appear in dashboard and email
- Marcos can acknowledge and resolve alerts

---

## 7. Summary

| Phase | Focus | Hours | Deliverable |
|-------|-------|-------|-------------|
| 1 | Orchestrator Infrastructure | 8 | One consolidated digest, agent health matrix |
| 2 | Monitor Agent | 6 | Quality self-monitoring, anomaly detection |
| 3 | Intel Agent + Cost Tracking | 6 | Financial monitoring, cost breakdown |
| 4 | Growth Agent + Mobile | 8 | Growth engine, mobile dashboard |
| 5 | Content Intelligence | 6 | Content QA, SEO drafts, versioning |
| 6 | Critical Alerts + Polish | 4 | Real-time alerting, end-to-end testing |
| **Total** | | **~38 hours** | |

**What's NOT in this plan (deferred):**
- Secretary Agent (email classification) — only useful with meaningful email volume
- Support Agent (teacher questions) — only useful with active user base
- Fully autonomous code fix + deploy — too risky without production data
- Real-time social media engagement — need social accounts first
- Autonomous content enrichment — pedagogical correctness requires human review

**What's different from the original plan:**
- 4 agents instead of 6 (Secretary and Support deferred)
- Orchestrator layer added (was missing)
- Inter-agent routing defined (was missing)
- Critical alert system added (was missing)
- Cost tracking per agent added (was missing)
- Agent performance metrics added (was missing)
- Mobile optimization added (was missing)
- Each phase is simpler — build the data pipeline first, add intelligence later
