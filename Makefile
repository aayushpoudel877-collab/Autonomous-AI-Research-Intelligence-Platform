install:
	pip install -e '.[dev]'

run:
	uvicorn nexus.api.main:app --reload

test:
	pytest -q

lint:
	ruff check nexus tests
