from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning
from dotenv import load_dotenv

from config import get_default_model, is_openai_provider
from orchestrator.custom_tools import SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool

load_dotenv()


def create_orchestrator() -> Agent:
    return Agent(
        name="Orchestrator",
        description=(
            "Primary coordinator for CogniESL — an AI-powered ESL teaching material generator. "
            "Interprets teacher requests, searches the grammar/activities/L1 database, "
            "and routes to specialist agents (Slides Agent or Docs Agent) with full context."
        ),
        instructions="./instructions.md",
        tools=[SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
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