# MIDAS Backend

Portfolio services, ADK agents, MCP tools, and LiteLLM model layer.

## Setup

```powershell
cd database
uv sync
uv run midas-db init

cd ../backend
uv sync --extra dev
copy .env.example .env
```

`midas-db init` starts embedded PostgreSQL and applies migrations. Connection details are saved to `.midas/database.json` at the repo root.

## Run

```powershell
# REST API
uv run midas-api

# MCP server (for Cursor / MCP clients)
uv run midas-mcp
```

## Configuration

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Optional override; defaults to `.midas/database.json` after `midas-db init` |
| `MIDAS_DEFAULT_MODEL` | Primary LiteLLM model |
| `OPENAI_API_KEY` | OpenAI credentials (if using OpenAI models) |

## Database

Embedded Postgres lifecycle, Alembic migrations, and DBeaver sync live in `../database/`. See `database/README.md`.
