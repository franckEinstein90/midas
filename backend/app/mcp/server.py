"""MIDAS MCP server — deterministic portfolio tools without LLM execution."""

from __future__ import annotations

import json
from datetime import date

from fastmcp import FastMCP

from app.services.factory import (
    build_exposure_service,
    build_holdings_service,
    build_portfolio_service,
    build_snapshot_service,
    get_service_session,
)

mcp = FastMCP(
    name="MIDAS Portfolio",
    instructions=(
        "MIDAS portfolio tools expose authoritative holdings, exposure, and snapshot "
        "calculations from PostgreSQL. These tools do not require an LLM."
    ),
)


def _run(service_call) -> str:
    db = get_service_session()
    try:
        return json.dumps(service_call(db), indent=2, default=str)
    finally:
        db.close()


@mcp.tool
def get_portfolio_summary(as_of_date: str | None = None) -> str:
    """Return consolidated portfolio summary including total market value."""
    return _run(
        lambda db: build_portfolio_service(db).get_portfolio_summary(
            date.fromisoformat(as_of_date) if as_of_date else None
        )
    )


@mcp.tool
def get_holdings(as_of_date: str | None = None) -> str:
    """Return all holdings across accounts."""
    return _run(
        lambda db: build_portfolio_service(db).get_holdings(
            date.fromisoformat(as_of_date) if as_of_date else None
        )
    )


@mcp.tool
def get_account_holdings(
    account_name: str | None = None,
    account_id: int | None = None,
    as_of_date: str | None = None,
) -> str:
    """Return holdings filtered to a specific account."""
    return _run(
        lambda db: build_holdings_service(db).get_account_holdings(
            account_id=account_id,
            account_name=account_name,
            as_of=date.fromisoformat(as_of_date) if as_of_date else None,
        )
    )


@mcp.tool
def get_sector_exposure(as_of_date: str | None = None) -> str:
    """Return sector exposure from instrument tags prefixed with sector:."""
    return _run(
        lambda db: build_exposure_service(db).get_sector_exposure(
            date.fromisoformat(as_of_date) if as_of_date else None
        )
    )


@mcp.tool
def get_tag_exposure(tag: str | None = None, as_of_date: str | None = None) -> str:
    """Return exposure aggregated by instrument tag/facet."""
    return _run(
        lambda db: build_exposure_service(db).get_tag_exposure(
            tag,
            date.fromisoformat(as_of_date) if as_of_date else None,
        )
    )


@mcp.tool
def get_currency_exposure(as_of_date: str | None = None) -> str:
    """Return portfolio exposure by instrument currency."""
    return _run(
        lambda db: build_exposure_service(db).get_currency_exposure(
            date.fromisoformat(as_of_date) if as_of_date else None
        )
    )


@mcp.tool
def compare_snapshots(date_a: str, date_b: str | None = None) -> str:
    """Compare portfolio totals between two dates."""
    return _run(
        lambda db: build_snapshot_service(db).compare_snapshots(
            date.fromisoformat(date_a),
            date.fromisoformat(date_b) if date_b else None,
        )
    )


@mcp.tool
def get_portfolio_value_history() -> str:
    """Return historical portfolio total market values."""
    return _run(lambda db: build_snapshot_service(db).get_portfolio_value_history())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
