"""Content versioning — Git commit utility for YAML database changes.

Ensures every change to data/ files is committed with a descriptive message.
Called by the orchestrator after any content sync or update.
"""
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = Path(_root) / "data"

log = logging.getLogger("content_versioning")


def git_commit_data_changes(description: str, agent_name: str = "ContentQA") -> bool:
    """Stage and commit all changes in the data/ directory.

    Args:
        description: Short description of the change (used in commit message)
        agent_name: Name of the agent making the change

    Returns:
        True if commit was made, False if nothing to commit or error
    """
    repo_root = Path(_root)

    # Check if data/ has changes
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "data/"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not result.stdout.strip():
            log.info("No changes in data/ to commit")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        log.warning(f"Git status check failed: {e}")
        return False

    # Stage data/ changes
    try:
        subprocess.run(
            ["git", "add", "data/"],
            cwd=str(repo_root),
            capture_output=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        log.error(f"Git add failed: {e}")
        return False

    # Commit with descriptive message
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit_msg = f"[{agent_name}] {description} — {now}"

    try:
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            log.info(f"Committed: {commit_msg}")
            return True
        else:
            log.warning(f"Git commit failed: {result.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        log.error(f"Git commit failed: {e}")
        return False


def get_recent_commits(limit: int = 10) -> list:
    """Get recent commits to the data/ directory."""
    repo_root = Path(_root)
    try:
        result = subprocess.run(
            ["git", "log", f"--max-count={limit}", "--oneline", "--", "data/"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            commits = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    parts = line.split(" ", 1)
                    if len(parts) == 2:
                        commits.append({"hash": parts[0], "message": parts[1]})
            return commits
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
    # Test: check for changes and commit if any
    committed = git_commit_data_changes("Test commit from content versioning module")
    print(f"Committed: {committed}")
    print(f"Recent commits: {get_recent_commits(5)}")
