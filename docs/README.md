# CogniESL — Documentation Index

## Start Here

1. **[CONCEPT.md](./CONCEPT.md)** — What is CogniESL? Who is it for? Why does it exist?
2. **[ARCHITECTURE.md](./ARCHITECTURE.md)** — System architecture, design decisions, and request flow.
3. **[CLAUDE_CODE_HANDOFF.md](./CLAUDE_CODE_HANDOFF.md)** — Complete handoff for AI developers.

## Reference

- **[DATA_FORMAT.md](./DATA_FORMAT.md)** — YAML schemas for grammar, L1 interference, and activities.
- **[TOOLS_REFERENCE.md](./TOOLS_REFERENCE.md)** — Every tool available to the agent, with parameters and usage patterns.
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** — How to build, configure, and deploy.
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** — Common issues and solutions.

## Design Standards

- **[ESL_Presentation_Master_Rules.md](./ESL_Presentation_Master_Rules.md)** — Pedagogical and visual standards for generated materials (80/20 rule, 6x6 rule, PPP framework, L1 Oracle section).

## Key Paths

| What | Where |
|------|-------|
| Agent definition | `agent/cogniesl_agent.py` |
| Agent instructions | `agent/instructions.md` |
| Server | `server.py` |
| Custom tools | `agent/tools/` |
| Slides tools | `agent/slides_tools/` |
| Docs tools | `agent/docs_tools/` |
| Grammar data | `data/grammar/` (300 files) |
| Activity data | `data/activities/` (218 files) |
| L1 interference data | `data/l1-interference/` (34 files) |
| Web UI | `webui/src/` |
| Environment | `.env` |
