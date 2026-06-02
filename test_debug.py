"""Debug test - run without guardrails to see agent's raw response."""
import asyncio, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ["DEFAULT_MODEL"] = "deepseek/deepseek-v4-flash"
os.environ["SUB_AGENT_MODEL"] = "deepseek/deepseek-v4-flash"
from dotenv import load_dotenv
load_dotenv(override=True)

from agency_swarm import Agent, ModelSettings
from agent.config import get_default_model
from agent.tools import SearchGrammarTool, GetL1InterferenceTool, SearchActivitiesTool
from agency_swarm.tools import IPythonInterpreter

# Create a minimal agent without guardrails for debugging
agent = Agent(
    name="DebugAgent",
    instructions=Path("agent/instructions.md").read_text(),
    tools=[SearchGrammarTool, GetL1InterferenceTool, SearchActivitiesTool, IPythonInterpreter],
    model=get_default_model(),
)

async def main():
    msg = "I need slides for present simple for Chinese and Japanese adults."
    print(f"Sending: {msg}")
    response = await agent.get_response(msg)
    text = response.final_output if hasattr(response, 'final_output') else str(response)
    Path("test_results/raw_response.txt").write_text(text)
    print(f"Response ({len(text)} chars):")
    print(text[:1000])

asyncio.run(main())
