.PHONY: run-api run-api-test-env test lint format fix check create-tables docker-up docker-down docker-ps docker-logs-api

TEST_DATABASE_URL=postgresql+psycopg://corebank:corebank@localhost:5433/corebank

run-api:
	uvicorn corebank_api.main:app --reload --app-dir apps/api/src

run-api-test-env:
	COREBANK_ENVIRONMENT=test uvicorn corebank_api.main:app --reload --app-dir apps/api/src

test:
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) pytest

lint:
	ruff check apps/api/src apps/api/tests

format:
	ruff format apps/api/src apps/api/tests

fix:
	ruff format apps/api/src apps/api/tests
	ruff check --fix apps/api/src apps/api/tests
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) pytest

check:
	ruff check apps/api/src apps/api/tests
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) pytest

create-tables:
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) PYTHONPATH=apps/api/src python apps/api/scripts/create_tables.py

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-ps:
	docker compose ps

docker-logs-api:
	docker compose logs api