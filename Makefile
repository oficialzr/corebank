.PHONY: run-api run-api-test-env run-web build-web generate-api promote-admin test-web test-e2e test lint format fix check migrate https-cert docker-up docker-down docker-ps docker-logs-api

TEST_DATABASE_URL=postgresql+psycopg://corebank:corebank@localhost:5433/corebank

run-api:
	uvicorn corebank_api.main:app --reload --app-dir apps/api/src

run-api-test-env:
	COREBANK_ENVIRONMENT=test uvicorn corebank_api.main:app --reload --app-dir apps/api/src

run-web:
	npm --prefix apps/web run dev

build-web:
	npm --prefix apps/web run build

generate-api:
	PYTHONPATH=apps/api/src .venv/bin/python apps/api/scripts/export_openapi.py apps/web/openapi.json
	npm --prefix apps/web run generate:api

promote-admin:
	@test -n "$(EMAIL)" || (echo "Usage: make promote-admin EMAIL=user@example.com" && exit 1)
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) PYTHONPATH=apps/api/src .venv/bin/python apps/api/scripts/set_admin.py "$(EMAIL)"

test-web:
	npm --prefix apps/web test

test-e2e:
	npm --prefix apps/web run test:e2e

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

migrate:
	COREBANK_DATABASE_URL=$(TEST_DATABASE_URL) PYTHONPATH=apps/api/src alembic -c apps/api/alembic.ini upgrade head

https-cert:
	./scripts/setup-local-https.sh

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-ps:
	docker compose ps

docker-logs-api:
	docker compose logs api
