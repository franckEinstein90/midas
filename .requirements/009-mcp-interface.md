# 009 — MCP Interface

## Purpose

The MIDAS MCP server exposes portfolio application capabilities to external clients (e.g. Cursor) as deterministic tools. MCP is a separate concern from model execution — MCP tools do not require an LLM to run.

## Architecture

```text
Cursor / MCP client
        ↓
    MIDAS MCP (FastMCP)
        ↓
 PortfolioService / ExposureService / SnapshotService
        ↓
   PostgreSQL
```

An ADK agent may use the same underlying services through its own tool wrappers:

```text
User → ADK agent → tool → PortfolioService → PostgreSQL
```

Both paths share application services; neither duplicates business logic.

## Server location

```text
backend/app/mcp/server.py
```

Run with:

```bash
cd backend
uv run midas-mcp
```

## Tool catalog

| MCP tool | Description |
|----------|-------------|
| `get_portfolio_summary` | Consolidated portfolio totals and counts |
| `get_holdings` | All holdings across accounts |
| `get_account_holdings` | Holdings filtered by account |
| `get_sector_exposure` | Sector allocation from `sector:` tags |
| `get_tag_exposure` | Exposure by facet/tag |
| `get_currency_exposure` | Exposure by instrument currency |
| `compare_snapshots` | Compare portfolio value between two dates |
| `get_portfolio_value_history` | Historical total market values |

## Design principles

1. **No LLM in the MCP path.** MCP tools call application services directly and return structured JSON.
2. **Same services as ADK.** MCP and ADK tools must not diverge in calculation logic.
3. **Deterministic output.** Given the same database state and parameters, tools return reproducible results.
4. **PostgreSQL is authoritative.** MCP tools read from the same database as the REST API and ADK agent.

## MCP vs ADK

| Aspect | MCP | ADK Agent |
|--------|-----|-----------|
| Client | Cursor, IDE, automation | Conversational user |
| LLM required | No | Yes (via LiteLLM) |
| Output | Structured JSON | Natural language + tool calls |
| Use case | Direct data access, automation | Interpretation and explanation |

Do not force every MCP operation through an LLM. Clients that need raw data should call MCP tools directly.

## Configuration

MCP tools use the same `DATABASE_URL` as the backend API. No separate MCP-specific credentials are required beyond database access.

## Testing

MCP tool handlers delegate to application services, which are covered by service unit tests. No live LLM or MCP client connection is required for ordinary backend tests.

## Future extensions

- Authentication for remote MCP deployment
- Read-only vs read-write tool separation
- Rate limiting at the MCP server boundary
- OpenAPI-derived MCP tools for REST endpoints

These are not required for bootstrap.
