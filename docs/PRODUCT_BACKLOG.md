# Forge — Product Backlog

> Bridge between teacher research findings and engineering execution.
> Generated from RESEARCH_FINDINGS_*.md by the forge-research-to-backlog agent.
> | Last updated: 2026-05-18 (Run 33 — Reviewed RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md)

---

## Legend

| Field | Meaning |
|-------|---------|
| P0 | Must build. High value, low cost, or critical path. |
| P1 | Should build. Next milestone. |
| P2 | Could build. Future expansion. |
| Source | Which RESEARCH_FINDINGS file proposed this |
| Status | New / Planned / In Progress / Done / Deprioritized |
| VISION.md | Already in VISION.md? Yes / No / Partial |

---

## P0 — Build Now

### P0.1 Flashcard Generation

- **Problem:** YL teachers spend hours creating/cutting/laminating flashcards. Current tools (Twinkl) offer static libraries. No competitor generates custom flashcards from conversation.
- **Proposed feature:** `{topic, level} → printable PDF flashcards with images`. User describes what they need, Forge generates a multi-page flashcard sheet.
- **Differentiator:** Forge could add L1-aware vocabulary (include L1 translations for Portuguese speakers).
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.1, 5)
- **VISION.md:** No — not mentioned in Section 8 (outputs) or Section 2 (solution)
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-09

---

### P0.2 Scenario / Role-Play Card Generation (Business English)

- **Problem:** Business English teachers' #1 pain point is creating authentic business scenarios (meetings, negotiations, presentations). No existing tool generates role-play cards for specific industries/L1s.
- **Proposed feature:** `{scenario type, industry, level, L1} → printable role-play cards + key phrases + facilitation notes`. E.g., "Meeting with Japanese clients — practice softening language" produces cards with student roles, discussion prompts, and key phrases.
- **High willingness to pay:** BE teachers earn $50-150/hr and will pay $20-50/mo for a tool that saves 2+ hours prep.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.3, 5)
- **VISION.md:** No
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-09

---

### P0.3 Assessment Generation

- **Problem:** Assessment creation is the #2 ESL teacher pain point (8.2 hrs/week on marking/evaluation). Adult Ed teachers need progress tests, exit tickets, and unit quizzes. No competitor generates custom assessments from conversation.
- **Proposed feature:** `{level, topic, question types (MCQ / fill-in / matching / short answer)} → printable PDF test + answer key`. Four assessment types: placement/diagnostic, unit/progress, exit tickets, summative.
- **Market gap:** Ellii has lesson-embedded quizzes (not standalone generation). Off2Class has pre-built (not customizable). This is wide open.
- **CEFR alignment required:** Questions must map to A1-C2 "can-do" descriptors for credibility.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_ASSESSMENT_AND_TESTING (sections 1-8); RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (section 1.2); RESEARCH_FINDINGS_TOP_10_PAIN_POINTS (recommendation 3)
- **VISION.md:** No — assessments not mentioned in Section 8
- **Effort estimate:** 2 sessions (new prompt templates + CEFR alignment logic)
- **Status:** New
- **Date added:** 2026-05-09

---

### P0.4 Conversation Lesson Mode (Instant Generation)

- **Problem:** Online 1-on-1 teachers (Preply, Cambly, iTalki) have back-to-back 30-min classes with zero prep time. They need "acceptable materials in 30 seconds."
- **Proposed feature:** A dedicated mode where the teacher types a topic and gets an instant lesson — discussion questions, vocabulary, follow-up homework. Minimal back-and-forth. One-shot generation.
- **Target persona:** Online ESL Teachers (Persona 6) — fastest-growing segment, moderate-high willingness to pay.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.6, 5)
- **VISION.md:** Partial — conversation interface is planned, but the "instant one-shot" mode is not specified
- **Effort estimate:** 0.5 session (new prompt template + mode switch)
- **Status:** New
- **Date added:** 2026-05-09

---

### P0.5 Level Differentiation ("Make This Harder/Easier")

- **Problem:** Teachers in mixed-ability classrooms need materials at multiple levels. No competitor provides built-in level variants from a single request.
- **Proposed feature:** After generating a worksheet/slide deck, teacher can say "make this harder" or "make this for B1 instead of A2." Forge regenerates at the requested level while keeping topic + structure.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_COMPETITIVE_GAPS (section 5, recommendation 6); RESEARCH_FINDINGS_TOP_10_PAIN_POINTS (recommendation 2)
- **VISION.md:** No
- **Effort estimate:** 1 session (conversation state management + level-switching prompt)
- **Status:** New
- **Date added:** 2026-05-09

---

## P1 — Next Milestone

### P1.1 Homework / Self-Study PDF Generation

- **Problem:** BE and Online teachers' students expect take-home practice. Teachers spend time creating homework PDFs.
- **Proposed feature:** When generating materials, optionally include a 1-page homework PDF with exercises + answer key for self-study.
- **Low effort:** Reuse assessment generation pipeline, just output is a shorter "homework" variant.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.3, 1.6, 5)
- **VISION.md:** No
- **Effort estimate:** 0.5 session
- **Status:** New
- **Date added:** 2026-05-09

---

### P1.2 L1‑Specific Error Callouts in Generated Output

- **Problem:** Teachers need materials that explicitly show students WHY their specific L1 causes certain errors. Generic materials don't do this.
- **Proposed feature:** Generated slides/worksheets automatically include highlighted callout boxes: "Spanish speakers: In Spanish you say 'X', which causes this error. In English, the structure is different." Powered by L1 database entries.
- **Forge's differentiator:** This makes L1 intelligence visible in every output. Competitors can't copy this without the L1 database.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (section 7, insight 1); RESEARCH_FINDINGS_COMPETITIVE_GAPS (section 5, recommendation 3)
- **VISION.md:** No — VISION mentions L1 intelligence in section 3.1 but doesn't specify it as visible callouts in output
- **Effort estimate:** 1 session (prompt template changes + L1 DB query integration)
- **Status:** New
- **Date added:** 2026-05-09

---

### P1.3 Structured Lesson Plan Output

- **Problem:** Current VISION.md specifies lesson plans as a .pdf output but doesn't detail the structure. Teachers (especially Adult Ed and EAP) need detailed, structured lesson plans with timing, procedure, differentiation notes.
- **Proposed feature:** Lesson plan output includes: learning objectives, materials needed, step-by-step procedure with timing estimates, differentiation notes for mixed levels, homework suggestions.
- **Already partially in plan:** VISION.md Section 8 mentions lesson plans. This is a specification refinement, not new.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.2, 1.5)
- **VISION.md:** Partial — mentioned but not specified in detail
- **Effort estimate:** 0.5 session
- **Status:** New
- **Date added:** 2026-05-09

---

### P1.4 Business English Scenario Library

- **Problem:** BE teachers create the same scenarios repeatedly (meetings, negotiations, presentations). A reusable template library would speed this up.
- **Proposed feature:** 10-15 pre-built scenario templates with blanks for customization. Teacher selects "Negotiation" → enters industry/difficulty → gets tailored materials. Powered by the activity library pattern.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (sections 1.3, 5)
- **VISION.md:** No
- **Effort estimate:** 1 session (YAML templates + prompt integration)
- **Status:** New
- **Date added:** 2026-05-09

---

## P2 — Future

### P2.1 Interactive Digital Lesson Viewer

- **Problem:** ESL Brains' e-lesson plans (interactive web-based) are popular but Forge generates only static downloads. Online teachers want interactive lessons.
- **Proposed feature:** Web-based lesson viewer with clickable exercises, auto-reveal answers, and slide navigation. Think "ESL Brains but generated on demand."
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_COMPETITIVE_GAPS (sections 2.3, 5)
- **VISION.md:** No
- **Effort estimate:** 3+ sessions (significant frontend work)
- **Status:** New

---

### P2.2 Student Error Tracking & Adaptive Materials

- **Problem:** Teachers want to track which errors each student makes and get materials that progressively address them.
- **Proposed feature:** Teacher can log student errors (e.g., "Maria keeps dropping articles"). Forge remembers and automatically incorporates these into future lesson generations. Spiderweb visualization of error clusters per student.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_COMPETITIVE_GAPS (section 5, recommendation 8)
- **VISION.md:** No
- **Effort estimate:** 3+ sessions (needs persistent storage + student profiles)
- **Status:** New

---

### P2.3 School / Institutional Licensing Tier

- **Problem:** Real revenue comes from schools, not individual teachers. Schools need shared account management, usage tracking, and curriculum alignment.
- **Proposed feature:** Institutional dashboard: manage teacher accounts, view usage stats, align generated materials to school curriculum, billing per seat.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS (section 7, insight 5); RESEARCH_FINDINGS_COMPETITIVE_GAPS (section 5)
- **VISION.md:** Partial — "Monetization" listed as "later, build first"
- **Effort estimate:** 5+ sessions (auth, accounts, billing, dashboard)
- **Status:** New

---

### P2.4 Video Lesson Support

- **Problem:** ISLCollective's video quizzes are popular but static. Teachers want to embed comprehension questions in YouTube videos.
- **Proposed feature:** Teacher provides a YouTube URL + level. Forge generates comprehension questions, discussion prompts, and vocabulary exercises based on the video content.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_COMPETITIVE_GAPS (section 5, recommendation 10)
- **VISION.md:** No
- **Effort estimate:** 2 sessions (YouTube API + question generation)
- **Status:** New

---

### P2.5 Institutional Licensing Tier (duplicate entry removed) 

---

### P2.30 Ready‑Made Material Packs

- **Problem:** Teachers lack ready‑to‑use lesson‑plan bundles, forcing them to assemble slides, worksheets, and flashcards manually.
- **Proposed feature:** Offer downloadable bundles of pre‑generated lesson‑plan materials (slides, worksheets, flashcards, activities) for common topics with a single click.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-15

---

### P2.31 Rapid‑Customization Templates

- **Problem:** After AI generation teachers still need to edit vocabulary or difficulty, spending time on manual tweaks.
- **Proposed feature:** UI allowing teachers to adjust AI‑generated content (swap vocabulary, change difficulty) via single‑click controls, instantly regenerating the affected sections.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-15

---

### P2.32 Micro‑Lesson Generator

- **Problem:** Teachers need quick, low‑time activities for days with limited class time.
- **Proposed feature:** One‑click generator for 5‑minute filler activities or warm‑ups, selectable by topic and level.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-15

---

### P2.33 Integrated Grading Assistant

- **Problem:** Grading short answers, essays and providing feedback consumes large amounts of teacher time.
- **Proposed feature:** AI‑driven auto‑grading engine that evaluates short‑answer responses, applies rubric scoring to essays, and produces instant feedback PDFs.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-15

---

### P2.34 Classroom‑Management Toolkit

- **Problem:** Managing disruptive behaviour and low‑tech classrooms wastes instructional time.
- **Proposed feature:** Generate printable behaviour‑management scripts, visual cue cards, and low‑tech activity backups on demand.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-15

---

### P2.35 Parent‑Communication Pack

- **Problem:** Teachers spend significant time drafting bilingual progress summaries and reports for parents.
- **Proposed feature:** Generate ready‑made bilingual email templates and printable progress‑summary reports that teachers can customise with a few clicks.
- **Priority:** P1
- ...
---

### P2.44 Mobile‑optimised UI

- **Problem:** 28 % of teachers teach from tablets; current UI is not fully optimized for touch and offline generation.
- **Proposed feature:** Lightweight web app with offline generation capability, larger touch targets, and simplified workflow for tablet‑first users.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TECHNOLOGY_STACK_2026-05-16.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-16

---

### P2.45 Budget‑friendly subscription tier

- **Problem:** Budget constraints limit purchase of premium platforms, driving interest in affordable, pay‑per‑use solutions.
- **Proposed feature:** Offer a budget‑friendly subscription tier (pay‑as‑you‑go) to attract cost‑sensitive teachers and schools.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-17

---

---

### P0.6 AI-generated lesson‑plan templates

- **Problem:** Teachers spend excessive time creating lesson plans, slides, and worksheets.
- **Proposed feature:** AI‑generated lesson‑plan templates (slides, worksheets, activities) instantly customizable per proficiency level.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P0.7 Auto‑graded speaking & writing rubrics

- **Problem:** Grading speaking and writing tasks is time‑intensive for teachers.
- **Proposed feature:** Auto‑graded speaking‑and‑writing rubrics using OpenSwarm‑generated feedback snippets.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P1.6 Adaptive content carousel

- **Problem:** Heterogeneous proficiency levels cause instructional inefficiency.
- **Proposed feature:** Adaptive content carousel allowing teachers to select a proficiency tier and auto‑populate differentiated activities.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-17

---

### P1.7 Resource marketplace integration

- **Problem:** Scarcity of high‑quality, curriculum‑aligned digital resources forces teachers to reinvent content.
- **Proposed feature:** One‑click import of vetted, copyright‑clear assets from Twinkl, BusyTeacher, etc.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.49 Student‑engagement analytics

- **Problem:** Teachers lack insight into learner disengagement early enough.
- **Proposed feature:** AI‑driven sentiment analysis on chat logs and participation metrics to flag disengaged learners.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.50 Built‑in admin dashboard

- **Problem:** Administrative paperwork (attendance, reporting, curriculum mapping) consumes teaching time.
- **Proposed feature:** Built‑in admin dashboard for attendance, reporting, and curriculum‑mapping exportable to school systems.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.51 Assessment builder

- **Problem:** Lack of ready‑made, standards‑aligned assessment templates.
- **Proposed feature:** Assessment builder with pre‑populated placement, progress, and final‑test templates aligned to CEFR levels.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.52 Professional‑development hub

- **Problem:** Professional development opportunities are scarce for teachers.
- **Proposed feature:** Short micro‑learning videos on tech integration, differentiated instruction, and AI usage.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

---

### P0.8 Automated Lesson‑Plan Generator

- **Problem:** Teachers spend hours creating lesson plans, slides, worksheets, and flashcards manually.
- **Proposed feature:** AI generates complete lesson plans (slides, worksheets, flashcards) in under 2 minutes from a brief prompt.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P0.9 L1‑Interference Insight Layer

- **Problem:** Materials lack explicit L1‑specific error explanations for students.
- **Proposed feature:** Embed error‑type notes and explanations tied to students' native language into generated materials.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P0.10 Slide & Flashcard Designer

- **Problem:** Teachers need attractive slides and printable flashcards quickly.
- **Proposed feature:** Drag‑free layout tool that produces downloadable PPTX/PDF slides and Anki‑compatible flashcard decks.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P0.11 Pricing Model Proof‑Point

- **Problem:** Teachers will only pay if they see clear time‑saved ROI.
- **Proposed feature:** UI calculator showing estimated weekly preparation time saved, justifying subscription pricing.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P1.8 LMS Connector

- **Problem:** Teachers waste time uploading and linking files across LMS platforms.
- **Proposed feature:** One‑click export of generated resources to Google Classroom, Canvas, Moodle (resource package + class code).
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.53 Material Quality Filter

- **Problem:** Auto‑generated content may vary in quality; teachers need curation.
- **Proposed feature:** Curate high‑quality templates and allow teachers to flag low‑quality outputs for continuous improvement.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

### P2.54 Audio/Video Library Integration

---
### P0.12 Ready‑to‑use lesson packs
- **Problem:** Teachers lack ready‑to‑use lesson‑plan bundles, forcing them to assemble slides, worksheets, and flashcards manually.
- **Proposed feature:** Offer downloadable bundles of pre‑generated lesson‑plan materials (slides, worksheets, flashcards, activities) for common topics with a single click.
- **Priority:** P0
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md
- **VISION.md:** No
- **Effort estimate:** quick (1 session)
- **Status:** New
- **Date added:** 2026-05-18

---
### P1.9 Adaptive content personalization
- **Problem:** Teachers need instantly adaptable content (e.g., vocabulary lists for a specific industry) but must edit manually.
- **Proposed feature:** Prompt‑based tweaks that instantly regenerate assets (slides, worksheets, vocab lists) with changed topic, difficulty, or industry without re‑authoring.
- **Priority:** P1
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md
- **VISION.md:** No
- **Effort estimate:** 1 session
- **Status:** New
- **Date added:** 2026-05-18

---
### P2.55 Usage analytics dashboard
- **Problem:** Teachers receive little data on which materials actually improve student outcomes, leading to repeated reuse of ineffective resources.
- **Proposed feature:** Capture click‑through and student performance metrics for generated assets and present a simple dashboard to inform teachers which materials are most effective.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-18

---
### P2.56 AI‑assistant onboarding flow
- **Problem:** Many ESL teachers are unfamiliar with AI‑assisted content generation and fear reliability/accuracy issues.
- **Proposed feature:** Interactive tutorial and best‑practice guide that walks teachers through using Forge, building confidence in AI‑generated content.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-18

- **Problem:** Sourcing authentic audio/video materials is time‑consuming.
- **Proposed feature:** searchable API integration (Creative Commons, ESLPod) to insert audio/video into lessons with one click.
- **Priority:** P2
- **Source:** RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md
- **VISION.md:** No
- **Effort estimate:** quick
- **Status:** New
- **Date added:** 2026-05-17

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

||| Research File | Backlog Items Generated |
|||---------------|------------------------|
||| RESEARCH_FINDINGS_ESL_TEACHER_PERSONAS | P0.1, P0.2, P0.4, P1.1, P1.2, P1.3, P1.4, P2.5, P2.6 |
||| RESEARCH_FINDINGS_ASSESSMENT_AND_TESTING | P0.3 |
||| RESEARCH_FINDINGS_COMPETITIVE_GAPS | P0.5, P2.1, P2.2, P2.3, P2.4 |
||| RESEARCH_FINDINGS_TOP_10_PAIN_POINTS / top10-pain-points | P0.3 (cross-ref), P0.5 |
||| RESEARCH_FINDINGS_AI_IN_ESL | Market context only (no new features) |
||| RESEARCH_FINDINGS_GRAMMAR_METHODOLOGIES | Methodology-agnostic recommendation (no backlog item — intentional) |
||| RESEARCH_FINDINGS_top-10-pain-points-of-esl-teachers_2026-05-09.md | P1.5, P1.6, P2.7, P2.8 |
||| RESEARCH_FINDINGS_TOP-10-PAIN-POINTS_2026-05-10.md | P0.6, P1.7, P2.9, P2.10, P2.11 |
||| RESEARCH_FINDINGS_ESL_TEACHER_WORKFLOW_DEEP_DIVE_2026-05-10.md | P1.8, P1.9, P1.10, P2.12, P2.13, P2.14 |
||| RESEARCH_FINDINGS_TOOL_ADOPTION_AND_WTP_2026-05-10.md | P0.7, P0.8, P1.11, P2.15, P2.16, P2.17 |
||| RESEARCH_FINDINGS_top-10-pain-points_2026-05-13.md | P0.18, P0.19, P0.20, P2.22, P2.23, P2.24, P2.25, P2.26, P2.27, P2.28, P2.29, P2.30, P2.31 |
||| RESEARCH_FINDINGS_top-10-pain-points_2026-05-14.md | P0.21, P1.16, P1.17 |
||| RESEARCH_FINDINGS_top-10-pain-points_2026-05-15.md | P0.22, P0.23, P0.25, P1.18, P1.19, P1.20, P2.34 |
||| RESEARCH_FINDINGS_top-10-pain-points_2026-05-16.md | P0.27, P0.28, P0.29, P0.30, P0.31, P1.22, P1.23, P1.24, P2.40, P2.41, P2.42, P2.43, P2.44 |
||| RESEARCH_FINDINGS_TECHNOLOGY_STACK_2026-05-16.md | P0.27, P0.28, P0.29, P0.30, P0.31, P1.22, P1.23, P1.24, P2.40, P2.41, P2.42, P2.43, P2.44 |
|||| RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-17.md | P0.8, P0.9, P0.10, P0.11, P1.8, P1.25, P1.26, P2.45, P2.46, P2.47, P2.48, P2.53, P2.54 |
||| RESEARCH_FINDINGS_TOP_10_PAIN_POINTS_2026-05-18.md | P0.13, P2.57 |
|||| RESEARCH_FINDINGS_top-10-pain-points_2026-05-17.md | — |
