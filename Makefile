.PHONY: run-api test

run-api:
	uvicorn corebank_api.main:app --reload --app-dir apps/api/src

run-api-test-env:
	COREBANK_ENVIRONMENT=test uvicorn corebank_api.main:app --reload --app-dir apps/api/src

test:
	pytest

lint:
	ruff check apps/api/src apps/api/tests

format:
	ruff format apps/api/src apps/api/tests

fix:
	ruff format apps/api/src apps/api/tests
	ruff check --fix apps/api/src apps/api/tests
	pytest

check:
	pytest
	ruff check apps/api/src apps/api/tests