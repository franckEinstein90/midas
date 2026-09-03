"""Seed reference data for local MIDAS development."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Account, Exchange, Facet, Institution

SEED_INSTITUTIONS = ["Wealthsimple", "Scotiabank"]

SEED_EXCHANGES = [
    ("TSX", "Toronto Stock Exchange"),
    ("TSXV", "TSX Venture Exchange"),
    ("NASDAQ", "Nasdaq"),
    ("NYSE", "New York Stock Exchange"),
    ("CBOE", "Cboe Canada"),
]

SEED_FACETS = [
    ("materials", "Materials sector exposure."),
    ("gold", "Gold-related exposure."),
    ("silver", "Silver-related exposure."),
    ("defense", "Defense and aerospace exposure."),
    ("china", "China-focused geographic exposure."),
    ("semidconductors", "Semiconductor industry exposure."),
    ("big tech", "Large-cap technology company exposure."),
    ("sector:financials", "Financial sector exposure."),
]

SEED_ACCOUNTS = [
    ("Wealthsimple", "FHSA", "FHSA"),
    ("Wealthsimple", "TFSA", "TFSA"),
    ("Wealthsimple", "Cash", "CASH"),
    ("Scotiabank", "LRSP", "LRSP"),
    ("Scotiabank", "Cash", "CASH"),
    ("Scotiabank", "RRSP", "RRSP"),
    ("Scotiabank", "TFSA", "TFSA"),
]


def seed_reference_data(db: Session) -> None:
    existing = db.scalar(select(Institution.id).limit(1))
    if existing is not None:
        return

    institutions: dict[str, Institution] = {}
    for name in SEED_INSTITUTIONS:
        institution = Institution(name=name)
        db.add(institution)
        institutions[name] = institution
    db.flush()

    for code, name in SEED_EXCHANGES:
        db.add(Exchange(code=code, name=name))

    for facet_name, description in SEED_FACETS:
        db.add(Facet(name=facet_name, description=description))

    for institution_name, account_name, account_type in SEED_ACCOUNTS:
        db.add(
            Account(
                institution_id=institutions[institution_name].id,
                account_name=account_name,
                account_type=account_type,
            )
        )

    db.commit()
