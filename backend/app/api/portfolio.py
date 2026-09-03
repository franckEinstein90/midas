"""Portfolio API routes under /api/portfolio."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_app_settings
from app.db.session import get_db
from app.services.exposure import ExposureService
from app.services.portfolio import PortfolioService
from app.services.snapshots import SnapshotService

router = APIRouter(prefix="/api/portfolio")


@router.get("/summary")
def portfolio_summary(db: Session = Depends(get_db)) -> dict:
    settings = get_app_settings()
    return PortfolioService(db, settings.reporting_currency).get_portfolio_summary()


@router.get("/holdings")
def portfolio_holdings(db: Session = Depends(get_db)) -> list[dict]:
    return PortfolioService(db).get_holdings()


@router.get("/exposure")
def portfolio_exposure(db: Session = Depends(get_db)) -> dict:
    return ExposureService(db).get_sector_exposure()


@router.get("/exposure/sector")
def sector_exposure(db: Session = Depends(get_db)) -> dict:
    return ExposureService(db).get_sector_exposure()


@router.get("/exposure/currency")
def currency_exposure(db: Session = Depends(get_db)) -> dict:
    return ExposureService(db).get_currency_exposure()


@router.get("/value-history")
def value_history(db: Session = Depends(get_db)) -> list[dict]:
    settings = get_app_settings()
    return SnapshotService(db, settings.reporting_currency).get_portfolio_value_history()
