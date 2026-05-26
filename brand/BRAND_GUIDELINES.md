# CogniESL Brand Guidelines

**Version:** 1.0  
**Last updated:** 2026-05-25  
**Logo files:** [logos/](logos/)

---

## 1. The Concept

CogniESL exists to make the invisible visible — specifically, the L1 interference patterns that cause specific errors in specific students. The core moment of the product is recognition: a teacher sees an L1 Oracle slide and thinks *"that's exactly what my students do."*

The logo encodes this in a single mark.

**The C-arc** is the letter C in CogniESL, drawn as a bold correction arc. The arc body (teal) represents the structure of language — something that wraps around, contains, and guides. The green uptick at the top is the correction: the moment an error is caught and redirected upward. Together, they are the product in a single gesture.

The mark and the type are inseparable. The arc *is* the C in CogniESL — you cannot read the wordmark without it.

---

## 2. The Mark

### Geometry

The C-arc is constructed from a single SVG arc path and a short diagonal line:

```
Arc:    M 45,50 A 18,18 0 1,1 45,21
        stroke-width: 9  stroke-linecap: round
        
Uptick: x1=45 y1=21  →  x2=57 y2=9
        stroke-width: 8  stroke-linecap: round
```

The arc spans approximately 260° of a circle with radius 18. It opens to the right, placing the body on the left — the classic C letterform. The uptick emerges from the top of the arc and extends above the cap line, pointing upper-right. This is the only element that breaks above the cap height, making it the most distinctive feature at small sizes.

**Never redraw the arc freehand.** Always use the SVG files in `logos/`. The geometry is locked.

### The wordmark

The wordmark is the arc-C followed by `ogniESL`, set in system-ui (or Helvetica Neue / Arial as fallback), weight 500. The `ESL` portion is set in the accent green. No separate symbol exists — the arc is the first letter.

```
Font:    system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif
Weight:  500 (medium) for all characters
Size:    38px in the standard SVG (scale proportionally)
"ogni":  Brand teal
"ESL":   Accent green, letter-spacing: 2
```

> **Note on text-to-paths:** The SVG files use live text. For production use in print, presentations, or design tools, convert text to outlines in Inkscape or Illustrator before exporting. This prevents font substitution on systems that don't have system-ui.

---

## 3. Colors

### Primary palette

| Role | Name | Light bg hex | Dark bg hex |
|------|------|-------------|-------------|
| Arc body / "ogni" | Brand Teal | `#0b7272` | `#10cccc` |
| Uptick / "ESL" | Accent Green | `#1baa6e` | `#22e088` |

### Usage rules

- **Light backgrounds** (white, off-white, light gray): use `#0b7272` and `#1baa6e`.
- **Dark backgrounds** (navy, charcoal, black): use `#10cccc` and `#22e088`.
- **Mono white**: use `#ffffff` for both elements. For use on the brand teal, on dark slide backgrounds, or on photography.
- **Mono teal**: use `#0b7272` for both elements. For single-color print, embossing, or contexts where green is unavailable.

### Slide system colors (inherited from the L1 Oracle slides)

The correction color system in slides echoes the logo intentionally:

| Slide use | Color |
|-----------|-------|
| Error / wrong example | `#e74c3c` (red) |
| Correction / correct example | `#27ae60` (green, close to Accent Green) |
| Slide accents / headings | `#0b7272` (Brand Teal) |

This is not an accident. The logo's teal-to-green arc mirrors the slide's red-to-green correction arc. Teachers who internalize the logo will recognize the visual language in the slides.

---

## 4. Logo Variants

### File inventory

| File | Use |
|------|-----|
| `cogniesl-wordmark-light.svg` | Default. Light backgrounds, marketing site, email header, presentations. |
| `cogniesl-wordmark-dark.svg` | Dark backgrounds, dark-mode UI, dark slide themes. |
| `cogniesl-wordmark-white.svg` | Mono white. On teal fill, photography, colored backgrounds. |
| `cogniesl-wordmark-mono.svg` | Mono teal. Single-color print, embossing, fax, B&W. |
| `cogniesl-symbol-light.svg` | App icon, favicon, slide watermark (light bg), social avatar. |
| `cogniesl-symbol-dark.svg` | App icon on dark, dark-mode favicon. |
| `cogniesl-symbol-white.svg` | Symbol on colored/teal backgrounds. Slide watermark on teal panels. |
| `cogniesl-symbol-mono.svg` | Symbol single-color print. |

### Decision guide

```
Background is white or light gray?     → wordmark-light or symbol-light
Background is dark / navy / black?     → wordmark-dark or symbol-dark
Background is teal (#0b7272)?          → wordmark-white or symbol-white
Need single color only?                → wordmark-mono or symbol-mono
Need the full name visible?            → wordmark variant
Space is small (icon, watermark)?      → symbol variant
```

---

## 5. Clear Space

The minimum clear space around the wordmark is equal to the height of the arc symbol on all sides. At the standard 62px height, clear space = 62px on each side.

For the symbol alone, minimum clear space = the symbol's own height on all sides.

**Never place the logo:**
- Touching another element, border, or text
- On a background with insufficient contrast (test with the WebAIM contrast checker)
- Overlapping a busy photograph without a semi-transparent backing

---

## 6. Minimum Sizes

| Format | Minimum size |
|--------|-------------|
| Wordmark (digital) | 120px wide |
| Wordmark (print) | 30mm wide |
| Symbol (digital) | 20px × 20px |
| Symbol (print) | 6mm × 6mm |

Below these sizes, the uptick and letter spacing become illegible. Use the symbol-only variant for tight spaces.

---

## 7. Application in CogniESL

### Slide watermark

Use `cogniesl-symbol-light.svg` or `cogniesl-symbol-white.svg` depending on slide background color. Place in the bottom-right corner of every slide at 20–24px height. Opacity: 35% for Pro/Founding tier, 65% for Free tier.

**Do not** place the watermark over text or critical content areas.

### Closing brand slide

The last slide of every generated deck is the CogniESL brand slide. It uses:
- `cogniesl-wordmark-light.svg` on a white background, centered
- Tagline below: *"L1-aware teaching materials, made in minutes."*
- URL: `cogniesl.com`
- Background: white with a subtle teal accent strip at the bottom edge

### Delivery email header

Use `cogniesl-wordmark-light.svg` in the email header, left-aligned, at approximately 160px wide. The email background is white.

### App navbar

The navbar already uses the wordmark. Keep it at its current size. If the navbar goes dark, switch to `cogniesl-wordmark-dark.svg`.

### App icon / favicon

Use `cogniesl-symbol-light.svg`. For favicon: render at 32×32px and 16×16px. For App Store / PWA icon: render at 512×512px on a white or teal (#0b7272) background with the symbol centered and padded.

### Social media avatar

Use `cogniesl-symbol-light.svg` on a white square background, centered with padding equal to 15% of the square's side. For profile photos that require a circle crop, ensure the symbol sits well within the safe area.

---

## 8. Typography (outside the logo)

The logo uses system-ui. The app and marketing site use the same stack. For documentation, slides, and brand materials, the following rules apply:

| Use | Specification |
|-----|--------------|
| Headings | system-ui, weight 500, Brand Teal (`#0b7272`) |
| Body text | system-ui, weight 400, near-black (`#1a2332`) |
| Accent / CTA | Accent Green (`#1baa6e`) for positive actions and highlights |
| Code / mono | Monospace fallback stack |

Do not introduce additional typefaces without updating this document.

---

## 9. What Not To Do

- **Do not** stretch, skew, or rotate the logo.
- **Do not** change the arc color or uptick color independently of this document.
- **Do not** redraw the arc. The geometry is exact — use the SVG files.
- **Do not** use the wordmark without the arc. `ogniESL` without the C-arc is not the logo.
- **Do not** place the white variant on a white background.
- **Do not** add drop shadows, glows, or outlines to the logo.
- **Do not** enclose the logo in a shape (circle, box) unless it is an app icon context.
- **Do not** use the red correction color (`#e74c3c`) in the logo — that is a slide-system color only.
- **Do not** set the `ESL` portion in teal — it must always be the accent green (or white in mono-white contexts).

---

## 10. File Naming Convention

```
cogniesl-[element]-[variant].svg

element:  wordmark | symbol
variant:  light | dark | white | mono
```

Examples: `cogniesl-wordmark-light.svg`, `cogniesl-symbol-dark.svg`

When exporting rasterized versions (PNG) for specific sizes, append the pixel dimension:

```
cogniesl-symbol-light-512.png
cogniesl-symbol-light-32.png
cogniesl-wordmark-light-400w.png
```

---

## 11. Future Work

- [ ] Convert text to outlines in all wordmark SVGs (requires Inkscape/Illustrator)
- [ ] Produce PNG exports at standard sizes (16, 32, 64, 128, 256, 512px for symbol)
- [ ] Create favicon.ico from symbol-light at 32px and 16px
- [ ] Design the closing brand slide HTML template (Track 3 V2 in ROADMAP.md)
- [ ] Implement slide watermark in HTML presenter (Track 3 V3 in ROADMAP.md)
- [ ] Lock final brand colors once app is styled end-to-end

---

*For the project plan, see [ROADMAP.md](../ROADMAP.md). For slide design rules, see [agent/slides_tools/html_writer_instructions.md](../agent/slides_tools/html_writer_instructions.md).*
