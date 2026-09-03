"""Portfolio-level aggregation service."""

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.services._helpers import holding_market_value, holdings_for_date, latest_as_of_date


class PortfolioService:
    """Consolidated portfolio views backed by PostgreSQL holdings data."""

    def __init__(self, db: Session, reporting_currency: str = "CAD") -> None:
        self._db = db
        self._reporting_currency = reporting_currency

    def get_portfolio_summary(self, as_of: date | None = None) -> dict:
        holdings = holdings_for_date(self._db, as_of)
        if not holdings:
            return {
                "as_of_date": None,
                "reporting_currency": self._reporting_currency,
                "total_market_value": 0.0,
                "holding_count": 0,
                "account_count": 0,
                "institution_count": 0,
                "message": "No holdings found for the requested date.",
            }

        total = sum(holding_market_value(h) for h in holdings)
        accounts = {h.account_id for h in holdings}
        institutions = {h.account.institution_id for h in holdings}
        resolved_date = holdings[0].as_of_date

        return {
            "as_of_date": resolved_date.isoformat(),
            "reporting_currency": self._reporting_currency,
            "total_market_value": round(total, 2),
            "holding_count": len(holdings),
            "account_count": len(accounts),
            "institution_count": len(institutions),
        }

    def get_holdings(self, as_of: date | None = None) -> list[dict]:
        holdings = holdings_for_date(self._db, as_of)
        return [self._serialize_holding(h) for h in holdings]

    @staticmethod
    def _serialize_holding(holding) -> dict:
        instrument = holding.instrument
        account = holding.account
        return {
            "account_id": account.id,
            "account_name": account.account_name,
            "account_type": account.account_type,
            "institution": account.institution.name,
            "instrument_id": instrument.id,
            "symbol": instrument.symbol,
            "instrument_name": instrument.name,
            "asset_class": instrument.asset_class,
            "currency": instrument.currency,
            "quantity": holding.quantity,
            "market_price": holding.market_price,
            "market_value": round(holding_market_value(holding), 2),
            "as_of_date": holding.as_of_date.isoformat(),
        }
