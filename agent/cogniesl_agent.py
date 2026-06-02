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
from agent.guardrails import require_esl_topic, validate_l1_content, validate_slide_count, validate_citations

# Module-level imports for _select_tools() (used before create_cogniesl_agent() executes)
from agency_swarm.tools import IPythonInterpreter
from tools import SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool
from slides_tools import (
    InsertNewSlides,
    ModifySlide,
    ManageTheme,
    BuildPptxFromHtmlSlides,
    DownloadImage,
    ImageSearch,
    GenerateImage,
)
from slides_tools.QueueGenerationJob import QueueGenerationJob
from slides_tools.MarkJobComplete import MarkJobComplete
from slides_tools.BuildOfflineBundle import BuildOfflineBundle
from slides_tools.SnapSlideForEmail import SnapSlideForEmail
from shared_tools.CopyFile import CopyFile
from utility_tools.ReadFile import ReadFile
from validation_tools import (
    ValidateSlideSet,
    ValidateAndFixSlides,
    ValidateL1Content,
)
from docs_tools.CreateDocument import CreateDocument
from docs_tools.ConvertDocument import ConvertDocument
from docs_tools.ModifyDocument import ModifyDocument
from docs_tools.ViewDocument import ViewDocument
from docs_tools.ListDocuments import ListDocuments


def _build_instructions() -> str:
    """Build agent instructions by appending dynamic context to the static instructions.md."""
    from datetime import datetime, timezone
    from pathlib import Path
    
    instructions_path = Path(__file__).parent / "instructions.md"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = instructions_path.read_text(encoding="utf-8")
    
    # List existing project folders so the agent can avoid name collisions
    try:
        from agent.slides_tools.slide_file_utils import get_mnt_dir
        mnt_dir = get_mnt_dir()
        projects = sorted(d.name for d in mnt_dir.iterdir() if d.is_dir())
    except (ImportError, FileNotFoundError):
        projects = []
    projects_block = "\n".join(f"  - {p}" for p in projects[:20]) if projects else "  (none)"
    
    return (
        f"{body}\n\n"
        f"Current date/time (UTC): {now_utc}\n\n"
        f"Existing project folders (do NOT reuse these names):\n{projects_block}"
    )


def _select_tools(format_request: str = "") -> list:
    """Select tools based on the teacher's requested format.

    Instead of loading all ~30 tools for every session, load only the
    tools needed for the requested format. Falls back to all tools
    when the format is ambiguous or unspecified.
    """
    fmt = format_request.lower()

    # Tools needed regardless of format
    required_tools = [
        SearchGrammarTool,
        GetL1InterferenceTool,
        SearchActivitiesTool,
        IPythonInterpreter,
        ReadFile,
        CopyFile,
        QueueGenerationJob,
        MarkJobComplete,
    ]

    # Format-specific tool groups
    slides_tools = [
        InsertNewSlides,
        ModifySlide,
        ManageTheme,
        BuildPptxFromHtmlSlides,
        BuildOfflineBundle,
        ImageSearch,
        DownloadImage,
        GenerateImage,
        SnapSlideForEmail,
        ValidateSlideSet,
        ValidateAndFixSlides,
        ValidateL1Content,
    ]

    docs_tools = [
        CreateDocument,
        ConvertDocument,
        ModifyDocument,
        ViewDocument,
        ListDocuments,
    ]

    if not fmt or fmt == "all":
        # Ambiguous or all formats — load everything
        return required_tools + slides_tools + docs_tools

    selected = list(required_tools)

    if any(w in fmt for w in ["slide", "presentation", "deck", "pptx", "powerpoint"]):
        selected.extend(slides_tools)

    if any(w in fmt for w in ["worksheet", "activity", "handout", "printable", "pdf", "exercise", "document"]):
        selected.extend(docs_tools)

    # If nothing matched the format filters, load everything (safe fallback)
    if len(selected) == len(required_tools):
        return required_tools + slides_tools + docs_tools

    return selected


def create_cogniesl_agent(format_request: str = ""):
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

    return Agent(
        name="CogniESL Agent",
        description=(
            "CogniESL — AI-powered ESL teaching material generator. "
            "Gathers requirements from teachers, searches the grammar/L1/activities database, "
            "and generates professional teaching materials (slides, worksheets, activities)."
        ),
        instructions=_build_instructions(),
        tools=_select_tools(format_request),
        model=get_default_model(),
        model_settings=ModelSettings(
            temperature=0.7,
            parallel_tool_calls=False,
        ),
        input_guardrails=[require_esl_topic],
        output_guardrails=[validate_l1_content, validate_citations, validate_slide_count],
        validation_attempts=2,
    )
