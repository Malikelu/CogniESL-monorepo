#!/bin/bash
# E2E Test via API - tests the full pipeline end-to-end
set -e

BASE="https://cogniesl-production.up.railway.app"
TOKEN="eyJhbG...Kd3U"  # test-e2e@test.com / test1234
SESSION="test-session-$(date +%s)"
RESULTS="test_api_results"
mkdir -p "$RESULTS"

echo "=== TEST 1: Complex request (2 L1s, multi-format) ==="

# Turn 1: Initial request
echo -e "\n--- Turn 1: Send request ---"
RESPONSE=$(curl -s -X POST "$BASE/cogniesl/get_response" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-ID: $SESSION" \
  -d '{"message":"I need slides, a worksheet, an activity guide, and homework for present simple for Chinese and Japanese adults."}')
echo "$RESPONSE" > "$RESULTS/01_turn1_response.json"
echo "Response length: $(echo "$RESPONSE" | wc -c) chars"
echo "Preview: $(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','')[:300] if isinstance(d,dict) else sys.stdin.read()[:300])" 2>/dev/null || echo "$RESPONSE" | head -c 300)"

# Turn 2: Provide email
echo -e "\n--- Turn 2: Provide email ---"
RESPONSE2=$(curl -s -X POST "$BASE/cogniesl/get_response" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-ID: $SESSION" \
  -d '{"message":"test-e2e@test.com"}')
echo "$RESPONSE2" > "$RESULTS/02_turn2_content_brief.json"
echo "Response length: $(echo "$RESPONSE2" | wc -c) chars"
echo "$RESPONSE2" | python3 -c "
import sys, json
d = json.load(sys.stdin)
resp = d.get('response', '') if isinstance(d, dict) else str(d)
print(resp[:500])
print('---')
# Check for key sections
for section in ['Content Brief', 'Slide Plan', 'L1 Oracle', 'Worksheet', 'Activity', 'Homework', 'Exercises', 'Formula', 'CCQ']:
    found = section.lower() in resp.lower()
    print(f\"  {'OK' if found else 'MISSING'}: {section}\")
"

echo -e "\n=== DONE ==="
echo "Results saved to $RESULTS/"
ls -la "$RESULTS/"
