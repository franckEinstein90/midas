"""Portfolio snapshot and history service."""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import PortfolioSnapshot
from app.services._helpers import holding_market_value, holdings_for_date, latest_as_of_date
from app.services.portfolio import PortfolioService


class SnapshotService:
    def __init__(self, db: Session, reporting_currency: str = "CAD") -> None:
        self._db = db
        self._reporting_currency = reporting_currency

    def get_portfolio_value_history(self) -> list[dict]:
        snapshots = list(
            self._db.scalars(
                select(PortfolioSnapshot).order_by(PortfolioSnapshot.as_of_date)
            ).all()
        )
        if snapshots:
            return [
                {
                    "as_of_date": s.as_of_date.isoformat(),
                    "total_market_value": s.total_market_value,
                    "reporting_currency": s.reporting_currency,
                }
                for s in snapshots
            ]

        # Derive from holdings when snapshot table is not populated yet.
        holdings = holdings_for_date(self._db)
        if not holdings:
            return []

        by_date: dict[date, float] = {}
        for holding in holdings:
            by_date[holding.as_of_date] = by_date.get(holding.as_of_date, 0.0) + (
                holding_market_value(holding)
            )

        return [
            {
                "as_of_date": d.isoformat(),
                "total_market_value": round(v, 2),
                "reporting_currency": self._reporting_currency,
            }
            for d, v in sorted(by_date.items())
        ]

    def compare_snapshots(
        self,
        date_a: date,
        date_b: date | None = None,
    ) -> dict:
        if date_b is None:
            latest = latest_as_of_date(self._db)
            if latest is None:
                return {"message": "No holdings available for comparison."}
            date_b = latest

        summary_a = PortfolioService(self._db).get_portfolio_summary(date_a)
        summary_b = PortfolioService(self._db).get_portfolio_summary(date_b)

        value_a = summary_a.get("total_market_value") or 0.0
        value_b = summary_b.get("total_market_value") or 0.0
        delta = value_b - value_a
        pct_change = (delta / value_a * 100) if value_a else None

        return {
            "date_a": date_a.isoformat(),
            "date_b": date_b.isoformat(),
            "value_a": value_a,
            "value_b": value_b,
            "absolute_change": round(delta, 2),
            "percentage_change": round(pct_change, 2) if pct_change is not None else None,
            "holding_count_a": summary_a.get("holding_count", 0),
            "holding_count_b": summary_b.get("holding_count", 0),
        }
