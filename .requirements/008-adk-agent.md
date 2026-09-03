# 008 — ADK Portfolio Agent

## Purpose

MIDAS uses the Google Agent Development Kit (ADK) for agent orchestration, tool selection, and conversational portfolio analysis. ADK does not perform authoritative financial calculations — it delegates those to MIDAS application services via tools.

## Architecture

```text
User
 ↓
ADK Portfolio Agent (midas_portfolio_agent)
 ↓
Service-backed tools (get_exposure, get_holdings, …)
 ↓
PortfolioService / ExposureService / SnapshotService
 ↓
PostgreSQL
 ↓
Structured JSON result
 ↓
ADK + LiteLLM
 ↓
Natural-language response
```

## Responsibilities

| Layer | Responsibility |
|-------|----------------|
| ADK agent | Instructions, tool selection, conversational flow |
| ADK tools | Thin wrappers calling application services |
| Application services | Deterministic portfolio calculations |
| LiteLLM | Model access only — see `010-litellm-model-layer.md` |
| PostgreSQL | System of record for holdings and snapshots |

## Agent location

```text
backend/app/agents/
  portfolio_agent.py   # Agent definition and instructions
  tools.py             # Service-backed tool functions
```

## Tool catalog

The portfolio agent exposes these tools, each backed by a MIDAS service:

| Tool | Service |
|------|---------|
| `get_portfolio_summary` | `PortfolioService` |
| `get_holdings` | `PortfolioService` |
| `get_account_holdings` | `HoldingsService` |
| `get_sector_exposure` | `ExposureService` |
| `get_tag_exposure` | `ExposureService` |
| `get_currency_exposure` | `ExposureService` |
| `compare_snapshots` | `SnapshotService` |
| `get_portfolio_value_history` | `SnapshotService` |

## Critical rule

The LLM must **not** compute authoritative financial values from raw data. When a user asks "What percentage of my portfolio is in Canadian financials?", the agent must call `get_sector_exposure` (or `get_tag_exposure`) and explain the structured result — not estimate percentages itself.

When data is unavailable, the agent must say so explicitly. It must not invent prices, FX rates, holdings, or portfolio values.

## Model access

The agent uses LiteLLM via ADK's `LiteLlm` connector:

```python
from google.adk.agents import Agent
from app.llm.client import get_llm_client

agent = Agent(
    model=get_llm_client().get_adk_litellm_model(),
    tools=[...],
)
```

Model selection is configured through environment variables (`MIDAS_DEFAULT_MODEL`, `MIDAS_FALLBACK_MODELS`) — never hard-coded in agent business logic.

## Instructions

The agent system prompt enforces:

1. Always use tools for portfolio calculations.
2. Explain structured results in plain language.
3. Never invent missing financial data.
4. Surface gaps explicitly when tools return empty results.

## Testing

- Unit and service tests mock the LLM boundary entirely.
- A separate integration test path (`tests/integration/`) runs live LiteLLM calls only when provider credentials are configured.
- The core financial application remains fully usable without any LLM connection.

## Future extensions

Purpose-specific agents (scenario analysis, document import) can be added later with separate logical model aliases. Do not implement elaborate multi-agent routing during bootstrap — one portfolio agent with service-backed tools is sufficient.
