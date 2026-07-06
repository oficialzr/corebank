# CoreBank MVP Roadmap

CoreBank is a training backend project that simulates a minimal banking system.

The main goal is to build a working MVP first, without premature overengineering.

## Main Rule

We only work on tasks that move the project toward MVP.

Anything not required for MVP goes to the Later Backlog.

## Current Phase

MVP Core completed. Next phase: MVP stabilization.

## MVP Definition

The MVP is ready when CoreBank can:

- Start as a FastAPI application.
- Pass tests.
- Create accounts.
- Return account information.
- Transfer money between accounts.
- Store transaction history.
- Return transactions.
- Have basic README documentation.
- Run locally with clear instructions.

## Not Required Before MVP

These topics are intentionally postponed:

- Authentication and authorization.
- Docker.
- Redis.
- Kafka.
- RabbitMQ.
- Kubernetes.
- CI/CD.
- Monitoring.
- Advanced validation.
- Complex error handling.
- Idempotency keys.
- Rate limiting.
- Production-grade logging.
- Complex architecture refactoring.

## MVP-0: Stabilize Project

Goal: Make the current codebase stable and runnable.

Tasks:

- Fix current failing tests.
- Make sure pytest passes.
- Make sure FastAPI starts locally.
- Make sure /health works.
- Push stable code to GitHub.

Done criteria:

- pytest passes.
- API starts locally.
- /health returns successful response.
- Changes are committed and pushed.

## MVP-1: Accounts

Goal: Implement basic account operations.

Required endpoints:

- POST /accounts
- GET /accounts/{account_id}
- GET /accounts

Account fields:

- id
- owner_name
- balance
- currency
- created_at

Done criteria:

- Account can be created.
- Account can be fetched by id.
- Accounts can be listed.
- Basic API tests exist.

## MVP-2: Transfers

Goal: Implement money transfers between accounts.

Required endpoint:

- POST /transfers

Transfer rules:

- Sender account must exist.
- Receiver account must exist.
- Sender must have enough money.
- Sender balance decreases.
- Receiver balance increases.
- Transaction is created.

Transaction fields:

- id
- from_account_id
- to_account_id
- amount
- currency
- status
- created_at

Done criteria:

- Successful transfer works.
- Failed transfer with insufficient funds works.
- Balances are updated correctly.
- Transaction is saved.
- Basic tests exist.

## MVP-3: Transactions

Goal: Implement transaction history.

Required endpoints:

- GET /transactions
- GET /transactions/{transaction_id}
- GET /accounts/{account_id}/transactions

Done criteria:

- All transactions can be listed.
- Transaction can be fetched by id.
- Account transactions can be listed.
- Basic tests exist.

## MVP-4: README MVP

Goal: Make the project understandable from GitHub.

README must include:

- Project description.
- Tech stack.
- Local run instructions.
- Test instructions.
- API endpoints.
- MVP roadmap link.
- Future improvements.

Done criteria:

- README explains how to run the project.
- README explains how to test the project.
- README links to MVP_ROADMAP.md.

## MVP-5: PostgreSQL Persistence

Goal: Replace in-memory storage with PostgreSQL.

Required:

- PostgreSQL integration.
- Database models.
- Repositories using database.
- Migrations.

Done criteria:

- Accounts are stored in PostgreSQL.
- Transactions are stored in PostgreSQL.
- API works after restart.
- Tests are updated.

Status: Done.

Implemented:
- Accounts are stored in PostgreSQL.
- Transactions are stored in PostgreSQL.
- Runtime uses PostgreSQL-only repositories.
- In-memory repository backend was removed.
- Tests use PostgreSQL-backed isolation.

## MVP-6: Docker Compose

Goal: Run CoreBank locally using Docker Compose.

Required:

- Dockerfile.
- docker-compose.yml.
- API service.
- PostgreSQL service.

Done criteria:

- docker compose up starts the project.
- API works from browser/curl.
- Database works.
- README has Docker instructions.

Status: Done.

Implemented:
- Dockerfile for API service.
- Docker Compose with API and PostgreSQL services.
- PostgreSQL healthcheck.
- API waits for PostgreSQL readiness.
- Database tables are created automatically on API container startup.
- API is available on localhost:8000.
- README includes Docker Compose run instructions.

## Later Backlog

These tasks are useful, but not part of MVP:

- Authentication.
- JWT.
- User model.
- Admin role.
- Redis cache.
- Message broker.
- Kafka/RabbitMQ events.
- CI/CD.
- Linters.
- Formatters.
- Pre-commit hooks.
- Observability.
- Prometheus.
- Grafana.
- Kubernetes.
- Load testing.
- Idempotency.
- Better error model.
- Advanced validation.
- OpenAPI polishing.

## Development Discipline

Before starting any task, define:

- Current MVP phase.
- Exact task.
- What we will not touch.
- Done criteria.

No extra refactoring unless it blocks the current MVP task.
