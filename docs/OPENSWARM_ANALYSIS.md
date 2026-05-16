# CogniESL × OpenSwarm — Complete Analysis & Build Prompt

> May 2026 — For Marcos, CEO
> Deep analysis of OpenSwarm capabilities and customization options

---

## PART 1: What OpenSwarm Actually Is

### 1.1 The Architecture

OpenSwarm is a **multi-agent system** built on Agency Swarm. It has 8 specialist agents coordinated by an Orchestrator.

**The 8 Agents:**

| Agent | Role | Tools |
|---|---|---|
| **Orchestrator** | Pure routing — interprets requests, delegates to specialists | SendMessage, Handoff |
| **Slides Agent** | Creates HTML slide decks → exports to PPTX | InsertNewSlides, ModifySlide, BuildPptxFromHtmlSlides, WebSearch, ImageGeneration |
| **Docs Agent** | Creates Word docs and PDFs | Document creation, PDF export |
| **Deep Research Agent** | Web research with citations | Web search, content synthesis |
| **Data Analyst** | Data analysis and charts | IPython kernel, statistical models |
| **Image Generation Agent** | Image creation/editing | Gemini, fal.ai |
| **Video Generation Agent** | Video production | Sora, Veo, Seedance |
| **Virtual Assistant** | General tasks | 10,000+ integrations via Composio |

### 1.2 How the Orchestrator Works

The Orchestrator is **pure routing**. It:
1. Interprets the user's request
2. Chooses the right specialist(s)
3. Delegates via:
   - **Handoff** — for single-specialist tasks (transfers full context)
   - **SendMessage** — for parallel multi-agent tasks
4. Never executes tasks itself

The Orchestrator's behavior is controlled entirely by its `instructions.md` file. This is a plain text file that acts as its "system prompt."

### 1.3 How Agents Use Tools

Each agent has **tools** — Python classes that the agent can call autonomously. For example, the Slides Agent has tools for:
- Creating slide placeholders
- Modifying slide content
- Building PPTX from HTML
- Searching the web
- Generating images

Tools are **standalone, configurable, and composable**. The agent decides when and how to use them based on its instructions.

### 1.4 How to Customize OpenSwarm

You customize OpenSwarm by:
1. **Modifying agent instructions** (the `instructions.md` files)
2. **Adding custom tools** (Python classes)
3. **Adding custom agents** (new specialists)

You do NOT need to modify the core framework.

---

## PART 2: The Opportunity

### 2.1 Why Our Previous Architecture Failed

We were building:
```
Chat AI → SharedContext → ManifestBuilder → QA Validation → Fix Loop → generateBundle → ZIP
```

This failed because:
1. We were building manifests instead of letting OpenSwarm's agents do what they're good at
2. Our chat AI was doing too much (gathering, validating, retrying, falling back)
3. The output quality depended on our manifest quality, not OpenSwarm's agent capabilities
4. We were using a free model that couldn't reliably follow complex instructions

### 2.2 The OpenSwarm Opportunity

**OpenSwarm's Orchestrator IS the chat AI we need.**

Instead of building a separate chat AI, we should:
1. Fork OpenSwarm
2. Customize the Orchestrator's instructions to understand ESL teaching
3. Add custom tools to access our database
4. Let the Orchestrator route to specialists with rich context
5. Let specialists generate materials using their own tools

**The flow becomes:**
```
Teacher → Orchestrator → Slides/Docs Agent → Materials → ZIP
```

No separate chat AI. No manifests. No validation loops.

---

## PART 3: What Needs to Be Modified

### 3.1 Orchestrator's instructions.md (CRITICAL)

This is the single most important file. The Orchestrator needs to:

1. **Understand ESL teaching requests:**
   - Topic/grammar point (e.g., "present simple", "passive voice")
   - CEFR level (A1, A2, B1, B2, C1, C2)
   - L1 languages (e.g., "Portuguese", "Spanish")
   - Age group (kids, teens, adults)
   - Format (slides, worksheet, flashcards, activity, or combination)

2. **Use custom tools to gather data:**
   - Search for grammar points by topic name
   - Get L1 interference patterns
   - Search for activities

3. **Ask clarifying questions (but NOT redundant ones):**
   - If the teacher says "slides only," DON'T ask about format again
   - If the teacher says "for Brazilian adults," you already know L1=Portuguese and age=adults
   - Only ask about truly missing information

4. **Route to the right specialist with ALL context:**
   - Handoff to Slides Agent with grammar data + L1 patterns + activity data
   - Handoff to Docs Agent with the same context

### 3.2 Custom Tools

Three tools need to be added:

**SearchGrammarTool:**
- Searches `data/grammar/` by topic name
- Must handle variations: "Simple Present" → `present_simple.yaml`
- Multi-strategy matching: exact → case-insensitive → fuzzy → word overlap
- Returns the full grammar point data

**SearchActivitiesTool:**
- Searches `data/activities/` by topic, level, age group, L1 languages
- Returns matching activities with full details (instructions, scripts, materials)

**GetL1InterferenceTool:**
- Gets L1 interference patterns for a specific grammar point + language
- Returns all patterns with examples, explanations, and teacher tips

### 3.3 Specialists' instructions.md (Minor Modifications)

**Slides Agent:**
- Use provided grammar data, L1 patterns, and activity data
- Include L1-specific callouts in slides (e.g., "⚠ Portuguese speakers often say 'She work' instead of 'She works'")
- Follow proper ESL teaching methodology (engagement → presentation → practice → production)

**Docs Agent:**
- Generate worksheets targeting specific L1 errors
- Create activity resources when activity data is provided
- Include answer keys

### 3.4 What Stays the Same

- OpenSwarm core framework
- All agent tools (Slides Agent tools, Docs Agent tools, etc.)
- FastAPI server
- Deep Research Agent, Data Analyst, Image Generation, Video Generation, Virtual Assistant (not needed for v1, but available later)

---

## PART 4: Deep Research Agent and Virtual Assistant

### 4.1 Deep Research Agent

**What it does:** Comprehensive, evidence-based web research with citations and balanced analysis.

**Can it search our database?** Technically yes, but it's the wrong tool. It's designed for web research, not local file search. Using it to search YAML files would be slow and overkill.

**When to use it:** Later, for enriching materials with additional examples or teaching techniques from the web. Not needed for v1.

### 4.2 Virtual Assistant

**What it does:** General tasks (writing, scheduling, messaging) with 10,000+ integrations via Composio.

**Can it search our database?** No. It's designed for productivity tools (Gmail, Slack, GitHub), not database search.

**When to use it:** Later, for teacher communication (email summaries, etc.). Not needed for v1.

### 4.3 Recommendation

Start simple. Add custom tools for database search. Get the basic flow working. THEN consider adding Deep Research Agent for enrichment if the basic output isn't good enough.

---

## PART 5: The Build Prompt

Here is the exact prompt to give to a fresh AI (Claude Code, Codex, Cursor, etc.):

---

```
You are building CogniESL — an AI-powered ESL teaching material generator.

## What the App Does

CogniESL helps ESL teachers create custom teaching materials through a simple chat conversation. The teacher describes what they need, and CogniESL generates professional materials (slides, worksheets, flashcards, activities) tailored to their students' language background.

## The Data

You have three databases in the `data/` folder:

1. **Grammar Points** (`data/grammar/`): 208 YAML files. Each file describes an English grammar point with formation rules, uses, examples, common errors, and teaching tips. The `grammar_point` field is the slug (e.g., `present_simple`), and the `title` is the human-readable name (e.g., "Present Simple (V1/es for 3rd person)").

2. **Activities** (`data/activities/`): 665 YAML files. Each file describes a classroom activity with step-by-step instructions, teacher scripts, materials needed, duration, target levels/ages, and grammar points covered.

3. **L1 Interference** (`data/l1-interference/`): 27 YAML files (one per language). Each file contains interference patterns for multiple grammar points. Each pattern includes: the specific error, a wrong→correct example, why it happens (linguistic explanation), teacher tips, and frequency/persistence/impact scores.

## The Architecture

Use OpenSwarm (https://github.com/VRSEN/OpenSwarm) as the core engine. Fork it and customize it.

### How It Should Work

1. Teacher talks to the Orchestrator (via CLI for now, web UI later)
2. Orchestrator understands the request and uses custom tools to search our database
3. Orchestrator routes to the right specialist (Slides Agent or Docs Agent) with ALL context
4. Specialist generates materials using OpenSwarm's built-in tools
5. Materials are packaged into a ZIP and a download link is returned

### What to Modify in OpenSwarm

**1. `orchestrator/instructions.md`** — THE MOST CRITICAL FILE

Rewrite it to:
- Understand ESL teaching requests (topic, level, L1, age, format)
- Use custom tools (SearchGrammarTool, GetL1InterferenceTool, SearchActivitiesTool) to gather data
- Ask clarifying questions when the request is ambiguous
- NOT ask redundant questions (if teacher says "slides only," don't ask about format again)
- Route to Slides Agent or Docs Agent with ALL context (grammar data, L1 patterns, activity data)

**2. Add three custom tools:**

- `SearchGrammarTool`: Searches `data/grammar/` by topic name with fuzzy matching. Handles variations like "Simple Present" → `present_simple.yaml`. Returns full grammar point data.

- `SearchActivitiesTool`: Searches `data/activities/` by topic, level, age group, L1 languages. Returns matching activities with full details.

- `GetL1InterferenceTool`: Gets L1 interference patterns for a grammar point + language. Returns all patterns with examples, explanations, and teacher tips.

**3. `slides_agent/instructions.md`** — Minor modifications:
- Use provided grammar data, L1 interference patterns, and activity data
- Include L1-specific callouts in slides
- Follow proper ESL teaching methodology

**4. `docs_agent/instructions.md`** — Minor modifications:
- Target specific L1 errors in exercises
- Generate activity resources when activity data is provided

### Key Requirements

1. **Grammar point matching must be robust.** Handle spaces, capitalization, and variations.
2. **L1 interference MUST be visible in materials.** Specific callouts targeting the students' L1 errors.
3. **"Activity" is a valid format.** Generate a standalone activity resource (instructions, materials, timing, script).
4. **Don't ask redundant questions.** If the teacher specifies a format, don't ask again.
5. **Persistent file storage.** Use S3 or Railway volumes. Never store files in container filesystem.
6. **CLI first.** Make it work via CLI before building a web UI.

### What NOT to Build

- No manifest system (no SharedContext, ManifestBuilder, QA validation, fix loops)
- No separate chat AI layer (OpenSwarm's Orchestrator IS the chat AI)
- No Python backend that generates PPTX/PDF from scratch (use OpenSwarm's agents)
- No web UI yet (CLI first)

### Testing

Test via CLI with these scenarios:
1. "I need slides for present simple for Brazilian adults"
2. "Create a worksheet on passive voice for Spanish-speaking teens"
3. "Generate flashcards about articles for Japanese students"
4. "I want an activity for present continuous for Arabic adults"

Evaluate:
- Does the Orchestrator ask the right questions?
- Does it find the correct grammar point and L1 data?
- Do the materials include L1-specific content?
- Is the output quality good enough for a teacher to use?

### Deployment

- Railway (OpenSwarm backend)
- S3 for file storage
- Environment variables: OPENROUTER_API_KEY or ANTHROPIC_API_KEY

---

Build this system. Start by reading the data files, then fork OpenSwarm, then customize the Orchestrator, then test via CLI.
```

---

## PART 6: Files to Give the AI

1. **This document** — the complete analysis
2. `docs/ARCHITECTURE_REDESIGN.md` — the architecture overview
3. `data/grammar/` — all 208 YAML files
4. `data/activities/` — all 665 YAML files
5. `data/l1-interference/` — all 27 YAML files

---

## PART 7: Critical Considerations

### 7.1 Can the Orchestrator Handle This?

**Yes, with proper instructions.** The Orchestrator is designed to interpret requests and delegate. We just need to teach it ESL teaching concepts and give it the right tools.

### 7.2 Will the Quality Be Better?

**Almost certainly yes.** OpenSwarm's Slides Agent already produces polished presentations. By giving it rich context (L1 patterns, activity data, grammar details), it can create materials that are genuinely tailored to the students.

### 7.3 What Could Go Wrong?

1. **Orchestrator might not understand ESL teaching** → Write clear instructions with examples
2. **Grammar point matching might fail** → Multi-strategy fuzzy matching
3. **Specialists might not use our data** → Modify their instructions to explicitly require L1 callouts
4. **File storage on Railway** → Use S3 or Railway volumes

### 7.4 How Long Will This Take?

With a good AI (Claude Code, Codex, or Cursor): **2-3 days** for a working CLI prototype.

The key advantage: we're customizing OpenSwarm, not building from scratch. The agents, tools, and infrastructure already exist. We just need to teach them about ESL teaching.
