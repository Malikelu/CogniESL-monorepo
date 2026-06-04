"""Shared model configuration — DeepSeek v4 flash only.

All CogniESL agents and sub-agents use DeepSeek via API exclusively.
No other providers are supported. This is enforced at every level.
"""
import os


def get_default_model(fallback: str = "deepseek/deepseek-v4-flash"):
    """Return the configured default model."""
    return os.getenv("DEFAULT_MODEL", fallback)


def get_bg_default_model(fallback: str = "deepseek/deepseek-v4-flash"):
    """Return the model for background-thread generation."""
    return os.getenv("BG_DEFAULT_MODEL", fallback)


def is_openai_provider() -> bool:
    return False
