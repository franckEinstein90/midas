import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from app_state import render_sidebar_exchange_rate

DB_PATH = Path(__file__).resolve().parent.parent / "midas.db"


@st.cache_data(ttl=60)
def get_all_instruments() -> pd.DataFrame:
    """Get all unique instruments from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT DISTINCT
                i.id,
                i.symbol,
                i.name,
                i.asset_class,
                ex.code AS exchange,
                i.currency
            FROM instruments i
            LEFT JOIN exchanges ex ON ex.id = i.exchange_id
            ORDER BY i.symbol
            """,
            conn,
        )
    return df


@st.cache_data(ttl=60)
def get_all_facets() -> list[str]:
    """Get all available facets from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        facets = conn.execute(
            "SELECT name FROM facets ORDER BY name"
        ).fetchall()
    return [f[0] for f in facets]


def get_instrument_facets(instrument_id: int) -> set[str]:
    """Get facets associated with a specific instrument."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT facet_name FROM instrument_facets WHERE instrument_id = ?",
            (instrument_id,),
        ).fetchall()
    return {row[0] for row in rows}


def add_instrument_facet(instrument_id: int, facet_name: str) -> None:
    """Add a facet to an instrument."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO instrument_facets(instrument_id, facet_name)
            VALUES (?, ?)
            ON CONFLICT(instrument_id, facet_name) DO NOTHING
            """,
            (instrument_id, facet_name),
        )
        conn.commit()


def remove_instrument_facet(instrument_id: int, facet_name: str) -> None:
    """Remove a facet from an instrument."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM instrument_facets WHERE instrument_id = ? AND facet_name = ?",
            (instrument_id, facet_name),
        )
        conn.commit()


def create_facet(facet_name: str, description: str) -> None:
    """Create a new facet."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO facets(name, description) VALUES (?, ?)",
            (facet_name, description),
        )
        conn.commit()


def delete_facet(facet_name: str) -> None:
    """Delete a facet from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM facets WHERE name = ?", (facet_name,))
        conn.commit()


def get_facet_description(facet_name: str) -> str:
    """Get the description of a facet."""
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT description FROM facets WHERE name = ?",
            (facet_name,),
        ).fetchone()
    return row[0] if row else ""


st.set_page_config(page_title="Tags", layout="wide")
st.title("🏷️ Tags & Instruments")
render_sidebar_exchange_rate()

if not DB_PATH.exists():
    st.error("midas.db was not found. Run scripts/create_database.py first.")
    st.stop()

# Initialize session state for selected instrument
if "selected_instrument_symbol" not in st.session_state:
    st.session_state.selected_instrument_symbol = None

# Tabs for tagging and facet management
tab_tagging, tab_facets = st.tabs(["Tag Instruments", "Manage Facets"])

with tab_tagging:
    st.subheader("Tag Instruments")

    # Refresh instruments list
    instruments_df = get_all_instruments()
    all_facets = get_all_facets()

    if instruments_df.empty:
        st.info("No instruments found in the database.")
    else:
        # Create a searchable selector with session state persistence
        symbols = instruments_df["symbol"].tolist()
        default_index = 0
        if st.session_state.selected_instrument_symbol in symbols:
            default_index = symbols.index(st.session_state.selected_instrument_symbol)
        
        selected_symbol = st.selectbox(
            "Select an instrument to tag",
            options=symbols,
            index=default_index,
        )
        st.session_state.selected_instrument_symbol = selected_symbol

        selected_row = instruments_df[
            instruments_df["symbol"] == selected_symbol
        ].iloc[0]
        instrument_id = int(selected_row["id"])

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Name:** {selected_row['name']}")
            st.write(f"**Asset Class:** {selected_row['asset_class']}")
            st.write(f"**Currency:** {selected_row['currency']}")
            if pd.notna(selected_row["exchange"]):
                st.write(f"**Exchange:** {selected_row['exchange']}")

        # Get current facets for this instrument
        current_facets = get_instrument_facets(instrument_id)

        st.subheader("Current Tags")
        if current_facets:
            cols = st.columns(3)
            for idx, facet in enumerate(sorted(current_facets)):
                with cols[idx % 3]:
                    col_remove, col_label = st.columns([0.15, 0.85])
                    with col_remove:
                        if st.button("✕", key=f"remove_{instrument_id}_{facet}"):
                            try:
                                remove_instrument_facet(instrument_id, facet)
                                st.cache_data.clear()
                                st.success(f"Removed tag '{facet}' from {selected_symbol}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error removing tag: {e}")
                    with col_label:
                        st.caption(facet)
        else:
            st.info("No tags assigned to this instrument.")

        st.subheader("Add Tags")
        available_facets = [f for f in all_facets if f not in current_facets]

        if available_facets:
            if "selected_facet_to_add" not in st.session_state:
                st.session_state.selected_facet_to_add = available_facets[0]
            
            if st.session_state.selected_facet_to_add not in available_facets:
                st.session_state.selected_facet_to_add = available_facets[0]
            
            facet_index = available_facets.index(st.session_state.selected_facet_to_add)
            facet_to_add = st.selectbox(
                "Select a tag to add",
                options=available_facets,
                index=facet_index,
            )
            st.session_state.selected_facet_to_add = facet_to_add
            
            if st.button("Add Tag"):
                add_instrument_facet(int(instrument_id), facet_to_add)
                st.cache_data.clear()
                st.rerun()
        else:
            st.info("All available tags are already assigned to this instrument.")

with tab_facets:
    st.subheader("Manage Facets (Tags)")

    # Display existing facets
    st.write("**Existing Facets:**")
    existing_facets = get_all_facets()

    if existing_facets:
        for facet in sorted(existing_facets):
            col1, col2, col3 = st.columns([0.15, 0.75, 0.1])
            with col1:
                if st.button("🗑️", key=f"delete_facet_{facet}"):
                    delete_facet(facet)
                    st.cache_data.clear()
                    st.rerun()
            with col2:
                desc = get_facet_description(facet)
                st.caption(f"**{facet}** — {desc}")
    else:
        st.info("No facets found.")

    st.divider()
    st.write("**Create New Facet:**")

    new_facet_name = st.text_input(
        "Facet name (e.g., 'renewable_energy')",
        key="new_facet_name",
    )
    new_facet_desc = st.text_area(
        "Description (optional, e.g., 'Renewable energy sector exposure')",
        key="new_facet_desc",
        height=80,
    )

    if st.button("Create Facet", key="create_facet_btn"):
        if not new_facet_name:
            st.error("Facet name is required.")
        else:
            try:
                create_facet(
                    new_facet_name.lower().strip(),
                    new_facet_desc or "",
                )
                st.cache_data.clear()
                st.success(f"Facet '{new_facet_name}' created.")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating facet: {e}")
