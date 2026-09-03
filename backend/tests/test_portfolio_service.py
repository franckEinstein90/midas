"""Portfolio service tests — no LLM required."""

from app.services.portfolio import PortfolioService


def test_portfolio_summary(db_session) -> None:
    service = PortfolioService(db_session)
    summary = service.get_portfolio_summary()

    assert summary["total_market_value"] == 15000.0
    assert summary["holding_count"] == 1
    assert summary["account_count"] == 1
    assert summary["institution_count"] == 1


def test_get_holdings(db_session) -> None:
    service = PortfolioService(db_session)
    holdings = service.get_holdings()

    assert len(holdings) == 1
    assert holdings[0]["symbol"] == "RY"
    assert holdings[0]["market_value"] == 15000.0
