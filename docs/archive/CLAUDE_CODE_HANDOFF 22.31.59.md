# CogniESL — Claude Code Handoff Document

> May 2026 — Single-Agent Architecture

This document gives a senior AI developer everything needed to understand, debug, and improve the CogniESL project.

---

## 1. Project Summary

CogniESL is an AI-powered ESL teaching material generator. Teachers describe what they need in natural language, and CogniESL generates professional teaching materials (slides, worksheets, activities) tailored to their students' native language (L1).

**Key differentiator**: L1 interference targeting — CogniESL knows that Portuguese speakers say "She work" instead of "She works," and builds materials that specifically address those errors.

---

## 2. Read These Files First (In Order)

1. **`docs/CONCEPT.md`** — Product vision and user experience
2. **`docs/ARCHITECTURE.md`** — System architecture and design decisions
3. **`docs/DATA_FORMAT.md`** — YAML data file specifications
4. **`docs/TOOLS_REFERENCE.md`** — Tool-by-tool reference
5. **`agent/instructions.md`** — The agent's system prompt (the brain)
6. **`agent/cogniesl_agent.py`** — Agent definition and tool registration
7. **`server.py`** — FastAPI server with session management

---

## 3. Complete File Inventory

### Backend Core
| File | Purpose |
|------|---------|
| `server.py` | FastAPI entry point, session store, response cleanup |
| `agent/cogniesl_agent.py` | Agent definition, patch application, tool registration |
| `agent/config.py` | Model configuration with LiteLLM routing |
| `agent/instructions.md` | Agent system prompt (~250 lines) |
| `.env` | Environment variables |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container definition |
| `railway.json` | Railway deployment config |

### Custom Tools (Database Search)
| File | Purpose |
|------|---------|
| `agent/tools/SearchGrammarTool.py` | Fuzzy grammar search (5 matching strategies) |
| `agent/tools/GetL1InterferenceTool.py` | L1 interference pattern lookup |
| `agent/tools/SearchActivitiesTool.py` | Activity search by topic/level/age/L1 |

### Slides Tools (PPTX Generation)
| File | Purpose |
|------|---------|
| `agent/slides_tools/InsertNewSlides.py` | Create new slide placeholders |
| `agent/slides_tools/ModifySlide.py` | Modify slide content |
| `agent/slides_tools/BuildPptxFromHtmlSlides.py` | Convert HTML slides to PPTX |
| `agent/slides_tools/ManageTheme.py` | Manage presentation themes |
| `agent/slides_tools/CheckSlide.py` | Validate slide content |
| `agent/slides_tools/CheckSlideCanvasOverflow.py` | Check for content overflow |
| `agent/slides_tools/SlideScreenshot.py` | Render slide screenshots |
| `agent/slides_tools/ReadSlide.py` | Read slide content |
| `agent/slides_tools/DeleteSlide.py` | Delete slides |
| `agent/slides_tools/RestoreSnapshot.py` | Restore from snapshot |
| `agent/slides_tools/CreatePptxThumbnailGrid.py` | Create thumbnail overview |
| `agent/slides_tools/GenerateImage.py` | AI image generation |
| `agent/slides_tools/ImageSearch.py` | Web image search |
| `agent/slides_tools/DownloadImage.py` | Download images |
| `agent/slides_tools/EnsureRasterImage.py` | Convert to raster format |
| `agent/slides_tools/ApplyPptxTextReplacements.py` | Bulk text replacement |
| `agent/slides_tools/ExtractPptxTextInventory.py` | Extract all text from PPTX |
| `agent/slides_tools/CreateImageMontage.py` | Image montage creation |
| `agent/slides_tools/RearrangePptxSlidesFromTemplate.py` | Rearrange from template |
| `agent/slides_tools/slide_file_utils.py` | Path resolution utilities |
| `agent/slides_tools/deck_utils.py` | Theme/test deck utilities |
| `agent/slides_tools/html_writer_instructions.md` | HTML slide authoring rules |
| `agent/slides_tools/html2pptx_runner.js` | HTML-to-PPTX JS converter |
| `agent/slides_tools/render_slides.py` | Slide rendering script |
| `agent/slides_tools/slide_html_utils.py` | HTML utility functions |
| `agent/slides_tools/template_registry.py` | Slide template registry |

### Docs Tools (DOCX/PDF Generation)
| File | Purpose |
|------|---------|
| `agent/docs_tools/CreateDocument.py` | Create DOCX from HTML |
| `agent/docs_tools/ConvertDocument.py` | Convert DOCX to PDF |
| `agent/docs_tools/ModifyDocument.py` | Modify existing documents |
| `agent/docs_tools/ViewDocument.py` | View document content |
| `agent/docs_tools/ListDocuments.py` | List generated documents |
| `agent/docs_tools/RestoreDocument.py` | Restore document from snapshot |
| `agent/docs_tools/utils/` | HTML-to-DOCX conversion engine (12 files) |

### Shared & Utility Tools
| File | Purpose |
|------|---------|
| `agent/shared_tools/CopyFile.py` | File copy with path normalization |
| `agent/shared_tools/ExecuteTool.py` | Generic tool execution |
| `agent/shared_tools/FindTools.py` | Tool discovery |
| `agent/shared_tools/ManageConnections.py` | Connection management |
| `agent/shared_tools/SearchTools.py` | Tool search |
| `agent/shared_tools/model_availability.py` | Provider capability checks |
| `agent/shared_tools/openai_client_utils.py` | OpenAI credential helpers |
| `agent/utility_tools/ReadFile.py` | Read file contents |
| `agent/utility_tools/WriteFile.py` | Write file contents |
| `agent/utility_tools/EditFile.py` | Edit file contents |
| `agent/utility_tools/ListDirectory.py` | List directory contents |

### Patches
| File | Purpose |
|------|---------|
| `agent/patches/patch_agency_swarm_dual_comms.py` | Dual communication channels |
| `agent/patches/patch_file_attachment_refs.py` | File attachment reference fix |
| `agent/patches/patch_ipython_interpreter_composio.py` | IPython Composio context |
| `agent/patches/patch_utf8_file_reads.py` | UTF-8 file read enforcement |

### Web UI (Next.js)
| File | Purpose |
|------|---------|
| `webui/src/app/page.tsx` | Main page with header + chat |
| `webui/src/app/layout.tsx` | Root layout (Inter + Nunito fonts) |
| `webui/src/app/globals.css` | Tailwind + custom theme |
| `webui/src/app/api/chat/route.ts` | API proxy to FastAPI backend |
| `webui/src/components/ChatInterface.tsx` | Chat UI with session management |
| `webui/package.json` | Node.js dependencies |
| `webui/tsconfig.json` | TypeScript config |
| `webui/next.config.ts` | Next.js config |

### Data (YAML Files)
| Directory | Count | Description |
|-----------|-------|-------------|
| `data/grammar/` | 300 files | Grammar point definitions |
| `data/activities/` | 218 files | Classroom activity definitions |
| `data/l1-interference/` | 34 files | L1 interference patterns by language |

---

## 4. How to Run Locally

### Prerequisites
- Python 3.12+
- Node.js 20+
- OpenRouter API key

### Backend
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"

# Create .env file
cp .env.example .env  # or create manually:
# OPENAI_API_KEY=sk-or-v1-your-key
# DEFAULT_MODEL=openrouter/anthropic/claude-haiku-4.5
# PORT=8080

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run server
python server.py
# → http://localhost:8080
```

### Web UI
```bash
cd webui
npm install
npm run dev
# → http://localhost:3000
```

### Docker
```bash
docker build -t cogniesl .
docker run -p 8080:8080 --env-file .env cogniesl
```

---

## 5. Testing the Full Flow

Send this message to the agent (via Web UI or curl):

```bash
curl -X POST http://localhost:8080/cogniesl/get_response \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-session-1" \
  -d '{"message": "I need slides for present simple for Brazilian adults"}'
```

Expected flow:
1. Agent asks about level (beginner/intermediate/advanced) and format
2. You respond: "beginner, slides and worksheets"
3. Agent confirms requirements
4. You respond: "yes"
5. Agent searches database, generates materials
6. Returns file paths for PPTX, DOCX, and PDF

---

## 6. Known Issues & Gotchas

### Session State
- The agent maintains state internally via Agency Swarm. Do NOT pass chat_history.
- Sessions expire after 30 minutes of inactivity.
- Each browser tab gets a unique session (localStorage-based).

### Path Resolution
- Tools use `Path(__file__).parents[N]` to find data/mnt directories.
- In Docker, set `COGNIESL_DATA_DIR=/app/data` to override.
- Output goes to `./mnt/{topic-slug}/` (created dynamically).

### Model Requirements
- The model MUST support tool calling (function calling).
- gpt-4o-mini is NOT recommended — poor instruction following.
- Claude Haiku 4.5 is the minimum viable model.
- Claude Sonnet 4.5 is recommended for production.

### Response Cleanup
- The server strips `<memory-context>` blocks and `[System note:...]` annotations.
- If you see these in responses, the agent is leaking internal context.

### L1 Interference Data
- 34 languages available. Check `data/l1-interference/` for the list.
- Not all grammar points have L1 data for all languages.
- The tool returns available grammar points if the requested one isn't found.

### File Generation
- Slides: HTML → BuildPptxFromHtmlSlides → PPTX
- Docs: HTML → CreateDocument → DOCX → ConvertDocument → PDF
- Playwright is required for PDF conversion (installed via Dockerfile).

---

## 7. What NOT to Modify

1. **Data files** (`data/grammar/`, `data/activities/`, `data/l1-interference/`) — These are the knowledge base. Don't edit unless fixing errors.
2. **Tool internals** (`slides_tools/`, `docs_tools/`) — These are from the Agency Swarm ecosystem. Modify only if absolutely necessary.
3. **Patches** (`patches/`) — These fix framework bugs. Don't remove.

Safe to modify:
- `agent/instructions.md` — Agent behavior and personality
- `agent/tools/*.py` — Custom tool logic
- `server.py` — Server behavior
- `webui/` — Frontend UI
- `.env` — Configuration

---

## 8. Adding a New Feature

### Adding a New Tool
1. Create the tool class in the appropriate directory (e.g., `agent/tools/`)
2. Inherit from `agency_swarm.tools.BaseTool`
3. Define fields with `pydantic.Field`
4. Implement `run()` method
5. Import and register in `agent/cogniesl_agent.py`
6. Update `agent/instructions.md` to mention the tool

### Adding New Grammar Data
1. Create a YAML file in `data/grammar/` following the schema in `docs/DATA_FORMAT.md`
2. Use the slug format: `present_simple.yaml`, `a_an_the.yaml`
3. No code changes needed — SearchGrammarTool finds it automatically

### Adding New L1 Data
1. Create or edit `data/l1-interference/{language}_interference.yaml`
2. Follow the schema in `docs/DATA_FORMAT.md`
3. No code changes needed — GetL1InterferenceTool finds it automatically

### Adding New Activities
1. Create a YAML file in `data/activities/`
2. Follow the schema in `docs/DATA_FORMAT.md`
3. No code changes needed — SearchActivitiesTool finds it automatically

---

## 9. Debugging Tips

### Agent Doesn't Follow Instructions
- Check `agent/instructions.md` for clarity
- Try a better model (Haiku 4.5 → Sonnet 4.5)
- Reduce temperature in `cogniesl_agent.py` (currently 0.7)

### Tool Not Found
- Check import chain in `cogniesl_agent.py`
- Verify `sys.path.insert(0, str(AGENT_DIR))` is present
- Check for circular imports

### Files Not Generated
- Check `./mnt/` directory permissions
- Verify playwright is installed: `python -m playwright install chromium`
- Check agent's tool output for error messages

### Session Lost
- Check `X-Session-ID` header is being sent
- Verify localStorage is available (not in incognito mode)
- Check server logs for session creation/cleanup messages
