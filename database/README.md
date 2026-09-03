# MIDAS database (embedded PostgreSQL + Alembic)

Local database lifecycle, schema migrations, and DBeaver connection sync. The backend ORM models in `../backend/app/db/models.py` remain the source of truth for autogenerate.

## Setup

```powershell
cd database
uv sync
uv run midas-db init
```

This starts embedded PostgreSQL (pgembed), applies migrations, seeds reference data, and writes connection details to `../.midas/database.json`.

## Commands

| Command | Description |
|---------|-------------|
| `uv run midas-db init` | Start Postgres + migrate + seed |
| `uv run midas-db start` | Start Postgres only |
| `uv run midas-db url` | Print saved `DATABASE_URL` |
| `uv run midas-dbeaver` | Refresh DBeaver connection from `.midas/database.json` |

## Migrations

Embedded Postgres must be running (`uv run midas-db start`).

```powershell
cd database
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "describe your change"
uv run alembic current
uv run alembic downgrade -1
```

See `migrations/README` for more detail.

## Connection

Apps read `DATABASE_URL` from the environment, or fall back to `../.midas/database.json` after `midas-db init`.

DBeaver: connect as user `postgres` with an empty password (trust auth). Restart DBeaver after `midas-db start` if the port changed.
