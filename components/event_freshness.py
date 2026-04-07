"""Event freshness / latency analysis component."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_event_freshness(df: pd.DataFrame) -> None:
    """Render the event freshness section."""
    st.header("Event Freshness")

    if df.empty:
        st.info("No events to analyse.")
        return

    now = pd.Timestamp.utcnow()
    timestamps = pd.to_datetime(df["event_timestamp"], errors="coerce")

    age_hours = (now - timestamps).dt.total_seconds() / 3600
    total = len(df)

    median_age = float(age_hours.median()) if total else 0
    older_24h_pct = float((age_hours > 24).sum() / total * 100) if total else 0
    future_pct = float((age_hours < 0).sum() / total * 100) if total else 0

    # --- Summary metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Median Event Age", f"{median_age:.1f} hrs")
    col2.metric("Events > 24 h Old", f"{older_24h_pct:.1f}%")
    col3.metric("Future Timestamps", f"{future_pct:.1f}%")

    if older_24h_pct > 10:
        st.warning(
            f"**{older_24h_pct:.1f}%** of events are older than 24 hours. "
            "Stale events may be down-weighted by ad platforms."
        )

    if future_pct > 0:
        st.info(
            f"**{future_pct:.1f}%** of events have timestamps in the future. "
            "Check for clock-sync or timezone issues."
        )

    # --- Hourly volume chart ---
    ts_df = df.copy()
    ts_df["_ts"] = timestamps
    ts_df = ts_df.dropna(subset=["_ts"])
    ts_df["hour_bucket"] = ts_df["_ts"].dt.floor("h")

    hourly = (
        ts_df.groupby("hour_bucket")
        .size()
        .reset_index(name="event_count")
        .sort_values("hour_bucket")
    )

    if not hourly.empty:
        fig = px.bar(
            hourly,
            x="hour_bucket",
            y="event_count",
            title="Event Volume by Hour",
            labels={"hour_bucket": "Hour", "event_count": "Events"},
        )
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=40, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)
