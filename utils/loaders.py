"""Data loading and validation utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

_REQUIRED_COLUMNS: list[str] = [
    "event_id",
    "event_name",
    "event_timestamp",
    "value",
    "currency",
    "email_provided",
    "phone_provided",
    "external_id_provided",
    "fbp_provided",
    "fbc_provided",
    "gclid_provided",
    "platform",
]


def get_required_columns() -> list[str]:
    """Return the list of required column names for an uploaded CSV."""
    return list(_REQUIRED_COLUMNS)


def _parse_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Convert event_timestamp to datetime."""
    df = df.copy()
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], errors="coerce")
    return df


def load_demo_data() -> pd.DataFrame:
    """Load the bundled demo dataset."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "demo_events.csv"
    df = pd.read_csv(csv_path)
    return _parse_timestamps(df)


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Read and validate a user-uploaded CSV.

    Raises a ``streamlit.error`` and stops execution if required columns are
    missing.
    """
    df = pd.read_csv(uploaded_file)
    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.error(
            f"Uploaded CSV is missing required column(s): **{', '.join(missing)}**. "
            f"Please ensure your file contains all of: {', '.join(_REQUIRED_COLUMNS)}"
        )
        st.stop()
    return _parse_timestamps(df)
