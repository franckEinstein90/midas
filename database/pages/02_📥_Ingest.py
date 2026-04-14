import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from app_state import render_sidebar_exchange_rate

DB_PATH = Path(__file__).resolve().parent.parent / "midas.db"
STATEMENTS_DIR = Path(__file__).resolve().parent.parent / ".statements"

COLUMN_MAPPINGS = {
    "symbol": ["symbol", "ticker", "code"],
    "name": ["name", "security name", "description", "instrument", "security"],
    "asset_class": ["asset class", "asset_class", "type", "asset type", "class"],
    "currency": ["currency", "ccy"],
    "quantity": ["quantity", "qty", "shares", "units"],
    "average_cost": ["average cost ($)", "average_cost", "avg_cost", "cost_basis", "acb"],
    "market_price": ["market price ($)", "market_price", "price", "current price", "last price"],
    "book_value": ["book value ($)", "book_value", "cost value"],
    "daily_change": ["daily change ($)", "daily_change", "day_change", "change"],
    "unrealized_gain_loss": [
        "all time value change ($)",
        "unrealized_gain_loss",
        "unrealized_gain",
        "unrealized p&l",
    ],
    "market_value": ["market value ($)", "market_value", "current_value", "value"],
}

REQUIRED_COLUMNS = ["symbol", "name", "quantity"]


def get_institutions() -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT name FROM institutions ORDER BY name").fetchall()
    return [row[0] for row in rows]


def get_accounts_for_institution(institution: str) -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT a.account_name
            FROM accounts a
            JOIN institutions i ON i.id = a.institution_id
            WHERE i.name = ?
            ORDER BY a.account_name
            """,
            (institution,),
        ).fetchall()
    return [row[0] for row in rows]


def get_account_id(institution: str, account_name: str) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT a.id
            FROM accounts a
            JOIN institutions i ON i.id = a.institution_id
            WHERE i.name = ? AND a.account_name = ?
            """,
            (institution, account_name),
        ).fetchone()
    if row is None:
        raise RuntimeError(f"Account not found: {institution}/{account_name}")
    return int(row[0])


def save_uploaded_statement(uploaded_file) -> Path:
    STATEMENTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = Path(uploaded_file.name).name
    target_path = STATEMENTS_DIR / f"{timestamp}_{safe_name}"
    target_path.write_bytes(uploaded_file.getbuffer())
    return target_path


def infer_column_names(df: pd.DataFrame) -> dict[str, str]:
    inferred: dict[str, str] = {}
    normalized = {str(col).strip().lower(): col for col in df.columns}

    for target_col, candidates in COLUMN_MAPPINGS.items():
        for candidate in candidates:
            if candidate in normalized:
                inferred[target_col] = normalized[candidate]
                break

    return inferred


def normalize_asset_class(value: str) -> str:
    value_lower = str(value).lower().strip()
    if "equity" in value_lower or "stock" in value_lower:
        return "STOCK"
    if "etf" in value_lower:
        return "ETF"
    if "bond" in value_lower or "fixed" in value_lower:
        return "BOND"
    if "gic" in value_lower:
        return "GIC"
    return "STOCK"


def to_float_or_none(value):
    if pd.isna(value) or value == "":
        return None
    return float(value)


def build_import_rows(df: pd.DataFrame, column_mapping: dict[str, str]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    errors: list[str] = []

    for idx, row in df.iterrows():
        try:
            symbol_col = column_mapping.get("symbol")
            name_col = column_mapping.get("name")
            quantity_col = column_mapping.get("quantity")

            symbol = str(row.get(symbol_col, "")).strip() if symbol_col else ""
            name = str(row.get(name_col, "")).strip() if name_col else ""

            quantity_raw = row.get(quantity_col, 0) if quantity_col else 0
            quantity = 0.0 if pd.isna(quantity_raw) else float(quantity_raw)

            if not symbol or symbol.lower() in {"none", "nan"}:
                errors.append(f"Row {idx + 2}: missing symbol")
                continue
            if not name or name.lower() in {"none", "nan"}:
                errors.append(f"Row {idx + 2}: missing security name")
                continue

            asset_class_col = column_mapping.get("asset_class")
            currency_col = column_mapping.get("currency")

            asset_class_val = row.get(asset_class_col, "STOCK") if asset_class_col else "STOCK"
            asset_class = normalize_asset_class(asset_class_val)

            currency_val = row.get(currency_col, "CAD") if currency_col else "CAD"
            currency = "CAD" if pd.isna(currency_val) else str(currency_val).strip()

            parsed = {
                "symbol": symbol,
                "name": name,
                "asset_class": asset_class,
                "currency": currency,
                "quantity": quantity,
                "average_cost": to_float_or_none(row.get(column_mapping.get("average_cost"))),
                "market_price": to_float_or_none(row.get(column_mapping.get("market_price"))),
                "book_value": to_float_or_none(row.get(column_mapping.get("book_value"))),
                "daily_change": to_float_or_none(row.get(column_mapping.get("daily_change"))),
                "unrealized_gain_loss": to_float_or_none(
                    row.get(column_mapping.get("unrealized_gain_loss"))
                ),
                "market_value": to_float_or_none(row.get(column_mapping.get("market_value"))),
            }
            rows.append(parsed)
        except Exception as exc:
            errors.append(f"Row {idx + 2}: {exc}")

    return rows, errors


def get_existing_account_holdings(account_id: int) -> dict[str, dict]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT i.symbol, i.name, i.asset_class, i.currency, h.quantity, h.market_value
            FROM holdings h
            JOIN instruments i ON i.id = h.instrument_id
            JOIN (
                SELECT instrument_id, MAX(as_of_date) AS max_date
                FROM holdings
                WHERE account_id = ?
                GROUP BY instrument_id
            ) latest ON latest.instrument_id = h.instrument_id AND latest.max_date = h.as_of_date
            WHERE h.account_id = ?
            """,
            (account_id, account_id),
        ).fetchall()

    existing: dict[str, dict] = {}
    for symbol, name, asset_class, currency, quantity, market_value in rows:
        existing[str(symbol).strip()] = {
            "symbol": symbol,
            "name": name,
            "asset_class": asset_class,
            "currency": currency,
            "quantity": float(quantity) if quantity is not None else 0.0,
            "market_value": float(market_value) if market_value is not None else 0.0,
        }
    return existing


def build_reconciliation_report(import_rows: list[dict], account_id: int) -> dict:
    existing = get_existing_account_holdings(account_id)
    incoming = {row["symbol"]: row for row in import_rows}

    symbols_existing = set(existing.keys())
    symbols_incoming = set(incoming.keys())

    additions = [incoming[s] for s in sorted(symbols_incoming - symbols_existing)]

    removals = [existing[s] for s in sorted(symbols_existing - symbols_incoming)]

    updates = []
    unchanged = []
    for symbol in sorted(symbols_existing & symbols_incoming):
        old = existing[symbol]
        new = incoming[symbol]
        old_qty = round(old.get("quantity", 0.0), 8)
        new_qty = round(new.get("quantity", 0.0), 8)
        old_mv = round(old.get("market_value", 0.0), 2)
        new_mv = round(new.get("market_value") or 0.0, 2)

        if old_qty != new_qty or old_mv != new_mv:
            updates.append(
                {
                    "symbol": symbol,
                    "name": new["name"],
                    "old_quantity": old_qty,
                    "new_quantity": new_qty,
                    "old_market_value": old_mv,
                    "new_market_value": new_mv,
                }
            )
        else:
            unchanged.append({"symbol": symbol, "name": new["name"], "quantity": new_qty})

    return {
        "additions": additions,
        "updates": updates,
        "removals": removals,
        "unchanged": unchanged,
        "incoming_rows": import_rows,
    }


def get_or_create_instrument(conn: sqlite3.Connection, row: dict) -> int:
    symbol = row["symbol"]
    name = row["name"]

    existing = conn.execute(
        "SELECT id FROM instruments WHERE symbol = ?",
        (symbol,),
    ).fetchone()

    if existing is None:
        cursor = conn.execute(
            """
            INSERT INTO instruments(symbol, name, asset_class, currency)
            VALUES (?, ?, ?, ?)
            """,
            (symbol, name, row["asset_class"], row["currency"]),
        )
        return int(cursor.lastrowid)

    instrument_id = int(existing[0])
    conn.execute(
        """
        UPDATE instruments
        SET name = ?, asset_class = ?, currency = ?
        WHERE id = ?
        """,
        (name, row["asset_class"], row["currency"], instrument_id),
    )
    return instrument_id


def apply_reconciliation(report: dict, account_id: int) -> tuple[int, int, int]:
    applied_adds = 0
    applied_updates = 0
    applied_removals = 0

    today = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(DB_PATH) as conn:
        for row in report["incoming_rows"]:
            instrument_id = get_or_create_instrument(conn, row)

            existing_today = conn.execute(
                """
                SELECT 1 FROM holdings
                WHERE account_id = ? AND instrument_id = ? AND as_of_date = ?
                """,
                (account_id, instrument_id, today),
            ).fetchone()

            conn.execute(
                """
                INSERT INTO holdings(
                    account_id, instrument_id, quantity, average_cost,
                    market_price, book_value, daily_change,
                    unrealized_gain_loss, market_value, as_of_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    row["quantity"],
                    row["average_cost"],
                    row["market_price"],
                    row["book_value"],
                    row["daily_change"],
                    row["unrealized_gain_loss"],
                    row["market_value"],
                    today,
                ),
            )

            if existing_today is None:
                applied_adds += 1
            else:
                applied_updates += 1

        for row in report["removals"]:
            instrument = conn.execute(
                "SELECT id FROM instruments WHERE symbol = ?",
                (row["symbol"],),
            ).fetchone()
            if instrument is None:
                continue

            instrument_id = int(instrument[0])
            conn.execute(
                """
                INSERT INTO holdings(
                    account_id, instrument_id, quantity, average_cost,
                    market_price, book_value, daily_change,
                    unrealized_gain_loss, market_value, as_of_date
                )
                VALUES (?, ?, 0, NULL, NULL, NULL, NULL, NULL, 0, ?)
                ON CONFLICT(account_id, instrument_id, as_of_date) DO UPDATE SET
                    quantity = 0,
                    average_cost = NULL,
                    market_price = NULL,
                    book_value = NULL,
                    daily_change = NULL,
                    unrealized_gain_loss = NULL,
                    market_value = 0
                """,
                (account_id, instrument_id, today),
            )
            applied_removals += 1

        conn.commit()

    return applied_adds, applied_updates, applied_removals


st.set_page_config(page_title="Ingest", layout="wide")
st.title("📥 Ingest Holdings Data")
render_sidebar_exchange_rate()

if not DB_PATH.exists():
    st.error("midas.db was not found. Run scripts/create_database.py first.")
    st.stop()

if "saved_statement_path" not in st.session_state:
    st.session_state.saved_statement_path = None
if "saved_statement_name" not in st.session_state:
    st.session_state.saved_statement_name = None
if "reconciliation_report" not in st.session_state:
    st.session_state.reconciliation_report = None

col1, col2 = st.columns(2)
institutions = get_institutions()
with col1:
    selected_institution = st.selectbox("Select Institution", options=institutions)
with col2:
    selected_account = st.selectbox(
        "Select Account",
        options=get_accounts_for_institution(selected_institution),
    )

st.divider()
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file with holdings data",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file:
    is_already_saved = (
        st.session_state.saved_statement_name == uploaded_file.name
        and st.session_state.saved_statement_path is not None
    )

    if not is_already_saved:
        st.info("Save the uploaded statement to .statements before processing.")
        if st.button("Save Statement"):
            saved_path = save_uploaded_statement(uploaded_file)
            st.session_state.saved_statement_name = uploaded_file.name
            st.session_state.saved_statement_path = str(saved_path)
            st.session_state.reconciliation_report = None
            st.success(f"Saved statement: {saved_path}")
            st.rerun()
        st.stop()

    saved_path = Path(st.session_state.saved_statement_path)
    st.caption(f"Saved statement: {saved_path}")

    try:
        if saved_path.suffix.lower() == ".csv":
            df = pd.read_csv(saved_path)
        else:
            df = pd.read_excel(saved_path)
    except Exception as exc:
        st.error(f"Failed to read saved statement: {exc}")
        st.stop()

    st.subheader("Preview")
    st.dataframe(df.head(10), width="stretch", hide_index=True)

    inferred_mapping = infer_column_names(df)
    st.subheader("Column Mapping")
    st.info("Review mappings, then generate a reconciliation report before applying changes.")

    column_mapping: dict[str, str] = {}
    mapping_cols = st.columns(2)
    available_cols = ["(skip)"] + list(df.columns)

    for i, target in enumerate(COLUMN_MAPPINGS.keys()):
        source = inferred_mapping.get(target, "(skip)")
        default_idx = available_cols.index(source) if source in available_cols else 0
        with mapping_cols[i % 2]:
            selected = st.selectbox(
                target,
                options=available_cols,
                index=default_idx,
                key=f"mapping_{target}",
            )
        if selected != "(skip)":
            column_mapping[target] = selected

    missing_required = [c for c in REQUIRED_COLUMNS if c not in column_mapping]
    if missing_required:
        st.error(f"Missing required mappings: {', '.join(missing_required)}")
        st.stop()

    account_id = get_account_id(selected_institution, selected_account)

    st.divider()
    if st.button("Generate Reconciliation Report"):
        parsed_rows, parse_errors = build_import_rows(df, column_mapping)
        report = build_reconciliation_report(parsed_rows, account_id)
        report["parse_errors"] = parse_errors
        report["account_id"] = account_id
        st.session_state.reconciliation_report = report
        st.rerun()

    report = st.session_state.reconciliation_report
    if report is not None:
        st.subheader("Reconciliation Report")

        metrics = st.columns(4)
        metrics[0].metric("In file", len(report["incoming_rows"]))
        metrics[1].metric("Add holdings", len(report["additions"]))
        metrics[2].metric("Update holdings", len(report["updates"]))
        metrics[3].metric("Remove holdings", len(report["removals"]))

        if report.get("parse_errors"):
            with st.expander(f"Parse Warnings ({len(report['parse_errors'])})"):
                for err in report["parse_errors"]:
                    st.text(err)

        if report["additions"]:
            st.markdown("**New Instruments/Holdings To Add**")
            st.dataframe(pd.DataFrame(report["additions"]), width="stretch", hide_index=True)

        if report["updates"]:
            st.markdown("**Existing Holdings To Update**")
            st.dataframe(pd.DataFrame(report["updates"]), width="stretch", hide_index=True)

        if report["removals"]:
            st.markdown("**Holdings To Remove (set quantity to 0 for today's snapshot)**")
            st.dataframe(pd.DataFrame(report["removals"]), width="stretch", hide_index=True)

        if st.button("Approve And Apply Changes", type="primary"):
            adds, updates, removals = apply_reconciliation(report, account_id)
            st.session_state.reconciliation_report = None
            st.success(
                f"Applied reconciliation for {selected_institution}/{selected_account}: "
                f"{adds} added, {updates} updated, {removals} removed."
            )
else:
    st.info("Upload a CSV or Excel file to get started.")
