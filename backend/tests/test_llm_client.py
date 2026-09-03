"""LLM client tests with mocked LiteLLM boundary."""

from unittest.mock import MagicMock, patch

from app.llm.client import LLMClient
from app.llm.config import LLMSettings


def test_llm_client_completion_uses_mocked_litellm() -> None:
    settings = LLMSettings(
        default_model="openai/gpt-4o-mini",
        fallback_models="",
        temperature=0.1,
    )
    client = LLMClient(settings=settings)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_response.model = "openai/gpt-4o-mini"

    with patch("app.llm.client.completion", return_value=mock_response) as mock_completion:
        result = client.complete([{"role": "user", "content": "Hello"}])

    mock_completion.assert_called_once()
    assert result.content == "Test response"
    assert result.model == "openai/gpt-4o-mini"


def test_llm_client_fallback_path() -> None:
    settings = LLMSettings(
        default_model="openai/gpt-4o-mini",
        fallback_models="anthropic/claude-3-haiku-20240307",
    )
    client = LLMClient(settings=settings)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Fallback ok"))]
    mock_response.model = "anthropic/claude-3-haiku-20240307"

    with patch(
        "app.llm.client.litellm.completion_with_fallbacks",
        return_value=mock_response,
    ) as mock_fallback:
        result = client.complete([{"role": "user", "content": "Hello"}])

    mock_fallback.assert_called_once()
    call_kwargs = mock_fallback.call_args.kwargs
    assert call_kwargs["fallbacks"] == ["anthropic/claude-3-haiku-20240307"]
    assert result.content == "Fallback ok"
