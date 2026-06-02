# OpenSwarm → CogniESL: Complete Adaptation Reference

**Source:** https://github.com/VRSEN/OpenSwarm + https://github.com/VRSEN/agency-swarm  
**Files analyzed:** 21 .md files + 8 Python/config files + 15 framework .mdx docs  
**Purpose:** Single source of truth for adapting OpenSwarm/Agency Swarm patterns to CogniESL/Forge

---

## TABLE OF CONTENTS

- Part 1: Reference — What OpenSwarm Is
- Part 2: Architecture & Process Patterns
- Part 3: HTML Styling, Design & PPTX
- Part 4: Advanced Patterns
- Part 5: Agency Swarm Framework Features (Not Used Yet)
- Part 6: Python Source Code Insights
- Part 7: Unified Implementation Plan
- Part 8: Done Right / Do Not Touch
- Part 9: Raw Source Files

---

# PART 1: REFERENCE — WHAT OPENS SWARM IS

## 1.1 Project Overview

OpenSwarm is a fully open-source multi-agent system coordinating **8 specialized agents** through an **Orchestrator**, built on [Agency Swarm](https://github.com/VRSEN/agency-swarm). Core promise: one prompt → complete deliverables (slides, docs, research, video, images).

## 1.2 Production Agents (Run-Time)

| Agent | Folder | Primary Function |
|-------|--------|-----------------|
| **Orchestrator** | `swarm.py` | Routes requests to specialists. Pure coordination. |
| **Virtual Assistant** | `virtual_assistant/` | Email, calendar, Slack, task management via Composio |
| **Deep Research** | `deep_research/` | Web research with citations, ScholarSearch |
| **Data Analyst** | `data_analyst_agent/` | Pandas analysis, charts, connections to GA/Stripe |
| **Slides Agent** | `slides_agent/` | HTML slides → PPTX, Chart.js, ECharts |
| **Docs Agent** | `docs_agent/` | HTML → DOCX/PDF with auto-versioning |
| **Image Generation** | `image_generation_agent/` | Gemini 2.5 Flash Image + fal.ai |
| **Video Generation** | `video_generation_agent/` | Veo 3.1 / Sora / Seedance video pipeline |

## 1.3 Build-Time Sub-Agents (Claude Code)

Used to BUILD new agencies. `.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| api-researcher | Researches MCP servers/APIs, documents API keys |
| prd-creator | Creates PRDs (strict 4-16 tools/agent rule) |
| agent-creator | Creates agent folder structure and base files |
| instructions-writer | Writes optimized instructions.md |
| tools-creator | Implements tools (MCP preferred), tests each |
| qa-tester | Sends 5 test queries, scores, suggests improvements |

**Build workflow:** api-researcher → prd-creator → (agent-creator + instructions-writer parallel) → tools-creator → qa-tester → iterate

## 1.4 Key Architectural Patterns

| Pattern | Details |
|---------|---------|
| **Agent folder structure** | `agent_name/{__init__.py, agent_name.py, instructions.md, tools/}` |
| **Communication flows** | Orchestrator-Workers (80%), Sequential Pipeline (15%), Collaborative Network (5%) |
| **Tool hierarchy** | Built-in tools → MCP servers → Custom tools (only as fallback) |
| **Shared state** | `self.context.set/get` via Agency Context framework |
| **Tool count discipline** | 4-16 tools per agent; split if exceeds 16 |

---

# PART 2: ARCHITECTURE & PROCESS PATTERNS

## 2.1 Agent Instructions Architecture

### OpenSwarm's Template

Every agent follows:
```
# Role → # Goals → # Context → # Process → # Output Format → # Additional Notes
```

**Example — Deep Research:**
- Process: numbered steps for WebSearchTool vs ScholarSearch, min 3-5 searches
- Output Format: 6 sections (Executive Summary, Key Findings, Evidence, Options, Recommendation, Risks)
- Quality Rule: "When sources conflict — document all, explain credibility"

### Current CogniESL Pattern: One monolithic 1349-line instructions.md

### What to Adapt

| Pattern | Application | Priority |
|---------|------------|----------|
| **Role-based separation** | Split Forge enrichment agents into per-role instructions | HIGH |
| **Output Format sections** | Every enrichment task defines exact output structure | HIGH |
| **Per-tool instructions** | Each search/extraction tool gets its own instruction reference | MEDIUM |

### Concrete: Forge Agent Template

```markdown
# Role
You are a [Grammar Enricher / L1 Specialist] for the Forge.
# Goals
- [Primary objective]
# Process (Numbered)
1. Load file
2. Extract fields
3. Cross-reference grammar-index.yaml
4. Add field with source citation
5. Validate
# Output Format
{field: value, source: "Author (Year)", tier: [1|2|3]}
# Error Handling
- YAML parse fail → log and skip
- Source not found → flag for review, do NOT fabricate
```

---

## 2.2 Quality Gate System (QA-Tester)

### OpenSwarm: 5 queries → score ≥8/10 → iterate

1. Generate 5 test queries (basic, multi-step, edge case, error, complex)
2. Execute each, score 1-10
3. Threshold: 5/5 pass at ≥8
4. Iterate: report fixes, re-test same 5 queries

### Current Forge: 6-pass manual system (citation → pedagogy → accuracy → completeness → expert → hallucination)

### What to Adapt

| Pattern | Application | Priority |
|---------|-------------|----------|
| **Standardized test queries** | 5 defined queries per batch instead of random spot checks | HIGH |
| **Quality score system** | Score 1-10 instead of pass/fail for trajectory data | MEDIUM |
| **Same-query iteration** | Re-run the SAME queries to measure improvement | MEDIUM |
| **File ownership** | QA agent REPORTS, enrichment agent FIXES | MEDIUM |

### Concrete: Test Query Template

```markdown
Each batch of 20 files:
1. Citation accuracy — pick 3 random citations, verify. Score: /10
2. Pedagogical usefulness — would an ESL teacher use this? Score: /10
3. Schema completeness — all required fields? Score: /10
4. Fabrication check — every claim traceable to source line? Score: /10
5. Format validity — YAML parses, no duplicate keys? Score: /10
PASS threshold: all 5 ≥ 8
```

---

## 2.3 Pipeline Architecture

### OpenSwarm: 3 patterns — Orchestrator-Workers (80%), Sequential Pipeline (15%), Collaborative Network (5%)

### Current CogniESL: Single-agent with ~30 tools. Current Forge: Human orchestrated.

### What to Adapt

| Pattern | Application | Priority |
|---------|-------------|----------|
| **Per-agent folder structure** | Forge assignments → `{instructions.md, tools/, references/}` | MEDIUM |
| **Sequential Pipeline** | Forge: Enricher → Validator → Committer | MEDIUM |

---

## 2.4 Tool Organization

### OpenSwarm: Hierarchy (built-in > MCP > custom), 4-16 per agent

### What to Adapt

| Pattern | Application | Priority |
|---------|-------------|----------|
| **Tool spec table** | Every enrichment task needs a script→data map | HIGH |
| **Tool documentation pattern** | Each script: description, inputs, outputs, errors | HIGH |

---

## 2.5 File/Project Structure

### OpenSwarm: Every agent has identical `{agent.py, instructions.md, tools/, __init__.py}`

### What to Adapt

| Pattern | Application | Priority |
|---------|-------------|----------|
| **YAML creation template** | New grammar/L1 files from template (like agent.py template) | HIGH |
| **.env template** | Document required env vars per tool | MEDIUM |

---

# PART 3: HTML STYLING, DESIGN & PPTX

## 3.1 Head-to-Head

| Feature | CogniESL (45KB) | OpenSwarm (11KB) | Better |
|---------|----------------|-------------------|--------|
| ESL pedagogy | Per-slide identity (A0-A8), CCQs, L1 Oracle | General-purpose | **CogniESL** |
| PPTX rules | None — assumes HTML viewer only | 8+ explicit PPTX rules | **OpenSwarm** |
| Animations | Full CSS, required on key slides | "Minimize — don't export" | **OpenSwarm** |
| Watermark/branding | Full system (free/pro, locked SVG) | None | **CogniESL** |
| Speaker notes | Mandatory, structured | None | **CogniESL** |
| Design vocabulary | Cards, gradients, clip-path, SVG | Accent bars, kicker labels, orbs, brackets | **OpenSwarm** |
| Validation | 12 rules | 15 rules | **OpenSwarm** |

## 3.2 PPTX Rules We Must Copy

**IMPORTANT CORRECTION:** CSS gradients DO work in PPTX. OpenSwarm's `BuildPptxFromHtmlSlides` converts gradients to vector SVGs, and `_convert_css_bg_images_to_img_tags()` in ModifySlide auto-converts CSS `background-image` to `<img>` tags. The tool handles this.

What still needs instruction changes:

**Rule 1: Badges/pills NOT inline in sentences**
The PPTX converter treats inline background-color spans as standalone shapes, splitting sentences.

**Rule 2: Minimum 8px gap between pill groups**
CSS border-radius makes HTML gaps look larger; PPTX renders exact coordinates.

**Rule 3: Only specific Google Fonts embed in PPTX**
Nunito is NOT on the embedding list. Replace with Montserrat or Inter.

**Rule 4: Animations don't export to PPTX**
PPtX uses only the final state. Dual-mode: HTML = animated, PPTX = static.

### Three Paths Forward

| Path | Effort | Trade-off |
|------|--------|-----------|
| **A — PPTX-aware HTML** (recommended) | 30 min doc update | Tool handles conversions; focus on Rules 1-4 |
| **B — Dual-mode (HTML + PPTX instructions)** | 2 hours | Two files to maintain |
| **C — Post-conversion CSS rewrite** | 4-6 hours code | Keep pristine HTML output |

## 3.3 Design Vocabulary to Adopt

Pure CSS — zero new tools:

| Technique | CSS Pattern | Where in CogniESL |
|-----------|-------------|-------------------|
| **Glowing orbs** | `filter:blur(100px); opacity:0.15` | A1 Hook — ambient depth |
| **Per-item color coding** | Unique accent per card | A7 Practice — variety |
| **Kicker labels** | `letter-spacing:2px; text-transform:uppercase` | Section labels |
| **Corner brackets** | Absolute L-shaped borders | A2 Meaning — frame |
| **Grid-div backgrounds** | 1px div lines at intervals | A5 Formula — grid |

## 3.4 Worksheet (DOCX) Styling

| OpenSwarm Rule | Adapt? |
|----------------|--------|
| Two-column sidebar: `<table>` must END where sidebar ends | YES — fixes multi-page worksheet layout |
| Auto-versioning: `report_v2.docx` with snapshot HTML | YES — teachers request changes |
| RestoreDocument: rollback to previous version | YES — complements versioning |
| Unsupported CSS for DOCX (no flex/grid/positioning) | YES — formal list prevents failures |
| A4 layout: `@page {size: A4}` inside `<head>` | Already aligned |

---

# PART 4: ADVANCED PATTERNS

## 4.1 Progressive Tool Disclosure (mcp-code-exec.md)

Load tools as importable modules instead of registering all 30 upfront. Claim: **98.7% token reduction (150K → 2K)**.

**For CogniESL:** Group tools by format type. Load only what matches the teacher's request:
- Slides only → slides_tools + search_tools + validation_tools
- Worksheet only → docs_tools + search_tools + validation_tools

**Effort:** 2-3 hours code. **Token savings estimate: 40-60%.**

## 4.2 Dual Output Format (data_analyst_agent)

Success format: Scope → Key Findings → Actions → Assumptions → Follow-up
Failure format: What failed → Why → What is needed → Next attempt

**For enrichment audit logs:** structured failure reports instead of vague "couldn't find it."

## 4.3 Tool Selection Hierarchy (virtual_assistant)

1. Specialized tools (highest) — grammar-index lookup
2. Generic fallback — direct YAML search
3. Programmatic — script-based enrichment (last resort)

## 4.4 1-3-1 Debugging Technique (virtual_assistant)

When stuck:
1. Define problem (one sentence)
2. Identify exactly 3 solutions
3. Recommend one

**Prevents open-ended "what should I do?" questions to Marcos.**

## 4.5 Research Methodology (api-researcher)

For source acquisition:
1. Understand needs
2. Search: OER → Academic PDFs → Published textbooks → Community
3. If found: document title, author, URL, chapters, tier
4. If not: document why
5. Save to SOURCE_INDEX.md

## 4.6 Tool Design Principles (create-prd.md)

Every tool: **Standalone**, **Configurable**, **Composable**.

Current enrichment scripts are monolithic. Redesign as:
```python
def extract(source, point) -> dict: ...
def apply(yaml_path, data, overwrite=False) -> bool: ...
def validate(yaml_path) -> dict: ...
```

## 4.7 Context Window Efficiency (virtual_assistant)

"Only log what you need. Context window is a public good."

Our REPORT.md is 176KB. Log: what was attempted ✓, what succeeded ✓, what failed + why ✓, what's next ✓. Skip full YAML dumps and tool traces.

---

# PART 5: AGENCY SWARM FRAMEWORK FEATURES (NOT USED YET)

CogniESL uses Agency Swarm v1.0.0 but only at surface level (Agent, Agency, BaseTool, SendMessage). The framework has powerful built-in features we're not using.

## 5.1 Input Guardrails

**Code-level validators that run BEFORE the agent sees a message.** Two modes:
- **Non-strict** (default): guidance returned as assistant message
- **Strict** (`raise_input_guardrail_error=True`): exception raised, turn aborted

```python
@input_guardrail
async def require_esl_topic(context, agent, user_input):
    text = user_input if isinstance(user_input, str) else " ".join(user_input)
    blocked = not any(t in text.lower() for t in ["grammar", "english", "esl"])
    return GuardrailFunctionOutput(
        output_info="I create ESL materials! What grammar point?" if blocked else "",
        tripwire_triggered=blocked,
    )
```

**Replaces from instructions.md:** 50+ lines of jailbreak protection, "if a user claims to be a developer" rules, bug-report handling. The agent never sees blocked input.

**Also works for inter-agent communication** — can validate messages between agents.

## 5.2 Output Guardrails

**Validates agent output BEFORE it reaches the teacher. Auto-retries on failure.**

```python
@output_guardrail
async def require_l1_content(context, agent, response_text):
    has_l1 = "L1" in response_text or "interference" in response_text.lower()
    return GuardrailFunctionOutput(
        output_info="Materials must include L1 interference section." if not has_l1 else "",
        tripwire_triggered=not has_l1,
    )

agent = Agent(
    name="CogniESL",
    output_guardrails=[require_l1_content],
    validation_attempts=2,  # Auto-retry up to 2 times
)
```

**CogniESL applications:**
- Ensure L1 Oracle is included when requested
- Validate slide count ≥ 16
- Check YAML enrichment has all required fields
- Prevent fabricated citations

## 5.3 Agency Context (self.context)

Framework's built-in shared state. Replaces `_shared_state`:

```python
# Tool A
self.context.set('database_context', context)
self.context.set('last_query', self.question)

# Tool B
context = self.context.get('database_context')
```

Can be initialized at Agency creation:
```python
agency = Agency(entry, communication_flows=[...], user_context={'session_id': '123'})
```

## 5.4 Parallel Tool Calls Control

```python
agent = Agent(
    model_settings=ModelSettings(parallel_tool_calls=False),
)
```

Prevents race conditions between dependent tools.

## 5.5 File Search with Vector Stores

If `files_folder` ends with `_vs_<vector_store_id>`, Agency Swarm auto-connects OpenAI Vector Store and adds `FileSearchTool`. Could be useful for L1 Research source documents.

## 5.6 Few-Shot Examples via Message History

```python
examples = [
    {"role": "user", "content": "I need present simple materials"},
    {"role": "assistant", "content": "Content Brief — Present Simple..."},
]
response = await agency.get_response(examples + [new_message])
```

More scalable than embedding examples in instructions.md.

## 5.7 What We're Already Using vs Missing

| Feature | Using It? |
|---------|-----------|
| Agent() with tools | YES |
| BaseTool with Pydantic | YES |
| Agency() with flows | YES |
| SendMessage / Handoff | YES |
| ModelSettings with reasoning | YES |
| LitellmModel | YES |
| **Input guardrails** | **NO — relies on instructions.md** |
| **Output guardrails** | **NO — relies on instructions.md** |
| **Agency Context (self.context)** | **PARTIAL — uses _shared_state** |
| **Parallel tool calls control** | **UNKNOWN** |
| **Vector Store File Search** | **NO** |
| **Few-shot via message history** | **NO — examples in instructions.md** |

---

# PART 6: PYTHON SOURCE CODE INSIGHTS

From OpenSwarm's Python source files (swarm.py, config.py, slides_agent.py, ModifySlide.py, InsertNewSlides.py, BuildPptxFromHtmlSlides.py).

## 6.1 Structured Slide Plan (InsertNewSlides.py)

Slide planner returns typed JSON, not free text:

```python
class _PlanSlide(BaseModel):
    page: int
    title: str
    content: str
    template_key: str | None       # Which template to use
    template_name: str | None
    template_status: "existing" | "new" | None
    depends_on: int | None         # Which slide must complete first
```

Our InsertNewSlides uses free-text task_brief. OpenSwarm uses Pydantic-validated typed output — no hallucination possible.

## 6.2 Template Registry (ModifySlide.py)

Persistent `_template_index.json` per project. Templates registered, looked up by key, selected by planner. Thread-safe with per-project locks. CogniESL's 8 slide types have no formal registry.

## 6.3 Background-Image Auto-Conversion (ModifySlide.py)

160-line function converting CSS `background-image` to `<img>` tags. Handles inline styles AND class-based CSS. CogniESL could copy it directly.

## 6.4 Base64 Image Stripping (ModifySlide.py)

When feeding existing HTML back to sub-agent, base64 images replaced with `[image]` placeholders. Prevents context-window overflow during single-slide edits.

## 6.5 Sub-Agent Model Separation (InsertNewSlides.py)

Separate models for planner vs HTML writer:
```python
_PLANNER_MODEL_CLAUDE = "anthropic/claude-sonnet-4-6"
_PLANNER_MODEL_OAI = "gpt-5.3-codex"
```

And `_get_caller_openai_client()` reuses the caller's auth credentials.

## 6.6 Dynamic Instructions Injection (slides_agent.py)

```python
def _build_instructions() -> str:
    now_utc = datetime.now(timezone.utc)
    body = _INSTRUCTIONS_PATH.read_text(encoding="utf-8")
    projects = _list_existing_projects()
    return f"{body}\n\nCurrent date: {now_utc}\n\nExisting projects:\n{projects}"
```

CogniESL's instructions.md is static. Dynamic injection would improve context.

## 6.7 Runtime Patches (swarm.py)

OpenSwarm applies 4 patches for Agency Swarm bugs (UTF-8, dual comms, file attachments, IPython+Composio). Pattern is clean and testable if CogniESL hits similar issues.

## 6.8 Slash-Based Model Routing (config.py)

```python
def _resolve(model: str):
    if "/" not in model:
        return model  # OpenAI
    bare = model[len("litellm/"):] if model.startswith("litellm/") else model
    return LitellmModel(model=bare)
```

Cleaner than CogniESL's prefix-based routing. Any `provider/model` string goes through LiteLLM.

---

# PART 7: UNIFIED IMPLEMENTATION PLAN

## 7.1 Immediate (Today, Zero Code)

| # | Action | Effort | Impact | Source |
|---|--------|--------|--------|--------|
| 1 | Rewrite Forge agent assignments using structured template | 1-2h | HIGH | §2.1 |
| 2 | Add Output Format sections to every agent task | 30min | HIGH | §2.1 |
| 3 | Create 5 standard test queries for enrichment gates | 30min | HIGH | §2.2 |
| 4 | Add input guardrail for ESL topic relevance | 30min | HIGH | §5.1 |
| 5 | Add output guardrail for L1 completeness + auto-retry | 30min | HIGH | §5.2 |
| 6 | Switch from `_shared_state` to `self.context` in new tools | 15min | MEDIUM | §5.3 |
| 7 | Add tool specification table per enrichment task | 15min | MEDIUM | §2.4 |
| 8 | Add next-step error hints to validation scripts | 1h | MEDIUM | §4.2 |
| 9 | Formalize YAML creation template | 30min | MEDIUM | §2.5 |
| 10 | Use 1-3-1 debugging technique when stuck | 0 (habit) | HIGH | §4.4 |
| 11 | Be concise in enrichment reports (context efficiency) | 0 (habit) | MEDIUM | §4.7 |

## 7.2 Short-Term (Before PPTX)

| # | Action | Effort | Source |
|---|--------|--------|--------|
| 1 | Add 5 PPTX compatibility rules to html_writer_instructions.md | 30min | §3.2 |
| 2 | Replace Nunito with Montserrat/Inter in font CDN link | 5min | §3.2(R3) |
| 3 | Add two-column sidebar fix to Docs Agent instructions | 15min | §3.4 |
| 4 | Copy `_convert_css_bg_images_to_img_tags()` into ModifySlide | 30min copy | §6.3 |
| 5 | Add output guardrail for slide count validation (≥16) | 30min | §5.2 |
| 6 | Set `parallel_tool_calls=False` if dependency issues | 5min | §5.4 |
| 7 | Move examples from instructions.md to message history | 1h | §5.6 |
| 8 | Choose Path A (PPTX-aware HTML) when PPTX becomes priority | planning | §3.2 |

## 7.3 Medium-Term (Architecture)

| # | Action | Effort | Impact | Source |
|---|--------|--------|--------|--------|
| 1 | Progressive tool disclosure — load tools by format | 2-3h code | HIGH (40-60% token savings) | §4.1 |
| 2 | Auto-versioning for DOCX exports | 2-3h code | MEDIUM | §3.4 |
| 3 | Template registry for slide types | 1-2h code | MEDIUM | §6.2 |
| 4 | Structured slide plan output (typed JSON) | 1-2h code | MEDIUM | §6.1 |
| 5 | Dynamic instructions injection | 30min code | MEDIUM | §6.6 |
| 6 | Base64 image stripping for single-slide edits | 30min code | LOW | §6.4 |
| 7 | Split Forge assignments into dedicated agent folders | 1-2h org | MEDIUM | §2.3 |
| 8 | Apply tool design principles to new enrichment scripts | Future only | HIGH | §4.6 |

## 7.4 Complete Pattern Map

| # | Pattern | OpenSwarm File | Effort | Impact |
|---|---------|---------------|--------|--------|
| 1 | Agent instructions template | deep_research/instructions.md | 1-2h | HIGH |
| 2 | QA tester (5 queries + score) | .claude/agents/qa-tester.md | 30min | HIGH |
| 3 | Dual output format | data_analyst_agent/instructions.md | 30min | HIGH |
| 4 | Progressive tool disclosure | .cursor/commands/mcp-code-exec.md | 2-3h | HIGH |
| 5 | Input guardrails | agency-swarm docs | 30min | HIGH |
| 6 | Output guardrails with auto-retry | agency-swarm docs | 30min | HIGH |
| 7 | 1-3-1 debugging | virtual_assistant/instructions.md | 0 (habit) | HIGH |
| 8 | PPTX compatibility rules | slides_agent/html_writer_instructions.md | 30min | MEDIUM |
| 9 | Design vocabulary (orbs, kickers) | slides_agent/html_writer_instructions.md | 0 (CSS) | MEDIUM |
| 10 | Tool selection hierarchy | virtual_assistant/instructions.md | 15min | MEDIUM |
| 11 | Research methodology | .claude/agents/api-researcher.md | 1h | MEDIUM |
| 12 | Agency Context (self.context) | agency-swarm docs | 15min | MEDIUM |
| 13 | Structured slide plan (typed JSON) | InsertNewSlides.py | 1-2h | MEDIUM |
| 14 | Document formatting (versioning, sidebar) | docs_agent/instructions.md | 2-3h | MEDIUM |
| 15 | Tool design principles | .cursor/commands/create-prd.md | Future | HIGH |
| 16 | Dynamic instructions injection | slides_agent.py | 30min | MEDIUM |
| 17 | Shared state pattern | .claude/agents/tools-creator.md | Future | MEDIUM |
| 18 | Context window efficiency | virtual_assistant/instructions.md | 0 (habit) | MEDIUM |
| 19 | Template registry | ModifySlide.py | 1-2h | MEDIUM |
| 20 | Few-shot via message history | agency-swarm docs | 1h | MEDIUM |

---

# PART 8: DONE RIGHT / DO NOT TOUCH

These aspects of CogniESL are already equal or superior to OpenSwarm.

| Feature | Why We're Better |
|---------|-----------------|
| **HTML→DOCX/PDF pipeline** | Already exists. OpenSwarm's is nearly identical |
| **Single prompt → deliverables** | Same value proposition |
| **Error handling for end users** | "Silent recovery" better than exposing internal errors |
| **Quality gate system** | Forge's 6-pass system MORE rigorous than 5-query qa-tester |
| **Source discipline** | "Empty > Fabricated" is right for educational content |
| **Content Brief with teacher approval** | Stronger quality gate than anything OpenSwarm has |
| **Per-session agent state** | Session management is production-ready |
| **Pedagogical specificity** | Per-slide-type identity deeply ESL-optimized |
| **Speaker notes** | Mandatory on every slide. OpenSwarm has none |
| **Watermarking** | Full system with tier-based opacity |

---

# PART 9: RAW SOURCE FILES

## From OpenSwarm (saved in study root)

| File | Size | Source |
|------|------|--------|
| html_writer_instructions.md | 11KB | slides_agent/tools/ |
| docs_agent_instructions.md | 18KB | docs_agent/ |
| mcp-code-exec.md | 12KB | .cursor/commands/ |
| create-prd.md | 4.5KB | .cursor/commands/ |
| write-instructions.md | 4KB | .cursor/commands/ |
| data_analyst_instructions.md | 6.7KB | data_analyst_agent/ |
| virtual_assistant_instructions.md | 10KB | virtual_assistant/ |
| swarm.py | 3.1KB | root |
| config.py | 1.2KB | root |
| env.example | 2.3KB | root |
| slides_agent.py | 3.7KB | slides_agent/ |
| ModifySlide.py | 26KB | slides_agent/tools/ |
| InsertNewSlides.py | 21KB | slides_agent/tools/ |
| BuildPptxFromHtmlSlides.py | 8.4KB | slides_agent/tools/ |
| agency-swarm-workflow.mdc | 21KB | .cursor/rules/ |

## From Agency Swarm (saved in agency-swarm/ subfolder)

| File | Size | Content |
|------|------|---------|
| AGENTS.md | 39KB | Full framework guide |
| docs/input-guardrails.mdx | 10KB | Input validation |
| docs/output-guardrails.mdx | 8.3KB | Output validation with auto-retry |
| docs/agency-context.mdx | 9.5KB | Shared state |
| docs/advanced-configuration.mdx | 3.8KB | Parallel tools, file search, cache |
| docs/few-shot-examples.mdx | 2.5KB | Message history examples |
| docs/communication-flows.mdx | 5.4KB | Handoff vs SendMessage |
| docs/fastapi-integration.mdx | 15KB | FastAPI + Agency Swarm |
| docs/streaming.mdx | 8.6KB | Streaming responses |
| docs/built-in-tools.mdx | 2.3KB | WebSearch, FileSearch, CodeInterpreter |
| docs/third-party-models.mdx | 6.4KB | Non-OpenAI config |
| docs/observability.mdx | 5.9KB | Monitoring/tracing |
| docs/deployment.mdx | 5.3KB | Production deployment |
| docs/mcp-tools-server.mdx | 4.4KB | MCP server creation |
| docs/agency-overview.mdx | 4.7KB | High-level framework |
| docs/agency-swarm-cli.mdx | 4.6KB | CLI usage |

---

*Consolidated 2026-06-02 by Apex*
*Sources: VRSEN/OpenSwarm (21 .md + 8 .py/config files) + VRSEN/agency-swarm (15 .mdx docs)*
