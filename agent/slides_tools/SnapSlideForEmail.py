"""
SnapSlideForEmail — screenshot the hook slide, crop to 1080×1080, add brand mark.

Used for the viral email mechanic (Track 3 item 5e):
  slide_02.html → 1280×720 screenshot → square crop → CogniESL brand overlay → PNG

The resulting image is embedded in the delivery email so teachers see a preview
of their materials before downloading. They forward it, post it, share it — viral growth.

Call this AFTER BuildPptxFromHtmlSlides, BEFORE MarkJobComplete.
"""

import base64
import logging
import tempfile
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

from .slide_file_utils import get_project_dir, list_slide_files

log = logging.getLogger(__name__)

_SLIDE_VIEWPORT = {"width": 1280, "height": 720}
# Crop: take center square from 1280×720 → 720×720, then scale to 1080×1080
_CROP_BOX = (280, 0, 1000, 720)   # x0, y0, x1, y1  (720px wide square from center)
_OUTPUT_SIZE = (1080, 1080)


class SnapSlideForEmail(BaseTool):
    """
    Screenshot the hook/title slide, crop to 1080×1080, add CogniESL brand overlay.

    Saves to ./mnt/{project_name}/snapshots/email_preview.png.
    Returns the file path — pass it to MarkJobComplete as snapshot_path so the
    delivery email includes the preview image.

    Call AFTER BuildPptxFromHtmlSlides, BEFORE MarkJobComplete.
    """

    project_name: str = Field(
        ...,
        description="Project folder name",
    )
    slide_index: int = Field(
        default=2,
        description=(
            "1-based index of the slide to screenshot. Defaults to 2 (hook slide). "
            "The lesson plan cover (slide 1) is teacher-only — use slide 2 for the snapshot."
        ),
    )

    def run(self) -> str:
        project_dir = get_project_dir(self.project_name)
        slides = list_slide_files(project_dir)

        if not slides:
            return f"Error: No slides found in project '{self.project_name}'."

        idx = min(self.slide_index, len(slides)) - 1
        slide_path = slides[idx].path

        if not slide_path.exists():
            return f"Error: Slide not found: {slide_path}"

        # Create snapshot output directory
        snap_dir = project_dir / "snapshots"
        snap_dir.mkdir(parents=True, exist_ok=True)
        output_path = snap_dir / "email_preview.png"

        try:
            self._render(slide_path, output_path)
        except ImportError as e:
            return f"Error: Missing dependency — {e}. Install playwright + Pillow."
        except Exception as e:
            return f"Error generating snapshot: {e}"

        if not output_path.exists():
            return "Error: Snapshot file was not created."

        size_kb = output_path.stat().st_size // 1024
        return (
            f"Snapshot created: {output_path} ({size_kb} KB)\n"
            f"Source slide: {slide_path.name}\n"
            f"Pass to MarkJobComplete as: snapshot_path={output_path}"
        )

    def _render(self, slide_path: Path, output_path: Path) -> None:
        from playwright.sync_api import sync_playwright
        from PIL import Image, ImageDraw, ImageFont
        import io

        # 1. Screenshot the slide at 1280×720
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport=_SLIDE_VIEWPORT)
            page.goto(slide_path.resolve().as_uri(), wait_until="load", timeout=20_000)
            page.wait_for_timeout(1000)  # wait for fonts/animations
            tmp = Path(tempfile.mktemp(suffix=".png"))
            page.screenshot(
                path=str(tmp),
                clip={"x": 0, "y": 0, **_SLIDE_VIEWPORT},
                type="png",
            )
            browser.close()

        # 2. Open, crop to center square, resize to 1080×1080
        img = Image.open(tmp).convert("RGBA")
        img = img.crop(_CROP_BOX)
        img = img.resize(_OUTPUT_SIZE, Image.Resampling.LANCZOS)

        # 3. Add brand watermark overlay (bottom-right corner)
        self._add_brand_watermark(img)

        # 4. Save as PNG
        img = img.convert("RGB")
        img.save(output_path, "PNG", optimize=True)
        tmp.unlink(missing_ok=True)

    @staticmethod
    def _add_brand_watermark(img: "Image.Image") -> None:
        """Draw a small CogniESL brand tag in the bottom-right corner."""
        try:
            from PIL import ImageDraw
        except ImportError:
            return  # non-fatal

        draw = ImageDraw.Draw(img, "RGBA")
        w, h = img.size

        # Pill background — semi-transparent teal
        pad_x, pad_y = 16, 10
        text = "cogniesl.com"
        # Estimate text size at ~24px (no custom font — use default)
        text_w, text_h = 140, 22
        pill_x0 = w - text_w - pad_x * 2 - 18
        pill_y0 = h - text_h - pad_y * 2 - 18
        pill_x1 = w - 18
        pill_y1 = h - 18

        draw.rounded_rectangle(
            [pill_x0, pill_y0, pill_x1, pill_y1],
            radius=12,
            fill=(11, 114, 114, 200),  # #0b7272 at 78% opacity
        )
        draw.text(
            (pill_x0 + pad_x, pill_y0 + pad_y),
            text,
            fill=(255, 255, 255, 230),
        )
