# d2c-signal-health-dashboard

An open source Streamlit dashboard for monitoring conversion signal health across Meta CAPI and Google Ads.

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/deploy)

![Dashboard Preview](assets/preview.png)

## Features

- **Match Rate Analysis** — per-field identity signal coverage with colour-coded thresholds and horizontal bar charts.
- **Value Distribution** — summary stats, histograms and box plots of conversion values by platform.
- **Deduplication Check** — detects duplicate event IDs and surfaces a duplicate rate.
- **Event Freshness** — measures event age, flags stale or future-timestamped events and charts hourly volume.
- **Platform Filtering** — filter by Meta, Google or view all events together.
- **CSV Upload** — bring your own data or explore with the bundled demo dataset.

## Live Demo

Deploy to Streamlit Cloud by clicking the badge above, or run locally (see below).

## Local Setup

```bash
git clone https://github.com/adzeta-labs/d2c-signal-health-dashboard.git
cd d2c-signal-health-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## CSV Schema

Your uploaded CSV must contain the following columns:

| Column | Type | Description |
|---|---|---|
| `event_id` | string | Unique event identifier |
| `event_name` | string | Event type (e.g. Purchase, AddToCart) |
| `event_timestamp` | datetime | ISO 8601 timestamp of the event |
| `value` | float | Conversion value |
| `currency` | string | Currency code (e.g. USD) |
| `email_provided` | bool | Whether an email was sent with the event |
| `phone_provided` | bool | Whether a phone number was sent |
| `external_id_provided` | bool | Whether an external ID was sent |
| `fbp_provided` | bool | Whether the Meta `_fbp` cookie was sent |
| `fbc_provided` | bool | Whether the Meta `_fbc` cookie was sent |
| `gclid_provided` | bool | Whether a Google Click ID was sent |
| `platform` | string | `meta` or `google` |

A sample file is included at `data/demo_events.csv`.

## Companion Repos

- [adzeta-labs/shopify-ltv-pixel](https://github.com/adzeta-labs/shopify-ltv-pixel)
- [adzeta-labs/ltv-signal-validator](https://github.com/adzeta-labs/ltv-signal-validator)
- [adzeta-labs/ecommerce-ltv-features](https://github.com/adzeta-labs/ecommerce-ltv-features)

## License

Apache 2.0 — see [LICENSE](LICENSE).

---

Built by [AdZeta](https://adzeta.io) — adzeta.io
