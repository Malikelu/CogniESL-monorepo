#!/usr/bin/env python3
"""
CogniESL automated end-to-end test script.
Uses only Python stdlib — no pip installs needed.

Usage:
    python test_cogniesl.py [BASE_URL]

    BASE_URL defaults to https://cogniesl-production.up.railway.app

Each test prints PASS or FAIL with a short reason.
Exit code: 0 if all pass, 1 if any fail.
"""

import json
import sys
import time
import urllib.request
import urllib.error
import uuid

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://cogniesl-production.up.railway.app"
RESULTS = []


def _req(method, path, body=None, headers=None, timeout=90):
    """Make an HTTP request, return (status_code, response_body_str)."""
    url = BASE_URL + path
    data = json.dumps(body).encode() if body else None
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as ex:
        return 0, str(ex)


def check(name, passed, reason=""):
    status = "PASS" if passed else "FAIL"
    msg = f"[{status}] {name}"
    if reason:
        msg += f" — {reason}"
    print(msg)
    RESULTS.append((name, passed))


# ── Test 1: Basic reachability ───────────────────────────────────────────────
print("\n=== Test 1: Server reachability ===")
code, body = _req("GET", "/", timeout=15)
check("Server responds", code in (200, 301, 302, 307, 308), f"HTTP {code}")


# ── Test 2: Healthcheck endpoint ─────────────────────────────────────────────
print("\n=== Test 2: /api/healthcheck ===")
code, body = _req("GET", "/api/healthcheck", timeout=15)
check("Healthcheck returns 200", code == 200, f"HTTP {code}")
if code == 200:
    try:
        data = json.loads(body)
        checks = data.get("checks", {})
        grammar_count = checks.get("grammar", {}).get("yaml_count", 0)
        l1_count = checks.get("l1-interference", {}).get("yaml_count", 0)
        activity_count = checks.get("activities", {}).get("yaml_count", 0)
        check("Grammar YAMLs accessible", grammar_count > 0, f"{grammar_count} files found")
        check("L1 interference YAMLs accessible", l1_count > 0, f"{l1_count} files found")
        check("Activity YAMLs accessible", activity_count > 0, f"{activity_count} files found")
        check("Grammar count ~302", grammar_count >= 280, f"{grammar_count} files (expect ~302)")
        check("L1 count ~36", l1_count >= 30, f"{l1_count} files (expect ~36)")
        check("Activity count ~220", activity_count >= 200, f"{activity_count} files (expect ~220)")
    except json.JSONDecodeError:
        check("Healthcheck JSON parseable", False, "invalid JSON")
else:
    print(f"  (skipping file-count checks — endpoint not available)")
    print(f"  Body: {body[:200]}")


# ── Test 3: Chat — first message → Content Brief ─────────────────────────────
print("\n=== Test 3: Chat flow ===")
session_id = f"test-{uuid.uuid4().hex[:8]}"
headers = {"X-Session-ID": session_id}

print("  Turn 1: Sending initial request…")
t0 = time.time()
code, body = _req(
    "POST",
    "/cogniesl/get_response",
    body={"message": "I want to teach Present Simple to adult beginners. My students speak Spanish."},
    headers=headers,
    timeout=120,
)
elapsed = time.time() - t0
check("Turn 1 returns 200", code == 200, f"HTTP {code} in {elapsed:.1f}s")

brief_present = False
if code == 200:
    try:
        resp = json.loads(body)
        text = resp.get("response", "")
        brief_present = (
            "present simple" in text.lower()
            and len(text) > 500
        )
        check(
            "Turn 1 contains Content Brief (>500 chars, mentions topic)",
            brief_present,
            f"{len(text)} chars"
        )
        if not brief_present:
            print(f"  Response preview: {text[:300]}")
    except json.JSONDecodeError:
        check("Turn 1 response parseable", False, "invalid JSON")


# ── Test 4: Approval → generation starts ────────────────────────────────────
print("\n=== Test 4: Approval → generation ===")
if brief_present:
    print("  Turn 2: Approving brief…")
    t0 = time.time()
    code, body = _req(
        "POST",
        "/cogniesl/get_response",
        body={"message": "Looks good, go ahead!"},
        headers=headers,
        timeout=300,  # generation can take up to 5 min
    )
    elapsed = time.time() - t0
    check("Turn 2 returns 200", code == 200, f"HTTP {code} in {elapsed:.1f}s")

    if code == 200:
        try:
            resp = json.loads(body)
            text = resp.get("response", "")
            has_download = "/download/" in text
            not_kickoff = len(text) > 200 or has_download
            check(
                "Turn 2 includes download link (generation completed)",
                has_download,
                f"{len(text)} chars, download={'yes' if has_download else 'no'}"
            )
            if not has_download:
                print(f"  Response preview: {text[:400]}")
                check(
                    "Turn 2 is not a one-liner kickoff message",
                    not_kickoff,
                    f"{len(text)} chars"
                )
        except json.JSONDecodeError:
            check("Turn 2 response parseable", False, "invalid JSON")
else:
    print("  (skipping — Turn 1 did not produce a Content Brief)")
    check("Turn 2 approval", False, "skipped — no brief from Turn 1")


# ── Summary ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
passed = sum(1 for _, ok in RESULTS if ok)
total = len(RESULTS)
print(f"Results: {passed}/{total} passed")
if passed < total:
    print("Failed checks:")
    for name, ok in RESULTS:
        if not ok:
            print(f"  ✗ {name}")
print("=" * 50)
sys.exit(0 if passed == total else 1)
