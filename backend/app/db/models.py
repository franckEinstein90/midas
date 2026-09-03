"""SQLAlchemy ORM models aligned with the MIDAS portfolio schema."""

from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pgvector.sqlalchemy import Vector

from app.db.session import Base


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    accounts: Mapped[list["Account"]] = relationship(back_populates="institution")


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("institution_id", "account_name"),
        CheckConstraint(
            "account_type IN ('FHSA', 'TFSA', 'RRSP', 'LRSP', 'CASH')",
            name="ck_accounts_account_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False
    )
    account_name: Mapped[str] = mapped_column(String, nullable=False)
    account_type: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False, default="CAD")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    institution: Mapped["Institution"] = relationship(back_populates="accounts")
    holdings: Mapped[list["Holding"]] = relationship(back_populates="account")


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class Instrument(Base):
    __tablename__ = "instruments"
    __table_args__ = (
        UniqueConstraint("symbol", "name", "exchange_id"),
        CheckConstraint(
            "asset_class IN ('STOCK', 'BOND', 'GIC', 'ETF')",
            name="ck_instruments_asset_class",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str | None] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=False)
    asset_class: Mapped[str] = mapped_column(String, nullable=False)
    exchange_id: Mapped[int | None] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL")
    )
    currency: Mapped[str] = mapped_column(String, nullable=False, default="CAD")

    facets: Mapped[list["InstrumentFacet"]] = relationship(back_populates="instrument")
    holdings: Mapped[list["Holding"]] = relationship(back_populates="instrument")


class Facet(Base):
    __tablename__ = "facets"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class InstrumentFacet(Base):
    __tablename__ = "instrument_facets"

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id", ondelete="CASCADE"), primary_key=True
    )
    facet_name: Mapped[str] = mapped_column(
        ForeignKey("facets.name", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    instrument: Mapped["Instrument"] = relationship(back_populates="facets")
    facet: Mapped["Facet"] = relationship()


class Holding(Base):
    __tablename__ = "holdings"
    __table_args__ = (
        UniqueConstraint("account_id", "instrument_id", "as_of_date"),
        CheckConstraint("quantity >= 0", name="ck_holdings_quantity_nonneg"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    average_cost: Mapped[float | None] = mapped_column(Float)
    market_price: Mapped[float | None] = mapped_column(Float)
    book_value: Mapped[float | None] = mapped_column(Float)
    daily_change: Mapped[float | None] = mapped_column(Float)
    unrealized_gain_loss: Mapped[float | None] = mapped_column(Float)
    market_value: Mapped[float | None] = mapped_column(Float)
    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    account: Mapped["Account"] = relationship(back_populates="holdings")
    instrument: Mapped["Instrument"] = relationship(back_populates="holdings")


class PortfolioSnapshot(Base):
    """Immutable dated portfolio observation for historical analysis."""

    __tablename__ = "portfolio_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    as_of_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    total_market_value: Mapped[float] = mapped_column(Float, nullable=False)
    reporting_currency: Mapped[str] = mapped_column(String, nullable=False, default="CAD")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class InstrumentEmbedding(Base):
    """Vector embeddings for instruments — requires pgvector extension."""

    __tablename__ = "instrument_embeddings"

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id", ondelete="CASCADE"), primary_key=True
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
