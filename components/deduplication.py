"""Event deduplication analysis component."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_deduplication(df: pd.DataFrame) -> None:
    """Render the deduplication analysis section."""
    st.header("Deduplication")

    if df.empty:
        st.info("No events to analyse.")
        return

    total_events = len(df)
    unique_ids = df["event_id"].nunique()
    duplicate_count = total_events - unique_ids
    dup_rate = duplicate_count / total_events * 100 if total_events else 0

    # --- Summary metrics ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Events", f"{total_events:,}")
    col2.metric("Unique Event IDs", f"{unique_ids:,}")
    col3.metric("Duplicate Events", f"{duplicate_count:,}")
    col4.metric("Duplicate Rate", f"{dup_rate:.1f}%")

    if dup_rate > 5:
        st.warning(
            f"**{dup_rate:.1f}%** of events share a duplicate event ID. "
            "Duplicates can inflate conversion counts and degrade signal accuracy."
        )

    # --- Duplicate table ---
    dup_ids = df["event_id"].value_counts()
    dup_ids = dup_ids[dup_ids > 1].reset_index()
    dup_ids.columns = ["event_id", "occurrences"]

    if not dup_ids.empty:
        st.subheader("Duplicate Event IDs")
        st.dataframe(dup_ids, use_container_width=True, hide_index=True)
    else:
        st.success("No duplicate event IDs detected.")
