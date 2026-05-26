# CogniESL: Founder Dashboard
**Purpose:** A private, password-protected dashboard at `/admin` that gives Marcos complete visibility into the business  
**Last updated:** 2026-05-24  
**Status: ✅ Built. Test by visiting /admin and entering ADMIN_PASSWORD.**

---

## Overview

The founder dashboard is a single-page interface accessible only to you. It aggregates data from the SQLite databases, the file system, Railway usage logs, and optionally Stripe and Plausible. At a glance, you should be able to answer: Is the business healthy? Is the product being used? Am I making or losing money? Where are things breaking?

This is not a reporting tool that runs nightly — it is a live view that refreshes each time you open it, so you always see the current state.

---

## How to Build It

The dashboard is a protected route in the existing FastAPI server. Add a `ADMIN_PASSWORD` environment variable. A simple middleware checks for a cookie `admin_session=<hash>` and redirects to a login form if missing. Once logged in, the dashboard page calls internal API endpoints that read directly from the databases.

No external service is required. The data already exists — it just needs to be surfaced.

```
GET  /admin                → login form or dashboard page
POST /admin/login           → sets admin_session cookie, redirects to /admin
GET  /api/admin/overview    → all metrics in one JSON payload
GET  /api/admin/users       → paginated user list
GET  /api/admin/generations → generation log with costs
GET  /api/admin/errors      → recent errors from the job log
```

All `/api/admin/*` endpoints require the admin cookie. Never expose them without authentication.

---

## Dashboard Sections

---

### Section 1 — Live Pulse (Top of the Page)
Four large number cards. Updated on every page load.

**Today's Generations**: How many generation jobs have been created today. A healthy day is any number > 0. If you see 0 for two days in a row, something is broken.

**Active Jobs Right Now**: Count of jobs in `running` state. If this is 0 and the queue is empty, the server is idle. If it's been > 60 minutes with the same job still `running`, something is stuck.

**New Signups Today**: Count of user rows with `created_at >= today`. Your acquisition signal.

**API Cost Today (Estimated)**: Estimated cost based on today's completed generations. Calculation: sum the `cost_estimate` column from the generations table for today. This is the burn number — the money leaving your account before any revenue arrives.

---

### Section 2 — Revenue & Subscriptions

**MRR (Monthly Recurring Revenue)**: Count of users with `subscription_tier = 'pro'`, multiplied by the blended average ($10.50/month). This is a proxy until Stripe is integrated — once Stripe is live, pull actual MRR from the Stripe API.

**Subscriber Count by Tier**:
- Free: [N users]
- Pro Monthly: [N users at $12/month]
- Pro Annual: [N users at $9/month]
- Founding Member: [N users at $7/month — permanent lock]
- School: [N accounts — manual tracking initially]

**Founding Member Slots**: Out of 100 total. Shows "47 / 100 used — 53 remaining." When this hits 100, it should auto-disable the founding member checkout link and alert you.

**Free → Pro Conversion Rate**: (Pro users created in last 30 days) / (Free users created in last 30 days). Industry benchmark is 2–5%. If yours is below 1%, the product or the pricing page needs work. If it's above 8%, you're leaving money on the table with too low pricing.

**Churn This Month**: Count of users who downgraded from Pro to Free (or cancelled). Requires a `subscription_history` table or a Stripe webhook log. Target: below 5% monthly.

**ARPU (Average Revenue Per User)**: MRR / total subscribers. Tells you whether your plan mix is working or if too many people are on the cheap annual plan.

---

### Section 3 — Usage & Generation Metrics

**Total Generations (All Time)**: Every generation job ever completed.

**Generations This Month**: Current month only. Compare to last month to see growth.

**Average Generations Per User Per Month**: Total monthly generations / active monthly users. If this is above 15, your Pro tier soft cap is being tested. If it's below 5, teachers aren't getting enough value from the product.

**Most Generated Grammar Points (Top 10)**: A ranked list showing which grammar topics are generating the most demand. This directly tells you which ones to prioritize for the Master Repository (Phase 8). Example:
```
1. Present Simple        — 234 generations
2. Past Simple           — 187 generations
3. Present Perfect       — 156 generations
4. Present Continuous    — 98 generations
5. Past Continuous       — 67 generations
```

**Most Requested L1 Languages (Top 10)**: Same concept for native languages. Tells you which interference files are being used most. Example:
```
1. Spanish               — 312 generations
2. Mandarin              — 189 generations
3. Brazilian Portuguese  — 134 generations
4. French                — 98 generations
5. Arabic                — 76 generations
```

**Format Distribution**: What percentage of generations include each format:
- Slides only: 45%
- Slides + Worksheet: 35%
- All 3 formats: 20%

**Generation Success Rate**: Completed / (Completed + Error). If this drops below 95%, the generation pipeline is breaking. Show the last 7 days as a sparkline.

**Average Generation Time**: Time between job creation and job completion, in minutes. Baseline is ~20–40 minutes. If this is rising, the agent is slowing down (model performance issue, context overflow, or TPM rate limiting).

---

### Section 4 — Cost & Margin Tracking

**Estimated API Cost This Month**: Sum of `cost_estimate` from the generations table, current month. This is your biggest variable expense.

**Estimated Gross Profit This Month**: MRR - API costs - fixed costs ($50 Railway, $0 Resend under 3k emails). If this number is negative (which it will be pre-Phase 8), show it in red with the label "Investing phase — normal for this stage."

**Cost Per Generation (30-day rolling average)**: Sum of costs / count of completions. Target: below $1.50 until Phase 8, then below $0.40 after cache hits dominate.

**Cost Per Subscriber (Monthly)**: Total API cost / number of active subscribers. Tells you how much each subscriber is "costing" you in API fees. If a subscriber generates 20 things at $1.50 each, they cost $30/month to serve but you're only charging $12. This is expected pre-Phase 8.

**Cache Hit Rate** (once Phase 8 is built): What percentage of generation requests were served from the Master Repository without calling the LLM. Target: 70%+ within 30 days of Phase 8 launch. This single metric tells you whether Phase 8 is working.

**Monthly Cost by Model**: If you ever use different models for different tasks (e.g., Haiku for orchestration, GPT-4.1 for HTML writing), break down costs by model. Tells you which model is your biggest expense and whether the split is optimized.

---

### Section 5 — Traffic & Acquisition

**Website Visitors (Last 30 Days)**: From Plausible Analytics (already installed). Show total unique visitors and page views. Call the Plausible API from the admin endpoint.

**Top Traffic Sources**: Where visitors are coming from — direct, organic search, Reddit, social, referrals. Copy this directly from the Plausible dashboard API. Tells you which acquisition channels are working.

**Waitlist Signups (All Time and This Month)**: Count of rows in the `waitlist` table (once the email capture is wired up). Your pipeline of future paid users.

**Registration Rate**: Website visitors → registrations. If 1,000 people visited and 20 registered, that's 2%. Industry benchmark for tools like this is 1–3%.

**Activation Rate**: Registrations → first generation. If 20 registered and 12 generated something, that's 60% activation. If this drops below 40%, the onboarding (the chat interview) is losing people before they see value.

**Time to First Generation**: Average minutes between user registration and their first generation job. If this is over 30 minutes, teachers are confused. Target: under 10 minutes.

---

### Section 6 — User Activity

**Daily Active Users (Last 30 Days)**: A simple bar chart. Each bar is one day. Height = distinct users who made at least one chat request. Shows whether you have a daily-use product or a weekly-use product (ESL teachers likely fall into "generate once a week for the next class" — that's fine, weekly active is the right metric for ESL).

**User Retention (Cohort Table)**: For each month a cohort of users signed up, what percentage were still active 1, 2, 3 months later. This is the most important product health metric. A healthy retention curve for an ESL tool might look like: Month 1: 60%, Month 2: 40%, Month 3: 35% (then flattens). If it drops to 10% by Month 2, teachers are trying the product and walking away.

**Top Users by Generations (All Time)**: A list of your 20 most engaged users with their generation count, account tier, and join date. These are your superfans. If any are on the Free tier with 50+ generations, reach out personally — they're your best Pro conversion candidates. If any are Pro with 100+ generations, they're getting massive value and are testimonial candidates.

**Users Who Generated Once, Never Returned**: A count of users who did exactly 1 generation and have not been seen since. This is your "tried it, didn't stick" number. High-value insight: if this group is large, the first generation experience isn't compelling enough. A/B test: send these users an email 3 days after their first generation with the subject "What did you think?"

---

### Section 7 — Error Monitoring

**Failed Jobs (Last 7 Days)**: List of generation jobs that ended in `error` status. For each: job_id, user email (if auth'd), grammar_point, L1, error message, timestamp. This is your bug tracker. If you see the same error appearing 5 times in one day, it's a production bug.

**Most Common Error Messages**: Grouped by error type. "rate_limit_exceeded" means the OpenRouter TPM limit is being hit. "timeout" means the generation took too long. "validation_failed" means the slide validator is rejecting output. Each has a specific fix.

**Jobs Stuck in Running State**: Any job that has been in `running` status for more than 2 hours is likely stuck. Show these with a "Kill" button that sets the job to `error` status so it doesn't block the queue.

**Empty Slide Count**: How many slides passed validation but were under the size threshold (2500 bytes). This means thin content is reaching teachers. If this number is non-zero, the validation is too permissive.

---

### Section 8 — Materials & Storage

**Total Materials Stored**: Count of rows in the materials table.

**Total Disk Usage (mnt/ directory)**: Size of the `mnt/` folder in megabytes. Once Railway Volume is attached, track how fast this grows. Alert if over 40GB (80% of a 50GB Volume).

**Materials Without Files**: Materials rows where `pptx_path` is set but the file doesn't exist on disk (orphaned records). These are materials that were generated on a previous Railway deployment and lost when disk was wiped. Show the count — anything above 0 means teachers have broken download links.

**Average Slide Count Per Generation**: Should be 13–18. If it consistently falls below 10, the generation is cutting corners. If above 20, something is generating too many slides.

---

### Section 9 — Scheduled Tasks & System Health

**Scheduled Tasks**: List all active scheduled tasks (from the `mcp__scheduled-tasks` system). For each: name, frequency, last run time, last run status. If the Curator Agent is built, show its last run report inline.

**Server Uptime**: Railway's deployment timestamp (how long since the current container started). If this is under 5 minutes, there was a recent crash or redeploy.

**Database Size**: Size of `cogniesl.db` and `jobs.db` in KB. SQLite handles hundreds of thousands of rows without issues, but good to monitor.

**Railway Environment**: Which environment is active (production vs staging). Show the Railway project name and environment name. Protects against accidentally running admin commands on the wrong environment.

---

## Data Model Additions Needed

To support the full dashboard, a few additions are needed to the existing databases:

**Add to `jobs` table**: `user_id` (already referenced but not stored), `cost_estimate` (float), `error_message` (text), `grammar_point` (text), `l1_languages` (text).

**New `generations` table**: `(id, user_id, job_id, created_at, grammar_point, l1_languages, formats, level, age_group, cost_estimate, model_version, cache_hit bool)`. This is the source of truth for all usage metrics and cost tracking.

**New `waitlist` table**: `(id, email, created_at, source)` — source records where the signup came from (homepage hero, blog post, etc.).

**New `subscription_events` table**: `(id, user_id, event_type, from_tier, to_tier, created_at, stripe_event_id)` — records every subscription change. Source of truth for MRR and churn calculations.

---

## How to Access the Dashboard

The dashboard lives at `https://your-railway-domain.up.railway.app/admin`. It is protected by a simple password (set in Railway environment variables as `ADMIN_PASSWORD`). No external auth service needed. The session cookie expires in 8 hours.

On first build: protect with a long random password. Store it in your password manager, not in the codebase.

---

## Build Priority

Build the dashboard in this order:

1. The admin authentication middleware and login form (1 day)
2. Section 1 (Live Pulse) and Section 7 (Error Monitoring) — these are the most operationally critical (1–2 days)
3. Section 3 (Usage Metrics) — tells you if the product is being used (1 day)
4. Section 4 (Cost tracking) — requires adding `cost_estimate` to the generations table (1 day)
5. Section 2 (Revenue) — requires Stripe integration first; can stub with DB counts until then
6. Sections 5, 6, 8, 9 — progressively add as time allows

The whole dashboard can be a single HTML file served by FastAPI — no React, no build step, no Node dependency. Use vanilla JS with `fetch()` to call the `/api/admin/*` endpoints and populate the page. This is the simplest possible implementation that gets you 90% of the value.

---

*The dashboard does not need to be beautiful — it needs to be accurate and fast to check. A clean table layout with color-coded numbers (green/yellow/red) is more useful than a polished design. Build it to be useful to you, not impressive to others.*
