"""ADK portfolio agent tools backed by MIDAS application services."""

from __future__ import annotations

import json
from datetime import date

from app.services.factory import (
    build_exposure_service,
    build_holdings_service,
    build_portfolio_service,
    build_snapshot_service,
    get_service_session,
)


def _json(data: object) -> str:
    return json.dumps(data, indent=2, default=str)


def get_portfolio_summary(as_of_date: str | None = None) -> str:
    """Return consolidated portfolio summary (total value, counts, as-of date).

    Args:
        as_of_date: Optional ISO date (YYYY-MM-DD). Uses latest holdings when omitted.
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_portfolio_service(db).get_portfolio_summary(as_of)
        return _json(result)
    finally:
        db.close()


def get_holdings(as_of_date: str | None = None) -> str:
    """Return all holdings across accounts for a given date.

    Args:
        as_of_date: Optional ISO date (YYYY-MM-DD). Uses latest holdings when omitted.
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_portfolio_service(db).get_holdings(as_of)
        return _json(result)
    finally:
        db.close()


def get_account_holdings(
    account_name: str | None = None,
    account_id: int | None = None,
    as_of_date: str | None = None,
) -> str:
    """Return holdings for a specific account.

    Args:
        account_name: Account name filter (e.g. TFSA, RRSP).
        account_id: Numeric account id filter.
        as_of_date: Optional ISO date (YYYY-MM-DD).
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_holdings_service(db).get_account_holdings(
            account_id=account_id,
            account_name=account_name,
            as_of=as_of,
        )
        return _json(result)
    finally:
        db.close()


def get_sector_exposure(as_of_date: str | None = None) -> str:
    """Return sector exposure percentages from tagged instruments.

    Args:
        as_of_date: Optional ISO date (YYYY-MM-DD).
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_exposure_service(db).get_sector_exposure(as_of)
        return _json(result)
    finally:
        db.close()


def get_tag_exposure(tag: str | None = None, as_of_date: str | None = None) -> str:
    """Return exposure aggregated by instrument tag/facet.

    Args:
        tag: Optional exact facet name filter.
        as_of_date: Optional ISO date (YYYY-MM-DD).
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_exposure_service(db).get_tag_exposure(tag, as_of)
        return _json(result)
    finally:
        db.close()


def get_currency_exposure(as_of_date: str | None = None) -> str:
    """Return portfolio exposure by instrument currency.

    Args:
        as_of_date: Optional ISO date (YYYY-MM-DD).
    """
    db = get_service_session()
    try:
        as_of = date.fromisoformat(as_of_date) if as_of_date else None
        result = build_exposure_service(db).get_currency_exposure(as_of)
        return _json(result)
    finally:
        db.close()


def compare_snapshots(date_a: str, date_b: str | None = None) -> str:
    """Compare portfolio totals between two snapshot dates.

    Args:
        date_a: Earlier ISO date (YYYY-MM-DD).
        date_b: Later ISO date (YYYY-MM-DD). Defaults to latest holdings date.
    """
    db = get_service_session()
    try:
        parsed_a = date.fromisoformat(date_a)
        parsed_b = date.fromisoformat(date_b) if date_b else None
        result = build_snapshot_service(db).compare_snapshots(parsed_a, parsed_b)
        return _json(result)
    finally:
        db.close()


def get_portfolio_value_history() -> str:
    """Return historical portfolio total market values over time."""
    db = get_service_session()
    try:
        result = build_snapshot_service(db).get_portfolio_value_history()
        return _json(result)
    finally:
        db.close()
