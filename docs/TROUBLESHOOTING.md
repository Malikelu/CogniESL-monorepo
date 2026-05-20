# CogniESL — Troubleshooting Guide

> Common issues, their causes, and solutions.

---

## 1. Agent Issues

### Agent Doesn't Follow Instructions
**Symptoms**: Agent asks rigid questions, mentions CEFR levels, skips L1 content, generates materials before confirming.

**Causes & Fixes**:
- **Wrong model**: gpt-4o-mini has poor instruction following. Switch to Claude Haiku 4.5+.
  ```bash
  # In .env
  DEFAULT_MODEL=openrouter/anthropic/claude-haiku-4.5
  ```
- **Instructions unclear**: Review `agent/instructions.md`. Add explicit examples of what NOT to do.
- **Temperature too high**: Lower temperature in `cogniesl_agent.py`:
  ```python
  model_settings=ModelSettings(temperature=0.5)  # default is 0.7
  ```

### Agent Leaks Internal Context
**Symptoms**: Response contains `<memory-context>`, `[System note:...]`, or tool names.

**Fix**: The server already strips these with regex. If they still appear:
1. Check `server.py` cleanup patterns match the current format
2. The model may be generating new formats — add patterns to the cleanup list

### Agent Doesn't Use Tools
**Symptoms**: Agent responds without searching the database or generating files.

**Causes & Fixes**:
- **Model doesn't support tool calling**: Use a model with function-calling support
- **Tool descriptions unclear**: Improve `description` fields in tool classes
- **Instructions don't mention tools**: Update `agent/instructions.md` to explicitly reference tools

---

## 2. Session Issues

### Session Lost Between Requests
**Symptoms**: Agent doesn't remember previous messages in the conversation.

**Causes & Fixes**:
- **Missing X-Session-ID header**: Verify the Web UI sends it:
  ```typescript
  // In ChatInterface.tsx
  headers: { "X-Session-ID": getOrCreateSessionId() }
  ```
- **localStorage cleared**: Session ID is stored in localStorage. Incognito mode or clearing browser data loses it.
- **Server restarted**: In-memory sessions don't survive restart. Use Redis for persistence if needed.

### Session Timeout
**Symptoms**: After 30 minutes of inactivity, the agent starts fresh.

**Fix**: This is by design. `SESSION_TIMEOUT = 1800` in `server.py`. Increase if needed.

### Too Many Sessions (Memory Leak)
**Symptoms**: Server memory grows over time.

**Causes**:
- Sessions never expire (timeout not working)
- Each session holds an agent with full context

**Fixes**:
- Verify timeout logic in `server.py` `get_agent()` function
- Reduce `SESSION_TIMEOUT`
- Restart server periodically
- Monitor with: `len(_agents)` logging

---

## 3. Tool Issues

### Grammar Topic Not Found
**Symptoms**: "Error: No grammar point found for 'simple present'"

**Causes & Fixes**:
- **Wrong slug format**: Tool normalizes input, but verify the file exists:
  ```bash
  ls data/grammar/ | grep -i present
  ```
- **File not in directory**: Ensure the YAML file is in `data/grammar/`, not a subdirectory
- **YAML parse error**: Validate the YAML file:
  ```bash
  python3 -c "import yaml; yaml.safe_load(open('data/grammar/present_simple.yaml'))"
  ```

### L1 Data Not Found
**Symptoms**: "Error: No L1 interference data for 'Brazilian'"

**Causes**:
- Language name mismatch. The tool searches filenames. Check:
  ```bash
  ls data/l1-interference/ | grep -i port
  ```
- Use "Portuguese" not "Brazilian" — the data is by language, not nationality.

### Activity Search Returns Nothing
**Symptoms**: "No activities found for topic='present simple'"

**Causes**:
- Too many filters. Try with only `topic` first.
- Keywords don't match. Check the activity's `keywords` field.

---

## 4. File Generation Issues

### PPTX Not Generated
**Symptoms**: Agent reports success but no `.pptx` file exists.

**Debugging Steps**:
1. Check `./mnt/` directory:
   ```bash
   find ./mnt -name "*.pptx" -mmin -10  # Files modified in last 10 min
   ```
2. Check HTML intermediate files:
   ```bash
   find ./mnt -name "*.html" -mmin -10
   ```
3. If HTML exists but PPTX doesn't: `BuildPptxFromHtmlSlides` failed. Check Node.js is installed.

### PDF Not Generated
**Symptoms**: DOCX exists but PDF doesn't.

**Causes & Fixes**:
- **Playwright not installed**:
  ```bash
  python -m playwright install chromium
  ```
- **Chromium missing system libraries** (Docker):
  ```dockerfile
  # Already in Dockerfile, but verify:
  RUN apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 ...
  ```
- **Timeout**: PDF generation can take 30-60s. Check the 120s timeout in `route.ts`.

### Files in Wrong Directory
**Symptoms**: Files appear in `agent/mnt/` instead of `./mnt/`.

**Cause**: Path resolution uses `Path(__file__).parents[N]`. If the working directory is wrong, paths resolve incorrectly.

**Fix**: Always run `server.py` from the project root:
```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
python server.py
```

---

## 5. Import Errors

### `ModuleNotFoundError: No module named 'shared_tools'`
**Cause**: Absolute import in a tool file.

**Fix**: Check for `from shared_tools.X` and change to relative `from .X` or `from ..shared_tools.X`.

### `ModuleNotFoundError: No module name 'agency_swarm'`
**Cause**: Dependencies not installed.

**Fix**:
```bash
pip install -r requirements.txt
```

### `ImportError: cannot import name 'LitellmModel'`
**Cause**: Agency Swarm version mismatch.

**Fix**:
```bash
pip install "agency-swarm[fastapi,jupyter,litellm]>=1.9.7"
```

---

## 6. Web UI Issues

### "Sorry, I'm having trouble connecting to the backend"
**Causes**:
- Backend not running
- Wrong `OPENSWARM_URL` in Web UI env
- CORS issue

**Fixes**:
1. Verify backend is running: `curl http://localhost:8080/`
2. Check `OPENSWARM_URL` in Web UI environment
3. The Next.js API route proxies to the backend — ensure it's running on the expected port

### Chat Doesn't Scroll to Bottom
**Cause**: CSS overflow issue.

**Fix**: Check `globals.css` for proper flex layout. The chat container should have `flex-1 overflow-y-auto`.

### Session ID Not Persisting
**Cause**: localStorage not available (SSR, incognito).

**Fix**: The `getOrCreateSessionId()` function handles this. Verify it's being called correctly in `ChatInterface.tsx`.

---

## 7. Performance Issues

### Slow Response (>60s for conversation)
**Causes**:
- Model is slow (Haiku is faster than Sonnet)
- Too many tools registered (30+ tools increase context size)
- Complex conversation history

**Fixes**:
- Use Haiku for conversation-heavy flows
- Reduce tool count if possible
- Check model response time in OpenRouter dashboard

### Slow Material Generation (>5 min)
**Causes**:
- PPTX generation involves HTML → PPTX conversion (Node.js)
- PDF generation uses Playwright (Chromium)
- Image generation calls external APIs

**Fixes**:
- This is expected for complex presentations
- Monitor with logging at each step
- Consider async generation with status polling for production

---

## 8. Docker-Specific Issues

### Container Exits Immediately
**Cause**: Missing env var or import error.

**Debug**:
```bash
docker run -it --env-file .env cogniesl /bin/bash
python server.py
```

### Playwright/Chromium Not Found
**Cause**: Playwright browsers not installed in container.

**Fix**: The Dockerfile includes `RUN python -m playwright install chromium`. Rebuild if modified.

### Data Files Not Found
**Cause**: `COGNIESL_DATA_DIR` not set or files not copied.

**Debug**:
```bash
docker run -it cogniesl /bin/bash
ls /app/data/grammar/ | head
```

---

## 9. Getting Help

When reporting an issue, include:
1. **Model**: What model is configured in `.env`?
2. **Input**: What message did you send?
3. **Output**: What was the agent's response?
4. **Logs**: Server logs from `server.py`
5. **Environment**: Local, Docker, or Railway?
6. **Session ID**: From the `X-Session-ID` header
