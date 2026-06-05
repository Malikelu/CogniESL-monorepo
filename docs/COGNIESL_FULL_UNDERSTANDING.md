# CogniESL — Complete Understanding

**Purpose:** Single source of truth for any AI agent working on this project.
Read this FIRST before writing any code, running any tests, or making any decisions.

**Last updated:** 2026-06-05
**Written because:** The pipeline broke after audit fixes because the agent didn't understand what CogniESL actually is. This document prevents that from happening again.

---

## 1. What CogniESL Is

CogniESL is an AI-powered ESL teaching material generator, sold as a subscription product.
A teacher describes their class (grammar topic, students' native language, age, level, skill focus),
and CogniESL generates a complete lesson package.

**The value proposition:** Materials are L1-aware — they specifically target the errors that
speakers of the students' native language make. A Spanish speaker learning Present Simple gets
slides highlighting third-person -s omission. A Japanese speaker gets different slides
targeting article omission. This is the differentiator.

**Business model:** Subscription — Free tier (5 generations/month, slides only, 5 L1 languages),
Pro tier ($12-18/month, all formats, all 36 L1 languages, 20 generations/month).

## 2. How It Works (Non-Technical)

The teacher chats with an AI agent that:
1. Asks clarifying questions (grammar, L1, age, level, skills, what materials they need)
2. Presents a Content Brief for approval
3. Fires off a background generation pipeline
4. Sends an email with download links when done

The pipeline:
- Loads pre-validated YAML data (grammar rules, L1 interference patterns, activity templates)
- Creates blank HTML slides
- Calls DeepSeek to write slide HTML content based on detailed task briefs
- Validates slides with Playwright (checks for overflow, missing content)
- Builds an offline HTML bundle (self-contained presentation viewer)
- Generates worksheet, activity guide, flashcards, progress tracker
- Converts everything to DOCX/PDF
- Marks job complete, sends email

## 3. All Materials CogniESL Can Produce

### Always generated (if format is in the request):

| # | Material | Formats | How Teacher Accesses It |
|---|----------|---------|------------------------|
| 1 | **Slides** | HTML bundle (.html) | Download link, or view in browser. Self-contained, works offline. F=fullscreen, N=notes, arrow keys. |
| 2 | **Worksheet** | DOCX + PDF | Download link. Sections A (fill the gap), B (error correction), C (L1 drill), D (write your own), E (answer key), F (homework). |
| 3 | **Activity Guide** | DOCX + PDF | Download link. Classroom activities from the database, differentiated by level. |
| 4 | **Flashcards** | PDF | Download link. Print-and-cut format. Front: error sentence (red), Back: correction + explanation (teal). |
| 5 | **Progress Tracker** | PDF | Download link. "After this lesson I can..." checklist with stars, L1 error checklist, example sentences. |

### Opt-in only (teacher must explicitly request):

| # | Material | Formats | Notes |
|---|----------|---------|-------|
| 6 | **PowerPoint** | .pptx | Only if teacher says "PPTX" or "PowerPoint" explicitly. NOT automatic. The primary viewing format is the HTML bundle — it's better (animations work, fonts render correctly, works offline). PPTX is a convenience export for teachers who need to edit. |

### Not yet implemented:

| # | Material | Status |
|---|----------|--------|
| 7 | **Homework** | No tool exists. Worksheet Section F covers basic homework. |
| 8 | **Quiz** | No tool exists. |

## 4. The Pipeline (Technical)

### Format flags (how the pipeline decides what to generate):

```python
has_slides = "slides" in all_formats or not all_formats    # Always true unless explicitly omitted
has_worksheet = "worksheet" in all_formats
has_activity = "activity" in all_formats or "activity guide" in all_formats
has_flashcards = "flashcards" in all_formats or "flash card" in all_formats
has_pptx = "pptx" in all_formats or "powerpoint" in all_formats    # OPT-IN ONLY
```

### Step-by-step:

| Step | What | Input | Output |
|------|------|-------|--------|
| 1 | Load YAML | grammar_point, l1_languages | grammar_data dict, l1_data_list |
| 2 | Slide plan | grammar_data, age, level | slide_plan (list of slide types), task_briefs dict |
| 3 | Blank slides + theme | project directory | slide_01.html ... slide_N.html, _theme.css |
| 4 | ModifySlide × N | task_briefs, blank slides, theme | Populated HTML slides with content |
| 5 | ValidateSlideSet | All slides | Validation pass/fail per slide |
| 6 | BuildOfflineBundle | All slides + theme | Self-contained .html bundle |
| 6.5 | BuildPptxFromHtmlSlides | Non-blank slides | .pptx file (ONLY if has_pptx) |
| 7 | Worksheet | grammar_data, l1_data | .source.html → ConvertDocument → .docx + .pdf |
| 8 | Activity Guide | grammar_data, activities | .source.html → ConvertDocument → .docx + .pdf |
| 9 | Flashcards | common_errors, l1_patterns | .source.html → ConvertDocument → .pdf |
| 9.5 | Progress Tracker | can-do statements, l1 pairs | .source.html → ConvertDocument → .pdf |
| 10 | MarkJobComplete | All file paths | Job marked "done", email sent, cache updated |

### File locations on Railway:

```
/app/data/mnt/{project_name}/
  presentations/
    slide_01.html ... slide_N.html     ← Generated slides
    _theme.css                         ← Theme DNA
    _checkpoint.json                   ← Batch progress
    {project_name}.html                ← Offline bundle
    {project_name}.pptx                ← PowerPoint (opt-in only)
  documents/
    {project_name}_worksheet.source.html     ← Source (CreateDocument)
    {project_name}_worksheet.docx            ← Delivery (ConvertDocument)
    {project_name}_worksheet.pdf             ← Delivery (ConvertDocument)
    {project_name}_activity_guide.source.html
    {project_name}_activity_guide.docx
    {project_name}_activity_guide.pdf
    {project_name}_flashcards.source.html
    {project_name}_flashcards.pdf
    {project_name}_progress-tracker.source.html
    {project_name}_progress-tracker.pdf
```

## 5. The Delivery Philosophy

**HTML-first, not PPTX-first.** This was a deliberate architectural decision.

The offline HTML bundle is the primary slide format. Teachers:
1. Open it in their browser (double-click the .html file)
2. Press F for fullscreen, N for speaker notes, arrow keys to navigate
3. No software needed — works on any computer

PPTX is a secondary convenience export. It's NOT in the default generation
because:
- It's 2,000× larger than HTML (15-35 MB vs ~120 KB)
- It costs more to store
- Animations and fonts may not render correctly
- Most teachers prefer the web viewer experience

**Teachers who need PPTX can ask for it.** The system supports it — it's just
not automatic. This was the user's explicit direction.

## 6. The "Database Is Sacred" Rule

All slide content comes from the YAML database:
- 302 grammar files with academic sources
- 36 L1 interference files per language
- 220 activity templates

The AI (DeepSeek) only does LAYOUT — arranging database content onto slides.
It never invents grammar rules, error examples, or pedagogical content.
The task_brief system feeds it exact content from the YAML files.

This means:
- Zero grammar errors (content is pre-validated)
- Scientifically-grounded teaching (peer-reviewed sources)
- L1 Oracle slides have real interference data, not AI guesses

## 7. Previous Mistakes (Do Not Repeat)

1. **PPTX added unconditionally to pipeline.** Fixed: now opt-in via `has_pptx` flag.
2. **Testing methodology was too narrow.** Only tested slides + bundle. Missed worksheet,
   activity guide, flashcards, progress tracker. Tests must validate ALL materials.
3. **Testing didn't verify layout/visual quality.** Slides must pass the "Would I pay
   a subscription for this?" test. 80/20 visual rule. CCQs before formulas.
4. **No way for Marcos to see results.** Tests must produce downloadable files so
   the human can visually inspect them. Links or local files.
5. **Reactive bug-fixing instead of understanding first.** The pptx mistake happened
   because I didn't re-read CLAUDE.md and the project docs before coding.

## 8. The Correct Approach

Before any code change:
1. Read this document
2. Read CLAUDE.md
3. State assumptions, ask if unclear
4. Make minimal changes — no "improvements" to adjacent code

Before testing:
1. Request ALL material formats in each test
2. One test at a time — wait for completion before starting next
3. Validate content accuracy (correct grammar point, correct L1 language)
4. Validate visual quality (speaker notes, themed, no blank slides)
5. Produce shareable results (download links, screenshots, or file dumps)
6. Vary grammar points, L1 languages, levels, age groups, skill focuses

## 9. Download Endpoints

After job status is "done":

| What | URL |
|------|-----|
| Slide viewer | `GET /api/jobs/{job_id}/bundle.html` |
| PowerPoint (if requested) | `GET /download/{job_id}/{project_name}.pptx` |
| Worksheet DOCX | `GET /download/{job_id}/{project_name}_worksheet.docx` |
| Worksheet PDF | `GET /download/{job_id}/{project_name}_worksheet.pdf` |
| Activity Guide DOCX | `GET /download/{job_id}/{project_name}_activity_guide.docx` |
| Activity Guide PDF | `GET /download/{job_id}/{project_name}_activity_guide.pdf` |
| Flashcards PDF | `GET /download/{job_id}/{project_name}_flashcards.pdf` |
| Progress Tracker PDF | `GET /download/{job_id}/{project_name}_progress-tracker.pdf` |
| Slide metadata JSON | `GET /api/jobs/{job_id}/slides` |
| Job status | `GET /api/jobs/{job_id}` |

For raw file inspection on Railway:
```bash
railway run ls /app/data/mnt/{project_name}/presentations/
railway run ls /app/data/mnt/{project_name}/documents/
railway run cat /app/data/mnt/{project_name}/presentations/_checkpoint.json
railway run wc -c /app/data/mnt/{project_name}/presentations/slide_*.html
```
