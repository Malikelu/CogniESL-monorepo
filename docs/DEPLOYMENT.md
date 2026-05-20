# CogniESL — Deployment Guide

> How to build, configure, and deploy CogniESL.

---

## 1. Prerequisites

- OpenRouter API key (https://openrouter.ai/keys)
- Docker (for containerized deployment) OR Python 3.12+ and Node.js 20+ (for direct deployment)
- Railway account (for cloud deployment) OR Vercel account (for frontend)

---

## 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Required: OpenRouter API key
OPENAI_API_KEY=sk-or-v1-your-key-here

# Required: Model selection
# Testing: openrouter/anthropic/claude-haiku-4.5 ($1/$5 per 1M tokens)
# Production: openrouter/anthropic/claude-sonnet-4.5 ($3/$15 per 1M tokens)
DEFAULT_MODEL=openrouter/anthropic/claude-haiku-4.5

# Optional: Server port (default: 8080)
PORT=8080

# Optional: Data directory override (for Docker)
# COGNIESL_DATA_DIR=/app/data
```

For the Web UI, the Next.js API route uses:
```bash
OPENSWARM_URL=http://localhost:8080  # Backend URL
```

---

## 3. Docker Deployment (Recommended)

### Build
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
docker build -t cogniesl .
```

### Run
```bash
docker run -p 8080:8080 --env-file .env cogniesl
```

### Docker Configuration Details
- **Base image**: `python:3.12-slim`
- **Node.js**: 20 LTS (for Playwright/PDF generation)
- **System deps**: git, curl, poppler-utils, Chromium libraries
- **Python deps**: installed from `requirements.txt`
- **Playwright**: Chromium installed at build time
- **Data dir**: `/app/data` (set via `COGNIESL_DATA_DIR`)
- **Output dir**: `/app/mnt` (created at build time)
- **Port**: 8080
- **Start command**: `python -u server.py`

---

## 4. Railway Deployment

### Configuration
The `railway.json` file configures Railway to:
- Build using the root `Dockerfile`
- Health check at `GET /` (expects `{"status": "ok"}`)
- Restart on failure (max 3 retries)

### Steps
1. Push code to GitHub
2. Create new Railway project
3. Connect GitHub repo
4. Set environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
   - `DEFAULT_MODEL`
5. Deploy

### Environment Variables in Railway
```
OPENAI_API_KEY=sk-or-v1-your-key
DEFAULT_MODEL=openrouter/anthropic/claude-sonnet-4.5
```

---

## 5. Local Development

### Backend Only
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Run server
python server.py
# → http://localhost:8080
```

### Web UI Only
```bash
cd webui
npm install
npm run dev
# → http://localhost:3000
```

### Full Stack
1. Start backend: `python server.py` (port 8080)
2. Start frontend: `cd webui && npm run dev` (port 3000)
3. Open http://localhost:3000

---

## 6. Testing the Deployment

### Health Check
```bash
curl http://localhost:8080/
# Expected: {"status": "ok", "service": "CogniESL"}
```

### Full Conversation Test
```bash
# Message 1: Initial request
curl -X POST http://localhost:8080/cogniesl/get_response \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-1" \
  -d '{"message": "I need slides for present simple for Brazilian adults"}'

# Message 2: Provide missing info
curl -X POST http://localhost:8080/cogniesl/get_response \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-1" \
  -d '{"message": "beginner level, slides and worksheets"}'

# Message 3: Confirm
curl -X POST http://localhost:8080/cogniesl/get_response \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-1" \
  -d '{"message": "yes, generate them"}'
```

---

## 7. Monitoring

### Server Logs
The FastAPI server logs:
- Session creation/cleanup
- Errors during message processing
- Agent activity (via agency_swarm logging)

### Key Metrics to Watch
- Response time (target: <30s for conversation, <120s for material generation)
- Error rate (target: <5%)
- Session count (memory usage scales with active sessions)

---

## 8. Scaling Considerations

### Current Architecture
- Single-process FastAPI server
- In-memory session store
- No external database

### Limitations
- Sessions are lost on restart
- Memory usage grows with active sessions
- No horizontal scaling (single process)

### Future Scaling Path
1. Replace in-memory session store with Redis
2. Add multiple workers (`uvicorn --workers 4`)
3. Use external file storage (S3) for generated materials
4. Add load balancer for multiple instances

---

## 9. Updating the Application

### Code Changes
1. Pull latest code
2. Rebuild Docker image: `docker build -t cogniesl .`
3. Redeploy

### Data Updates
1. Add/edit YAML files in `data/`
2. No restart needed — tools read files on each call
3. For Docker: rebuild image to include new data files

### Model Changes
1. Update `DEFAULT_MODEL` in `.env`
2. Restart server
3. No code changes needed (LiteLLM handles routing)
