# LLM ARCHITECTURE — LITELLM

MIDAS must use **LiteLLM** as the model abstraction and routing layer.

The application must NOT couple its ADK agents directly to OpenAI, Anthropic, Gemini, Azure OpenAI, or another model provider.

Architecture:

```text
MIDAS domain/application services
          ↑
       ADK tools
          ↑
      ADK agents
          ↓
       LiteLLM
          ↓
 ┌────────┼─────────┬─────────┐
OpenAI  Gemini   Anthropic   other providers
```

For the initial implementation, use the **LiteLLM Python SDK in-process**.

Do NOT deploy the LiteLLM Proxy as a separate service during this bootstrap.

However, isolate model configuration so MIDAS can later switch to a LiteLLM Proxy without changing agent business logic.

Add a backend module approximately like:

```text
backend/app/
  llm/
    config.py
    models.py
    client.py
```

Responsibilities:

`config.py`

* environment-based LLM configuration
* default model
* fallback models
* temperature and other appropriate defaults
* provider credentials obtained only from environment variables

`models.py`

* logical MIDAS model names / aliases
* model selection policy

`client.py`

* LiteLLM integration
* common invocation configuration where needed
* no portfolio business logic

Use a logical configuration such as:

```text
MIDAS_DEFAULT_MODEL=
MIDAS_FALLBACK_MODELS=
```

Provider credentials should remain standard environment variables supported by LiteLLM, for example:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

Do not commit credentials.

Do not hard-code a specific production model into domain code.

A model identifier should be configurable without changing Python source.

For local development, select one sensible model as the documented example, but treat it purely as a configurable default.

---

# ADK + LITELLM

Use Google Agent Development Kit for orchestration and agent/tool semantics.

Use LiteLLM for access to language models.

The conceptual separation is:

```text
ADK = agent orchestration
LiteLLM = model abstraction/routing
MIDAS services = financial/business logic
MCP = external tool interface
```

Do not blur those responsibilities.

The MIDAS portfolio agent should contain instructions and tool selection logic.

It must NOT calculate portfolio metrics itself when an application service already provides that calculation.

For example:

User:

"What percentage of my portfolio is in Canadian financials?"

Preferred path:

```text
User
 ↓
ADK Portfolio Agent
 ↓
get_exposure tool
 ↓
ExposureService
 ↓
PostgreSQL
 ↓
structured result
 ↓
ADK
 ↓
LiteLLM
 ↓
natural-language response
```

The LLM should explain and reason about structured financial results.

It should not be responsible for computing authoritative financial values from raw database rows.

---

# MODEL PROVIDER INDEPENDENCE

MIDAS should be capable of using different models for different purposes later.

Possible future policies include:

* inexpensive model for simple portfolio questions
* stronger reasoning model for counterfactual analysis
* local model for privacy-sensitive operations
* fallback provider during outages
* specialized model for document/import interpretation

Do NOT implement elaborate routing now.

Create the architecture so these policies can be added later.

For the bootstrap, support:

1. one configurable primary model
2. an optional ordered fallback list

Use LiteLLM's supported routing/fallback facilities where they improve simplicity.

Do not build a custom model router unnecessarily.

---

# FUTURE LITELLM PROXY

Document, but do not implement, a future architecture:

```text
FastAPI / ADK
      ↓
LiteLLM Proxy
      ↓
multiple model providers
```

The proxy may eventually provide:

* centralized provider credentials
* model aliases
* retries and fallbacks
* usage tracking
* cost tracking
* budgets
* rate limits
* logging/observability
* provider switching

The application should therefore avoid assumptions that require direct provider SDK access.

Do not introduce OpenAI, Anthropic, or Gemini SDK calls directly into MIDAS application services unless required internally by the selected ADK/LiteLLM integration.

---

# MCP + ADK + LITELLM

The MCP server is a separate concern from model execution.

MIDAS MCP tools should expose application capabilities such as:

```text
get_portfolio_summary
get_holdings
get_account_holdings
get_sector_exposure
get_tag_exposure
get_currency_exposure
compare_snapshots
get_portfolio_value_history
```

MCP tools call MIDAS application services directly.

They do NOT need an LLM to execute deterministic operations.

For example:

```text
Cursor / MCP client
        ↓
    MIDAS MCP
        ↓
 PortfolioService
        ↓
   PostgreSQL
```

An ADK agent may also use those same service-backed tools:

```text
User
 ↓
ADK agent
 ↓
tool
 ↓
PortfolioService
```

Do not force every MCP operation through an LLM.

This distinction is important.

---

# REQUIREMENTS

Add:

```text
.requirements/
  008-adk-agent.md
  009-mcp-interface.md
  010-litellm-model-layer.md
```

`010-litellm-model-layer.md` should describe:

* why LiteLLM is used
* model-provider independence
* configuration
* fallbacks
* credential handling
* future LiteLLM Proxy migration
* logging/privacy considerations
* distinction between LLM reasoning and authoritative portfolio calculations

---

# TESTING

Mock the LLM boundary during ordinary backend tests.

Tests for holdings, exposure, imports, snapshots, scenarios, and valuation must NOT require a live model API.

Have a small separate integration-test path for LiteLLM/ADK that only runs when appropriate credentials are configured.

The core financial application must remain completely usable without an LLM connection.

---

# IMPORTANT RULE

Treat AI as an interface and analytical assistant over MIDAS.

Do not make the LLM the financial system of record.

PostgreSQL + deterministic MIDAS application services are authoritative.

The LLM can:

* interpret
* summarize
* explain
* compare
* help construct scenario requests
* reason about returned results

The LLM must not invent missing prices, FX rates, holdings, transactions, or portfolio values.

When necessary data is unavailable, surface that fact explicitly.
