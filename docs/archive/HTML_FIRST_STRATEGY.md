# CogniESL — HTML-First Presentation Strategy

**Decision date:** 2026-05-25  
**Status:** Implemented  
**Related:** [DECOUPLED_PPTX_SPEC.md](DECOUPLED_PPTX_SPEC.md)

---

## The Decision

HTML is the primary presentation format for CogniESL materials. PPTX is a secondary opt-in format for teachers who explicitly need it for compatibility reasons.

This is not a workaround — it is a deliberate product direction.

---

## Why HTML-First

**CogniESL's competitive advantage is visual quality.** Materials that look like a design agency made them, not like a teacher spent an afternoon in PowerPoint. That advantage only exists in HTML.

When slides were designed with PPTX export in mind, the agent was implicitly constrained:
- Avoid overlapping elements (PPTX positioning breaks)
- Avoid CSS animations (PPTX has no equivalent)
- Avoid complex gradients (flattened on export)
- Stick to layouts that convert cleanly

HTML-first removes all of those constraints. The agent can use any CSS — entrance animations, slide transitions, multi-layer backgrounds, gradient text, custom typography, SVG overlays — and the teacher sees exactly what was designed.

**PPTX export is a conversion with loss.** It flattens CSS into static shapes and strips animations. Every teacher who uses the PPTX is getting a worse version of what was built. HTML-first means the teacher gets the real thing.

---

## What Changed

### Primary deliverable: offline HTML bundle

`BuildOfflineBundle` generates a single `.html` file containing all slides. It:
- Inlines Google Fonts and Font Awesome as base64 data URIs (no internet needed to render)
- Inlines all local images as base64 data URIs
- Wraps slides in a navigation shell with:
  - Prev/next buttons + keyboard arrow navigation
  - Slide counter (3 / 15)
  - Fullscreen toggle (F key or button)
  - Speaker notes panel (N key or button)
  - CogniESL branding in the nav bar
- Each slide runs in an isolated iframe (srcdoc) — no CSS conflicts between slides
- Single `.html` file, ~2–5 MB, opens in any browser with a double-click

### Secondary deliverable: PPTX (opt-in only)

`BuildPptxFromHtmlSlides` is still available but no longer called by default. The agent only generates PPTX when the teacher explicitly asks for it ("I need a PowerPoint version" or "I need to share this in PPT format").

In the future, PPTX generation will be rebuilt as a decoupled tool (`BuildSimplePptx`) that generates from structured content data rather than converting from HTML — producing a clean functional presentation without trying to mirror the HTML design. See [DECOUPLED_PPTX_SPEC.md](DECOUPLED_PPTX_SPEC.md).

### Framing in the product

The HTML bundle is positioned as the **premium format**, not as a workaround:

> "Your presentation is in HTML format — this means it keeps all the animations, gradients, and visual design exactly as created. Open it in any browser, press F for fullscreen."

This framing is used in:
- The delivery email (primary download button with inline instructions)
- The agent's closing message after generation
- My Materials download buttons (HTML bundle listed first)

The PPTX, when offered, is framed as "PowerPoint version — simplified layout, works in PowerPoint and Keynote."

---

## Slide Design Is Now Unconstrained

`html_writer_instructions.md` was updated to remove all PPTX-compatibility constraints. The agent is now explicitly encouraged to use:

- **CSS entrance animations** — elements that fade in, slide up, or scale as the slide loads
- **Slide transitions** — smooth cross-fades or slide transitions between sections (handled by the bundle nav shell)
- **Complex layouts** — overlapping elements, asymmetric grids, full-bleed backgrounds
- **Gradient text** — `background-clip: text` for headings
- **SVG elements** — inline decorative SVGs, diagrams, arrows
- **Layered backgrounds** — gradient + pattern + transparency stacks

The design bar is: "Could this appear in a premium Canva template?" If yes, it belongs in a CogniESL slide.

---

## Teacher Workflow

### Online (primary — most teachers)

1. Generation completes → teacher gets email with snapshot preview
2. Teacher clicks "Open Presentation" in email → opens in-app presenter at `/present/[jobId]`
3. OR: teacher goes to My Materials → clicks Present button → same presenter
4. Teacher presses F for fullscreen → teaches class

### Offline (classroom without wifi)

1. Teacher downloads the HTML bundle from My Materials (or email) beforehand
2. Saves to laptop Desktop
3. In classroom: double-click → opens in browser → F for fullscreen → teaches class
4. No internet required — fonts, images, everything is self-contained

### "I need PowerPoint"

Teacher types: "Can I also get this as a PowerPoint?" → agent calls `BuildPptxFromHtmlSlides` → adds PPTX to their materials.

---

## What Was Not Changed

- The in-app HTML presenter (`/present/[jobId]`) — still the primary online viewing experience, unchanged
- The slide HTML source files — still generated as individual `.html` files in `mnt/{project_name}/slides/`
- `BuildPptxFromHtmlSlides` — still in the codebase, just no longer called by default
- All other deliverables (worksheet, activity guide, flashcards, progress tracker) — unchanged

---

## Open Items

- [ ] `BuildSimplePptx` — decoupled PPTX generator from structured content (see spec)
- [ ] Slide transition animations in the bundle nav shell (currently nav shows/hides iframe instantly)
- [ ] Print stylesheet for the bundle (Ctrl+P produces one slide per page)
- [ ] Bundle download from the in-app presenter (the "Download bundle" button should offer the pre-built `.html` file directly)
