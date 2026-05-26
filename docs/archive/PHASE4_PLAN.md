# Phase 4: Content Brief, Post-Delivery UX & Single-Slide Edits
**Status:** Planning complete — not yet implemented  
**Last updated:** 2026-05-22

---

## Overview

Phase 4 has four interconnected components that together create a complete, professional teacher experience:

| Component | What it does | Where the change lives |
|---|---|---|
| 4A — Content Brief Preview | Teacher approves content before generation | `agent/instructions.md` |
| 4B — Post-generation message | Explains what was delivered + edit capability | `agent/instructions.md` |
| 4C — Single-slide change flow | Teacher requests targeted edits after delivery | `agent/instructions.md` |
| 4D — Project memory | Agent remembers which project belongs to this teacher | `agent/instructions.md` |

---

## 4A — Content Brief Preview

### What it does
After collecting all required info and searching the database, the agent shows a structured preview of the exact content that will go into the slides. The teacher reviews and approves (or requests changes) **before any generation starts**. This is the primary quality gate.

### Trigger condition
After Step 3 (Search Activities) is complete and all required fields are confirmed:
- Grammar point ✓
- L1 language(s) ✓
- Age group ✓
- Level ✓
- Format(s) requested ✓
- Activity type (if requested) ✓

### Exact format of the brief

```
**Content Brief — [Grammar Point] | [L1 Language(s)] | [Age Group] | [Level]**

📖 **What this grammar means:**
[core_meaning from YAML — one sentence, verbatim]

🔍 **Concept Check Questions** *(shown to students BEFORE the formula)*
1. Q: [exact CCQ 1 from YAML] → A: [exact answer 1]
2. Q: [exact CCQ 2 from YAML] → A: [exact answer 2]

📐 **Formula**
[exact structure from YAML, e.g. "Subject + had + past participle + would have + past participle"]

🌍 **L1 Oracle — [Language 1]:**
✗ "[example_wrong from YAML]" → ✓ "[example_correct from YAML]"
*Why:* [why_it_happens from YAML — one sentence]

🌍 **L1 Oracle — [Language 2 if applicable]:**
✗ "[example_wrong]" → ✓ "[example_correct]"
*Why:* [why_it_happens]

🎮 **Activity** *(if requested)*
[activity name] ([duration] min) — [one-line description from YAML]

📦 **Delivering:** [list of formats: slides / worksheet / activity guide]

---
Does this look right? Reply **'looks good'** to generate, or tell me what to change.
```

### Handling teacher feedback on the brief

**"Looks good" / "yes" / "go ahead"** → proceed to generation immediately  
**"Change the CCQ"** → update that field, show the updated brief again, wait for re-approval  
**"Use a different activity"** → search activities again with new criteria, update brief, re-show  
**"Actually add a worksheet too"** → update the format list, confirm, proceed  
**"Change the L1 to French"** → re-search L1 interference file, update L1 Oracle section, re-show  
**"Change the grammar point to X"** → start fresh from the grammar search, produce a new brief  

**Rule:** Never start generation after a change request without showing the updated brief and getting explicit approval. The brief must always be the last thing the teacher sees before generation begins.

### Edge cases to handle

- **Teacher changes the grammar point** after seeing the brief → full re-search, new brief
- **Teacher says "close enough" or "it's fine"** → treat as "looks good"
- **Teacher asks "what if I add Chinese too?"** → add L1, fetch interference patterns, update L1 Oracle section, show updated brief
- **Teacher asks to skip the brief** ("just generate it") → still show the brief but make it shorter; never skip entirely (brief is the quality gate)
- **Brief is too long** → if more than 2 L1 languages, collapse each L1 Oracle to one line in the brief, but still generate full content

---

## 4B — Post-generation Message

### What it does
After PPTX is built and delivered, the agent sends a closing message that:
1. Confirms what was delivered
2. Mentions single-slide edit capability
3. Upsells formats not yet requested (consistent with current upsell rule)

### Exact format

```
Done! Here's what I created for [Grammar Point] — [L1(s)] — [Age Group]:

[List of delivered files with download links]

A few things to know:
- **Need to change something?** Just tell me which slide and what to change — I'll update that one slide in about a minute without touching the rest.
- **Want to add more?** [Only mention formats NOT already delivered: e.g. "I can also add a worksheet or activity guide anytime."]

Your materials are saved and I can update them anytime in this conversation.
```

### Rules
- Only mention formats the teacher did NOT request (consistent with current upsell logic)
- If teacher requested all formats, skip the upsell line entirely
- Keep it brief — two or three lines max after the file list
- Always include the "need to change something" line — this is not optional

---

## 4C — Single-Slide Change Flow

### Recognition triggers
The agent should recognize a single-slide change request when the teacher says things like:
- "Change slide 6 to use travel instead of medicine"
- "The clause order slide has an error"  
- "Can you make the L1 Oracle slide more visual?"
- "Slide 8 is too text-heavy"
- "Update the formula to show the negative form too"
- "Remove the activity from slide 12"

### How the agent identifies the target slide
The agent knows the `project_name` from the conversation (see 4D). It can identify slides by:
- **Slide number** (explicit: "slide 6") → directly target `slide_06`
- **Section/topic name** ("the clause order slide", "the CCQ slide") → match against the slide plan stored in memory or inferred from project context
- **Content description** ("the one with the speech bubble", "where the formula is") → scan slide filenames or ask "do you mean slide 8 — Clause Order Flexibility?"

**When ambiguous:** Ask once: *"Just to confirm — are you referring to slide 8 (Clause Order Flexibility)?"*

### The exact tool sequence for a single-slide change

1. `ModifySlide` — project_name + target slide + new task_brief describing the change  
   - The task_brief must include: what to keep (other content on the slide), what to change, and relevant YAML excerpts if content is being added
2. `ValidateSlideSet` — validate just the changed slide (or all slides if uncertain)
3. `BuildPptxFromHtmlSlides` — rebuild the full PPTX from all slides (14 old + 1 new)
4. Deliver the new PPTX with a message like: *"Done — updated slide 8. Here's your new PPTX. The other 14 slides are unchanged."*

### Rules for single-slide changes
- **Never regenerate the whole deck** for a single-slide change
- **Always rebuild the PPTX** after a slide change — don't tell the teacher to use the old file
- **Preserve the project_name** — all changes go to the same project folder
- **If the change touches grammar content** (different formula, different CCQ) → fetch the relevant YAML first, use exact content from database — never invent grammar content
- **If the change is stylistic** (color, layout, visual style) → no database lookup needed
- **Multiple slide changes in one request** ("change slides 6 and 8") → run `ModifySlide` for each sequentially, then rebuild PPTX once at the end

### What NOT to do
- Do not ask the teacher to "regenerate everything" for a small change
- Do not say the change is impossible because it would affect other slides
- Do not run the full generation pipeline (InsertNewSlides) for a single-slide edit

---

## 4D — Project Memory

### What the agent needs to remember after generation
After any generation completes, the agent must store in conversation context:
- `project_name` — the folder name (e.g. `third_conditional_teen_chinese_japanese`)
- `slide_count` — how many slides were generated
- `grammar_point` — what grammar was taught
- `l1_languages` — which L1s were included
- `slide_plan` — a brief mapping of slide number → section name (e.g. "slide_08 = Clause Order Flexibility") so it can identify slides by topic

**How to store it:** At the end of generation, the agent writes a one-line summary to its internal context: *"Project: third_conditional_teen_chinese_japanese | 15 slides | Third Conditional | Chinese + Japanese | Slide plan: 01=Hook, 02=CCQ1, 03=CCQ2..."*

### Returning user — same session
If the teacher returns to the same chat session, `project_name` is still in context. The agent can immediately handle change requests without asking.

### Returning user — new session
The teacher opens a new conversation. Two options:

**Option 1 (MVP):** Agent asks: *"Are you continuing work on a previous set of materials? If so, what was the topic and language combination?"* Teacher says "third conditional for Chinese students" → agent reconstructs `project_name`, confirms ("I found your third_conditional_teen_chinese_japanese project — 15 slides, is that the one?"), proceeds.

**Option 2 (future UI):** A "Your Materials" panel in the CogniESL UI shows all past projects with thumbnails. Teacher clicks a project → chat pre-loads with the project context. This requires the UI to expose the `mnt/` folder contents. Plan this for Phase 5 or later.

### Fallback if project can't be found
If the teacher references a change but the project_name can't be determined: *"I want to make sure I update the right file — can you remind me what the topic and language combination was? For example, 'third conditional for Chinese teens.'"*

---

## Implementation Order (when Phase 4 starts)

1. **4A — Content Brief** (~45 min)
   - Add the brief template to `agent/instructions.md` after Step 3 / before Part 3
   - Add change-handling rules
   - Test with Maria persona (gives everything upfront — she should see the brief before generation)
   - Test with a persona who requests a change in the brief

2. **4D — Project Memory** (~20 min)
   - Add post-generation memory instruction to `agent/instructions.md`
   - Test: verify agent stores project_name and slide plan after generation
   - Test: verify agent can handle single-slide change request immediately after delivery

3. **4C — Single-slide change flow** (~30 min)
   - Add recognition triggers and tool sequence to `agent/instructions.md`
   - Test: generate a deck, then request a change to slide 5, verify only slide 5 changes
   - Verify PPTX is rebuilt and delivered correctly

4. **4B — Post-generation message** (~15 min)
   - Add post-generation message template to `agent/instructions.md`
   - Verify it mentions single-slide edits
   - Verify upsell logic only mentions formats not already delivered

5. **End-to-end test** (~30 min)
   - Full flow: chat interview → Content Brief → approval → generation → delivery → single-slide change → updated PPTX
   - Use a teacher persona who (a) approves the brief, (b) changes one thing in the brief, and (c) requests a slide edit after delivery

---

## Success Criteria for Phase 4

- [ ] Content Brief appears before every generation — no exceptions
- [ ] Brief shows exact YAML content (CCQs, formula, L1 Oracle) not paraphrased
- [ ] Teacher can request changes to the brief and see an updated version
- [ ] Generation only starts after explicit "looks good" approval
- [ ] Post-generation message always mentions single-slide edit capability
- [ ] Single-slide change completes in under 2 minutes (1 slide × 20s delay + PPTX rebuild)
- [ ] PPTX after single-slide change has all other slides unchanged
- [ ] Agent remembers project_name and can handle follow-up changes in the same session
- [ ] New session reconnect works (teacher gives topic, agent finds project)

---

## Open Questions (to decide before implementing)

1. **Should the Content Brief show the full slide plan** (all 15 slide titles)? Or just the key content points? Showing all 15 might overwhelm teachers, but it lets them catch structural issues early.

2. **Should single-slide changes also update the worksheet** (if one was generated)? If a teacher changes an example in slide 6, the worksheet might have the same example. This adds complexity — skip for MVP, add later.

3. **Project naming** — currently project folders are named automatically by the orchestrator (e.g. `third_conditional_teen_chinese_japanese`). Should teachers be able to name their own projects? ("Save this as 'Class 3B - May 2026'"). This would make reconnecting easier.

4. **Version history** — if a teacher changes slide 6, should the old version be kept as a backup? Currently `BuildPptxFromHtmlSlides` auto-versions (`deck_v2.pptx`, `deck_v3.pptx`). The HTML source files are overwritten. Is this okay?
