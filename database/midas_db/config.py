"""Connection settings for embedded Postgres and Alembic."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONNECTION_FILE = REPO_ROOT / ".midas" / "database.json"


def load_embedded_database_url() -> str | None:
    if not CONNECTION_FILE.exists():
        return None
    try:
        data = json.loads(CONNECTION_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data.get("database_url")


@lru_cache
def get_database_url() -> str:
    if url := os.getenv("DATABASE_URL"):
        return url
    if url := load_embedded_database_url():
        return url
    return "postgresql://postgres@127.0.0.1:5432/midas"
