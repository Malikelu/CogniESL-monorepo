"""CogniESL Agent — Single agent that handles the full workflow."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Ensure the agent directory is on the path for tool imports
AGENT_DIR = Path(__file__).parent
sys.path.insert(0, str(AGENT_DIR))

from config import get_default_model


def create_cogniesl_agent():
    # Apply runtime patches to agency_swarm
    from patches.patch_agency_swarm_dual_comms import apply_dual_comms_patch
    from patches.patch_file_attachment_refs import apply_file_attachment_reference_patch
    from patches.patch_ipython_interpreter_composio import apply_ipython_composio_context_patch
    from patches.patch_utf8_file_reads import apply_utf8_file_read_patch
    apply_dual_comms_patch()
    apply_file_attachment_reference_patch()
    apply_ipython_composio_context_patch()
    apply_utf8_file_read_patch()

    from agency_swarm import Agent, ModelSettings
    from agency_swarm.tools import IPythonInterpreter

    from tools import SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool
    from slides_tools import (
        InsertNewSlides,
        ModifySlide,
        ManageTheme,
        DeleteSlide,
        SlideScreenshot,
        ReadSlide,
        BuildPptxFromHtmlSlides,
        RestoreSnapshot,
        CreatePptxThumbnailGrid,
        CheckSlideCanvasOverflow,
        CheckSlide,
        DownloadImage,
        EnsureRasterImage,
        ImageSearch,
        GenerateImage,
    )
    from docs_tools.CreateDocument import CreateDocument
    from docs_tools.ConvertDocument import ConvertDocument
    from docs_tools.ModifyDocument import ModifyDocument
    from docs_tools.ViewDocument import ViewDocument
    from docs_tools.ListDocuments import ListDocuments
    from docs_tools.RestoreDocument import RestoreDocument
    from shared_tools.CopyFile import CopyFile
    from utility_tools.ReadFile import ReadFile

    instructions_path = AGENT_DIR / "instructions.md"

    return Agent(
        name="CogniESL Agent",
        description=(
            "CogniESL — AI-powered ESL teaching material generator. "
            "Gathers requirements from teachers, searches the grammar/L1/activities database, "
            "and generates professional teaching materials (slides, worksheets, activities)."
        ),
        instructions=instructions_path.read_text(encoding="utf-8"),
        tools=[
            # Database search tools
            SearchGrammarTool,
            SearchActivitiesTool,
            GetL1InterferenceTool,
            # Slides tools
            InsertNewSlides,
            ModifySlide,
            ManageTheme,
            DeleteSlide,
            SlideScreenshot,
            ReadSlide,
            BuildPptxFromHtmlSlides,
            RestoreSnapshot,
            CreatePptxThumbnailGrid,
            CheckSlideCanvasOverflow,
            CheckSlide,
            DownloadImage,
            EnsureRasterImage,
            ImageSearch,
            GenerateImage,
            # Docs tools
            CreateDocument,
            ConvertDocument,
            ModifyDocument,
            ViewDocument,
            ListDocuments,
            RestoreDocument,
            # Utility tools
            IPythonInterpreter,
            ReadFile,
            CopyFile,
        ],
        model=get_default_model(),
        model_settings=ModelSettings(
            temperature=0.7,
        ),
    )
