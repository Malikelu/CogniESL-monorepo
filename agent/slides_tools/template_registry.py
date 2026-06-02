"""Persistent slide template registry per project."""
import json
import threading
from pathlib import Path


_index_locks: dict[str, threading.Lock] = {}
_index_locks_guard = threading.Lock()


def _index_lock_for(project_dir: Path) -> threading.Lock:
    """Get or create a per-project lock for thread-safe index access."""
    key = str(project_dir)
    with _index_locks_guard:
        if key not in _index_locks:
            _index_locks[key] = threading.Lock()
        return _index_locks[key]


def load_template_index(project_dir: Path) -> dict:
    """Load the template index JSON for a project."""
    path = project_dir / "_template_index.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_template_index(project_dir: Path, index: dict) -> None:
    """Save the template index JSON for a project."""
    with _index_lock_for(project_dir):
        path = project_dir / "_template_index.json"
        path.write_text(json.dumps(index, indent=2, default=str), encoding="utf-8")


def register_template(project_dir: Path, template_key: str, metadata: dict) -> None:
    """Register a template in the project's index."""
    index = load_template_index(project_dir)
    index[template_key] = metadata
    save_template_index(project_dir, index)


def template_path(project_dir: Path, template_key: str) -> Path | None:
    """Resolve a template_key to its file path, or None if not found."""
    index = load_template_index(project_dir)
    entry = index.get(template_key)
    if entry and "path" in entry:
        candidate = project_dir / entry["path"]
        if candidate.exists():
            return candidate
    # Fallback: check conventional paths
    for suffix in [".html", ".j2", ".jinja"]:
        candidate = project_dir / f"{template_key}{suffix}"
        if candidate.exists():
            return candidate
    return None


def known_template_keys() -> set[str]:
    """Return the set of standard CogniESL slide template keys."""
    return {
        "A0", "A1", "A2", "A3", "A5", "A5b", "A5c", "A6", "A7", "A8",
    }


def is_valid_template_key(key: str) -> bool:
    """Check if a template key is one of the standard types."""
    return key in known_template_keys()
