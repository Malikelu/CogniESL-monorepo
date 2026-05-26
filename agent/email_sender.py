"""
CogniESL email sender — sends a branded completion email via Resend.

Setup:
  1. Sign up at resend.com (free: 3,000 emails/month)
  2. Add RESEND_API_KEY to .env
  3. Add COGNIESL_BASE_URL to .env (e.g. https://cogniesl.com or http://localhost:8080)
  4. Verify your sending domain at resend.com/domains (or use onboarding@resend.dev for testing)
"""
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def send_completion_email(
    to_email: str,
    job_id: str,
    project_name: str,
    grammar_point: str,
    l1_languages: str,
    file_paths: list[str],
    snapshot_path: str | None = None,
) -> bool:
    """
    Send a branded completion email with download buttons.
    Returns True on success, False on failure (never raises).
    """
    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key:
        logger.warning("RESEND_API_KEY not set — skipping completion email")
        return False

    base_url = os.getenv("COGNIESL_BASE_URL", "http://localhost:8080").rstrip("/")

    try:
        import resend  # pip install resend
        resend.api_key = api_key
    except ImportError:
        logger.warning("resend package not installed — run: pip install resend")
        return False

    # Build snapshot preview HTML (if provided)
    snapshot_html = _build_snapshot_html(snapshot_path) if snapshot_path else ""

    # Check if an HTML bundle is in the file list (it always should be now)
    has_html_bundle = any(fp.endswith(".html") for fp in file_paths)

    # Build download button HTML for each file
    buttons_html = _build_buttons(base_url, job_id, file_paths)
    l1_display = l1_languages or "your students"
    subject = f"Your {grammar_point} materials are ready! 🎉"

    # "How to open" tip block — shown only when HTML bundle is present
    html_tip_html = ""
    if has_html_bundle:
        html_tip_html = """
          <div style="margin:20px 0 28px;padding:14px 18px;background:#f0fdf4;border-left:4px solid #1baa6e;border-radius:0 6px 6px 0;">
            <p style="margin:0 0 6px;font-size:13px;font-weight:700;color:#065f46;text-transform:uppercase;letter-spacing:0.5px;">🎬 Your presentation uses the richer HTML format</p>
            <p style="margin:0;font-size:13px;color:#374151;line-height:1.6;">
              It keeps all animations and visual design exactly as created — better than PowerPoint.<br>
              <strong>To present:</strong> download the .html file → double-click → press <strong>F</strong> for fullscreen → arrow keys to navigate.
            </p>
          </div>"""

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f8f9fa;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:40px 20px;">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

        <!-- Header — white background, brand wordmark as styled text (SVG not supported in email clients) -->
        <tr><td style="background:#ffffff;padding:28px 40px 20px;text-align:center;border-bottom:4px solid #0b7272;">
          <p style="margin:0;font-size:26px;font-weight:500;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:0.5px;">
            <span style="color:#0b7272;">Cogni</span><span style="color:#1baa6e;letter-spacing:2px;">ESL</span>
          </p>
          <p style="margin:6px 0 0;color:#6b7280;font-size:13px;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">L1-aware teaching materials, made in minutes.</p>
        </td></tr>

        <!-- Body -->
        <tr><td style="padding:40px 40px 32px;">
          <h2 style="margin:0 0 8px;color:#0b7272;font-size:22px;">Your materials are ready! 🎉</h2>
          <p style="margin:0 0 20px;color:#4b5563;font-size:16px;line-height:1.6;">
            Here are your <strong>{grammar_point}</strong> materials for {l1_display} speakers.
            Click any button below to download:
          </p>

          {snapshot_html}

          {html_tip_html}

          {buttons_html}

          <hr style="border:none;border-top:1px solid #e5e7eb;margin:32px 0;">

          <p style="margin:0;color:#6b7280;font-size:14px;line-height:1.6;">
            <strong>Need to change something?</strong> Go back to your CogniESL chat and tell me
            which slide to update — I'll regenerate just that slide in about a minute,
            without touching the rest.
          </p>
        </td></tr>

        <!-- Footer -->
        <tr><td style="background:#f9fafb;padding:20px 40px;text-align:center;">
          <p style="margin:0;color:#9ca3af;font-size:12px;">
            CogniESL · Unsubscribe · You received this because you requested materials
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""

    try:
        resend.Emails.send({
            "from": os.getenv("COGNIESL_FROM_EMAIL", "CogniESL <onboarding@resend.dev>"),
            "to": [to_email],
            "subject": subject,
            "html": html,
        })
        logger.info(f"Completion email sent to {to_email} for job {job_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send completion email for job {job_id}: {e}")
        return False


def _build_snapshot_html(snapshot_path: str) -> str:
    """Embed slide preview PNG as base64 inline image in the email."""
    import base64
    try:
        data = Path(snapshot_path).read_bytes()
        b64 = base64.b64encode(data).decode()
        return f"""
          <div style="margin-bottom:24px;text-align:center;">
            <img src="data:image/png;base64,{b64}"
                 style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.12);"
                 alt="Preview of your materials"/>
            <p style="margin:8px 0 0;font-size:12px;color:#9ca3af;">Preview of your materials</p>
          </div>"""
    except Exception:
        return ""  # Non-fatal — skip preview if image unavailable


def _build_buttons(base_url: str, job_id: str, file_paths: list[str]) -> str:
    """Build an HTML block of download buttons — one per file."""
    rows = []
    for fp in file_paths:
        filename = Path(fp).name
        label, emoji = _label_for_file(filename)
        url = f"{base_url}/download/{job_id}/{filename}"
        rows.append(f"""
          <tr><td style="padding:6px 0;">
            <a href="{url}" style="display:block;text-align:center;padding:14px 24px;
               background:#0b7272;color:#ffffff;text-decoration:none;border-radius:8px;
               font-size:15px;font-weight:600;">
              {emoji} {label}
            </a>
          </td></tr>""")
    return f'<table width="100%" cellpadding="0" cellspacing="0">{"".join(rows)}</table>'


def _label_for_file(filename: str) -> tuple[str, str]:
    """Return (human label, emoji) for a file."""
    name = filename.lower()
    if name.endswith(".pptx"):
        return "Download Slides (PowerPoint)", "📊"
    if "worksheet" in name and name.endswith(".pdf"):
        return "Download Worksheet (PDF)", "📄"
    if "worksheet" in name and name.endswith(".docx"):
        return "Download Worksheet (Word)", "📝"
    if "activity" in name and name.endswith(".pdf"):
        return "Download Activity Guide (PDF)", "🎮"
    if "activity" in name and name.endswith(".docx"):
        return "Download Activity Guide (Word)", "🎮"
    if name.endswith(".html"):
        return "Download Presentation (HTML — full animations, works offline)", "🎬"
    if "flashcard" in name and name.endswith(".pdf"):
        return "Download Flashcards (PDF)", "🃏"
    if "progress-tracker" in name and name.endswith(".pdf"):
        return "Download Progress Tracker (PDF)", "📋"
    if name.endswith(".pdf"):
        return "Download PDF", "📄"
    if name.endswith(".docx"):
        return "Download Document (Word)", "📝"
    return f"Download {filename}", "📥"


def send_daily_digest_email(digest_data: dict) -> None:
    """Send the Marcos daily digest email via Resend.

    digest_data: JSON from /api/admin/daily-digest endpoint.
    Reads FOUNDER_EMAIL env var for recipient. Silently skips if not configured.
    """
    founder_email = os.getenv("FOUNDER_EMAIL", "").strip()
    if not founder_email:
        logger.info("FOUNDER_EMAIL not set — skipping daily digest email")
        return
    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key:
        logger.warning("RESEND_API_KEY not set — skipping daily digest email")
        return
    import json, urllib.request, urllib.error
    a = digest_data.get("at_a_glance", {})
    actions = digest_data.get("actions_needed", [])
    ag = digest_data.get("agent_status", {})
    sh = digest_data.get("system_health", {})
    date = digest_data.get("date", "today")
    lines = [
        f"COGNIESL DAILY DIGEST — {date}",
        "",
        "AT A GLANCE",
        f"  Generations: {a.get('gens_today', 0)}  |  Signups: {a.get('signups_today', 0)}",
        f"  Active (7d): {a.get('active_users_7d', 0)}  |  MRR: ${a.get('mrr_usd', 0):.2f}",
        f"  API cost today: ${a.get('api_cost_today_usd', 0):.4f}  |  Month: ${a.get('api_cost_month_usd', 0):.2f}",
        "",
    ]
    if actions:
        lines.append("ACTIONS NEEDED")
        for act in actions:
            icon = "🔴" if act["priority"] == "high" else "🟡"
            lines.append(f"  {icon} [{act['type']}] {act['summary']}")
        lines.append("")
    lines.extend([
        "SYSTEM HEALTH",
        f"  Approved jobs (7d): {sh.get('failed_jobs_7d', 'N/A')} failed",
        f"  Content issue rate: {sh.get('content_issue_rate_pct', 0)}%",
        f"  Unreviewed feedback: {sh.get('unreviewed_feedback', 0)}",
        f"  Users at risk: {sh.get('users_at_risk', 0)}",
        f"  Agent pending: {ag.get('pending_approvals', 0)}",
        "",
        "Full dashboard: " + os.getenv("COGNIESL_BASE_URL", "https://cogniesl.com") + "/admin",
    ])
    html_body = "<pre style='font-family:system-ui,sans-serif;font-size:14px;line-height:1.6;'>" + "\n".join(lines) + "</pre>"
    payload = json.dumps({
        "from": os.getenv("EMAIL_FROM", "CogniESL <onboarding@resend.dev>"),
        "to": [founder_email],
        "subject": f"CogniESL Daily Digest — {date}",
        "html": html_body,
    }).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req)
        logger.info(f"Daily digest email sent to {founder_email} (status {resp.status})")
    except urllib.error.HTTPError as e:
        logger.error(f"Failed to send digest email: {e.code} {e.read().decode()}")
