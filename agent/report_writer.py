"""Agent report generation stub.

This module is the extension point for the self-running agent system.
Each agent (QA, CMO, CFO, Curator, Secretary) will have a corresponding
function here that:
1. Queries relevant data from the databases
2. Uses LiteLLM/Claude to generate a text report
3. Stores a summary as an agent_action (status='pending') for Marcos to review

Called by scheduled tasks or on-demand triggers. Not yet wired to a scheduler.
"""
import os
import sys
from datetime import datetime, timezone


def _log_action(agent_name: str, action_type: str, description: str) -> str:
    """Log an agent action to the database. Returns action_id."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from auth import db as auth_db
    return auth_db.log_agent_action(agent_name, action_type, description)


def generate_health_report() -> str:
    """Generate a basic system health report. Returns action_id.

    This is the simplest report — pure data, no AI needed. Useful as a
    template for more complex agent reports.
    """
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from auth import db as auth_db
    stats = auth_db.get_engagement_stats()
    summary = auth_db.get_feedback_summary()
    agent_sum = auth_db.get_agent_action_summary()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    description = (
        f"System Health Report — {now}\n"
        f"Active users (7d): {stats['wau']} · Total users: {stats['total_users']}\n"
        f"Total generations: {stats['total_gens']} · Avg per user: {stats['avg_gens_per_user']}\n"
        f"Feedback: {summary['total']} total ({summary['unreviewed']} unreviewed)\n"
        f"Agent pending actions: {agent_sum['pending']}\n"
    )
    return _log_action("Secretary", "report", description)


# ─── Future agent report functions (stubs) ────────────────────────────────────

def generate_qa_report():
    """QA Agent: Analyze failed jobs, audit logs, error patterns."""
    raise NotImplementedError("QA Agent report — build in Phase I-3")


def generate_cmo_report():
    """CMO Agent: Marketing metrics, social mentions, growth signals."""
    raise NotImplementedError("CMO Agent report — build in Phase I-4")


def generate_cfo_report():
    """CFO Agent: Revenue, costs, churn risk, unit economics."""
    raise NotImplementedError("CFO Agent report — build in Phase I-3")


def generate_curator_report():
    """Curator Agent: Master repo coverage, pre-generation priorities."""
    raise NotImplementedError("Curator Agent report — build in Phase I-4")


def generate_secretary_report():
    """Secretary Agent: Email classification summary, pending replies."""
    raise NotImplementedError("Secretary Agent report — build in Phase I-6")
