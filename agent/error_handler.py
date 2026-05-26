"""Comprehensive error handling and recovery for CogniESL Agent."""

from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass


class ErrorSeverity(Enum):
    """Error severity levels."""

    INFO = "info"  # Informational, no action needed
    WARNING = "warning"  # Should be addressed but not blocking
    ERROR = "error"  # Blocking error, requires action
    CRITICAL = "critical"  # System-level failure


@dataclass
class CogniESLError:
    """Standard error structure for CogniESL operations."""

    severity: ErrorSeverity
    error_type: str
    message: str
    user_message: str  # Friendly message for teacher
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "severity": self.severity.value,
            "error_type": self.error_type,
            "message": self.message,
            "user_message": self.user_message,
            "suggestion": self.suggestion,
            "context": self.context,
        }


class ErrorHandler:
    """Centralized error handling with recovery strategies."""

    # Error registry with helpful messages
    ERROR_MESSAGES = {
        "GRAMMAR_NOT_FOUND": {
            "user": "I couldn't find '{topic}' in the database. Available topics include: {available}",
            "suggestion": "Try one of the suggested topics, or spell it differently.",
        },
        "L1_NOT_FOUND": {
            "user": "I don't have L1 data for '{language}'. Available languages: {available}",
            "suggestion": "Choose from the available languages, or request 'mixed' if you have multiple L1s.",
        },
        "INCOMPLETE_REQUIREMENTS": {
            "user": "I need a bit more info before I can generate materials.",
            "suggestion": "Please provide: topic, student language background, age group, level, and what format you need (slides/worksheet/both).",
        },
        "NO_CONFIRMATION": {
            "user": "Before I start generating, let me confirm your requirements are correct.",
            "suggestion": "Review the summary and say 'yes' when you're ready.",
        },
        "SLIDE_GENERATION_FAILED": {
            "user": "I had trouble generating {slide_name} after multiple attempts. Using fallback HTML instead.",
            "suggestion": "The fallback slide has basic content. You may want to edit it manually.",
        },
        "VALIDATION_FAILED": {
            "user": "Some validation checks didn't pass: {failures}",
            "suggestion": "I'm attempting to fix these automatically. If it continues to fail, there may be a system issue.",
        },
        "DATABASE_ERROR": {
            "user": "I encountered an issue accessing the database.",
            "suggestion": "Please try again. If the problem persists, the database files may need to be checked.",
        },
        "FILE_NOT_FOUND": {
            "user": "I couldn't find the required file: {file}",
            "suggestion": "Check that the file exists and is in the correct location.",
        },
    }

    @staticmethod
    def grammar_not_found(
        topic: str, available: list
    ) -> CogniESLError:
        """Handle grammar topic not found."""
        available_str = ", ".join(available[:5])
        if len(available) > 5:
            available_str += f", and {len(available) - 5} more"

        return CogniESLError(
            severity=ErrorSeverity.ERROR,
            error_type="GRAMMAR_NOT_FOUND",
            message=f"Grammar file not found: {topic}",
            user_message=f"I couldn't find '{topic}' in the database. Available topics include: {available_str}",
            suggestion="Try one of the suggested topics, or spell it differently.",
            context={"requested_topic": topic, "available_count": len(available)},
        )

    @staticmethod
    def l1_not_found(
        language: str, available: list
    ) -> CogniESLError:
        """Handle L1 language not found."""
        available_str = ", ".join(available[:5])
        if len(available) > 5:
            available_str += f", and {len(available) - 5} more"

        return CogniESLError(
            severity=ErrorSeverity.WARNING,
            error_type="L1_NOT_FOUND",
            message=f"L1 interference file not found: {language}",
            user_message=f"I don't have specific L1 data for '{language}'. I'll generate general materials instead. Available languages: {available_str}",
            suggestion="Choose a language I have data for if you want L1-targeted materials.",
            context={"requested_language": language, "available_count": len(available)},
        )

    @staticmethod
    def incomplete_requirements(missing: list) -> CogniESLError:
        """Handle incomplete teacher requirements."""
        missing_str = ", ".join(missing)
        return CogniESLError(
            severity=ErrorSeverity.ERROR,
            error_type="INCOMPLETE_REQUIREMENTS",
            message=f"Missing required information: {missing_str}",
            user_message="I need a bit more info before I can generate materials.",
            suggestion=f"Please provide: {missing_str}",
            context={"missing_fields": missing},
        )

    @staticmethod
    def no_confirmation(requirements: Dict[str, Any]) -> CogniESLError:
        """Handle unconfirmed requirements."""
        return CogniESLError(
            severity=ErrorSeverity.WARNING,
            error_type="NO_CONFIRMATION",
            message="Requirements not explicitly confirmed by teacher",
            user_message="Before I start generating, let me confirm your requirements are correct.",
            suggestion="Review the summary above and say 'yes' when you're ready.",
            context={"requirements": requirements},
        )

    @staticmethod
    def slide_generation_failed(
        slide_name: str, attempts: int, reason: str
    ) -> CogniESLError:
        """Handle slide generation failure (fallback used)."""
        return CogniESLError(
            severity=ErrorSeverity.WARNING,
            error_type="SLIDE_GENERATION_FAILED",
            message=f"Failed to generate {slide_name} after {attempts} attempts",
            user_message=f"I had trouble generating {slide_name} after {attempts} attempts. Using fallback HTML instead.",
            suggestion="The fallback slide has basic content. You may want to edit it manually.",
            context={
                "slide_name": slide_name,
                "attempts": attempts,
                "reason": reason,
            },
        )

    @staticmethod
    def validation_failed(
        validator_name: str, failures: list
    ) -> CogniESLError:
        """Handle validation failure."""
        failures_str = "; ".join(failures[:3])
        if len(failures) > 3:
            failures_str += f"; and {len(failures) - 3} more"

        return CogniESLError(
            severity=ErrorSeverity.ERROR,
            error_type="VALIDATION_FAILED",
            message=f"Validation failed: {failures_str}",
            user_message=f"Some validation checks didn't pass: {failures_str}",
            suggestion="I'm attempting to fix these automatically. If it continues to fail, there may be a system issue.",
            context={
                "validator": validator_name,
                "failures": failures,
            },
        )

    @staticmethod
    def database_error(operation: str, reason: str) -> CogniESLError:
        """Handle database access errors."""
        return CogniESLError(
            severity=ErrorSeverity.ERROR,
            error_type="DATABASE_ERROR",
            message=f"Database error during {operation}: {reason}",
            user_message="I encountered an issue accessing the database.",
            suggestion="Please try again. If the problem persists, the database files may need to be checked.",
            context={"operation": operation, "reason": reason},
        )

    @staticmethod
    def file_not_found(file_path: str) -> CogniESLError:
        """Handle file not found errors."""
        return CogniESLError(
            severity=ErrorSeverity.ERROR,
            error_type="FILE_NOT_FOUND",
            message=f"File not found: {file_path}",
            user_message=f"I couldn't find the required file: {file_path}",
            suggestion="Check that the file exists and is in the correct location.",
            context={"file_path": file_path},
        )

    @staticmethod
    def recover_from_grammar_not_found(
        user_input: str, available_topics: list
    ) -> str:
        """Generate recovery suggestion for grammar topic."""
        # Find closest match
        user_norm = user_input.lower().replace(" ", "_")
        for topic in available_topics:
            if user_norm in topic or topic in user_norm:
                return f"Did you mean '{topic}'? I can create materials for that."

        # Suggest similar topics
        if available_topics:
            return f"Similar topics I can help with: {', '.join(available_topics[:3])}"

        return "Unfortunately, I don't have any grammar topics in the database. Please check that the data folder is set up correctly."

    @staticmethod
    def recover_from_l1_not_found(
        user_input: str, available_languages: list
    ) -> str:
        """Generate recovery suggestion for L1 language."""
        # Find closest match
        user_norm = user_input.lower().replace(" ", "_")
        for lang in available_languages:
            if user_norm in lang or lang in user_norm:
                return f"I have data for '{lang}'. Would that work for your students?"

        # Suggest available languages
        if available_languages:
            return f"I have data for: {', '.join(available_languages[:5])}. Which of these applies to your students?"

        return "I don't have L1 interference data loaded. I can create general materials without L1-specific targeting."

    @staticmethod
    def format_error_for_teacher(error: CogniESLError) -> str:
        """Format error message for teacher presentation."""
        msg = error.user_message

        if error.suggestion:
            msg += f"\n\n**Suggestion**: {error.suggestion}"

        if error.severity == ErrorSeverity.CRITICAL:
            msg += "\n\n⚠️ This is a critical issue. Please contact support if it persists."

        return msg
