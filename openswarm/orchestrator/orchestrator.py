from agency_swarm import Agent, ModelSettings
from dotenv import load_dotenv

from config import is_openai_provider

load_dotenv()


def _is_reasoning_model() -> bool:
    """Check if the configured model supports reasoning (o1, o3, etc.)."""
    import os
    model = os.getenv("ORCHESTRATOR_MODEL", "gpt-4o")
    return model.startswith("o1") or model.startswith("o3") or model.startswith("o4")


def create_orchestrator() -> Agent:
    import os
    model = os.getenv("ORCHESTRATOR_MODEL", "gpt-4o")
    reasoning = None
    if is_openai_provider() and _is_reasoning_model():
        from openai.types.shared import Reasoning
        reasoning = Reasoning(effort="medium", summary="auto")

    return Agent(
        name="Orchestrator",
        description=(
            "CogniESL Orchestrator — pure router that coordinates the ESL material generation pipeline. "
            "Routes teacher requests to the ESL Intake Agent, then to the ESL Pedagogy Agent, "
            "and finally to production specialists (Slides Agent, Docs Agent). "
            "Never gathers data or generates content itself."
        ),
        instructions="./instructions.md",
        tools=[],  # Pure router — no custom tools
        model=model,
        model_settings=ModelSettings(
            reasoning=reasoning,
        ),
        conversation_starters=[
            "I need slides for present simple for my Brazilian students.",
            "Create a worksheet on articles for Spanish-speaking teens.",
            "What materials can you generate for ESL teachers?",
            "Generate an activity for present continuous for Arabic adults.",
        ],
    )
