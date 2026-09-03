"""Shared service helpers."""

from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Account, Holding, Institution, Instrument


def latest_as_of_date(db: Session) -> date | None:
    return db.scalar(select(func.max(Holding.as_of_date)))


def holdings_for_date(db: Session, as_of: date | None = None) -> list[Holding]:
    if as_of is None:
        as_of = latest_as_of_date(db)
    if as_of is None:
        return []

    return list(
        db.scalars(
            select(Holding)
            .where(Holding.as_of_date == as_of)
            .options(
                joinedload(Holding.account).joinedload(Account.institution),
                joinedload(Holding.instrument).joinedload(Instrument.facets),
            )
        )
        .unique()
        .all()
    )


def holding_market_value(holding: Holding) -> float:
    if holding.market_value is not None:
        return float(holding.market_value)
    if holding.market_price is not None:
        return float(holding.market_price) * float(holding.quantity)
    if holding.book_value is not None:
        return float(holding.book_value)
    return 0.0
