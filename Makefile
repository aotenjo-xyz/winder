.PHONY: format lint check

format:
	black .

lint:
	ruff check .

check:
	black --check .
	ruff check .