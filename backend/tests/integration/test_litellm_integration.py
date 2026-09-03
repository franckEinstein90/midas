"""Optional LiteLLM/ADK integration tests — require live credentials."""

import os

import pytest

from app.llm.client import LLMClient


def _has_llm_credentials() -> bool:
    return any(
        os.getenv(key)
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY")
    )


@pytest.mark.integration
@pytest.mark.skipif(not _has_llm_credentials(), reason="No LLM provider credentials configured")
def test_live_litellm_completion() -> None:
    client = LLMClient()
    response = client.complete(
        [{"role": "user", "content": "Reply with the single word: pong"}],
        max_tokens=10,
    )
    assert response.content
    assert len(response.content.strip()) > 0
