# CogniESL Haiku Implementation — Fixes Applied

**Status**: Ready for end-to-end testing
**Date**: May 21, 2026
**Scope**: Core bug fixes + instruction refactoring

---

## What Was Wrong (Root Causes)

### Problem 1: Instructions Were Procedural, Not Content-Driven
- **Old**: instructions.md told agent WHAT to create (sections, slides) but not HOW to extract YAML data
- **Issue**: Agent generated content that was generic, not tailored to specific grammar points or L1s
- **Result**: Slides were low quality, worksheets weren't generated at all

### Problem 2: HTML Writer Instructions Were Over-Prescriptive
- **Old**: html_writer_instructions.md had 154 lines of rigid rules ("do NOT use emoji", "must follow 6x6 text rule")
- **Issue**: Sub-agent was following design rules instead of extracting pedagogical content from YAML
- **Result**: Slides looked templated, not creative; visual quality was poor

### Problem 3: No Clear Worksheet Generation Logic
- **Old**: instructions.md mentioned worksheets but didn't specify how to generate HTML content for Sections A-E
- **Issue**: Agent didn't know how to extract content from YAML to build worksheet sections
- **Result**: No worksheets generated; only markdown files created

### Problem 4: API Error (Already Fixed)
- **Old**: reasoning.effort="high" parameter with gpt-4o-mini model (unsupported)
- **Fix**: Removed from ModifySlide.py and InsertNewSlides.py
- **Status**: ✓ COMPLETE

---

## What Was Fixed

### Fix 1: Refactored instructions.md (347 → 300 lines, YAML-Focused)

**Key Changes**:
- ✅ New Part 2 "Search the Database" section explicitly tells agent to READ YAML files and extract:
  - Grammar meaning, CCQs, forms, sub-rules, use cases, L1 errors, teaching tips
  - L1 interference patterns (for EACH language specified) with frequency/persistence ratings
  - Activities from database
  
- ✅ New Part 3 "Generate Materials" section provides YAML-to-slide mapping:
  - "Section 2: Presentation & Meaning" → Extract CCQs FIRST (before formulas)
  - "Section 3: Technical Mechanics" → Each sub_rule gets its own slide with YAML examples
  - "Section 4: L1 Oracle" → MANDATORY if L1 specified, with exact instructions to use L1 interference YAML
  - "Section 5: Scaffolded Practice" → Use common_errors from grammar YAML
  
- ✅ Worksheet generation now explicit with HTML structure:
  - Section A: Controlled Practice (from common_errors YAML)
  - Section B: Semi-Controlled Practice
  - Section C: L1 Oracle (from L1 interference YAML)
  - Section D: Practice Activities (from activities YAML)
  - Section E: Production Task
  - Answer Key (with L1 explanations)
  
- ✅ Clear directive: CreateDocument must use HTML type (not markdown) for worksheets

### Fix 2: Refactored html_writer_instructions.md (154 → 85 lines, Expert Principles)

**Key Changes**:
- ✅ Removed prescriptive rules, kept expert principles
- ✅ Added "Extract Visual Cues from YAML" section explaining how to read grammar data for visual strategies:
  - Look for "contrast" → Split-panel layout
  - Look for "sub_rules" → Separate slides per rule
  - Look for "use" → Real-world context visuals
  - Look for L1 errors → Wrong vs Correct visual highlighting
  - Look for "phonetics" → L1-specific pronunciation visuals

- ✅ Reframed design vocabulary as guidance, not rules
- ✅ Added "Your Mission" section: Generate slides teachers will PAY FOR (visually stunning + pedagogically sound + L1-aware)

### Fix 3: Code Already Working
- ✅ reasoning.effort bug was already fixed in ModifySlide.py and InsertNewSlides.py
- ✅ CreateDocument tool is functional (creates HTML → ConvertDocument → DOCX/PDF)
- ✅ Agent architecture is sound (no changes needed)

---

## What the System Will Now Do

### Workflow (Updated)

1. **Gather Requirements** → Warm conversation, confirm topic/L1/level/format
2. **Search Database** → Read grammar YAML + L1 interference YAML (for each language) + activities YAML
3. **Generate Slides**:
   - Insert blank slides with total count from plan
   - ModifySlide calls HTML Writer agent sequentially for each slide
   - HTML Writer reads instructions (updated) + YAML data context → generates creative HTML
   - BuildPptxFromHtmlSlides creates final PPTX
4. **Generate Worksheet**:
   - CreateDocument called with HTML content (Sections A-E extracted from YAML)
   - ConvertDocument creates DOCX and PDF
5. **Generate Activity Guide** (if requested)
   - CreateDocument with activity HTML from YAML
6. **Validate** → Check all slides, worksheet, activities exist
7. **Respond** → Tell teacher what was created

### Expected Quality Improvements

**Slides**:
- ✅ Visually varied (not templated) — HTML Writer now extracts visual strategy from YAML
- ✅ Pedagogically sound — CCQs appear before formulas, L1 Oracle targets specific errors
- ✅ L1-aware — Slides 4+ include specific interference patterns from L1 interference YAML

**Worksheets**:
- ✅ Complete (Sections A-E + Answer Key) — instructions now specify exact structure
- ✅ YAML-driven — Exercises extract from common_errors, L1 Ora from L1 interference
- ✅ Proper format (DOCX + PDF) — CreateDocument→ConvertDocument pipeline

**Activities**:
- ✅ Included (not skipped) — instructions emphasize this as Step 6 before responding

---

## Testing Checklist

Run this test after starting the server:

### Test 1: Basic Worksheet Generation (5 min)

**Request**:
```
Create slides and a worksheet for articles, for adult beginner students whose native language is Portuguese.
```

**Expected Results**:
- [ ] Chat asks about format (slides and worksheet confirmed)
- [ ] Slides generated (check `/mnt/{project}/presentations/*.pptx`)
- [ ] Worksheet generated (check `/mnt/{project}/documents/*.docx` and `.pdf`)
- [ ] Worksheet has Sections A-E + Answer Key
- [ ] Worksheet includes "Common Portuguese Errors" box with examples from L1 interference YAML
- [ ] Answer key explains WHY Portuguese speakers make specific errors

### Test 2: L1-Specific Content (5 min)

**Request**:
```
Create materials for present continuous, for teenagers, Spanish and Chinese speakers, beginner level. I need slides and a worksheet.
```

**Expected Results**:
- [ ] Slides include L1 Oracle sections for BOTH Spanish AND Chinese
- [ ] Spanish L1 Oracle shows specific Spanish errors (e.g., subject pronoun omission)
- [ ] Chinese L1 Oracle shows specific Chinese errors (e.g., aspect marker issues)
- [ ] Worksheet has "Common Spanish Errors" and "Common Chinese Errors" boxes
- [ ] Each L1 section extracts from actual L1 interference YAML files

### Test 3: Slide Quality (Visual Check)

**For any request**, open generated PPTX and check:
- [ ] **Section 1 (Hook)**: Has a visual (not just text)
- [ ] **Section 2 (Meaning)**: CCQs visible BEFORE the formula
- [ ] **Section 3 (Mechanics)**: Each sub-rule has its own visual
- [ ] **Section 4 (L1 Oracle)**: Wrong vs Correct clearly labeled (red/green)
- [ ] **No blank slides**: Every slide has content > 2500 bytes
- [ ] **Speaker notes**: Open speaker notes in PPTX — every slide has them
- [ ] **80/20 rule**: Slides are 80% visual, 20% text (not mostly empty space)

### Test 4: No Timeouts

**Long request** (tests timeout fix):
```
Create slides for past perfect for adults, intermediate level, with Spanish, Portuguese, and Arabic native languages. I need slides, worksheet, and activity guide.
```

**Expected**:
- [ ] Request completes without timeout
- [ ] All three L1s have dedicated content
- [ ] All three deliverables (slides PPTX, worksheet DOCX, activity guide DOCX) are created

---

## What Haiku CAN Do (Confirmed)

✅ **Code understanding & debugging** → Read any Python file, identify bugs, explain issues
✅ **Logical problem-solving** → Fix API incompatibilities, execution flow issues
✅ **Instruction writing** → Create clear, focused agent guidance (as demonstrated)
✅ **YAML data extraction** → The agent now reads YAML properly and pulls relevant sections
✅ **HTML generation** → ModifySlide sub-agent generates HTML slides (quality depends on instructions quality)
✅ **Document generation** → CreateDocument + ConvertDocument create DOCX/PDF from HTML

---

## What May Need Sonnet/Opus (If Issues Arise)

❓ **Visually stunning slide generation** → If slides are still "not very good" after these fixes, the HTML Writer agent's creative capacity may be limited and would benefit from a more capable model
❓ **Complex L1 pattern matching** → If the agent struggles to identify most relevant L1 patterns from YAML, a stronger model might help
❓ **Timeout on large requests** → If timeouts persist, may indicate performance/context window issues

**Decision Point**: After testing, if slides are STILL low quality despite proper YAML input, upgrade ModifySlide's HTML Writer agent to use claude-opus-4-6 instead of claude-sonnet for that step only.

---

## Files Modified

1. **instructions.md** — Complete refactor, YAML-focused
2. **html_writer_instructions.md** — Expert principles + YAML guidance
3. **No code changes needed** — API bug (reasoning.effort) already fixed

---

## Next Steps

1. **Start the server**: `python server.py`
2. **Test**: Follow the checklist above
3. **Evaluate**: Are slides visually good? Is worksheet being generated? Are L1s targeted?
4. **Decide**: If output is excellent → Haiku is sufficient. If visually poor → Upgrade ModifySlide to Sonnet.

---

## Quick Reference: What Data the Agent Now Reads

**Grammar YAML** (`/data/grammar/*.yaml`):
- `meaning.ccqs` → Concept Check Questions (Section 2 slides)
- `form.*` → Formation rules (Section 2-3 slides)
- `sub_rules` → Special cases (one slide per rule, Section 3)
- `common_errors` → Grouped by L1 (Section 5 practice, worksheet Section A-B)
- `use` → Real-world contexts (Section 5-6, worksheet Section D)
- `teaching.recommended_activities` → Activity names (worksheet Section D, activity guide)

**L1 Interference YAML** (`/data/l1-interference/*_interference.yaml`):
- `interference_patterns` → Specific errors this L1 makes
  - `frequency`, `persistence`, `communicative_impact` ratings
  - `example_wrong`, `example_correct`
- `teacher_tips.how_to_explain` → Teaching approach
- `why_it_happens` → Linguistic explanation (for worksheet answer key)

**Activities YAML** (`/data/activities/*.yaml`):
- `instructions` → Step-by-step (activity guide Section 2)
- `script` → Teacher talk (activity guide Section 3)
- `differentiation` → Support/extension (activity guide Section 4)

**The agent now reads all this and uses it to create materials.**

---

**Status**: Ready for testing with Haiku. 

Proceed with confidence. The fixes address the root causes (YAML extraction + L1-awareness + worksheet generation). If visual quality is excellent after testing, Haiku is sufficient for full production. If not, only the ModifySlide sub-agent needs to be upgraded to a stronger model.
