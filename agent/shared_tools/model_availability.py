"""Model availability hints — DeepSeek v4 flash only.

Image and video generation are not available (DeepSeek has no media API).
"""
from __future__ import annotations


def direct_openai_available(tool=None) -> bool:
    return False


def image_model_availability_message(tool=None, *, failed_requirement: str | None = None) -> str:
    return (
        "Image generation is not available. CogniESL only supports DeepSeek v4 flash.\n"
        "DeepSeek does not provide an image generation API."
        if failed_requirement is None
        else f"{failed_requirement}\n\nImage generation not available — DeepSeek only."
    )


def video_model_availability_message(tool=None, *, failed_requirement: str | None = None) -> str:
    return (
        "Video generation is not available. CogniESL only supports DeepSeek v4 flash.\n"
        "DeepSeek does not provide a video generation API."
        if failed_requirement is None
        else f"{failed_requirement}\n\nVideo generation not available — DeepSeek only."
    )
