from agency_swarm import Agent, ModelSettings
from dotenv import load_dotenv

from config import is_openai_provider

load_dotenv()


def create_esl_intake_agent() -> Agent:
    return Agent(
        name="ESL Intake Agent",
        description=(
            "CogniESL Intake Specialist — conducts conversational interviews with ESL teachers "
            "to gather lesson requirements (topic, L1, age, format). "
            "Validates data against the CogniESL database. "
            "Routes to the Orchestrator with a structured Requirement Spec."
        ),
        instructions="./instructions.md",
        model="gpt-4o",  # Use gpt-4o for reliable instruction following
        model_settings=ModelSettings(
            reasoning=None,
        ),
        conversation_starters=[
            "I need a lesson on Present Perfect for my Brazilian students.",
            "Can you help me create materials for teaching articles?",
            "I want to teach past simple to Spanish-speaking teens.",
        ],
    )
