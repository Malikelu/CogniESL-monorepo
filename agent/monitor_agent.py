"""Monitor Agent — quality self-monitoring for CogniESL.

Checks:
1. Output sampler: randomly samples recent generations and validates quality
2. Error tracker: reads failed_jobs, correlates by error type
3. Anomaly detector: compares current metrics to 7-day rolling average

Called by the orchestrator. Results are stored as agent_actions for Marcos to review.
"""
import json
import logging
import os
import random
import sqlite3
import sys
from datetime import datetime, timezone, timedelta

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from auth import db as auth_db

log = logging.getLogger("monitor")

# Quality thresholds
MIN_SLIDE_COUNT = 12          # Minimum expected slides
MIN_PPTX_SIZE_KB = 50         # Minimum PPTX file size in KB
ANOMALY_DEVIATION_PCT = 50    # Flag if metric deviates > 50% from average


def _get_7day_metrics() -> dict:
    """Get key metrics for the last 7 days and the 7 days before that."""
    now = datetime.now(timezone.utc)
    d7 = (now - timedelta(days=7)).isoformat()
    d14 = (now - timedelta(days=14)).isoformat()

    with auth_db._conn() as conn:
        gens_7d = conn.execute(
            "SELECT COUNT(*) FROM generations WHERE created_at >= ?", (d7,)
        ).fetchone()[0]
        gens_prev_7d = conn.execute(
            "SELECT COUNT(*) FROM generations WHERE created_at >= ? AND created_at < ?",
            (d14, d7)
        ).fetchone()[0]

        cost_7d = conn.execute(
            "SELECT COALESCE(SUM(cost_estimate), 0) FROM generations WHERE created_at >= ?",
            (d7,)
        ).fetchone()[0]
        cost_prev_7d = conn.execute(
            "SELECT COALESCE(SUM(cost_estimate), 0) FROM generations WHERE created_at >= ? AND created_at < ?",
            (d14, d7)
        ).fetchone()[0]

        feedback_7d = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE created_at >= ?", (d7,)
        ).fetchone()[0]
        issues_7d = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE created_at >= ? AND rating='issues'",
            (d7,)
        ).fetchone()[0]

    return {
        "gens_7d": gens_7d,
        "gens_prev_7d": gens_prev_7d,
        "cost_7d": cost_7d,
        "cost_prev_7d": cost_prev_7d,
        "feedback_7d": feedback_7d,
        "issues_7d": issues_7d,
        "issue_rate": round(issues_7d / max(feedback_7d, 1) * 100, 1),
    }


def _sample_outputs(sample_size: int = 3) -> list:
    """Randomly sample recent generations and check quality."""
    now = datetime.now(timezone.utc)
    d30 = (now - timedelta(days=30)).isoformat()

    with auth_db._conn() as conn:
        rows = conn.execute(
            """SELECT g.id, g.grammar_point, g.l1_languages, g.job_id,
                      m.slide_count, m.pptx_path
               FROM generations g
               LEFT JOIN materials m ON m.job_id = g.job_id
               WHERE g.created_at >= ?
               ORDER BY RANDOM() LIMIT ?""",
            (d30, sample_size),
        ).fetchall()

    results = []
    for row in rows:
        issues = []
        slide_count = row["slide_count"] or 0
        if slide_count > 0 and slide_count < MIN_SLIDE_COUNT:
            issues.append(f"Low slide count: {slide_count} (expected >= {MIN_SLIDE_COUNT})")

        pptx_path = row["pptx_path"]
        if pptx_path:
            full_path = os.path.join(_root, pptx_path)
            if os.path.exists(full_path):
                size_kb = os.path.getsize(full_path) / 1024
                if size_kb < MIN_PPTX_SIZE_KB:
                    issues.append(f"Small PPTX: {size_kb:.0f}KB (expected >= {MIN_PPTX_SIZE_KB}KB)")
            else:
                issues.append("PPTX file missing")

        results.append({
            "generation_id": row["id"],
            "grammar_point": row["grammar_point"],
            "l1": row["l1_languages"],
            "slide_count": slide_count,
            "issues": issues,
            "passed": len(issues) == 0,
        })

    return results


def _check_anomalies(metrics: dict) -> list:
    """Compare current metrics to previous period. Return list of anomalies."""
    anomalies = []

    # Generation count drop
    if metrics["gens_prev_7d"] > 0:
        deviation = (metrics["gens_7d"] - metrics["gens_prev_7d"]) / metrics["gens_prev_7d"] * 100
        if deviation < -ANOMALY_DEVIATION_PCT:
            anomalies.append(
                f"Generations dropped {abs(deviation):.0f}% vs previous week "
                f"({metrics['gens_prev_7d']} → {metrics['gens_7d']})"
            )

    # Cost spike
    if metrics["cost_prev_7d"] > 0:
        deviation = (metrics["cost_7d"] - metrics["cost_prev_7d"]) / metrics["cost_prev_7d"] * 100
        if deviation > ANOMALY_DEVIATION_PCT:
            anomalies.append(
                f"API cost up {deviation:.0f}% vs previous week "
                f"(${metrics['cost_prev_7d']:.2f} → ${metrics['cost_7d']:.2f})"
            )

    # Issue rate spike
    if metrics["issue_rate"] > 15:
        anomalies.append(f"High issue rate: {metrics['issue_rate']}% (threshold: 15%)")

    return anomalies


def _get_failed_jobs_summary() -> dict:
    """Get summary of recent failed jobs."""
    try:
        from agent import jobs as jobs_db
        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        with sqlite3.connect(jobs_db._DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT job_id, error, created_at FROM jobs WHERE status='error' AND created_at >= ? ORDER BY created_at DESC LIMIT 20",
                (cutoff,)
            ).fetchall()
        return {
            "failed_count": len(rows),
            "recent_failures": [{"job_id": r["job_id"], "error": r["error"]} for r in rows[:5]],
        }
    except Exception:
        return {"failed_count": 0, "recent_failures": []}


def run() -> dict:
    """Run the Monitor Agent. Returns result dict for the orchestrator."""
    log.info("Monitor Agent starting...")

    # 1. Get metrics
    metrics = _get_7day_metrics()

    # 2. Sample outputs
    sampled = _sample_outputs(sample_size=3)
    passed = sum(1 for s in sampled if s["passed"])
    quality_score = round(passed / max(len(sampled), 1) * 100, 1)

    # 3. Check anomalies
    anomalies = _check_anomalies(metrics)

    # 4. Failed jobs
    failed_jobs = _get_failed_jobs_summary()

    # Get grammar points with most issues
    grammar_issues = []
    try:
        with auth_db._conn() as conn:
            rows = conn.execute(
                """SELECT m.grammar_point, COUNT(*) as issue_count
                   FROM feedback f
                   LEFT JOIN materials m ON m.id = f.material_id
                   WHERE f.rating = 'issues' AND f.created_at >= ?
                   GROUP BY m.grammar_point
                   ORDER BY issue_count DESC LIMIT 5""",
                ((datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),)
            ).fetchall()
            grammar_issues = [dict(r) for r in rows if r["grammar_point"]]
    except Exception:
        pass

    # Build result (internal tracking fields prefixed with _)
    result = {
        "type": "monitor_report",
        "quality_score": quality_score,
        "sampled_count": len(sampled),
        "sampled_passed": passed,
        "sampled_details": sampled,
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "metrics_7d": metrics,
        "failed_jobs": failed_jobs,
        "issues_by_grammar": grammar_issues,
    }

    # Log as agent_action
    status = "critical" if anomalies or failed_jobs["failed_count"] > 3 else "warning" if quality_score < 80 else "ok"
    description = (
        f"Monitor: Quality {quality_score}%. {len(anomalies)} anomalies. "
        f"{failed_jobs['failed_count']} failed jobs. Issue rate: {metrics['issue_rate']}%."
    )
    if anomalies:
        description += f" Top anomaly: {anomalies[0]}"

    try:
        action_id = auth_db.log_agent_action("Monitor", "report", description)
        result["action_id"] = action_id
    except Exception:
        pass

    log.info(f"Monitor Agent completed: quality={quality_score}%, anomalies={len(anomalies)}")
    return result
