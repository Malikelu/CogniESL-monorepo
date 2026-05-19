# CogniESL — Complete Handoff Document for Claude Code

## PART 1: CONCEPT (READ THIS FIRST)

CogniESL is an AI-powered ESL teaching material generator. Teachers describe what they need in natural language, and CogniESL generates professional teaching materials (slides, worksheets, activities) tailored to their students' native language (L1).

The key differentiator is **L1 interference targeting** — CogniESL knows that Portuguese speakers say "She work" instead of "She works," and builds materials that specifically address those errors.

**Full concept document:**
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/docs/CONCEPT.md`

**ESL Presentation Master Rules (design standards for materials):**
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/docs/ESL_Presentation_Master_Rules.md`

**Architecture documents:**
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/docs/ARCHITECTURE_REDESIGN.md`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/docs/OPENSWARM_ANALYSIS.md`

## PART 2: REFERENCE LINKS

- OpenSwarm GitHub: https://github.com/VRSEN/OpenSwarm
- Agency Swarm: https://github.com/agency-swarm/agency-swarm

## PART 3: COMPLETE CODEBASE FILES (READ ALL)

### Web UI (Next.js)
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/src/app/page.tsx`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/src/app/layout.tsx`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/src/app/globals.css`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/src/app/api/chat/route.ts`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/src/components/ChatInterface.tsx`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/package.json`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/webui/next.config.ts` (or .js)

### Backend Core
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/config.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/cogniesl_swarm.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/server.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/.env`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/shared_instructions.md`

### Orchestrator
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/orchestrator.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/instructions.md`

### ESL Intake Agent
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/esl_intake_agent/esl_intake_agent.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/esl_intake_agent/instructions.md`

### ESL Pedagogy Agent
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/esl_pedagogy_agent/esl_pedagogy_agent.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/esl_pedagogy_agent/instructions.md`

### Slides Agent
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/slides_agent/slides_agent.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/slides_agent/instructions.md`

### Docs Agent
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/docs_agent/docs_agent.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/docs_agent/instructions.md`

### Custom Tools
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/custom_tools/__init__.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/custom_tools/SearchGrammarTool.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/custom_tools/SearchActivitiesTool.py`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/orchestrator/custom_tools/GetL1InterferenceTool.py`

### Data Files (Sample — read structure)
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/data/grammar/present_simple.yaml`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/data/grammar/articles.yaml`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/data/l1-interference/portuguese_interference.yaml`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/data/activities/3-2-1-exit.yaml`

### Generated Output (from previous testing — verify these exist)
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/mnt/present_simple_tense/presentations/slide_01.html`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/mnt/present_simple_worksheets/documents/present_simple_worksheet.docx`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/mnt/present_simple_worksheets/documents/present_simple_worksheet.pdf`

## PART 4: DEPLOYMENT CONTEXT

### Current Deployment
- **Backend:** Railway (openswarm folder)
- **Web UI:** Vercel (webui folder)
- **Environment variables needed:** OPENAI_API_KEY, DEFAULT_MODEL, ORCHESTRATOR_MODEL, PORT

### Deployment Files
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/Dockerfile`
`/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm/railway.json`

## PART 5: KNOWN ISSUES (FROM TESTING)

### Issue 1: ESL Intake Agent Doesn't Follow Instructions
The Intake Agent should ask 4 questions (L1, age, format, confirm) then transfer. Instead, it responds with teaching content. The model (gpt-4o-mini) ignores "you are an interviewer" instructions. Tested with 4 different instruction approaches — none work reliably.

### Issue 2: reasoning.effort Error
Slides Agent and Docs Agent have `reasoning=Reasoning(effort="...")` in model_settings. gpt-4o-mini doesn't support this. Causes HTTP 400 errors.

### Issue 3: API Conversation State
The server creates a new agency per request. Even with chat_history sent from the Web UI, the Orchestrator doesn't reliably transfer in a fresh agency context.

### Issue 4: ESL Pedagogy Agent Output
May not be creating proper Lesson Scripts. Needs audit.

### Issue 5: Production Agents Using L1 Data
Slides/Docs agents may not be properly incorporating L1 interference data into generated materials.

## PART 6: WHAT WORKS (FROM TESTING)

- Agent communication flows (handoff, send_message) work correctly
- Custom tools (SearchGrammar, SearchActivities, GetL1Interference) work
- Production agents CAN generate files (15 HTML slides + DOCX + PDF were generated)
- Data files are well-structured and complete
- Orchestrator → ESL Intake Agent transfer works in persistent (TUI) context
- Full pipeline works in TUI mode: Orchestrator → Intake → Pedagogy → Production

## PART 7: YOUR TASK

1. Read ALL files listed above (start with CONCEPT.md)
2. Identify all bugs, issues, and missing pieces
3. Fix the known issues
4. Ensure the full flow works through the API:
   - "I need ESL materials for present simple for Portuguese-speaking adults"
   - "Slides and worksheets"
   - "Yes, generate them"
5. Verify materials include L1-specific content
6. Verify Web UI can communicate with backend
7. Report what you found and fixed

## PART 8: CONSTRAINTS

- Do NOT modify data files (grammar, activities, L1 interference)
- Do NOT change the core OpenSwarm/Agency Swarm framework
- Keep the existing agent architecture or ask Marcos if yo ufind a better solution
- Use gpt-4o-mini as default model (gpt-4o is too expensive for production, UNLESS the model becomes a problem because it is not good enough)
- Maintain the existing file structure or suggest a better strucutre if necessary
