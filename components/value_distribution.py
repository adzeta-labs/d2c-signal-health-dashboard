"""Conversion value distribution component."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_value_distribution(df: pd.DataFrame) -> None:
    """Render the conversion-value distribution section."""
    st.header("Value Distribution")

    if df.empty:
        st.info("No events to analyse.")
        return

    values = df["value"]
    non_null = values.dropna()
    total = len(values)

    null_count = int(values.isna().sum())
    zero_count = int((non_null == 0).sum())
    null_pct = null_count / total * 100 if total else 0
    zero_pct = zero_count / total * 100 if total else 0

    # --- Summary statistics ---
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Min", f"{non_null.min():.2f}" if len(non_null) else "—")
    col2.metric("Max", f"{non_null.max():.2f}" if len(non_null) else "—")
    col3.metric("Mean", f"{non_null.mean():.2f}" if len(non_null) else "—")
    col4.metric("Median", f"{non_null.median():.2f}" if len(non_null) else "—")
    col5.metric("% Zero-value", f"{zero_pct:.1f}%")
    col6.metric("% Null-value", f"{null_pct:.1f}%")

    if zero_pct > 20:
        st.warning(
            f"**{zero_pct:.1f}%** of events have a zero conversion value. "
            "This may reduce signal quality for value-based optimisation."
        )

    # --- Histogram ---
    fig_hist = px.histogram(
        non_null,
        nbins=40,
        title="Conversion Value Histogram",
        labels={"value": "Conversion Value", "count": "Events"},
    )
    fig_hist.update_layout(
        xaxis_title="Conversion Value",
        yaxis_title="Event Count",
        height=350,
        margin=dict(l=10, r=10, t=40, b=30),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- Box plot by platform ---
    plot_df = df.dropna(subset=["value"])
    if not plot_df.empty and "platform" in plot_df.columns:
        fig_box = px.box(
            plot_df,
            x="platform",
            y="value",
            title="Value Spread by Platform",
            color="platform",
        )
        fig_box.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=40, b=30),
        )
        st.plotly_chart(fig_box, use_container_width=True)
