"""Orchestrator — coordinates department agents, synthesizes outputs, produces one digest.

Runs on schedule (via Hermes cron or server.py scheduler). For each run:
1. Initialize all 4 agent health records
2. Run each department agent in sequence
3. Correlate findings across agents
4. Produce ONE consolidated digest
5. Log inter-agent routing messages
6. Write agent_actions for Marcos' approval

Not autonomous — all agent outputs are proposals. Marcos approves via dashboard.
"""
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone

# Ensure project root is on sys.path
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from auth import db as auth_db

log = logging.getLogger("orchestrator")

# Agent names (must match what's stored in agent_actions.agent_name)
AGENTS = ["Monitor", "Curator", "Growth", "Intel"]

# Default schedule (in hours) for each run — overridden by cron config
SCHEDULE = {
    "Monitor": 4,    # Every 4 hours
    "Curator": 24,   # Nightly
    "Growth": 24,    # Daily
    "Intel": 24,     # Daily
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _init_agents() -> None:
    """Ensure all agent health records exist."""
    for name in AGENTS:
        auth_db.init_agent_health(name)


def _run_agent(name: str) -> dict:
    """Run a single department agent. Returns result dict or error dict."""
    start = time.time()
    try:
        if name == "Monitor":
            result = _run_monitor()
        elif name == "Curator":
            result = _run_curator()
        elif name == "Growth":
            result = _run_growth()
        elif name == "Intel":
            result = _run_intel()
        else:
            result = {"error": f"Unknown agent: {name}", "type": "unknown"}

        runtime = time.time() - start
        success = "error" not in result
        auth_db.update_agent_health(name, success=success, runtime_seconds=runtime)
        log.info(f"Agent {name}: {'OK' if success else 'FAIL'} ({runtime:.1f}s)")
        return result

    except Exception as e:
        runtime = time.time() - start
        auth_db.update_agent_health(name, success=False, runtime_seconds=runtime)
        log.error(f"Agent {name} crashed: {e}", exc_info=True)
        return {"error": str(e), "type": "crash"}


def _run_monitor() -> dict:
    """Run Monitor Agent — quality self-monitoring."""
    from agent.monitor_agent import run as monitor_run
    return monitor_run()


def _run_curator() -> dict:
    """Run Curator Agent — master repo management."""
    stats = {}
    try:
        from agent.master_repository import cache_stats
        stats = cache_stats()
    except Exception:
        pass

    # Get grammar points with most issues
    recent_issues = []
    try:
        from datetime import timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        with auth_db._conn() as conn:
            rows = conn.execute(
                """SELECT m.grammar_point, COUNT(*) as cnt
                   FROM feedback f
                   LEFT JOIN materials m ON m.id = f.material_id
                   WHERE f.rating = 'issues' AND f.created_at >= ? AND m.grammar_point != ''
                   GROUP BY m.grammar_point ORDER BY cnt DESC LIMIT 5""",
                (cutoff,)
            ).fetchall()
            recent_issues = [dict(r) for r in rows]
    except Exception:
        pass

    action_id = auth_db.log_agent_action(
        "Curator", "report",
        f"Curator check — Cache: {stats.get('common_cached', '?')}/{stats.get('common_total', '?')} combinations. "
        f"Issue-flagged combos: {len(recent_issues)}"
    )

    return {
        "type": "curator_report",
        "cache_stats": stats,
        "issues_by_grammar": recent_issues,
        "action_id": action_id,
    }


def _run_growth() -> dict:
    """Run Growth Agent — marketing, churn prevention, superfans."""
    now = datetime.now(timezone.utc)
    from datetime import timedelta
    d7 = (now - timedelta(days=7)).isoformat()

    # Signups and conversion
    with auth_db._conn() as conn:
        signups_today = conn.execute(
            "SELECT COUNT(*) FROM users WHERE created_at >= ?",
            (now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),)
        ).fetchone()[0]
        signups_week = conn.execute(
            "SELECT COUNT(*) FROM users WHERE created_at >= ?", (d7,)
        ).fetchone()[0]
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        paying = conn.execute(
            "SELECT COUNT(*) FROM users WHERE subscription_tier IN ('pro','founding_member')"
        ).fetchone()[0]

        # Recent generations
        gens_week = conn.execute(
            "SELECT COUNT(*) FROM generations WHERE created_at >= ?", (d7,)
        ).fetchone()[0]

        # Unreviewed positive feedback (testimonials)
        testimonials = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE rating='perfect' AND reviewed=0"
        ).fetchone()[0]

    # Churn risks (reuse existing function)
    churn_risks = auth_db.compute_churn_risk_scores()
    critical_churn = [u for u in churn_risks if u["risk_level"] in ("critical", "high")]

    # Superfans: users with 10+ generations and positive feedback
    superfans = []
    try:
        with auth_db._conn() as conn:
            top_users = conn.execute(
                """SELECT u.id, u.email, u.subscription_tier, COUNT(g.id) as gen_count
                   FROM users u JOIN generations g ON g.user_id = u.id
                   GROUP BY u.id HAVING gen_count >= 10
                   ORDER BY gen_count DESC LIMIT 5"""
            ).fetchall()
            for u in top_users:
                # Check for positive feedback
                fb_count = conn.execute(
                    "SELECT COUNT(*) FROM feedback WHERE user_id=? AND rating IN ('perfect','good')",
                    (u["id"],)
                ).fetchone()[0]
                if fb_count > 0:
                    superfans.append({
                        "user_id": u["id"],
                        "email": u["email"],
                        "tier": u["subscription_tier"],
                        "gen_count": u["gen_count"],
                        "positive_feedback": fb_count,
                    })
    except Exception:
        pass

    action_id = auth_db.log_agent_action(
        "Growth", "report",
        f"Growth: {signups_today} signups today, {signups_week}/week. "
        f"{len(critical_churn)} churn risks. {len(superfans)} superfans. {testimonials} unreviewed testimonials."
    )

    return {
        "type": "growth_report",
        "signups_today": signups_today,
        "signups_week": signups_week,
        "total_users": total_users,
        "paying_users": paying,
        "generations_week": gens_week,
        "churn_risks": critical_churn,
        "superfans": superfans,
        "unreviewed_testimonials": testimonials,
        "action_id": action_id,
    }


def _run_intel() -> dict:
    """Run Intel Agent — business intelligence and cost tracking."""
    now = datetime.now(timezone.utc)
    from datetime import timedelta
    d1 = (now - timedelta(days=1)).isoformat()
    d30 = (now - timedelta(days=30)).isoformat()

    with auth_db._conn() as conn:
        gens_today = conn.execute(
            "SELECT COUNT(*) FROM generations WHERE created_at >= ?", (d1,)
        ).fetchone()[0]
        cost_today = conn.execute(
            "SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at >= ?", (d1,)
        ).fetchone()[0]
        cost_month = conn.execute(
            "SELECT COALESCE(SUM(cost_estimate),0) FROM generations WHERE created_at >= ?", (d30,)
        ).fetchone()[0]

    # Funnel
    funnel = auth_db.get_engagement_funnel()

    # Anomaly: compare today's generation count to 7-day average
    with auth_db._conn() as conn:
        daily_counts = conn.execute(
            """SELECT DATE(created_at) as day, COUNT(*) as cnt
               FROM generations WHERE created_at >= ?
               GROUP BY DATE(created_at) ORDER BY day DESC LIMIT 7""",
            (d30,)
        ).fetchall()
    avg_daily = sum(r["cnt"] for r in daily_counts) / max(len(daily_counts), 1)
    anomaly = None
    if avg_daily > 0 and gens_today < avg_daily * 0.5:
        anomaly = f"Generations today ({gens_today}) are 50% below 7-day average ({avg_daily:.0f})"

    action_id = auth_db.log_agent_action(
        "Intel", "report",
        f"Intel: Today {gens_today} gens, ${cost_today:.2f}. "
        f"Month: ${cost_month:.2f}. "
        f"Funnel: {funnel['stages'][1]['pct']}% activation."
        + (f" ANOMALY: {anomaly}" if anomaly else "")
    )

    return {
        "type": "intel_report",
        "generations_today": gens_today,
        "cost_today": cost_today,
        "cost_month": cost_month,
        "funnel": funnel,
        "anomaly": anomaly,
        "action_id": action_id,
    }


def _correlate_results(results: dict) -> list:
    """Cross-reference findings across agents. Returns list of routing messages."""
    messages = []

    monitor = results.get("Monitor", {})
    growth = results.get("Growth", {})
    intel = results.get("Intel", {})
    curator = results.get("Curator", {})

    # If Monitor detected quality issues → route to Curator
    issues = monitor.get("issues_by_grammar", [])
    if issues:
        messages.append({
            "from": "Monitor", "to": "Curator",
            "type": "regenerate",
            "payload": json.dumps({"grammar_points": [i["grammar"] for i in issues[:3]]}),
        })

    # If Intel detected cost spike → route to Monitor
    if intel.get("anomaly"):
        messages.append({
            "from": "Intel", "to": "Monitor",
            "type": "alert",
            "payload": json.dumps({"anomaly": intel["anomaly"]}),
        })

    # If Growth identified churn risks that are also superfans → route to Intel
    churn = growth.get("churn_risks", [])
    superfans = {s["user_id"] for s in growth.get("superfans", [])}
    valuable_churn = [u for u in churn if u["user_id"] in superfans]
    if valuable_churn:
        messages.append({
            "from": "Growth", "to": "Intel",
            "type": "alert",
            "payload": json.dumps({"valuable_users_at_risk": [u["email"] for u in valuable_churn[:3]]}),
        })

    # If Curator has issues → route to Monitor for regeneration
    curator_issues = curator.get("issues_by_grammar", [])
    if curator_issues:
        messages.append({
            "from": "Curator", "to": "Monitor",
            "type": "regenerate",
            "payload": json.dumps({"count": len(curator_issues), "grammar_points": [i.get("grammar", "") for i in curator_issues[:3]]}),
        })

    return messages


def _synthesize_digest(results: dict) -> dict:
    """Produce ONE consolidated digest from all agent results."""
    now = datetime.now(timezone.utc)

    monitor = results.get("Monitor", {})
    growth = results.get("Growth", {})
    intel = results.get("Intel", {})
    curator = results.get("Curator", {})

    # Agent health
    health_records = auth_db.get_all_agent_health()
    agent_health = {h["agent_name"]: h["status"] for h in health_records}

    # Actions needed
    actions_needed = []

    # Churn risks
    for user in growth.get("churn_risks", []):
        actions_needed.append({
            "type": "churn_risk",
            "priority": "high" if user["risk_level"] == "critical" else "medium",
            "summary": f"{user['email']} — {user['risk_score']}/100 ({user['risk_level']}). {', '.join(user['reasons'][:2])}",
        })

    # Intel anomalies
    if intel.get("anomaly"):
        actions_needed.append({
            "type": "anomaly",
            "priority": "medium",
            "summary": intel["anomaly"],
        })

    # Curator flags
    for issue in monitor.get("issues_by_grammar", []):
        actions_needed.append({
            "type": "content_quality",
            "priority": "medium",
            "summary": f"Quality issue with {issue.get('grammar', 'unknown')} — {issue.get('count', '?')} reports",
        })

    # Pending agent actions summary
    agent_summary = auth_db.get_agent_action_summary()

    digest = {
        "date": now.strftime("%Y-%m-%d"),
        "generated_at": now.isoformat(),
        "orchestrator_status": "completed",
        "agent_health": agent_health,
        "at_a_glance": {
            "gens_today": intel.get("generations_today", 0),
            "signups_today": growth.get("signups_today", 0),
            "cost_today_usd": intel.get("cost_today", 0),
            "cost_month_usd": intel.get("cost_month", 0),
        },
        "actions_needed": actions_needed[:10],  # Cap at 10
        "agent_status": {
            "pending_approvals": agent_summary.get("pending", 0),
            "approved_last_7d": agent_summary.get("approved_last_7d", 0),
            "rejected_last_7d": agent_summary.get("rejected_last_7d", 0),
        },
        "monitor_summary": {
            "quality_score": monitor.get("quality_score", "N/A"),
            "anomalies": monitor.get("anomalies_detected", 0),
            "sampled_outputs": monitor.get("sampled_count", 0),
        },
        "growth_summary": {
            "superfans": len(growth.get("superfans", [])),
            "churn_risks": len(growth.get("churn_risks", [])),
            "testimonials_pending": growth.get("unreviewed_testimonials", 0),
        },
        "intel_summary": {
            "funnel_activation_pct": intel.get("funnel", {}).get("stages", [{}])[1].get("pct", 0),
            "anomaly": intel.get("anomaly"),
        },
        "curator_summary": {
            "cache_coverage": curator.get("cache_stats", {}).get("common_cached", 0),
            "flagged_for_regeneration": len(curator.get("issues_by_grammar", [])),
        },
    }

    return digest


def run_orchestrator(run_type: str = "scheduled") -> dict:
    """Main orchestrator entry point. Run all agents, correlate, synthesize.

    Returns the consolidated digest. Also stores it via save_daily_digest().
    """
    log.info(f"Orchestrator starting (run_type={run_type})")
    run_id = auth_db.create_orchestrator_run(run_type)
    _init_agents()

    results = {}
    agents_run = []
    critical_alerts = 0
    error_msg = ""

    try:
        for name in AGENTS:
            log.info(f"Running {name} Agent...")
            result = _run_agent(name)
            results[name] = result
            agents_run.append(name)

            # Count critical issues
            if "error" in result:
                critical_alerts += 1

            # Write inter-agent routing messages (from previous agents' results)
            if len(agents_run) > 1:
                pending = _correlate_results(results)
                for msg in pending:
                    try:
                        auth_db.create_agent_message(
                            msg["from"], msg["to"], msg["type"],
                            msg.get("payload", "{}")
                        )
                    except Exception:
                        pass

        # Synthesize one digest
        digest = _synthesize_digest(results)

        # Store digest
        try:
            auth_db.save_daily_digest(json.dumps(digest))
        except Exception as e:
            log.error(f"Failed to save digest: {e}")

        # Store in agent_actions for dashboard visibility
        try:
            auth_db.log_agent_action(
                "Orchestrator", "digest",
                f"Digest generated — {len(agents_run)} agents run, "
                f"{len(digest.get('actions_needed', []))} actions needed, "
                f"{digest.get('agent_status', {}).get('pending_approvals', 0)} pending approvals."
            )
        except Exception:
            pass

        auth_db.complete_orchestrator_run(
            run_id,
            agents_run=json.dumps(agents_run),
            critical_alerts=critical_alerts,
        )

        log.info(f"Orchestrator completed: {len(agents_run)} agents, {critical_alerts} errors")
        return digest

    except Exception as e:
        log.error(f"Orchestrator failed: {e}", exc_info=True)
        auth_db.complete_orchestrator_run(run_id, error_message=str(e))
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
    result = run_orchestrator(run_type="manual")
    print(json.dumps(result, indent=2, default=str))
