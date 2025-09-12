.PHONY: format lint check

format:
	black .

lint:
	ruff .

check:
	black --check .
	ruff --check .