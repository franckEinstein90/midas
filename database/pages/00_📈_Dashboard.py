import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from app_state import render_sidebar_exchange_rate

DB_PATH = Path(__file__).resolve().parent.parent / "midas.db"


def gain_loss_color(value: object) -> str:
    if pd.isna(value):
        return ""
    try:
        return "color: red;" if float(value) < 0 else ""
    except (TypeError, ValueError):
        return ""


@st.cache_data(ttl=60)
def load_holdings() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        summary = pd.read_sql_query(
            """
            SELECT
                inst.name AS institution,
                acc.account_name,
                COUNT(*) AS positions,
                ROUND(SUM(h.market_value), 2) AS total_market_value
            FROM holdings h
            JOIN accounts acc ON acc.id = h.account_id
            JOIN institutions inst ON inst.id = acc.institution_id
            GROUP BY inst.name, acc.account_name
            ORDER BY inst.name, acc.account_name
            """,
            conn,
        )
        holdings = pd.read_sql_query(
            """
            SELECT
                inst.name AS institution,
                acc.account_name,
                i.symbol,
                i.name,
                i.asset_class,
                ex.code AS exchange,
                i.currency,
                h.quantity,
                h.average_cost,
                h.market_price,
                h.market_value,
                h.unrealized_gain_loss,
                h.as_of_date
            FROM holdings h
            JOIN instruments i ON i.id = h.instrument_id
            JOIN accounts acc ON acc.id = h.account_id
            JOIN institutions inst ON inst.id = acc.institution_id
            LEFT JOIN exchanges ex ON ex.id = i.exchange_id
            ORDER BY inst.name, acc.account_name, i.symbol
            """,
            conn,
        )
    return summary, holdings


st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📈 Dashboard")
st.caption(f"Database: {DB_PATH}")
render_sidebar_exchange_rate()

if st.button("🔄 Refresh"):
    load_holdings.clear()
    st.rerun()

if not DB_PATH.exists():
    st.error("midas.db was not found. Run scripts/create_database.py first.")
    st.stop()

try:
    summary, holdings = load_holdings()
except Exception as exc:
    st.exception(exc)
    st.stop()

holdings = holdings.copy()
holdings["gain_loss_pct"] = holdings.apply(
    lambda row: (row["unrealized_gain_loss"] / (row["market_value"] - row["unrealized_gain_loss"]))
    if pd.notna(row["market_value"])
    and pd.notna(row["unrealized_gain_loss"])
    and (row["market_value"] - row["unrealized_gain_loss"]) not in (0, 0.0)
    else None,
    axis=1,
)

st.success("Connected to midas.db")

total_positions = int(len(holdings.index))
total_market_value = float(holdings["market_value"].fillna(0).sum())
total_unrealized = float(holdings["unrealized_gain_loss"].fillna(0).sum())

col1, col2, col3 = st.columns(3)
col1.metric("Positions", total_positions)
col2.metric("Market Value", f"{total_market_value:,.2f}")
col3.metric("Unrealized Gain/Loss", f"{total_unrealized:,.2f}")

st.subheader("Accounts Summary")
st.dataframe(
    summary.style.format({"total_market_value": "{:,.2f}"}),
    width="stretch",
    hide_index=True,
)

institutions = sorted(holdings["institution"].dropna().unique().tolist())
selected_institutions = st.multiselect(
    "Filter by institution",
    options=institutions,
    default=institutions,
)

filtered = holdings[holdings["institution"].isin(selected_institutions)]

st.subheader("Holdings")
st.dataframe(
    filtered.rename(columns={"gain_loss_pct": "Gain/Loss %"}).style.format(
        {
            "average_cost": "{:,.2f}",
            "market_price": "{:,.2f}",
            "market_value": "{:,.2f}",
            "unrealized_gain_loss": "{:,.2f}",
            "Gain/Loss %": "{:.2%}",
        }
    ).map(gain_loss_color, subset=["unrealized_gain_loss", "Gain/Loss %"]),
    width="stretch",
    hide_index=True,
)
