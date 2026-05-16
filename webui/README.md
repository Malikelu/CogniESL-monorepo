# CogniESL Web UI

This directory will contain the Next.js chat interface that connects to OpenSwarm's FastAPI API.

## Status: Placeholder — To be built in Phase 5

## Plan
- Next.js 16 app with Tailwind v4
- Same design identity as marketing site (teal/coral/gold, Inter+Nunito)
- Chat interface → OpenSwarm FastAPI (port 8080)
- Features: chat, material history, download center
- Deploy to Vercel (separate from OpenSwarm backend on Railway)

## API Contract
The Web UI will communicate with OpenSwarm's FastAPI server:
- `POST /api/chat` — Send message, get response
- `GET /api/sessions` — List chat sessions
- `GET /api/files/:id` — Download generated files
