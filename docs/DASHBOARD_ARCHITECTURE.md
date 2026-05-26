# CogniESL Admin Dashboard — Complete Technical Reference

**Version:** 1.0.0  
**Last Updated:** 2026-05-24  
**Author:** Built by OWL (Claude Code) under Marcos' direction  
**Status:** All phases implemented. Ready for deployment (Track 1).

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [File Inventory](#3-file-inventory)
4. [Database Schema — Complete](#4-database-schema--complete)
5. [API Reference — All Endpoints](#5-api-reference--all-endpoints)
6. [Dashboard UI Specification](#6-dashboard-ui-specification)
7. [What Was Built Per Phase](#7-what-was-built-per-phase)
8. [Debugging Guide](#8-debugging-guide)
9. [Future Implementation Guide](#9-future-implementation-guide)
10. [Environment & Deployment Notes](#10-environment--deployment-notes)

---

## 1. Overview

### What The Dashboard Is

The CogniESL Admin Dashboard (`/admin`) is Marcos' **CEO Command Center** — the single screen where he monitors, approves, and steers the entire product. It evolved from a simple metrics viewer into a four-tab intelligence system:

| Tab | Purpose | Phases |
|-----|---------|--------|
| **📊 Digest** | One-screen daily briefing — metrics + action items + system health | D |
| **📈 Details** | Original analytics — live pulse, users, feedback, errors, trends | A + original |
| **🤖 Agents** | Agent work queue — approve/reject proposals, activity feed | B |
| **🧠 Intelligence** | Predictive analytics — funnel, churn risk, content quality | C |

### Design Principles

- **Single-file UI:** `admin/dashboard.html` is self-contained (HTML + CSS + JS). No build step, no framework, no external dependencies.
- **Additive changes:** Every database change is `CREATE TABLE IF NOT EXISTS` or `ALTER TABLE ... ADD COLUMN`. Zero destructive migrations.
- **Admin auth:** SHA256 hash of `ADMIN_PASSWORD` env var, stored in `admin_session` cookie (8-hour TTL, httponly, SameSite=strict).
- **No new dependencies:** Everything uses existing Python stdlib + FastAPI + SQLite.

---

## 2. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │           admin/dashboard.html (single file)             │     │
│  │  ┌──────────┬──────────┬──────────┬──────────────────┐  │     │
│  │  │ 📊 Digest│📈 Details│🤖 Agents │🧠 Intelligence   │  │     │
│  │  └──────────┴──────────┴──────────┴──────────────────┘  │     │
│  │         fetch() with credentials:'same-origin'            │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────┬────────────────────────────────────┘
                              │ HTTP
┌─────────────────────────────▼────────────────────────────────────┐
│                    FastAPI — server.py                            │
│                                                                  │
│  Auth layer: _require_admin() checks admin_session cookie        │
│  Auth layer: _require_auth() checks JWT bearer token             │
│                                                                  │
│  ┌─────────────────── Admin API Routes ───────────────────────┐  │
│  │ GET    /admin                  → dashboard.html or login    │  │
│  │ POST   /admin/login            → set admin_session cookie  │  │
│  │ GET    /api/admin/overview     → metrics + failed jobs     │  │
│  │ GET    /api/admin/users        → paginated user list       │  │
│  │ GET    /api/admin/feedback     → feedback + summary        │  │
│  │ POST   /api/admin/feedback/{id}/resolve  → mark reviewed   │  │
│  │ GET    /api/admin/users/{id}   → full user activity        │  │
│  │ GET    /api/admin/events       → event timeline            │  │
│  │ GET    /api/admin/engagement   → DAU/WAU/MAU + stats       │  │
│  │ GET    /api/admin/agent-actions → agent action list        │  │
│  │ POST   /api/admin/agent-actions/{id}/resolve → approve     │  │
│  │ GET    /api/admin/agent-reports → summary + pending        │  │
│  │ GET    /api/admin/churn-risk   → at-risk paying users      │  │
│  │ GET    /api/admin/funnel       → engagement funnel         │  │
│  │ GET    /api/admin/content-quality → quality heatmap data   │  │
│  │ GET    /api/admin/trends       → 30-day daily snapshots    │  │
│  │ GET    /api/admin/daily-digest → consolidated CEO digest   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────── Public API Routes ──────────────────────┐  │
│  │ POST /api/auth/* (register, login, forgot-password, etc.)  │  │
│  │ GET/POST /api/materials/* (CRUD)                           │  │
│  │ POST /cogniesl/get_response (main agent endpoint)          │  │
│  │ GET /api/jobs/* (job status, slides, bundle)               │  │
│  │ POST /api/feedback (submit feedback, auth optional)         │  │
│  │ POST /api/waitlist                                         │  │
│  │ POST/GET /api/stripe/* (checkout, webhook, founding status)│  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │ SQLite
┌─────────────────────────────▼────────────────────────────────────┐
│                        Database Layer                            │
│                                                                  │
│  ┌────────────────────── cogniesl.db ─────────────────────────┐  │
│  │ users │ materials │ generations │ feedback │ events        │  │
│  │ waitlist │ subscription_events │ password_reset_tokens      │  │
│  │ agent_actions │ daily_snapshots │ daily_digests             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────── jobs.db ─────────────────────────────┐  │
│  │ jobs (job_id, status, grammar_point, error, file_paths...) │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  All DB operations in: auth/db.py                                │
│  Jobs DB operations in: agent/jobs.py                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. File Inventory

### Files Modified in This Work

| File | Lines | What Changed |
|------|-------|-------------|
| `CogniESL/auth/db.py` | 1,045 | Added 3 tables (`agent_actions`, `daily_snapshots`, `daily_digests`), 3 indexes, 18 new functions. See [database section](#4-database-schema--complete) for full list. |
| `CogniESL/server.py` | 1,291 | Added 13 new admin API endpoints (all prefix `/api/admin/`). Zero changes to existing endpoints. |
| `CogniESL/admin/dashboard.html` | 921 | Complete rewrite. Preserved all original sections. Added 4-tab layout, drill-down modal, sparklines, funnel, churn cards, quality heatmap, agent queue, feedback center, digest card. |
| `CogniESL/agent/email_sender.py` | 210 | Added `send_daily_digest_email()` function at end of file. Reads `FOUNDER_EMAIL` and `RESEND_API_KEY` env vars. Uses the same Resend API pattern as existing `send_completion_email()`. |

### Files Created in This Work

| File | Lines | Purpose |
|------|-------|---------|
| `CogniESL/agent/report_writer.py` | 71 | Extension point for self-running agent reports. Contains `generate_health_report()` (works today, no AI needed) and stubs for QA, CMO, CFO, Curator, Secretary agents (raise `NotImplementedError`). |

### Key Existing Files (Not Modified but Relevant)

| File | Lines | Purpose |
|------|-------|---------|
| `CogniESL/agent/jobs.py` | 147 | Job lifecycle (create, update, mark complete). Jobs DB is separate SQLite file (`jobs.db`). |
| `CogniESL/agent/audit_logger.py` | 195 | Audit trail logging to `logs/cogniesl_audit_*.log` files. Not in database. |
| `CogniESL/agent/curator_agent.py` | 294 | Pre-generates popular grammar+L1 combinations. CLI + scheduler. |
| `CogniESL/agent/cogniesl_agent.py` | 122 | Main agent orchestrator. |
| `CogniESL/docs/SELF_RUNNING_COGNIESL.md` | 1,102 | Vision document for the self-running system. Defines all agent roles. |
| `CogniESL/ROADMAP.md` | 198 | Master project plan with 4 parallel tracks. |
| `CogniESL/CLAUDE.md` | 241 | Behavioral guidelines + project specification for AI development. |

---

## 4. Database Schema — Complete

### Database: `cogniesl.db` (17 Tables)

All operations in `auth/db.py`. Schema is created/updated in `init_auth_db()` at app startup.

#### `users`
```
id                  TEXT    PRIMARY KEY
email               TEXT    UNIQUE NOT NULL
password_hash       TEXT    NOT NULL
created_at          TEXT    NOT NULL
subscription_tier   TEXT    NOT NULL DEFAULT 'free'
stripe_customer_id  TEXT    DEFAULT ''
```

#### `materials`
```
id                    TEXT    PRIMARY KEY
user_id               TEXT    NOT NULL → users.id
job_id                TEXT
project_name          TEXT    NOT NULL
grammar_point         TEXT    NOT NULL
l1_languages          TEXT    NOT NULL DEFAULT ''
age_group             TEXT    NOT NULL DEFAULT 'adults'
level                 TEXT    NOT NULL DEFAULT ''
formats               TEXT    NOT NULL DEFAULT ''
slide_count           INTEGER DEFAULT 0
pptx_path             TEXT
worksheet_pdf_path    TEXT
worksheet_docx_path   TEXT
activity_pdf_path     TEXT
activity_docx_path    TEXT
created_at            TEXT    NOT NULL
model_version         TEXT    DEFAULT ''
```

#### `generations`
```
id              TEXT    PRIMARY KEY
user_id         TEXT    NOT NULL → users.id
created_at      TEXT    NOT NULL
grammar_point   TEXT    NOT NULL DEFAULT ''
l1_languages    TEXT    NOT NULL DEFAULT ''
formats         TEXT    NOT NULL DEFAULT ''
level           TEXT    NOT NULL DEFAULT ''
age_group       TEXT    NOT NULL DEFAULT ''
cost_estimate   REAL    DEFAULT 0.0
model_version   TEXT    DEFAULT ''
cache_hit       INTEGER DEFAULT 0
job_id          TEXT    DEFAULT ''
```

#### `feedback`
```
id            TEXT    PRIMARY KEY
user_id       TEXT    NOT NULL DEFAULT ''
material_id   TEXT
job_id        TEXT
rating        TEXT    NOT NULL          -- 'perfect' | 'good' | 'issues'
tags          TEXT    DEFAULT ''       -- comma-separated
comment       TEXT    DEFAULT ''
source        TEXT    DEFAULT 'explicit'
created_at    TEXT    NOT NULL
reviewed      INTEGER DEFAULT 0
resolution    TEXT    DEFAULT ''
```

#### `events`
```
id            TEXT    PRIMARY KEY
user_id       TEXT    NOT NULL DEFAULT ''
event_type    TEXT    NOT NULL
metadata      TEXT    DEFAULT '{}'     -- JSON string
created_at    TEXT    NOT NULL
```

#### `password_reset_tokens`
```
token       TEXT    PRIMARY KEY
user_id     TEXT    NOT NULL
expires_at  TEXT    NOT NULL
used        INTEGER DEFAULT 0
```

#### `waitlist`
```
id          TEXT    PRIMARY KEY
email       TEXT    UNIQUE NOT NULL
created_at  TEXT    NOT NULL
source      TEXT    DEFAULT 'homepage'
```

#### `subscription_events`
```
id                    TEXT    PRIMARY KEY
user_id               TEXT    NOT NULL
stripe_event_id       TEXT    NOT NULL
event_type            TEXT    NOT NULL
subscription_status   TEXT    NOT NULL DEFAULT ''
new_tier              TEXT    NOT NULL DEFAULT ''
created_at            TEXT    NOT NULL
raw_json              TEXT    DEFAULT ''
```

#### `agent_actions` (NEW in Phase I-2)
```
id            TEXT    PRIMARY KEY
agent_name    TEXT    NOT NULL
action_type   TEXT    NOT NULL
description   TEXT    NOT NULL
status        TEXT    DEFAULT 'pending'  -- 'pending' | 'approved' | 'rejected'
marcos_notes  TEXT    DEFAULT ''
created_at    TEXT    NOT NULL
resolved_at   TEXT    DEFAULT ''
routed_to     TEXT    DEFAULT ''         -- Phase I-3: inter-agent routing
routed_at     TEXT    DEFAULT ''         -- Phase I-3: when routed
estimated_cost_usd REAL DEFAULT 0       -- Phase I-3: cost tracking
```

#### `daily_snapshots` (NEW in Phase I-2)
```
id                TEXT    PRIMARY KEY
snapshot_date     TEXT    NOT NULL
total_users       INTEGER DEFAULT 0
total_gens        INTEGER DEFAULT 0
total_cost        REAL    DEFAULT 0.0
active_users_7d   INTEGER DEFAULT 0
signups_today     INTEGER DEFAULT 0
created_at        TEXT    NOT NULL
```

#### `daily_digests` (NEW in Phase I-2)
```
id            TEXT    PRIMARY KEY
digest_date   TEXT    NOT NULL
content_json  TEXT    NOT NULL       -- full digest as JSON
sent          INTEGER DEFAULT 0
created_at    TEXT    NOT NULL
```

#### `orchestrator_runs` (NEW in Phase I-3)
```
id              TEXT    PRIMARY KEY
run_type        TEXT    NOT NULL       -- 'scheduled' | 'manual' | 'retry'
status          TEXT DEFAULT 'running' -- 'running' | 'completed' | 'failed' | 'paused'
started_at      TEXT    NOT NULL
completed_at    TEXT
agents_run      TEXT DEFAULT '[]'      -- JSON array of agent names
critical_alerts INTEGER DEFAULT 0
error_message   TEXT DEFAULT ''
```

#### `agent_health` (NEW in Phase I-3)
```
agent_name              TEXT    PRIMARY KEY
last_run_at             TEXT
last_success_at         TEXT
consecutive_failures    INTEGER DEFAULT 0
avg_runtime_seconds     REAL DEFAULT 0
total_runs              INTEGER DEFAULT 0
status                  TEXT DEFAULT 'unknown'  -- 'healthy' | 'degraded' | 'failing' | 'paused'
```

#### `agent_messages` (NEW in Phase I-3) — inter-agent routing log
```
id            TEXT    PRIMARY KEY
from_agent    TEXT    NOT NULL
to_agent      TEXT    NOT NULL
message_type  TEXT    NOT NULL        -- 'regenerate' | 'flag_content' | 'pause' | 'alert'
payload       TEXT DEFAULT '{}'       -- JSON blob
created_at    TEXT    NOT NULL
processed     INTEGER DEFAULT 0
processed_at  TEXT
```

#### `agent_costs` (NEW in Phase I-3) — per-action cost tracking
```
id              TEXT    PRIMARY KEY
agent_name      TEXT    NOT NULL
action_id       TEXT                  -- links to agent_actions.id
estimated_cost_usd REAL DEFAULT 0
tokens_input    INTEGER DEFAULT 0
tokens_output   INTEGER DEFAULT 0
model_used      TEXT DEFAULT ''
created_at      TEXT    NOT NULL
```

#### `critical_alerts` (NEW in Phase I-8)
```
id              TEXT    PRIMARY KEY
alert_type      TEXT    NOT NULL        -- 'error_spike' | 'zero_gen' | 'content_bug' | 'churn' | 'funnel'
severity        TEXT    NOT NULL        -- 'critical' | 'high'
description     TEXT    NOT NULL
details_json    TEXT DEFAULT '{}'       -- JSON blob
created_at      TEXT    NOT NULL
acknowledged    INTEGER DEFAULT 0
acknowledged_at TEXT
resolved        INTEGER DEFAULT 0
resolved_at     TEXT
marcos_notes    TEXT DEFAULT ''
```

#### `social_shares` (planned, not yet created)
```
id              TEXT    PRIMARY KEY
user_id         TEXT    NOT NULL
platform        TEXT    NOT NULL        -- 'x' | 'instagram' | 'facebook' | 'google_review' | 'referral'
testimonial_text TEXT DEFAULT ''
created_at      TEXT    NOT NULL
```

All operations in `auth/db.py`. Schema is created/updated in `init_auth_db()` at app startup.

#### `users`
```
id                  TEXT    PRIMARY KEY
email               TEXT    UNIQUE NOT NULL
password_hash       TEXT    NOT NULL
created_at          TEXT    NOT NULL
subscription_tier   TEXT    NOT NULL DEFAULT 'free'
stripe_customer_id  TEXT    DEFAULT ''
```

#### `materials`
```
id                    TEXT    PRIMARY KEY
user_id               TEXT    NOT NULL → users.id
job_id                TEXT
project_name          TEXT    NOT NULL
grammar_point         TEXT    NOT NULL
l1_languages          TEXT    NOT NULL DEFAULT ''
age_group             TEXT    NOT NULL DEFAULT 'adults'
level                 TEXT    NOT NULL DEFAULT ''
formats               TEXT    NOT NULL DEFAULT ''
slide_count           INTEGER DEFAULT 0
pptx_path             TEXT
worksheet_pdf_path    TEXT
worksheet_docx_path   TEXT
activity_pdf_path     TEXT
activity_docx_path    TEXT
created_at            TEXT    NOT NULL
model_version         TEXT    DEFAULT ''
```

#### `generations`
```
id              TEXT    PRIMARY KEY
user_id         TEXT    NOT NULL → users.id
created_at      TEXT    NOT NULL
grammar_point   TEXT    NOT NULL DEFAULT ''
l1_languages    TEXT    NOT NULL DEFAULT ''
formats         TEXT    NOT NULL DEFAULT ''
level           TEXT    NOT NULL DEFAULT ''
age_group       TEXT    NOT NULL DEFAULT ''
cost_estimate   REAL    DEFAULT 0.0
model_version   TEXT    DEFAULT ''
cache_hit       INTEGER DEFAULT 0
job_id          TEXT    DEFAULT ''
```

#### `feedback`
```
id            TEXT    PRIMARY KEY
user_id       TEXT    NOT NULL DEFAULT ''
material_id   TEXT
job_id        TEXT
rating        TEXT    NOT NULL          -- 'perfect' | 'good' | 'issues'
tags          TEXT    DEFAULT ''       -- comma-separated
comment       TEXT    DEFAULT ''
source        TEXT    DEFAULT 'explicit'
created_at    TEXT    NOT NULL
reviewed      INTEGER DEFAULT 0
resolution    TEXT    DEFAULT ''
```

#### `events`
```
id            TEXT    PRIMARY KEY
user_id       TEXT    NOT NULL DEFAULT ''
event_type    TEXT    NOT NULL
metadata      TEXT    DEFAULT '{}'     -- JSON string
created_at    TEXT    NOT NULL
```

#### `password_reset_tokens`
```
token       TEXT    PRIMARY KEY
user_id     TEXT    NOT NULL
expires_at  TEXT    NOT NULL
used        INTEGER DEFAULT 0
```

#### `waitlist`
```
id          TEXT    PRIMARY KEY
email       TEXT    UNIQUE NOT NULL
created_at  TEXT    NOT NULL
source      TEXT    DEFAULT 'homepage'
```

#### `subscription_events`
```
id                    TEXT    PRIMARY KEY
user_id               TEXT    NOT NULL
stripe_event_id       TEXT    NOT NULL
event_type            TEXT    NOT NULL
subscription_status   TEXT    NOT NULL DEFAULT ''
new_tier              TEXT    NOT NULL DEFAULT ''
created_at            TEXT    NOT NULL
raw_json              TEXT    DEFAULT ''
```

#### `agent_actions` (NEW)
```
id            TEXT    PRIMARY KEY
agent_name    TEXT    NOT NULL
action_type   TEXT    NOT NULL
description   TEXT    NOT NULL
status        TEXT    DEFAULT 'pending'  -- 'pending' | 'approved' | 'rejected'
marcos_notes  TEXT    DEFAULT ''
created_at    TEXT    NOT NULL
resolved_at   TEXT    DEFAULT ''
```

#### `daily_snapshots` (NEW)
```
id                TEXT    PRIMARY KEY
snapshot_date     TEXT    NOT NULL
total_users       INTEGER DEFAULT 0
total_gens        INTEGER DEFAULT 0
total_cost        REAL    DEFAULT 0.0
active_users_7d   INTEGER DEFAULT 0
signups_today     INTEGER DEFAULT 0
created_at        TEXT    NOT NULL
```

#### `daily_digests` (NEW)
```
id            TEXT    PRIMARY KEY
digest_date   TEXT    NOT NULL
content_json  TEXT    NOT NULL       -- full digest as JSON
sent          INTEGER DEFAULT 0
created_at    TEXT    NOT NULL
```

### Database: `jobs.db` (1 Table)

Operations in `agent/jobs.py`.

#### `jobs`
```
job_id          TEXT    PRIMARY KEY
status          TEXT    NOT NULL DEFAULT 'pending'
email           TEXT
user_id         TEXT
project_name    TEXT
grammar_point   TEXT
l1_languages    TEXT
age_group       TEXT
formats         TEXT                -- JSON array
file_paths      TEXT                -- JSON array
created_at      TEXT    NOT NULL
completed_at    TEXT
error           TEXT
```

### Indexes (NEW)
```sql
CREATE INDEX IF NOT EXISTS idx_generations_created ON generations(created_at)
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at)
CREATE INDEX IF NOT EXISTS idx_daily_snapshots_date ON daily_snapshots(snapshot_date)
```

### All DB Functions (18 New in auth/db.py)

| Function | File | Purpose | Called By |
|----------|------|---------|-----------|
| `resolve_feedback(feedback_id, resolution_text)` | db.py | Mark feedback reviewed + set resolution | API `POST /api/admin/feedback/{id}/resolve` |
| `get_user_activity(user_id)` | db.py | Full user profile: gens, mats, fb, events, subs | API `GET /api/admin/users/{id}` |
| `get_events_timeline(event_type, limit, offset)` | db.py | Recent events, optionally filtered | API `GET /api/admin/events` |
| `count_events_by_type(days)` | db.py | Count events by type over N days | API `GET /api/admin/events` |
| `get_engagement_stats()` | db.py | DAU/WAU/MAU + avg gens + one-and-done | API `GET /api/admin/engagement`, daily digest |
| `log_agent_action(agent_name, action_type, description)` | db.py | Insert agent action | report_writer.py, future agents |
| `list_agent_actions(status, agent_name, limit)` | db.py | Query agent actions with filters | API `GET /api/admin/agent-actions` |
| `resolve_agent_action(action_id, status, notes)` | db.py | Approve/reject agent action | API `POST /api/admin/agent-actions/{id}/resolve` |
| `get_agent_action_summary()` | db.py | Count by status and agent | API `GET /api/admin/agent-reports`, daily digest |
| `has_pending_action(agent_name, action_type)` | db.py | Check for duplicate proposals | Future agent scheduling |
| `take_daily_snapshot()` | db.py | Compute today's metrics, store once/day | API `GET /api/admin/daily-digest` |
| `get_daily_snapshots(days)` | db.py | Return last N days of snapshots | API `GET /api/admin/trends` |
| `compute_churn_risk_scores()` | db.py | Score paying users for churn risk | API `GET /api/admin/churn-risk`, daily digest |
| `get_engagement_funnel()` | db.py | Signup→Activation→Engagement→Power→Paid | API `GET /api/admin/funnel` |
| `get_content_quality_signals()` | db.py | Issue rates by grammar + L1 | API `GET /api/admin/content-quality`, daily digest |
| `save_daily_digest(content_json)` | db.py | Store digest for history | (future: email function) |
| `get_latest_digest()` | db.py | Retrieve most recent digest | (future: archive page) |

---

## 5. API Reference — All Endpoints

### Authentication Pattern

**User endpoints** use JWT bearer token (from `Authorization: Bearer <token>` header). Created at login, stored in JWT.

**Admin endpoints** use cookie-based session. Cookie name: `admin_session`. Set by `POST /admin/login`. Value: SHA256 hash of `ADMIN_PASSWORD` env var.

```python
# Every admin endpoint starts with this pattern:
if not _require_admin(request):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)
```

### Admin Endpoints (17 routes)

| # | Method | Endpoint | Response | Description |
|---|--------|----------|----------|-------------|
| 1 | GET | `/admin` | HTML | Serve dashboard (or login form if unauthenticated) |
| 2 | POST | `/admin/login` | JSON `{ok: true}` | Authenticate, set cookie |
| 3 | GET | `/api/admin/overview` | JSON | Pulse, monthly, users, top grammar/L1, failed jobs |
| 4 | GET | `/api/admin/users` | JSON | Paginated user list (query: `page`, `per_page`) |
| 5 | GET | `/api/admin/feedback` | JSON | Feedback list (query: `limit`, `unreviewed`) |
| 6 | POST | `/api/admin/feedback/{id}/resolve` | JSON `{ok: true}` | Body: `{resolution: "text"}`. Mark reviewed. |
| 7 | GET | `/api/admin/users/{user_id}` | JSON | Full user activity profile |
| 8 | GET | `/api/admin/events` | JSON | Event timeline (query: `event_type`, `limit`, `offset`) |
| 9 | GET | `/api/admin/engagement` | JSON | DAU/WAU/MAU, avg gens, one-and-done |
| 10 | GET | `/api/admin/agent-actions` | JSON | Agent actions (query: `status`, `agent_name`, `limit`) |
| 11 | POST | `/api/admin/agent-actions/{id}/resolve` | JSON `{ok: true}` | Body: `{status: "approved"|"rejected", notes: ""}` |
| 12 | GET | `/api/admin/agent-reports` | JSON | Summary + pending items |
| 13 | GET | `/api/admin/churn-risk` | JSON | At-risk paying users with scores |
| 14 | GET | `/api/admin/funnel` | JSON | Engagement funnel stages |
| 15 | GET | `/api/admin/content-quality` | JSON | Issue rates by grammar/L1, top issue tags |
| 16 | GET | `/api/admin/trends` | JSON | Daily snapshots (query: `days`, default 30) |
| 17 | GET | `/api/admin/daily-digest` | JSON | Consolidated CEO digest |

### Complete Request/Response Examples

#### `GET /api/admin/users/{user_id}`

**Response:**
```json
{
  "user": {
    "id": "abc-123",
    "email": "teacher@example.com",
    "subscription_tier": "pro",
    "created_at": "2026-05-01T10:00:00+00:00"
  },
  "stats": {
    "total_generations": 12,
    "total_materials": 8,
    "total_feedback": 3,
    "total_cost": 4.52,
    "last_seen": "2026-05-24T14:30:00+00:00"
  },
  "generations": [{ "grammar_point": "present_simple", "cost_estimate": 0.35, ... }],
  "materials": [{ "project_name": "...", ... }],
  "feedback": [{ "rating": "issues", "tags": "wrong_level", ... }],
  "events": [{ "event_type": "generation_completed", ... }],
  "subscription_history": [{ "event_type": "customer.subscription.created", ... }]
}
```

#### `GET /api/admin/daily-digest`

**Response:**
```json
{
  "date": "2026-05-24",
  "generated_at": "2026-05-24T08:00:00+00:00",
  "at_a_glance": {
    "gens_today": 6,
    "signups_today": 2,
    "active_users_7d": 15,
    "mrr_usd": 84.00,
    "api_cost_today_usd": 1.80,
    "api_cost_month_usd": 62.40
  },
  "actions_needed": [
    {
      "type": "churn_risk",
      "priority": "high",
      "summary": "2 paying users at risk (1 critical)"
    }
  ],
  "agent_status": {
    "pending_approvals": 3,
    "approved_last_7d": 5,
    "rejected_last_7d": 1
  },
  "system_health": {
    "failed_jobs_7d": 1,
    "content_issue_rate_pct": 8.3,
    "unreviewed_feedback": 4,
    "users_at_risk": 2
  }
}
```

#### `GET /api/admin/churn-risk`

**Response:**
```json
{
  "at_risk_users": [
    {
      "user_id": "abc-123",
      "email": "teacher@example.com",
      "tier": "pro",
      "risk_score": 78,
      "risk_level": "high",
      "reasons": [
        "No activity in 18 days",
        "Declining usage: 5→1 gens/week"
      ],
      "last_generation": "2026-05-06T10:00:00+00:00",
      "total_gens": 14
    }
  ]
}
```

#### `POST /api/admin/agent-actions/{id}/resolve`

**Request body:**
```json
{
  "status": "approved",
  "notes": "Looks good, deploying now"
}
```

**Response:** `{"ok": true}`

---

## 6. Dashboard UI Specification

### File: `admin/dashboard.html`
**Size:** 921 lines (HTML + CSS + JS, single self-contained file)

### Tab Structure

```
┌──────────────────────────────────────────────────────────────┐
│ ⚡ CogniESL Founder Dashboard          [Refresh] [Sign out]  │
├──────────────────────────────────────────────────────────────┤
│ 📊 Digest │ 📈 Details │ 🤖 Agents (badge) │ 🧠 Intelligence│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                    [Active Tab Content]                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Tab 1: 📊 Digest (CEO Daily Digest)

Three zones stacked vertically:

1. **At a Glance** (2-column grid of 6 metric cards):
   - Generations Today · Signups Today · Active (7d) · MRR · Cost Today · Cost Month

2. **Actions Needed** (list of priority items):
   - Each item: priority dot (red/amber) + icon + summary text
   - Empty state: green "✅ All clear!"

3. **System Health** (inline badges):
   - Agent pending · Approved (7d) · Rejected (7d) · Failed jobs · Unreviewed feedback · Users at risk · Content issue rate

**Auto-refresh:** Every 5 minutes (`setInterval(loadAll, 300000)`)

**Badge:** Tab shows red badge with count of `actions_needed.length`

---

### Tab 2: 📈 Details (Original + Enhancements)

Sections in order:

| Section | Description | Source Endpoint |
|---------|-------------|-----------------|
| **Live Pulse** | 6 cards: gens today, active jobs, signups, cost today, gens month, MRR | `/api/admin/overview` |
| **Subscriptions by Tier** | Free/Pro/Founding counts + total + waitlist | `/api/admin/overview` |
| **Engagement Pulse** | DAU/WAU/MAU grid + zero-gens + one-and-done | `/api/admin/engagement` |
| **Founding Member Slots** | Progress bar, warning when ≤10 remain | `/api/admin/overview` |
| **Error Monitoring** | Failed jobs table (or green checkmark) | `/api/admin/overview` |
| **Top Grammar Points** | Ranked bar chart, top 10 | `/api/admin/overview` |
| **Top Native Languages** | Ranked bar chart, top 10 | `/api/admin/overview` |
| **30-Day Trends** | 3 sparkline charts (signups, gens, cost) | `/api/admin/trends` |
| **Feedback Center** | Summary stats + toggle (Unreviewed/All) + resolve table | `/api/admin/feedback` |
| **User List** | Paginated table, click email → drill-down modal | `/api/admin/users` |

---

### Tab 3: 🤖 Agents (Agent Command Center)

| Section | Description |
|---------|-------------|
| **Pending Actions** | Each item: agent badge + description + time + ✓/✗ buttons |
| **Activity Feed** | Chronological list of all agent actions, color-coded by status |

**Badge:** Shows count of pending actions

---

### Tab 4: 🧠 Intelligence (Predictive Analytics)

| Section | Visualization | Source |
|---------|---------------|--------|
| **Engagement Funnel** | Horizontal CSS bars, width = conversion % | `/api/admin/funnel` |
| **Churn Risk Alerts** | Cards: email, tier, score, reasons, last gen | `/api/admin/churn-risk` |
| **Content Quality** | Heatmap tables: grammar + L1 issue rates (green/amber/red cells) + issue tags | `/api/admin/content-quality` |

---

### User Drill-Down Modal

Triggered by clicking any email in the User List table. Opens an overlay modal with:

- **Header:** User email + close button
- **Stats row:** Tier, join date, last seen, total gens/materials/feedback/cost
- **4 tabs:** Generations | Materials | Feedback | Events
- Each tab shows a data table with relevant columns

---

### CSS Classes (Key Reference)

**Semantic colors:**
```
.green  → --green  → good/positive
.red    → --red    → problem/critical
.amber  → --amber  → warning/caution
.teal   → --teal   → information/neutral
```

**Agent badges:**
```
.agent-qa         → green
.agent-curator    → purple
.agent-cmo        → blue
.agent-cfo        → green
.agent-secretary  → amber
```

**Quality cells:**
```
.q-green  → issue rate < 5%
.q-amber  → issue rate 5-15%
.q-red    → issue rate > 15%
```

**Churn cards:**
```
.churn-critical  → red left border + red bg
.churn-high      → amber left border + amber bg
.churn-medium    → blue left border + blue bg
```

---

### Dashboard JavaScript API

| Function | Purpose | Called When |
|----------|---------|-------------|
| `loadAll()` | Master loader — fetches all tabs | Page load, refresh button, auto-refresh |
| `loadDigest()` | Fetch + render CEO digest | `loadAll()`, Digest tab active |
| `loadOverview()` | Fetch + render Live Pulse + Tiers + Founding + Errors + Grammar + L1 | `loadAll()` |
| `loadEngagement()` | Fetch + render engagement stats | `loadAll()` |
| `loadTrends()` | Fetch + render sparklines | `loadAll()` |
| `loadFeedback()` | Fetch + render feedback center | `loadAll()`, toggle change |
| `loadUsers(page)` | Fetch + render paginated user list | `loadAll()`, pagination click |
| `loadAgents()` | Fetch + render agent queue + feed | Agents tab click |
| `loadIntelligence()` | Fetch + render funnel + churn + quality | Intelligence tab click |
| `loadFunnel()` | Fetch + render funnel | `loadIntelligence()` |
| `loadChurnRisk()` | Fetch + render churn cards | `loadIntelligence()` |
| `loadContentQuality()` | Fetch + render quality heatmap | `loadIntelligence()` |
| `openUserModal(userId, email)` | Open drill-down modal | Email click in user list |
| `closeModal()` | Close drill-down modal | Close button, click outside, Escape |
| `switchTab(name)` | Switch tab (digest/details/agents/intelligence) | Tab click |
| `switchModalTab(name)` | Switch modal tab (gens/mats/fb/evts) | Modal tab click |
| `showFeedback(filter)` | Toggle feedback list (unreviewed/all) | Toggle button click |
| `resolveFeedback(id)` | Resolve feedback with prompt | Resolve button click |
| `resolveAgent(id, status)` | Approve/reject agent action | ✓/✗ button click |

---

## 7. What Was Built Per Phase

### Phase A: Feedback Center + User Intelligence
*Goal: Make feedback actionable and give visibility into individual user behavior.*

**Database (auth/db.py):**
- [x] `agent_actions` table (also serves Phase B)
- [x] `resolve_feedback()` function
- [x] `get_user_activity()` function — full profile query
- [x] `get_events_timeline()` function
- [x] `count_events_by_type()` function
- [x] `get_engagement_stats()` function — DAU/WAU/MAU + one-and-done

**API (server.py):**
- [x] `POST /api/admin/feedback/{id}/resolve`
- [x] `GET /api/admin/users/{user_id}`
- [x] `GET /api/admin/events`
- [x] `GET /api/admin/engagement`

**Dashboard (admin/dashboard.html):**
- [x] Feedback Center section with resolve workflow
- [x] Engagement Pulse cards
- [x] User drill-down modal with 4 tabs
- [x] Clickable email addresses in user list

**New API endpoints: 4** | **New DB functions: 5** | **Effort: ~5 hours**

---

### Phase B: Agent Infrastructure
*Goal: Foundation for self-running system — agent action logging + approval workflow.*

**Database (auth/db.py):**
- [x] `log_agent_action()` function
- [x] `list_agent_actions()` function
- [x] `resolve_agent_action()` function
- [x] `get_agent_action_summary()` function
- [x] `has_pending_action()` function — duplicate prevention

**API (server.py):**
- [x] `GET /api/admin/agent-actions`
- [x] `POST /api/admin/agent-actions/{id}/resolve`
- [x] `GET /api/admin/agent-reports`

**Dashboard (admin/dashboard.html):**
- [x] Agents tab with pending queue + approve/reject buttons
- [x] Agent activity feed with status color coding
- [x] Tab badge showing pending count

**New file (agent/):**
- [x] `report_writer.py` — extension point for agent reports. `generate_health_report()` works today (pure data, no AI). Stubs for QA, CMO, CFO, Curator, Secretary raise `NotImplementedError`.

**New API endpoints: 3** | **New DB functions: 5** | **New file: 1** | **Effort: ~5 hours**

---

### Phase C: Intelligence Layer
*Goal: Anomaly detection, churn risk, engagement funnel, content quality signals.*

**Database (auth/db.py):**
- [x] `daily_snapshots` table + indexes
- [x] `take_daily_snapshot()` — idempotent (runs once/day)
- [x] `get_daily_snapshots(days)`
- [x] `compute_churn_risk_scores()` — scoring algorithm:
  - Days since last generation (weight 40%)
  - Declining usage trend (weight 30%)
  - Approaching tier limit (weight 20%)
  - Unresolved "issues" feedback (weight 10%)
  - Thresholds: critical ≥60, high ≥40, medium ≥20
- [x] `get_engagement_funnel()` — 5-stage funnel
- [x] `get_content_quality_signals()` — issue rates by grammar/L1 + top tags

**API (server.py):**
- [x] `GET /api/admin/churn-risk`
- [x] `GET /api/admin/funnel`
- [x] `GET /api/admin/content-quality`
- [x] `GET /api/admin/trends`

**Dashboard (admin/dashboard.html):**
- [x] Intelligence tab with engagement funnel (CSS bar visualization)
- [x] Churn risk alert cards (color-coded by severity)
- [x] Content quality heatmap (grammar + L1 tables, green/amber/red cells)
- [x] 3 trend sparklines in Details tab

**New API endpoints: 4** | **New DB functions: 5** | **New tables: 1** | **Effort: ~8 hours**

---

### Phase D: CEO Daily Digest
*Goal: One consolidated view — everything needing attention in under 60 seconds.*

**Database (auth/db.py):**
- [x] `daily_digests` table
- [x] `save_daily_digest()` function
- [x] `get_latest_digest()` function

**API (server.py):**
- [x] `GET /api/admin/daily-digest` — aggregates all data sources into single response

**Dashboard (admin/dashboard.html):**
- [x] Digest tab as default view (renders first)
- [x] 3-zone digest card: At a Glance + Actions Needed + System Health
- [x] Tab badge showing action item count
- [x] Auto-refresh every 5 minutes
- [x] Tab navigation system (Digest / Details / Agents / Intelligence)
- [x] All original dashboard sections preserved in Details tab

**Email extension (agent/email_sender.py):**
- [x] `send_daily_digest_email(digest_data)` — plain-text daily email via Resend. Requires `FOUNDER_EMAIL` env var.

**New API endpoints: 1** | **New DB functions: 2** | **New email function: 1** | **Effort: ~7 hours**

---

### Summary Metrics

| Metric | Count |
|--------|-------|
| **New database tables** | 3 (`agent_actions`, `daily_snapshots`, `daily_digests`) |
| **New database indexes** | 3 |
| **New DB functions** | 18 |
| **New API endpoints** | 13 |
| **New dashboard sections** | 8 |
| **New dashboard tabs** | 4 |
| **New files created** | 1 (`report_writer.py`) |
| **Files extended** | 1 (`email_sender.py`) |
| **Total new lines of code** | ~1,800 |
| **Total effort** | ~25 hours |

---

## 8. Debugging Guide

### If the Dashboard Doesn't Load

1. **Check admin password is set:**
   ```bash
   echo $ADMIN_PASSWORD  # Must be non-empty
   ```
2. **Login manually:** Navigate to `/admin`, enter password
3. **Check server logs:** Look for 401 errors on `/api/admin/*` endpoints

### If Data Is Missing

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| All metrics show "—" or 0 | DB file empty / app not yet used | Normal for fresh deploy — data accumulates with use |
| Trends show "No trend data yet" | `daily_snapshots` table is empty | Snapshots are created by the daily-digest endpoint (runs once per day). Call it manually: `curl -b "admin_session=<hash>" /api/admin/daily-digest` |
| Failed jobs always empty | `jobs.db` not found or in different path | The code checks both `agent/jobs.db` and `jobs.db` in root. Make sure it's deployed. |
| Churn risk always empty | No paying users yet | Only Pro/Founding users are scored |
| Content quality shows no data | No feedback yet | Requires feedback submissions with material_id |
| Agent badge shows wrong count | Pending items may have been resolved | Click Agents tab to verify |

### Database Inspection

```bash
# Connect to SQLite
sqlite3 cogniesl.db

# Check table exists
.tables

# Check row counts
SELECT 'users' as tbl, COUNT(*) FROM users
UNION ALL SELECT 'generations', COUNT(*) FROM generations
UNION ALL SELECT 'feedback', COUNT(*) FROM feedback
UNION ALL SELECT 'events', COUNT(*) FROM events
UNION ALL SELECT 'agent_actions', COUNT(*) FROM agent_actions
UNION ALL SELECT 'daily_snapshots', COUNT(*) FROM daily_snapshots;

# Check recent feedback
SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10;

# Check agent actions
SELECT agent_name, action_type, status, description FROM agent_actions ORDER BY created_at DESC LIMIT 10;

# Check daily snapshots
SELECT * FROM daily_snapshots ORDER BY snapshot_date DESC LIMIT 5;
```

### API Testing

```bash
# Get admin session hash (SHA256 of ADMIN_PASSWORD)
echo -n "your-password" | sha256sum

# Test any admin endpoint
curl -b "admin_session=<sha256-hash>" https://your-app.up.railway.app/api/admin/daily-digest | python3 -m json.tool

# Test feedback resolution
curl -X POST -b "admin_session=<hash>" \
  -H "Content-Type: application/json" \
  -d '{"resolution": "Fixed by updating grammar YAML"}' \
  https://your-app.up.railway.app/api/admin/feedback/<feedback-id>/resolve

# Test agent action resolution
curl -X POST -b "admin_session=<hash>" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved", "notes": "Good fix"}' \
  https://your-app.up.railway.app/api/admin/agent-actions/<action-id>/resolve
```

### Common Errors

**"Unauthorized" (401):**
- `ADMIN_PASSWORD` env var not set → `_ADMIN_PW_HASH` equals empty hash → `_require_admin()` always False
- Cookie expired (8 hours) → Re-login at `/admin`
- Cookie not sent → Ensure `credentials: 'same-origin'` is in fetch calls (it is)

**"Feedback not found" (404):**
- Resolve endpoint can't find the feedback ID → Check `SELECT id FROM feedback;`

**"Column not found":**
- DB migration didn't run → Restart the app (migrations run in `init_auth_db()` at startup)
- For existing deployments: the `CREATE TABLE IF NOT EXISTS` and `ALTER TABLE` blocks handle this automatically

**Dashboard shows old data:**
- Click Refresh button or wait for 5-minute auto-refresh
- Check that timestamps update correctly

---

## 9. Future Implementation Guide

### How to Add a New Admin API Endpoint

1. **Add DB function** in `auth/db.py`:
```python
def get_my_new_metric() -> dict:
    with _conn() as conn:
        row = conn.execute("SELECT ...").fetchone()
    return dict(row) if row else {}
```

2. **Add API endpoint** in `server.py` (before the Stripe section):
```python
@app.get("/api/admin/my-new-metric")
async def api_admin_my_new_metric(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse(_auth_db.get_my_new_metric())
```

3. **Add to dashboard** in `admin/dashboard.html`:
   - Add a `loadMyNewMetric()` function in the `<script>` section
   - Call it from `loadAll()` or the relevant tab loader
   - Add HTML section with an id, populate it in the JS function

### How to Add a New Agent Type

1. **Uncomment the stub** in `agent/report_writer.py`:
```python
def generate_qa_report():
    """QA Agent: Analyze failed jobs, audit logs, error patterns."""
    # Read failed jobs from jobs.db
    # Analyze patterns
    # Create agent_action with findings
    raise NotImplementedError("QA Agent report — build in Phase I-3")  # Remove this
```

2. **Implement the report** by querying data from `auth/db.py` and `agent/jobs.py`, then calling `_log_action("QA", "report", description)`.

3. **Wire to scheduler** — create a scheduled task (cron or background thread) that calls `report_writer.generate_qa_report()` on a schedule.

### How to Enable the Daily Digest Email

1. Add `FOUNDER_EMAIL=your@email.com` to Railway env vars
2. Add `RESEND_API_KEY=...` (already present if email works)
3. The email function exists in `agent/email_sender.py` but is **not yet wired to a scheduler**. When ready:
   ```python
   # In a scheduled task or endpoint:
   from agent.email_sender import send_daily_digest_email
   from agent.report_writer import generate_health_report
   import json
   
   # Get digest data (or call the API endpoint)
   digest_data = {...}  # from /api/admin/daily-digest response
   send_daily_digest_email(digest_data)
   ```

### How to Add Event Tracking for New Actions

```python
from auth import db as auth_db
import json

# Anywhere in server.py after an action:
auth_db.log_event("generation_completed", user_id=str(user.id), metadata=json.dumps({
    "grammar_point": grammar,
    "cost": cost_estimate
}))
```

### How to Add a New Dashboard Tab

1. Add tab button in HTML:
```html
<div class="tab" onclick="switchTab('newtab')" id="tab-newtab">🔔 New Tab</div>
```

2. Add content container:
```html
<div class="tab-content" id="content-newtab">
  <!-- sections here -->
</div>
```

3. Add `loadNewTab()` to the JS `loadAll()` function and switch handler.

---

## 10. Environment & Deployment Notes

### Required Environment Variables

| Variable | Required For | Example |
|----------|-------------|---------|
| `ADMIN_PASSWORD` | Admin dashboard access | `my-secret-pw` |
| `FOUNDER_EMAIL` | Daily digest email | `marcos@cogniesL.com` |
| `RESEND_API_KEY` | Email delivery | `re_xxxxxxxx` |
| `JWT_SECRET_KEY` | User auth tokens | `random-secret-key` |
| `STRIPE_SECRET_KEY` | Billing | `sk_live_xxx` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhooks | `whsec_xxx` |
| `OPENROUTER_API_KEY` | AI model access | `sk-or-v1-xxx` |
| `COGNIESL_DATA_DIR` | Persistent data (Railway Volume) | `/app/data` |
| `COGNIESL_BASE_URL` | Links in emails | `https://cogniesl.com` |
| `FOUNDING_MEMBER_SLOTS_TOTAL` | Founding tier cap | `100` |

### Railway Deployment Checklist

| Step | Status |
|------|--------|
| Attach Railway Volume: `cogniesl` service → Volumes → Add → mount path `/app/data` | ⬜ Marcos |
| Run: `railway up` | ⬜ Marcos |
| Fix Stripe price IDs in Railway env vars | ⬜ Marcos |
| Add `FOUNDER_EMAIL` to Railway env vars | ⬜ Marcos |
| Test generation end-to-end on Railway | ⬜ Marcos |
| Test Stripe checkout (card `4242 4242 4242 4242`) | ⬜ Marcos |
| Open `/admin`, verify Founder Dashboard shows real data | ⬜ Marcos |
| Verify all tabs work: Digest, Details, Agents, Intelligence | ⬜ Marcos |
| Test feedback submission → appears in dashboard | ⬜ Marcos |

### Database Migration Behavior

All schema changes are **automatic and additive**. When the app starts:

1. `init_auth_db()` runs
2. `CREATE TABLE IF NOT EXISTS` — creates any missing tables
3. `ALTER TABLE ... ADD COLUMN` — wrapped in try/except, silently skips existing columns
4. `CREATE INDEX IF NOT EXISTS` — creates missing indexes

**No manual migration needed.** Existing data is never modified or deleted by schema changes.

### File Encoding Notes

- `dashboard.html` — Pure ASCII/UTF-8, no special characters that would cause encoding issues
- All Python files — UTF-8, standard encoding
- Database files — SQLite binary format

---

## Appendix A: Churn Risk Algorithm Detail

The churn risk score (0-100) for paying users (Pro/Founding) is computed as follows:

```python
score = 0
reasons = []

# Factor 1: Days since last generation (40% weight)
if last_gen_date:
    days_inactive = (now - last_gen_date).days
    if days_inactive > 14:
        score += min(40, days_inactive)
else:
    score += 30  # Never generated

# Factor 2: Declining usage trend (30% weight)
if prev_week_gens > 0 and curr_week_gens < prev_week_gens:
    score += 30

# Factor 3: Approaching tier limit (20% weight)
if total_gens >= tier_limit * 0.8:
    score += 20

# Factor 4: Unresolved "issues" feedback (10% weight)
if unreviewed_issues_count > 0:
    score += 10
```

Risk levels: **critical** (≥60), **high** (≥40), **medium** (≥20), **low** (<20). Only medium+ are shown in the dashboard.

---

## Appendix B: Session Management

### Admin Sessions
- **Mechanism:** Cookie-based (`admin_session`)
- **Hash:** SHA256 of `ADMIN_PASSWORD` env var
- **Timeout:** 8 hours (`max_age=28800`)
- **Security flags:** `httponly=True`, `samesite="strict"`
- **Comparison:** Uses `hmac.compare_digest()` (constant-time, timing-attack resistant)

### User Sessions (JWT)
- **Mechanism:** Bearer token in `Authorization` header
- **Algorithm:** HS256 (HMAC-SHA256)
- **Secret:** `JWT_SECRET_KEY` env var
- **Payload:** `{sub: user_id, iat: timestamp}`

---

## Appendix C: Database Connection Pattern

All database access in `auth/db.py` follows this pattern:

```python
def some_function(params):
    with _conn() as conn:
        # conn is sqlite3.Connection with row_factory = sqlite3.Row
        row = conn.execute("SELECT ...", (params,)).fetchall()
    return [dict(r) for r in row]
```

Key points:
- `_conn()` returns a connection with `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON`
- `sqlite3.Row` factory allows both `row["column"]` and `row[0]` access
- `with _conn() as conn` auto-commits on success, auto-rollback on exception
- For explicit commit (INSERT/UPDATE), call `conn.commit()` inside the block

---

*This document is the complete technical reference for the CogniESL Admin Dashboard system. For the product vision and self-running architecture, see `docs/SELF_RUNNING_COGNIESL.md`. For the project plan, see `ROADMAP.md`.*
