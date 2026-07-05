.PHONY: run-api test

run-api:
	uvicorn corebank_api.main:app --reload --app-dir apps/api/src

run-api-test-env:
	COREBANK_ENVIRONMENT=test uvicorn corebank_api.main:app --reload --app-dir apps/api/src

test:
	pytest
