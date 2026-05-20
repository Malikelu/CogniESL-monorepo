# ⚠️ SUPERSEDED — Merged into FOUR_SKILLS_PLAN.md
This document's content has been merged into `FOUR_SKILLS_PLAN.md`, which is now the single source of truth.
Do not make changes here. Make changes to `FOUR_SKILLS_PLAN.md` instead.

---

# COGNISKILLS EXPANSION PLAN — Reading, Writing, Listening & Speaking
# Version 1.0 — Following Grammar DB Pattern
# Date: 2026-05-19
# Author: Apex (for Marcos)

---

## EXECUTIVE SUMMARY

Expand CogniESL beyond grammar to cover the four macro-skills: **Reading, Writing, Listening, Speaking**.

The approach follows the EXACT same pattern as the grammar database:
1. Define the concept (what is it, why it matters)
2. CCQs (how to check students understand)
3. How to teach it (step by step)
4. Sub-skills and micro-skills (detailed breakdown)
5. Common teacher mistakes
6. Phonetics (where applicable)
7. Teaching methodology and activities
8. Sources (same 5-tier system: primary, secondary, validation, pedagogical, teaching practice)
9. Common student errors by L1 group
10. Register/situational variation
11. L1 interference (added to existing L1 files)

---

## PART 1: AUTHORITATIVE SOURCE BOOKS

### Tier 1 — Buy/Access First

| # | Book | Authors | Year | Skills |
|---|------|---------|------|--------|
| 1 | **Reading in a Second Language** | Grabe & Stoller | 2020, Cambridge | Reading |
| 2 | **Teaching ESL/EFL Reading and Writing** | I.S.P. Nation | 2008, Routledge | Reading, Writing |
| 3 | **Teaching ESL/EFL Listening and Speaking** | I.S.P. Nation & Jonathan Newton | 2008, Routledge | Listening, Speaking |
| 4 | **Teaching and Learning Second Language Listening** | Vandergrift & Goh | 2012, Routledge | Listening |
| 5 | **Teaching Speaking: A Holistic Approach** | Goh & Burns | 2012, Cambridge | Speaking |
| 6 | **Teaching ESL Composition** | Ferris & Hedgcock | 2013, Routledge | Writing |
| 7 | **Second Language Writing** | Ken Hyland | 2003, Cambridge | Writing |
| 8 | **Sound Foundations** | Adrian Underhill | 2005, Macmillan | Listening, Speaking |
| 9 | **Teaching Pronunciation** | Celce-Murcia, Brinton, Goodwin | 2010, Cambridge | Speaking |
| 10 | **Teaching Listening Comprehension** | Penny Ur | 1984, Cambridge | Listening |
| 11 | **Exploring Second Language Reading** | Neil Anderson | 1999, Heinle | Reading |

### Tier 2 — Highly Recommended

| # | Book | Authors | Year | Skills |
|---|------|---------|------|--------|
| 12 | **Listening in the Language Classroom** | John Field | 2008, Cambridge | Listening |
| 13 | **Teaching Second Language Writing** | Charlene Polio | 2017, Cambridge | Writing |
| 14 | **How to Teach Speaking** | Scott Thornbury | 2005, Pearson | Speaking |
| 15 | **Teaching Second Language Reading** | Thom Hudson | 2007, Oxford | Reading |

---

## PART 2: DATA SCHEMA — FOLLOWING GRAMMAR DB PATTERN

### 2A. DIRECTORY STRUCTURE

```
data/
  grammar/              (existing: 300 files)
  activities/           (existing: 218 files)
  l1-interference/      (existing: 32 files)
  reading-skills/       (NEW: ~20 files)
  writing-skills/       (NEW: ~20 files)
  listening-skills/     (NEW: ~20 files)
  speaking-skills/      (NEW: ~25 files)
```

### 2B. SKILL TOPIC SCHEMA

This follows the EXACT same structure as grammar YAML files. Every section mirrors what we built for grammar.

```yaml
# data/speaking-skills/turn_taking.yaml

skill: turn_taking
title: Turn-Taking in Conversation
description: >
  Teaching students how English conversation manages who speaks when —
  how to take a turn, hold a turn, and yield a turn, and the signals
  that regulate conversational flow.
level: A2
category: interactional_competence
macro_skill: speaking

# ─── 1. CONCEPT DEFINITION ───
# (Same as grammar "meaning" section)
concept:
  core_concept: >
    Turn-taking is the system by which speakers alternate in conversation.
    In English, speakers use specific signals — intonation drops, fillers,
    and discourse markers — to manage who speaks when. Unlike some languages
    where overlapping speech is normal, English conversation generally
    expects one speaker at a time with minimal overlap.
  what_it_is_not: >
    Turn-taking is NOT about being polite or rude. It is a structural
    feature of conversation that varies across cultures. What counts as
    "interrupting" in English may be normal engagement in another language.
  contrast: >
    English turn-taking: One speaker at a time, brief pauses between turns,
    intonation signals for yielding. Japanese turn-taking: Frequent
    back-channeling (aizuchi), more tolerance for silence, different
    overlap norms. Spanish turn-taking: More overlapping speech, shorter
    pauses, simultaneous speech as engagement.

# ─── 2. CCQs (Concept Checking Questions) ───
# (Same structure as grammar CCQs — this is how teachers check understanding)
ccqs:
  - question: >
      If I'm speaking and my intonation goes down at the end of my sentence,
      am I inviting the other person to speak, or am I indicating I have
      more to say?
    answer: >
      A falling intonation at the end of a sentence typically signals that
      you have finished your turn and are yielding the floor. The other
      person can now speak. If you want to keep talking, you would use
      a level or rising intonation, or a filler like "so... anyway..."
    purpose: >
      Tests whether the student understands that intonation signals
      turn-yielding in English.
  - question: >
      In English conversation, if two people start speaking at the same time,
      what usually happens?
    answer: >
      One person typically stops and yields to the other. The person who
      continues is "holding the floor." This is different from some cultures
      where simultaneous speech is a sign of engagement.
    purpose: >
      Tests understanding of English overlap resolution norms.
  - question: >
      Is saying "Uh-huh" or "Yeah" while someone is speaking considered
      interrupting in English?
    answer: >
      No — these are back-channel signals that show you are listening and
      engaged. They are expected in English conversation. However, excessive
      back-channeling (as is normal in Japanese) can feel overwhelming to
      English speakers.
    purpose: >
      Tests understanding of back-channeling norms.

# ─── 3. HOW TO TEACH IT (Step by step) ───
# (Same as grammar "teaching" section but expanded)
teaching:
  methodology: Guided discovery with controlled then freer practice
  procedure:
    - step: "Awareness raising"
      detail: >
        Play a recording of a natural English conversation. Ask students:
        "How do they know when to speak? What signals do they use?"
        Elicit: falling intonation, pauses, discourse markers ("so," "anyway").
    - step: "Signal identification"
      detail: >
        Teach key turn-taking signals:
        Yielding: falling intonation, "so anyway," "what do you think?"
        Holding: fillers ("um," "well," "so"), level intonation
        Taking: "Can I add something?", "Sorry, just to...", "Going back to what you said..."
    - step: "Controlled practice"
      detail: >
        Give students a conversation script with turn-taking signals marked.
        Students practice reading it aloud, paying attention to the signals.
    - step: "Freer practice"
      detail: >
        Students have a discussion where they must use at least 3 turn-taking
        signals. Teacher monitors and gives feedback.
  tips:
    - >
      Start with awareness — most students don't realize turn-taking is
      systematic. The recording exercise is essential.
    - >
      Contrast with L1 norms explicitly. Students need to understand that
      English turn-taking is different, not "better."
    - >
      Practice in pairs first, then groups. Group discussions are harder
      because there are more people competing for turns.
  common_teacher_mistakes:
    - mistake: Assuming students already know how turn-taking works
      fix: Always start with awareness raising. Even advanced students may not realize the system.
    - mistake: Only teaching "polite interruption" phrases
      fix: Teach the full system — yielding, holding, and taking. Not just interruption.
    - mistake: Ignoring L1 differences
      fix: Explicitly contrast English norms with the student's L1 norms.

# ─── 4. SUB-SKILLS (Detailed breakdown) ───
# (Same as grammar "sub_rules" section)
sub_skills:
  - type: yielding_signals
    skill: How to signal you are finished speaking
    signals:
      - Falling intonation at end of sentence
      - "So anyway..." (topic closure)
      - "What do you think?" (explicit handover)
      - Longer pause (1-2 seconds)
    examples:
      - "And that's why I think we should go. [falling intonation] What do you think?"
      - "So anyway, that's the story. [pause]"
    explanation: >
      English speakers use a combination of intonation, discourse markers,
      and pauses to signal turn-yielding. Students who don't use these
      signals may be perceived as "monologuing" or not giving others a chance.
  - type: holding_signals
    skill: How to signal you are not finished
    signals:
      - Fillers: "um," "well," "so," "let me think"
      - Level or rising intonation (not falling)
      - Raising a finger or hand gesture
      - "Just a second," "I'm not done yet"
    examples:
      - "So... um... what I was trying to say was... [level intonation]"
      - "Well, there are actually two points. The first is..."
    explanation: >
      Holding signals prevent others from taking the turn. Students who
      don't use them may find others "stealing" their turn, which causes
      frustration and communication breakdown.
  - type: taking_signals
    skill: How to take a turn politely
    signals:
      - "Can I add something?"
      - "Sorry, just to jump in..."
      - "Going back to what you said about..."
      - "That reminds me of..."
      - Brief overlap + one person yields
    examples:
      - "Can I add something? I think there's another way to look at this."
      - "Sorry, just to jump in — I disagree with that point because..."
    explanation: >
      Taking signals acknowledge that you are entering the conversation.
      Without them, you may be perceived as interrupting. The key is to
      briefly overlap, then have one person yield.
  - type: back_channeling
    skill: How to show you are listening
    signals:
      - "Uh-huh," "Yeah," "Right," "I see," "Mm-hmm"
      - Nodding
      - Brief comments: "Exactly," "That's true"
    examples:
      - Speaker A: "So I went to the store and—" Speaker B: "Uh-huh" Speaker A: "—they didn't have what I needed."
    explanation: >
      Back-channeling shows engagement without taking the turn. English
      uses it less frequently than Japanese but more than some European
      languages. The right amount signals active listening.

# ─── 5. CONTEXTS OF USE ───
# (Same as grammar "use" section)
use:
  - context: Pair discussions
    description: Two people discussing a topic. Turn-taking is relatively simple.
    examples:
      - "What do you think about...?" "I think... What about you?"
  - context: Group discussions
    description: 3+ people. More complex turn-taking with more competition for the floor.
    examples:
      - "Can I add to what Maria said?"
      - "Sorry, just to jump in before we move on..."
  - context: Classroom participation
    description: Student-teacher and student-student turn-taking in class.
    examples:
      - "Can I say something?" "I have a question about..."
  - context: Phone conversations
    description: No visual cues. Turn-taking relies entirely on verbal signals.
    examples:
      - "So anyway, that's why I called. [pause] What do you think?"
  - context: Meetings
    description: Formal turn-taking with chairperson managing the floor.
    examples:
      - "If I could just finish my point..." "Can I come back to that?"

# ─── 6. PHONETICS (Where applicable) ───
# (Same as grammar "phonetics" section)
phonetics:
  - note: >
      Turn-taking signals are primarily intonational. A falling intonation
      contour (high to low) signals turn-yielding. A level or rising
      intonation signals the speaker is not finished.
    l1_issue: >
      Speakers of tone languages (Mandarin, Vietnamese, Thai) may apply
      L1 tonal patterns to English intonation, making their turn-yielding
      signals unclear to English listeners.
    practice: >
      Drill falling vs. level intonation on sentence-final words.
      "I think we should go [FALLING = finished] vs I think we should go
      [LEVEL = not finished, more to say]"
  - note: >
      Back-channel signals ("uh-huh," "mm-hmm") use a mid-level or slightly
      rising tone in English. A flat or falling tone can sound dismissive.
    l1_issue: >
      Japanese speakers may use back-channel signals too frequently
      (aizuchi norm), which can feel overwhelming to English speakers.
    practice: >
      Practice appropriate frequency: one back-channel signal per 10-15 seconds
      of the other person's speech.

# ─── 7. TEACHING ACTIVITIES ───
# (Same as grammar "recommended_activities" section)
recommended_activities:
  - name: Conversation Signals Hunt
    duration: 15
    description: >
      Students listen to a recorded conversation and tally each time they
      hear a turn-taking signal (yielding, holding, taking, back-channeling).
      They categorize each signal and discuss.
  - name: Turn-Taking Poker
    duration: 20
    description: >
      Students discuss a topic in pairs. Each student has 5 cards with
      turn-taking phrases. They must use all 5 cards during the conversation.
      First to use all cards wins.
  - name: Overlap Resolution Practice
    duration: 15
    description: >
      Students practice the "both start speaking → one yields" sequence.
      Teacher calls a topic, two students start speaking simultaneously,
      and they must resolve it naturally.

# ─── 8. SOURCES (Same 5-tier system as grammar) ───
sources:
  primary: "Goh & Burns (2012) Teaching Speaking: A Holistic Approach, Cambridge University Press, Chapter 6"
  secondary: "Thornbury & Slade (2006) Conversation: From Description to Pedagogy, Cambridge University Press, Chapter 4"
  validation: "Nation & Newton (2008) Teaching ESL/EFL Listening and Speaking, Routledge, Chapter 5"
  pedagogical: "Thornbury (2005) How to Teach Speaking, Pearson, Chapter 5"
  teaching_practice: "Folse (2009) Keys to Teaching Grammar to English Language Learners, University of Michigan Press, activities section"

# ─── 9. COMMON STUDENT ERRORS BY L1 GROUP ───
# (Same as grammar "common_errors" section)
common_errors:
  - error: Excessive back-channeling during partner's speech
    correction: Reduce back-channeling to once every 10-15 seconds
    explanation: >
      Japanese conversation norms expect frequent aizuchi (back-channeling)
      to show engagement. In English, this frequency can feel like the
      listener is trying to take over the conversation or is impatient.
    l1_groups:
      - Japanese (aizuchi norm: frequent back-channeling is polite)
      - Korean (similar back-channeling norms)
  - error: Long silences between turns, causing awkward pauses
    correction: Use fillers or brief responses to fill gaps
    explanation: >
      Japanese and Korean conversation tolerates longer silences between
      turns. In English, silences longer than 1-2 seconds feel awkward.
      Students need to learn to use brief responses to keep the conversation flowing.
    l1_groups:
      - Japanese (silence is acceptable, even respectful)
      - Korean (similar silence tolerance)
  - error: Overlapping speech perceived as interrupting
    correction: Wait for a clear pause or yielding signal before speaking
    explanation: >
      Spanish and Arabic conversation norms tolerate more overlapping speech
      than English. Students from these backgrounds may be perceived as
      "interrupting" when they are following their L1 norm of showing engagement.
    l1_groups:
      - Spanish (overlap = engagement)
      - Arabic (overlap = engagement)
      - Italian (similar overlap norms)
  - error: Not using any turn-taking signals — just waiting for silence
    correction: Teach explicit turn-taking phrases
    explanation: >
      Students from cultures with different turn-taking norms may simply
      wait for the other person to finish, then start speaking. This can
      lead to either long silences or both people starting at once.
    l1_groups:
      - Chinese (different turn-taking system)
      - Thai (different norms)
      - Finnish (longer pause tolerance)

# ─── 10. REGISTER / SITUATIONAL VARIATION ───
# (Same as grammar "register_notes" section)
register_notes:
  - note: >
      Informal conversation: More overlap, shorter pauses, more fillers.
      Formal conversation/meetings: Longer pauses, more explicit turn-taking
      phrases ("If I may..."), chairperson manages the floor.
  - note: >
      Phone conversations: No visual cues, so verbal turn-taking signals
      become essential. Students who rely on eye contact or gestures in
      face-to-face conversation struggle on the phone.
  - note: >
      Academic discussions: More structured turn-taking, often with a
      moderator. Students need to learn academic discussion phrases:
      "Building on what X said...", "I'd like to push back on that..."

# ─── 11. L1 INTERFERENCE SUMMARY ───
# (Brief summary — full data goes in L1 interference files)
l1_interference_summary:
  japanese: High — back-channeling frequency, silence tolerance, different overlap norms
  korean: High — similar to Japanese
  spanish: Medium — overlap tolerance, shorter pauses
  arabic: Medium — overlap tolerance
  chinese: Medium — different turn-taking system
  german: Low — similar turn-taking norms to english
  portuguese: Medium — some overlap tolerance
  # ... all 31 languages

# ─── 12. METADATA ───
created: 2026-05-19
last_revised: 2026-05-19
status: draft
```

### 2C. CATEGORY TAXONOMY

**Speaking skills:**
- interactional_competence (turn-taking, back-channeling, repair)
- pronunciation_segmentals (individual sounds by L1)
- pronunciation_suprasegmentals (stress, rhythm, intonation)
- functional_language (requests, refusals, apologies, opinions, suggestions)
- fluency_development
- discussion_skills
- presentation_skills

**Listening skills:**
- listening_strategies (gist, detail, inference, prediction)
- phonological_awareness (connected speech, stress, intonation recognition)
- listening_situations (lectures, conversations, announcements, phone)
- note_taking

**Writing skills:**
- organization (paragraph, essay, text structure)
- genre (email, narrative, descriptive, argumentative, report)
- process (brainstorming, drafting, revising, editing)
- mechanics (punctuation, capitalization, spelling)
- cohesion_and_coherence

**Reading skills:**
- expeditious_reading (skimming, scanning)
- careful_reading (detail, inference, critical)
- vocabulary_from_context
- text_structure_recognition
- extensive_vs_intensive

---

## PART 3: L1 INTERFERENCE — FULL DATA IN L1 FILES

### 3A. STRUCTURE

Add a new top-level key `skill_interference` to each L1 interference file, following the EXACT same pattern as `grammar_points`:

```yaml
# In portuguese_interference.yaml (alongside existing grammar_points)

skill_interference:
  speaking:
    - skill: turn_taking
      interference_patterns:
        - pattern: Overlapping speech perceived as interrupting
          example_portuguese: "(overlapping) Mas eu acho que—"
          example_gloss: "(overlapping) But I think that—"
          example_wrong: "(interrupting partner) But I think that—"
          example_correct: "(waiting for pause) Can I add something? I think that—"
          explanation: >
            Portuguese conversation tolerates more overlapping speech than
            English. Portuguese speakers may be perceived as interrupting
            when they are following their L1 norm of showing engagement.
          frequency: 3
          persistence: 3
          communicative_impact: 2
        - pattern: Using "né?" as a turn-taking filler
          example_portuguese: "Eu acho isso, né?"
          example_gloss: "I think this, right?"
          example_wrong: "I think this, né?"
          example_correct: "I think this, right?" / "Don't you think?"
          explanation: >
            "Né?" is a Brazilian Portuguese tag used to seek agreement and
            manage turns. Students may transfer it directly to English as
            "né?" which English speakers won't understand.
          frequency: 4
          persistence: 2
          communicative_impact: 3
      why_it_happens: >
        Portuguese conversational norms differ from English in overlap
        tolerance and turn-management strategies. Brazilian Portuguese
        in particular uses more simultaneous speech and different
        back-channeling patterns.
      teacher_tips:
        how_explain: >
          Record a Portuguese conversation and an English conversation.
          Play both. Ask students: "What differences do you notice?"
          Elicit: overlap frequency, pause length, back-channeling.
        where_to_start: >
          Start with awareness of differences. Then practice English
          turn-taking signals explicitly.
        sequencing: >
          Week 1: Awareness (recordings, contrastive analysis).
          Week 2: Signal identification (yielding, holding, taking).
          Week 3: Controlled practice (scripted conversations).
          Week 4: Freer practice (discussion tasks with feedback).
        exercises:
          - name: Overlap Count
            type: listening_task
            description: >
              Students listen to an English conversation and count the
              number of overlaps. Compare with a Portuguese recording.
            duration: 10
          - name: Turn-Taking Script
            type: role_play
            description: >
              Students practice a conversation using a script with
              turn-taking signals marked. Gradually remove the script.
            duration: 15
      sources: &portuguese_speaking_sources
        - "Goh & Burns (2012) Teaching Speaking, Cambridge, Chapter 6"
        - "Thornbury (2005) How to Teach Speaking, Pearson, Chapter 5"
      source_count: 2
      source_type: literature
      frequency: 3
      persistence: 3
      communicative_impact: 2
      flagged: false
      tier: 1
      individually_assessed: true
      assessment: Expert-evaluated for Portuguese L1 speaking interference
      notes: >
        Portuguese overlap tolerance is the most documented speaking
        interference. Back-channeling differences are also significant.
      source_rank: 1
      citations:
        - claim: Portuguese overlap tolerance differs from English
          source: "Goh & Burns (2012) Teaching Speaking, Cambridge University Press"
          location: "Chapter 6: Interactional competence"
          tier: 1

    - skill: pronunciation_segmentals
      interference_patterns:
        - pattern: /θ/ → /t/ or /s/ substitution
          example_portuguese: "Eu tenho três livros"
          example_gloss: "I have three books"
          example_wrong: "I have tree books" / "I have sree books"
          example_correct: "I have three books" /θriː/
          explanation: >
            Portuguese has no /θ/ sound. Students substitute the closest
            Portuguese sound: /t/ (dental stop) or /s/ (fricative).
            The /t/ substitution is more common in Brazilian Portuguese.
          frequency: 5
          persistence: 4
          communicative_impact: 2
        - pattern: /ð/ → /d/ or /z/ substitution
          example_portuguese: "Eu gosto disso"
          example_gloss: "I like this"
          example_wrong: "I like dis" / "I like zis"
          example_correct: "I like this" /ðɪs/
          explanation: >
            Portuguese has no /ð/ sound. Students substitute /d/ or /z/.
          frequency: 5
          persistence: 4
          communicative_impact: 2
        - pattern: Final /m/ and /n/ nasalization
          example_portuguese: "Bom dia"
          example_gloss: "Good morning"
          example_wrong: "I amm goingg" (nasalized final consonants)
          example_correct: "I am going" (no nasalization on final /m/ or /g/)
          explanation: >
            Portuguese nasalizes vowels before /m/ and /n/. Students may
            transfer this to English, producing nasalized final consonants
            that sound unnatural.
          frequency: 3
          persistence: 3
          communicative_impact: 1
      # ... (same rich structure as grammar interference)

  listening:
    - skill: connected_speech
      interference_patterns:
        - pattern: Difficulty perceiving reduced vowels (schwa)
          example_audio: "I can't believe it" → /aɪ kænʔ bəˈliːv ɪt/
          example_wrong: Student hears "I can believe it" (misses the reduced /ə/ in "can't")
          example_correct: Student recognizes "can't" vs "can" through context and reduced vowel
          explanation: >
            Portuguese is syllable-timed with clear vowel pronunciation.
            English schwa /ə/ is nearly inaudible to Portuguese listeners.
            This causes comprehension failures with function words.
          frequency: 5
          persistence: 4
          communicative_impact: 4
        - pattern: Difficulty with consonant cluster reduction
          example_audio: "last time" → /læs taɪm/ (t dropped)
          example_wrong: Student expects to hear /læst taɪm/ and misses the word
          example_correct: Student recognizes the reduced form
          explanation: >
            Portuguese has simpler syllable structures (CV preferred).
            English consonant clusters, especially with reductions, are
            difficult for Portuguese listeners to parse.
          frequency: 4
          persistence: 3
          communicative_impact: 3
      # ... (same rich structure)

  writing:
    - skill: paragraph_structure
      interference_patterns:
        - pattern: Long, elaborate sentences with multiple embeddings
          example_portuguese: "O homem, que era muito alto e que tinha um chapéu grande, que era vermelho, andou..."
          example_gloss: "The man, who was very tall and who had a big hat, which was red, walked..."
          example_wrong: "The man, who was very tall and who had a big hat, which was red, walked..."
          example_correct: "The tall man wore a big red hat. He walked..."
          explanation: >
            Portuguese writing style favors longer sentences with multiple
            relative clauses. English academic writing prefers shorter,
            clearer sentences. Portuguese students produce English paragraphs
            that are grammatically correct but stylistically overloaded.
          frequency: 3
          persistence: 3
          communicative_impact: 2
        - pattern: Using "and" to connect ideas instead of subordination
          example_portuguese: "Ele chegou e sentou e começou a falar"
          example_gloss: "He arrived and sat and started to speak"
          example_wrong: "He arrived and sat down and started to speak"
          example_correct: "When he arrived, he sat down and started speaking."
          explanation: >
            Portuguese favors coordination ("and") over subordination.
            English academic writing expects more complex sentence structures
            with subordinate clauses.
          frequency: 4
          persistence: 3
          communicative_impact: 2
      # ... (same rich structure)

  reading:
    - skill: skimming
      interference_patterns:
        - pattern: Slower reading speed due to syllable-by-syllable decoding
          example_wrong: Student reads every word carefully, cannot skim effectively
          example_correct: Student moves eyes rapidly, focuses on key words
          explanation: >
            Portuguese reading instruction emphasizes careful decoding.
            Portuguese readers may transfer this careful approach to English,
            making skimming difficult. They need explicit instruction that
            skimming means NOT reading every word.
          frequency: 3
          persistence: 2
          communicative_impact: 2
      # ... (same rich structure)
```

---

## PART 4: POPULATION STRATEGY

### 4A. PRIORITY ORDER

**Phase 0: Foundation** (Week 1)
- Create directories, types, loaders, validation script
- Build 2 sample files per skill (8 total) for testing
- Integrate tools and system prompt
- Test end-to-end

**Phase 1: Speaking MVP** (Weeks 2-3) — SHIP FIRST
- 8 speaking topics with FULL CCQs, sub-skills, common errors, activities
- L1 skill interference for top 5 L1s (PT, ES, JA, AR, KO)
- **Ship to production**

**Phase 2: Listening MVP** (Weeks 3-4)
- 8 listening topics
- **Ship to production**

**Phase 3: Expansion** (Weeks 4-6)
- Remaining speaking + listening topics
- L1 skill interference for all 31 languages

**Phase 4: Writing** (Weeks 6-8)
- 20 writing topics

**Phase 5: Reading** (Weeks 8-10)
- 20 reading topics

**Phase 6: Final Audit** (Week 11)
- Full audit of all new content

### 4B. SPEAKING MVP — 8 Topics

1. `turn_taking` — Conversation management
2. `pronunciation_segmentals` — Individual sounds by L1
3. `pronunciation_suprasegmentals` — Stress, rhythm, intonation
4. `functional_requests` — Making and responding to requests
5. `functional_opinions` — Expressing and asking for opinions
6. `discussion_skills` — Structured discussion participation
7. `fluency_development` — Building speaking fluency
8. `back_channeling` — Showing you are listening

### 4C. LISTENING MVP — 8 Topics

1. `listening_for_gist` — Understanding main ideas
2. `listening_for_detail` — Understanding specific information
3. `connected_speech` — Linking, elision, assimilation, weak forms
4. `word_stress_recognition` — Identifying stressed syllables
5. `note_taking` — Taking notes from spoken English
6. `inferring_from_context` — Guessing meaning while listening
7. `listening_strategies` — Pre/during/post listening strategies
8. `understanding_different_accents` — Exposure to variety

### 4D. QUALITY PROCESS PER FILE

For EACH topic file, following the grammar DB process:

1. **Research** (30-60 min): Consult primary sources
2. **Concept definition** (30 min): Write core concept, what it's not, contrast
3. **CCQs** (30 min): Write 3-5 concept checking questions with answers and purpose
4. **Teaching procedure** (30 min): Step-by-step how to teach it
5. **Sub-skills** (30 min): Detailed breakdown with examples
6. **Contexts of use** (20 min): Where/when this skill is used
7. **Phonetics** (20 min, if applicable): Pronunciation issues by L1
8. **Activities** (20 min): 2-3 recommended activities
9. **Sources** (10 min): 5-tier source list
10. **Common errors** (30 min): Errors by L1 group with corrections and explanations
11. **Register notes** (15 min): Formal/informal variations
12. **L1 interference summary** (15 min): Brief summary for all 31 languages

Total: ~4-5 hours per file. Speaking MVP (8 files): ~32-40 hours.

### 4E. WHAT NOT TO DO

1. NEVER use scripts to generate content
2. NEVER skip CCQs — they are the most important teaching tool
3. NEVER skip L1 groups in common errors
4. NEVER use placeholder content
5. NEVER skip sources — all 5 tiers required

---

## PART 5: APP CHANGES

### 5A. NEW DATA LOADERS

```
src/lib/data/loadReadingSkills.ts
src/lib/data/loadWritingSkills.ts
src/lib/data/loadListeningSkills.ts
src/lib/data/loadSpeakingSkills.ts
```

### 5B. NEW AI TOOLS

```typescript
getSkillTopic: {
  description: >
    Get skill topic data (reading/writing/listening/speaking).
    Returns concept definition, CCQs, teaching procedure, sub-skills,
    common errors, activities, and sources. Use when teacher mentions
    a skill-based class.
  inputSchema: z.object({ id: z.string() }),
}
searchSkillTopics: {
  description: >
    Search skill topics by skill type, level, category, or keyword.
  inputSchema: z.object({
    skill: z.enum(["reading", "writing", "listening", "speaking"]).optional(),
    level: z.string().optional(),
    category: z.string().optional(),
    query: z.string().optional(),
  }),
}
```

### 5C. SYSTEM PROMPT CHANGES

**Skill detection:**
- Explicit: "speaking class," "reading lesson," "listening practice," "writing workshop"
- Implicit: "conversation class," "pronunciation help," "essay writing," "understanding lectures"
- Grammar: "present perfect," "passive voice"
- Default: grammar mode

**Skill mode flow:**
- Step S1: searchSkillTopics → Step S2: getSkillTopic → Step S3: Share L1 insights FROM skill topic → Step S4: Activities → Step S5: Summary → Step S6: Generate

**CCQ emphasis:**
- When teaching skill topics, the AI should ALWAYS suggest CCQs to the teacher
- "Here are some CCQs you can use to check understanding: [list CCQs from the skill topic]"

### 5D. GENERATEBUNDLE CHANGES

New fields: `skillTopic`, `skill`

**MVP**: Generate lesson plans only (text-based). Each lesson plan includes:
- Warm-up activity
- Main teaching procedure (with CCQs)
- Practice activities (controlled → freer)
- Cool-down
- Teacher notes with L1-specific tips

### 5E. FEATURE FLAG

`ENABLE_SKILL_MODE=true` env var. When false, skill tools not registered.

---

## PART 6: EXECUTION ROADMAP

### Week 1: Foundation
- Create directories, types, loaders, validation
- Build 2 sample files per skill
- Integrate tools and prompt
- Test end-to-end

### Week 2: Speaking MVP — Content
- 8 speaking topics with FULL CCQs, sub-skills, errors, activities
- L1 skill interference for top 5 L1s

### Week 3: Speaking MVP — Ship
- Backend generation for speaking lesson plans
- Integration test
- **Ship to production**

### Week 4: Listening MVP
- 8 listening topics
- **Ship to production**

### Weeks 5-6: Expansion
- Remaining speaking + listening topics
- L1 skill interference for all 31 languages

### Weeks 7-8: Writing
- 20 writing topics

### Weeks 9-10: Reading
- 20 reading topics

### Week 11: Final Audit
- Full audit of all new content

---

## APPENDIX A: LESSONS FROM GRAMMAR DB PROJECT

What we did right (replicate this):
- CCQs were the backbone of every grammar file — do the same for skills
- Common errors by L1 group were extremely valuable — do the same
- 5-tier source system gave authority — do the same
- Multi-pass auditing caught errors — do the same

What we did wrong (avoid this):
- Script-generated content was garbage — NO scripts for skill content
- LLM-only data was unreliable — Every claim must be sourced
- Incomplete L1 coverage — All 31 languages required

---

END OF DOCUMENT — Version 1.0
