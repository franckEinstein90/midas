# 010 — LiteLLM Model Layer

## Purpose

MIDAS uses **LiteLLM** as the model abstraction and routing layer. Application code must not couple directly to OpenAI, Anthropic, Gemini, Azure OpenAI, or other provider SDKs.

## Architecture

```text
MIDAS domain/application services
          ↑
       ADK tools
          ↑
      ADK agents
          ↓
       LiteLLM (in-process SDK)
          ↓
 ┌────────┼─────────┬─────────┐
OpenAI  Gemini   Anthropic   other providers
```

For bootstrap, MIDAS uses the **LiteLLM Python SDK in-process**. The LiteLLM Proxy is **not** deployed as a separate service yet, but configuration is isolated so migration later requires no changes to agent business logic.

## Module layout

```text
backend/app/llm/
  config.py    # Environment-based LLM configuration
  models.py    # Logical MIDAS model aliases and selection policy
  client.py    # LiteLLM integration and invocation
```

## Why LiteLLM

1. **Provider independence.** Switch models or providers via configuration, not code changes.
2. **Unified interface.** One completion API for 100+ models.
3. **Built-in fallbacks.** LiteLLM's fallback facilities handle provider outages without a custom router.
4. **Future proxy migration.** The same model identifiers work with an in-process SDK or a LiteLLM Proxy.

## Configuration

Environment variables (see `backend/.env.example`):

| Variable | Description |
|----------|-------------|
| `MIDAS_DEFAULT_MODEL` | Primary LiteLLM model identifier (e.g. `openai/gpt-4o-mini`) |
| `MIDAS_FALLBACK_MODELS` | Comma-separated ordered fallback models |
| `MIDAS_TEMPERATURE` | Default sampling temperature |
| `MIDAS_TIMEOUT_SECONDS` | Request timeout |
| `LITELLM_PROXY_BASE_URL` | *(Future)* Proxy endpoint |
| `LITELLM_PROXY_API_KEY` | *(Future)* Proxy API key |

Provider credentials use standard LiteLLM environment variables:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

**Do not commit credentials.** Do not hard-code production model identifiers in domain code.

## Fallbacks

Bootstrap supports:

1. One configurable primary model (`MIDAS_DEFAULT_MODEL`)
2. An optional ordered fallback list (`MIDAS_FALLBACK_MODELS`)

When fallbacks are configured, `LLMClient` uses `litellm.completion_with_fallbacks`. No custom model router is implemented.

Future policies (inexpensive model for simple questions, stronger model for scenarios, local model for privacy) can be added by extending `MIDASModel` aliases in `models.py` without changing service code.

## ADK integration

ADK agents access models through the `LiteLlm` connector:

```python
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model="openai/gpt-4o-mini")
```

MIDAS wraps this in `LLMClient.get_adk_litellm_model()` so model resolution stays centralized.

## Future LiteLLM Proxy migration

Documented target architecture (not implemented during bootstrap):

```text
FastAPI / ADK
      ↓
LiteLLM Proxy
      ↓
multiple model providers
```

The proxy may eventually provide centralized credentials, model aliases, retries, usage/cost tracking, budgets, rate limits, and observability. `LLMSettings.proxy_base_url` and `proxy_api_key` are reserved for this migration.

When migrating:

1. Deploy LiteLLM Proxy.
2. Set `LITELLM_PROXY_BASE_URL` and `LITELLM_PROXY_API_KEY`.
3. No changes to ADK agent instructions or application services.

## Logging and privacy

- LiteLLM debug output is suppressed in application logs (`litellm.suppress_debug_info = True`).
- Do not log full prompt content or API keys in production.
- Portfolio holdings and financial data sent to the LLM should come from tool results the agent already retrieved — not raw database dumps in prompts.
- When using cloud providers, be aware that prompt content may leave your infrastructure. Local models via LiteLLM remain an option for privacy-sensitive operations in the future.

## LLM vs authoritative calculations

| LLM may | LLM must not |
|---------|--------------|
| Interpret tool results | Invent prices or FX rates |
| Summarize exposure | Compute holdings from memory |
| Explain comparisons | Overwrite PostgreSQL data |
| Help construct scenario requests | Act as the financial system of record |

PostgreSQL + deterministic MIDAS application services are authoritative. The LLM is an interface and analytical assistant.

## Testing

- Ordinary backend tests mock the LLM boundary (`tests/test_llm_client.py`).
- Holdings, exposure, import, snapshot, and valuation tests never require a live model API.
- Integration tests (`tests/integration/test_litellm_integration.py`) run only when provider credentials are configured (`pytest -m integration`).
- The core financial application remains completely usable without an LLM connection.

## Dependencies

- `litellm>=1.84.0`
- `google-adk>=2.4.0` (ADK LiteLLM connector)

Do not add direct provider SDK dependencies to application services unless required internally by ADK/LiteLLM.
