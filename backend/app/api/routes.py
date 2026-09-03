"""Frontend-facing API routes under /api."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.config import get_app_settings
from app.db.models import Account
from app.db.session import get_db
from app.services.snapshots import SnapshotService

router = APIRouter(prefix="/api")


@router.get("/accounts")
def list_accounts(db: Session = Depends(get_db)) -> list[dict]:
    accounts = db.scalars(
        select(Account)
        .options(joinedload(Account.institution))
        .order_by(Account.id)
    ).unique().all()

    return [
        {
            "id": account.id,
            "account_name": account.account_name,
            "account_type": account.account_type,
            "currency": account.currency,
            "institution": account.institution.name,
        }
        for account in accounts
    ]


@router.get("/snapshots")
def list_snapshots(db: Session = Depends(get_db)) -> list[dict]:
    settings = get_app_settings()
    return SnapshotService(db, settings.reporting_currency).get_portfolio_value_history()
