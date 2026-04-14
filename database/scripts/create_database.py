import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "midas.db"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS institutions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    institution_id INTEGER NOT NULL,
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL CHECK (account_type IN ('FHSA', 'TFSA', 'RRSP', 'LRSP', 'CASH')),
    currency TEXT NOT NULL DEFAULT 'CAD',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (institution_id, account_name),
    FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exchanges (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS instruments (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    name TEXT NOT NULL,
    asset_class TEXT NOT NULL CHECK (asset_class IN ('STOCK', 'BOND', 'GIC', 'ETF')),
    exchange_id INTEGER,
    currency TEXT NOT NULL DEFAULT 'CAD',
    UNIQUE (symbol, name, exchange_id),
    FOREIGN KEY (exchange_id) REFERENCES exchanges(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS facets (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS instrument_facets (
    instrument_id INTEGER NOT NULL,
    facet_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (instrument_id, facet_name),
    FOREIGN KEY (instrument_id) REFERENCES instruments(id) ON DELETE CASCADE,
    FOREIGN KEY (facet_name) REFERENCES facets(name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS holdings (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    instrument_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity >= 0),
    average_cost REAL,
    market_price REAL,
    book_value REAL,
    daily_change REAL,
    unrealized_gain_loss REAL,
    market_value REAL,
    as_of_date TEXT NOT NULL DEFAULT (DATE('now')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, instrument_id, as_of_date),
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (instrument_id) REFERENCES instruments(id) ON DELETE CASCADE
);
"""

SEED_INSTITUTIONS = [
    "Wealthsimple",
    "Scotiabank",
]

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


def create_db(db_path: Path) -> bool:
    """Create the SQLite database if needed and ensure schema is current."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    created = not db_path.exists()

    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)

        instrument_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(instruments)")
        }
        if "exchange_id" not in instrument_columns:
            conn.execute(
                "ALTER TABLE instruments ADD COLUMN exchange_id INTEGER REFERENCES exchanges(id) ON DELETE SET NULL"
            )

        holding_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(holdings)")
        }
        holding_migrations = {
            "market_price": "ALTER TABLE holdings ADD COLUMN market_price REAL",
            "book_value": "ALTER TABLE holdings ADD COLUMN book_value REAL",
            "daily_change": "ALTER TABLE holdings ADD COLUMN daily_change REAL",
            "unrealized_gain_loss": "ALTER TABLE holdings ADD COLUMN unrealized_gain_loss REAL",
            "market_value": "ALTER TABLE holdings ADD COLUMN market_value REAL",
        }
        for column_name, migration_sql in holding_migrations.items():
            if column_name not in holding_columns:
                conn.execute(migration_sql)

        for institution in SEED_INSTITUTIONS:
            conn.execute(
                "INSERT OR IGNORE INTO institutions(name) VALUES (?)",
                (institution,),
            )

        for exchange_code, exchange_name in SEED_EXCHANGES:
            conn.execute(
                "INSERT OR IGNORE INTO exchanges(code, name) VALUES (?, ?)",
                (exchange_code, exchange_name),
            )

        for facet_name, facet_description in SEED_FACETS:
            conn.execute(
                "INSERT OR IGNORE INTO facets(name, description) VALUES (?, ?)",
                (facet_name, facet_description),
            )

        for institution_name, account_name, account_type in SEED_ACCOUNTS:
            conn.execute(
                """
                INSERT OR IGNORE INTO accounts(institution_id, account_name, account_type)
                VALUES (
                    (SELECT id FROM institutions WHERE name = ?),
                    ?,
                    ?
                )
                """,
                (institution_name, account_name, account_type),
            )

        conn.commit()
    return created


def main() -> None:
    created = create_db(DB_PATH)
    if created:
        print(f"Created SQLite portfolio database at: {DB_PATH}")
    else:
        print(f"Database already exists at: {DB_PATH}; schema verified")


if __name__ == "__main__":
    main()
