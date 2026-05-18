from agency_swarm import Agent, ModelSettings
from dotenv import load_dotenv

from config import is_openai_provider
from orchestrator.custom_tools import SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool

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
            "Primary coordinator for CogniESL — an AI-powered ESL teaching material generator. "
            "Interprets teacher requests, searches the grammar/activities/L1 database, "
            "and routes to specialist agents (Slides Agent or Docs Agent) with full context."
        ),
        instructions="./instructions.md",
        tools=[SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool],
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


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_orchestrator()).terminal_demo()
