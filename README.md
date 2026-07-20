# CoreBank

CoreBank is a training backend project that simulates a small banking system.

The project is currently focused on a working MVP: accounts, transfers,
transactions, PostgreSQL persistence, local Docker setup, automated migrations,
tests, and a basic JWT authentication layer.

## Current Status

Current phase: **Authenticated core banking MVP and the first user dashboard
are implemented.**

Implemented:

- FastAPI application with `/health` and `/version`
- Account API
- Transfer API
- Transaction API
- User registration API
- User login API
- Bearer token authentication with JWT
- User-owned accounts and authorization on banking endpoints
- User-scoped transaction history and protected outgoing transfers
- Current user endpoint
- Password hashing with `pwdlib[argon2]`
- PostgreSQL persistence through SQLAlchemy repositories
- Alembic migrations for users, accounts, and transactions
- Docker Compose setup for API and PostgreSQL
- Makefile commands for common development tasks
- CI workflow with PostgreSQL service, lint, migrations, and tests
- Standardized business error responses with stable error codes
- OpenAPI error response schemas for custom API errors
- React and TypeScript landing page with registration and login
- Persistent frontend session restored through the current-user endpoint
- Dockerized web frontend with an API reverse proxy
- Protected dashboard with balances, accounts, and recent transactions
- Account opening from the dashboard
- PostgreSQL-backed test suite

Not implemented yet:

- Cards
- Audit events
- Idempotency keys
- Redis
- Message broker and workers
- Monitoring
- Kubernetes

Current test inventory:

```text
72 tests collected
```

The tests require a reachable PostgreSQL database. The complete suite has been
verified against PostgreSQL 16.

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- HTTPX
- Ruff
- Uvicorn
- Docker Compose
- React
- TypeScript
- Vite
- Nginx

## Project Structure

```text
corebank/
├── apps/
│   ├── api/
│       ├── migrations/
│       ├── src/
│       │   └── corebank_api/
│       │       ├── api/
│       │       ├── core/
│       │       ├── database/
│       │       ├── domain/
│       │       ├── repositories/
│       │       ├── schemas/
│       │       ├── services/
│       │       └── main.py
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
│   └── web/
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── docs/
├── docker-compose.yml
├── Makefile
├── MVP_ROADMAP.md
├── pyproject.toml
└── README.md
```

## MVP Scope

The core banking MVP includes:

- Create accounts
- List accounts
- Get account by id
- Transfer money between accounts
- Save transaction history
- List transactions
- Get transaction by id
- Filter transactions by account id
- Store users for registration
- Hash user passwords before saving
- Issue JWT access tokens
- Read the current user from a bearer token
- Isolate accounts and transactions by the current user
- Allow transfers only from accounts owned by the current user
- Display real account data in the protected web dashboard
- Run migrations
- Run tests locally and in CI
- Start the API locally or with Docker Compose

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

## Run with Docker Compose

Start API and PostgreSQL:

```bash
docker compose up --build
```

The API container applies Alembic migrations before starting Uvicorn.

The API will be available at:

```text
http://127.0.0.1:8000
```

The web application will be available at:

```text
http://127.0.0.1:3000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Stop containers:

```bash
docker compose down
```

## Run API Locally

When running the API outside Docker, make sure PostgreSQL is available and the
database schema is migrated.

The default local database URL is:

```text
postgresql+psycopg://corebank:corebank@localhost:5432/corebank
```

The Makefile test database URL points to Docker Compose PostgreSQL on port
`5433`:

```text
postgresql+psycopg://corebank:corebank@localhost:5433/corebank
```

If you want to run the API locally against the Docker Compose PostgreSQL
container, export the same database URL:

```bash
export COREBANK_DATABASE_URL=postgresql+psycopg://corebank:corebank@localhost:5433/corebank
```

Apply migrations:

```bash
make migrate
```

Start the FastAPI application:

```bash
make run-api
```

Equivalent direct command:

```bash
uvicorn corebank_api.main:app --reload --app-dir apps/api/src
```

## Run Web Locally

The frontend requires Node.js 22+. Install its dependencies and start Vite:

```bash
cd apps/web
npm install
npm run dev
```

The development site is available at `http://127.0.0.1:5173` and proxies
requests from `/api` to the FastAPI application at `http://127.0.0.1:8000`.
The frontend implementation plan is documented in
[docs/frontend.md](docs/frontend.md).

## Run Tests

Start PostgreSQL first, then run migrations and tests:

```bash
docker compose up -d postgres
make migrate
make test
```

Run lint and tests together:

```bash
make check
```

## API Endpoints

### System

```text
GET /health
GET /version
```

### Authentication

```text
POST /auth/register
POST /auth/login
GET /auth/me
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@example.com","password":"strong-password","full_name":"Alex Ivanov"}'
```

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@example.com","password":"strong-password"}'
```

### Accounts

```text
GET /accounts
GET /accounts/{account_id}
POST /accounts
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/accounts \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"currency":"RUB"}'
```

### Transfers

```text
POST /transfers
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/transfers \
  -H "Authorization: Bearer <access_token>" \
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
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/transactions
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/transactions/{transaction_id}
curl -H "Authorization: Bearer <access_token>" "http://127.0.0.1:8000/transactions?account_id=acc-001"
```

## Current Business Rules

Accounts:

- Every newly created account belongs to the authenticated user.
- Owner name is taken from the authenticated user profile.
- Users can list and read only their own accounts.
- Legacy accounts without an assigned user are hidden from user-scoped APIs.
- Account currency must be one of `RUB`, `USD`, or `EUR`.
- New accounts start with zero balance.
- Account IDs are UUID-based values with the `acc-` prefix.

Transfers:

- Source account must exist and belong to the authenticated user.
- Destination account must exist.
- Source and destination accounts must be different.
- Accounts must use the same currency.
- Source account must have enough money.
- Transfer amount must be greater than zero.
- Successful transfer updates both balances.
- Successful transfer creates a transaction record.
- Related account rows are locked during balance updates.
- Concurrent transfers cannot overspend the source account.

Transactions:

- Transaction IDs are UUID-based values with the `tx-` prefix.
- Transaction lists are ordered by `created_at` descending.
- Users see transactions involving at least one of their accounts.
- Transactions can be filtered only by an account owned by the current user.

Users:

- Registration normalizes email to lowercase.
- Passwords are stored as hashes, not as plain text.
- Login returns a bearer access token.
- `/auth/me` requires a valid bearer token.
- Duplicate email registration returns a stable `email_already_registered`
  error code.
- Invalid login returns a stable `invalid_credentials` error code.
- Invalid or expired token returns a stable `invalid_token` error code.

## Next Steps

Near-term:

- Keep the PostgreSQL-backed test suite green.
- Build the guided transfer flow in the dashboard.
- Generate frontend API types from the OpenAPI schema.
- Move authentication from local storage to secure HttpOnly cookies.
- Keep README and roadmap synchronized with implemented behavior.

Later:

- Cards
- Audit events
- Idempotency for transfers
- Redis
- Message broker and workers
- Observability
- Kubernetes deployment

## License

This project is licensed under the MIT License.
