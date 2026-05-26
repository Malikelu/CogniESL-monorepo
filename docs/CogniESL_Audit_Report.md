# CogniESL Audit Report: Agent Generation Pipeline

## Executive Summary

**CogniESL** is an agentic ESL teaching material generator that orchestrates a complex multi-tool pipeline to produce slides, worksheets, and activity guides. The system has **strong foundational design** (clear pedagogical rules, L1-aware content generation, comprehensive database structure) but suffers from **critical implementation issues** that undermine output quality:

- **Fragile content generation**: Slides frequently come back empty or incomplete
- **Weak validation**: No automated checks ensure materials meet quality standards
- **Model capability mismatch**: Using free Google Gemma-4 due to Claude reasoning model failures
- **Manual error recovery**: Pipeline requires human intervention to detect and fix failures
- **Unclear L1 targeting**: No guarantee that language-specific error patterns are included
- **Speaker notes inconsistency**: No automated validation that notes exist on every slide

---

## Project Structure

```
CogniESL/
├── .env                              # OpenRouter API key, DEFAULT_MODEL config
├── server.py                         # FastAPI server (port 8080), session management
├── agent/
│   ├── cogniesl_agent.py            # Main agent, registers 40+ tools
│   ├── config.py                    # Model routing via LitellmModel
│   ├── instructions.md              # Agent system prompt (301 lines, critical)
│   ├── slides_tools/
│   │   ├── InsertNewSlides.py       # Sub-agent: creates slide plan + blanks
│   │   ├── ModifySlide.py           # Sub-agent: generates HTML per slide
│   │   ├── BuildPptxFromHtmlSlides.py
│   │   ├── html_writer_instructions.md
│   │   ├── slide_html_utils.py      # ensure_full_html(), validate_html()
│   │   ├── slide_file_utils.py
│   │   └── template_registry.py
│   ├── docs_tools/
│   │   ├── CreateDocument.py
│   │   ├── ModifyDocument.py
│   │   ├── ConvertDocument.py
│   │   └── ...
│   ├── shared_tools/
│   └── tools/                        # SearchGrammarTool, GetL1InterferenceTool, etc.
├── data/
│   ├── grammar/                      # 100+ YAML files with grammar content
│   └── activities/                   # Activity templates
└── mnt/                              # Generated presentations stored here
```

---

## Critical Issues Found

### 1. **Fragile Slide Generation Pipeline** ⚠️ SEVERITY: CRITICAL

**Problem**: The ModifySlide tool uses a sub-agent to generate HTML for each slide. The instructions explicitly state:

> "After each ModifySlide call, verify the slide was actually populated by checking the file size. If the file is under 2500 bytes, it is likely empty — call ModifySlide again"

This indicates slides are **frequently failing silently**. The agent should not require manual file size checks.

**Root Cause**: 
- Sub-agent architecture is over-complex for simple HTML generation
- No built-in validation or retry logic in the tool itself
- Agent relies on post-hoc human verification

**Impact**:
- Teachers get incomplete materials
- Agent must retry multiple times per slide
- Pipeline becomes unpredictable and slow

**Fix**:
1. Add automatic validation inside ModifySlide
2. Built-in retry logic (up to 3 attempts) before failing
3. Minimum content validation before returning success
4. Log warnings if file < 2500 bytes

---

### 2. **Model Capability Mismatch** ⚠️ SEVERITY: CRITICAL

**Problem**: The `.env` file shows:

```
# Production: openrouter/anthropic/claude-sonnet-4.6
# NOTE: openrouter/owl-alpha was tried but causes infinite reasoning loops
# Switched to gemma-4 which is also free but actually completes the pipeline.
DEFAULT_MODEL=openrouter/google/gemma-4-26b-a4b-it:free
```

**Analysis**:
- Claude Sonnet (intended production model) causes **infinite reasoning loops**
- Using free Google Gemma-4 as fallback, which lacks reasoning ability
- Gemma-4 is "non-reasoning" model — cannot handle complex task decomposition
- System requires sophisticated multi-step reasoning for pedagogical correctness

**Impact**:
- Agent cannot reason about L1 error patterns properly
- Slide content generation is superficial and formulaic
- No guarantee of educational quality
- Free model may be inconsistent or unreliable

**Fix**:
1. Debug why Claude Sonnet causes infinite loops (likely over-complex agent prompt)
2. Simplify agent instructions to reduce reasoning overhead
3. Break complex tasks into simpler sub-tasks
4. Consider switching to Claude 3.5 Sonnet or another capable model
5. Add timeouts and early-exit conditions for reasoning

---

### 3. **Missing Automated Validation Checklist** ⚠️ SEVERITY: HIGH

**Problem**: The instructions include a 12-point validation checklist:

```markdown
### Validation Checklist (Run This Before Responding)

- [ ] All slides have content
- [ ] Speaker notes on EVERY slide
- [ ] L1 Oracle section exists for EACH language
- [ ] CCQs are present in Section 2
- [ ] PPTX was built successfully
- [ ] Worksheet has an answer key
- [ ] Activities are age-appropriate
- [ ] 80/20 visual rule
- [ ] No duplicate slides
```

**Current State**: This checklist is **entirely manual**. The agent must:
1. Read each slide HTML file
2. Check file size > 2500 bytes
3. Grep for `data-speaker-notes`
4. Verify language names appear in content
5. Count slides in the plan vs. actual slides

**Expected State**: This should be **completely automated** before the agent responds to the teacher.

**Impact**:
- Validation is inconsistent and error-prone
- Teachers receive incomplete/invalid materials
- Agent cannot detect its own failures
- User must manually verify quality

**Fix**:
1. Create a `ValidationTool` that runs after PPTX creation
2. Automate all checklist items:
   - Verify each slide file exists and > 2500 bytes
   - Grep every slide for `data-speaker-notes`
   - Count total slides vs. plan
   - Validate 80/20 visual rule (image area / text area)
   - Check for duplicates
3. Return a validation report to the agent
4. Agent should **not respond to teacher** until all checks pass
5. Auto-retry failed slides before reporting errors

---

### 4. **No Guaranteed L1 Oracle Content** ⚠️ SEVERITY: HIGH

**Problem**: The instructions state:

> "Section 4: L1 Oracle (1-2 slides per L1) — CRITICAL when L1 data exists"
> 
> "If the teacher specified MULTIPLE L1s (e.g., 'Chinese and Spanish speakers'), create L1 Oracle content for EACH language."

**Current State**:
- System searches GetL1InterferenceTool for each L1
- But there's **no validation** that L1-specific slides were actually created
- No check that error patterns with high frequency/persistence are included
- Agent may skip L1 content if ModifySlide fails

**Impact**:
- Materials may miss the most critical teaching point (L1-specific errors)
- Teacher has no way to know if content targets their students' actual errors
- Undermines the whole value proposition of L1-aware generation

**Fix**:
1. Add **L1OracleValidator** tool that:
   - Counts L1 Oracle slides per language
   - Verifies specific error patterns are present
   - Checks that ratings (frequency, persistence) are considered
   - Flags slides with generic L1 content
2. Agent must track L1 coverage throughout pipeline
3. Fail the pipeline if any specified L1 is missing content
4. Respond to teacher with L1 summary: "Targeting Spanish-specific errors (3-person -s omission, etc.)"

---

### 5. **Speaker Notes Not Guaranteed** ⚠️ SEVERITY: HIGH

**Problem**: Instructions say:

> "Every single slide MUST include speaker notes using the `data-speaker-notes` attribute. This is non-negotiable."

But validation is manual (grep for `data-speaker-notes` across all files).

**Current State**:
- No automated check that speaker notes exist
- If ModifySlide fails partially, speaker notes might be missing
- No fallback mechanism to add them

**Impact**:
- Teachers may receive slides without guidance on what to say
- Undermines pedagogical effectiveness
- Violates explicit requirement

**Fix**:
1. Make speaker notes **mandatory in the HTML writer instructions**
2. Add a **SpeakerNotesValidator** tool that:
   - Verifies every slide has `data-speaker-notes`
   - Validates notes include: Teacher talk, CCQs, Watch for
   - Flags empty or minimal notes
3. If slide missing notes, trigger auto-regeneration
4. Agent cannot proceed to PPTX build if any slide lacks notes

---

### 6. **Silent Failures in Sub-agents** ⚠️ SEVERITY: HIGH

**Problem**: InsertNewSlides and ModifySlide use sub-agents. If a sub-agent fails:

- The tool may return a partial/empty response
- Main agent continues without noticing
- User gets incomplete materials

Example from instructions:
> "If ModifySlide fails for a slide, do NOT skip it. Retry with simplified content. If it fails 3 times, create a basic HTML slide manually using the Write tool."

**Current State**: Retry logic is **documented but not implemented** in the tools themselves.

**Impact**:
- Pipeline is brittle and requires manual oversight
- No guaranteed error recovery
- Teacher has no visibility into tool failures

**Fix**:
1. Implement automatic retry logic in ModifySlide:
   ```python
   def run(self):
       for attempt in range(1, 4):
           try:
               result = self._generate_html(...)
               if self._validate(result):
                   return result
           except Exception as e:
               if attempt == 3:
                   raise
       # Fallback: create minimal valid HTML
       return self._fallback_html()
   ```
2. Add retry budgets per slide
3. Log all failures for debugging
4. Provide fallback slide template

---

### 7. **No Content Quality Gates** ⚠️ SEVERITY: MEDIUM

**Problem**: No verification that generated content:
- Actually teaches the topic
- Follows the 80/20 visual rule
- Is age-appropriate
- Makes sense pedagogically

**Current State**: The 80/20 rule is mentioned in instructions but never validated:
> "80/20 visual rule (80% visual, 20% text) — Spot-check 3-4 slides"

"Spot-check" means **manual, inconsistent validation**.

**Impact**:
- Materials may be visually confusing or text-heavy
- Pedagogical structure may be incorrect
- Teacher must review every slide before using

**Fix**:
1. Create a **ContentQualityValidator**:
   - Measure image vs. text area (using Playwright)
   - Flag slides that violate 80/20 rule
   - Check for orphaned text (text without adjacent visual)
   - Verify slide count matches pedagogy (more complex topics = more slides)
2. Run validator on all slides before PPTX build
3. Report quality scores to agent and teacher
4. Flag low-quality slides for regeneration

---

### 8. **Weak Requirement Gathering** ⚠️ SEVERITY: MEDIUM

**Problem**: The agent follows a conversational flow to gather requirements:
- Topic/grammar point
- L1/native language
- Age group
- Level
- Format

But there's **no validation** that requirements are:
- Sufficient to generate materials
- Consistent with system capabilities
- Actually confirmed by the teacher

**Impact**:
- Agent may proceed with incomplete information
- Teacher changes mind mid-process
- No clear confirmation step before generation starts

**Fix**:
1. Add a **RequirementValidator** tool
2. Before proceeding to generation, agent should:
   - Confirm all 5 parameters are specified
   - Show a summary: "Creating **slides + worksheet** for **present simple** for **adult students** from **Brazil** at **beginner** level"
   - Wait for explicit teacher confirmation
   - Store confirmed requirements for audit trail
3. Flag any missing parameters

---

### 9. **File Path References Unverified** ⚠️ SEVERITY: MEDIUM

**Problem**: Instructions say:

> "Verify files exist before reporting them. Check the actual file paths on disk:
> - Slides: `./mnt/{project_name}/presentations/{project_name}.pptx`"

But there's **no tool** that does this automatically.

**Impact**:
- Agent may report files that don't exist
- Teacher gets error when trying to download
- Looks unprofessional

**Fix**:
1. Add automatic file existence check after PPTX build
2. Only report files that exist on disk
3. Include file size in report
4. Provide direct download links (if web UI available)

---

### 10. **No Audit Trail or Logging** ⚠️ SEVERITY: MEDIUM

**Problem**: 
- No record of what was generated
- No timestamps
- No error logs for debugging
- Can't track what materials exist

**Impact**:
- Hard to debug failures
- No accountability
- Difficult to improve pipeline

**Fix**:
1. Create a generation log file per teacher request:
   ```
   {
     "timestamp": "2026-05-20T10:30:00Z",
     "teacher_id": "...",
     "requirements": {...},
     "database_searches": [...],
     "slide_generation": {...},
     "validation_results": {...},
     "output_files": [...]
   }
   ```
2. Log all tool calls and results
3. Include in final response to teacher

---

## Design Strengths ✅

The system has excellent foundational design:

1. **Clear Pedagogical Framework**: 
   - Engagement hook → Presentation → Mechanics → L1 Oracle → Practice → Production
   - Speaker notes on every slide
   - CCQs before formulas

2. **L1-Aware Content**:
   - Searches for language-specific errors
   - Targets high-frequency patterns
   - Customizable per language

3. **Comprehensive Database**:
   - 100+ grammar YAML files
   - L1 interference patterns
   - Activity templates

4. **Professional Output**:
   - PPTX with editable elements
   - Worksheets with answer keys
   - Consistent design system

5. **Visual Design Standards**:
   - Clear CSS architecture
   - Responsive layout system
   - Accessibility considerations

---

## Recommended Fix Priority

### Phase 1: Critical (Do First)
1. **Add ValidateAndFixSlides tool** — automated file checks + auto-retry
2. **Implement automatic validation checklist** — runs before responding to teacher
3. **Fix model configuration** — debug Claude Sonnet loop issue, switch to better model
4. **Add L1OracleValidator** — ensure L1 content exists for each language

### Phase 2: High (Do Next)
5. **Add SpeakerNotesValidator** — verify notes on every slide
6. **Add ContentQualityValidator** — check 80/20 visual rule
7. **Implement auto-retry in ModifySlide** — built into tool, not manual
8. **Add RequirementValidator** — confirm parameters before generation

### Phase 3: Medium (Polish)
9. **Add audit logging** — JSON logs per generation
10. **Add file existence validation** — verify outputs before reporting
11. **Create generation status page** — show progress to teacher
12. **Add error recovery UI** — let teacher trigger regeneration per slide

---

## Summary

**CogniESL has strong design but weak execution.** The pipeline is:
- ✅ Pedagogically sound
- ✅ L1-aware and customizable
- ✅ Technically feasible
- ❌ Fragile and error-prone
- ❌ Requires manual validation
- ❌ Limited by model capability

**Primary fixes** (do these first):
1. Automate the validation checklist
2. Add retry logic to ModifySlide
3. Debug and fix Claude model selection
4. Ensure L1 Oracle content is always generated
