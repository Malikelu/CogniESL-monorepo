from agency_swarm import Agent, ModelSettings
from dotenv import load_dotenv

from config import is_openai_provider
from orchestrator.custom_tools import SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool

load_dotenv()


def create_esl_pedagogy_agent() -> Agent:
    return Agent(
        name="ESL Pedagogy Agent",
        description=(
            "CogniESL Pedagogy Agent — expert ESL instructional designer. "
            "Receives requirements from the Intake Agent, searches the CogniESL database, "
            "customizes content for specific student profiles (age/L1/level), "
            "creates a detailed Lesson Script, and routes to production specialists."
        ),
        instructions="./instructions.md",
        tools=[SearchGrammarTool, SearchActivitiesTool, GetL1InterferenceTool],
        model="gpt-4o",  # Use gpt-4o for reliable instruction following
        model_settings=ModelSettings(
            reasoning=None,
        ),
        conversation_starters=[
            "Create a Lesson Script on Present Perfect for Brazilian adults at A2 level.",
            "Prepare a lesson on articles for Spanish-speaking teens.",
        ],
    )
