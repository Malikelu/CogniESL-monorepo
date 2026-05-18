# FastAPI entry point — run with: python server.py

import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

import uvicorn
from cogniesl_swarm import create_agency
from agency_swarm.integrations.fastapi import run_fastapi

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app = run_fastapi(
        agencies={
            "cogniesl": create_agency,
        },
        port=port,
        enable_logging=True,
        return_app=True,
        allowed_local_file_dirs=[
            "./uploads",
        ],
    )

    @app.get("/")
    async def healthcheck():
        return {"status": "ok", "service": "CogniESL"}

    uvicorn.run(app, host="0.0.0.0", port=port, ws="websockets-sansio")
