"""LiteLLM integration — model invocation without portfolio business logic."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import litellm
from litellm import completion

from app.llm.config import LLMSettings, get_llm_settings
from app.llm.models import MIDASModel, resolve_litellm_model

logger = logging.getLogger(__name__)

# Reduce LiteLLM log noise in application logs.
litellm.suppress_debug_info = True


@dataclass(frozen=True)
class LLMResponse:
    content: str
    model: str
    raw: Any


class LLMClient:
    """Thin wrapper around LiteLLM for MIDAS agents and services."""

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self._settings = settings or get_llm_settings()
        if self._settings.proxy_base_url:
            litellm.api_base = self._settings.proxy_base_url
            if self._settings.proxy_api_key:
                litellm.api_key = self._settings.proxy_api_key

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        logical_model: MIDASModel = MIDASModel.DEFAULT,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Run a chat completion with optional fallback models."""
        model = resolve_litellm_model(logical_model)
        fallbacks = self._settings.fallback_model_list

        call_kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": (
                temperature if temperature is not None else self._settings.temperature
            ),
            "timeout": self._settings.timeout_seconds,
            **kwargs,
        }
        if max_tokens is not None or self._settings.max_tokens is not None:
            call_kwargs["max_tokens"] = max_tokens or self._settings.max_tokens

        if fallbacks:
            call_kwargs["fallbacks"] = fallbacks
            response = litellm.completion_with_fallbacks(**call_kwargs)
        else:
            response = completion(**call_kwargs)

        content = response.choices[0].message.content or ""
        used_model = getattr(response, "model", model)
        logger.debug("LLM completion via model=%s", used_model)
        return LLMResponse(content=content, model=used_model, raw=response)

    def get_adk_litellm_model(self, logical: MIDASModel = MIDASModel.DEFAULT):
        """Return an ADK LiteLlm wrapper for agent construction."""
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=resolve_litellm_model(logical))


@lru_cache
def get_llm_client() -> LLMClient:
    return LLMClient()
