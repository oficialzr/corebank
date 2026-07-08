# CoreBank

CoreBank is a training backend project that simulates a small banking system.

The current goal is to build a working MVP first: accounts, transfers, transactions, tests and clear local run instructions. Production-like infrastructure will be added later only when the MVP is stable.

## Current MVP Status

Current phase: **MVP Core completed. Next phase: MVP stabilization**

Already implemented:

- FastAPI application startup
- Health and version endpoints
- Account API
- Transfer API
- Transaction API
- PostgreSQL persistence
- PostgreSQL repositories
- Docker Compose setup
- Service layer
- Account created_at field in API responses
- Transaction ordering by creation time
- Concurrent-safe transfer balance updates
- Basic domain errors
- Pytest test suite
- MVP roadmap

Current test status:

```bash
49 PostgreSQL-backed tests
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Pytest
- Ruff
- Uvicorn

Planned later:

- Redis
- RabbitMQ or Kafka
- CI/CD
- Monitoring
- Kubernetes

## Project Structure

```text
corebank/
├── apps/
│   └── api/
│       ├── src/
│       │   └── corebank_api/
│       │       ├── api/
│       │       ├── core/
│       │       ├── domain/
│       │       ├── repositories/
│       │       ├── schemas/
│       │       ├── services/
│       │       └── main.py
│       ├── tests/
│       └── requirements.txt
├── docs/
├── MVP_ROADMAP.md
├── pyproject.toml
└── README.md
```

## MVP Scope

The MVP includes only the minimum features required to demonstrate the core banking flow.

Included in MVP:

- Create accounts
- List accounts
- Get account by id
- Transfer money between accounts
- Save transaction history
- List transactions
- Get transaction by id
- Filter transactions by account id
- Run tests locally
- Start API locally

Not included before MVP is stable:

- Authentication
- Authorization
- Redis
- Message brokers
- CI/CD
- Monitoring
- Kubernetes
- Advanced validation
- Complex architecture refactoring

The detailed roadmap is stored in [MVP_ROADMAP.md](MVP_ROADMAP.md).

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r apps/api/requirements.txt
```

## Run API

Start the FastAPI application:

```bash
uvicorn corebank_api.main:app --reload --app-dir apps/api/src
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Run with Docker Compose

Start API and PostgreSQL:

```bash
docker compose up --build
```
Database tables are created automatically when the API container starts.

Check that API is running:

```bash
curl http://127.0.0.1:8000/health
```

Check accounts endpoint:

```bash
curl http://127.0.0.1:8000/accounts
```

Stop containers:

```bash
docker compose down
```

## Run Tests

Run the full test suite:

```bash
pytest
```

Expected result:

```text
46 passed
```

## API Endpoints

### Service

```text
GET /health
GET /version
```

### Accounts

```text
GET /accounts
GET /accounts/{account_id}
POST /accounts
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/accounts \
  -H "Content-Type: application/json" \
  -d '{"owner_name":"Ivan Sidorov","currency":"RUB"}'
```

### Transfers

```text
POST /transfers
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/transfers \
  -H "Content-Type: application/json" \
  -d '{"from_account_id":"acc-001","to_account_id":"acc-002","amount":1000}'
```

### Transactions

```text
GET /transactions
GET /transactions/{transaction_id}
GET /transactions?account_id={account_id}
```

Examples:

```bash
curl http://127.0.0.1:8000/transactions
curl http://127.0.0.1:8000/transactions/{transaction_id}
curl "http://127.0.0.1:8000/transactions?account_id=acc-001"
```

## Current Business Rules

Transfers currently support these basic rules:

- Source account must exist
- Destination account must exist
- Source and destination accounts must be different
- Accounts must use the same currency
- Source account must have enough money
- Transfer amount must be greater than zero
- Successful transfer updates both balances
- Successful transfer creates a transaction record
- Transfer locks related account rows while updating balances
- Concurrent transfers cannot overspend the source account

## Development Discipline

CoreBank is developed through MVP phases.

Before starting a task, define:

- Current MVP phase
- Exact task
- What is out of scope
- Done criteria

Main rule:

> If a task does not move the project toward MVP, it goes to the Later Backlog.

## Next Steps

Near-term roadmap:

- Continue MVP stabilization
- Keep README and roadmap synchronized with implemented behavior
- Keep PostgreSQL-backed tests green
- Avoid adding production infrastructure before the MVP is stable

Long-term improvements:

- Authentication and authorization
- Persistent database migrations
- Message broker integration
- Background workers
- Observability
- CI/CD
- Kubernetes deployment

## License

This project is licensed under the MIT License.
