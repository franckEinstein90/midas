"""Create or update the MIDAS connection in DBeaver from .midas/database.json."""

from __future__ import annotations

import json
import os
from pathlib import Path

CONNECTION_ID = "postgres-jdbc-1a0193midas-64193midas01"
CONNECTION_NAME = "MIDAS (embedded)"


def _dbeaver_data_sources_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise SystemExit("APPDATA is not set; cannot locate DBeaver config.")
    return (
        Path(appdata)
        / "DBeaverData"
        / "workspace6"
        / "General"
        / ".dbeaver"
        / "data-sources.json"
    )


def _load_database_info(repo_root: Path) -> dict:
    connection_file = repo_root / ".midas" / "database.json"
    if not connection_file.exists():
        raise SystemExit(
            f"No embedded database found at {connection_file}. Run: midas-db start"
        )
    return json.loads(connection_file.read_text(encoding="utf-8"))


def _build_connection(info: dict) -> dict:
    host = info["host"]
    port = str(info["port"])
    database = info["database"]
    user = info.get("user", "postgres")
    url = f"jdbc:postgresql://{host}:{port}/{database}"

    return {
        "provider": "postgresql",
        "driver": "postgres-jdbc",
        "name": CONNECTION_NAME,
        "save-password": True,
        "configuration": {
            "host": host,
            "port": port,
            "database": database,
            "url": url,
            "configurationType": "MANUAL",
            "type": "dev",
            "closeIdleConnection": True,
            "properties": {
                "connectTimeout": "20",
                "loginTimeout": "20",
            },
            "provider-properties": {
                "@dbeaver-show-non-default-db@": "false",
            },
            "auth-model": "native",
            "user": user,
        },
    }


def sync_dbeaver_connection(repo_root: Path | None = None) -> None:
    repo_root = repo_root or Path(__file__).resolve().parents[2]
    info = _load_database_info(repo_root)
    connection = _build_connection(info)

    path = _dbeaver_data_sources_path()
    if not path.exists():
        raise SystemExit(f"DBeaver config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("connections", {})[CONNECTION_ID] = connection
    path.write_text(json.dumps(data, indent="\t") + "\n", encoding="utf-8")

    print(f"DBeaver connection '{CONNECTION_NAME}' updated.")
    print(f"  Host: {info['host']}:{info['port']}")
    print(f"  Database: {info['database']}")
    print(f"  User: {info.get('user', 'postgres')} (trust auth — leave password blank)")
    print("Restart DBeaver or refresh connections if it was already open.")


if __name__ == "__main__":
    sync_dbeaver_connection()
