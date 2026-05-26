# Phase 5: Async Generation + Email Delivery
**Status:** Planned — not yet implemented  
**Last updated:** 2026-05-22  
**Priority:** High — prerequisite for production (current HTTP timeout breaks all real requests)

---

## The Problem

The current architecture holds an HTTP connection open for the entire generation run (20–40 min). Browsers and servers close connections after ~60–120 seconds. Every real teacher request times out.

---

## The Solution (minimum viable, Karpathy-style)

Three components added to the existing FastAPI + agency_swarm stack:

1. **Background job runner** — generation runs in a separate thread/process, returns job_id immediately
2. **Job status table** — SQLite table tracking job state + file paths when done
3. **Email on completion** — Resend API sends a branded email with download links

No Redis, no Celery, no WebSockets. Python's `concurrent.futures.ThreadPoolExecutor` is enough for MVP.

---

## Component 1: Background Job Runner

### What changes in `server.py`

Current flow:
```
POST /api/chat → agent runs (blocks) → returns response after 30 min → browser times out
```

New flow:
```
POST /api/chat → enqueue job → return {"status": "generating", "job_id": "abc123"} immediately
                ↓
           background thread runs agent
                ↓
           on completion: writes job to DB, sends email
```

### Implementation

**New file: `jobs.py`** (next to `server.py`):
```python
import sqlite3
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "jobs.db"
_executor = ThreadPoolExecutor(max_workers=2)  # max 2 concurrent generations

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'pending',
                email TEXT,
                project_name TEXT,
                grammar_point TEXT,
                l1_languages TEXT,
                file_paths TEXT,  -- JSON array of paths
                created_at TEXT,
                completed_at TEXT,
                error TEXT
            )
        """)

def enqueue(agent_fn, kwargs: dict, email: str) -> str:
    """Submit a generation job. Returns job_id immediately."""
    job_id = str(uuid.uuid4())[:8]
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT INTO jobs (job_id, status, email, created_at) VALUES (?, 'pending', ?, ?)",
            (job_id, email, datetime.utcnow().isoformat())
        )
    _executor.submit(_run_job, job_id, agent_fn, kwargs, email)
    return job_id

def _run_job(job_id, agent_fn, kwargs, email):
    try:
        _update(job_id, status="running")
        result = agent_fn(**kwargs)  # runs the agent — blocks here until done
        _update(job_id, status="done", file_paths=result.get("file_paths", []),
                project_name=result.get("project_name"),
                grammar_point=result.get("grammar_point"),
                l1_languages=result.get("l1_languages"),
                completed_at=datetime.utcnow().isoformat())
        if email:
            send_completion_email(email, job_id, result)
    except Exception as e:
        _update(job_id, status="error", error=str(e))

def _update(job_id, **kwargs):
    cols = ", ".join(f"{k}=?" for k in kwargs)
    with sqlite3.connect(DB_PATH) as db:
        db.execute(f"UPDATE jobs SET {cols} WHERE job_id=?", (*kwargs.values(), job_id))

def get_job(job_id: str) -> dict | None:
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    if not row:
        return None
    cols = ["job_id","status","email","project_name","grammar_point","l1_languages",
            "file_paths","created_at","completed_at","error"]
    return dict(zip(cols, row))
```

**Changes to `server.py`:**

1. At startup: `jobs.init_db()`
2. In the chat endpoint: detect when the agent is about to start generation (after Content Brief approval). At that point:
   - Extract `teacher_email` from session (to be stored during the chat interview — see below)
   - Call `jobs.enqueue(run_agent, {...}, email=teacher_email)`
   - Return immediately: `{"message": "Your materials are being generated! You'll receive an email when ready — usually 15–25 minutes.", "job_id": job_id}`

**New endpoint: `GET /api/jobs/{job_id}`** — for polling (optional, useful for testing)
```python
@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(404)
    return job
```

**New endpoint: `GET /download/{job_id}/{filename}`** — serves the generated file
```python
@app.get("/download/{job_id}/{filename}")
async def download_file(job_id: str, filename: str):
    job = jobs.get_job(job_id)
    if not job or job["status"] != "done":
        raise HTTPException(404)
    # Find the file in the project folder
    project_dir = Path("mnt") / job["project_name"]
    # Search presentations/ and documents/ subdirs
    for subdir in ["presentations", "documents"]:
        path = project_dir / subdir / filename
        if path.exists():
            return FileResponse(path, filename=filename)
    raise HTTPException(404)
```

---

## Component 2: Email collection during chat interview

The agent needs the teacher's email address before starting generation. Add this to the chat interview flow in `agent/instructions.md`:

**Where:** After confirming all requirements (topic, L1, age, format) but BEFORE running database searches.

**Exact question:**
> "One last thing — what email should I send your materials to when they're ready?"

**Rules:**
- Ask only once. Accept any valid email format. Store it in session context.
- If the teacher skips or doesn't want to provide email: proceed without email, materials only available via the chat (current behavior).
- Never ask for email before confirming the materials request — email is always last.

---

## Component 3: Email on completion

**Service**: Resend (resend.com) — 3,000 emails/month free, simple Python SDK, transactional email.

**New file: `email_sender.py`**:
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

BASE_URL = os.environ.get("COGNIESL_BASE_URL", "http://localhost:8080")

def send_completion_email(email: str, job_id: str, result: dict):
    grammar_point = result.get("grammar_point", "your materials")
    l1 = result.get("l1_languages", "")
    file_paths = result.get("file_paths", [])
    
    # Build download links
    links_html = ""
    for fp in file_paths:
        filename = Path(fp).name
        url = f"{BASE_URL}/download/{job_id}/{filename}"
        emoji = "📊" if filename.endswith(".pptx") else ("📄" if filename.endswith(".pdf") else "📝")
        label = _label_for_file(filename)
        links_html += f'<p><a href="{url}" style="display:inline-block;padding:12px 24px;background:#4f46e5;color:white;text-decoration:none;border-radius:8px;font-weight:bold;">{emoji} {label}</a></p>\n'
    
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
      <h1 style="color:#1e1b4b;">Your CogniESL materials are ready! 🎉</h1>
      <p>Here are your materials for <strong>{grammar_point}</strong>{f' — {l1}' if l1 else ''}:</p>
      {links_html}
      <p style="color:#6b7280;font-size:14px;">Need to change something? Go back to your CogniESL chat — just tell me which slide and what to change.</p>
      <hr style="border:none;border-top:1px solid #e5e7eb;margin:24px 0;">
      <p style="color:#9ca3af;font-size:12px;">CogniESL — AI-powered ESL teaching materials</p>
    </div>
    """
    
    resend.Emails.send({
        "from": "CogniESL <materials@cogniesl.com>",
        "to": email,
        "subject": f"Your {grammar_point} materials are ready!",
        "html": html,
    })

def _label_for_file(filename: str) -> str:
    if filename.endswith(".pptx"): return "Download Slides (PPTX)"
    if "worksheet" in filename and filename.endswith(".pdf"): return "Download Worksheet (PDF)"
    if "activity" in filename and filename.endswith(".pdf"): return "Download Activity Guide (PDF)"
    if filename.endswith(".docx"): return "Download Document (Word)"
    return f"Download {filename}"
```

**Add to `.env`:**
```
RESEND_API_KEY=re_xxxxx
COGNIESL_BASE_URL=http://localhost:8080  # change to production URL when deployed
```

---

## What the teacher experiences

1. Opens CogniESL chat, goes through the interview
2. Sees Content Brief, says "looks good"
3. Types their email when asked
4. Receives immediately: *"Your materials are being generated! You'll receive an email at [email] when ready — usually 15–25 minutes."*
5. Closes the tab, goes to teach their class
6. ~20 minutes later, email arrives in inbox with 3 download buttons
7. One click to download the PPTX, worksheet, activity guide

---

## Implementation Order

1. **`jobs.py`** — create the file, init_db(), enqueue(), _run_job(), get_job()
2. **`server.py`** — call init_db() at startup; add `/download/{job_id}/{filename}` endpoint; add `/api/jobs/{job_id}` endpoint; modify chat endpoint to enqueue instead of await
3. **`email_sender.py`** — create the file, wire to resend
4. **`agent/instructions.md`** — add email collection step (one line, after requirements confirmed, before database searches)
5. **`.env`** — add RESEND_API_KEY, COGNIESL_BASE_URL
6. **`requirements.txt`** — add `resend`

**Total estimate**: ~3–4 hours dev time (mostly wiring, not complex logic)

---

## Open Questions (decide before implementing)

1. **How long do download links stay active?** Suggest: 7 days. After that, teacher needs to re-request. (Keeps storage manageable.)
2. **What if generation fails?** Send a failure email: "Something went wrong — please try again or contact support." Simple is fine for MVP.
3. **What domain to send email from?** Need a domain for Resend to send from (free with Resend). Suggest: `materials@cogniesl.com` once domain is purchased.
4. **What if teacher doesn't provide email?** For MVP: graceful degradation — materials still generate but are only accessible via the project folder path. Phase 7 (user accounts) will add proper material persistence.
5. **Concurrent generation cap**: `ThreadPoolExecutor(max_workers=2)` means max 2 simultaneous generations. With ~30 min per generation, this handles ~4 teachers/hour. Sufficient for beta, needs scaling later.
