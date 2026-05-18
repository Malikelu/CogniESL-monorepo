# FastAPI entry point — run with: python server.py

import logging
import os
import time
from collections import defaultdict
from threading import Lock
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from cogniesl_swarm import create_agency

# Session-based agency store
_agencies: dict[str, object] = {}
_last_access: dict[str, float] = {}
_lock = Lock()

# Cleanup sessions older than 30 minutes
SESSION_TIMEOUT = 1800


def get_agency(session_id: str):
    """Get or create a persistent agency for a session."""
    with _lock:
        now = time.time()
        # Cleanup old sessions
        expired = [sid for sid, t in _last_access.items() if now - t > SESSION_TIMEOUT]
        for sid in expired:
            del _agencies[sid]
            del _last_access[sid]
            logging.info(f"Cleaned up expired session: {sid}")

        if session_id not in _agencies:
            logging.info(f"Creating new agency for session: {session_id}")
            _agencies[session_id] = create_agency()

        _last_access[session_id] = now
        return _agencies[session_id]


app = FastAPI()


@app.get("/")
async def healthcheck():
    return {"status": "ok", "service": "CogniESL"}


@app.post("/cogniesl/get_response")
async def get_response(request: Request):
    """Persistent agency endpoint — maintains conversation context per session."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status=400)

    message = body.get("message", "")
    if not message:
        return JSONResponse({"error": "Message is required"}, status=400)

    # Get session ID from header or generate from IP
    session_id = request.headers.get("X-Session-ID", request.client.host)

    # Get or create persistent agency
    agency = get_agency(session_id)

    try:
        # Build chat history if provided
        chat_history = body.get("chat_history")

        if chat_history:
            response = agency.get_response_sync(
                message=message,
                chat_history=chat_history,
            )
        else:
            response = agency.get_response_sync(message=message)

        # Extract the response text
        response_text = str(response)

        # Clean up any leaked internal context
        import re
        response_text = re.sub(r"<memory-context>[\s\S]*?</memory-context>", "", response_text)
        response_text = re.sub(r"<memory-context>[\s\S]*", "", response_text)
        response_text = re.sub(r"\[System note:[\s\S]*?\]", "", response_text)
        response_text = re.sub(r"\n{3,}", "\n\n", response_text).strip()

        return JSONResponse({"response": response_text})

    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)
        return JSONResponse(
            {"response": f"Sorry, an error occurred. Please try again."},
            status=200,
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
