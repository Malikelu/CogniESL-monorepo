"""Audit logging for CogniESL Agent — tracks all tool calls and results for debugging."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class AuditLogger:
    """Centralized audit logging for all agent operations."""

    def __init__(self, project_name: Optional[str] = None):
        """Initialize audit logger with optional project context."""
        self.project_name = project_name or "cogniesl"
        self.logs = []
        self.setup_logging()

    def setup_logging(self):
        """Configure Python logging to file and console."""
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"cogniesl_audit_{timestamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("CogniESL.Audit")
        self.log_file = log_file

    def log_requirement_gathered(self, requirements: Dict[str, Any]):
        """Log when teacher requirements are gathered."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "REQUIREMENT_GATHERED",
            "data": requirements,
        }
        self.logs.append(entry)
        self.logger.info(f"Requirements gathered: {json.dumps(requirements)}")

    def log_database_search(
        self,
        search_type: str,
        query: str,
        results_count: int,
        status: str = "SUCCESS",
    ):
        """Log database search operations."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "DATABASE_SEARCH",
            "search_type": search_type,
            "query": query,
            "results_count": results_count,
            "status": status,
        }
        self.logs.append(entry)
        self.logger.info(
            f"DB Search [{search_type}] '{query}': {results_count} results"
        )

    def log_tool_call(
        self,
        tool_name: str,
        input_params: Dict[str, Any],
        status: str = "STARTED",
    ):
        """Log tool invocation."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "TOOL_CALL",
            "tool_name": tool_name,
            "status": status,
            "input_params": self._sanitize(input_params),
        }
        self.logs.append(entry)
        self.logger.info(f"Tool: {tool_name} | Status: {status}")

    def log_tool_result(
        self,
        tool_name: str,
        status: str,
        result_summary: str,
        error: Optional[str] = None,
    ):
        """Log tool result."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "TOOL_RESULT",
            "tool_name": tool_name,
            "status": status,
            "result_summary": result_summary,
            "error": error,
        }
        self.logs.append(entry)
        if error:
            self.logger.error(f"Tool {tool_name} failed: {error}")
        else:
            self.logger.info(f"Tool {tool_name} result: {result_summary}")

    def log_slide_generation(
        self,
        slide_name: str,
        attempt: int,
        status: str,
        error: Optional[str] = None,
    ):
        """Log slide generation attempts."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "SLIDE_GENERATION",
            "slide_name": slide_name,
            "attempt": attempt,
            "status": status,
            "error": error,
        }
        self.logs.append(entry)
        if error:
            self.logger.warning(
                f"Slide {slide_name} (attempt {attempt}) failed: {error}"
            )
        else:
            self.logger.info(f"Slide {slide_name} (attempt {attempt}) {status}")

    def log_validation(
        self,
        validator_name: str,
        checks_passed: int,
        checks_failed: int,
        checks_warned: int,
    ):
        """Log validation results."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "VALIDATION",
            "validator": validator_name,
            "passed": checks_passed,
            "failed": checks_failed,
            "warned": checks_warned,
        }
        self.logs.append(entry)
        self.logger.info(
            f"Validation [{validator_name}]: {checks_passed} passed, "
            f"{checks_failed} failed, {checks_warned} warned"
        )

    def log_error(self, error_type: str, message: str, context: Optional[Dict] = None):
        """Log errors with context."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "ERROR",
            "error_type": error_type,
            "message": message,
            "context": context,
        }
        self.logs.append(entry)
        self.logger.error(f"{error_type}: {message}")

    def log_material_delivery(self, files: Dict[str, str]):
        """Log when materials are delivered to teacher."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "MATERIAL_DELIVERY",
            "files": files,
        }
        self.logs.append(entry)
        self.logger.info(f"Materials delivered: {json.dumps(files)}")

    def dump_audit_log(self) -> str:
        """Return formatted audit log as JSON."""
        return json.dumps(self.logs, indent=2)

    def save_audit_log(self, project_dir: Path):
        """Save audit log to project directory."""
        audit_file = project_dir / "audit.json"
        with open(audit_file, "w") as f:
            json.dump(self.logs, f, indent=2)
        self.logger.info(f"Audit log saved: {audit_file}")

    def _sanitize(self, obj: Any) -> Any:
        """Remove sensitive data from logged objects."""
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self._sanitize(item) for item in obj]
        if isinstance(obj, str) and len(obj) > 500:
            return f"{obj[:100]}...(truncated {len(obj)-100} chars)"
        return obj
