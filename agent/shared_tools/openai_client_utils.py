"""OpenAI client utilities — DEPRECATED.

CogniESL only supports DeepSeek v4 flash via API. OpenAI is not available.
Image generation is not currently supported (DeepSeek has no image API).
"""
import os


def get_caller_openai_credentials(tool) -> tuple[str, str] | None:
    return None


def get_openai_client(tool=None) -> object:
    raise RuntimeError(
        "OpenAI is not available. CogniESL only supports DeepSeek v4 flash via API. "
        "Image generation is not currently supported."
    )
