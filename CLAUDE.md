# CogniESL: Project Specification for AI Development

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

State your assumptions explicitly. If uncertain, ask.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
If something is unclear, stop. Name what's confusing. Ask.
2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

No features beyond what was asked.
No abstractions for single-use code.
No "flexibility" or "configurability" that wasn't requested.
No error handling for impossible scenarios.
If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

Don't "improve" adjacent code, comments, or formatting.
Don't refactor things that aren't broken.
Match existing style, even if you'd do it differently.
If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:

Remove imports/variables/functions that YOUR changes made unused.
Don't remove pre-existing dead code unless asked.
The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

"Add validation" → "Write tests for invalid inputs, then make them pass"
"Fix the bug" → "Write a test that reproduces it, then make it pass"
"Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.


## Project Overview

**CogniESL** is an AI-powered ESL teaching material generator that will be offered as a subscription product. It generates complete, high-quality teaching materials (slides, worksheets, activity guides) tailored to students' native language(s) and proficiency level.

**Status**: In development. Phase 1 fixes in progress. Goal: Production-ready with premium quality materials.

---

## Core Principles

### 1. **Quality Over Speed**
- Materials must be pedagogically sound and visually stunning
- A single grammar error ruins the entire app's reputation
- All content is pulled from validated database, never AI-generated
- Teachers must feel that materials save them time and are worth paying for

### 2. **Database is Sacred**
- CogniESL has a VERY rich, pre-validated database:
  - **302 grammar files** with academic sources and pedagogical guidance
  - **36 L1 interference files** with language-specific error patterns and ratings
  - **220 activity templates** with instructions and differentiation
- **RULE**: Use database content exclusively. Never generate grammar or pedagogical content with AI.
- Database ensures zero grammatical errors and scientifically-grounded teaching practices

### 3. **L1-Aware Content is Critical**
- The unique value proposition: materials target specific errors that speakers of specific native languages make
- Each L1 file contains:
  - Specific interference patterns (e.g., Spanish speakers omit third-person -s)
  - Frequency, persistence, and communicative impact ratings
  - Peer-reviewed academic sources
  - Teacher tips on how to address the errors
  - Example sentences with wrong → correct pairs
- **RULE**: If an L1 is specified, L1 Oracle content MUST be generated for that language. No exceptions.

### 4. **Visual Quality Matters**
- Materials follow the **80/20 visual rule**: 80% visual content, 20% text
- Teacher evaluation question: "Would I pay a subscription for this?"
- Criteria:
  - Visually stunning (not boring, not generic)
  - Complete (no missing sections or empty slides)
  - Pedagogically sound (CCQs before formulas, L1-specific errors highlighted)
  - Saves time (teacher can use immediately, no editing needed)

---

## Data Structure & How It Guides Material Generation

### Grammar Files
**Location**: `/data/grammar/` (302 YAML files)

**Key fields used for slide generation**:
- `meaning.ccqs`: Concept Check Questions (show BEFORE formulas)
- `form.affirmative/negative/questions`: Formation rules with examples
- `sub_rules`: Spelling rules, irregulars (one slide per rule)
- `common_errors`: Wrong → correct pairs for practice section
- `phonetics`: Pronunciation notes, L1-specific issues
- `use`: Real-world contexts and examples (for practice/production)

### L1 Interference Files
**Location**: `/data/l1-interference/` (36 YAML files, one per language)

**Structure**: For each grammar point, contains:
- `interference_patterns`: Specific errors this L1 makes
- `why_it_happens`: Linguistic explanation
- `teacher_tips`: How to explain + exercises targeting this error
- `examples`: Wrong → correct pairs (e.g., "*He walk" → "He walks")
- `frequency`, `persistence`, `communicative_impact`: Rating 1-5 (prioritize high ratings)
- `sources`: Academic citations

**L1 Oracle Rule**: For each specified L1 language, create 1-2 slides highlighting:
- The specific error pattern (in red: "*He walk")
- The correction (in green: "He walks")
- Brief explanation of why (from `why_it_happens`)
- Examples from the L1 file

### Activity Files
**Location**: `/data/activities/` (220 YAML files)

**Key fields**:
- `instructions`: Step-by-step procedure (use verbatim)
- `script`: Exact words teacher should say
- `differentiation.support`: How to support lower-level students
- `differentiation.extension`: How to extend for advanced students
- `bestForLevels`: A1, A2, B1, B2, C1
- `l1Enhanced`: Indicates if it targets specific L1 issues

---

## Quality Validation Checklist

**These are NON-NEGOTIABLE. Agent must verify before responding to teacher:**

- [ ] **Slides Complete**: All slides > 2500 bytes (no empty slides)
- [ ] **Speaker Notes**: Every slide has `data-speaker-notes` with: teacher talk + CCQs + watch for
- [ ] **L1 Oracle**: For each specified L1, at least 1-2 dedicated slides with specific error examples
- [ ] **CCQs Present**: Concept Check Questions appear in Section 2 BEFORE formulas
- [ ] **Visual Quality**: 80/20 rule (80% visual, 20% text) — not text-heavy, not blank space
- [ ] **PPTX Built**: File exists and is > 100KB
- [ ] **Worksheet Complete**: Has Sections A-E + Answer Key with L1 explanations
- [ ] **No Duplicates**: No two slides have identical content
- [ ] **Age-Appropriate**: Activities match specified age group

---

## Testing Strategy

### Model Selection
**For Development/Testing**:
- **Claude Haiku** (via Claude Pro) — cheapest Claude, sufficient for testing
- **OpenRouter owl-alpha** (free) — if hitting Pro caps, use as fallback
- Both are capable enough to validate pipeline

**For Production**:
- Upgrade to Claude Sonnet after Phase 1 validates

### Test Progression

**Level 1: Basic**
- Test case: "Present Simple for adult Spanish speakers at beginner level"
- Expected: 15-18 slides with L1 Oracle for Spanish
- Validation: Visual inspection + teacher evaluation

**Level 2: Intermediate**
- Test case: "Past Simple for teenagers, Chinese and Spanish speakers, intermediate"
- Expected: 18-22 slides with L1 Oracle for BOTH languages
- Validation: Each L1 has dedicated content

**Level 3: Stress Test**
- Mixed languages, impossible requests, edge cases
- Test chat interview with difficult personas

---

## Implementation Approach

### Do Not
- ❌ Generate grammar content with AI (database only)
- ❌ Skip L1 Oracle sections
- ❌ Skip validation before responding
- ❌ Report empty or incomplete materials
- ❌ Accept poor visual quality

### Do
- ✅ Read and understand database FIRST
- ✅ Pull all content from validated database
- ✅ Verify L1 Oracle content for each specified language
- ✅ Run complete validation before delivery
- ✅ Visually inspect materials before responding
- ✅ Use cheap models for testing (Haiku, owl-alpha)
- ✅ Get teacher feedback on visual quality

---

## Success Criteria

**Phase 1**:
- ✓ End-to-end generation works (chat → materials)
- ✓ No empty slides or missing content
- ✓ All specified L1s have Oracle content
- ✓ Validation catches errors automatically
- ✓ Materials are visually acceptable for subscription
- ✓ Chat interview is smooth and intuitive

**Phase 2**:
- ✓ All 10 audit fixes implemented
- ✓ Comprehensive error handling
- ✓ Audit logging for debugging
- ✓ System is stable and predictable

**Phase 3**:
- ✓ UI enhancements
- ✓ Ready for production
- ✓ Subscription infrastructure ready

---

**Last Updated**: May 20, 2026  
**Status**: Ready for Phase 1 implementation
