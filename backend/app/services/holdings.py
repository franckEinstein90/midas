"""Account-level holdings service."""

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.services._helpers import holding_market_value, holdings_for_date
from app.services.portfolio import PortfolioService


class HoldingsService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_account_holdings(
        self,
        account_id: int | None = None,
        account_name: str | None = None,
        as_of: date | None = None,
    ) -> list[dict]:
        holdings = holdings_for_date(self._db, as_of)
        filtered = []
        for holding in holdings:
            account = holding.account
            if account_id is not None and account.id != account_id:
                continue
            if account_name is not None and account.account_name != account_name:
                continue
            filtered.append(PortfolioService._serialize_holding(holding))

        if not filtered and (account_id is not None or account_name is not None):
            return [{"message": "No holdings found for the specified account."}]
        return filtered
