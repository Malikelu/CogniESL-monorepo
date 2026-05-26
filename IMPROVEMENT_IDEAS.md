# CogniESL: Improvement Ideas
**Focus:** High-impact, low-disruption improvements — no drastic changes to the architecture  
**Last updated:** 2026-05-24  
**Implemented:** 1a ✅ · 1b ✅ · 1d ✅ · 1e ✅ · 4c ✅ · 4d ✅ · 5a ✅ · 5b ✅ · 5c ✅  
**Not yet built:** 5g (daily digest) → 3a (lesson plan) → 5d (social share) → 5f (Google review) → 3b (homework F) → 5e (branded snapshot) → 3c (pronunciation slide) → 3e (flashcards) → 3d (progress tracker) → 1c (L1 comparison box, needs forge)

---

## 1. L1 Oracle Delivery — Making It Hit Harder

The L1 Oracle is the strongest differentiator. Every improvement to it directly increases perceived value. Here are specific, implementable improvements that do not require database changes:

### 1a. Multi-L1 Oracle Slides (no additional YAML needed)
Currently each L1 Oracle slide shows one wrong/correct pair. The YAML files often have 3–5 error examples per grammar point. Show all of them in a card grid on the slide rather than just one. The visual impact of seeing five specific, named errors your students make is much stronger than seeing one.

Implementation: The HTML writer already has the data via the task_brief. Just add 2–4 more contrast cards below or beside the main pair. The bottom explanation strip stays. One slide, much more content, same cost.

### 1b. The "Why" Statement as a Visual Headline
Currently `why_it_happens` appears in small text in the bottom strip. Make it the slide's headline — a large, teacher-readable explanation in the center of the green panel. Something like: "Spanish present tense works for both habitual and immediate actions. English separates them. Your students are applying Spanish logic."

Teachers read the WHY and immediately have language to use in class. That's an unlock moment.

### 1c. L1 → English Comparison Box
Add a small comparison box showing the equivalent structure in the student's L1 alongside the English. For Spanish: `Yo voy al colegio cada día` → `I go to school every day`. This gives the teacher a way to bridge — "In Spanish you say X, in English we say Y." Teachers who don't speak the student's L1 can still use this as a reference.

This requires adding L1 sentence examples to the interference YAML files. Not all have them, but the top 5 languages do. Start there.

### 1d. Teacher Script Inclusion in Speaker Notes
The L1 file already contains `teacher_tips` — a pedagogical explanation of how to address the error. Currently only a fraction of this makes it into speaker notes. Make it mandatory: every L1 Oracle slide's speaker notes must include the complete `teacher_tips` text verbatim, formatted as "Suggested teacher script: [text]". This is the hidden gem of the database — most of it never reaches the teacher's ears.

### 1e. L1 Oracle as the Second-to-Last Slide (Consistent Position)
Right now L1 Oracle slides are scattered in position depending on the deck. Move them to a consistent position: always the second-to-last slide group, right before the wrap-up. Teachers will learn "the L1 slides are near the end" and look forward to them. Predictability = comfort.

---

## 2. Database Enrichment — The Highest Leverage Work

The database is what makes CogniESL trustworthy. Every addition compounds over all future generations. Here are specific enrichments that would make the biggest difference:

### 2a. Add L1 Sample Sentences to All 36 Interference Files
The most requested enrichment: a native-language example sentence alongside every English wrong/correct pair. Currently most files have only English. Adding even one L1 sentence per error pattern would enable the L1 → English comparison box described above.

Priority order for enrichment: Spanish, Mandarin, Brazilian Portuguese, French, Arabic (these are the top 5 L1s and cover ~65% of US ESL classrooms).

Each entry needs two lines added:
```yaml
example_l1: "Yo voy al colegio cada día."
example_l1_gloss: "I go to school each day." # literal word-for-word translation
```

This is manual work but low-skill — native speakers can add these without linguistic expertise.

### 2b. Expand Common Errors in Grammar Files
The grammar YAML `common_errors` section has 3–5 items per grammar point. Increasing this to 8–10 items would allow more variety across multiple worksheet exercises without repetition. Currently the worksheet generator sometimes reuses the same base sentence across exercises because the pool is small.

Target: every grammar file has at least 8 `common_errors` entries with wrong/correct/explanation triplets.

### 2c. Add "Real Student Quotes" Examples
One high-impact addition: a `student_quotes` field in each L1 interference file containing anonymized examples of actual sentences real students have written or said. These are different from constructed examples — they feel authentic. Teachers recognize them immediately ("my students say exactly that").

Format:
```yaml
student_quotes:
  - "My teacher say that homework is important." # L1: Spanish
  - "She don't like the homework." # L1: Spanish
```

These would appear in the L1 Oracle slide as an additional card: "Teachers report hearing..." with the real quote in quotation marks.

### 2d. Add Corpus Frequency Data to Grammar Files
Add a `corpus_frequency` field indicating how often the structure appears in real English text (based on corpora like COCA or BNC). This would allow:
- A "How common is this?" indicator on slides
- Prioritization advice: "This structure appears in 73% of academic texts — very important for your B2 students"
- A teaching priority score that teachers can use to decide which grammar points to teach first

This would require research but the data is publicly available from COCA/BNC. Medium effort, high differentiation.

### 2e. Add "Typical Lesson Duration" to Activity Files
Currently activity files are missing a time estimate. Adding `duration_minutes: 20` to each activity YAML would let the Content Brief show the teacher an estimated lesson time. "This lesson will take approximately 45 minutes: 10 min exposition + 15 min L1 practice + 20 min writing activity." Teachers plan lessons in 45-minute blocks — this makes the brief more useful.

---

## 3. Material Depth — What Else Would Wow Teachers

These are additions to the generated materials that would meaningfully increase the value of each generation:

### 3a. A "Lesson Plan" Cover Page (Highest Impact)
Add a one-page lesson plan document to every generation (not the activity guide, but a proper structured plan):

```
LESSON PLAN — Present Simple — Spanish Adults — B1

Objective: Students will be able to use Present Simple for habits and routines without L1 interference from Spanish

Duration: 45–55 minutes

Stage 1: Hook (5 min) — Slide 1
Stage 2: Meaning (10 min) — Slides 2–3. CCQ: "Is the sun rising right now? (No — always true)"
Stage 3: Form (10 min) — Slides 4–7. Watch for: -s omission on 3rd person
Stage 4: L1 Focus (5 min) — Slides 12–13. Key error: "He walk" → "He walks"
Stage 5: Practice (10 min) — Slide 14. Activity: [name]
Stage 6: Production (10 min) — Worksheet Section E

Anticipated difficulties: [from L1 file]
Differentiation: [from activity file]
```

This is the document teachers currently write by hand before class. Giving it to them pre-filled, based on the actual slides and L1 data, is enormous time savings. One generation → lesson plan + slides + worksheet + activity guide = everything for the week.

### 3b. A "Follow-Up Homework" Section in the Worksheet
Add a Section F to every worksheet: 2–3 homework exercises (slightly harder than Section E, designed for completion outside class). These would use the production context from the grammar YAML and the teacher wouldn't need to create homework separately.

Minimal additional cost (same pipeline, small additional output).

### 3c. Pronunciation Guidance Slide
For each grammar point, the grammar YAML often has `phonetics` data — when the third-person -s is pronounced /s/, /z/, or /ɪz/, for example. This is frequently overlooked but teachers ask for it often. Add a dedicated pronunciation slide between the form slides and the practice slide:

- Shows the pronunciation rule with examples
- Groups words by sound pattern
- Includes L1-specific phonetic difficulties (from the L1 YAML if available)

Spanish speakers, for example, have difficulty with the /z/ sound in "lives" and "goes" because Spanish lacks this phoneme in most positions. This data is already in the database — it just needs a dedicated slide to surface it.

### 3d. A "Progress Tracker" Template (Simple, High Perceived Value)
A one-page student self-assessment template that matches the specific lesson:

```
After this lesson, I can:
□ Use Present Simple for habits ("I play football every week")
□ Avoid my typical error: ________________________________
□ Give 3 examples of my own:
   1. _______________________________________________
   2. _______________________________________________
   3. _______________________________________________
```

This takes ~5 minutes to generate (mostly fill-in-the-blank template with lesson data) but gives teachers a professional-looking student handout they didn't have to make.

### 3e. Flashcard Set (Low Effort, High Teacher Utility)
Generate a set of 10–15 vocabulary/structure flashcards as a PDF (simple 2-column format: term/example on left, definition/translation on right). Teachers print these and cut them for pair-work activities. The data (vocabulary from `use` context, example sentences from `common_errors`) already exists in the YAML files.

This doesn't require a new agent — just a simple template fill. Adds ~$0.05 to generation cost.

---

## 4. UX Improvements (No Backend Changes)

### 4a. Slide Preview in the Chat Before PPTX
After generation, show a thumbnail image of slide 1 directly in the chat window (as a base64 image). The teacher sees a preview of the visual quality before even opening the email. Creates an immediate "wow" moment. Implementation: take a screenshot of slide 1 HTML using Playwright and attach it to the response.

### 4b. "Teach Me Why" Mode
Optional toggle in the chat: "Explain this to me as you go." When active, the agent narrates each slide as it's generating: "Slide 3 is a CCQ slide — this is designed to check understanding before showing grammar formulas. Here's the question I'm using from the database..." Teachers who are new to L1-aware teaching learn from watching the generation. High retention value.

### 4c. Quick Edit Suggestions After Delivery
After sending the "your materials are ready" message, add 3 clickable suggestions:
- "Change the examples to use [topic] vocabulary"
- "Add a second L1 for [language]"
- "Make the worksheet harder (B2 level)"

These are the most common post-delivery requests. Pre-populating them as chips means the teacher doesn't have to think of the right phrasing.

### 4d. Topic Vocabulary Lock-In During Interview
Add one question to the chat interview: "Is there a specific topic or vocabulary set you want to use? (e.g., technology, sports, food, travel — or leave blank for general English)." This vocabulary set then appears throughout examples and the production section consistently. Currently examples are chosen from the grammar YAML which uses generic contexts. Topic consistency makes the lesson feel more coherent.

---

---

## 5. Self-Running App — Phase I Quick Wins
*Full design in `docs/SELF_RUNNING_COGNIESL.md`. Items below are the first-priority, high-leverage builds.*

### 5a. Feedback Widget on Material Cards (Highest Priority)
Add a `👍 Perfect / 👍 Good / 👎 Issues` row to every card in My Materials. One tap, no page navigation. If "Issues" is tapped, expand 6 category chips inline (`Wrong level`, `L1 errors`, `Missing content`, `Wrong grammar`, `Formatting`, `Other`).

Requires:
- New `feedback` table in `cogniesl.db`
- `POST /api/feedback` endpoint (no auth friction — just material_id + rating)
- Frontend addition to materials card component

This is the primary feedback channel. All subsequent intelligence depends on having this data.

### 5b. Behavioral Events Table
New `events` table logging: `generation_started`, `generation_completed`, `material_downloaded`, `feedback_submitted`, `login`. Inserted by server-side hooks, no UI needed.

Key signal: a teacher who downloads materials but never returns within 14 days is a churn signal. A teacher who regenerates the same grammar point within 48h was unsatisfied with the first output. You can't act on these patterns until you're logging them.

### 5c. Frustration Detection in Chat Agent
One instruction added to `instructions.md`: "If the teacher's message expresses dissatisfaction or rejection of generated output (e.g., 'this is wrong', 'that's not what I meant', 'the level is off'), silently call the `log_feedback` tool with the specific issue mentioned." No extra UI. No teacher action required. Free signal capture.

### 5d. Post-Generation Social Share Prompt
After materials are delivered, agent adds to the completion message: "If CogniESL saved you time today, one sentence about your experience helps other teachers find us. Want to share? 🎉" → if yes, show 4 pre-written templates + platform buttons.

**When:** only when generation completed without errors and teacher showed no frustration signals in chat.

### 5e. Branded Slide Snapshot for Sharing
After generation, use Playwright (already in codebase) to screenshot slide 1 → resize to 1080×1080 PNG → overlay with CogniESL watermark → attach to delivery email with caption "Love your materials? Share this image."

This is the strongest viral mechanic: a beautiful image of professional materials with a subtle "Generated with CogniESL" seen by every teacher who receives it by email.

### 5f. Google Review Request (After 3rd Generation)
After a teacher's 3rd successful generation, agent adds one line to the delivery message: "You've made 3 sets of materials with CogniESL 🎉. If it's working for you, a Google review helps other teachers find us [link]." Logic: only once per user, only after positive signal (no frustration, no bug), minimum 7 days since signup.

### 5g. Daily Digest Email to Marcos
Scheduled task (7am daily): queries DB → formats a summary → emails Marcos via Resend:
- Generations today vs. 7-day average
- API cost today
- New feedback (any Issues ratings?)
- New signups
- System health (error rate from jobs table)

Phase 1 of the self-running system. Takes ~4 hours to build and transforms how Marcos monitors the product.

---

*All improvements in this document are additive — they extend existing capabilities without requiring architectural changes. Priority order: 1a ✅ · 1b ✅ · 1d ✅ · 1e ✅ · 4c ✅ · 4d ✅ → next: 5a (feedback widget), 5b (events table), 5g (daily digest), 3a (lesson plan cover page), 5d (social share prompt), 5e (branded snapshot).*
