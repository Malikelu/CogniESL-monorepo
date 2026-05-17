"""
Non-interactive test of the CogniESL Orchestrator.
Tests the 4 scenarios from the plan using gpt-4o-mini.
"""
import sys
import os

os.chdir('/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL/openswarm')
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from orchestrator import create_orchestrator
from agency_swarm import Agency

print("=" * 60)
print("COGNIESL ORCHESTRATOR TEST")
print("=" * 60)

orchestrator = create_orchestrator()
print(f"\nOrchestrator: {orchestrator.name}")
print(f"Model: {orchestrator.model}")
print(f"Tools: {[t.name if hasattr(t, 'name') else str(t) for t in orchestrator.tools]}")

agency = Agency(orchestrator)

# Test scenarios
scenarios = [
    "I need slides for present simple for Brazilian adults",
    "Create a worksheet on articles for Spanish-speaking teens",
    "Generate an activity for present continuous for Arabic adults",
]

for i, msg in enumerate(scenarios, 1):
    print(f"\n{'=' * 60}")
    print(f"SCENARIO {i}: {msg}")
    print(f"{'=' * 60}")
    try:
        response = agency.get_response_sync(
            message=msg,
            agent=orchestrator,
        )
        print(f"\nResponse:\n{response}")
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")

print(f"\n{'=' * 60}")
print("ALL TESTS COMPLETE")
print(f"{'=' * 60}")
