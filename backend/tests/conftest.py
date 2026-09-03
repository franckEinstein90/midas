"""Pytest configuration and shared fixtures."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import (
    Account,
    Base,
    Facet,
    Holding,
    Institution,
    Instrument,
    InstrumentFacet,
)


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    institution = Institution(name="Wealthsimple")
    session.add(institution)
    session.flush()

    account = Account(
        institution_id=institution.id,
        account_name="TFSA",
        account_type="TFSA",
        currency="CAD",
    )
    session.add(account)
    session.flush()

    instrument = Instrument(
        symbol="RY",
        name="Royal Bank",
        asset_class="STOCK",
        currency="CAD",
    )
    session.add(instrument)
    session.flush()

    session.add(Facet(name="sector:financials", description="Financial sector"))
    session.add(
        InstrumentFacet(instrument_id=instrument.id, facet_name="sector:financials")
    )
    session.add(
        Holding(
            account_id=account.id,
            instrument_id=instrument.id,
            quantity=100,
            market_price=150.0,
            market_value=15000.0,
            as_of_date=date(2025, 1, 15),
        )
    )
    session.commit()

    yield session
    session.close()
