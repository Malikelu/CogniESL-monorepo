# CogniESL Implementation Fixes

Complete implementation guide with code snippets for all 7 fixes. See AUDIT_SUMMARY.md and CogniESL_Audit_Report.md for context.

---

## Fix 1: Automate the Validation Checklist

**File**: Create `agent/validation_tools/ValidateSlideSet.py`

This tool automatically validates all generated slides before building PPTX.

(See AUDIT_SUMMARY.md for the complete code - save to agent/validation_tools/ValidateSlideSet.py)

---

## Fix 2: Add Automatic Retry Logic to ModifySlide

**File**: Modify `agent/slides_tools/ModifySlide.py`

Add automatic retry and fallback mechanisms to the main generation method.

(See AUDIT_SUMMARY.md for retry code and fallback HTML template)

---

## Fix 3: Create ValidateAndFixSlides Tool

**File**: Create `agent/validation_tools/ValidateAndFixSlides.py`

Auto-regenerates failed slides detected by ValidateSlideSet.

(See AUDIT_SUMMARY.md for the complete code)

---

## Fix 4: Add L1 Oracle Validator

**File**: Create `agent/validation_tools/ValidateL1Content.py`

Verifies that language-specific error content is present for each L1.

(See AUDIT_SUMMARY.md for the complete code)

---

## Fix 5: Update Agent Instructions with Validation

**File**: Modify `agent/instructions.md`

Replace the manual "Validation Checklist" section with:

```markdown
## Part 3b: Automatic Validation Pipeline

After Step 3 (populate all slides), the pipeline MUST run validation before building PPTX.

**Step 3.5: Validate All Slides (AUTOMATIC)**

1. Call `ValidateSlideSet` with:
   ```
   project_name: [your project]
   slide_count: [total slides from plan]
   l1_languages: [languages from requirements, if any]
   ```

2. Check the validation report:
   - If all "PASSED", proceed to Step 4
   - If any "FAILED", call `ValidateAndFixSlides` to retry
   - Re-run `ValidateSlideSet` until all pass

3. Call `ValidateL1Content` if L1s were specified

4. Only proceed to BuildPptxFromHtmlSlides when:
   - ✓ All slides have content (file size > 2500 bytes)
   - ✓ Every slide has speaker notes
   - ✓ L1 Oracle content exists for each language
   - ✓ CCQs present in presentation section
   - ✓ PPTX file created successfully

**Do NOT respond to the teacher until ALL validations pass.**
```

---

## Fix 6: Model Configuration

**File**: Modify `agent/config.py`

```python
"""Shared model configuration — with intelligent fallback."""
import os


def get_default_model(fallback: str = "claude-3-5-sonnet-20241022"):
    """Return the configured default model.
    
    Avoids reasoning-only models (o1, o3) which cause infinite loops in agents.
    Uses instruction-following models instead.
    """
    model = os.getenv("DEFAULT_MODEL", fallback)
    return _resolve(model)


def is_openai_provider() -> bool:
    """Check if provider is OpenAI."""
    return "/" not in os.getenv("DEFAULT_MODEL", "")


def _resolve(model: str):
    """Route 'provider/model' through LitellmModel."""
    if "/" not in model:
        return model
    bare = model[len("litellm/"):] if model.startswith("litellm/") else model
    try:
        from agency_swarm import LitellmModel
        return LitellmModel(model=bare)
    except ImportError:
        return model
```

**File**: Update `.env`

```
# CogniESL Environment Configuration

# OpenRouter API key
OPENAI_API_KEY=sk-or-v1-...

# Model selection:
# PRODUCTION: anthropic/claude-3-5-sonnet-20241022 (best for agents)
# TESTING: openrouter/google/gemma-4-26b-a4b-it:free (fast, free)
# AVOID: o1, o3, owl-alpha (reasoning-only — cause infinite loops)
DEFAULT_MODEL=anthropic/claude-3-5-sonnet-20241022

# Server port
PORT=8080
```

---

## Fix 7: Add Requirement Validation

**File**: Create `agent/validation_tools/ValidateRequirements.py`

(See AUDIT_SUMMARY.md for the complete code)

---

## Implementation Checklist

Complete these in order:

### Phase 1: Critical (1-2 days)

- [ ] Fix `.env` model selection
- [ ] Create `ValidateSlideSet.py`
- [ ] Create `ValidateAndFixSlides.py`
- [ ] Create `ValidateL1Content.py`
- [ ] Update `ModifySlide.py` with retry logic
- [ ] Update `agent/instructions.md` with validation step
- [ ] Register new tools in `cogniesl_agent.py`
- [ ] Test with simple grammar topic

### Phase 2: High Priority (2-3 days)

- [ ] Create content quality validator
- [ ] Create requirement validator
- [ ] Add audit logging
- [ ] Add file existence checks
- [ ] Update speaker notes requirements

### Phase 3: Polish (Future)

- [ ] Create generation progress page
- [ ] Add per-slide regeneration UI
- [ ] Implement feedback loop
- [ ] Performance optimization

---

## Testing Commands

```python
# Test ValidateSlideSet
ValidateSlideSet(
    project_name="test_project",
    slide_count=15,
    l1_languages=["Spanish", "Portuguese"]
).run()

# Test ValidateAndFixSlides
ValidateAndFixSlides(
    project_name="test_project",
    slide_names_to_fix=["slide_03", "slide_07"]
).run()

# Test ValidateL1Content
ValidateL1Content(
    project_name="test_project",
    l1_languages=["Spanish", "Portuguese"]
).run()
```

---

## Integration Points

**In `agent/cogniesl_agent.py`**:

```python
# Add to imports
from validation_tools import (
    ValidateSlideSet,
    ValidateAndFixSlides,
    ValidateL1Content,
    ValidateRequirements,
)

# Add to tools list in Agent()
tools=[
    # ... existing tools ...
    ValidateSlideSet,
    ValidateAndFixSlides,
    ValidateL1Content,
    ValidateRequirements,
]
```

---

## Success Metrics

After Phase 1 implementation, verify:

- [ ] No empty slides (all > 2500 bytes)
- [ ] All slides have speaker notes
- [ ] L1 Oracle sections exist for each language
- [ ] PPTX builds successfully
- [ ] Validation runs automatically
- [ ] Teachers receive complete materials

---

## Support Files

All code snippets are provided in:
- `AUDIT_SUMMARY.md` — Quick reference with full code
- `CogniESL_Audit_Report.md` — Detailed analysis of each issue
- This file — Implementation guide

---

For questions or issues during implementation, refer to the detailed issue analysis in `CogniESL_Audit_Report.md`.
