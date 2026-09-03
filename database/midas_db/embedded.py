"""Embedded PostgreSQL (pgembed) for local development — no Docker required."""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

from midas_db.config import REPO_ROOT

logger = logging.getLogger(__name__)

MIDAS_STATE_DIR = REPO_ROOT / ".midas"
PGDATA_DIR = MIDAS_STATE_DIR / "pgdata"
CONNECTION_FILE = MIDAS_STATE_DIR / "database.json"
DEFAULT_DB_NAME = "midas"


def get_connection_file() -> Path:
    return CONNECTION_FILE


def load_embedded_database_url() -> str | None:
    if not CONNECTION_FILE.exists():
        return None
    data = json.loads(CONNECTION_FILE.read_text(encoding="utf-8"))
    return data.get("database_url")


def _write_connection_file(database_url: str, port: int) -> None:
    MIDAS_STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "database_url": database_url,
        "host": "127.0.0.1",
        "port": port,
        "database": DEFAULT_DB_NAME,
        "user": "postgres",
    }
    CONNECTION_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _ensure_database(server, db_name: str) -> None:
    exists = server.psql(
        f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';"
    )
    if "(1 row)" in exists or "1 row" in exists:
        return
    server.psql(f"CREATE DATABASE {db_name};")


def _enable_pgvector(server) -> bool:
    import pgembed

    if pgembed.has_extension("pgvector"):
        server.create_extension("vector")
        logger.info("pgvector extension enabled.")
        return True

    try:
        server.psql("CREATE EXTENSION IF NOT EXISTS vector;")
        logger.info("pgvector extension enabled via SQL.")
        return True
    except Exception as exc:
        logger.warning(
            "pgvector is not available in this embedded PostgreSQL build: %s. "
            "Portfolio tables will still work; embedding features require pgvector.",
            exc,
        )
        return False


def _ensure_postgres_timezone() -> None:
    conf_path = PGDATA_DIR / "postgresql.conf"
    if not conf_path.exists():
        return

    text = conf_path.read_text(encoding="utf-8")
    if "\ntimezone = 'GMT'" in text or text.startswith("timezone = 'GMT'"):
        return

    updated = text.replace("#timezone = 'GMT'", "timezone = 'GMT'")
    if updated == text and "timezone = 'GMT'" not in text:
        updated = text.rstrip() + "\n\n# MIDAS: pgembed default\ntimezone = 'GMT'\n"
    conf_path.write_text(updated, encoding="utf-8")


def _ensure_pgembed_timezones() -> bool:
    from midas_db.timezones import ensure_pgembed_timezones

    return ensure_pgembed_timezones()


def start_embedded_postgres() -> str:
    """Start embedded PostgreSQL and return the midas DATABASE_URL."""
    import pgembed

    PGDATA_DIR.mkdir(parents=True, exist_ok=True)
    installed_timezones = _ensure_pgembed_timezones()
    _ensure_postgres_timezone()
    server = pgembed.get_server(PGDATA_DIR, cleanup_mode=None)
    _ensure_database(server, DEFAULT_DB_NAME)

    pgvector_enabled = _enable_pgvector(server)

    info = server.get_postmaster_info()
    database_url = (
        f"postgresql://postgres@127.0.0.1:{info.port}/{DEFAULT_DB_NAME}"
    )
    _write_connection_file(database_url, info.port)

    print(f"Embedded PostgreSQL running on 127.0.0.1:{info.port}")
    print(f"DATABASE_URL={database_url}")
    print(f"pgvector: {'enabled' if pgvector_enabled else 'not available on this platform yet'}")
    if installed_timezones:
        print(
            "Timezone data installed for pgembed. "
            "Restart embedded Postgres once if DBeaver still fails to connect."
        )
    print(f"Connection details saved to {CONNECTION_FILE}")
    _sync_dbeaver_connection()
    return database_url


def _sync_dbeaver_connection() -> None:
    try:
        from midas_db.dbeaver import sync_dbeaver_connection

        sync_dbeaver_connection(REPO_ROOT)
    except Exception as exc:
        logger.warning("Could not update DBeaver connection: %s", exc)


def init_schema(database_url: str) -> None:
    env = os.environ.copy()
    env["DATABASE_URL"] = database_url
    script = REPO_ROOT / "database" / "scripts" / "init_db.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT / "database",
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Schema initialization failed.")


def start_and_init() -> str:
    database_url = start_embedded_postgres()
    init_schema(database_url)
    print("MIDAS schema initialized.")
    return database_url


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="MIDAS embedded PostgreSQL manager")
    parser.add_argument(
        "command",
        choices=["start", "init", "url"],
        help="start server, start+init schema, or print saved URL",
    )
    args = parser.parse_args()

    if args.command == "url":
        url = load_embedded_database_url()
        if not url:
            raise SystemExit(
                "No embedded database URL found. Run: uv run midas-db init"
            )
        print(url)
        return

    if args.command == "start":
        start_embedded_postgres()
        return

    start_and_init()


if __name__ == "__main__":
    main()
