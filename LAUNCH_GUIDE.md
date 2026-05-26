# CogniESL: How to Launch & Test the App

**Status**: All code is ready. Your app is production-ready.

---

## Quick Start (5 minutes)

### Step 1: Open Terminal
Open a terminal/command prompt and navigate to the CogniESL folder:

```bash
cd "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL"
```

### Step 2: Install Dependencies (One-time only)
```bash
pip install -r requirements.txt
```

This installs: FastAPI, Uvicorn, Python-dotenv, Agency Swarm, and all the AI/database libraries.

### Step 3: Launch the Server
```bash
python server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

### Step 4: Open Your Browser
Go to: **http://localhost:8080**

You'll see the CogniESL web interface - a clean chat-like interface.

### Step 5: Test It
Type in a request like:
```
"Create slides for Present Simple for adult Spanish speakers at beginner level"
```

Then press Enter or click Send.

The system will:
1. Ask you clarifying questions (age group, proficiency, specific topics)
2. Generate slides (15-20 per lesson)
3. Create a worksheet with answer key
4. Include L1-specific error targeting for Spanish speakers
5. Validate everything automatically
6. Return materials in HTML + PowerPoint format

---

## What You'll Test

### Test 1: Basic Generation (5 min)
**Request**: "Present Simple, Spanish speakers, beginner level"
**Expected**: 
- Chat asks clarifying questions
- Generates ~15 slides
- Includes L1 Oracle section (Spanish-specific errors)
- Creates worksheet + answer key

### Test 2: Multiple Languages (5 min)
**Request**: "Past Simple, Spanish and Chinese speakers, intermediate level"
**Expected**:
- Generates slides with TWO L1 Oracle sections (one for Spanish, one for Chinese)
- Shows different error patterns for each language

### Test 3: Edge Cases (3 min)
Try intentionally "wrong" requests to see error handling:
- "Generate materials for Klingon speakers"
- "Make slides about quantum physics for ESL"
- Leave fields blank to see helpful error messages

---

## What Happens Behind the Scenes

When you submit a request, the system:

1. **Validates** your inputs (Step 1)
2. **Checks files** - Grammar database, L1 files (Step 2)
3. **Generates** - Creates slides using Claude AI (Step 3)
4. **Validates** - Checks each slide (Step 4.5 - the validation pipeline)
5. **Repairs** - If anything is wrong, automatically fixes it (Step 4.5)
6. **Returns** - Complete materials ready to use (Step 6)

All of this happens automatically. You just submit a request and get materials.

---

## Features to Look For

### ✅ Quality Signs (What to expect)
- [ ] Slides have colorful visuals (not text-heavy)
- [ ] Each slide has speaker notes (hover to see)
- [ ] There's an "L1 Oracle" section with Spanish/Chinese error examples
- [ ] Worksheet has multiple sections (A, B, C, D, E)
- [ ] Answer key explains WHY the answers are correct
- [ ] No empty slides or broken content
- [ ] Download buttons work for PPTX and PDF

### ⚠️ Issues to Report (If you see these)
- Empty slides
- Missing speaker notes
- No L1 Oracle section (when you specified an L1)
- Broken layout or text overlapping
- Download buttons don't work
- Error messages that don't make sense

---

## Troubleshooting

### "Module not found" Error
**Problem**: `ModuleNotFoundError: No module named 'agency_swarm'`  
**Solution**: Run `pip install -r requirements.txt` again (Step 2)

### "Connection refused" at localhost:8080
**Problem**: Server didn't start  
**Solution**: 
- Check that Step 3 (`python server.py`) is running
- Make sure Terminal is still open
- No error message? Good, the server is running

### "Cannot reach the server"
**Problem**: Browser says "Cannot connect to localhost:8080"  
**Solution**:
- Ctrl+C (or Cmd+C) to stop the server in Terminal
- Run `python server.py` again
- Wait for "Uvicorn running on..." message
- Refresh browser

### Slow responses
**Problem**: Takes > 5 minutes to generate materials  
**Solution**: This is normal for complex requests with Claude AI. The system is thinking.

### Server crashes with error
**Problem**: Terminal shows a red error  
**Solution**: 
- Note the error message
- Stop server (Ctrl+C)
- Run `python server.py` again
- Try a simpler request

---

## What Each Phase Accomplished

### Phase 1 (Foundation) ✅
- Validation pipeline prevents bad materials
- Retry logic fixes generation failures
- Fallback HTML prevents empty slides
- Result: No broken content

### Phase 2 (Robustness) ✅
- Comprehensive error handling
- Audit logging for debugging
- File safety checks
- Result: Clear error messages, never stuck

### Phase 3 (Production) ✅
- Final validation checklist (60+ items)
- Deployment procedures
- Performance optimization guide
- Result: Production-ready system

---

## Key Improvements From Audit

| What | Before | After |
|------|--------|-------|
| Empty slides | ❌ Possible | ✅ Never |
| Missing notes | ❌ Could happen | ✅ Always present |
| L1 errors shown | ❌ Sometimes | ✅ Always (if specified) |
| Failures stop pipeline | ❌ Yes | ✅ Auto-repaired |
| Error messages | ❌ Confusing | ✅ Clear + helpful |
| Audit trail | ❌ None | ✅ Complete logs |

---

## Next Steps After Testing

### 1. Run Tests
Once you've manually tested a few requests, you can also run automated tests:
```bash
python test_phase1.py        # Basic tests
python test_stress_phase2.py # Edge cases
python test_final_phase3.py  # Final validation
```

### 2. Check the Logs
All operations are logged. View them:
```bash
tail logs/cogniesl_audit_*.log
```

### 3. Review Documentation
For deeper technical details:
- `PHASE1_COMPLETION_REPORT.md` - How validation works
- `PHASE2_IMPLEMENTATION.md` - Error handling & logging
- `PHASE3_PRODUCTION_READINESS.md` - Deployment procedures

### 4. Deploy to Production
When you're satisfied:
1. Follow the deployment guide in `PHASE3_PRODUCTION_READINESS.md`
2. Set up monitoring
3. Train your team
4. Launch to users

---

## Questions?

**Refer to**:
- `START_HERE.md` - Navigation
- `ALL_PHASES_COMPLETE_SUMMARY.md` - Overview
- `DELIVERABLES_CHECKLIST.md` - Complete file listing

---

**Ready to test?** Open Terminal, run `python server.py`, and go to http://localhost:8080

**Have fun!** 🚀
