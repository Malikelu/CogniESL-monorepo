# Phase 6 Plan: User Accounts + My Materials Library

**Status:** Planned (not started)  
**Prerequisite:** Phase 5 tested and stable (async generation + email delivery working)  
**Goal:** Teachers have persistent accounts. Every generation is saved to their personal library. They can re-download, edit, or regenerate past materials without starting from scratch.

---

## What Phase 6 Adds

1. **User accounts** — teachers register with email + password (or Google SSO)
2. **My Materials library** — all generated sets saved per account, browsable and re-downloadable
3. **Session continuity** — returning teacher's project history is available to the agent
4. **Account-scoped storage** — files stored under `/mnt/{user_id}/{project_name}/` instead of a shared folder

---

## Component Breakdown

### 6A: Authentication

**Approach:** Email/password with JWT tokens. Google OAuth as a bonus in Phase 7+.

**New files:**
- `auth/models.py` — User model: `id (uuid), email, password_hash, created_at, subscription_tier`
- `auth/auth.py` — `register(email, password)`, `login(email, password)`, `verify_token(token)`, `hash_password()`, `create_jwt()`
- `auth/db.py` — SQLite (or PostgreSQL later) schema for users table

**New endpoints in `server.py`:**
```python
POST /api/auth/register   # email + password → creates account
POST /api/auth/login      # email + password → returns JWT token
GET  /api/auth/me         # returns current user info (requires auth header)
```

**Frontend changes:**
- Login/register page at `/login`
- JWT stored in `localStorage` under `cogniesl_token`
- All `/cogniesl/get_response` and `/download` requests include `Authorization: Bearer {token}` header

**Server-side session linking:**
- `X-Session-ID` header (already used) is linked to a user account via the JWT
- Unauthenticated sessions are allowed (for demos) but materials aren't saved to a library

---

### 6B: Per-User File Storage

**Current:** `/mnt/{project_name}/` (shared, no user isolation)  
**Phase 6:** `/mnt/{user_id}/{project_name}/`

**Changes:**
- `server.py` — all file paths resolved relative to user's folder
- `agent/instructions.md` — project_name paths updated: `./mnt/{user_id}/{project_name}/...`
- `jobs.py` — add `user_id` column to jobs table
- `/download/{job_id}/{filename}` endpoint — verifies requesting user owns the job

**Migration:** Existing test projects in `/mnt/` are unaffected (they belong to no user). New authenticated generations go into user folders.

---

### 6C: My Materials Library (Database + API)

**New table:** `materials`

```sql
CREATE TABLE materials (
  id          TEXT PRIMARY KEY,  -- uuid
  user_id     TEXT NOT NULL,     -- foreign key to users
  project_name TEXT NOT NULL,
  grammar_point TEXT,
  l1_languages  TEXT,
  age_group     TEXT,
  formats       TEXT,            -- JSON array: ["slides","worksheet"]
  slide_count   INTEGER,
  pptx_path     TEXT,
  worksheet_pdf_path  TEXT,
  worksheet_docx_path TEXT,
  activity_pdf_path   TEXT,
  activity_docx_path  TEXT,
  created_at    TEXT,
  model_version TEXT             -- which LLM generated it (for curator agent)
);
```

**New endpoints:**
```python
GET  /api/materials           # list all materials for current user (paginated)
GET  /api/materials/{id}      # get single material details + download links
DELETE /api/materials/{id}    # soft-delete (mark archived)
```

**Agent changes:**
- `MarkJobComplete` also writes a row to `materials` table after generation
- `agent/instructions.md` — returning teacher flow (Part 6) updated: agent can call a `ListMaterials` tool to reconstruct project memory for past sessions

---

### 6D: Frontend — My Materials Page

**New route:** `/materials`

**UI elements:**
- List of past generated sets, newest first
- Each card: grammar point + L1 + age group + date + format badges (slides / WS / AG)
- Download buttons per file format (links to `/download/{job_id}/{filename}`)
- "Continue editing" button → opens a new chat session pre-loaded with this project's context
- Search/filter bar: by grammar point, by L1, by date range

**Implementation:** Single HTML page using vanilla JS + fetch API (no framework, consistent with current frontend approach).

---

### 6E: Agent Library Awareness

The agent should be able to see the teacher's past materials and pick up where they left off.

**New tool:** `ListMaterials(user_id, grammar_point=None, l1=None, limit=10)`  
Returns: list of recent materials with project_name, slide_count, formats generated.

**Updated Part 6 (returning teacher flow) in `instructions.md`:**
```
If teacher is authenticated and references a past project:
1. Call ListMaterials to find matching projects
2. Show: "I found your [grammar_point]-[l1] set from [date] — [N] slides, [formats]. Is that the one?"
3. On confirmation: reconstruct PROJECT MEMORY from the materials record
4. Proceed with the change request
```

This removes the awkward "what was your topic and language?" reconnect for authenticated users.

---

## Technical Notes

### Authentication stack
- `bcrypt` for password hashing (pip install bcrypt)
- `python-jose` for JWT tokens (pip install python-jose[cryptography])
- Token expiry: 30 days (long-lived for teachers; they don't log in daily)
- No refresh token in Phase 6 — just re-login if expired

### Database strategy
- Stay on SQLite for Phase 6 (already used for jobs.db)
- Single `cogniesl.db` with three tables: users, jobs, materials
- PostgreSQL migration in Phase 8+ when multi-server deployment is needed

### File storage
- Stay on local disk for Phase 6
- S3/R2 migration in Phase 8+ (same time as PostgreSQL)

### Security
- All `/api/materials/*` and `/download/*` endpoints require valid JWT
- User can only access their own files (enforced by `user_id` check, not just job_id)
- Password minimum: 8 chars (enforced client + server side)

---

## Test Plan

**Test 6A — Register + login:**
- Register with email, verify JWT returned
- Login with same credentials, verify JWT
- Invalid password → 401

**Test 6B — Per-user storage:**
- Generate as User A → files appear in `/mnt/{user_a_id}/project/`
- User B cannot download User A's files

**Test 6C — Materials library:**
- After generation, `/api/materials` returns the new entry
- Download links from the library resolve correctly

**Test 6D — Frontend:**
- My Materials page loads and displays past generations
- Download buttons work for each file format

**Test 6E — Agent library awareness:**
- Returning user says "continue my present perfect for French adults" → agent finds the project without asking for clarification

---

## Implementation Order

1. `auth/` module + users table + register/login endpoints (6A)
2. Per-user storage paths in server.py + agent instructions (6B)
3. `materials` table + `/api/materials` endpoints (6C)
4. `MarkJobComplete` writes to materials table (6C — agent side)
5. `ListMaterials` tool + updated returning-teacher flow in instructions.md (6E)
6. My Materials frontend page (6D)
7. Test all 5 scenarios above

**Estimated effort:** Medium — no new LLM calls, no new generation pipeline changes. Pure backend + frontend work.

---

## Out of Scope for Phase 6

- Google OAuth (Phase 7)
- Subscription billing / Stripe (Phase 7)
- Subscription tier enforcement (Phase 7)
- S3/R2 storage migration (Phase 8)
- PostgreSQL migration (Phase 8)
- Admin dashboard (Phase 9)
- Curator agent (Phase 9)

---

**Last Updated:** 2026-05-22  
**Status:** Planned — starts after Phase 5 testing complete
