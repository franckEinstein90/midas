"""Service factory for agents and MCP tools."""

from sqlalchemy.orm import Session

from app.config import get_app_settings
from app.db.session import SessionLocal
from app.services.exposure import ExposureService
from app.services.holdings import HoldingsService
from app.services.portfolio import PortfolioService
from app.services.snapshots import SnapshotService


def get_service_session() -> Session:
    return SessionLocal()


def build_portfolio_service(db: Session) -> PortfolioService:
    settings = get_app_settings()
    return PortfolioService(db, reporting_currency=settings.reporting_currency)


def build_holdings_service(db: Session) -> HoldingsService:
    return HoldingsService(db)


def build_exposure_service(db: Session) -> ExposureService:
    return ExposureService(db)


def build_snapshot_service(db: Session) -> SnapshotService:
    settings = get_app_settings()
    return SnapshotService(db, reporting_currency=settings.reporting_currency)
