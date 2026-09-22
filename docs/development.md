# Development

Install with `pip install -e '.[dev]'`, run `pytest -q`, then `uvicorn nexus.api.main:app --reload`. Keep provider-specific integrations behind interfaces. Every feature should ship with tests, documentation, and an observable failure mode.
