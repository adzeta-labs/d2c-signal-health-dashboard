"""Match-rate / identity signal coverage component."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

_IDENTITY_FIELDS: list[str] = [
    "email_provided",
    "phone_provided",
    "external_id_provided",
    "fbp_provided",
    "fbc_provided",
    "gclid_provided",
]

_FIELD_LABELS: dict[str, str] = {
    "email_provided": "Email",
    "phone_provided": "Phone",
    "external_id_provided": "External ID",
    "fbp_provided": "fbp (Meta)",
    "fbc_provided": "fbc (Meta)",
    "gclid_provided": "gclid (Google)",
}


def _coverage_colour(pct: float) -> str:
    """Return a colour hex based on generic display thresholds."""
    if pct >= 80:
        return "#2ecc71"  # green
    if pct >= 50:
        return "#f39c12"  # amber
    return "#e74c3c"  # red


def render_match_rate(df: pd.DataFrame) -> None:
    """Render the identity signal match-rate section."""
    st.header("Identity Signal Match Rate")

    if df.empty:
        st.info("No events to analyse.")
        return

    coverages: dict[str, float] = {}
    for field in _IDENTITY_FIELDS:
        if field in df.columns:
            coverages[field] = float(df[field].sum() / len(df) * 100)
        else:
            coverages[field] = 0.0

    overall = sum(coverages.values()) / len(coverages)

    # --- Overall score ---
    colour = _coverage_colour(overall)
    st.markdown(
        f"### Overall Identity Signal Coverage: "
        f"<span style='color:{colour}'>{overall:.1f}%</span>",
        unsafe_allow_html=True,
    )
    st.caption("Simple average of per-field coverage rates.")

    # --- Per-field metrics ---
    cols = st.columns(3)
    for idx, (field, pct) in enumerate(coverages.items()):
        col = cols[idx % 3]
        col.metric(label=_FIELD_LABELS.get(field, field), value=f"{pct:.1f}%")

    # --- Horizontal bar chart ---
    labels = [_FIELD_LABELS.get(f, f) for f in coverages]
    values = list(coverages.values())
    colours = [_coverage_colour(v) for v in values]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=colours,
            text=[f"{v:.1f}%" for v in values],
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Coverage by Identity Field",
        xaxis_title="Coverage %",
        yaxis_title="",
        xaxis=dict(range=[0, 100]),
        height=350,
        margin=dict(l=10, r=10, t=40, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)
