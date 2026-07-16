# CoreBank MVP Roadmap

CoreBank is a training backend project that simulates a minimal banking system.

The main goal is to build a correct, runnable MVP first. Extra infrastructure
and production features are added only when they solve a real project need.

## Main Rule

Work on tasks that move the project toward a stable MVP.

Anything not required for the current MVP phase goes to the Later Backlog.

## Current Phase

**Core banking MVP is implemented. Stabilization and auth foundation are in
progress.**

The project already has the core banking flow:

- accounts
- transfers
- transaction history
- PostgreSQL persistence
- Alembic migrations
- Docker Compose
- CI
- PostgreSQL-backed tests

The project has also started the authentication foundation:

- user table
- registration endpoint
- login endpoint
- bearer access token
- current user endpoint
- email normalization
- password hashing
- duplicate email handling

Fine-grained authorization, account ownership, and protected banking endpoints
are not implemented yet.

## Current Test Status

Current test inventory:

```text
67 tests collected
```

Tests are PostgreSQL-backed. A local test run needs PostgreSQL to be available,
then migrations should be applied before running the suite.

Recommended commands:

```bash
docker compose up -d postgres
make migrate
make test
```

In the current environment, collection succeeded but tests were skipped because
PostgreSQL was not available.

## MVP Definition

The core banking MVP is ready when CoreBank can:

- Start as a FastAPI application.
- Pass the PostgreSQL-backed test suite.
- Create accounts.
- Return account information.
- Transfer money between accounts.
- Store transaction history.
- Return transactions.
- Persist users, accounts, and transactions in PostgreSQL.
- Authenticate users with bearer access tokens.
- Run migrations with Alembic.
- Run locally with clear instructions.
- Run with Docker Compose.
- Document implemented endpoints and development commands.

Status: **Core banking MVP done. Stabilization continues.**

## Not Required For The Core Banking MVP

These topics are intentionally postponed or only partially started:

- Login endpoint.
- Fine-grained authorization.
- Protected banking endpoints.
- Account ownership by user.
- Cards.
- Audit events.
- Idempotency keys.
- Redis.
- Kafka/RabbitMQ.
- Background workers.
- Monitoring.
- Kubernetes.
- Rate limiting.
- Production-grade logging.
- Complex architecture refactoring.

## MVP-0: Stabilize Project

Goal: Make the codebase stable and runnable.

Status: Done.

Implemented:

- FastAPI application starts.
- `/health` returns a successful response.
- `/version` returns service information.
- Pytest configuration is stored in `pyproject.toml`.
- Makefile contains common development commands.
- CI workflow exists.

Done criteria:

- API starts locally.
- `/health` works.
- Tests can be run with documented commands.

## MVP-1: Accounts

Goal: Implement basic account operations.

Status: Done.

Required endpoints:

- `POST /accounts`
- `GET /accounts/{account_id}`
- `GET /accounts`

Implemented fields:

- `id`
- `owner_name`
- `balance`
- `currency`
- `created_at`

Implemented behavior:

- Account IDs are UUID-based and use the `acc-` prefix.
- New accounts start with zero balance.
- Owner name is stripped and must not be blank.
- Currency is validated as `RUB`, `USD`, or `EUR`.
- API tests and service tests cover account behavior.

## MVP-2: Transfers

Goal: Implement money transfers between accounts.

Status: Done.

Required endpoint:

- `POST /transfers`

Implemented rules:

- Sender account must exist.
- Receiver account must exist.
- Sender and receiver must be different accounts.
- Accounts must use the same currency.
- Sender must have enough money.
- Transfer amount must be greater than zero.
- Sender balance decreases.
- Receiver balance increases.
- Transaction is created.
- Balance updates and transaction creation happen in one database transaction.
- Related account rows are locked during transfer updates.
- Concurrent overspending is covered by a service test.

Implemented response:

- `transaction_id`
- `from_account_id`
- `to_account_id`
- `amount`
- `status`

## MVP-3: Transactions

Goal: Implement transaction history.

Status: Done.

Required endpoints:

- `GET /transactions`
- `GET /transactions/{transaction_id}`
- `GET /transactions?account_id={account_id}`

Implemented behavior:

- Transaction IDs are UUID-based and use the `tx-` prefix.
- All transactions can be listed.
- Transaction can be fetched by id.
- Account transactions can be listed.
- Transaction lists are ordered by `created_at` descending.
- Blank account filter is rejected with a stable error code.
- API tests and service tests cover transaction behavior.

## MVP-4: README MVP

Goal: Make the project understandable from GitHub.

Status: Done, maintained continuously.

README includes:

- Project description.
- Current implementation status.
- Tech stack.
- Local setup instructions.
- Docker Compose instructions.
- Migration instructions.
- Test instructions.
- API endpoints.
- Current business rules.
- MVP roadmap link.
- Future improvements.

## MVP-5: PostgreSQL Persistence

Goal: Replace in-memory storage with PostgreSQL.

Status: Done.

Implemented:

- SQLAlchemy database models.
- PostgreSQL repositories.
- PostgreSQL-only runtime repository backend.
- Alembic migration for accounts and transactions.
- PostgreSQL-backed tests.
- Docker Compose PostgreSQL service.
- CI PostgreSQL service.

Current persisted tables:

- `accounts`
- `transactions`
- `users`

## MVP-6: Docker Compose

Goal: Run CoreBank locally using Docker Compose.

Status: Done.

Implemented:

- API Dockerfile.
- `docker-compose.yml`.
- PostgreSQL service with healthcheck.
- API service depends on healthy PostgreSQL.
- Alembic migrations run before API startup in the API container.
- API is available on `localhost:8000`.

## MVP-7: Error Responses

Goal: Make custom business errors predictable for API clients.

Status: Done for implemented business errors.

Implemented:

- Shared `api_error()` helper.
- Error response schema.
- Stable machine-readable error codes.
- Account not found error.
- Transaction not found error.
- Transfer failure codes:
  - `source_account_not_found`
  - `destination_account_not_found`
  - `same_account_transfer`
  - `currency_mismatch`
  - `insufficient_funds`
- User registration duplicate email code:
  - `email_already_registered`
- API tests validate complete error responses for implemented cases.

## MVP-8: User Registration Foundation

Goal: Add the first user/authentication building block without protecting the
banking API yet.

Status: Partially done.

Implemented:

- `users` table.
- `UserModel`.
- User schemas.
- SQL users repository.
- User service.
- `POST /auth/register`.
- `POST /auth/login`.
- `GET /auth/me`.
- Email normalization to lowercase.
- Password hashing.
- JWT access token creation.
- JWT access token validation.
- Duplicate email rejection.
- Invalid credential rejection.
- Invalid token rejection.
- API, service, and repository tests.

Not implemented yet:

- User-to-account ownership.
- Authorization checks on account, transfer, and transaction endpoints.

Done criteria for this phase:

- Registration is stable and documented.
- Login endpoint is stable and documented.
- Password verification is used during login.
- JWT token issuance and token validation are covered by tests.
- README documents the auth flow clearly.
- Banking endpoints are still intentionally unprotected until ownership and
  authorization are designed.

## MVP Stabilization Backlog

Near-term stabilization tasks:

- Keep migrations and models synchronized.
- Keep README and `MVP_ROADMAP.md` synchronized with actual code.
- Decide whether local development should standardize on PostgreSQL port
  `5432` or Docker Compose port `5433`.
- Decide account ownership model.
- Protect write operations after authorization exists.
- Add tests for any new auth behavior before expanding infrastructure.

## Later Backlog

These tasks are useful, but not part of the current MVP phase:

- Cards.
- Audit events.
- Idempotency keys for transfers.
- Redis cache.
- Kafka/RabbitMQ events.
- Background workers.
- Pre-commit hooks.
- Observability.
- Prometheus.
- Grafana.
- Kubernetes.
- Load testing.
- Advanced validation.
- Production-grade logging.

## Development Discipline

Before starting any task, define:

- Current MVP phase.
- Exact task.
- What is out of scope.
- Done criteria.

No extra refactoring unless it blocks the current MVP task.
