# CoreBank Development Guide

This document describes how to run the CoreBank project locally during
development.

Current stage:

```text
v0.2 - First API
```

At this stage the project contains:

- FastAPI application
- health check endpoint
- version endpoint
- pytest tests
- Makefile commands
- pyproject.toml configuration

---

# 1. Requirements

Required tools:

- Python 3.12+
- Git
- Make
- virtualenv / venv

Optional tools:

- curl
- tree
- VS Code

Docker is not required yet.

Docker will be added in a later release.

---

# 2. Project Structure

Current backend structure:

```text
corebank/
  apps/
    api/
      requirements.txt
      src/
        corebank_api/
          __init__.py
          main.py
      tests/
        test_health.py
  docs/
  pyproject.toml
  Makefile
  README.md
```

Meaning:

- `apps/api/` contains the first API service
- `apps/api/src/corebank_api/` contains application code
- `apps/api/tests/` contains API tests
- `pyproject.toml` contains tool configuration
- `Makefile` contains useful development commands

---

# 3. Create Virtual Environment

From the project root:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, terminal should show something like:

```text
(.venv)
```

This means Python packages will be installed inside the project virtual
environment instead of the global system Python.

---

# 4. Install Dependencies

From the project root:

```bash
pip install -r apps/api/requirements.txt
```

Current dependencies:

- fastapi
- uvicorn[standard]
- pytest
- httpx

Why these dependencies are needed:

- FastAPI is used to build the HTTP API
- Uvicorn is used to run the FastAPI application
- Pytest is used to run tests
- HTTPX is used internally by FastAPI TestClient for API tests

---

# 5. Run API

Recommended command:

```bash
make run-api
```

This command runs:

```bash
uvicorn corebank_api.main:app --reload --app-dir apps/api/src
```

Meaning:

- `uvicorn` starts the ASGI server
- `corebank_api.main:app` points to the FastAPI app object
- `--reload` restarts the server when code changes
- `--app-dir apps/api/src` tells Python where the source code is located

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 6. Check API Manually

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Version endpoint:

```bash
curl http://127.0.0.1:8000/version
```

Expected response:

```json
{"service":"corebank-api","version":"0.1.0","environment":"local"}
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 7. Run Tests

Recommended command:

```bash
make test
```

This command runs:

```bash
pytest
```

Expected result:

```text
2 passed
```

The test configuration is stored in:

```text
pyproject.toml
```

Current pytest configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["apps/api/tests"]
pythonpath = ["apps/api/src"]
```

Meaning:

- pytest searches tests in `apps/api/tests`
- pytest can import application code from `apps/api/src`
- tests can be started with simple `pytest`

---

# 8. Useful Commands

Run API:

```bash
make run-api
```

Run tests:

```bash
make test
```

Show Git status:

```bash
git status
```

Show project tree:

```bash
tree
```

Install dependencies:

```bash
pip install -r apps/api/requirements.txt
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Deactivate virtual environment:

```bash
deactivate
```

---

# 9. Current API Endpoints

Current endpoints:

```text
GET /health
GET /version
```

## GET /health

Purpose:

- check that API is alive

Response:

```json
{"status":"ok"}
```

## GET /version

Purpose:

- return basic service information

Response:

```json
{
  "service": "corebank-api",
  "version": "0.1.0",
  "environment": "local"
}
```

---

# 10. Current Testing Strategy

Current tests check:

- `/health` returns HTTP 200
- `/health` returns expected JSON
- `/version` returns HTTP 200
- `/version` returns expected JSON

Why this matters:

- endpoints are protected from accidental changes
- future refactoring becomes safer
- CI/CD can run these tests later
- project has a professional development workflow from the beginning

---

# 11. What Is Not Added Yet

Not added yet:

- PostgreSQL
- Redis
- RabbitMQ
- Docker
- Kubernetes
- authentication
- business entities
- real money transfer logic
- migrations
- monitoring

These parts will be added in later releases.

Current goal is to keep the first API simple and working.

---

# 12. Next Development Steps

Next planned steps:

- improve application structure
- add configuration module
- add project metadata
- add linting with Ruff
- add type checking with Mypy later
- prepare for first user/account endpoints
- prepare for PostgreSQL in release v0.3
