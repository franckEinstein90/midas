"""Application-wide configuration."""

from functools import lru_cache
import json
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]
EMBEDDED_CONNECTION_FILE = REPO_ROOT / ".midas" / "database.json"


def _load_embedded_url() -> str | None:
    if not EMBEDDED_CONNECTION_FILE.exists():
        return None
    try:
        data = json.loads(EMBEDDED_CONNECTION_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data.get("database_url")


class AppSettings(BaseSettings):
    """Environment-based application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(default="postgresql://postgres@127.0.0.1:5432/midas")
    reporting_currency: str = "CAD"
    log_level: str = "INFO"

    def model_post_init(self, __context: object) -> None:
        if os.getenv("DATABASE_URL"):
            return
        if embedded := _load_embedded_url():
            object.__setattr__(self, "database_url", embedded)


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
