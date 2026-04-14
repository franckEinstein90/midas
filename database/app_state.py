import streamlit as st

USD_TO_CAD_RATE_KEY = "global_usd_to_cad_rate"


def render_sidebar_exchange_rate() -> float:
    """Render and return the global USD->CAD exchange rate from sidebar."""
    if USD_TO_CAD_RATE_KEY not in st.session_state:
        st.session_state[USD_TO_CAD_RATE_KEY] = 1.38

    with st.sidebar:
        st.markdown("### Global Settings")
        st.number_input(
            "USD to CAD exchange rate",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key=USD_TO_CAD_RATE_KEY,
        )

    return float(st.session_state[USD_TO_CAD_RATE_KEY])