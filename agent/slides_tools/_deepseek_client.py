"""
Shared DeepSeek client factory for CogniESL sub-agents.

Provides a single source of truth for creating direct AsyncOpenAI clients
pointed at DeepSeek's API. Both ModifySlide and InsertNewSlides use this
instead of maintaining duplicate copies.

Uses DEEPSEEK_API_KEY from .env. No agents SDK, no LiteLLM — calls go
directly to https://api.deepseek.com/chat/completions for minimal latency.
"""

import os
from openai import AsyncOpenAI

# Default model for sub-agents (no "deepseek/" prefix — that's a LiteLLM convention).
DEEPSEEK_FLASH_MODEL = "deepseek-v4-flash"


def resolve_sub_agent_model() -> str:
    """Return the model ID to use for sub-agent LLM calls.

    Reads BG_SUB_AGENT_MODEL or SUB_AGENT_MODEL from env, strips any
    LiteLLM-style provider prefix (e.g. "deepseek/deepseek-v4-flash" →
    "deepseek-v4-flash"), and falls back to DEEPSEEK_FLASH_MODEL.
    """
    model = os.getenv("BG_SUB_AGENT_MODEL") or os.getenv("SUB_AGENT_MODEL", DEEPSEEK_FLASH_MODEL)
    if "/" in model:
        model = model.split("/", 1)[1]
    return model


def make_deepseek_client() -> AsyncOpenAI:
    """Create a direct AsyncOpenAI client pointed at DeepSeek's API.

    Uses DEEPSEEK_API_KEY from .env. Raises RuntimeError if the key is not set.
    """
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required. Set it in .env")
    return AsyncOpenAI(
        api_key=deepseek_key,
        base_url="https://api.deepseek.com",
    )


async def call_deepseek(
    client: AsyncOpenAI,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Call DeepSeek API directly and return the text response.

    Disables thinking mode to minimize latency. In non-thinking mode,
    DeepSeek v4 flash outputs at 120-240 tokens/sec with TTFT 0.6-1.2s,
    vs 30-60s in thinking mode (which defaults to enabled).
    """
    response = await client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        extra_body={"thinking": {"type": "disabled"}},
    )
    return response.choices[0].message.content or ""
