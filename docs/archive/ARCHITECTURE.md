# CogniESL — Architecture Document

> May 2026 — Single-Agent Architecture

---

## 1. Overview

CogniESL is an AI-powered ESL teaching material generator built on a **single-agent architecture** using the [Agency Swarm](https://github.com/agency-swarm/agency-swarm) framework. One agent handles the entire workflow: conversing with teachers, searching the database, and generating professional teaching materials (slides, worksheets, activities).

### Why Single-Agent?

The previous multi-agent architecture (Orchestrator → Intake → Pedagogy → Production) was slow, unreliable, and expensive. Key problems:

- **gpt-4o-mini** couldn't reliably follow complex multi-agent instructions
- Agent-to-agent handoffs introduced latency and failure points
- Session state didn't survive across HTTP requests
- 5x more API calls per conversation

The single agent does everything in one context: requirement gathering, database search, material generation, and file delivery.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Teacher (Browser)                   │
│                         │                                │
│                    HTTP POST                             │
│                  /api/chat (Next.js)                     │
│                         │                                │
│                    ▼                                     │
│  ┌──────────────────────────────────┐                   │
│  │     Next.js Web UI               │                   │
│  │  - Chat interface                │                   │
│  │  - Session ID (localStorage)     │                   │
│  │  - X-Session-ID header           │                   │
│  └──────────────┬───────────────────┘                   │
│                 │ HTTP POST                               │
│                 │ /cogniesl/get_response                  │
│                 │ X-Session-ID header                     │
│                 ▼                                         │
│  ┌──────────────────────────────────┐                   │
│  │     FastAPI Server (server.py)   │                   │
│  │  - Session-based agent store     │                   │
│  │  - 30-min session timeout        │                   │
│  │  - Response cleanup (regex)      │                   │
│  └──────────────┬───────────────────┘                   │
│                 │                                         │
│                 ▼                                         │
│  ┌──────────────────────────────────┐                   │
│  │     CogniESL Agent (Agency Swarm)│                   │
│  │                                  │                   │
│  │  ┌────────────────────────────┐  │                   │
│  │  │ Custom Tools               │  │                   │
│  │  │ - SearchGrammarTool        │  │                   │
│  │  │ - GetL1InterferenceTool    │  │                   │
│  │  │ - SearchActivitiesTool     │  │                   │
│  │  └────────────────────────────┘  │                   │
│  │  ┌────────────────────────────┐  │                   │
│  │  │ Slides Tools (17 tools)    │  │                   │
│  │  │ - InsertNewSlides          │  │                   │
│  │  │ - ModifySlide              │  │                   │
│  │  │ - BuildPptxFromHtmlSlides  │  │                   │
│  │  │ - ManageTheme              │  │                   │
│  │  │ - CheckSlide               │  │                   │
│  │  │ - SlideScreenshot          │  │                   │
│  │  │ - GenerateImage            │  │                   │
│  │  │ - ImageSearch              │  │                   │
│  │  │ - ... (9 more)             │  │                   │
│  │  └────────────────────────────┘  │                   │
│  │  ┌────────────────────────────┐  │                   │
│  │  │ Docs Tools (6 tools)       │  │                   │
│  │  │ - CreateDocument           │  │                   │
│  │  │ - ConvertDocument          │  │                   │
│  │  │ - ModifyDocument           │  │                   │
│  │  │ - ViewDocument             │  │                   │
│  │  │ - ListDocuments            │  │                   │
│  │  │ - RestoreDocument          │  │                   │
│  │  └────────────────────────────┘  │                   │
│  │  ┌────────────────────────────┐  │                   │
│  │  │ Utility Tools              │  │                   │
│  │  │ - IPythonInterpreter       │  │                   │
│  │  │ - WebSearchTool            │  │                   │
│  │  │ - ReadFile                 │  │                   │
│  │  │ - CopyFile                 │  │                   │
│  │  └────────────────────────────┘  │                   │
│  └──────────────┬───────────────────┘                   │
│                 │                                         │
│                 ▼                                         │
│  ┌──────────────────────────────────┐                   │
│  │     Data Layer (YAML files)      │                   │
│  │  - data/grammar/ (300 files)     │                   │
│  │  - data/activities/ (218 files)  │                   │
│  │  - data/l1-interference/ (34)    │                   │
│  └──────────────────────────────────┘                   │
│                                                           │
│  ┌──────────────────────────────────┐                   │
│  │     Output                       │                   │
│  │  - ./mnt/{topic}/presentations/  │                   │
│  │  - ./mnt/{topic}/documents/      │                   │
│  └──────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Folder Structure

```
CogniESL/
├── agent/                          # Single agent + all tools
│   ├── config.py                   # Model configuration (LiteLLM routing)
│   ├── cogniesl_agent.py           # Agent definition + tool registration
│   ├── instructions.md             # Agent system prompt (~250 lines)
│   ├── patches/                    # Runtime monkey-patches for agency_swarm
│   │   ├── patch_agency_swarm_dual_comms.py
│   │   ├── patch_file_attachment_refs.py
│   │   ├── patch_ipython_interpreter_composio.py
│   │   └── patch_utf8_file_reads.py
│   ├── tools/                      # Custom database search tools
│   │   ├── __init__.py
│   │   ├── SearchGrammarTool.py    # Fuzzy grammar search (5 strategies)
│   │   ├── GetL1InterferenceTool.py # L1 pattern lookup
│   │   └── SearchActivitiesTool.py # Activity search by topic/level/age
│   ├── slides_tools/               # PPTX generation tools (17 tools)
│   │   ├── __init__.py
│   │   ├── InsertNewSlides.py
│   │   ├── ModifySlide.py
│   │   ├── BuildPptxFromHtmlSlides.py
│   │   ├── ManageTheme.py
│   │   ├── CheckSlide.py
│   │   ├── CheckSlideCanvasOverflow.py
│   │   ├── SlideScreenshot.py
│   │   ├── ReadSlide.py
│   │   ├── DeleteSlide.py
│   │   ├── RestoreSnapshot.py
│   │   ├── CreatePptxThumbnailGrid.py
│   │   ├── GenerateImage.py
│   │   ├── ImageSearch.py
│   │   ├── DownloadImage.py
│   │   ├── EnsureRasterImage.py
│   │   ├── ApplyPptxTextReplacements.py
│   │   ├── ExtractPptxTextInventory.py
│   │   ├── CreateImageMontage.py
│   │   ├── RearrangePptxSlidesFromTemplate.py
│   │   ├── slide_file_utils.py     # Path resolution for slide output
│   │   ├── deck_utils.py           # Theme/test deck utilities
│   │   ├── html_writer_instructions.md
│   │   ├── html2pptx_runner.js
│   │   ├── render_slides.py
│   │   ├── slide_html_utils.py
│   │   └── template_registry.py
│   ├── docs_tools/                 # Document generation tools (6 tools)
│   │   ├── __init__.py
│   │   ├── CreateDocument.py
│   │   ├── ConvertDocument.py
│   │   ├── ModifyDocument.py
│   │   ├── ViewDocument.py
│   │   ├── ListDocuments.py
│   │   ├── RestoreDocument.py
│   │   └── utils/                  # HTML-to-DOCX conversion engine
│   │       ├── doc_file_utils.py   # Path resolution for doc output
│   │       ├── html_docx_core.py
│   │       ├── html_docx_blocks.py
│   │       ├── html_docx_css.py
│   │       ├── html_docx_images.py
│   │       ├── html_docx_page.py
│   │       ├── html_docx_paragraphs.py
│   │       ├── html_docx_playwright.py
│   │       ├── html_docx_selectors.py
│   │       ├── html_docx_shared.py
│   │       ├── html_docx_tables.py
│   │       ├── html_docx_constants.py
│   │       └── html_validation.py
│   ├── shared_tools/               # Cross-cutting utilities
│   │   ├── __init__.py
│   │   ├── CopyFile.py             # File copy with path normalization
│   │   ├── ExecuteTool.py
│   │   ├── FindTools.py
│   │   ├── ManageConnections.py
│   │   ├── SearchTools.py
│   │   ├── model_availability.py   # Provider capability checks
│   │   └── openai_client_utils.py  # OpenAI credential helpers
│   └── utility_tools/              # File system tools
│       ├── ReadFile.py
│       ├── WriteFile.py
│       ├── EditFile.py
│       └── ListDirectory.py
├── data/                           # YAML database
│   ├── grammar/                    # 300 grammar point files
│   ├── activities/                 # 218 activity files
│   └── l1-interference/            # 34 L1 interference files
│       ├── portuguese_interference.yaml
│       ├── spanish_interference.yaml
│       ├── ... (32 more)
│       ├── enrichment_data/        # Supplementary data (not loaded by tools)
│       └── hand_curated/           # Manual curation (not loaded by tools)
├── webui/                          # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Main page with header + chat
│   │   │   ├── layout.tsx          # Root layout (Inter + Nunito fonts)
│   │   │   ├── globals.css         # Tailwind + custom theme vars
│   │   │   └── api/chat/
│   │   │       └── route.ts        # API proxy to FastAPI backend
│   │   └── components/
│   │       └── ChatInterface.tsx   # Chat UI with session management
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.ts
├── server.py                       # FastAPI entry point
├── .env                            # Environment configuration
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container definition
├── railway.json                    # Railway deployment config
└── docs/                           # Project documentation
    ├── ARCHITECTURE.md             # This file
    ├── CLAUDE_CODE_HANDOFF.md      # AI developer handoff
    ├── CONCEPT.md                  # Product concept
    ├── DATA_FORMAT.md              # YAML data file specifications
    ├── DEPLOYMENT.md               # Deployment guide
    ├── TOOLS_REFERENCE.md          # Tool-by-tool reference
    └── TROUBLESHOOTING.md          # Common issues and fixes
```

---

## 4. Request Flow

### 4.1 End-to-End Flow

```
1. Teacher types message in Web UI
2. ChatInterface sends POST /api/chat { message, X-Session-ID }
3. Next.js API route proxies to FastAPI: POST /cogniesl/get_response
4. FastAPI looks up or creates agent for session_id
5. Agent processes message through its full workflow:
   a. If gathering requirements: responds with questions/confirmation
   b. If confirmed: searches database (grammar → L1 → activities)
   c. Generates materials (slides via slides_tools, docs via docs_tools)
   d. Returns file paths and summary
6. FastAPI cleans response (removes leaked internal context)
7. Response flows back through Next.js → Web UI → Teacher
```

### 4.2 Session Management

- **Session ID**: Generated in browser localStorage (`cogniesl_session_id`), format: `sess_{timestamp}_{random}`
- **Session store**: In-memory dict in `server.py`, keyed by session ID
- **Session timeout**: 30 minutes of inactivity
- **Agent persistence**: Agency Swarm maintains conversation context internally — no chat_history passing needed
- **Header**: `X-Session-ID` carries the session identifier through the full stack

### 4.3 Model Configuration

- **Provider**: OpenRouter (via LiteLLM)
- **Format**: `openrouter/{provider}/{model}` (e.g., `openrouter/anthropic/claude-haiku-4.5`)
- **Routing**: `config.py` detects `/` in model name → wraps in `LitellmModel`
- **Testing model**: `openrouter/anthropic/claude-haiku-4.5` ($1/$5 per 1M tokens)
- **Production model**: `openrouter/anthropic/claude-sonnet-4.5` ($3/$15 per 1M tokens)

---

## 5. Key Design Decisions

### 5.1 Single Agent vs. Multi-Agent

| Aspect | Multi-Agent (Old) | Single-Agent (New) |
|--------|-------------------|-------------------|
| Agents | 5 (Orchestrator, Intake, Pedagogy, Slides, Docs) | 1 |
| API calls per session | ~15-25 | ~3-5 |
| Latency | 60-120s | 15-30s |
| Failure points | Handoff chain | None |
| Cost | ~$0.05/session | ~$0.01/session |
| Instruction following | Poor (gpt-4o-mini) | Good (Haiku 4.5+) |

### 5.2 Session-Based Agency Store

The old architecture created a new agency per request. The new one keeps agents in a dict, keyed by session ID. Agency Swarm maintains conversation state internally, so we only send the new message each time.

### 5.3 No chat_history Passing

Previous versions sent the full conversation history with each request. This caused loops where the agent would re-read old context and repeat itself. Now the agent maintains its own state.

### 5.4 Response Cleanup

The FastAPI server applies regex cleanup to remove any leaked internal context:
- `<memory-context>...</memory-context>` blocks
- `[System note:...]` annotations
- Excessive newlines

### 5.5 Path Resolution

All tools resolve the data/output directory using `Path(__file__).parents[N]`:
- `agent/tools/*.py` → `parents[2]` → `CogniESL/data/`
- `agent/slides_tools/*.py` → `parents[2]` → `CogniESL/mnt/`
- `agent/docs_tools/utils/*.py` → `parents[3]` → `CogniESL/mnt/`

Docker override: Set `COGNIESL_DATA_DIR` env var to `/app/data`.

---

## 6. Patches

Four runtime monkey-patches are applied when the agent is created:

| Patch | What It Does |
|-------|-------------|
| `patch_agency_swarm_dual_comms.py` | Enables dual communication channels in agency_swarm |
| `patch_file_attachment_refs.py` | Fixes file attachment reference handling |
| `patch_ipython_interpreter_composio.py` | Adds Composio context to IPython interpreter |
| `patch_utf8_file_reads.py` | Ensures UTF-8 encoding for all file reads |

These are imported and applied in `create_cogniesl_agent()` before any tools are loaded.

---

## 7. Data Flow for Material Generation

```
Teacher confirms requirements
         │
         ▼
SearchGrammarTool(topic)
  → Reads data/grammar/{slug}.yaml
  → Returns: meaning, form, sub_rules, phonetics, common_errors, etc.
         │
         ▼
GetL1InterferenceTool(grammar_point, language)
  → Reads data/l1-interference/{language}_interference.yaml
  → Returns: interference_patterns, examples, teacher_tips
         │
         ▼
SearchActivitiesTool(topic, level, age_group)
  → Scans data/activities/*.yaml
  → Returns: matching activities with instructions, scripts, materials
         │
         ▼
Agent generates materials using slides_tools + docs_tools
  → Slides: HTML → BuildPptxFromHtmlSlides → PPTX
  → Docs: HTML → CreateDocument → DOCX → ConvertDocument → PDF
         │
         ▼
Output files in ./mnt/{topic-slug}/
  ├── presentations/{topic}-slides.pptx
  └── documents/{topic}-worksheet.docx
  └── documents/{topic}-worksheet.pdf
```

---

## 8. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | OpenRouter API key (prefixed `sk-or-v1-`) |
| `DEFAULT_MODEL` | Yes | — | Model ID (e.g., `openrouter/anthropic/claude-haiku-4.5`) |
| `PORT` | No | `8080` | FastAPI server port |
| `COGNIESL_DATA_DIR` | No | `../data` | Override data directory path (used in Docker) |
| `OPENSWARM_URL` | Yes (Web UI) | `http://localhost:8080` | Backend URL for Next.js API route |

---

## 9. Deployment

- **Platform**: Railway (backend), Vercel (frontend) — or monolith on Railway
- **Container**: Python 3.12-slim with Node.js 20 LTS
- **Build**: `pip install -r requirements.txt` → `playwright install chromium`
- **Start**: `python server.py` (uvicorn on 0.0.0.0:8080)
- **Health check**: `GET /` → `{"status": "ok", "service": "CogniESL"}`

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.
