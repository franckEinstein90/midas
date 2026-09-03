# MIDAS database (embedded PostgreSQL via pgembed)

MIDAS uses **embedded PostgreSQL** for local development — no Docker Desktop, no separate Postgres install.

The [`pgembed`](https://pypi.org/project/pgembed/) package bundles PostgreSQL 17 binaries via pip. On first start it picks a free local TCP port (commonly near 5432) and persists data under `.midas/pgdata/`.

## Quick start

```powershell
cd database
uv sync
uv run midas-db init
```

This will:

1. Start embedded PostgreSQL on `127.0.0.1` (port stored in `.midas/database.json`)
2. Create the `midas` database
3. Enable pgvector when the extension is available
4. Apply Alembic migrations and seed reference data

## Connection URL

After `midas-db init`, connection details are written to:

```text
.midas/database.json
```

Backend, frontend API, and MCP tools read this automatically unless `DATABASE_URL` is set explicitly.

```powershell
cd database
uv run midas-db url
```

## Migrations

Alembic migrations live in `database/migrations/`. See `database/migrations/README`.

## Commands

| Command | Description |
|---------|-------------|
| `uv run midas-db init` | Start embedded Postgres + migrate + seed |
| `uv run midas-db start` | Start server only |
| `uv run midas-db url` | Print saved DATABASE_URL |
| `uv run midas-dbeaver` | Refresh DBeaver connection |

## Production

Production deployments should set `DATABASE_URL` to a managed PostgreSQL instance with pgvector enabled. Embedded Postgres is for local development only.

## Architecture

```text
database/ (pgembed + Alembic)
    ↓
127.0.0.1:<port>/midas
    ↓
backend services / MCP / frontend API
```

All application layers share one PostgreSQL instance. SQLite is not used.
