"""Shared model configuration — DeepSeek v4 flash only.

All CogniESL agents and sub-agents use DeepSeek via API exclusively.
No other providers are supported.

DeepSeek models use the format "deepseek/deepseek-v4-flash" which is a
LiteLLM-specific routing prefix. The agents SDK's MultiProvider does not
recognise the "deepseek/" prefix, so we wrap those models in LitellmModel
before returning them. The Agent constructor accepts both string and
LitellmModel instances.
"""
import os


def get_default_model(fallback: str = "deepseek/deepseek-v4-flash"):
    """Return the configured default model, wrapped for Litellm routing."""
    model = os.getenv("DEFAULT_MODEL", fallback)
    return _resolve(model)


def get_bg_default_model(fallback: str = "deepseek/deepseek-v4-flash"):
    """Return the model for background-thread generation."""
    model = os.getenv("BG_DEFAULT_MODEL") or os.getenv("DEFAULT_MODEL", fallback)
    return _resolve(model)


def is_openai_provider() -> bool:
    return False


def _resolve(model: str):
    """Wrap 'deepseek/' models in LitellmModel so the agents SDK can route them.

    The agents SDK's MultiProvider only knows about 'openai/' and 'litellm/'
    prefixes. 'deepseek/deepseek-v4-flash' without a recognised prefix causes
    an 'Unknown prefix: deepseek' error. Wrapping in LitellmModel bypasses
    the prefix parsing and hands the request directly to LiteLLM.

    Note: We explicitly pass base_url to override LiteLLM's default
    /beta endpoint. DeepSeek's documented API base is https://api.deepseek.com.
    """
    if "/" not in model:
        return model
    try:
        from agency_swarm import LitellmModel  # noqa: PLC0415
        if model.startswith("deepseek/"):
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            if deepseek_key:
                return LitellmModel(model=model, api_key=deepseek_key, base_url="https://api.deepseek.com")
            return LitellmModel(model=model, base_url="https://api.deepseek.com")
        if model.startswith("litellm/"):
            return LitellmModel(model=model[len("litellm/"):])
        return LitellmModel(model=model)
    except ImportError:
        return model
