"""Exposure aggregation service."""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.services._helpers import holding_market_value, holdings_for_date


class ExposureService:
    """Deterministic exposure calculations — not LLM-derived."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_sector_exposure(self, as_of: date | None = None) -> dict:
        return self._exposure_by_facet_prefix("sector:", as_of)

    def get_tag_exposure(self, tag: str | None = None, as_of: date | None = None) -> dict:
        holdings = holdings_for_date(self._db, as_of)
        totals: dict[str, float] = defaultdict(float)
        portfolio_total = 0.0

        for holding in holdings:
            value = holding_market_value(holding)
            portfolio_total += value
            for instrument_facet in holding.instrument.facets:
                facet_name = instrument_facet.facet_name
                if tag is not None and facet_name != tag:
                    continue
                totals[facet_name] += value

        return self._format_exposure(totals, portfolio_total, holdings, label="tag")

    def get_currency_exposure(self, as_of: date | None = None) -> dict:
        holdings = holdings_for_date(self._db, as_of)
        totals: dict[str, float] = defaultdict(float)
        portfolio_total = 0.0

        for holding in holdings:
            value = holding_market_value(holding)
            portfolio_total += value
            totals[holding.instrument.currency] += value

        return self._format_exposure(
            totals, portfolio_total, holdings, label="currency"
        )

    def _exposure_by_facet_prefix(self, prefix: str, as_of: date | None) -> dict:
        holdings = holdings_for_date(self._db, as_of)
        totals: dict[str, float] = defaultdict(float)
        portfolio_total = 0.0

        for holding in holdings:
            value = holding_market_value(holding)
            portfolio_total += value
            matched = False
            for instrument_facet in holding.instrument.facets:
                facet_name = instrument_facet.facet_name
                if facet_name.startswith(prefix):
                    key = facet_name.removeprefix(prefix)
                    totals[key] += value
                    matched = True
            if not matched:
                totals["unclassified"] += value

        return self._format_exposure(
            totals, portfolio_total, holdings, label=prefix.rstrip(":")
        )

    @staticmethod
    def _format_exposure(
        totals: dict[str, float],
        portfolio_total: float,
        holdings: list,
        *,
        label: str,
    ) -> dict:
        if not holdings:
            return {
                "as_of_date": None,
                "portfolio_total": 0.0,
                label: [],
                "message": "No holdings found for exposure calculation.",
            }

        rows = []
        for key, value in sorted(totals.items(), key=lambda item: item[1], reverse=True):
            pct = (value / portfolio_total * 100) if portfolio_total else 0.0
            rows.append(
                {
                    "name": key,
                    "market_value": round(value, 2),
                    "percentage": round(pct, 2),
                }
            )

        return {
            "as_of_date": holdings[0].as_of_date.isoformat(),
            "portfolio_total": round(portfolio_total, 2),
            label: rows,
        }
