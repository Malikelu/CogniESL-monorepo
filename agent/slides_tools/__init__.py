"""Tools for the slides_agent."""

# Template registry (Phase 4a)
from .template_registry import (
    is_valid_template_key,
    known_template_keys,
    load_template_index,
    register_template,
    save_template_index,
    template_path,
)

# Structured slide plan models (Phase 4a)
from .InsertNewSlides import PlanResponse, PlanSlide

# Slide creation and management: InsertNewSlides then ModifySlide
from .InsertNewSlides import InsertNewSlides
from .ModifySlide import ModifySlide
from .ManageTheme import ManageTheme
from .DeleteSlide import DeleteSlide
from .SlideScreenshot import SlideScreenshot
from .ReadSlide import ReadSlide

# PPTX building and validation
from .BuildPptxFromHtmlSlides import BuildPptxFromHtmlSlides
from .RestoreSnapshot import RestoreSnapshot
from .CreatePptxThumbnailGrid import CreatePptxThumbnailGrid
from .CheckSlideCanvasOverflow import CheckSlideCanvasOverflow
from .CheckSlide import CheckSlide

# Template-based editing (for existing PPTX files)
from .ExtractPptxTextInventory import ExtractPptxTextInventory
from .RearrangePptxSlidesFromTemplate import RearrangePptxSlidesFromTemplate
from .ApplyPptxTextReplacements import ApplyPptxTextReplacements

# Asset utilities
from .EnsureRasterImage import EnsureRasterImage
from .CreateImageMontage import CreateImageMontage
from .DownloadImage import DownloadImage
from .ImageSearch import ImageSearch
from .GenerateImage import GenerateImage

__all__ = [
    # Template registry
    "is_valid_template_key",
    "known_template_keys",
    "load_template_index",
    "register_template",
    "save_template_index",
    "template_path",
    # Structured slide plan
    "PlanResponse",
    "PlanSlide",
    # Slide management
    "InsertNewSlides",
    "ModifySlide",
    "ManageTheme",
    "DeleteSlide",
    "SlideScreenshot",
    "ReadSlide",
    # PPTX building
    "BuildPptxFromHtmlSlides",
    "RestoreSnapshot",
    "CreatePptxThumbnailGrid",
    "CheckSlideCanvasOverflow",
    "CheckSlide",
    # Template editing
    "ExtractPptxTextInventory",
    "RearrangePptxSlidesFromTemplate",
    "ApplyPptxTextReplacements",
    # Assets
    "EnsureRasterImage",
    "CreateImageMontage",
    "DownloadImage",
    "ImageSearch",
    "GenerateImage",
]
