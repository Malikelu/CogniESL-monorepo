# CogniESL × OpenSwarm — Architecture Redesign Document

> May 2026 — For Marcos, CEO
> Updated after deep analysis of OpenSwarm capabilities

---

## 1. The Problem

After a week of debugging Forge, the conclusion is clear: **the entire architecture was wrong.**

We had:
- **Good data:** 208 grammar points, 665 activities, 27 L1 interference files
- **Powerful backend:** OpenSwarm's agents can generate polished presentations and documents
- **Broken integration:** We were building manifests, validation layers, and complex tool-calling chains instead of letting OpenSwarm do what it's good at

The result: every chat session was a new adventure in what would break. The materials were technically generated but pedagogically weak. Teachers would never pay for this.

---

## 2. The Key Insight

**OpenSwarm's Orchestrator IS the chat AI we've been trying to build.**

The Orchestrator already knows how to:
- Interpret user requests
- Choose the right specialist agent
- Delegate with full context via Handoff or SendMessage
- Manage multi-agent workflows

We don't need to build a separate chat AI. We need to **teach the Orchestrator to understand ESL teaching** and give it access to our database.

---

## 3. The Architecture

### 3.1 How It Works

```
Teacher → OpenSwarm Orchestrator → Specialist Agent → Materials → ZIP
```

1. **Teacher talks to the Orchestrator** (via CLI or web UI)
2. **Orchestrator understands the request** — uses custom tools to search our database
3. **Orchestrator routes to the right specialist** — Slides Agent or Docs Agent with ALL context
4. **Specialist generates materials** — using OpenSwarm's built-in tools (web search, PPTX generation, PDF generation)
5. **Materials are packaged into ZIP** — download link returned to teacher

### 3.2 What the Orchestrator Does

The Orchestrator's job is **pure routing with context gathering**:

1. Interpret the teacher's request (topic, level, L1, age, format)
2. Search our database using custom tools:
   - `SearchGrammarTool` — find grammar point data
   - `GetL1InterferenceTool` — get L1 patterns
   - `SearchActivitiesTool` — find matching activities
3. Ask clarifying questions if needed (but NOT redundant ones)
4. Route to Slides Agent or Docs Agent with ALL the context

### 3.3 What the Specialists Do

**Slides Agent:**
- Receives rich context (grammar data, L1 patterns, activity data)
- Uses its own tools (web search, image generation, PPTX building)
- Creates professional presentations with L1 callouts
- Exports to PPTX

**Docs Agent:**
- Receives rich context
- Creates worksheets targeting specific L1 errors
- Creates activity resources (instructions, materials, timing, script)
- Exports to PDF

---

## 4. What Needs to Be Modified

### 4.1 Fork and Customize OpenSwarm

Fork the VRSEN/OpenSwarm repo. Modify these files:

**1. `orchestrator/instructions.md`** — THE MOST CRITICAL FILE

The Orchestrator needs to understand ESL teaching requests. It should:
- Recognize ESL teaching concepts (topic, CEFR level, L1 languages, age group, format)
- Know how to use our custom tools to search the database
- Ask clarifying questions when the request is ambiguous
- NOT ask redundant questions (if teacher says "slides only," don't ask about format again)
- Route to the right specialist with ALL context

**2. Add three custom tools:**

- `SearchGrammarTool` — searches `data/grammar/` by topic name with fuzzy matching
- `SearchActivitiesTool` — searches `data/activities/` by topic/level/age/L1
- `GetL1InterferenceTool` — gets L1 patterns for a grammar point + language

**3. `slides_agent/instructions.md`** — Minor modifications to:
- Use provided grammar data, L1 patterns, and activity data
- Include L1-specific callouts in slides
- Follow proper ESL teaching methodology

**4. `docs_agent/instructions.md`** — Minor modifications to:
- Target specific L1 errors in exercises
- Generate activity resources when activity data is provided

### 4.2 What Stays the Same

- OpenSwarm core framework (Agency Swarm)
- Slides Agent tools (InsertNewSlides, ModifySlide, BuildPptxFromHtmlSlides, etc.)
- Docs Agent tools
- FastAPI server (server.py)
- All other agents (Deep Research, Data Analyst, Image Generation, Video Generation, Virtual Assistant)

### 4.3 What Needs to Be Built from Scratch

1. **Web UI (Next.js)** — Chat interface that talks to OpenSwarm's API
2. **File storage layer** — S3 or Railway volumes for persistent file storage
3. **Database loading** — Code to load YAML files into searchable format at startup

---

## 5. What Does NOT Need to Be Built

- ❌ No manifest system (SharedContext, ManifestBuilder)
- ❌ No QA validation (6x6 rules, 80/20 visual ratio, speaker notes)
- ❌ No fix loop controller
- ❌ No separate chat AI
- ❌ No Python backend that generates PPTX/PDF from scratch
- ❌ No complex multi-step tool calling chains

---

## 6. Database Integration

Our YAML files are already well-structured. We just need to make them accessible:

**Approach: Simple file-based search**
- Load all YAML files at startup into a searchable data structure
- Tools search the in-memory data
- No external dependencies
- Fast enough for 208 + 665 + 27 files

**Grammar point matching must be robust:**
- Handle variations: "Simple Present" → `present_simple.yaml`
- Handle capitalization, spaces, special characters
- Try exact match → case-insensitive → fuzzy match → word-level overlap

---

## 7. Known Failure Points and Mitigations

| Failure Point | Mitigation |
|---|---|
| Orchestrator doesn't understand ESL teaching | Write clear instructions.md with examples |
| Orchestrator asks redundant questions | Explicit instructions: "If teacher specifies format, don't ask again" |
| Specialists don't use our data | Modify their instructions.md to explicitly require L1 callouts |
| Grammar point matching fails | Multi-strategy matching (exact → case-insensitive → fuzzy → word overlap) |
| Files lost on Railway deploys | Use S3 or Railway volumes, never container filesystem |
| Deep Research / Virtual Assistant not needed yet | Start simple, add later if output quality needs improvement |

---

## 8. Implementation Plan

### Step 1: Archive Forge, Create CogniESL
- Move Forge to archive
- Create new CogniESL folder
- Move only data files and analysis docs

### Step 2: Fork OpenSwarm
- Fork VRSEN/OpenSwarm to CogniESL repo
- Set up local development environment

### Step 3: Customize Orchestrator
- Rewrite `orchestrator/instructions.md`
- Add three custom tools
- Test via CLI

### Step 4: Customize Specialists
- Modify `slides_agent/instructions.md`
- Modify `docs_agent/instructions.md`
- Test material generation via CLI

### Step 5: Build Web UI
- Simple Next.js chat interface
- Talks to OpenSwarm's FastAPI API
- Shows download button when materials ready

### Step 6: Deploy to Railway
- Monolith deployment
- S3 for file storage
- Test end-to-end

---

## 9. Success Criteria

1. **Reliability:** 9 out of 10 sessions produce materials without errors
2. **Quality:** Materials include L1-specific callouts, proper activity instructions, professional design
3. **Speed:** Materials generated in under 60 seconds from confirmation to download
4. **Simplicity:** The entire custom code fits in one page

---

## 10. Final Thought

We were trying to build a Ferrari with bicycle parts. The data is the engine — it's good. OpenSwarm is the chassis — it's powerful. But we were building a broken transmission.

The solution: fork OpenSwarm, teach the Orchestrator to understand ESL teaching, and let the specialists do what they're good at.

No manifests. No validation loops. No separate chat AI. Just OpenSwarm with our data.
