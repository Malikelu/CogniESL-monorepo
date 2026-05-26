#!/usr/bin/env python3
"""Phase 1 Test: Simple grammar topic (Present Simple + Spanish speakers + beginner level)"""
import asyncio
import sys
from pathlib import Path

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent / "agent"))

from agent.cogniesl_agent import create_cogniesl_agent


async def test_phase1():
    """Test end-to-end generation with a simple topic."""
    print("=" * 70)
    print("PHASE 1 TEST: Present Simple for Spanish Beginners")
    print("=" * 70)
    print()

    agent = create_cogniesl_agent()

    # Test request: Simple grammar topic
    test_request = """
I need materials for teaching present simple to adult learners.
They're all Spanish speakers, beginners.
I need slides and a worksheet.
"""

    print(f"Request: {test_request.strip()}")
    print()
    print("Starting agent conversation...")
    print("-" * 70)

    try:
        result = await agent.get_response(test_request)
        print(f"Agent Response:")
        print(f"{result.final_output}")
        print()
        print("-" * 70)
        print("✓ Test completed successfully")
        return True
    except Exception as e:
        print(f"✗ Test failed with error:")
        print(f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_phase1())
    sys.exit(0 if success else 1)
