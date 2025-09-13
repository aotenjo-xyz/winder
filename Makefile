.PHONY: format lint check create-env update-env

format:
	black .

lint:
	ruff check .

check:
	black --check .
	ruff check .

create-env:
	conda env create -f scripts/environment.yml

update-env:
	conda env update -f scripts/environment.yml --name winding