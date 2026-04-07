"""Signal Health Dashboard — main Streamlit application."""

from __future__ import annotations

import streamlit as st

from components.match_rate import render_match_rate
from components.value_distribution import render_value_distribution
from components.deduplication import render_deduplication
from components.event_freshness import render_event_freshness
from utils.loaders import load_demo_data, load_uploaded_data, get_required_columns

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Signal Health Dashboard",
    page_icon="📡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 📡 **Signal Health Dashboard**")
    st.caption("by [AdZeta](https://adzeta.io)")
    st.divider()

    data_source = st.radio(
        "Data Source",
        options=["Use demo data", "Upload CSV"],
        index=0,
    )

    df = None

    if data_source == "Upload CSV":
        st.markdown("#### Required CSV columns")
        st.code("\n".join(get_required_columns()), language="text")
        uploaded = st.file_uploader("Upload your events CSV", type=["csv"])
        if uploaded is not None:
            df = load_uploaded_data(uploaded)
        else:
            st.info("Upload a CSV file to get started.")
    else:
        df = load_demo_data()

    st.divider()

    platform_filter = st.selectbox(
        "Platform Filter",
        options=["All", "Meta only", "Google only"],
        index=0,
    )

# ---------------------------------------------------------------------------
# Apply platform filter
# ---------------------------------------------------------------------------

if df is not None and not df.empty:
    if platform_filter == "Meta only":
        df = df[df["platform"] == "meta"]
    elif platform_filter == "Google only":
        df = df[df["platform"] == "google"]

# ---------------------------------------------------------------------------
# Main content — tabs
# ---------------------------------------------------------------------------

if df is not None:
    tab_match, tab_value, tab_dedup, tab_fresh = st.tabs(
        ["Match Rate", "Value Distribution", "Deduplication", "Event Freshness"]
    )

    with tab_match:
        render_match_rate(df)

    with tab_value:
        render_value_distribution(df)

    with tab_dedup:
        render_deduplication(df)

    with tab_fresh:
        render_event_freshness(df)
else:
    st.title("Signal Health Dashboard")
    st.write("Select a data source from the sidebar to begin.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.divider()
st.caption("Built by [AdZeta](https://adzeta.io) — adzeta.io")
