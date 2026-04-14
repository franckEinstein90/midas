from create_database import DB_PATH, create_db
import sqlite3


HOLDINGS = [
    {
        "name": "PURPOSE HIGH INTEREST SAVINGS FUND UNITS",
        "symbol": "PSA",
        "asset_class": "ETF",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 458,
        "average_cost": 50.0595,
        "market_price": 50.06,
        "book_value": 22927.25,
        "daily_change": 0.0,
        "unrealized_gain_loss": 0.23,
        "market_value": 22927.48,
        "facets": [],
    },
    {
        "name": "BANK OF MONTREAL",
        "symbol": "BMO",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 65,
        "average_cost": 152.2869,
        "market_price": 201.54,
        "book_value": 9928.59,
        "daily_change": 31.94,
        "unrealized_gain_loss": 3171.51,
        "market_value": 13100.10,
        "facets": [],
    },
    {
        "name": "BANK OF NOVA SCOTIA",
        "symbol": "BNS",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 111,
        "average_cost": 85.3202,
        "market_price": 101.67,
        "book_value": 9470.54,
        "daily_change": 19.16,
        "unrealized_gain_loss": 1814.83,
        "market_value": 11285.37,
        "facets": [],
    },
    {
        "name": "CANADIAN IMPERIAL BANK OF COMMERCE",
        "symbol": "CM",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 87,
        "average_cost": 107.0885,
        "market_price": 144.40,
        "book_value": 9356.62,
        "daily_change": 34.27,
        "unrealized_gain_loss": 3206.18,
        "market_value": 12562.80,
        "facets": [],
    },
    {
        "name": "CANADIAN NATIONAL RAILWAY CO",
        "symbol": "CNR",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 23,
        "average_cost": 139.6965,
        "market_price": 152.89,
        "book_value": 3227.99,
        "daily_change": 8.94,
        "unrealized_gain_loss": 288.48,
        "market_value": 3516.47,
        "facets": [],
    },
    {
        "name": "INVESCO S&P 500 EQUAL WEIGH INDEX ETF",
        "symbol": "EQL",
        "asset_class": "ETF",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 100,
        "average_cost": 38.72,
        "market_price": 41.61,
        "book_value": 3876.99,
        "daily_change": 7.33,
        "unrealized_gain_loss": 284.01,
        "market_value": 4161.00,
        "facets": [],
    },
    {
        "name": "FORTIS INC",
        "symbol": "FTS",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 35,
        "average_cost": 71.0257,
        "market_price": 78.46,
        "book_value": 2495.88,
        "daily_change": 10.03,
        "unrealized_gain_loss": 250.22,
        "market_value": 2746.10,
        "facets": [],
    },
    {
        "name": "GREAT-WEST LIFECO INC",
        "symbol": "GWO",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 85,
        "average_cost": 56.6941,
        "market_price": 68.80,
        "book_value": 4843.95,
        "daily_change": 20.73,
        "unrealized_gain_loss": 1004.05,
        "market_value": 5848.00,
        "facets": [],
    },
    {
        "name": "IGM FINANCIAL INC",
        "symbol": "IGM",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 115,
        "average_cost": 50.8713,
        "market_price": 70.69,
        "book_value": 5875.15,
        "daily_change": 38.37,
        "unrealized_gain_loss": 2254.20,
        "market_value": 8129.35,
        "facets": [],
    },
    {
        "name": "LAURENTIAN BANK OF CANADA",
        "symbol": "LB",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 60,
        "average_cost": 34.95,
        "market_price": 40.25,
        "book_value": 2106.98,
        "daily_change": 14.62,
        "unrealized_gain_loss": 308.02,
        "market_value": 2415.00,
        "facets": [],
    },
    {
        "name": "NATIONAL BANK OF CANADA",
        "symbol": "NA",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 41,
        "average_cost": 144.7844,
        "market_price": 197.54,
        "book_value": 5956.12,
        "daily_change": 35.98,
        "unrealized_gain_loss": 2143.02,
        "market_value": 8099.14,
        "facets": [],
    },
    {
        "name": "SUNCOR ENERGY INC",
        "symbol": "SU",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 45,
        "average_cost": 80.2167,
        "market_price": 89.41,
        "book_value": 3624.72,
        "daily_change": 11.0,
        "unrealized_gain_loss": 398.73,
        "market_value": 4023.45,
        "facets": ["materials"],
    },
    {
        "name": "TORONTO-DOMINION BANK",
        "symbol": "TD",
        "asset_class": "STOCK",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 56,
        "average_cost": 106.6512,
        "market_price": 140.67,
        "book_value": 5997.42,
        "daily_change": 31.35,
        "unrealized_gain_loss": 1880.10,
        "market_value": 7877.52,
        "facets": [],
    },
    {
        "name": "ISHARES S&P/TSX GLOBAL GOLD INDEX ETF",
        "symbol": "XGD",
        "asset_class": "ETF",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 30,
        "average_cost": 59.51,
        "market_price": 60.72,
        "book_value": 1790.29,
        "daily_change": 1.75,
        "unrealized_gain_loss": 31.31,
        "market_value": 1821.60,
        "facets": ["gold", "materials"],
    },
    {
        "name": "ISHARES S&P/TSX CAPPED MATERIALS INDEX ETF",
        "symbol": "XMA",
        "asset_class": "ETF",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 30,
        "average_cost": 45.90,
        "market_price": 49.01,
        "book_value": 1377.00,
        "daily_change": 6.78,
        "unrealized_gain_loss": 93.30,
        "market_value": 1470.30,
        "facets": ["materials"],
    },
    {
        "name": "BMO LOW VOLATILITY CANADIAN EQUITY ETF SERIES ETF UNITS",
        "symbol": "ZLB",
        "asset_class": "ETF",
        "currency": "CAD",
        "exchange_code": "TSX",
        "quantity": 40,
        "average_cost": 53.38,
        "market_price": 58.99,
        "book_value": 2145.18,
        "daily_change": 10.0,
        "unrealized_gain_loss": 214.42,
        "market_value": 2359.60,
        "facets": [],
    },
    {
        "name": "CREDICORP LTD",
        "symbol": "BAP",
        "asset_class": "STOCK",
        "currency": "USD",
        "exchange_code": "NYSE",
        "quantity": 10,
        "average_cost": 253.3521,
        "market_price": 361.34,
        "book_value": 2544.21,
        "daily_change": 42.02,
        "unrealized_gain_loss": 1069.19,
        "market_value": 3613.40,
        "facets": [],
    },
    {
        "name": "FIRST SOLAR INC",
        "symbol": "FSLR",
        "asset_class": "STOCK",
        "currency": "USD",
        "exchange_code": "NASDAQ",
        "quantity": 10,
        "average_cost": 200.4675,
        "market_price": 200.35,
        "book_value": 2009.67,
        "daily_change": -0.31,
        "unrealized_gain_loss": -6.17,
        "market_value": 2003.50,
        "facets": [],
    },
    {
        "name": "ALPHABET INC CLASS C CAPITAL STOCK",
        "symbol": "GOOG",
        "asset_class": "STOCK",
        "currency": "USD",
        "exchange_code": "NASDAQ",
        "quantity": 31,
        "average_cost": 255.6971,
        "market_price": 319.21,
        "book_value": 7961.54,
        "daily_change": 24.29,
        "unrealized_gain_loss": 1933.97,
        "market_value": 9895.51,
        "facets": ["big tech"],
    },
    {
        "name": "GLOBAL X FUNDS GLOBAL X DEFENSE TECH ETF",
        "symbol": "SHLD",
        "asset_class": "ETF",
        "currency": "USD",
        "exchange_code": None,
        "quantity": 40,
        "average_cost": 65.8,
        "market_price": 74.52,
        "book_value": 2636.99,
        "daily_change": 13.04,
        "unrealized_gain_loss": 343.81,
        "market_value": 2980.80,
        "facets": ["defense"],
    },
    {
        "name": "ISHARES TR ISHARES SEMICONDUCTOR ETF",
        "symbol": "SOXX",
        "asset_class": "ETF",
        "currency": "USD",
        "exchange_code": "NASDAQ",
        "quantity": 3,
        "average_cost": 387.14,
        "market_price": 393.34,
        "book_value": 1166.41,
        "daily_change": 1.17,
        "unrealized_gain_loss": 13.61,
        "market_value": 1180.02,
        "facets": ["semidconductors"],
    },
    {
        "name": "STATE STREET SPDR S&P 500 ETF TRUST UNITS",
        "symbol": "SPY",
        "asset_class": "ETF",
        "currency": "USD",
        "exchange_code": None,
        "quantity": 2,
        "average_cost": 626.88,
        "market_price": 686.10,
        "book_value": 1258.75,
        "daily_change": 9.01,
        "unrealized_gain_loss": 113.45,
        "market_value": 1372.20,
        "facets": ["big tech"],
    },
    {
        "name": "SUBSEA 7 S A SPONSORED ADR",
        "symbol": "SUBCY",
        "asset_class": "STOCK",
        "currency": "USD",
        "exchange_code": None,
        "quantity": 60,
        "average_cost": 31.605,
        "market_price": 33.21,
        "book_value": 1906.28,
        "daily_change": 4.53,
        "unrealized_gain_loss": 86.32,
        "market_value": 1992.60,
        "facets": ["defense"],
    },
]


def get_account_id(conn: sqlite3.Connection) -> int:
    row = conn.execute(
        """
        SELECT a.id
        FROM accounts a
        JOIN institutions i ON i.id = a.institution_id
        WHERE i.name = ? AND a.account_name = ?
        """,
        ("Scotiabank", "Cash"),
    ).fetchone()
    if row is None:
        raise RuntimeError("Scotiabank Cash account was not found in the database.")
    return row[0]


def get_exchange_id(conn: sqlite3.Connection, exchange_code: str | None) -> int | None:
    if exchange_code is None:
        return None

    row = conn.execute(
        "SELECT id FROM exchanges WHERE code = ?",
        (exchange_code,),
    ).fetchone()
    if row is None:
        raise RuntimeError(f"Exchange code {exchange_code!r} is not seeded in the database.")
    return row[0]


def upsert_instrument(conn: sqlite3.Connection, holding: dict) -> int:
    exchange_id = get_exchange_id(conn, holding["exchange_code"])
    row = conn.execute(
        """
        SELECT id
        FROM instruments
        WHERE symbol = ? AND name = ?
        """,
        (
            holding["symbol"],
            holding["name"],
        ),
    ).fetchone()

    if row is None:
        cursor = conn.execute(
            """
            INSERT INTO instruments(symbol, name, asset_class, exchange_id, currency)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                holding["symbol"],
                holding["name"],
                holding["asset_class"],
                exchange_id,
                holding["currency"],
            ),
        )
        return cursor.lastrowid

    instrument_id = row[0]
    conn.execute(
        """
        UPDATE instruments
        SET asset_class = ?, exchange_id = ?, currency = ?
        WHERE id = ?
        """,
        (
            holding["asset_class"],
            exchange_id,
            holding["currency"],
            instrument_id,
        ),
    )
    return instrument_id


def upsert_facets(conn: sqlite3.Connection, instrument_id: int, facet_names: list[str]) -> None:
    for facet_name in facet_names:
        conn.execute(
            """
            INSERT INTO instrument_facets(instrument_id, facet_name)
            VALUES (?, ?)
            ON CONFLICT(instrument_id, facet_name) DO NOTHING
            """,
            (instrument_id, facet_name),
        )


def upsert_holding(conn: sqlite3.Connection, account_id: int, instrument_id: int, holding: dict) -> None:
    conn.execute(
        """
        INSERT INTO holdings(
            account_id,
            instrument_id,
            quantity,
            average_cost,
            market_price,
            book_value,
            daily_change,
            unrealized_gain_loss,
            market_value,
            as_of_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, DATE('now'))
        ON CONFLICT(account_id, instrument_id, as_of_date) DO UPDATE SET
            quantity = excluded.quantity,
            average_cost = excluded.average_cost,
            market_price = excluded.market_price,
            book_value = excluded.book_value,
            daily_change = excluded.daily_change,
            unrealized_gain_loss = excluded.unrealized_gain_loss,
            market_value = excluded.market_value
        """,
        (
            account_id,
            instrument_id,
            holding["quantity"],
            holding["average_cost"],
            holding["market_price"],
            holding["book_value"],
            holding["daily_change"],
            holding["unrealized_gain_loss"],
            holding["market_value"],
        ),
    )


def populate_scotiabank_cash_holdings() -> None:
    create_db(DB_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        account_id = get_account_id(conn)

        for holding in HOLDINGS:
            instrument_id = upsert_instrument(conn, holding)
            upsert_facets(conn, instrument_id, holding["facets"])
            upsert_holding(conn, account_id, instrument_id, holding)

        conn.commit()


def main() -> None:
    populate_scotiabank_cash_holdings()
    print(f"Loaded {len(HOLDINGS)} holdings into Scotiabank Cash in {DB_PATH}")


if __name__ == "__main__":
    main()