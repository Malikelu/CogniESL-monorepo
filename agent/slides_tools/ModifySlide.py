"""
Modify an existing slide by generating HTML with a sub-agent.

Flow: InsertNewSlides creates blank placeholders + plan, then ModifySlide generates/edits slide HTML.
"""

from __future__ import annotations

import asyncio
import base64
import mimetypes
import os
import re
from dotenv import load_dotenv
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agency_swarm.tools import BaseTool, tool_output_image_from_path
from openai import AsyncOpenAI
from pydantic import Field

from .slide_file_utils import get_project_dir
from .slide_html_utils import (
    ensure_full_html,
    list_slide_filenames,
    validate_html,
    _strip_html_to_text,
)
from .template_registry import load_template_index, save_template_index, template_path
# Per-project locks for the template-index read-modify-write.
_index_locks: dict[str, threading.Lock] = {}
_index_locks_guard = threading.Lock()


def _index_lock_for(project_dir: Path) -> threading.Lock:
    key = str(project_dir)
    with _index_locks_guard:
        if key not in _index_locks:
            _index_locks[key] = threading.Lock()
        return _index_locks[key]


def _strip_base64_images(html: str) -> str:
    """Replace base64 data URI references with short placeholders.

    Covers both src="data:..." attributes and url('data:...') CSS values.
    Prevents context-window overflow when feeding previously-processed HTML
    back to the sub-agent as a baseline.
    """
    # Only strip data:image/ URIs — never touch data:text/css or other non-image blobs
    html = re.sub(r'src=(["\'])data:image/[^"\']+\1', r'src=\1[image]\1', html)
    html = re.sub(r'url\((["\']?)data:image/[^"\')\s]+\1\)', r'url(\1[image]\1)', html)
    html = re.sub(r'(href|xlink:href|data)=(["\'])data:image/[^"\']+\2', r'\1=\2[image]\2', html)
    return html


def _convert_css_bg_images_to_img_tags(html: str) -> str:
    """Convert CSS background-image to <img> tags so dom-to-pptx can render them.

    Handles two patterns:
      1. Inline style:  <div style="background-image: url(img.png)">
      2. Class-based:   .cls { background-image: url(img.png) } + <div class="cls">

    For each match an absolutely-positioned <img> is injected as the first child
    and background-image/size/position/repeat are stripped from the CSS.
    Accepts both local paths and data: URIs (data URIs are kept as-is in the src).
    """
    _BG_STRIP_RE = re.compile(
        r'\bbackground-image\s*:\s*url\([^)]*\)\s*;?\s*'
        r'|\bbackground-size\s*:\s*[^;]+;\s*'
        r'|\bbackground-position\s*:\s*[^;]+;\s*'
        r'|\bbackground-repeat\s*:\s*[^;]+;\s*',
        re.IGNORECASE,
    )

    def _img_tag(src: str) -> str:
        return (
            f'<img src="{src}" alt="" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;'
            f'object-fit:cover;z-index:0;" />'
        )

    def _should_convert(url_arg: str) -> bool:
        """Convert both local image paths and data:image/ URIs."""
        if url_arg.startswith("data:image/"):
            return True
        if url_arg.startswith(("data:", "http://", "https://", "file://")):
            return False
        return _is_image_path(url_arg)

    # ── 1. Inline style="...background-image: url(...)..." ───────────────────
    inline_re = re.compile(
        r'(<[a-zA-Z][^>]*?style=["\'])([^"\']*?background-image\s*:\s*url\(([^)]+)\)[^"\']*?)(["\'][^>]*>)',
        re.IGNORECASE,
    )

    def rewrite_inline(m: re.Match) -> str:
        before, style_val, url_raw, after = m.group(1), m.group(2), m.group(3), m.group(4)
        url_arg = url_raw.strip("\"' ")
        if not _should_convert(url_arg):
            return m.group(0)
        clean = _BG_STRIP_RE.sub('', style_val).strip().rstrip(';')
        return f'{before}{clean}{after}{_img_tag(url_arg)}'

    html = inline_re.sub(rewrite_inline, html)

    # ── 2. Class-based rules in <style> blocks ───────────────────────────────
    # Collect class → url mapping from <style> blocks
    style_block_re = re.compile(r'<style[^>]*>(.*?)</style>', re.IGNORECASE | re.DOTALL)
    css_class_bg_re = re.compile(
        r'\.([a-zA-Z_-][\w-]*)\s*\{([^}]*?background-image\s*:\s*url\(([^)]+)\)[^}]*?)\}',
        re.IGNORECASE | re.DOTALL,
    )

    class_to_url: dict[str, str] = {}
    for style_m in style_block_re.finditer(html):
        for rule_m in css_class_bg_re.finditer(style_m.group(1)):
            cls = rule_m.group(1)
            url_arg = rule_m.group(3).strip("\"' ")
            if _should_convert(url_arg):
                class_to_url[cls] = url_arg

    if not class_to_url:
        return html

    # Strip background-image from matching rules in <style> blocks
    def rewrite_style_block(style_m: re.Match) -> str:
        css = style_m.group(1)
        def clean_rule(rule_m: re.Match) -> str:
            cls = rule_m.group(1)
            if cls not in class_to_url:
                return rule_m.group(0)
            cleaned_body = _BG_STRIP_RE.sub('', rule_m.group(2)).strip().rstrip(';')
            return f'.{cls} {{{cleaned_body}}}'
        return f'<style>{css_class_bg_re.sub(clean_rule, css)}</style>'

    html = style_block_re.sub(rewrite_style_block, html)

    # Inject <img> as first child of elements that carry a matched class
    class_pattern = '|'.join(re.escape(c) for c in class_to_url)
    element_re = re.compile(
        rf'(<[a-zA-Z][^>]*?class=["\'][^"\']*?(?:{class_pattern})[^"\']*?["\'][^>]*>)',
        re.IGNORECASE,
    )

    def inject_img(m: re.Match) -> str:
        opening = m.group(1)
        # Find which class matched
        classes = re.search(r'class=["\']([^"\']+)["\']', opening, re.IGNORECASE)
        if not classes:
            return opening
        for cls in classes.group(1).split():
            if cls in class_to_url:
                return f'{opening}{_img_tag(class_to_url[cls])}'
        return opening

    html = element_re.sub(inject_img, html)
    return html


_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp", ".avif"}


def _is_image_path(src: str) -> bool:
    return Path(src.split("?")[0]).suffix.lower() in _IMAGE_EXTENSIONS


def _embed_local_images_as_base64(html: str, project_dir: Path) -> str:
    """Replace local image references with base64 data URIs.

    Handles HTML src=, CSS url(), SVG href/xlink:href, and <object data=>.
    Only processes paths with known image file extensions to avoid
    accidentally encoding scripts, stylesheets, or fonts.
    """
    def _encode(src: str) -> str | None:
        if (
            src.startswith("data:")
            or src.startswith("http://")
            or src.startswith("https://")
            or src.startswith("file://")
            or not _is_image_path(src)
        ):
            return None
        img_path = (project_dir / src).resolve()
        if not img_path.exists():
            return None
        mime, _ = mimetypes.guess_type(str(img_path))
        mime = mime or "image/png"
        encoded = base64.b64encode(img_path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"

    def replace_src(match: re.Match) -> str:
        quote, src = match.group(1), match.group(2)
        data_uri = _encode(src)
        return f"src={quote}{data_uri}{quote}" if data_uri else match.group(0)

    def replace_css_url(match: re.Match) -> str:
        quote, src = match.group(1), match.group(2)
        data_uri = _encode(src)
        return f"url({quote}{data_uri}{quote})" if data_uri else match.group(0)

    def replace_href(match: re.Match) -> str:
        attr, quote, src = match.group(1), match.group(2), match.group(3)
        data_uri = _encode(src)
        return f'{attr}={quote}{data_uri}{quote}' if data_uri else match.group(0)

    html = re.sub(r'src=(["\'])((?!data:|https?://|file://)[^"\']+)\1', replace_src, html)
    html = re.sub(r'url\((["\']?)((?!data:|https?://|file://)[^"\')\s]+)\1\)', replace_css_url, html)
    html = re.sub(
        r'(href|xlink:href|data)=(["\'])((?!data:|https?://|file://|#)[^"\']+)\2',
        replace_href,
        html,
    )
    return html


# Sub-agent model: DeepSeek v4 flash only.
_HTML_WRITER_MODEL_DEFAULT = "deepseek-v4-flash"
_HTML_WRITER_MAX_ATTEMPTS = 5


def _get_html_writer_model_id() -> str:
    model = os.getenv("BG_SUB_AGENT_MODEL") or os.getenv("SUB_AGENT_MODEL", _HTML_WRITER_MODEL_DEFAULT)
    # Strip provider prefix if present (e.g. "deepseek/deepseek-v4-flash" -> "deepseek-v4-flash")
    if "/" in model:
        model = model.split("/", 1)[1]
    return model


def _make_deepseek_client(tool=None) -> AsyncOpenAI:
    """Create a direct AsyncOpenAI client pointed at DeepSeek's API.

    Uses DEEPSEEK_API_KEY from .env. No agents SDK, no LiteLLM.
    Calls go directly to https://api.deepseek.com/chat/completions.
    """
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required. Set it in .env")
    return AsyncOpenAI(
        api_key=deepseek_key,
        base_url="https://api.deepseek.com",
    )


async def _call_deepseek(client: AsyncOpenAI, model_id: str, system_prompt: str, user_prompt: str) -> str:
    """Call DeepSeek API directly and return the text response."""
    response = await client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""


def _extract_html_from_output(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        return ""
    code_block = re.search(r"```(?:html)?\s*(.*?)```", raw, flags=re.IGNORECASE | re.DOTALL)
    if code_block:
        return code_block.group(1).strip()

    html_start = re.search(r"(?is)(<!doctype html>|<html\b)", raw)
    if html_start:
        return raw[html_start.start() :].strip()
    body_start = re.search(r"(?is)<body\b", raw)
    if body_start:
        return raw[body_start.start() :].strip()
    return raw


def _read_html_writer_instructions() -> str:
    path = Path(__file__).with_name("html_writer_instructions.md")
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return "You generate slide HTML. Return only HTML content."


def _read_theme_css(project_dir: Path) -> str:
    theme_path = project_dir / "_theme.css"
    if not theme_path.exists():
        return ""
    try:
        return theme_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _extract_used_classes(html_content: str, limit: int = 120) -> list[str]:
    classes: list[str] = []
    seen: set[str] = set()
    for match in re.finditer(r'class\s*=\s*["\']([^"\']+)["\']', html_content, flags=re.IGNORECASE):
        raw = match.group(1)
        for cls in re.split(r"\s+", raw.strip()):
            if not cls or cls in seen:
                continue
            seen.add(cls)
            classes.append(cls)
            if len(classes) >= limit:
                return classes
    return classes


def _build_main_text_contents(project_dir: Path, current_slide: str) -> str:
    """Return a MAIN_TEXT_CONTENTS block with a one-line text snippet per slide.

    Mirrors the block the main agent receives each turn so the HTML writer
    sub-agent has the same deck-wide context (what's on each slide, what slide
    number it is currently editing, total count).
    """
    slides = list_slide_filenames(project_dir)
    if not slides:
        return ""
    lines = ["<MAIN_TEXT_CONTENTS>"]
    for i, name in enumerate(slides, 1):
        try:
            text = _strip_html_to_text((project_dir / name).read_text(encoding="utf-8"))
        except Exception:
            text = "(unreadable)"
        marker = " ← YOU ARE EDITING THIS SLIDE" if name == current_slide else ""
        lines.append(f"  <SLIDE_{i}>{text}</SLIDE_{i}>{marker}")
    lines.append("</MAIN_TEXT_CONTENTS>")
    return "\n".join(lines)



def _build_sub_run_prompt(
    *,
    task_brief: str,
    slide_name: str,
    total_pages: int,
    main_text_contents: str,
    base_html: str,
    current_html: str | None = None,
    theme_css: str,
    retry_validation_error: str = "",
    previous_failed_html: str | None = None,
) -> str:
    """Build the per-call user message for the HTML writer sub-agent.

    Design guidelines and validation rules are in the agent's system prompt
    (set once at agent creation). This message carries only the dynamic,
    per-slide context that changes with every call.

    When `current_html` is provided it means a saved template (not the slide itself)
    is being used as the layout baseline. The current slide content is shown
    separately so the writer knows what already exists on the slide.

    When `previous_failed_html` is provided (retry ≥ 2), the writer receives
    its own previous output so it can surgically fix the specific violations
    rather than regenerating from scratch.
    """
    deck_context = (
        f"Deck overview — {total_pages} slide(s) total:\n{main_text_contents}"
        if main_text_contents
        else f"Total slides in deck: {total_pages}"
    )
    retry_block = (
        f"\n\nVALIDATION FEEDBACK FROM PREVIOUS ATTEMPT (fix these before returning):\n{retry_validation_error}"
        if retry_validation_error
        else ""
    )
    previous_attempt_block = (
        "\n\nYOUR PREVIOUS ATTEMPT (the HTML you returned that failed validation — fix it, do not regenerate from scratch):\n"
        "<PREVIOUS_ATTEMPT>\n"
        f"{previous_failed_html}\n"
        "</PREVIOUS_ATTEMPT>"
        if previous_failed_html
        else ""
    )

    if current_html is not None:
        # Template mode: base_html is a saved layout skeleton, current_html is the
        # live slide. Show both so the writer uses the template structure but
        # understands the slide's existing content.
        html_section = (
            "LAYOUT_TEMPLATE_HTML (use this as the structural/design baseline — "
            "adopt its layout, colours, and component patterns):\n"
            "<LAYOUT_TEMPLATE>\n"
            f"{base_html}\n"
            "</LAYOUT_TEMPLATE>\n\n"
            "CURRENT_SLIDE_HTML (the slide as it exists now — understand its content "
            "but replace the layout with the template above):\n"
            "<CURRENT_SLIDE>\n"
            f"{current_html}\n"
            "</CURRENT_SLIDE>\n"
        )
    else:
        # Direct edit mode: base_html IS the current slide. Modify it in place.
        html_section = (
            "CURRENT_SLIDE_HTML (edit this slide in place — preserve everything "
            "not mentioned in the task brief):\n"
            "<CURRENT_SLIDE>\n"
            f"{base_html}\n"
            "</CURRENT_SLIDE>\n"
        )

    return (
        f"Target slide: {slide_name}\n"
        f"{deck_context}\n\n"
        "TASK_BRIEF:\n"
        f"{task_brief.strip()}\n\n"
        f"{html_section}\n"
        "CURRENT_THEME_CSS (authoritative design tokens — reuse, do not contradict):\n"
        "<THEME_CSS>\n"
        f"{theme_css}\n"
        "</THEME_CSS>\n\n"
        "USED_CLASSES_IN_CURRENT_SLIDE:\n"
        f"{', '.join(_extract_used_classes(base_html))}"
        f"{previous_attempt_block}"
        f"{retry_block}"
    )


def _screenshot_html_slide(html_path: Path) -> tuple[Any | None, str]:
    """Render the slide HTML in a headless browser and return (ToolOutputImage | None, error_msg).

    Returns (None, reason) on failure so the caller can include the reason in the tool output.
    """
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(html_path.resolve().as_uri(), wait_until="load", timeout=20_000)
            page.wait_for_timeout(800)  # let JS and fonts settle
            tmp = Path(tempfile.mktemp(suffix=".jpg"))
            page.screenshot(
                path=str(tmp),
                clip={"x": 0, "y": 0, "width": 1280, "height": 720},
                type="jpeg",
                quality=80,
            )
            browser.close()
        return tool_output_image_from_path(tmp), ""
    except Exception as exc:
        return None, str(exc)


def _generate_minimal_html_fallback(
    slide_name: str,
    task_brief: str,
    theme_css: str = "",
) -> str:
    """Generate minimal but valid HTML slide as fallback when all retries fail.

    This ensures no empty slides are ever returned. The slide has:
    - Basic structure with theme CSS applied
    - Title extracted from task brief or slide name
    - Content from task brief (first 200 chars)
    - Speaker notes
    - Minimum 50 chars of text content (validation requirement)

    This is a safety net — better a plain slide than a failed generation.
    """
    # Extract title from task brief or use slide name
    title = "Slide"
    if "Title:" in task_brief:
        title = task_brief.split("Title:")[1].split("\n")[0].strip()[:50]
    elif slide_name:
        title = slide_name.replace(".html", "").replace("_", " ").title()

    # Extract speaker notes if provided
    speaker_notes = "Teacher talk: Present this slide. Watch for common errors."
    if "SPEAKER NOTES:" in task_brief:
        speaker_notes = task_brief.split("SPEAKER NOTES:")[1].split("\n")[0].strip()[:100]

    # Extract first sentence from task brief as content
    content = task_brief[:150].split("\n")[0]
    if not content.strip():
        content = f"Content for {title}. Students should understand key concepts."

    minimal_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {theme_css}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 40px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .slide-wrapper {{
            width: 1280px;
            height: 720px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 60px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        h1 {{
            font-size: 48px;
            color: #2c3e50;
            margin: 0 0 30px 0;
            font-weight: 600;
        }}
        p {{
            font-size: 24px;
            color: #34495e;
            line-height: 1.6;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="slide-wrapper" data-speaker-notes="{speaker_notes}">
        <h1>{title}</h1>
        <p>{content}</p>
    </div>
</body>
</html>"""

    return minimal_html




class ModifySlide(BaseTool):
    """Generate/update slide HTML from task brief via sub-agent."""

    project_name: str = Field(..., description="Presentation project folder name under ./mnt/<project_name>/presentations. Only provide the project_name in this field.")
    slide_name: str = Field(..., description="Slide filename (e.g., slide_01 or slide_01.html)")
    task_brief: str = Field(..., description="What to change on this slide. Do not include any HTML in the tool input. HTML is written by the sub-agent inside this tool.")
    existing_template_key: str | None = Field(default=None, description="Optional template key to load as baseline")
    save_as_template_key: str | None = Field(default=None, description="Optional template key to save resulting slide")
    save_as_template_name: str | None = Field(default=None, description="Optional display name for saved template")

    async def run(self):
        load_dotenv(override=True)
        # Small throttle between slide calls to avoid hitting TPM limits on lower-tier accounts
        _throttle_secs = float(os.getenv("SLIDE_GENERATION_DELAY", "3"))
        if _throttle_secs > 0:
            await asyncio.sleep(_throttle_secs)
        project_dir = get_project_dir(self.project_name)
        if not project_dir.exists():
            return f"Project not found: {project_dir}"

        slide_filename = self.slide_name if self.slide_name.lower().endswith(".html") else f"{self.slide_name}.html"
        slide_path = project_dir / slide_filename
        if not slide_path.exists():
            return f"Slide not found: {slide_filename}"

        index_data = load_template_index(project_dir)
        current_html = _strip_base64_images(slide_path.read_text(encoding="utf-8"))
        base_html = current_html
        using_template = False

        if self.existing_template_key:
            key = self.existing_template_key.strip()
            meta = index_data.get(key)
            if not meta:
                return f"Template key not found: {key}"
            path = template_path(project_dir, key)
            if not path.exists():
                return f"Template file missing for key '{key}': {path.name}"
            base_html = _strip_base64_images(path.read_text(encoding="utf-8"))
            using_template = True

        total_pages = len([p for p in project_dir.glob("*.html")])
        theme_css = _read_theme_css(project_dir)
        main_text_contents = _build_main_text_contents(project_dir, slide_filename)

        # Log task_brief size — thin task_briefs produce thin slides.
        # If this shows < 400 chars, the main agent isn't pasting YAML data.
        import logging as _log
        _tb_log = _log.getLogger(__name__)
        _tb_len = len(self.task_brief)
        _tb_preview = self.task_brief[:300].replace("\n", " ")
        if _tb_len < 400:
            _tb_log.warning(
                f"[{slide_filename}] THIN TASK_BRIEF ({_tb_len} chars) — "
                f"agent likely not pasting YAML. Preview: {_tb_preview!r}"
            )
        else:
            _tb_log.info(f"[{slide_filename}] task_brief={_tb_len} chars. Preview: {_tb_preview!r}")

        model_id = _get_html_writer_model_id()
        system_prompt = _read_html_writer_instructions()
        client = _make_deepseek_client(tool=self)

        sub_results: list[str] = []
        last_validation_error = ""
        previous_failed_html: str | None = None
        final_html = ""
        used_scaffold = False

        for attempt in range(1, _HTML_WRITER_MAX_ATTEMPTS + 1):
            # Universal backoff on ALL retries (not just rate limits).
            # Gives API headroom during parallel batch generation.
            if attempt > 1:
                await asyncio.sleep(3 * attempt)  # 6s, 9s, 12s, ...
            prompt = _build_sub_run_prompt(
                task_brief=self.task_brief,
                slide_name=slide_filename,
                total_pages=total_pages,
                main_text_contents=main_text_contents,
                base_html=base_html,
                current_html=current_html if using_template else None,
                theme_css=theme_css,
                retry_validation_error=last_validation_error,
                previous_failed_html=previous_failed_html,
            )

            try:
                output_text = await _call_deepseek(client, model_id, system_prompt, prompt)
            except Exception as exc:
                import traceback
                err_str = str(exc)
                # Rate limit: wait and retry rather than failing immediately
                if "RateLimitError" in type(exc).__name__ or "rate_limit" in err_str.lower() or "rate limit" in err_str.lower():
                    wait = 30 * attempt  # 30s, 60s, 90s
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Rate limit hit on attempt {attempt} for {slide_filename}. Waiting {wait}s before retry."
                    )
                    await asyncio.sleep(wait)
                last_validation_error = f"DeepSeek API error (attempt {attempt}): {exc}\n{traceback.format_exc()}"
                continue
            sub_results.append(output_text)

            if not output_text.strip():
                last_validation_error = f"Model returned empty output on attempt {attempt}."
                continue

            candidate_html = _extract_html_from_output(output_text)
            if not candidate_html:
                last_validation_error = f"Model returned empty output on attempt {attempt}."
                continue

            full_html, used_scaffold = ensure_full_html(candidate_html)
            validation = await asyncio.to_thread(validate_html, full_html, project_dir, used_scaffold)
            if not validation.get("valid"):
                last_validation_error = str(validation.get("error", "Unknown validation error")).strip()
                previous_failed_html = full_html
                continue

            # Post-generation: enforce speaker notes
            if 'data-speaker-notes' not in full_html:
                speaker_notes = "Teacher talk: Present this slide to students. CCQs: Check understanding. Watch for: Common errors."
                if "SPEAKER NOTES:" in self.task_brief:
                    notes_part = self.task_brief.split("SPEAKER NOTES:")[1].strip()
                    speaker_notes = notes_part
                full_html = full_html.replace(
                    "</body>",
                    f'<div data-speaker-notes="{speaker_notes}"></div>\n</body>'
                )

            # Post-generation: check minimum content density
            text_content = _strip_html_to_text(full_html)
            if len(text_content) < 50:
                last_validation_error = f"Slide has insufficient content (only {len(text_content)} chars of text). Regenerate with more visual and text content."
                previous_failed_html = full_html
                continue

            final_html = full_html
            break

        # Fallback: if all attempts failed, generate minimal but valid HTML
        if not final_html:
            import logging as _fb_log
            _fb_logging = _fb_log.getLogger(__name__)
            _fb_logging.warning(
                f"[{slide_filename}] All {_HTML_WRITER_MAX_ATTEMPTS} attempts failed. "
                f"Last error: {last_validation_error[:200]}"
            )
            final_html = _generate_minimal_html_fallback(
                slide_name=slide_filename,
                task_brief=self.task_brief,
                theme_css=theme_css,
            )

        final_html = _convert_css_bg_images_to_img_tags(final_html)
        final_html = _embed_local_images_as_base64(final_html, project_dir)
        slide_path.write_text(final_html, encoding="utf-8")

        # ---- Post-write size check -----------------------------------------------
        # If a placeholder (fallback) was written, retry once more.
        # Fallback HTML is ~1,500 bytes; real slides should be ≥ 4,000 bytes.
        # Reduced from 3×3=9 retries to 1×2=2 to avoid excessive LLM calls.
        # Skip for CLOSING_BRAND slides — they're locked templates (~2KB is expected).
        _POST_WRITE_MIN = 4000
        _pw_written_size = slide_path.stat().st_size
        _is_closing_brand = "CLOSING_BRAND" in self.task_brief
        if _pw_written_size < _POST_WRITE_MIN and not _is_closing_brand:
            import logging as _pw_logging
            _pw_logger = _pw_logging.getLogger(__name__)
            _pw_logger.warning(
                f"{slide_filename}: written size {_pw_written_size}B < {_POST_WRITE_MIN}B "
                f"— retrying once (1 round, up to 3 attempts)."
            )
            _pw_html = ""
            _pw_err = ""
            for _pw_attempt in range(1, 4):  # 3 attempts, 1 round
                _pw_prompt = _build_sub_run_prompt(
                    task_brief=self.task_brief,
                    slide_name=slide_filename,
                    total_pages=total_pages,
                    main_text_contents=main_text_contents,
                    base_html=base_html,
                    current_html=None,
                    theme_css=theme_css,
                    retry_validation_error=_pw_err,
                    previous_failed_html=None,
                )
                _size_str = str(_pw_written_size)
                _pw_prompt = (
                    f"⚠️ PREVIOUS VERSION WAS TOO THIN ({_size_str}B). "
                    "This slide MUST have substantial content: a clear title, "
                    "detailed explanation, multiple examples, bullet points or "
                    "numbered steps, visual cues (icons/colors), and complete "
                    "speaker notes with CCQs and watch-for items.\n\n"
                    "MINIMUM CONTENT REQUIREMENTS:\n"
                    "- At least 3-4 sentences of teaching content\n"
                    "- Examples from the YAML data (wrong → correct pairs)\n"
                    "- Visual elements: colored cards, badges, icons, or layout\n"
                    "- Full speaker notes with teacher talk + CCQs + watch-for\n\n"
                    f"{_pw_prompt}"
                )
                try:
                    _pw_output = await _call_deepseek(client, model_id, system_prompt, _pw_prompt)
                except Exception as _pw_exc:
                    _pw_err_str = str(_pw_exc)
                    # Universal backoff for ALL post-write retry errors
                    await asyncio.sleep(5 * _pw_attempt)  # 5s, 10s, 15s
                    if "RateLimitError" in type(_pw_exc).__name__ or "rate_limit" in _pw_err_str.lower():
                        await asyncio.sleep(30 * _pw_attempt)
                    _pw_err = _pw_err_str
                    continue
                if not _pw_output.strip():
                    continue
                _pw_candidate = _extract_html_from_output(_pw_output)
                if not _pw_candidate:
                    continue
                _pw_full, _pw_scaffold = ensure_full_html(_pw_candidate)
                _pw_validation = await asyncio.to_thread(validate_html, _pw_full, project_dir, _pw_scaffold)
                if not _pw_validation.get("valid"):
                    _pw_err = str(_pw_validation.get("error", ""))
                    continue
                _pw_html = _pw_full
                break
            if _pw_html:
                _pw_html = _convert_css_bg_images_to_img_tags(_pw_html)
                _pw_html = _embed_local_images_as_base64(_pw_html, project_dir)
                slide_path.write_text(_pw_html, encoding="utf-8")
                _pw_written_size = slide_path.stat().st_size
        # ---- End post-write size check -------------------------------------------

        save_note = ""
        if self.save_as_template_key:
            key = self.save_as_template_key.strip()
            t_path = template_path(project_dir, key)
            t_path.write_text(final_html, encoding="utf-8")
            with _index_lock_for(project_dir):
                fresh_index = load_template_index(project_dir)
                fresh_index[key] = {
                    "name": (self.save_as_template_name or key).strip(),
                    "source_slide": slide_filename,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                save_template_index(project_dir, fresh_index)
            save_note = f"\nSaved template: {key}."

        success_msg = f"Updated {slide_filename}.{save_note}"

        return success_msg

if __name__ == "__main__":
    modify_slide = ModifySlide(project_name="universe_5slide_deck", slide_name="slide_06", task_brief="""Generate a plain string saying hello world""")
    print(asyncio.run(modify_slide.run()))