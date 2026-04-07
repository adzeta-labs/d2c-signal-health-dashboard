# Contributing to d2c-signal-health-dashboard

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository.
2. Clone your fork and create a feature branch:

```bash
git checkout -b my-feature
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app locally:

```bash
streamlit run app.py
```

## Development Guidelines

- All dashboard component modules live in `components/`.
- Data loading logic lives in `utils/loaders.py`.
- Use Plotly for all charts.
- Keep all logic generic — no proprietary thresholds, scoring rules or classification labels.

## Pull Requests

1. Ensure the app runs without errors before opening a PR.
2. Keep changes focused — one feature or fix per PR.
3. Target the `main` branch.

## Code Style

- Follow PEP 8.
- Use type annotations for function signatures.

## License

By contributing you agree that your contributions will be licensed under the Apache 2.0 License.
