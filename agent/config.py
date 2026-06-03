"""Shared model configuration helpers — read by all agents at startup."""
import os


def get_default_model(fallback: str = "gpt-4o-mini"):
    """Return the configured default model for standard (main-thread) agents."""
    model = os.getenv("DEFAULT_MODEL", fallback)
    return _resolve(model)


def get_bg_default_model(fallback: str = "gpt-4o-mini"):
    """Return the model for background-thread generation.

    Uses BG_DEFAULT_MODEL if set, otherwise falls back to DEFAULT_MODEL.

    Why this exists: DeepSeek via LiteLLM works in the main (FastAPI) thread
    but can fail silently in threading.Thread + asyncio.run() contexts because
    LiteLLM's env-var key resolution behaves differently. Setting BG_DEFAULT_MODEL
    routes background traffic through OpenRouter (confirmed working) while keeping
    the main thread on the cheaper direct-DeepSeek path.

    Railway env var guide:
      BG_DEFAULT_MODEL=openrouter/deepseek/deepseek-v4-flash   # production (cheap)
      BG_DEFAULT_MODEL=openrouter/owl-alpha                    # early testing (free)
      (leave unset to use DEFAULT_MODEL — works if direct DeepSeek is stable)
    """
    model = os.getenv("BG_DEFAULT_MODEL") or os.getenv("DEFAULT_MODEL", fallback)
    return _resolve(model)


def is_openai_provider() -> bool:
    """Return True when the configured provider is OpenAI (not LiteLLM).

    OpenAI model IDs never contain a slash (e.g. 'gpt-4o-mini', 'o3').
    Any 'provider/model' string (e.g. 'anthropic/claude-sonnet-4-6',
    'litellm/gemini/gemini-2.5-flash') is treated as a LiteLLM-routed model.
    """
    return "/" not in os.getenv("DEFAULT_MODEL", "")


def _resolve(model: str):
    """Route 'provider/model' strings through LitellmModel.

    Handles both explicit 'litellm/<model>' and bare 'provider/model' forms.
    OpenAI model IDs contain no slash, so they pass through unchanged.

    For deepseek/ models, DEEPSEEK_API_KEY is passed explicitly rather than
    relying on LiteLLM's env-var resolution, which can fail in background
    threading.Thread contexts.
    """
    if "/" not in model:
        return model
    bare = model[len("litellm/"):] if model.startswith("litellm/") else model
    try:
        from agency_swarm import LitellmModel  # noqa: PLC0415
        if bare.startswith("deepseek/"):
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            if deepseek_key:
                return LitellmModel(model=bare, api_key=deepseek_key)
        return LitellmModel(model=bare)
    except ImportError:
        return model
