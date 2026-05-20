# CogniESL — Backlog Analysis & Implementation Plan

> Generated: 2026-05-19
> Compares `forge/docs/PRODUCT_BACKLOG.md` against current CogniESL codebase state.

---

## Executive Summary

The CogniESL app has a **solid foundation**: a single-agent AI material generator that produces PPTX slides, DOCX/PDF worksheets, and activity guides with L1-specific error targeting. The backlog contains **~50+ feature requests** from 14+ research files. After deduplication and cross-referencing with existing capabilities, the unique actionable features are:

- **Already built (core):** Lesson slides, worksheets, activity guides, L1 Oracle sections
- **Quick wins (0.5–1 session each):** ~12 features that reuse existing pipelines
- **Medium effort (1–2 sessions):** ~6 features needing new prompt templates or moderate new code
- **Heavy lifts (3+ sessions):** ~4 features requiring significant new architecture

---

## 1. Deduplicated Unique Features

The backlog has massive duplication across research runs. Below is the deduplicated feature set grouped by theme:

### A. Content Generation Formats

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **Slides (PPTX)** | Core product | ✅ Yes | — |
| **Worksheets (DOCX/PDF)** | Core product | ✅ Yes | — |
| **Activity Guides** | Core product | ✅ Yes | — |
| **Flashcards (PDF)** | P0.1, P0.10 | ❌ No | Low |
| **Role-Play Cards** | P0.2 | ❌ No | Low |
| **Assessments/Quizzes** | P0.3, P2.51 | ❌ No | Medium |
| **Lesson Plans (structured)** | P1.3, P0.6, P0.8 | ⚠️ Partial (basic guide exists) | Low |
| **Homework PDFs** | P1.1 | ❌ No | Low (reuse assessment pipeline) |
| **Micro-Lessons (5-min warmups)** | P2.32 | ❌ No | Low |
| **Ready-Made Material Packs** | P2.30, P0.12 | ❌ No | Low |
| **Parent Communication Packs** | P2.35 | ❌ No | Low |
| **Classroom Management Toolkit** | P2.34 | ❌ No | Low |
| **Video Lesson Support** | P2.4, P2.54 | ❌ No | Medium |

### B. Customization & Adaptation

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **Level Differentiation** | P0.5, P1.6, P1.9 | ❌ No | Low |
| **Rapid-Customization Templates** | P2.31 | ❌ No | Medium |
| **L1-Specific Error Callouts** | P1.2, P0.9 | ⚠️ Partial (in slides only) | Low |
| **Adaptive Content Carousel** | P1.6 | ❌ No | Medium |

### C. Teaching Modes

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **Conversation Lesson Mode (instant)** | P0.4 | ❌ No | Low |
| **Business English Scenario Library** | P1.4 | ❌ No | Low |
| **Grading Assistant** | P2.33, P0.7 | ❌ No | Medium |

### D. Platform & Distribution

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **Interactive Digital Lesson Viewer** | P2.1 | ❌ No | High |
| **LMS Connector** | P1.8 | ❌ No | Medium |
| **Mobile-Optimized UI** | P2.44 | ❌ No | Medium |
| **Resource Marketplace Integration** | P1.7 | ❌ No | High |

### E. Analytics & Admin

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **Student Error Tracking** | P2.2 | ❌ No | High |
| **Usage Analytics Dashboard** | P2.55, P2.49 | ❌ No | High |
| **Admin Dashboard** | P2.50 | ❌ No | High |
| **Institutional Licensing** | P2.3 | ❌ No | Very High |

### F. UX & Onboarding

| Feature | Backlog IDs | Already Built? | Effort |
|---------|-------------|----------------|--------|
| **AI Onboarding Flow** | P2.56 | ❌ No | Low |
| **Pricing/ROI Calculator** | P0.11 | ❌ No | Low |
| **Material Quality Filter** | P2.53 | ❌ No | Medium |
| **Professional Development Hub** | P2.52 | ❌ No | Medium |

---

## 2. What Already Exists (and What It Enables)

### Core Agent Infrastructure
- **Single-agent architecture** with 30+ tools — adding new output formats is primarily a prompt template change
- **Session management** — already handles multi-turn conversations, enabling "make harder/easier" follow-ups
- **Database search tools** — grammar (300 points), L1 interference (32 languages), activities (218)

### Output Generation Pipeline
- **PPTX slides** — full pipeline from HTML templates → python-pptx → downloadable files
- **DOCX worksheets** — HTML → python-docx with answer keys
- **PDF conversion** — WeasyPrint for printable output
- **File delivery** — organized output directory, project summary, teacher guide

### L1 Intelligence
- **L1 Oracle sections** already in slides — the callout box pattern (P1.2, P0.9) just needs to be extended to worksheets/assessments
- **32 L1 databases** — ready to power any L1-aware feature

### What This Means for Implementation
The **heavy infrastructure is already built**. Most P0/P1 features are:
1. New prompt templates telling the agent to generate a different output format
2. Reuse of existing DOCX/PDF generation pipelines
3. Minor UI additions for mode switching

---

## 3. Recommended Implementation Phases

### Phase 1: Quick Wins (Week 1–2)
*High value, low effort. Reuse existing pipelines. No new infrastructure.*

| Priority | Feature | Rationale | Est. Effort |
|----------|---------|-----------|-------------|
| **1** | **P0.4 — Conversation Lesson Mode** | Biggest addressable market (online 1-on-1 teachers). Just a new prompt template + mode switch. | 0.5 session |
| **2** | **P0.1 — Flashcard Generation** | #1 teacher pain point. Reuse DOCX pipeline, output a grid layout PDF. | 1 session |
| **3** | **P0.5 — Level Differentiation** | Competitive differentiator. Agent already has level context; just needs "regenerate at level X" logic. | 1 session |
| **4** | **P1.3 — Structured Lesson Plan Output** | Already partially built (TEACHER_GUIDE.txt). Formalize the template. | 0.5 session |
| **5** | **P1.1 — Homework PDF Generation** | Reuse assessment/worksheet pipeline, shorter output. | 0.5 session |
| **6** | **P2.32 — Micro-Lesson Generator** | Same as lesson mode but constrained to 5-min activities. | 0.5 session |
| **7** | **P2.56 — AI Onboarding Flow** | Reduces churn. Static content + guided first session. | 0.5 session |

**Phase 1 total: ~5 sessions. Delivers 7 backlog items.**

### Phase 2: Core Differentiators (Week 3–4)
*High value, medium effort. New templates + moderate new logic.*

| Priority | Feature | Rationale | Est. Effort |
|----------|---------|-----------|-------------|
| **8** | **P0.3 — Assessment Generation** | #2 teacher pain point. Needs CEFR alignment + answer key generation. Reuse DOCX pipeline. | 2 sessions |
| **9** | **P0.2 — Role-Play Card Generation** | BE teachers' #1 pain point, high WTP ($20-50/mo). New card layout template. | 1 session |
| **10** | **P1.2 — L1 Error Callouts in All Outputs** | Extends existing L1 Oracle to worksheets/assessments. Prompt template change. | 1 session |
| **11** | **P1.4 — Business English Scenario Library** | YAML templates + prompt integration. Enables P0.2 reuse. | 1 session |
| **12** | **P2.30 — Ready-Made Material Packs** | Pre-generate bundles for common topics. One-click download. | 1 session |

**Phase 2 total: ~6 sessions. Delivers 5 backlog items (including the highest-WTP features).**

### Phase 3: Enhanced UX (Week 5–6)
*Medium value, medium effort. UI improvements + new interaction patterns.*

| Priority | Feature | Rationale | Est. Effort |
|----------|---------|-----------|-------------|
| **13** | **P2.31 — Rapid-Customization Templates** | UI for post-generation edits (swap vocab, change difficulty). Needs frontend work + regeneration API. | 2 sessions |
| **14** | **P2.33 — Grading Assistant** | Auto-grade short answers against rubric. Needs rubric template + comparison logic. | 2 sessions |
| **15** | **P1.8 — LMS Connector** | Export to Google Classroom/Canvas. API integration work. | 1 session |
| **16** | **P2.44 — Mobile-Optimized UI** | 28% of teachers use tablets. Responsive design pass. | 1 session |

**Phase 3 total: ~6 sessions. Delivers 4 backlog items.**

### Phase 4: Platform Expansion (Week 7+)
*Higher effort, longer-term value. New architecture needed.*

| Priority | Feature | Rationale | Est. Effort |
|----------|---------|-----------|-------------|
| **17** | **P2.1 — Interactive Digital Lesson Viewer** | Competitive gap vs ESL Brains. Needs frontend SPA + slide rendering. | 3+ sessions |
| **18** | **P2.2 — Student Error Tracking** | Needs persistent storage (database) + student profiles. | 3+ sessions |
| **19** | **P2.55 — Usage Analytics Dashboard** | Needs event tracking + dashboard UI. | 2 sessions |
| **20** | **P2.3 — Institutional Licensing** | Auth, accounts, billing. Full platform feature. | 5+ sessions |

**Phase 4 total: ~13+ sessions. Delivers 4 backlog items.**

---

## 4. Features to Deprioritize (For Now)

| Feature | Backlog IDs | Reason |
|---------|-------------|--------|
| **Video Lesson Support** | P2.4, P2.54 | Needs YouTube API + content analysis. Low teacher demand vs effort. |
| **Resource Marketplace** | P1.7 | Legal/copyright complexity. Build own library first. |
| **PD Hub** | P2.52 | Content creation effort. Partner with existing PD providers later. |
| **Budget Subscription Tier** | P2.45 | Business decision, not engineering. Decide after product-market fit. |
| **Material Quality Filter** | P2.53 | Premature. Need usage data first. |
| **Admin Dashboard** | P2.50 | Only relevant for institutional tier (Phase 4). |

---

## 5. Risk Assessment

### Low Risk (Phase 1–2)
- All features reuse existing agent + document generation infrastructure
- No new dependencies or external APIs needed
- Prompt template changes are easily reversible

### Medium Risk (Phase 3)
- LMS integration depends on third-party API stability
- Grading assistant quality depends on rubric design
- Customization UI needs careful UX to avoid complexity

### High Risk (Phase 4)
- Student tracking requires persistent storage (currently stateless)
- Interactive viewer is a significant frontend undertaking
- Institutional licensing requires auth system (currently session-based)

---

## 6. Key Architectural Decisions Needed

1. **Storage:** Phases 1–2 work with current stateless file output. Phase 4 needs a database (SQLite for local, PostgreSQL for cloud).
2. **CEFR Alignment:** Assessment generation (P0.3) needs CEFR "can-do" descriptors added to grammar YAML files.
3. **Output Format:** Flashcards and role-play cards need new HTML templates but reuse existing DOCX/PDF converters.
4. **Mode Switching:** Conversation Lesson Mode (P0.4) needs a way to signal "instant generation" vs. "conversational gathering" — likely a prompt prefix or session flag.

---

## 7. Suggested Immediate Next Step

**Start with Phase 1, Feature 1: Conversation Lesson Mode (P0.4)**

Why:
- **0.5 session effort** — just a new prompt template
- **Largest addressable market** — online 1-on-1 teachers (Preply, Cambly, iTalki)
- **Validates the "instant generation" pattern** that micro-lessons and material packs reuse
- **No new infrastructure** — works with current agent + output pipeline
- **Competitive gap** — no competitor offers instant lesson generation from a single prompt

Implementation:
1. Add a "Quick Lesson" button to the UI that sets `mode=instant` in the session
2. Add a prompt template for one-shot lesson generation (discussion questions + vocabulary + homework)
3. Agent generates all materials in a single pass without requirement-gathering back-and-forth
