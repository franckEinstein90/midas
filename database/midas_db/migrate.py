"""Run Alembic migrations programmatically."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from midas_db.config import get_database_url


def _alembic_config() -> Config:
    ini_path = Path(__file__).resolve().parents[1] / "alembic.ini"
    return Config(str(ini_path))


def ensure_pgvector() -> None:
    try:
        engine = create_engine(get_database_url())
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
    except Exception:
        pass


def upgrade_head() -> None:
    ensure_pgvector()
    command.upgrade(_alembic_config(), "head")
