#!/usr/bin/env python3
"""
Real end-to-end test - submit actual request to the server and capture output.
"""
import asyncio
import aiohttp
import json

async def test_app():
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8080/cogniesl/get_response"

        # Test request
        payload = {
            "message": "I need to teach articles to adults, 4 Brazilians and 4 Arabs. I need slides, worksheet, and one activity"
        }

        headers = {
            "X-Session-ID": "test_session_12345",
            "Content-Type": "application/json"
        }

        print("=" * 80)
        print("TESTING CogniESL APP")
        print("=" * 80)
        print(f"\nRequest: {payload['message']}\n")
        print("Waiting for response...\n")

        try:
            async with session.post(url, json=payload, headers=headers, timeout=120) as resp:
                data = await resp.json()
                print(f"Status: {resp.status}")
                print(f"Response:\n{json.dumps(data, indent=2)}\n")

                if "response" in data:
                    print("=" * 80)
                    print("AGENT RESPONSE:")
                    print("=" * 80)
                    print(data["response"])
                    print("=" * 80)
        except asyncio.TimeoutError:
            print("ERROR: Request timed out after 120 seconds")
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_app())
