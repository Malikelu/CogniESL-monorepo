"""
E2E Test with proper session management (ThreadManager for conversation history)
"""
import asyncio, sys, os, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ["DEFAULT_MODEL"] = "deepseek/deepseek-v4-flash"
os.environ["SUB_AGENT_MODEL"] = "deepseek/deepseek-v4-flash"
from dotenv import load_dotenv
load_dotenv(override=True)
from agent.cogniesl_agent import create_cogniesl_agent
from agency_swarm import ThreadManager
from agency_swarm.agent.context_types import AgencyContext, AgentRuntimeState

RESULTS = Path("/tmp/cogniesl_e2e_test")
RESULTS.mkdir(parents=True, exist_ok=True)

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}")

def save(label, text):
    RESULTS.joinpath(label).write_text(text)

async def main():
    log("Creating agent and context...")
    agent = create_cogniesl_agent(format_request="")
    ctx = AgencyContext(
        agency_instance=None,
        thread_manager=ThreadManager(),
        runtime_state=AgentRuntimeState(agent._tool_concurrency_manager),
    )
    log("Ready\n")

    # Turn 1
    msg1 = "I need slides, a worksheet, an activity guide, and homework for present simple for Chinese and Japanese adults."
    log(f"TURN 1: {msg1[:60]}...")
    r1 = await agent.get_response(msg1, context=ctx)
    t1 = r1.final_output if hasattr(r1, 'final_output') else str(r1)
    save("01_initial.txt", t1)
    log(f"  Response ({len(t1)} chars): {t1[:200]}...\n")

    # Turn 2: Email (if asked)
    log("TURN 2: test@teacher.com")
    r2 = await agent.get_response("test@teacher.com", context=ctx)
    t2 = r2.final_output if hasattr(r2, 'final_output') else str(r2)
    save("02_content_brief.txt", t2)
    log(f"  Response ({len(t2)} chars)")
    log(f"  Full response:\n{t2}\n")

    # Analyze Content Brief
    log("=" * 60)
    log("CONTENT BRIEF ANALYSIS")
    log("=" * 60)
    
    sections = [
        "Content Brief", "What This Grammar Means", "Concept Check",
        "Formula", "L1 Oracle", "Exercises",
        "Slide Plan", "Worksheet Preview", "Homework Preview",
        "Delivering", "Pronunciation", "Phonetics", "Activity",
    ]
    
    for s in sections:
        if s.lower() in t2.lower():
            log(f"  OK: {s}")
        else:
            log(f"  MISSING: {s}")
    
    # Slide count
    idx = t2.find("Slide Plan")
    if idx >= 0:
        plan = t2[idx:idx+2000]
        count = plan.count("| **")
        log(f"  Slides: {count}")
    
    for lang in ["Chinese", "Japanese"]:
        log(f"  L1 {lang}: {'OK' if lang in t2 else 'MISSING'}")
    
    log(f"\nFiles: {RESULTS}/")
    for p in sorted(RESULTS.iterdir()):
        log(f"  {p.name}")

asyncio.run(main())
