"""Exposure service tests — authoritative calculations, no LLM."""

from app.services.exposure import ExposureService


def test_sector_exposure(db_session) -> None:
    service = ExposureService(db_session)
    result = service.get_sector_exposure()

    assert result["portfolio_total"] == 15000.0
    assert len(result["sector"]) == 1
    assert result["sector"][0]["name"] == "financials"
    assert result["sector"][0]["percentage"] == 100.0


def test_currency_exposure(db_session) -> None:
    service = ExposureService(db_session)
    result = service.get_currency_exposure()

    assert result["currency"][0]["name"] == "CAD"
    assert result["currency"][0]["percentage"] == 100.0
