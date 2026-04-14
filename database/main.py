import streamlit as st

from app_state import render_sidebar_exchange_rate

st.set_page_config(
    page_title="Midas Portfolio",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Midas Portfolio")
render_sidebar_exchange_rate()

st.write(
    """
    Welcome to your multi-account portfolio tracker.
    Use the sidebar to navigate between pages.
    """
)
