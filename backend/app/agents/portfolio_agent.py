"""MIDAS portfolio ADK agent."""

from google.adk.agents import Agent

from app.agents.tools import (
    compare_snapshots,
    get_account_holdings,
    get_currency_exposure,
    get_holdings,
    get_portfolio_summary,
    get_portfolio_value_history,
    get_sector_exposure,
    get_tag_exposure,
)
from app.llm.client import get_llm_client

PORTFOLIO_AGENT_INSTRUCTION = """You are MIDAS, a portfolio analysis assistant.

Your role is to interpret, summarize, and explain portfolio data returned by tools.
You must NOT invent prices, holdings, FX rates, or portfolio values.

Rules:
1. Always use the provided tools for authoritative portfolio calculations.
2. When asked about exposure, sector allocation, or holdings, call the appropriate tool first.
3. Explain structured tool results clearly in natural language.
4. If data is missing or a tool returns an empty result, say so explicitly.
5. Never perform financial arithmetic on raw holdings when a tool already provides the answer.
"""


def create_portfolio_agent() -> Agent:
    """Build the root ADK portfolio agent using LiteLLM for model access."""
    llm_client = get_llm_client()
    return Agent(
        model=llm_client.get_adk_litellm_model(),
        name="midas_portfolio_agent",
        description=(
            "Answers portfolio questions using deterministic MIDAS services "
            "for holdings, exposure, and snapshot comparisons."
        ),
        instruction=PORTFOLIO_AGENT_INSTRUCTION,
        tools=[
            get_portfolio_summary,
            get_holdings,
            get_account_holdings,
            get_sector_exposure,
            get_tag_exposure,
            get_currency_exposure,
            compare_snapshots,
            get_portfolio_value_history,
        ],
    )


root_agent = create_portfolio_agent()
