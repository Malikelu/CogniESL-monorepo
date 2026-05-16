# CogniESL

AI-powered ESL teaching material generator. Teachers describe what they need, and CogniESL generates professional materials (slides, worksheets, activities) tailored to their students' language background.

## Architecture

```
Teacher → OpenSwarm Orchestrator → Specialist Agent → Materials → ZIP
```

- **Orchestrator:** Understands ESL teaching requests, searches the database, routes to specialists
- **Slides Agent:** Creates professional PPTX presentations with L1 callouts
- **Docs Agent:** Creates worksheets, exercises, and activity resources

## Project Structure

```
CogniESL/
├── data/                  # ESL database (YAML files)
│   ├── grammar/           # 300 grammar points
│   ├── activities/        # 218 classroom activities
│   └── l1-interference/   # 34 L1 interference files
├── docs/                  # Reference documentation
│   ├── ARCHITECTURE_REDESIGN.md
│   ├── OPENSWARM_ANALYSIS.md
│   └── ESL_Presentation_Master_Rules.md
├── openswarm/             # Forked OpenSwarm (customized)
│   ├── orchestrator/      # Custom ESL orchestrator + tools
│   ├── slides_agent/      # ESL slide generation
│   ├── docs_agent/        # ESL document generation
│   └── ...
└── webui/                 # Next.js chat interface (Phase 5)
```

## Quick Start

### 1. Set up environment
```bash
cd openswarm
cp .env.example .env
# Add your OpenAI API key to .env
```

### 2. Install dependencies
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run CLI demo
```bash
python run.py
```

### 4. Run API server
```bash
python server.py
```

## Custom Tools

Three custom tools are available to the Orchestrator:

1. **SearchGrammarTool** — Search grammar database by topic (fuzzy matching)
2. **SearchActivitiesTool** — Search activities by topic/level/age/L1
3. **GetL1InterferenceTool** — Get L1 interference patterns for grammar point + language

## Tech Stack

- **Backend:** OpenSwarm (Python, Agency Swarm, FastAPI)
- **LLM:** OpenAI (default), Anthropic (planned)
- **Data:** YAML files (300 grammar points, 218 activities, 34 L1 files)
- **Web UI:** Next.js 16, Tailwind v4 (Phase 5)
- **Deployment:** Railway (backend), Vercel (frontend)
