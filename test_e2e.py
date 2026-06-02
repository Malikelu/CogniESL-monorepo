"""E2E test - full conversation: request -> confirm -> Content Brief"""
import asyncio, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ["DEFAULT_MODEL"] = "deepseek/deepseek-v4-flash"
os.environ["SUB_AGENT_MODEL"] = "deepseek/deepseek-v4-flash"
from dotenv import load_dotenv
load_dotenv(override=True)
from agent.cogniesl_agent import create_cogniesl_agent

RESULTS = Path("test_results")
RESULTS.mkdir(exist_ok=True)

def log(m): print(f"[{__import__('time').strftime('%H:%M:%S')}] {m}")

async def chat(agent, msg, label):
    log(f">> {msg[:80]}...")
    resp = await agent.get_response(msg)
    text = resp.final_output if hasattr(resp, 'final_output') else str(resp)
    RESULTS.joinpath(f"{label}.txt").write_text(text)
    log(f"<< ({len(text)} chars)")
    return text

async def main():
    agent = create_cogniesl_agent(format_request="")
    log("Agent created\n")
    
    # Turn 1: Initial request
    r1 = await chat(agent,
        "I need slides, a worksheet, an activity guide, and homework for present simple for Chinese and Japanese adults.",
        "01_initial_response")
    log(f"  Preview: {r1[:300]}...\n")
    
    # Turn 2: Provide email
    r2 = await chat(agent,
        "teacher@school.com",
        "02_content_brief")
    log(f"  Content Brief preview: {r2[:500]}...\n")
    
    # Check Content Brief structure
    checks = {
        "Content Brief header": "Content Brief" in r2 or "**Content Brief" in r2,
        "Core meaning": "means" in r2.lower() or "meaning" in r2.lower(),
        "CCQs": "Concept Check" in r2,
        "Formula": "Formula" in r2,
        "L1 Oracle - Chinese": "Chinese" in r2,
        "L1 Oracle - Japanese": "Japanese" in r2,
        "Exercises": "Exercises" in r2,
        "Slide Plan": "Slide Plan" in r2,
        "Worksheet Preview": "Worksheet" in r2,
        "Activity section": "Activity" in r2,
        "Homework mention": "homework" in r2.lower(),
        "Delivery line": "Delivering" in r2,
    }
    
    log("Content Brief Structure:")
    for name, ok in checks.items():
        log(f"  {'OK' if ok else 'MISSING'}: {name}")

asyncio.run(main())
