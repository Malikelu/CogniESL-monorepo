"""
BuildOfflineBundle — generate a single self-contained HTML presentation file.

Each slide becomes an isolated iframe (srcdoc). Google Fonts, Font Awesome, and all
local images are base64-encoded and inlined — the file works completely offline.

The resulting file includes:
  - Prev/next navigation (buttons + arrow keys)
  - Slide counter
  - Fullscreen toggle (F key)
  - Speaker notes panel (N key)
  - CogniESL branding in the nav bar

Call AFTER all slides are generated and built, BEFORE SnapSlideForEmail and MarkJobComplete.

Output: ./mnt/{project_name}/presentations/{project_name}.html
"""

import base64
import html
import logging
import re
import urllib.request
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

from .slide_file_utils import get_project_dir, list_slide_files

log = logging.getLogger(__name__)

# Chrome UA so Google Fonts returns WOFF2 (not WOFF/TTF)
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
_FONT_CACHE: dict[str, str] = {}  # URL → base64 data URI (module-level cache)


# ── Resource inlining helpers ──────────────────────────────────────────────

def _fetch(url: str, binary: bool = False) -> bytes | str | None:
    """Fetch a URL. Returns bytes if binary=True, str otherwise. None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            return data if binary else data.decode("utf-8", errors="replace")
    except Exception as e:
        log.warning(f"[bundle] Failed to fetch {url}: {e}")
        return None


def _font_data_uri(url: str, mime: str = "font/woff2") -> str:
    """Fetch a font file and return a base64 data URI."""
    if url in _FONT_CACHE:
        return _FONT_CACHE[url]
    data = _fetch(url, binary=True)
    if not data:
        return url  # fallback — leave URL as-is
    b64 = base64.b64encode(data).decode()
    uri = f"data:{mime};base64,{b64}"
    _FONT_CACHE[url] = uri
    return uri


def _inline_google_fonts(css_url: str) -> str:
    """
    Fetch a Google Fonts CSS URL, replace all WOFF2 src URLs with data URIs,
    and return the fully inlined @font-face CSS block.
    """
    css = _fetch(css_url)
    if not css:
        return ""
    # Replace each url(https://fonts.gstatic.com/...) with a data URI
    def replace_font_url(m):
        font_url = m.group(1).strip("'\"")
        return f"url({_font_data_uri(font_url)})"
    css = re.sub(r"url\(([^)]+gstatic\.com[^)]+)\)", replace_font_url, css)
    return css


def _inline_fontawesome(css_url: str) -> str:
    """
    Fetch Font Awesome CSS, replace all font src URLs with data URIs.
    Handles both cdnjs and jsdelivr CDN patterns.
    """
    css = _fetch(css_url)
    if not css:
        return ""
    base = css_url.rsplit("/", 1)[0] + "/"

    def replace_fa_url(m):
        raw = m.group(1).strip("'\"")
        # Strip query strings like ?v=6.5.0
        src_url = raw.split("?")[0]
        if src_url.startswith("http"):
            full_url = src_url
        elif src_url.startswith("../"):
            # Resolve relative to cdnjs base
            parts = css_url.split("/")
            # Go up from /css/all.min.css to /webfonts/
            full_url = "/".join(parts[:-2]) + "/" + src_url[3:]
        else:
            full_url = base + src_url
        # Only inline WOFF2 for size; leave others as-is (browser picks first)
        if "woff2" in src_url.lower() or raw.endswith(".woff2"):
            return f"url({_font_data_uri(full_url)})"
        return m.group(0)

    css = re.sub(r"url\(([^)]+)\)", replace_fa_url, css)
    return css


def _inline_slide_resources(slide_html: str, slide_path: Path) -> str:
    """
    Given a full slide HTML string:
    1. Replace Google Fonts @import/link with inlined @font-face CSS
    2. Replace Font Awesome CDN link with inlined CSS
    3. Replace local <img src="..."> with base64 data URIs
    Returns a self-contained HTML string.
    """
    # --- Google Fonts: @import url('https://fonts.googleapis.com/...') ---
    def replace_gf_import(m):
        url = m.group(1).strip("'\"")
        if "fonts.googleapis.com" not in url:
            return m.group(0)
        inlined = _inline_google_fonts(url)
        return f"/* Google Fonts inlined */\n{inlined}" if inlined else ""

    slide_html = re.sub(
        r"@import\s+url\(['\"]?(https://fonts\.googleapis\.com[^'\")\s]+)['\"]?\)\s*;",
        replace_gf_import,
        slide_html,
    )

    # --- Google Fonts: <link rel="stylesheet" href="https://fonts.googleapis.com/..."> ---
    def replace_gf_link(m):
        url = m.group(1)
        inlined = _inline_google_fonts(url)
        return f"<style>/* Google Fonts inlined */\n{inlined}</style>" if inlined else ""

    slide_html = re.sub(
        r'<link[^>]+href=["\']?(https://fonts\.googleapis\.com[^"\'>\s]+)["\']?[^>]*>',
        replace_gf_link,
        slide_html,
    )

    # --- Font Awesome CDN ---
    def replace_fa_link(m):
        url = m.group(1)
        inlined = _inline_fontawesome(url)
        return f"<style>/* Font Awesome inlined */\n{inlined}</style>" if inlined else m.group(0)

    slide_html = re.sub(
        r'<link[^>]+href=["\']?(https://(?:cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net)[^"\'>\s]+font.awesome[^"\'>\s]+\.css)["\']?[^>]*>',
        replace_fa_link,
        slide_html,
        flags=re.IGNORECASE,
    )

    # --- Local images: <img src="relative/path/..."> ---
    def replace_local_img(m):
        src = m.group(1)
        if src.startswith(("http://", "https://", "data:")):
            return m.group(0)  # external or already inlined
        img_path = (slide_path.parent / src).resolve()
        if not img_path.exists():
            # Try relative to project mnt root
            img_path = (slide_path.parent.parent / src.lstrip("./")).resolve()
        if img_path.exists():
            suffix = img_path.suffix.lower().lstrip(".")
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                    "gif": "image/gif", "svg": "image/svg+xml", "webp": "image/webp"}.get(suffix, "image/png")
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            return m.group(0).replace(m.group(1), f"data:{mime};base64,{b64}")
        return m.group(0)

    slide_html = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']', replace_local_img, slide_html)

    return slide_html


def _extract_speaker_notes(slide_html: str) -> str:
    """Extract data-speaker-notes content from a slide HTML string."""
    m = re.search(r'data-speaker-notes=["\']([^"\']*)["\']', slide_html, re.DOTALL)
    if m:
        return m.group(1)
    # Also try <div class="speaker-notes">...</div>
    m = re.search(r'class=["\']speaker-notes["\'][^>]*>(.*?)</div>', slide_html, re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


# ── Navigation shell template ──────────────────────────────────────────────

_NAV_SHELL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} — CogniESL</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 100%; height: 100%; background: #0b1a1a; overflow: hidden; }}

  /* Slide area */
  #stage {{
    position: fixed;
    top: 0; left: 0; right: 0;
    bottom: 52px;
  }}
  .slide-frame {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border: none;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
  }}
  .slide-frame.active {{
    opacity: 1;
    pointer-events: auto;
  }}

  /* Nav bar */
  #nav {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 52px;
    background: #0b2222;
    border-top: 1px solid #1baa6e33;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    z-index: 100;
    font-family: system-ui, -apple-system, sans-serif;
  }}
  .nav-btn {{
    background: #0b7272;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.15s;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .nav-btn:hover {{ background: #1baa6e; }}
  .nav-btn:disabled {{ opacity: 0.3; cursor: default; background: #0b7272; }}
  #counter {{
    color: #9ca3af;
    font-size: 13px;
    min-width: 60px;
    text-align: center;
    letter-spacing: 0.5px;
  }}
  #brand {{
    position: absolute;
    right: 16px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #6b7280;
  }}
  #brand span {{ color: #0b7272; }}
  #brand em {{ color: #1baa6e; font-style: normal; letter-spacing: 2px; }}

  /* Speaker notes panel */
  #notes-panel {{
    position: fixed;
    bottom: 52px; left: 0; right: 0;
    height: 0;
    overflow: hidden;
    background: #071010;
    border-top: 1px solid #0b7272;
    transition: height 0.2s ease;
    z-index: 50;
  }}
  #notes-panel.open {{
    height: 180px;
  }}
  #notes-content {{
    padding: 14px 20px;
    color: #d1d5db;
    font-size: 13px;
    line-height: 1.65;
    font-family: system-ui, -apple-system, sans-serif;
    overflow-y: auto;
    height: 100%;
    white-space: pre-wrap;
  }}
  #notes-label {{
    position: absolute;
    top: 8px; left: 20px;
    font-size: 10px;
    font-weight: 700;
    color: #0b7272;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }}

  /* Fullscreen: hide nav */
  :fullscreen #nav, :-webkit-full-screen #nav {{
    display: none;
  }}
  :fullscreen #stage, :-webkit-full-screen #stage {{
    bottom: 0;
  }}
  :fullscreen #notes-panel, :-webkit-full-screen #notes-panel {{
    display: none;
  }}

  /* Progress bar */
  #progress {{
    position: fixed;
    top: 0; left: 0;
    height: 2px;
    background: #1baa6e;
    transition: width 0.25s ease;
    z-index: 200;
  }}
</style>
</head>
<body>

<div id="progress"></div>

<div id="stage">
{slide_iframes}
</div>

<!-- Speaker notes -->
<div id="notes-panel">
  <div id="notes-label">Speaker Notes</div>
  <div id="notes-content"></div>
</div>

<!-- Navigation bar -->
<div id="nav">
  <button class="nav-btn" id="btn-prev" onclick="prev()" title="Previous (←)">&#8592; Prev</button>
  <span id="counter">1 / {total}</span>
  <button class="nav-btn" id="btn-next" onclick="next()" title="Next (→)">Next &#8594;</button>
  <button class="nav-btn" onclick="toggleNotes()" title="Toggle notes (N)" id="btn-notes">&#128203; Notes</button>
  <button class="nav-btn" onclick="toggleFullscreen()" title="Fullscreen (F)">&#9974; Full</button>
  <div id="brand"><span>Cogni</span><em>ESL</em></div>
</div>

<script>
  const notes = {notes_json};
  const total  = {total};
  let current  = 0;
  let notesOpen = false;

  const frames   = Array.from(document.querySelectorAll('.slide-frame'));
  const counter  = document.getElementById('counter');
  const progress = document.getElementById('progress');
  const notesEl  = document.getElementById('notes-content');
  const notesPnl = document.getElementById('notes-panel');
  const btnPrev  = document.getElementById('btn-prev');
  const btnNext  = document.getElementById('btn-next');

  function show(n) {{
    frames.forEach((f, i) => f.classList.toggle('active', i === n));
    counter.textContent = (n + 1) + ' / ' + total;
    progress.style.width = ((n + 1) / total * 100) + '%';
    notesEl.textContent = notes[n] || '';
    btnPrev.disabled = n === 0;
    btnNext.disabled = n === total - 1;
    current = n;
  }}

  function next() {{ if (current < total - 1) show(current + 1); }}
  function prev() {{ if (current > 0) show(current - 1); }}

  function toggleNotes() {{
    notesOpen = !notesOpen;
    notesPnl.classList.toggle('open', notesOpen);
    // Shrink stage when notes open
    document.getElementById('stage').style.bottom = notesOpen ? (52 + 180) + 'px' : '52px';
  }}

  function toggleFullscreen() {{
    if (!document.fullscreenElement) {{
      document.documentElement.requestFullscreen().catch(() => {{}});
    }} else {{
      document.exitFullscreen();
    }}
  }}

  document.addEventListener('keydown', e => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {{ e.preventDefault(); next(); }}
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                    {{ e.preventDefault(); prev(); }}
    if (e.key === 'f' || e.key === 'F') toggleFullscreen();
    if (e.key === 'n' || e.key === 'N') toggleNotes();
    if (e.key === 'Escape' && notesOpen) toggleNotes();
  }});

  // Initialise
  show(0);

  // Load slide content from <script type="text/html"> tags into iframe srcdoc
  // (avoids HTML-attribute escaping issues with large slide HTML)
  const slideData = document.querySelectorAll('script[type="text/cogniesl-slide"]');
  slideData.forEach((s, i) => {{
    frames[i].srcdoc = s.textContent;
  }});
</script>

<!-- Slide content stored in script tags to avoid attribute escaping issues -->
{slide_scripts}

</body>
</html>
"""


# ── Main tool ──────────────────────────────────────────────────────────────

class BuildOfflineBundle(BaseTool):
    """
    Generate a single self-contained offline HTML presentation file.

    Inlines all fonts (Google Fonts, Font Awesome) and images as base64 data URIs.
    Each slide runs in its own iframe for CSS isolation.
    Includes prev/next navigation, keyboard shortcuts, speaker notes, and fullscreen.

    Call AFTER all slides are generated, BEFORE SnapSlideForEmail and MarkJobComplete.
    The output path is what you pass to MarkJobComplete as html_bundle_path.
    """

    project_name: str = Field(
        ...,
        description="Project folder name (e.g. 'present_perfect_french_adults')",
    )
    grammar_point: str = Field(
        default="",
        description="Grammar point name shown in the file title bar (e.g. 'Present Perfect')",
    )

    def run(self) -> str:
        project_dir = get_project_dir(self.project_name)
        slides = list_slide_files(project_dir)

        if not slides:
            return f"Error: No slides found in project '{self.project_name}'."

        log.info(f"[bundle] Building offline bundle for {self.project_name} ({len(slides)} slides)")

        slide_iframes = []
        slide_scripts = []
        notes_list = []

        for i, slide in enumerate(slides):
            raw_html = slide.path.read_text(encoding="utf-8")

            # Extract speaker notes before inlining (they're in an attribute)
            notes_list.append(_extract_speaker_notes(raw_html))

            # Inline all external resources
            inlined_html = _inline_slide_resources(raw_html, slide.path)

            # Each slide: an iframe + a <script type="text/cogniesl-slide"> tag
            active_cls = " active" if i == 0 else ""
            slide_iframes.append(
                f'  <iframe class="slide-frame{active_cls}" id="slide-{i}" '
                f'title="Slide {i+1}"></iframe>'
            )
            # Store slide HTML in a script tag.
            # Defensive: escape any </script> sequences inside the slide HTML so the
            # browser doesn't terminate the outer script tag prematurely.
            safe_html = inlined_html.replace("</script>", "<\\/script>")
            slide_scripts.append(
                f'<script type="text/cogniesl-slide">{safe_html}</script>'
            )

            log.info(f"[bundle] Processed slide {i+1}/{len(slides)}: {slide.path.name}")

        # Build notes JSON (escape for JS string)
        import json
        notes_json = json.dumps(notes_list)

        # Render the shell
        bundle_html = _NAV_SHELL.format(
            title=html.escape(self.grammar_point or self.project_name),
            total=len(slides),
            slide_iframes="\n".join(slide_iframes),
            slide_scripts="\n".join(slide_scripts),
            notes_json=notes_json,
        )

        # Save
        out_dir = project_dir / "presentations"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{self.project_name}.html"
        out_path.write_text(bundle_html, encoding="utf-8")

        size_kb = out_path.stat().st_size // 1024
        return (
            f"Offline HTML bundle created: {out_path} ({size_kb} KB)\n"
            f"Slides: {len(slides)}  |  Speaker notes: {sum(1 for n in notes_list if n)} slides\n"
            f"Fonts inlined: Google Fonts + Font Awesome (works without internet)\n"
            f"Pass to MarkJobComplete as: html_bundle_path={out_path}\n\n"
            f"Teacher instructions:\n"
            f"  1. Download the .html file\n"
            f"  2. Double-click to open in any browser\n"
            f"  3. Press F for fullscreen, arrow keys to navigate, N for speaker notes"
        )
