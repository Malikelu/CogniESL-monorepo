# Decoupled PPTX Generator — Spec

**Status:** Planned (not yet built)  
**Related:** [HTML_FIRST_STRATEGY.md](HTML_FIRST_STRATEGY.md)  
**Replaces:** `BuildPptxFromHtmlSlides` (HTML-to-PPTX conversion)

---

## The Problem with the Current Approach

`BuildPptxFromHtmlSlides` converts HTML slides to PPTX by screenshotting each slide (via Playwright) and embedding the screenshots as images in PowerPoint slides. This produces a PPTX where:

- All content is a flat bitmap — no editable text, no real shapes
- File is large (screenshots at full resolution)
- Teacher can't edit anything in PowerPoint
- Animations are lost (static screenshot of the initial state)
- The HTML design had to be constrained to look acceptable when screenshotted

This approach exists because it was the fastest path to a working PPTX. It was never the right long-term solution.

---

## The Right Approach: Generate From Structured Content

`BuildSimplePptx` will generate PPTX directly from the structured content data the agent already has — the same grammar YAML data, L1 patterns, and slide content that was used to build the HTML slides. It will not attempt to mirror the HTML design.

The PPTX will look like what a skilled teacher built in PowerPoint: clean, professional, fully editable. The HTML will look like what a design agency built. Both are excellent, for different purposes.

---

## What BuildSimplePptx Produces

A clean PPTX with:
- **Editable text** — all content as real PowerPoint text objects
- **CogniESL brand colors** — teal (#0b7272) and green (#1baa6e) as theme colors
- **Consistent layout per slide type** — one template per section type (hook, CCQ, formula, L1 Oracle, practice, wrap-up)
- **No animations** (PowerPoint animations are a different product)
- **Speaker notes** — same data-speaker-notes content as the HTML slides

It will NOT attempt to replicate CSS gradients, custom fonts, or complex layouts. It trades visual richness for editability and compatibility.

---

## Input: Structured Slide Content

The agent passes a JSON array of slide descriptors — one per slide — containing the content that was used to build each HTML slide:

```python
BuildSimplePptx(
  project_name = "present_perfect_french_adults",
  grammar_point = "Present Perfect",
  slides_json = json.dumps([
    {
      "type": "LESSON_PLAN_COVER",
      "title": "Present Perfect — French Speakers — Adults",
      "objectives": ["..."],
      "stage_plan": [{"stage": "Hook", "slides": "2", "minutes": 5}, ...],
      "ccqs": ["Have you ever eaten sushi?", ...],
      "l1_errors": ["*I have seen him yesterday → I saw him yesterday", ...]
    },
    {
      "type": "HOOK",
      "title": "Have you ever...?",
      "visual_concept": "Travel experiences — passport stamps",
      "hook_question": "Have you ever been to Japan?",
      "speaker_notes": "..."
    },
    {
      "type": "CCQ",
      "question": "Did we say WHEN it happened?",
      "answer": "No — we're talking about experience, not the specific time.",
      "speaker_notes": "..."
    },
    {
      "type": "FORMULA",
      "affirmative": "Subject + have/has + past participle",
      "negative": "Subject + haven't/hasn't + past participle",
      "question": "Have/Has + subject + past participle?",
      "examples": ["I have visited Paris.", "She hasn't eaten yet."],
      "speaker_notes": "..."
    },
    {
      "type": "L1_ORACLE",
      "l1_language": "French",
      "error": "*I am here since 3 hours.",
      "correction": "I have been here for 3 hours.",
      "why": "French uses present tense (je suis) for ongoing states; English uses present perfect.",
      "speaker_notes": "..."
    },
    ...
  ])
)
```

---

## Slide Layout Templates (per type)

Each slide type has a fixed, clean PPTX layout:

| Type | Layout |
|------|--------|
| LESSON_PLAN_COVER | Title + 4-column table (stage plan) + CCQ list |
| HOOK | Large title + subtitle + background color block |
| MEANING | Title + 2-column layout (concept left, example right) |
| CCQ | Large question text centered + answer below |
| FORMULA | Title + 3 formula boxes (affirmative / negative / question) |
| PRONUNCIATION | Title + IPA text blocks |
| L1_ORACLE | Red error text → green correction text + explanation |
| PRACTICE | Title + exercise list |
| WRAP_UP | Title + key takeaways list |
| CLOSING_BRAND | CogniESL logo centered + tagline |

All layouts use:
- **Nunito font** (embedded in PPTX via python-pptx font embedding, or fallback to Calibri)
- **Teal (#0b7272)** for headings and accents
- **Green (#1baa6e)** for corrections and positive highlights
- **Red (#dc2626)** for errors and negative examples
- **White background** — clean and printable

---

## Implementation Notes

**Library:** `python-pptx` — already a dependency (used by `BuildPptxFromHtmlSlides`)

**Key python-pptx patterns needed:**
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.33)   # 16:9 widescreen
prs.slide_height = Inches(7.5)

slide_layout = prs.slide_layouts[6]  # Blank layout
slide = prs.slides.add_slide(slide_layout)

# Add text box
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1.5))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Have you ever...?"
p.font.size = Pt(40)
p.font.color.rgb = RGBColor(0x0b, 0x72, 0x72)
p.font.bold = True

# Add speaker notes
notes_slide = slide.notes_slide
notes_slide.notes_text_frame.text = speaker_notes_string
```

**File output:** `./mnt/{project_name}/presentations/{project_name}-simple.pptx`  
(Different filename from any existing HTML-converted PPTX to avoid conflicts)

---

## When to Build

After HTML-first is live and we have usage data. If teachers are actively requesting PPTX, build this. If nobody asks for it, don't.

**Trigger:** Teacher types anything like:
- "Can I get a PowerPoint version?"
- "I need this as a .pptx"
- "My school uses PowerPoint"
- "Can you export to PowerPoint?"

Agent calls `BuildSimplePptx` with the structured content it already has from the generation session.

---

## What Happens to BuildPptxFromHtmlSlides

It stays in the codebase but is no longer called by default. It can be used as a fallback if the agent needs a quick screenshot-based PPTX for any reason. It will eventually be deprecated once `BuildSimplePptx` is built.
