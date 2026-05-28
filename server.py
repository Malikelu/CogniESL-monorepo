"""CogniESL Server — FastAPI entry point. Run with: python server.py"""
import asyncio
import hashlib
import logging
import os
import re
import time
from pathlib import Path
from threading import Lock
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)

# Disable openai-agents tracing — it spams the log with 400 errors about
# unknown span parameters that don't affect functionality.
try:
    from agents import set_tracing_disabled
    set_tracing_disabled(True)
except Exception:
    pass

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from agent.cogniesl_agent import create_cogniesl_agent
from agent import jobs as _jobs
from auth import db as _auth_db
from auth.auth import (
    AuthError,
    register as auth_register,
    login as auth_login,
    get_current_user,
    hash_password,
)

# Session store: agent + agency_context (for persistent conversation history)
_agents: dict[str, object] = {}
_contexts: dict[str, object] = {}
_last_access: dict[str, float] = {}
_lock = Lock()

# Global generation lock — only one session may run slide/doc generation at a time.
# This prevents concurrent sessions from saturating the TPM rate limit.
_generation_lock = asyncio.Lock()

SESSION_TIMEOUT = 14400  # 4 hours — teacher may review the Content Brief and come back later


def _make_context(agent):
    """Create a persistent AgencyContext for a standalone agent."""
    from agency_swarm.utils.thread import ThreadManager
    from agency_swarm.agent.context_types import AgencyContext, AgentRuntimeState
    return AgencyContext(
        agency_instance=None,
        thread_manager=ThreadManager(),
        runtime_state=AgentRuntimeState(agent._tool_concurrency_manager),
    )


def get_session(session_id: str):
    """Get or create a persistent agent + context for a session."""
    with _lock:
        now = time.time()
        expired = [sid for sid, t in _last_access.items() if now - t > SESSION_TIMEOUT]
        for sid in expired:
            del _agents[sid]
            del _contexts[sid]
            del _last_access[sid]
            logging.info(f"Cleaned up expired session: {sid}")

        if session_id not in _agents:
            logging.info(f"Creating new agent for session: {session_id}")
            agent = create_cogniesl_agent()
            _agents[session_id] = agent
            _contexts[session_id] = _make_context(agent)

        _last_access[session_id] = now
        return _agents[session_id], _contexts[session_id]


def _clean_response(text: str) -> str:
    text = re.sub(r"<memory-context>[\s\S]*?</memory-context>", "", text)
    text = re.sub(r"<memory-context>[\s\S]*", "", text)
    text = re.sub(r"\[System note:[\s\S]*?\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


app = FastAPI()

# Initialise databases on startup
_jobs.init_db()
_auth_db.init_auth_db()


# ── Daily digest email scheduler (I-3) ──────────────────────────────────────
# Sends a branded digest to FOUNDER_EMAIL every day at 7:00 AM server time.
# Uses only stdlib threading — no APScheduler required.
def _run_daily_digest_scheduler():
    """Background daemon: sleeps until 7am each day, then sends the digest email."""
    import threading
    import datetime
    import urllib.request
    import json

    def _next_7am_seconds() -> float:
        """Return seconds until the next 07:00 local time."""
        now = datetime.datetime.now()
        target = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if target <= now:
            target += datetime.timedelta(days=1)
        return (target - now).total_seconds()

    def _loop():
        while True:
            delay = _next_7am_seconds()
            logging.info(f"[digest] Next digest email in {delay/3600:.1f}h")
            import time
            time.sleep(delay)
            try:
                base_url = os.getenv("COGNIESL_BASE_URL", "http://localhost:8080").rstrip("/")
                req = urllib.request.Request(f"{base_url}/api/admin/daily-digest")
                admin_token = os.getenv("ADMIN_TOKEN", "")
                if admin_token:
                    req.add_header("Authorization", f"Bearer {admin_token}")
                with urllib.request.urlopen(req, timeout=30) as resp:
                    digest_data = json.loads(resp.read())
                from agent.email_sender import send_daily_digest_email
                send_daily_digest_email(digest_data)
            except Exception as exc:
                logging.error(f"[digest] Failed to send daily digest: {exc}")

    t = threading.Thread(target=_loop, daemon=True, name="daily-digest-scheduler")
    t.start()
    logging.info("[digest] Daily digest scheduler started (fires at 07:00 daily)")


if os.getenv("FOUNDER_EMAIL") and os.getenv("RESEND_API_KEY"):
    _run_daily_digest_scheduler()

# CORS — allow marketing site and dev server to reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://cogniesl.com",
        "https://www.cogniesl.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount generated slide HTML files so the presenter can load them by URL
_SLIDES_MNT_DIR = Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent)) / "mnt"
_SLIDES_MNT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/slides", StaticFiles(directory=str(_SLIDES_MNT_DIR)), name="slides")
logging.info(f"Mounted slides from {_SLIDES_MNT_DIR}")


@app.get("/")
async def healthcheck():
    return {"status": "ok", "service": "CogniESL"}


@app.get("/api/healthcheck")
async def api_healthcheck():
    """Verify static YAML data is accessible (grammar, L1 interference, activities)."""
    static_dir = Path(os.getenv("COGNIESL_STATIC_DIR", Path(__file__).parent / "data"))
    checks = {}
    for subdir in ("grammar", "l1-interference", "activities"):
        d = static_dir / subdir
        count = len(list(d.glob("*.yaml"))) if d.exists() else 0
        checks[subdir] = {"path": str(d), "yaml_count": count, "ok": count > 0}
    overall = all(v["ok"] for v in checks.values())
    status_code = 200 if overall else 503
    return JSONResponse({"status": "ok" if overall else "degraded", "checks": checks}, status_code=status_code)


@app.get("/api/jobs/{job_id}")
async def job_status(job_id: str):
    """Return the current status of a generation job (for debugging / future polling)."""
    job = _jobs.get_job(job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    return JSONResponse(job)


@app.get("/download/{job_id}/{filename}")
async def download_file(job_id: str, filename: str):
    """
    Serve a generated file by job_id + filename.
    Links of this form are sent in the completion email.
    """
    job = _jobs.get_job(job_id)
    if not job or job.get("status") != "done":
        return JSONResponse({"error": "File not available"}, status_code=404)

    project_name = job.get("project_name", "")
    if not project_name:
        return JSONResponse({"error": "Project not found"}, status_code=404)

    # Sanitise filename — no path traversal
    safe_name = Path(filename).name
    project_dir = Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent)) / "mnt" / project_name
    for subdir in ("presentations", "documents"):
        candidate = project_dir / subdir / safe_name
        if candidate.exists() and candidate.is_file():
            return FileResponse(
                str(candidate),
                filename=safe_name,
                media_type="application/octet-stream",
            )
    return JSONResponse({"error": "File not found"}, status_code=404)


# ─── Auth endpoints ───────────────────────────────────────────────────────────

@app.post("/api/auth/register")
async def api_register(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    try:
        user, token = auth_register(body.get("email", ""), body.get("password", ""), body.get("name", ""))
        return JSONResponse({"user": vars(user), "token": token})
    except AuthError as e:
        return JSONResponse({"error": e.message}, status_code=e.status_code)


@app.post("/api/auth/login")
async def api_login(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    try:
        user, token = auth_login(body.get("email", ""), body.get("password", ""))
        return JSONResponse({"user": vars(user), "token": token})
    except AuthError as e:
        return JSONResponse({"error": e.message}, status_code=e.status_code)


@app.get("/api/auth/me")
async def api_me(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    token = auth_header[7:]
    user = get_current_user(token)
    if not user:
        return JSONResponse({"error": "Invalid or expired token"}, status_code=401)
    return JSONResponse({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at,
        "subscription_tier": user.subscription_tier,
    })


@app.get("/api/auth/usage")
async def api_usage(request: Request):
    """Return the current user's monthly generation count and tier limit."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    user = get_current_user(auth_header[7:])
    if not user:
        return JSONResponse({"error": "Invalid or expired token"}, status_code=401)
    monthly = _auth_db.count_monthly_generations(user.id)
    tier_limit = _auth_db.get_tier_limit(user.subscription_tier)
    return JSONResponse({
        "monthly_generations": monthly,
        "tier_limit": tier_limit,
        "subscription_tier": user.subscription_tier,
    })


@app.get("/api/auth/stats")
async def api_stats(request: Request):
    """Return gamification stats for the authenticated user."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    user = get_current_user(auth_header[7:])
    if not user:
        return JSONResponse({"error": "Invalid or expired token"}, status_code=401)
    activity = _auth_db.get_user_activity(user.id)
    stats = activity.get("stats", {})
    total = stats.get("total_generations", 0)
    # Derive unique languages taught from generation records
    langs: set[str] = set()
    for g in activity.get("generations", []):
        for lang in (g.get("l1_languages") or "").split(","):
            lang = lang.strip()
            if lang:
                langs.add(lang)
    return JSONResponse({
        "total_generations": total,
        "hours_saved": round(total * 0.75, 1),
        "languages_taught": sorted(langs),
        "languages_count": len(langs),
        "member_since": stats.get("first_seen", ""),
    })


@app.delete("/api/auth/me")
async def api_delete_account(request: Request):
    """Permanently delete the authenticated user's account and all their data."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    user = get_current_user(auth_header[7:])
    if not user:
        return JSONResponse({"error": "Invalid or expired token"}, status_code=401)
    _auth_db.delete_user_account(user.id)
    return JSONResponse({"deleted": True})


@app.post("/api/auth/forgot-password")
async def api_forgot_password(request: Request):
    """Send a password reset email. Always returns 200 to avoid email enumeration."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    email = body.get("email", "").lower().strip()
    user = _auth_db.get_user_by_email(email)
    if user:
        token = _auth_db.create_reset_token(user.id)
        base_url = os.getenv("BASE_URL", "http://localhost:3000")
        reset_url = f"{base_url}/reset-password?token={token}"
        # Send via Resend if configured
        resend_key = os.getenv("RESEND_API_KEY", "")
        if resend_key:
            try:
                import resend as _resend
                _resend.api_key = resend_key
                from_email = os.getenv("RESEND_FROM_EMAIL", "CogniESL <noreply@cogniesl.com>")
                _resend.Emails.send({
                    "from": from_email,
                    "to": email,
                    "subject": "Reset your CogniESL password",
                    "html": f"""
                    <p>Hi,</p>
                    <p>Click the link below to reset your CogniESL password.
                    This link expires in 2 hours.</p>
                    <p><a href="{reset_url}" style="background:#0D7377;color:#fff;
                    padding:12px 24px;border-radius:8px;text-decoration:none;
                    font-weight:bold;">Reset Password</a></p>
                    <p>If you didn't request this, ignore this email.</p>
                    <p>— The CogniESL Team</p>
                    """,
                })
            except Exception as e:
                logging.error(f"Failed to send reset email: {e}")
        else:
            logging.info(f"[DEV] Password reset token for {email}: {reset_url}")
    return JSONResponse({"message": "If that email exists, a reset link has been sent."})


@app.post("/api/auth/reset-password")
async def api_reset_password(request: Request):
    """Validate a reset token and update the user's password."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    token = body.get("token", "")
    new_password = body.get("password", "")
    if len(new_password) < 8:
        return JSONResponse({"error": "Password must be at least 8 characters"}, status_code=400)
    user_id = _auth_db.use_reset_token(token)
    if not user_id:
        return JSONResponse({"error": "Invalid or expired reset link"}, status_code=400)
    _auth_db.update_password(user_id, hash_password(new_password))
    return JSONResponse({"message": "Password updated successfully."})


# ─── Waitlist endpoint ────────────────────────────────────────────────────────

@app.post("/api/waitlist")
async def api_join_waitlist(request: Request):
    """Add an email to the waitlist."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    email = body.get("email", "").lower().strip()
    if not email or "@" not in email:
        return JSONResponse({"error": "Invalid email address"}, status_code=400)
    _auth_db.add_to_waitlist(email, source=body.get("source", "homepage"))
    return JSONResponse({"message": "You're on the list!"})


# ─── Materials endpoints ───────────────────────────────────────────────────────

def _require_auth(request: Request):
    """Extract and validate Bearer token; return User or raise JSONResponse."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, JSONResponse({"error": "Unauthorized"}, status_code=401)
    token = auth_header[7:]
    user = get_current_user(token)
    if not user:
        return None, JSONResponse({"error": "Invalid or expired token"}, status_code=401)
    return user, None


@app.get("/api/materials")
async def api_list_materials(request: Request):
    user, err = _require_auth(request)
    if err:
        return err
    grammar_point = request.query_params.get("grammar_point")
    l1 = request.query_params.get("l1")
    materials = _auth_db.list_materials(user.id, grammar_point=grammar_point, l1=l1)
    count = _auth_db.count_materials(user.id)
    return JSONResponse({"materials": materials, "total": count})


@app.get("/api/materials/{material_id}")
async def api_get_material(material_id: str, request: Request):
    user, err = _require_auth(request)
    if err:
        return err
    mat = _auth_db.get_material(material_id, user.id)
    if not mat:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return JSONResponse(mat)


@app.delete("/api/materials/{material_id}")
async def api_delete_material(material_id: str, request: Request):
    user, err = _require_auth(request)
    if err:
        return err
    deleted = _auth_db.delete_material(material_id, user.id)
    if not deleted:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return JSONResponse({"deleted": True})


@app.post("/api/materials/{material_id}/edits")
async def api_log_material_edit(material_id: str, request: Request):
    user, err = _require_auth(request)
    if err:
        return err
    mat = _auth_db.get_material(material_id, user.id)
    if not mat:
        return JSONResponse({"error": "Not found"}, status_code=404)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    edit_id = _auth_db.log_material_edit(
        material_id=material_id,
        user_id=user.id,
        edit_type=body.get("edit_type", "slide_change"),
        description=body.get("description", ""),
        slide_index=body.get("slide_index"),
    )
    return JSONResponse({"ok": True, "edit_id": edit_id})


@app.post("/cogniesl/get_response")
async def get_response(request: Request):
    """Persistent agent endpoint — maintains conversation context per session."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "")
    if not message:
        return JSONResponse({"error": "Message is required"}, status_code=400)

    # Auth required — anonymous generation is not allowed.
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Authentication required"}, status_code=401)
    _authed_user = get_current_user(auth_header[7:])
    if not _authed_user:
        return JSONResponse({"error": "Invalid or expired token"}, status_code=401)

    session_id = request.headers.get("X-Session-ID", request.client.host)
    agent, ctx = get_session(session_id)

    ctx.user_id = _authed_user.id  # type: ignore[attr-defined]
    message = (
        f"<memory-context>teacher_email={_authed_user.email} — "
        f"the teacher is logged in. Store this as teacher_email immediately. "
        f"Do NOT ask for their email address at any point in this conversation.</memory-context>\n"
        + message
    )

    # Free-tier enforcement: block generation if user has hit their monthly limit
    _GENERATION_TRIGGER_WORDS = (
        "go ahead", "looks good", "generate", "create", "make it",
        "start", "build", "produce", "yes, ", "yes please", "approved",
    )
    _message_lower = message.lower()
    _is_generation_trigger = any(w in _message_lower for w in _GENERATION_TRIGGER_WORDS)
    if _is_generation_trigger:
        if _authed_user.subscription_tier == "free":
            _monthly = _auth_db.count_monthly_generations(_authed_user.id)
            if _monthly >= _auth_db.get_tier_limit("free"):
                return JSONResponse({"response": (
                    "You've used all 5 of your free generations this month! 🎉\n\n"
                    "Upgrade to **Pro** for 20 generations/month, all 36 native languages, "
                    "and complete materials (slides + worksheet + activity guide).\n\n"
                    "[Upgrade to Pro →](/pricing)"
                )})

    # ── Approval detection ────────────────────────────────────────────────────
    # A short message with approval words means the teacher said "yes" to the
    # Content Brief. This is the turn where QueueGenerationJob MUST be called.
    # We distinguish this from the initial request (which can contain "yes" in
    # other contexts) by requiring the message to be short (< 120 chars).
    _raw_msg = body.get("message", "").strip()  # original, before email injection
    _approval_words = (
        "looks good", "go ahead", "yes", "approved", "start", "go",
        "ok", "okay", "let's go", "sounds good", "perfect", "great",
        "proceed", "do it", "make it", "yep", "yup", "sure", "correct",
        "that's right", "that works", "generate", "create", "build",
    )
    _is_approval = len(_raw_msg) < 120 and any(w in _raw_msg.lower() for w in _approval_words)

    # When the teacher approves, inject a hard force into their message.
    # Injecting into the USER TURN is much stronger than system-prompt instructions —
    # the model attends most closely to the most recent message it receives.
    if _is_approval:
        message = (
            "<memory-context>ACTION REQUIRED — TOOL CALL ONLY: The teacher just approved "
            "the Content Brief. Do NOT write any text in your response. Your ONLY action "
            "is to call QueueGenerationJob immediately, then run the full generation pipeline. "
            "A text response here means generation never starts and the teacher waits forever. "
            "Call the tool now.</memory-context>\n"
            + message
        )
        logging.info(f"[{session_id}] Approval detected — injected generation force into message")

    # Detect if this turn is likely to trigger a multi-minute generation pipeline.
    # Lock the global asyncio lock so concurrent sessions don't saturate TPM limits.
    # Use specific multi-word phrases to avoid locking on common words like "yes" or "make".
    _generation_keywords = ("slides", "worksheet", "activity guide", "generate materials",
                            "go ahead", "looks good", "let's go", "start generating",
                            "create materials", "build materials")
    _likely_generation = _is_approval or any(kw in message.lower() for kw in _generation_keywords)

    def _is_kickoff_message(text: str) -> bool:
        """True if the agent sent a short announcement instead of calling tools.
        Catches two failure modes:
          1. Pre-brief kickoff: "Your brief is coming right up!" (should be calling DB tools)
          2. Post-approval kickoff: "I'll start generating now" (should be calling QueueGenerationJob)
        The actual Content Brief is always > 700 chars, so length guards against false positives."""
        if len(text.strip()) > 700 or "/download/" in text:
            return False
        _kickoff_phrases = (
            # Pre-brief kickoffs (agent announces DB search instead of doing it)
            # NOTE: "coming up" removed — too generic (matches "Here's what's coming up")
            "stay tuned", "coming right up",
            "putting together", "will be ready", "brief is coming",
            "getting your brief", "preparing your brief",
            # Post-approval kickoffs (agent announces generation instead of doing it)
            "be right back", "give me a few", "one moment", "just a moment",
            "starting now", "i'll start", "i will start", "i'll get started",
            "i'll begin", "back shortly", "back soon", "back with your",
            "generating your", "creating your", "building your",
            "let me start", "let me generate", "let me build",
            "i'll now", "i will now", "back in a few",
            "i'm generating", "i am generating",
            "i'm creating", "i am creating", "i'm building", "i am building",
        )
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in _kickoff_phrases)

    async def _run():
        response = await agent.get_response(message=message, agency_context=ctx)
        text = str(getattr(response, 'final_output', response))

        if _is_kickoff_message(text):
            logging.warning(f"[{session_id}] Kickoff detected ('{text[:80].strip()}') — retrying (attempt 1)")
            if _is_approval:
                _force = (
                    "<memory-context>CRITICAL: You sent text instead of calling "
                    "QueueGenerationJob. Call QueueGenerationJob RIGHT NOW — "
                    "no text before the tool call.</memory-context>\n"
                    "Generate now."
                )
            else:
                _force = (
                    "<memory-context>CRITICAL: You sent a holding message instead of "
                    "running the database searches. Call SearchGrammarTool RIGHT NOW, "
                    "then GetL1InterferenceTool, then SearchActivitiesTool (if needed), "
                    "then return the full Content Brief. No more holding messages.</memory-context>\n"
                    "Search the database and show the Content Brief now."
                )
            retry_response = await agent.get_response(message=_force, agency_context=ctx)
            text = str(getattr(retry_response, 'final_output', retry_response))

            # Second retry if the first one also produced a kickoff
            if _is_kickoff_message(text):
                logging.warning(f"[{session_id}] Kickoff still detected after retry — forcing harder (attempt 2)")
                if _is_approval:
                    _force2 = (
                        "<memory-context>FINAL WARNING: Call QueueGenerationJob NOW. "
                        "Zero text. Tool call only.</memory-context>\n"
                        "Call the tool."
                    )
                else:
                    _force2 = (
                        "<memory-context>FINAL WARNING: Call SearchGrammarTool NOW. "
                        "No text. Tool call only.</memory-context>\n"
                        "Call SearchGrammarTool."
                    )
                retry2_response = await agent.get_response(message=_force2, agency_context=ctx)
                text = str(getattr(retry2_response, 'final_output', retry2_response))

        return text

    try:
        # Acquire the generation lock for any turn that might trigger tool chains
        # (generation, brief preparation, or explicit approval)
        if _likely_generation or _is_approval:
            async with _generation_lock:
                response_text = await asyncio.shield(_run())
        else:
            response_text = await asyncio.shield(_run())
        response_text = _clean_response(response_text)
        return JSONResponse({"response": response_text})

    except asyncio.CancelledError:
        # Client disconnected (browser timeout) — generation continues in background.
        # Files will be written to disk; teacher can restart the chat to get download links.
        logging.info(f"[{session_id}] Client disconnected — generation continues in background via shield")
        raise

    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)
        return JSONResponse(
            {"response": "Sorry, an error occurred. Please try again."},
            status_code=200,
        )


# ─── HTML Presenter endpoints ─────────────────────────────────────────────────

@app.get("/api/jobs/{job_id}/slides")
async def api_job_slides(job_id: str):
    """Return ordered slide metadata + speaker notes for the HTML presenter."""
    job = _jobs.get_job(job_id)
    if not job or job.get("status") != "done":
        return JSONResponse({"error": "Not available"}, status_code=404)

    project_name = job.get("project_name", "")
    if not project_name:
        return JSONResponse({"error": "No project"}, status_code=404)

    presentations_dir = Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent)) / "mnt" / project_name / "presentations"
    if not presentations_dir.exists():
        return JSONResponse({"error": "Slides not found"}, status_code=404)

    slides = []
    for i in range(1, 100):
        slide_path = presentations_dir / f"slide_{i:02d}.html"
        if not slide_path.exists():
            break
        html_text = slide_path.read_text(encoding="utf-8")
        notes_match = re.search(r'data-speaker-notes="([^"]*)"', html_text)
        notes = notes_match.group(1).replace("&quot;", '"') if notes_match else ""
        slides.append({
            "index": i,
            "url": f"/slides/{project_name}/presentations/slide_{i:02d}.html",
            "notes": notes,
        })

    # Find PPTX filename if it exists
    pptx_filename = None
    for f in presentations_dir.glob("*.pptx"):
        pptx_filename = f.name
        break

    return JSONResponse({
        "job_id": job_id,
        "project_name": project_name,
        "grammar_point": job.get("grammar_point", ""),
        "l1_languages": job.get("l1_languages", ""),
        "total": len(slides),
        "slides": slides,
        "pptx_filename": pptx_filename,
    })


@app.get("/api/jobs/{job_id}/bundle.html")
async def api_job_bundle(job_id: str):
    """Return a single self-contained HTML presentation bundle for offline use."""
    import json as _json_mod

    job = _jobs.get_job(job_id)
    if not job or job.get("status") != "done":
        return JSONResponse({"error": "Not available"}, status_code=404)

    project_name = job.get("project_name", "")
    if not project_name:
        return JSONResponse({"error": "No project"}, status_code=404)

    presentations_dir = Path(os.getenv("COGNIESL_DATA_DIR", Path(__file__).parent)) / "mnt" / project_name / "presentations"

    # Inline _theme.css so it works without the server
    theme_css = ""
    theme_path = presentations_dir / "_theme.css"
    if theme_path.exists():
        theme_css = theme_path.read_text(encoding="utf-8")

    slides_data = []
    for i in range(1, 100):
        slide_path = presentations_dir / f"slide_{i:02d}.html"
        if not slide_path.exists():
            break
        html_text = slide_path.read_text(encoding="utf-8")
        if theme_css:
            html_text = html_text.replace(
                '<link rel="stylesheet" href="./_theme.css" />',
                f"<style>{theme_css}</style>",
            )
        notes_match = re.search(r'data-speaker-notes="([^"]*)"', html_text)
        notes = notes_match.group(1).replace("&quot;", '"') if notes_match else ""
        slides_data.append({"html": html_text, "notes": notes})

    grammar = job.get("grammar_point", "").replace("_", " ").title()
    l1 = job.get("l1_languages", "")
    title = f"{grammar} — {l1} — CogniESL" if l1 else f"{grammar} — CogniESL"

    # Build bundle using placeholder substitution (avoids f-string / JSON brace conflicts)
    slides_json = _json_mod.dumps(slides_data, ensure_ascii=False)
    # Escape </script> so the inline JSON doesn't break the outer <script> tag
    slides_json = slides_json.replace("</", "<\\/")  # </ → <\/ safe in JS parsers
    bundle = _BUNDLE_TEMPLATE.replace("__TITLE__", title).replace("__SLIDES_DATA__", slides_json)

    return HTMLResponse(
        content=bundle,
        headers={"Content-Disposition": f'attachment; filename="{project_name}.html"'},
    )


_BUNDLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;font-family:system-ui,sans-serif;overflow:hidden;height:100vh;display:flex;flex-direction:column}
#ctrl{background:#111;padding:8px 14px;display:flex;align-items:center;gap:10px;flex-shrink:0;border-bottom:1px solid #222}
#ctrl h1{color:#aaa;font-size:12px;font-weight:500;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn{background:#1e1e1e;color:#ccc;border:1px solid #333;border-radius:6px;padding:5px 10px;font-size:12px;cursor:pointer}
.btn:hover{background:#2a2a2a;color:#fff}.btn.on{background:#0d9488;border-color:#0d9488;color:#fff}
.btn:disabled{opacity:0.35;cursor:default}
#cnt{color:#555;font-size:12px;white-space:nowrap;min-width:50px;text-align:center}
#stage{flex:1;display:flex;overflow:hidden}
#sc{flex:1;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
#frame{width:1280px;height:720px;border:none;transform-origin:center center;display:block}
#notes{width:300px;background:#111;border-left:1px solid #222;padding:16px;overflow-y:auto;flex-shrink:0;display:none}
#notes.show{display:block}
#notes h2{color:#0d9488;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px}
#nt{color:#bbb;font-size:12px;line-height:1.6;white-space:pre-wrap}
#hint{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:#2a2a2a;font-size:11px;pointer-events:none;user-select:none}
</style></head>
<body>
<div id="ctrl">
  <h1>__TITLE__</h1>
  <span id="cnt">1 / 1</span>
  <button class="btn" id="bp" onclick="go(-1)">◀</button>
  <button class="btn" id="bn" onclick="go(1)">▶</button>
  <button class="btn" id="bno" onclick="toggleNotes()">📝 Notes</button>
  <button class="btn" onclick="toggleFS()">⛶</button>
  <span style="color:#333;font-size:10px;flex-shrink:0">CogniESL</span>
</div>
<div id="stage">
  <div id="sc">
    <iframe id="frame" sandbox="allow-same-origin allow-scripts"></iframe>
    <div id="hint">← → navigate &nbsp;·&nbsp; N notes &nbsp;·&nbsp; F fullscreen</div>
  </div>
  <div id="notes"><h2>Speaker Notes</h2><div id="nt"></div></div>
</div>
<script>
const S=__SLIDES_DATA__;
let cur=0,notesOn=false;
function scale(){
  const f=document.getElementById('frame'),c=document.getElementById('sc');
  const s=Math.min((c.clientWidth-24)/1280,(c.clientHeight-24)/720);
  f.style.transform='scale('+s+')';
}
function load(i){
  const f=document.getElementById('frame'),sl=S[i];
  f.srcdoc=sl.html;
  document.getElementById('cnt').textContent=(i+1)+' / '+S.length;
  document.getElementById('nt').textContent=sl.notes||'(No speaker notes)';
  document.getElementById('bp').disabled=i===0;
  document.getElementById('bn').disabled=i===S.length-1;
}
function go(d){const n=cur+d;if(n<0||n>=S.length)return;cur=n;load(cur);}
function toggleNotes(){
  notesOn=!notesOn;
  document.getElementById('notes').classList.toggle('show',notesOn);
  document.getElementById('bno').classList.toggle('on',notesOn);
  scale();
}
function toggleFS(){
  if(!document.fullscreenElement)document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' ')go(1);
  else if(e.key==='ArrowLeft')go(-1);
  else if(e.key==='n'||e.key==='N')toggleNotes();
  else if(e.key==='f'||e.key==='F')toggleFS();
});
window.addEventListener('resize',scale);
document.getElementById('frame').addEventListener('load',scale);
load(0);scale();
</script>
</body></html>"""


# ─── Feedback endpoints ────────────────────────────────────────────────────────

@app.post("/api/feedback")
async def api_submit_feedback(request: Request):
    """Submit feedback for a generated material. Auth optional."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    rating = body.get("rating", "").strip()
    if rating not in ("perfect", "good", "issues"):
        return JSONResponse({"error": "Invalid rating"}, status_code=400)

    # Optional auth — we log user_id if available
    user_id = ""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        from auth.auth import get_current_user as _gcu
        u = _gcu(auth_header[7:])
        if u:
            user_id = u.id

    fid = _auth_db.save_feedback(
        rating=rating,
        user_id=user_id,
        material_id=body.get("material_id", ""),
        job_id=body.get("job_id", ""),
        tags=",".join(body.get("tags", [])),
        comment=body.get("comment", ""),
        source=body.get("source", "explicit"),
    )

    # Log event too
    import json as _je
    _auth_db.log_event(
        "feedback_submitted",
        user_id=user_id,
        metadata=_je.dumps({"rating": rating, "material_id": body.get("material_id", "")}),
    )

    return JSONResponse({"id": fid, "ok": True})


@app.get("/api/admin/feedback")
async def api_admin_feedback(request: Request):
    """Admin endpoint — list recent feedback."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    limit = int(request.query_params.get("limit", "100"))
    unreviewed = request.query_params.get("unreviewed", "false").lower() == "true"
    items = _auth_db.list_feedback(limit=limit, unreviewed_only=unreviewed)
    summary = _auth_db.get_feedback_summary()
    return JSONResponse({"feedback": items, "summary": summary})


# ─── Admin / Founder Dashboard ────────────────────────────────────────────────

_ADMIN_PW_HASH = hashlib.sha256(
    os.getenv("ADMIN_PASSWORD", "").encode()
).hexdigest()
_ADMIN_DASHBOARD_HTML = Path(__file__).parent / "admin" / "dashboard.html"


def _require_admin(request: Request) -> bool:
    cookie = request.cookies.get("admin_session", "")
    if not _ADMIN_PW_HASH or _ADMIN_PW_HASH == hashlib.sha256(b"").hexdigest():
        return False  # Refuse access if ADMIN_PASSWORD is not set
    return _hmac.compare_digest(cookie, _ADMIN_PW_HASH)


@app.get("/admin")
async def admin_dashboard(request: Request):
    if not _require_admin(request):
        # Serve an inline login form
        login_html = """<!DOCTYPE html><html><head><title>CogniESL Admin</title>
<style>body{font-family:system-ui;background:#0f172a;display:flex;align-items:center;
justify-content:center;min-height:100vh;margin:0;}
.box{background:#1e293b;border-radius:12px;padding:32px;width:320px;}
h1{color:#f8fafc;font-size:18px;margin:0 0 24px;}
input{width:100%;box-sizing:border-box;background:#0f172a;border:1px solid #334155;
border-radius:8px;color:#f8fafc;padding:10px 12px;font-size:14px;margin-bottom:16px;}
button{width:100%;background:#0d9488;color:#fff;border:none;border-radius:8px;
padding:10px;font-size:14px;font-weight:600;cursor:pointer;}
.err{color:#f87171;font-size:13px;margin-top:12px;display:none;}
</style></head><body><div class="box">
<h1>🔒 CogniESL Admin</h1>
<form id="f">
<input type="password" id="pw" placeholder="Admin password" autofocus />
<button type="submit">Sign in</button>
<div class="err" id="err">Incorrect password</div>
</form>
<script>
document.getElementById('f').onsubmit=async function(e){e.preventDefault();
const r=await fetch('/admin/login',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({password:document.getElementById('pw').value})});
if(r.ok){location.reload();}else{document.getElementById('err').style.display='block';}
};
</script></div></body></html>"""
        return HTMLResponse(login_html)
    if _ADMIN_DASHBOARD_HTML.exists():
        return FileResponse(str(_ADMIN_DASHBOARD_HTML))
    return JSONResponse({"error": "Dashboard HTML not found"}, status_code=404)


@app.post("/admin/login")
async def admin_login(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    pw = body.get("password", "")
    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    if not _hmac.compare_digest(pw_hash, _ADMIN_PW_HASH):
        return JSONResponse({"error": "Invalid password"}, status_code=401)
    response = JSONResponse({"ok": True})
    response.set_cookie("admin_session", pw_hash, httponly=True, max_age=28800, samesite="strict")
    return response


@app.get("/api/admin/overview")
async def api_admin_overview(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    week_ago = (now - timedelta(days=7)).isoformat()

    db = _auth_db._conn()

    # --- Live Pulse ---
    gens_today = db.execute(
        "SELECT COUNT(*) FROM generations WHERE created_at >= ?", (today_start,)
    ).fetchone()[0]
    signups_today = db.execute(
        "SELECT COUNT(*) FROM users WHERE created_at >= ?", (today_start,)
    ).fetchone()[0]
    cost_today = db.execute(
        "SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at >= ?", (today_start,)
    ).fetchone()[0]
    gens_month = db.execute(
        "SELECT COUNT(*) FROM generations WHERE created_at >= ?", (month_start,)
    ).fetchone()[0]
    cost_month = db.execute(
        "SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at >= ?", (month_start,)
    ).fetchone()[0]

    # --- Users by tier ---
    tier_counts_rows = db.execute(
        "SELECT subscription_tier, COUNT(*) as cnt FROM users GROUP BY subscription_tier"
    ).fetchall()
    tier_counts = {r["subscription_tier"]: r["cnt"] for r in tier_counts_rows}
    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    # --- Revenue proxy ---
    pro_count = tier_counts.get("pro", 0)
    founding_count = tier_counts.get("founding_member", 0)
    mrr_proxy = pro_count * 10.50 + founding_count * 7.0

    # --- Top grammar points ---
    top_grammar = db.execute(
        """SELECT grammar_point, COUNT(*) as cnt FROM generations
           WHERE grammar_point != '' GROUP BY grammar_point
           ORDER BY cnt DESC LIMIT 10"""
    ).fetchall()

    # --- Top L1 languages ---
    top_l1 = db.execute(
        """SELECT l1_languages, COUNT(*) as cnt FROM generations
           WHERE l1_languages != '' GROUP BY l1_languages
           ORDER BY cnt DESC LIMIT 10"""
    ).fetchall()

    # --- Waitlist count ---
    waitlist_count = db.execute("SELECT COUNT(*) FROM waitlist").fetchone()[0]

    # --- All-time generation total ---
    total_gens = db.execute("SELECT COUNT(*) FROM generations").fetchone()[0]

    # --- Active jobs (from jobs DB) ---
    active_jobs = 0
    try:
        jobs_db_path = Path(__file__).parent / "agent" / "jobs.db"
        if not jobs_db_path.exists():
            jobs_db_path = Path(__file__).parent / "jobs.db"
        if jobs_db_path.exists():
            import sqlite3 as _sqlite3
            jconn = _sqlite3.connect(str(jobs_db_path))
            jconn.row_factory = _sqlite3.Row
            active_jobs = jconn.execute(
                "SELECT COUNT(*) FROM jobs WHERE status='running'"
            ).fetchone()[0]
    except Exception:
        pass

    # --- Failed jobs last 7 days ---
    failed_jobs = []
    try:
        if jobs_db_path.exists():
            rows = jconn.execute(
                """SELECT id, status, created_at, error_message, grammar_point, l1_languages
                   FROM jobs WHERE status='error' AND created_at >= ?
                   ORDER BY created_at DESC LIMIT 20""",
                (week_ago,)
            ).fetchall()
            failed_jobs = [dict(r) for r in rows]
    except Exception:
        pass

    db.close()

    return JSONResponse({
        "pulse": {
            "gens_today": gens_today,
            "active_jobs": active_jobs,
            "signups_today": signups_today,
            "cost_today_usd": round(cost_today, 4),
        },
        "monthly": {
            "gens_month": gens_month,
            "cost_month_usd": round(cost_month, 4),
            "mrr_proxy_usd": round(mrr_proxy, 2),
        },
        "users": {
            "total": total_users,
            "by_tier": tier_counts,
            "founding_slots_used": founding_count,
            "founding_slots_total": _FOUNDING_MEMBER_SLOTS_TOTAL,
            "waitlist": waitlist_count,
        },
        "totals": {
            "all_time_gens": total_gens,
        },
        "top_grammar": [{"grammar": r["grammar_point"], "count": r["cnt"]} for r in top_grammar],
        "top_l1": [{"l1": r["l1_languages"], "count": r["cnt"]} for r in top_l1],
        "failed_jobs": failed_jobs,
    })


@app.get("/api/admin/users")
async def api_admin_users(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    page = int(request.query_params.get("page", "1"))
    per_page = int(request.query_params.get("per_page", "50"))
    offset = (page - 1) * per_page
    db = _auth_db._conn()
    total = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    rows = db.execute(
        """SELECT u.id, u.email, u.created_at, u.subscription_tier,
                  (SELECT COUNT(*) FROM generations g WHERE g.user_id=u.id) as total_gens,
                  (SELECT COUNT(*) FROM materials m WHERE m.user_id=u.id) as total_materials
           FROM users u ORDER BY u.created_at DESC LIMIT ? OFFSET ?""",
        (per_page, offset),
    ).fetchall()
    db.close()
    return JSONResponse({
        "users": [dict(r) for r in rows],
        "total": total,
        "page": page,
        "per_page": per_page,
    })


# ─── Admin: feedback resolution ───────────────────────────────────────────────

@app.post("/api/admin/feedback/{feedback_id}/resolve")
async def api_admin_resolve_feedback(request: Request, feedback_id: str):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    resolution = body.get("resolution", "")
    ok = _auth_db.resolve_feedback(feedback_id, resolution)
    if not ok:
        return JSONResponse({"error": "Feedback not found"}, status_code=404)
    return JSONResponse({"ok": True})


# ─── Admin: user drill-down ───────────────────────────────────────────────────

@app.get("/api/admin/users/{user_id}")
async def api_admin_user_detail(request: Request, user_id: str):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    activity = _auth_db.get_user_activity(user_id)
    if not activity:
        return JSONResponse({"error": "User not found"}, status_code=404)
    return JSONResponse(activity)


# ─── Admin: event timeline ────────────────────────────────────────────────────

@app.get("/api/admin/events")
async def api_admin_events(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    event_type = request.query_params.get("event_type") or None
    limit = int(request.query_params.get("limit", "200"))
    offset = int(request.query_params.get("offset", "0"))
    events = _auth_db.get_events_timeline(event_type=event_type, limit=limit, offset=offset)
    by_type = _auth_db.count_events_by_type(days=30)
    return JSONResponse({"events": events, "by_type": by_type})


# ─── Admin: engagement stats ──────────────────────────────────────────────────

@app.get("/api/admin/engagement")
async def api_admin_engagement(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse(_auth_db.get_engagement_stats())


# ─── Admin: agent actions ─────────────────────────────────────────────────────

@app.get("/api/admin/agent-actions")
async def api_admin_agent_actions(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    status = request.query_params.get("status") or None
    agent_name = request.query_params.get("agent_name") or None
    limit = int(request.query_params.get("limit", "50"))
    items = _auth_db.list_agent_actions(status=status, agent_name=agent_name, limit=limit)
    return JSONResponse({"actions": items})


@app.post("/api/admin/agent-actions/{action_id}/resolve")
async def api_admin_resolve_agent_action(request: Request, action_id: str):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    status_val = body.get("status", "")
    if status_val not in ("approved", "rejected"):
        return JSONResponse({"error": "status must be 'approved' or 'rejected'"}, status_code=400)
    notes = body.get("notes", "")
    ok = _auth_db.resolve_agent_action(action_id, status_val, notes)
    if not ok:
        return JSONResponse({"error": "Action not found"}, status_code=404)
    return JSONResponse({"ok": True})


@app.get("/api/admin/agent-reports")
async def api_admin_agent_reports(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse(_auth_db.get_agent_action_summary())


# ─── Admin: churn risk ────────────────────────────────────────────────────────

@app.get("/api/admin/churn-risk")
async def api_admin_churn_risk(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse({"at_risk_users": _auth_db.compute_churn_risk_scores()})


# ─── Admin: engagement funnel ─────────────────────────────────────────────────

@app.get("/api/admin/funnel")
async def api_admin_funnel(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse(_auth_db.get_engagement_funnel())


# ─── Admin: content quality signals ───────────────────────────────────────────

@app.get("/api/admin/content-quality")
async def api_admin_content_quality(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return JSONResponse(_auth_db.get_content_quality_signals())


# ─── Admin: trends (daily snapshots) ──────────────────────────────────────────

@app.get("/api/admin/trends")
async def api_admin_trends(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    days = int(request.query_params.get("days", "30"))
    snapshots = _auth_db.get_daily_snapshots(days=days)
    return JSONResponse({"snapshots": snapshots})


# ─── Admin: daily digest ──────────────────────────────────────────────────────

@app.get("/api/admin/daily-digest")
async def api_admin_daily_digest(request: Request):
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    db = _auth_db._conn()
    gens_today = db.execute("SELECT COUNT(*) FROM generations WHERE created_at>=?", (today_start,)).fetchone()[0]
    gens_yesterday = db.execute("SELECT COUNT(*) FROM generations WHERE created_at>=? AND created_at<?", (yesterday_start, today_start)).fetchone()[0]
    signups_today = db.execute("SELECT COUNT(*) FROM users WHERE created_at>=?", (today_start,)).fetchone()[0]
    signups_yesterday = db.execute("SELECT COUNT(*) FROM users WHERE created_at>=? AND created_at<?", (yesterday_start, today_start)).fetchone()[0]
    cost_today = db.execute("SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at>=?", (today_start,)).fetchone()[0]
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    cost_month = db.execute("SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at>=?", (month_start,)).fetchone()[0]
    tier_rows = db.execute("SELECT subscription_tier, COUNT(*) as cnt FROM users GROUP BY subscription_tier").fetchall()
    tiers = {r["subscription_tier"]: r["cnt"] for r in tier_rows}
    pro_count = tiers.get("pro", 0)
    founding_count = tiers.get("founding_member", 0)
    mrr = pro_count * 10.50 + founding_count * 7.0
    week_ago = (now - timedelta(days=7)).isoformat()
    failed_7d = 0
    try:
        jobs_db_path = Path(__file__).parent / "agent" / "jobs.db"
        if not jobs_db_path.exists():
            jobs_db_path = Path(__file__).parent / "jobs.db"
        if jobs_db_path.exists():
            import sqlite3 as _sql
            jconn = _sql.connect(str(jobs_db_path))
            jconn.row_factory = _sql.Row
            failed_7d = jconn.execute("SELECT COUNT(*) FROM jobs WHERE status='error' AND created_at>=?", (week_ago,)).fetchone()[0]
    except Exception:
        pass
    db.close()
    try:
        _auth_db.take_daily_snapshot()
    except Exception:
        pass
    churn = _auth_db.compute_churn_risk_scores()
    agent_summary = _auth_db.get_agent_action_summary()
    quality = _auth_db.get_content_quality_signals()
    fb_summary = _auth_db.get_feedback_summary()
    actions_needed = []
    critical_churn = [u for u in churn if u["risk_level"] in ("critical", "high")]
    if critical_churn:
        actions_needed.append({
            "type": "churn_risk", "priority": "high",
            "summary": f"{len(critical_churn)} paying users at risk ({len([u for u in churn if u['risk_level']=='critical'])} critical)",
        })
    if agent_summary["pending"] > 0:
        actions_needed.append({
            "type": "agent_approval", "priority": "high" if agent_summary["pending"] > 5 else "medium",
            "summary": f"{agent_summary['pending']} agent proposals awaiting your review",
        })
    if fb_summary.get("unreviewed", 0) > 0:
        actions_needed.append({
            "type": "feedback_review", "priority": "medium",
            "summary": f"{fb_summary['unreviewed']} unreviewed feedback items",
        })
    if quality.get("issue_rate_pct", 0) > 15:
        actions_needed.append({
            "type": "content_quality", "priority": "medium",
            "summary": f"Content issue rate is {quality['issue_rate_pct']}% (threshold: 15%)",
        })
    actions_needed.sort(key=lambda x: 0 if x["priority"] == "high" else 1)
    today_str = now.strftime("%Y-%m-%d")
    return JSONResponse({
        "date": today_str,
        "generated_at": now.isoformat(),
        "at_a_glance": {
            "gens_today": gens_today,
            "signups_today": signups_today,
            "active_users_7d": _auth_db.get_engagement_stats().get("wau", 0),
            "mrr_usd": round(mrr, 2),
            "api_cost_today_usd": round(cost_today, 4),
            "api_cost_month_usd": round(cost_month, 4),
        },
        "actions_needed": actions_needed,
        "agent_status": {
            "pending_approvals": agent_summary["pending"],
            "approved_last_7d": agent_summary["approved_last_7d"],
            "rejected_last_7d": agent_summary["rejected_last_7d"],
        },
        "system_health": {
            "failed_jobs_7d": failed_7d,
            "content_issue_rate_pct": quality.get("issue_rate_pct", 0),
            "unreviewed_feedback": fb_summary.get("unreviewed", 0),
            "users_at_risk": len(churn),
        },
    })


# ─── Stripe billing endpoints ─────────────────────────────────────────────────

import hmac as _hmac
import stripe as _stripe
import json as _json

_stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
_STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
_FOUNDING_MEMBER_SLOTS_TOTAL = int(os.getenv("FOUNDING_MEMBER_SLOTS_TOTAL", "100"))


@app.post("/api/stripe/create-checkout")
async def api_create_checkout(request: Request):
    """Create a Stripe Checkout Session and return the URL."""
    user, err = _require_auth(request)
    if err:
        return err
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    price_id = body.get("price_id", "").strip()
    if not price_id:
        return JSONResponse({"error": "price_id required"}, status_code=400)
    if not _stripe.api_key:
        return JSONResponse({"error": "Stripe not configured"}, status_code=503)

    base_url = os.getenv("BASE_URL", "https://cogniesl.com")
    try:
        # Create a Stripe customer linked to this user
        customer = _stripe.Customer.create(
            email=user.email,
            metadata={"user_id": user.id},
        )
        _auth_db.set_stripe_customer_id(user.id, customer.id)

        session = _stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=f"{base_url}/materials?upgraded=1",
            cancel_url=f"{base_url}/pricing",
            subscription_data={"metadata": {"user_id": user.id}},
        )
        return JSONResponse({"checkout_url": session.url})
    except _stripe.error.StripeError as e:
        logging.error(f"Stripe checkout error: {e}")
        return JSONResponse({"error": str(e.user_message)}, status_code=400)


@app.post("/api/stripe/webhook")
async def api_stripe_webhook(request: Request):
    """Handle Stripe webhook events to update subscription tiers."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        event = _stripe.Webhook.construct_event(payload, sig_header, _STRIPE_WEBHOOK_SECRET)
    except _stripe.error.SignatureVerificationError:
        return JSONResponse({"error": "Invalid signature"}, status_code=400)
    except Exception as e:
        logging.error(f"Stripe webhook error: {e}")
        return JSONResponse({"error": "Webhook error"}, status_code=400)

    event_type = event["type"]
    logging.info(f"[Stripe] Event: {event_type} id={event['id']}")

    if event_type in ("customer.subscription.created", "customer.subscription.updated"):
        sub = event["data"]["object"]
        status = sub.get("status", "")
        price_id = ""
        try:
            price_id = sub["items"]["data"][0]["price"]["id"]
        except (KeyError, IndexError):
            pass
        founding_price = os.getenv("STRIPE_FOUNDING_PRICE_ID", "")
        is_founding = founding_price and price_id == founding_price
        if status == "active":
            new_tier = "founding_member" if is_founding else "pro"
        else:
            new_tier = "free"

        # Resolve user by metadata or customer ID
        user_id = (sub.get("metadata") or {}).get("user_id") or ""
        if not user_id:
            stripe_cust_id = sub.get("customer", "")
            u = _auth_db.get_user_by_stripe_customer_id(stripe_cust_id)
            if u:
                user_id = u.id
        if user_id:
            _auth_db.update_subscription_tier(user_id, new_tier)
            _auth_db.record_subscription_event(
                user_id=user_id,
                stripe_event_id=event["id"],
                event_type=event_type,
                subscription_status=status,
                new_tier=new_tier,
                raw_json=_json.dumps({"price_id": price_id, "status": status}),
            )
            logging.info(f"[Stripe] Updated user {user_id} → {new_tier}")

    elif event_type == "customer.subscription.deleted":
        sub = event["data"]["object"]
        user_id = (sub.get("metadata") or {}).get("user_id") or ""
        if not user_id:
            stripe_cust_id = sub.get("customer", "")
            u = _auth_db.get_user_by_stripe_customer_id(stripe_cust_id)
            if u:
                user_id = u.id
        if user_id:
            _auth_db.update_subscription_tier(user_id, "free")
            _auth_db.record_subscription_event(
                user_id=user_id,
                stripe_event_id=event["id"],
                event_type=event_type,
                subscription_status="canceled",
                new_tier="free",
            )
            logging.info(f"[Stripe] Downgraded user {user_id} → free")

    return JSONResponse({"received": True})


# ─── Orchestrator API endpoints (Phase I-3) ────────────────────────────────────

@app.get("/api/admin/orchestrator/status")
async def api_admin_orchestrator_status(request: Request):
    """Get the most recent orchestrator run and agent health."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    status = _auth_db.get_orchestrator_status()
    health = _auth_db.get_all_agent_health()
    return JSONResponse({
        "last_run": status,
        "agent_health": health,
    })


@app.post("/api/admin/orchestrator/run")
async def api_admin_orchestrator_run(request: Request):
    """Trigger a manual orchestrator run."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    try:
        from agent.orchestrator import run_orchestrator
        digest = run_orchestrator(run_type="manual")
        return JSONResponse({"ok": True, "digest": digest})
    except Exception as e:
        logging.error(f"Manual orchestrator run failed: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/admin/orchestrator/history")
async def api_admin_orchestrator_history(request: Request):
    """Get recent orchestrator run history."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    limit = int(request.query_params.get("limit", "30"))
    history = _auth_db.get_orchestrator_history(limit=limit)
    return JSONResponse({"runs": history})


@app.get("/api/admin/agent-health")
async def api_admin_agent_health(request: Request):
    """Get health status for all department agents."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    health = _auth_db.get_all_agent_health()
    return JSONResponse({"agents": health})


@app.get("/api/admin/alerts")
async def api_admin_alerts(request: Request):
    """Get active (unresolved) critical alerts."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    alerts = _auth_db.get_active_alerts()
    return JSONResponse({"alerts": alerts})


@app.post("/api/admin/alerts/{alert_id}/acknowledge")
async def api_admin_acknowledge_alert(alert_id: str, request: Request):
    """Marcos acknowledges a critical alert."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    _auth_db.acknowledge_alert(alert_id)
    return JSONResponse({"ok": True})


@app.post("/api/admin/alerts/{alert_id}/resolve")
async def api_admin_resolve_alert(alert_id: str, request: Request):
    """Marcos resolves a critical alert."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    _auth_db.resolve_alert(alert_id, marcos_notes=body.get("notes", ""))
    return JSONResponse({"ok": True})


@app.get("/api/admin/costs/daily")
async def api_admin_daily_costs(request: Request):
    """Get today's costs broken down by agent."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    from datetime import datetime, timezone
    costs = _auth_db.get_daily_agent_costs()
    return JSONResponse({"costs": costs, "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")})


@app.get("/api/admin/costs/weekly")
async def api_admin_weekly_costs(request: Request):
    """Get 7-day cost trend."""
    if not _require_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    costs = _auth_db.get_weekly_agent_costs()
    return JSONResponse({"costs": costs})


# ─── Stripe (existing endpoints follow) ────────────────────────────────────────
async def api_founding_member_status():
    """Public endpoint: how many founding member slots are used vs. total."""
    slots_used = _auth_db.count_founding_members()
    return JSONResponse({
        "slots_used": slots_used,
        "slots_total": _FOUNDING_MEMBER_SLOTS_TOTAL,
    })



if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=300)