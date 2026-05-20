"""CogniESL Server — FastAPI entry point. Run with: python server.py"""
import logging
import os
import re
import time
from pathlib import Path
from threading import Lock
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from agent.cogniesl_agent import create_cogniesl_agent

# Session store: agent + agency_context (for persistent conversation history)
_agents: dict[str, object] = {}
_contexts: dict[str, object] = {}
_last_access: dict[str, float] = {}
_lock = Lock()

SESSION_TIMEOUT = 1800  # 30 minutes


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


# Path to the built web UI (Next.js static export)
_WEBUI_DIR = Path(__file__).parent / "webui" / "out"
_UI_INDEX = _WEBUI_DIR / "index.html" if _WEBUI_DIR.exists() else None

app = FastAPI()

# CORS — allow Next.js dev server (port 3000) to reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount Next.js static export if it exists
if _UI_INDEX and _UI_INDEX.exists():
    _next_static = _WEBUI_DIR / "_next"
    if _next_static.exists():
        app.mount("/_next", StaticFiles(directory=str(_next_static)), name="next_static")
        logging.info(f"Mounted _next/static from {_next_static}")


# Root-level static assets (favicon, svg files in Next.js export root)
_ROOT_ASSETS_DIR = _WEBUI_DIR if (_UI_INDEX and _UI_INDEX.exists()) else None
if _ROOT_ASSETS_DIR:
    app.mount("/root-assets", StaticFiles(directory=str(_ROOT_ASSETS_DIR)), name="root_assets")


def _serve_file_or_index(path: str) -> FileResponse | JSONResponse:
    """Serve a file from the web UI directory, falling back to index.html."""
    if _ROOT_ASSETS_DIR is None:
        return JSONResponse({"error": "No web UI"}, status_code=404)
    file_path = _ROOT_ASSETS_DIR / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    # SPA fallback: serve index.html for all unmatched routes
    if _UI_INDEX and _UI_INDEX.exists():
        return FileResponse(str(_UI_INDEX))
    return JSONResponse({"error": "Not found"}, status_code=404)


@app.get("/")
async def healthcheck():
    # Serve the web UI index if it exists
    if _UI_INDEX and _UI_INDEX.exists():
        return FileResponse(str(_UI_INDEX))
    return {"status": "ok", "service": "CogniESL"}


@app.get("/favicon.ico")
async def favicon():
    return _serve_file_or_index("favicon.ico")


@app.get("/{path:path}")
async def spa_catch_all(path: str):
    """Catch-all for SPA routing - returns index.html after static asset checks."""
    # Skip API paths
    if path.startswith("cogniesl/"):
        return JSONResponse({"error": "Not found"}, status_code=404)
    return _serve_file_or_index(path)


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

    session_id = request.headers.get("X-Session-ID", request.client.host)
    agent, ctx = get_session(session_id)

    try:
        response = await agent.get_response(message=message, agency_context=ctx)
        response_text = str(getattr(response, 'final_output', response))
        response_text = _clean_response(response_text)
        return JSONResponse({"response": response_text})

    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)
        return JSONResponse(
            {"response": "Sorry, an error occurred. Please try again."},
            status_code=200,
        )


@app.api_route("/{path:path}", methods=["GET"])
async def spa_fallback(path: str):
    """Serve the SPA index.html for any frontend routes not matched by API."""
    if path.startswith("api/") or path.startswith("cogniesl/") or path.startswith("_next/"):
        return JSONResponse({"error": "Not found"}, status_code=404)
    _mount_webui(app)
    if _WEBUI_DIR.exists() and (_WEBUI_DIR / "index.html").exists():
        return FileResponse(str(_WEBUI_DIR / "index.html"))
    return JSONResponse({"error": "Not found"}, status_code=404)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)