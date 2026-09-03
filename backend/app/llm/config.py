"""Environment-based LLM configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LiteLLM configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="MIDAS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    default_model: str = Field(
        default="openai/gpt-4o-mini",
        description="Primary LiteLLM model identifier (provider/model format).",
    )
    fallback_models: str = Field(
        default="",
        description="Comma-separated ordered fallback LiteLLM model identifiers.",
    )
    temperature: float = 0.2
    max_tokens: int | None = None
    timeout_seconds: int = 60

    # Future LiteLLM Proxy support — when set, client routes through the proxy.
    proxy_base_url: str | None = Field(
        default=None,
        validation_alias="LITELLM_PROXY_BASE_URL",
    )
    proxy_api_key: str | None = Field(
        default=None,
        validation_alias="LITELLM_PROXY_API_KEY",
    )

    @property
    def fallback_model_list(self) -> list[str]:
        if not self.fallback_models.strip():
            return []
        return [m.strip() for m in self.fallback_models.split(",") if m.strip()]


@lru_cache
def get_llm_settings() -> LLMSettings:
    return LLMSettings()
