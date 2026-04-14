import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from app_state import render_sidebar_exchange_rate

DB_PATH = Path(__file__).resolve().parent.parent / "midas.db"
UNTAGGED_LABEL = "(untagged)"


def gain_loss_color(value: object) -> str:
    if pd.isna(value):
        return ""
    try:
        return "color: red;" if float(value) < 0 else ""
    except (TypeError, ValueError):
        return ""


def save_instrument_facets(instrument_id: int, selected_facets: list[str]) -> None:
    """Replace facet assignments for one instrument."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM instrument_facets WHERE instrument_id = ?",
            (instrument_id,),
        )
        conn.executemany(
            "INSERT INTO instrument_facets (instrument_id, facet_name) VALUES (?, ?)",
            [(instrument_id, facet_name) for facet_name in selected_facets],
        )
        conn.commit()


def get_instrument_account_breakdown(instrument_id: int) -> pd.DataFrame:
    """Return holdings breakdown by institution/account for one instrument."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT
                inst.name AS institution,
                acc.account_name,
                ROUND(SUM(h.quantity), 6) AS quantity,
                ROUND(SUM(h.book_value), 2) AS book_value,
                ROUND(SUM(h.market_value), 2) AS market_value,
                ROUND(SUM(h.unrealized_gain_loss), 2) AS unrealized_gain_loss
            FROM holdings h
            JOIN accounts acc ON acc.id = h.account_id
            JOIN institutions inst ON inst.id = acc.institution_id
            WHERE h.instrument_id = ?
            GROUP BY inst.name, acc.account_name
            ORDER BY inst.name, acc.account_name
            """,
            conn,
            params=(instrument_id,),
        )


@st.dialog("Edit Instrument Facets")
def edit_instrument_dialog(
    instrument_id: int,
    symbol: str,
    name: str,
    current_facets: list[str],
    all_facets: list[str],
) -> None:
    st.write(f"{symbol} - {name}")

    account_breakdown = get_instrument_account_breakdown(instrument_id)
    st.markdown("**Holdings by Account**")
    if account_breakdown.empty:
        st.info("No account holdings found for this instrument.")
    else:
        st.dataframe(
            account_breakdown.style.format(
                {
                    "book_value": "{:,.2f}",
                    "market_value": "{:,.2f}",
                    "unrealized_gain_loss": "{:,.2f}",
                }
            ).map(gain_loss_color, subset=["unrealized_gain_loss"]),
            use_container_width=True,
            hide_index=True,
        )

    updated_facets = st.multiselect(
        "Assigned facets",
        options=all_facets,
        default=current_facets,
        key=f"edit_facets_{instrument_id}",
    )

    c1, c2 = st.columns(2)
    if c1.button("Save", type="primary", key=f"save_facets_{instrument_id}"):
        save_instrument_facets(instrument_id, sorted(updated_facets))
        load_data.clear()
        st.success("Facet assignments updated.")
        st.rerun()
    if c2.button("Cancel", key=f"cancel_facets_{instrument_id}"):
        st.rerun()


@st.cache_data(ttl=60)
def load_data() -> tuple[pd.DataFrame, list[str]]:
    """Load all holdings (grouped by instrument) and all facets."""
    with sqlite3.connect(DB_PATH) as conn:
        holdings = pd.read_sql_query(
            """
            SELECT
                i.id AS instrument_id,
                i.symbol,
                i.name,
                i.asset_class,
                ex.code AS exchange,
                i.currency,
                ROUND(SUM(h.quantity), 6)          AS quantity,
                ROUND(AVG(h.average_cost), 4)       AS average_cost,
                ROUND(AVG(h.market_price), 4)       AS market_price,
                ROUND(SUM(h.book_value), 2)         AS book_value,
                ROUND(SUM(h.market_value), 2)       AS market_value,
                ROUND(SUM(h.unrealized_gain_loss), 2) AS unrealized_gain_loss
            FROM holdings h
            JOIN instruments i ON i.id = h.instrument_id
            LEFT JOIN exchanges ex ON ex.id = i.exchange_id
            GROUP BY i.id, i.symbol, i.name, i.asset_class, ex.code, i.currency
            ORDER BY i.symbol
            """,
            conn,
        )

        # facets per instrument  (comma-separated for display; one row per tag for filtering)
        facet_map = pd.read_sql_query(
            """
            SELECT instrument_id, facet_name
            FROM instrument_facets
            """,
            conn,
        )

        all_facets: list[str] = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM facets ORDER BY name"
            ).fetchall()
        ]

    # attach a comma-separated tags column to holdings
    if not facet_map.empty:
        tags_by_instrument = (
            facet_map.groupby("instrument_id")["facet_name"]
            .apply(lambda s: ", ".join(sorted(s)))
            .reset_index()
            .rename(columns={"facet_name": "tags"})
        )
        holdings = holdings.merge(tags_by_instrument, on="instrument_id", how="left")
    else:
        holdings["tags"] = ""

    holdings["tags"] = holdings["tags"].fillna("")

    return holdings, all_facets


# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="By Category", layout="wide")
st.title("🗂️ By Category")
st.caption(f"Database: {DB_PATH}")
usd_to_cad_rate = render_sidebar_exchange_rate()

if not DB_PATH.exists():
    st.error("midas.db was not found. Run scripts/create_database.py first.")
    st.stop()

try:
    holdings, all_facets = load_data()
except Exception as exc:
    st.exception(exc)
    st.stop()

# ── tag filter ────────────────────────────────────────────────────────────────
filter_categories = all_facets + [UNTAGGED_LABEL]
all_asset_classes = sorted(holdings["asset_class"].dropna().unique().tolist())
facets_key = "by_category_facet_filter_df"
if facets_key not in st.session_state:
    st.session_state[facets_key] = pd.DataFrame(
        {
            "in": [True for _ in filter_categories],
            "facet": filter_categories,
        }
    )
else:
    current_df = st.session_state[facets_key]
    current_in = {
        str(row["facet"]): bool(row["in"])
        for _, row in current_df.iterrows()
    }
    st.session_state[facets_key] = pd.DataFrame(
        {
            "in": [current_in.get(facet, True) for facet in filter_categories],
            "facet": filter_categories,
        }
    )

selected_asset_classes: list[str] = all_asset_classes.copy()
with st.expander("Filter", expanded=False):
    left_col, right_col = st.columns([2, 1])

    with left_col:
        edited_facets = st.data_editor(
            st.session_state[facets_key],
            key="by_category_facet_editor",
            hide_index=True,
            width="stretch",
            num_rows="fixed",
            column_config={
                "in": st.column_config.CheckboxColumn("In"),
                "facet": st.column_config.TextColumn("Facet", disabled=True),
            },
        )
        st.session_state[facets_key] = edited_facets

    with right_col:
        st.caption("Actions")
        if st.button("Select all", width="stretch"):
            st.session_state[facets_key]["in"] = True
            st.rerun()
        if st.button("Clear all", width="stretch"):
            st.session_state[facets_key]["in"] = False
            st.rerun()

        selected_asset_classes = st.multiselect(
            "Asset class",
            options=all_asset_classes,
            default=all_asset_classes,
            key="by_category_asset_class_filter",
        )

if not all_facets:
    st.info("No named facets exist yet. Only untagged instruments can be filtered.")

st.divider()

# ── filter logic ──────────────────────────────────────────────────────────────
selected: set[str] = set()
facets_key = "by_category_facet_filter_df"
if facets_key in st.session_state:
    selected = {
        str(row["facet"])
        for _, row in st.session_state[facets_key].iterrows()
        if bool(row["in"])
    }

if selected:
    selected_named_facets = selected - {UNTAGGED_LABEL}
    include_untagged = UNTAGGED_LABEL in selected

    def matches(row_tags: str) -> bool:
        if not row_tags:
            return include_untagged
        instrument_tags = {t.strip() for t in row_tags.split(",")}
        return bool(instrument_tags & selected_named_facets)

    filtered = holdings[holdings["tags"].apply(matches)]
else:
    filtered = holdings.iloc[0:0]

filtered = filtered.copy()
filtered["Gain/Loss %"] = filtered.apply(
    lambda row: (row["unrealized_gain_loss"] / row["book_value"])
    if pd.notna(row["book_value"]) and row["book_value"] not in (0, 0.0)
    else None,
    axis=1,
)

if selected_asset_classes:
    filtered = filtered[filtered["asset_class"].isin(selected_asset_classes)]
else:
    filtered = filtered.iloc[0:0]

filtered["book_value_cad"] = filtered.apply(
    lambda row: row["book_value"] * usd_to_cad_rate
    if str(row["currency"]).upper() == "USD"
    else row["book_value"],
    axis=1,
)

# ── summary metrics ───────────────────────────────────────────────────────────
total_positions = len(filtered)
total_market_value = float(filtered["market_value"].fillna(0).sum())
total_unrealized = float(filtered["unrealized_gain_loss"].fillna(0).sum())

c1, c2, c3 = st.columns(3)
c1.metric("Instruments", total_positions)
c2.metric("Total Market Value", f"{total_market_value:,.2f}")
c3.metric("Unrealized Gain/Loss", f"{total_unrealized:,.2f}")

# ── instruments table ─────────────────────────────────────────────────────────
st.subheader("Instruments")

display_df = filtered.drop(columns=["instrument_id", "unrealized_gain_loss"]).reset_index(drop=True)
display_df = display_df[
    [
        "symbol",
        "name",
        "asset_class",
        "exchange",
        "currency",
        "quantity",
        "average_cost",
        "market_price",
        "book_value",
        "book_value_cad",
        "market_value",
        "Gain/Loss %",
        "tags",
    ]
]
table_event = st.dataframe(
    display_df.style.format(
        {
            "average_cost": "{:,.2f}",
            "market_price": "{:,.2f}",
            "book_value": "{:,.2f}",
            "book_value_cad": "{:,.2f}",
            "market_value": "{:,.2f}",
            "Gain/Loss %": "{:.2%}",
        }
    ).map(gain_loss_color, subset=["Gain/Loss %"]),
    width="stretch",
    height=700,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="by_category_instruments_table",
)

selected_rows: list[int] = []
if table_event is not None:
    try:
        selected_rows = list(table_event.selection.rows)
    except Exception:
        if isinstance(table_event, dict):
            selected_rows = table_event.get("selection", {}).get("rows", [])

open_selected = st.button(
    "Edit Selected Instrument",
    type="primary",
    disabled=not selected_rows,
)

if selected_rows and open_selected:
    selected_idx = int(selected_rows[0])
    selected_row = filtered.reset_index(drop=True).iloc[selected_idx]
    current_facets = [
        facet.strip()
        for facet in str(selected_row["tags"]).split(",")
        if facet.strip()
    ]
    edit_instrument_dialog(
        instrument_id=int(selected_row["instrument_id"]),
        symbol=str(selected_row["symbol"]),
        name=str(selected_row["name"]),
        current_facets=current_facets,
        all_facets=all_facets,
    )
