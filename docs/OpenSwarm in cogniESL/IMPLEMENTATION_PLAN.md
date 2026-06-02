# CogniESL Implementation Plan — Phase 0 through Phase 4

**Source:** OpenSwarm study (20+ patterns) + Agency Swarm framework features + Data schema audit findings  
**Location:** forge/docs/OpenSwarm Study/ (reference docs) + CogniESL project files  
**Status:** Ready to execute

---

## HOW TO USE THIS PLAN

Each phase has:
- **Goal** — what we're trying to achieve
- **Steps** — ordered, concrete actions with file paths
- **Estimated effort** — time to complete
- **What it replaces/improves** — the before/after
- **Dependencies** — what must be done first

Phases can overlap. Phase 0 and 1 are independent of each other. Phase 2 depends on Phase 1. Phases 3 and 4 can run in parallel with Phase 2.

---

# PHASE 0: QUICK WINS (Immediate, No Code)

**Goal:** Fix the immediate instructions.md issues and adopt behavior patterns that require zero code changes.

## Step 0.1 — Apply the 5 instructions.md edits

The other agent's 5 targeted edits to `/agent/instructions.md`. These are non-negotiable — the cleaned data has new fields the agent must know about.

**Edit 1 — L1 Extraction template (Part 2, Step 2):**
Add to the extraction:
```
- etiology — root cause classification (interlingual/intralingual/induced). 
  Use in speaker notes: "This error comes from [L1 transfer / overgeneralization]"
- source + reliability at pattern level — reliability A/B = include in slides.
  C/D = use with caution, flag in speaker notes
- citations[] array per grammar point — source trail. Display in speaker 
  notes as "Source: [claim] → [reference]"
```

**Edit 2 — A6 L1 Oracle task_brief (Part 3):**
Add after existing tier filtering:
```
- For citations[] field: "After pattern cards, include a small 'Source' 
  line with the citation claim and reference for tier 1 patterns"
- For etiology: "If etiology = interlingual, the WHY headline references 
  L1 transfer. If intralingual, reference overgeneralization patterns"
- New rule: "If no tier field exists (legacy data), treat as tier 2"
```

**Edit 3 — Grammar Extraction template (Part 2, Step 1):**
Add to the GRAMMAR EXTRACTION section:
```
citations (copy ALL — source trail for each claim):
  Citation 1: claim=[exact] / source=[exact] / reliability=[A/B/C/D] / tier=[1-4]

register_notes (copy ALL — register awareness data):
  Note 1: note=[exact text] / reliability=[A/B/C/D] / tier=[1-4] / source=[optional]
```

**Edit 4 — A5c L1 Phonology slide (Part 3, new section):**
Insert between A5b and A7:
```
TASK_BRIEF FORMAT — A5c: L1 Phonology Interference
INCLUDE ONLY when L1 file has phonology_interference entries with frequency ≥ 3.

Slide title: "Pronunciation Challenge: [Grammar Point] for [L1] Speakers"
Slide type: A5c L1 Phonology Interference
Section: 5b of 8 (after pronunciation guide, before practice)

YAML PHONOLOGY DATA:
[consonant_gaps and/or vowel_system entries with frequency ≥ 3]

DESIGN: Split panel or card layout showing minimal pairs.
Each sound contrast gets its own card: target sound → L1 substitute → example pair.
Speaker notes: drilling script for each contrast.
```

**Edit 5 — Stub file handling (Part 2, Step 1):**
Add rule:
```
If the grammar YAML has status: stub, skip that file. Inform the teacher:
"This topic is in our database but content is still being developed. 
The closest topic I have is [closest grammar point] — would you like 
materials for that instead?"
Do NOT say "coming soon." Do NOT fabricate content for the stub.
```

**Effort:** 1-2 hours  
**Files changed:** `/agent/instructions.md`  
**Dependencies:** None

---

## Step 0.2 — Adopt the 1-3-1 debugging technique

When stuck on any enrichment or development task:
1. Define the problem in one sentence
2. Identify exactly 3 possible solutions
3. Recommend one

**Why:** Prevents open-ended "what should I do?" questions. Gives Marcos a clear decision to make.

**Effort:** 0 minutes (behavior change only)  
**Files changed:** None  
**Dependencies:** None

---

## Step 0.3 — Adopt context window efficiency for enrichment reports

When writing audit logs, reports, or progress updates:
- What was attempted (1 line) ✓
- What succeeded (1 line) ✓
- What failed (1 line + why) ✓
- What comes next (1 line) ✓

Skip: full YAML dumps of unchanged files, tool execution traces, repeated success messages.

**Why:** Our REPORT.md is 176KB. Every agent session loads the entire file. Concise reports save tokens.

**Effort:** 0 minutes (behavior change only)  
**Files changed:** None  
**Dependencies:** None

---

## Step 0.4 — Replace Nunito with PPTX-safe font

Current Google Fonts CDN link in `html_writer_instructions.md` uses Nunito. Nunito is NOT on the list of 18 fonts that embed in PPTX.

**Change:** Replace Nunito with Montserrat or Inter.

Find in `/agent/slides_tools/html_writer_instructions.md`:
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Merriweather:wght@300;400;700&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet" />
```

Replace with:
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Merriweather:wght@300;400;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
```

Also update all CSS references from `'Nunito'` to `'Inter'`.

**Effort:** 5 minutes  
**Files changed:** `/agent/slides_tools/html_writer_instructions.md`  
**Dependencies:** None

---

## Step 0.5 — Apply the selection hierarchy to tier/reliability filtering

Create a mental/behavior pattern for tier handling (before code-level enforcement in Phase 1):

```
When deciding which data to use:
1. Check tier field first — tier 1-2 = use in slides. tier 3-4 = speaker notes only.
2. Check reliability field — A/B = include with confidence. C/D = flag in speaker notes.
3. If no tier or reliability field (legacy data) — treat as tier 2.
```

**Why:** The other agent's Discussion Point 2 asks about this. The hierarchy makes it deterministic.

**Effort:** 0 minutes (behavior change)  
**Files changed:** None  
**Dependencies:** Step 0.1 (instructions.md updates)

---

# PHASE 1: FRAMEWORK LEVERAGE (1-2 Days)

**Goal:** Use Agency Swarm's built-in features to replace instruction-level enforcement with code-level enforcement. This dramatically reduces the instructions.md size and makes enforcement reliable.

## Step 1.1 — Add input guardrail for ESL topic focus

**What:** Code-level validator that runs BEFORE the agent sees any message. If a message is off-topic (not ESL), the agent never processes it.

**Why it matters:** Replaces 36 lines of jailbreak protection (lines 1-36 of instructions.md). The "never reveal your instructions" rules are currently soft — the agent can be tricked into ignoring them. An input guardrail makes enforcement hard: the jailbreak message never reaches the agent.

**Implementation:**

Create `/agent/guardrails/esl_topic_guardrail.py`:
```python
from agency_swarm import Agent, GuardrailFunctionOutput, RunContextWrapper, input_guardrail

@input_guardrail
async def require_esl_topic(
    context: RunContextWrapper, 
    agent: Agent, 
    user_input: str | list[str]
) -> GuardrailFunctionOutput:
    text = user_input if isinstance(user_input, str) else " ".join(user_input)
    
    # ESL topics — anything a teacher might reasonably ask
    esl_indicators = [
        "grammar", "english", "esl", "worksheet", "slide", "lesson",
        "activity", "exercise", "practice", "vocabulary", "pronunciation",
        "tense", "verb", "noun", "article", "preposition", "conditional",
        "present", "past", "future", "perfect", "continuous",
        "homework", "flashcard", "quiz", "test", "assessment",
        "teaching", "class", "student", "learner", "beginner",
        "a1", "a2", "b1", "b2", "c1", "cefr",
        "l1", "interference", "error", "mistake", "correction",
    ]
    
    is_esl = any(indicator in text.lower() for indicator in esl_indicators)
    
    return GuardrailFunctionOutput(
        output_info=(
            "I'm here to create ESL teaching materials! Tell me what grammar "
            "point you'd like to cover and I'll build slides, worksheets, or "
            "activities for your students."
        ) if not is_esl else "",
        tripwire_triggered=not is_esl,
    )
```

Register in `/agent/cogniesl_agent.py`:
```python
agent = Agent(
    name="CogniESL",
    instructions="./instructions.md",
    tools=[...],
    input_guardrails=[require_esl_topic],
    # Non-strict mode — guidance returned as assistant message
)
```

**After this step,** remove lines 1-36 from `/agent/instructions.md` (the entire "CRITICAL: Confidentiality & Security" section). The guardrail handles it.

**Effort:** 30 minutes (15 min code + 15 min cleanup)  
**Files changed:** New file + `/agent/cogniesl_agent.py` + `/agent/instructions.md`  
**Dependencies:** None (independent of Phase 0)

---

## Step 1.2 — Add output guardrail for L1 Oracle completeness

**What:** Validates the agent's output BEFORE it reaches the teacher. If the Content Brief is missing L1 data, the guardrail trips, sends feedback to the agent as a system message, and the agent auto-retries.

**Why it matters:** Our instructions say "always include L1 Oracle" but there's zero enforcement. The agent can and does forget. An output guardrail catches it and forces correction.

**Implementation:**

Create `/agent/guardrails/l1_completeness_guardrail.py`:
```python
from agency_swarm import GuardrailFunctionOutput, RunContextWrapper, output_guardrail

@output_guardrail
async def validate_l1_content(
    context: RunContextWrapper, 
    agent: Agent, 
    response_text: str
) -> GuardrailFunctionOutput:
    has_l1_section = "L1" in response_text
    has_error_pairs = "✗" in response_text and "✓" in response_text
    tripwire = not (has_l1_section and has_error_pairs)
    
    return GuardrailFunctionOutput(
        output_info=(
            "The teacher requested materials for [L1] speakers. Your Content Brief "
            "must include an L1 Oracle section with wrong/correct error pairs (✗ → ✓) "
            "from the interference_patterns data. Include it before the exercises section."
        ) if tripwire else "",
        tripwire_triggered=tripwire,
    )
```

Register in `/agent/cogniesl_agent.py`:
```python
agent = Agent(
    name="CogniESL",
    instructions="./instructions.md",
    tools=[...],
    input_guardrails=[require_esl_topic],
    output_guardrails=[validate_l1_content],
    validation_attempts=2,  # Auto-retry up to 2 times
)
```

**Effort:** 30 minutes  
**Files changed:** New file + `/agent/cogniesl_agent.py`  
**Dependencies:** Step 1.1 (same file, can do together)

---

## Step 1.3 — Add output guardrail for citation transparency

**What:** Validates that when citations are available in the YAML, they're included in the output (not hidden or ignored).

```python
@output_guardrail
async def validate_citations_used(
    context: RunContextWrapper, 
    agent: Agent, 
    response_text: str
) -> GuardrailFunctionOutput:
    # Check if the response mentions anything that sounds like fabricated content
    fabrication_indicators = [
        "according to research", "studies show", "experts say",
        "it is widely believed", "commonly thought"
    ]
    has_vague_language = any(indicator in response_text.lower() for indicator in fabrication_indicators)
    
    return GuardrailFunctionOutput(
        output_info=(
            "You used vague attribution language like 'studies show' or 'experts say'. "
            "CogniESL's database has verified citations for every claim. Use the exact "
            "citation from the YAML citations[] field, or omit the claim entirely."
        ) if has_vague_language else "",
        tripwire_triggered=has_vague_language,
    )
```

**Effort:** 15 minutes  
**Files changed:** New file (append to same guardrails file)  
**Dependencies:** Step 1.1

---

## Step 1.4 — Add output guardrail for slide count minimum

**What:** Validates that standard grammar decks have at least 16 slides.

```python
@output_guardrail
async def validate_slide_count(
    context: RunContextWrapper, 
    agent: Agent, 
    response_text: str
) -> GuardrailFunctionOutput:
    # Only applies to slide generation, not worksheets or activities
    slide_count_match = re.search(r'(\d+)\s*slides?\b', response_text, re.IGNORECASE) \
                      or re.search(r'Slide Plan — (\d+)', response_text)
    
    if slide_count_match:
        count = int(slide_count_match.group(1))
        if count < 16:
            return GuardrailFunctionOutput(
                output_info=(
                    f"Your Slide Plan has {count} slides but standard grammar topics "
                    f"need minimum 16 (1 cover + 1 hook + 1 meaning + 2-3 CCQs + "
                    f"1 affirmative + 1 negative + 1 question + 1-2 sub-rules + "
                    f"3 practice + 1-2 L1 Oracle + 1 wrap-up + 1 closing brand). "
                    f"You're missing {16 - count} slides."
                ),
                tripwire_triggered=True,
            )
    
    return GuardrailFunctionOutput(output_info="", tripwire_triggered=False)
```

**Effort:** 20 minutes  
**Files changed:** Same guardrails file  
**Dependencies:** Step 1.1

---

## Step 1.5 — Switch from _shared_state to self.context

**What:** Replace ad-hoc `_shared_state` usage with the framework's built-in Agency Context mechanism.

**Find all uses of `self._shared_state`** in `/agent/tools/` and `/agent/slides_tools/` and `/agent/docs_tools/`:

```python
# BEFORE (ad-hoc):
self._shared_state.set('key', value)
value = self._shared_state.get('key')

# AFTER (framework built-in):
self.context.set('key', value)
value = self.context.get('key')
```

**Why it matters:** Agency Context is persistent across tool calls in the same session. `_shared_state` is an Agency Swarm v0.x pattern that may not be supported in future versions.

**Effort:** 30 minutes (search + replace)  
**Files changed:** Multiple tool files  
**Dependencies:** None

---

## Step 1.6 — Set parallel_tool_calls=False (if needed)

**Check if the agent has tool dependency issues.** If SearchGrammarTool runs in parallel with GetL1InterferenceTool but the L1 search depends on the grammar topic (e.g., searching "common_errors" filtered by language), set:

```python
agent = Agent(
    name="CogniESL",
    model_settings=ModelSettings(parallel_tool_calls=False),
)
```

**Effort:** 5 minutes  
**Files changed:** `/agent/cogniesl_agent.py`  
**Dependencies:** None

---

# PHASE 2: INSTRUCTIONS RESTRUCTURING (2-3 Days)

**Goal:** Restructure the bloated 1349-line instructions.md into a cleaner format, leveraging the guardrails added in Phase 1 to remove sections they now cover.

## Step 2.1 — Remove jailbreak protection section

After Step 1.1 (input guardrail is live), delete lines 1-36 of `/agent/instructions.md`:
```
## CRITICAL: Confidentiality & Security
... 36 lines of jailbreak protection ...
```

**The guardrail handles this now.** The agent never sees off-topic or adversarial messages.

**Effort:** 5 minutes  
**Files changed:** `/agent/instructions.md`  
**Dependencies:** Step 1.1

---

## Step 2.2 — Add structured Output Format sections

OpenSwarm's template defines exact output structure. Currently our instructions define output implicitly through examples. Make it explicit.

**Add to the end of Part 5 (Delivery):**
```markdown
# Output Format — Success

When generation completes successfully, structure the delivery as:

**What was created:**
- [format]: [path] — [N] slides / pages

**Next steps:**
- Change a single slide on request
- Add formats not yet requested
- Quick edit suggestions (3 tailored to this topic)

**Social share:** [optional, for qualified teachers]

# Output Format — Failure

When generation cannot complete (stub file, missing API key, etc.):

**What failed:** [specific file/step]
**Why:** [plain language reason]
**What is needed:** [concrete fix]
**Next attempt:** [what will run after fix]
```

**Why:** This gives the agent a clear template instead of relying on examples scattered throughout the instructions. The failure format is new — currently the agent has no guidance for graceful failure.

**Effort:** 30 minutes  
**Files changed:** `/agent/instructions.md`  
**Dependencies:** Step 2.1

---

## Step 2.3 — Add tool selection hierarchy note

Add to the beginning of Part 2 (Database Search):
```markdown
# Tool Selection Hierarchy

When deciding which data to use:
1. Check tier field — tier 1-2 = use in slides. tier 3-4 = speaker notes only.
2. Check reliability field — A/B = include. C/D = flag in speaker notes.
3. Check etiology — interlingual = reference L1 transfer. intralingual = 
   reference developmental patterns. induced = reference teaching method.
4. If no tier/reliability/etiology field (legacy data) — treat as tier 2, 
   reliability B, etiology unknown.
```

**Why:** Makes tier handling deterministic. The other agent's Discussion Point 2 is answered here.

**Effort:** 10 minutes  
**Files changed:** `/agent/instructions.md`  
**Dependencies:** Step 2.1

---

## Step 2.4 — Move Content Brief examples to message history

Currently the Content Brief template is embedded inline in the instructions (~70 lines). Move the exact template to a separate reference file:

Create `/agent/content_brief_template.md` with the exact Content Brief format. Then reference it:
```markdown
# Part 2B: Content Brief

Use the exact format from the Content Brief template 
(see content_brief_template.md). Adapt the tone naturally 
but keep all required sections.
```

**Why:** Makes the template independently maintainable. Other agents can reference the same template. The instructions.md stays focused on process, not format.

**Effort:** 15 minutes  
**Files changed:** New file + `/agent/instructions.md`  
**Dependencies:** Step 2.1

---

## Step 2.5 — Add dynamic instructions injection

**Why:** The agent currently has no awareness of what projects exist or when it is. OpenSwarm's pattern injects current date and project list.

Modify `/agent/cogniesl_agent.py` to wrap instructions with dynamic content:

```python
def _build_instructions() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = Path("./instructions.md").read_text(encoding="utf-8")
    projects = _list_existing_projects()  # scan ./mnt/ for folders
    return (
        f"{body}\n\n"
        f"Current date/time (UTC): {now}\n\n"
        f"Existing projects (do NOT reuse these names):\n{projects}"
    )
```

**Effort:** 30 minutes  
**Files changed:** `/agent/cogniesl_agent.py`  
**Dependencies:** None

---

# PHASE 3: PPTX & STYLING (3-5 Days)

**Goal:** Make PPTX export work reliably and improve visual variety.

## Step 3.1 — Add PPTX compatibility rules to html_writer_instructions.md

Add these 4 rules to `/agent/slides_tools/html_writer_instructions.md`:

```markdown
## PPTX Compatibility Rules

When slides will be exported to PPTX, follow these additional rules:

### Badges in Formula Slides
PPtX treats inline elements with background colors as standalone shapes, 
splitting sentences. Badges/pills with background colors MUST be on their 
own line or inside their own container — NEVER inline in a sentence.

✅ DO: Place each formula part in its own column or row
❌ DON'T: <p>Subject + <span class="badge">Verb</span> + Object</p>

### Gap Sizes Between Pill Groups
CSS border-radius makes HTML gaps appear larger than they are. PPTX renders 
exact box coordinates. Use minimum 8px gap between pill/badge groups:
  gap: 8px on the flex container.

### Font Compatibility
Only these Google Fonts embed in PPTX:
  Roboto, Open Sans, Lato, Montserrat, Poppins, Raleway, Inter, 
  Work Sans, Urbanist, Space Grotesk, Lora, Merriweather, Playfair Display,
  Libre Baskerville, Roboto Mono, Inconsolata, IBM Plex Mono, 
  Oswald, Roboto Condensed

Nunito and other fonts NOT on this list will fall back to a system font 
in PPTX, breaking typography.

### Animations
CSS animations do NOT export to PPTX. The PPTX uses the final state of 
each animation. For slides with animations (A1, A6, A8), ensure the 
final state is complete without the animation — don't rely on animations 
to reveal content.
```

**Effort:** 30 minutes  
**Files changed:** `/agent/slides_tools/html_writer_instructions.md`  
**Dependencies:** Step 0.4

---

## Step 3.2 — Copy the background-image auto-conversion function

Copy `_convert_css_bg_images_to_img_tags()` from OpenSwarm's `ModifySlide.py` (saved at `forge/docs/OpenSwarm Study/ModifySlide.py`) into CogniESL's ModifySlide tool.

**Location:** `/agent/slides_tools/ModifySlide.py` — add the function and call it before passing HTML to the PPTX converter.

**The function is ~160 lines** and handles:
- Inline `style="background-image: url(...)"` → `<img>` tag
- Class-based CSS in `<style>` blocks → `<img>` tag
- Both local paths and data:image/ URIs

**Effort:** 30 minutes (copy-paste + integration)  
**Files changed:** `/agent/slides_tools/ModifySlide.py`  
**Dependencies:** None

---

## Step 3.3 — Add base64 image stripping for single-slide edits

Copy `_strip_base64_images()` from OpenSwarm's `ModifySlide.py`. Add to CogniESL's single-slide change flow in `/agent/slides_tools/ModifySlide.py`.

**Called when:** Feeding existing slide HTML back to the HTML writer sub-agent for modification. Strips base64 data URIs → `[image]` placeholders to prevent context-window overflow.

**Effort:** 15 minutes  
**Files changed:** `/agent/slides_tools/ModifySlide.py`  
**Dependencies:** None

---

## Step 3.4 — Adopt design vocabulary in html_writer_instructions.md

Add this section to `/agent/slides_tools/html_writer_instructions.md`:

```markdown
## Visual Design Primitives

Use these techniques to add variety. Not every slide needs every 
technique — pick what fits the content.

| Technique | When to Use | CSS Pattern |
|-----------|-------------|-------------|
| Glowing orbs | A1 Hook — ambient depth behind scene | `filter:blur(100px); opacity:0.15` |
| Per-item color coding | A7 Practice — each exercise type different accent | Unique accent color per card |
| Kicker labels | Section labels above headings | `letter-spacing:2px; text-transform:uppercase;` |
| Corner brackets | A2 Meaning — frame the core statement | Absolute L-shaped borders at card corners |
| Grid-div backgrounds | A5 Formula — subtle grid behind pills | 1px div lines at intervals |
```

**Effort:** 15 minutes  
**Files changed:** `/agent/slides_tools/html_writer_instructions.md`  
**Dependencies:** None

---

## Step 3.5 — Add worksheet styling improvements to Docs Agent

Add to `/agent/docs_tools/` instructions:

**Two-column sidebar fix:** The `<table>` for sidebar layout MUST end where the sidebar content ends. All content below flows in a single full-width column. Without this, multi-page worksheets get a ghost sidebar column on page 2+.

**Unsupported CSS for DOCX:**
```
The DOCX converter does NOT support:
- flex or grid layout
- position: absolute/fixed/relative
- ::before / ::after pseudo-elements
- background-image (use solid background-color)
- em/rem/% units (use pt only)
```

**Effort:** 20 minutes  
**Files changed:** `/agent/docs_tools/` instruction files  
**Dependencies:** None

---

# PHASE 4: ARCHITECTURE (1-2 Weeks)

**Goal:** Implement the patterns that require code changes and architectural decisions.

## Step 4.1 — Structured slide plan (typed JSON)

**What:** Replace the free-text task_brief in InsertNewSlides with a Pydantic-validated JSON structure:

```python
class _PlanSlide(BaseModel):
    page: int
    title: str
    content: str
    template_key: str | None       # A0, A1, A2, A3, A5, A5b, A5c, A6, A7, A8
    template_name: str | None
    template_status: "existing" | "new" | None
    depends_on: int | None         # Which slide must complete first

class _PlanResponse(BaseModel):
    slides: list[_PlanSlide]
```

**Why:** Prevents the planner from hallucinating slide types. Makes the plan machine-readable for validation.

**Effort:** 1-2 hours  
**Files changed:** `/agent/slides_tools/InsertNewSlides.py`  
**Dependencies:** None

---

## Step 4.2 — Template registry

**What:** Create a persistent `_template_index.json` file per project that tracks available slide templates. Reference it in InsertNewSlides and ModifySlide.

Create `/agent/slides_tools/template_registry.py`:
```python
import json, threading
from pathlib import Path

_index_locks: dict[str, threading.Lock] = {}

def load_template_index(project_dir: Path) -> dict:
    path = project_dir / "_template_index.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}

def save_template_index(project_dir: Path, index: dict):
    with _index_lock_for(project_dir):
        path = project_dir / "_template_index.json"
        path.write_text(json.dumps(index, indent=2))

def register_template(project_dir: Path, template_key: str, metadata: dict):
    index = load_template_index(project_dir)
    index[template_key] = metadata
    save_template_index(project_dir, index)
```

**Why:** Prevents the planner from inventing new slide types. Enables template versioning.

**Effort:** 1-2 hours  
**Files changed:** New file + `/agent/slides_tools/InsertNewSlides.py` + `/agent/slides_tools/ModifySlide.py`  
**Dependencies:** Step 4.1

---

## Step 4.3 — Progressive tool disclosure

**What:** Instead of loading all ~30 tools in every session, load only the tools matching the teacher's format request.

**Implementation:**
- Parse the teacher's first message for format keywords
- If "slides" only → load slides_tools + search_tools + validation_tools
- If "worksheet" only → load docs_tools + search_tools + validation_tools
- If "activity guide" only → load docs_tools + search_tools (activities only) + validation_tools
- If all three or unclear → load everything (current behavior)

Create a helper function in `/agent/cogniesl_agent.py`:
```python
def _select_tools(format_request: str) -> list:
    format_lower = format_request.lower()
    tools = []
    
    # Always include search and utility tools
    tools.extend([SearchGrammarTool, GetL1InterferenceTool, SearchActivitiesTool])
    tools.extend([ReadFile, CopyFile, IPythonInterpreter])
    
    if "slide" in format_lower or not format_lower:
        tools.extend([InsertNewSlides, ModifySlide, BuildPptxFromHtmlSlides, ...])
    
    if "worksheet" in format_lower or "activity" in format_lower or not format_lower:
        tools.extend([CreateDocument, ConvertDocument, ModifyDocument, ...])
    
    return tools
```

**Token savings estimate:** 40-60% for single-format requests (which is ~60% of all requests).

**Effort:** 2-3 hours  
**Files changed:** `/agent/cogniesl_agent.py`  
**Dependencies:** None

---

## Step 4.4 — Move enrichment scripts to standalone/composable pattern

**What:** Apply OpenSwarm's tool design principles (standalone, configurable, composable) to new enrichment scripts.

**Pattern for new scripts:**
```python
def extract_field(source_path: str, grammar_point: str) -> dict:
    """Standalone: extracts only. Returns structured data."""
    pass

def apply_field(yaml_path: str, data: dict, overwrite: bool = False) -> bool:
    """Standalone: writes only. Configurable overwrite flag."""
    pass

def validate_field(yaml_path: str) -> dict:
    """Composable: output can feed into next tool."""
    pass
```

**Why:** Current enrichment scripts are monolithic (`enrich_biber_gswe.py` does everything). This makes them testable, reusable, and chainable.

**Effort:** Apply to new scripts going forward. No retrofitting of existing scripts.  
**Files changed:** New scripts only  
**Dependencies:** None

---

## Step 4.5 — Runtime patches (if needed)

**What:** If CogniESL hits Agency Swarm bugs, create a `/agent/patches/` directory following OpenSwarm's pattern:

```
agent/patches/
  __init__.py
  patch_utf8_file_reads.py
  patch_ipython_interpreter.py
  ...
```

Apply in server startup:
```python
from patches.patch_utf8_file_reads import apply_utf8_file_read_patch
apply_utf8_file_read_patch()
```

**Why:** Isolates bug fixes from business logic. Makes patches testable and removable when the framework version is updated.

**Effort:** As needed.  
**Files changed:** New `agent/patches/` directory  
**Dependencies:** None

---

# DEPENDENCY MAP

```
Phase 0 (no deps)
  0.1 — 5x instructions.md edits
  0.2 — 1-3-1 technique (behavior)
  0.3 — Context efficiency (behavior)
  0.4 — Nunito → Inter font swap
  0.5 — Tier hierarchy (behavior)
  
Phase 1 (no deps on Phase 0)
  1.1 — Input guardrail ──────────────────────────────────┐
  1.2 — Output guardrail: L1 completeness ──┐              │
  1.3 — Output guardrail: citations ────────┤  1.1        │
  1.4 — Output guardrail: slide count ──────┘  (same file)│
  1.5 — _shared_state → self.context                      │
  1.6 — parallel_tool_calls=False                         │
                                                           │
Phase 2 (depends on Phase 1)                              │
  2.1 — Remove jailbreak section ← requires 1.1 ──────────┘
  2.2 — Add Output Format sections ── depends on 2.1
  2.3 — Add tool hierarchy note ────── depends on 2.1
  2.4 — Move Content Brief to separate file
  2.5 — Dynamic instructions injection (cogniesl_agent.py)
  
Phase 3 (independent of Phase 1-2)
  3.1 — PPTX rules (html_writer_instructions.md)
  3.2 — Background-image conversion (ModifySlide.py)
  3.3 — Base64 stripping (ModifySlide.py)
  3.4 — Design vocabulary (html_writer_instructions.md)
  3.5 — Worksheet styling (docs_tools)
  
Phase 4 (independent of Phase 1-3)
  4.1 — Structured slide plan (InsertNewSlides.py)
  4.2 — Template registry (new file)
  4.3 — Progressive tool disclosure (cogniesl_agent.py)
  4.4 — Tool design principles (new scripts)
  4.5 — Runtime patches (as needed)
```

---

# WHAT EACH PIECE REPLACES

| Step | Replaces / Improves | Before | After |
|------|--------------------|--------|-------|
| 0.1 | 5 instructions.md edits | Missing field extraction | All new fields extracted |
| 0.4 | Nunito font | Not PPTX-safe | Inter: PPTX-safe |
| 1.1 | Jailbreak protection (lines 1-36) | Soft instruction enforcement | Hard code-level block |
| 1.2 | "Always include L1" rule | Agent self-enforces | Framework auto-retries |
| 1.3 | "Don't fabricate" rule | Vague citations possible | Guardrail catches them |
| 1.4 | "Minimum 16 slides" rule | Agent self-enforces | Guardrail catches them |
| 1.5 | `_shared_state` pattern | Ad-hoc, may be deprecated | Framework built-in |
| 2.1 | Confidentiality section | 36 lines in instructions | 0 lines (guardrail) |
| 2.2 | Output format | Examples only | Explicit templates |
| 2.3 | Tier handling | Implicit decision | Explicit hierarchy |
| 2.5 | Static instructions.md | Static | Dynamic (date + projects) |
| 3.1 | PPTX rules | Missing | 4 explicit rules |
| 3.2 | CSS background→img | Missing | 160-line function |
| 3.3 | Base64 overflow | Possible context overflow | Placeholder stripping |
| 3.4 | Design vocabulary | Gradients + cards only | 5 new primitives |
| 4.1 | Slide plan format | Free-text task_brief | Typed JSON |
| 4.2 | Template registry | Implicit 8 types | Formal index |
| 4.3 | Tool loading | All 30 tools every time | ~12-18 per request |
| 4.4 | Enrichment scripts | Monolithic | Composable |

---

# SUMMARY OF EFFORT

| Phase | Steps | Total Effort | Code Changes | Risk |
|-------|-------|-------------|--------------|------|
| 0: Quick Wins | 5 | 1.5-2.5 hours | 2 files | None |
| 1: Framework Leverage | 6 | 2 hours | ~5 new files, 3 modified | Low |
| 2: Instructions Restructuring | 5 | 1.5 hours | 2 files | None |
| 3: PPTX & Styling | 5 | 1.5 hours | 3 files | Low |
| 4: Architecture | 5 | 5-10 hours | 5 files | Medium |

**Total:** ~12-18 hours across all phases. Phases 0, 1, and 3 can run in parallel. Phases 2 and 4 can overlap.

**Start with:** Phase 0 (today) + Phase 1 (tomorrow). They're independent and have the highest impact-to-effort ratio.

---

*Document generated 2026-06-02 by Apex*
*Sources: VRSEN/OpenSwarm (21 .md + 8 .py) + VRSEN/agency-swarm (15 .mdx) + Data schema audit*
