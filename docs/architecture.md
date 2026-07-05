# CoreBank Architecture

This document describes the planned architecture of the CoreBank project.

CoreBank is built step by step. The architecture starts simple and becomes
more complex only when the project has a real reason for it.

The main goal is to understand why each component exists, what problem it
solves, and how it communicates with other parts of the system.

---

# 1. Architecture Goals

CoreBank architecture should be:

- simple at the beginning
- easy to understand
- easy to run locally
- easy to extend step by step
- close to real backend systems
- focused on correctness of money operations
- observable in later releases
- deployable to Docker and Kubernetes

The project does not start with microservices.

At the beginning, a modular monolith is a better choice because:

- the domain is still being designed
- business rules are not stable yet
- there is no real load yet
- there is no need for distributed complexity yet
- it is easier to refactor one application than many services
- it is easier to understand the system while learning

The architecture can evolve later if there is a real reason.

---

# 2. High-Level System Idea

CoreBank is a simplified banking backend platform.

The system will support:

- users
- accounts
- cards
- balances
- transfers
- transactions
- audit events
- notifications
- analytics

The most important responsibility of the system is safe money movement.

A transfer must not:

- lose money
- create money from nowhere
- update only one side of the operation
- be executed twice by accident
- change balances without transaction history
- change critical data without audit trail

Because of this, the architecture is designed around consistency,
transaction safety and observability.

---

# 3. Initial Architecture

The first working version will be simple:

```text
Client
  |
  v
CoreBank API
```

At this stage, there is no database yet.

The goal of this stage is to create the first backend application and prove
that it can:

- start successfully
- receive HTTP requests
- return HTTP responses
- expose health check endpoint
- have a clean project structure
- be tested locally

This version belongs to release:

```text
v0.2 - First API
```

---

# 4. Architecture with PostgreSQL

The next important step is persistent data storage.

```text
Client
  |
  v
CoreBank API
  |
  v
PostgreSQL
```

PostgreSQL becomes the source of truth.

It stores:

- users
- accounts
- cards
- transfers
- transactions
- audit events

PostgreSQL is used because the system needs:

- reliable data storage
- relational data model
- transactions
- constraints
- consistency
- history of operations
- safe money movement

Money-related operations must be handled carefully.

For example, a transfer between two accounts should be done inside one
database transaction:

```text
Start database transaction
  |
  |-- check source account
  |-- check destination account
  |-- check source balance
  |-- decrease source balance
  |-- increase destination balance
  |-- create transaction records
  |-- create audit event
  |
Commit database transaction
```

If any step fails, the whole operation must be rolled back.

This prevents situations where money was withdrawn from one account but was
not deposited to another account.

This version belongs to release:

```text
v0.3 - PostgreSQL
```

---

# 5. Architecture with Docker

After the API and PostgreSQL exist, the project should be runnable in a
predictable environment.

```text
Docker Compose
  |
  |---- CoreBank API container
  |---- PostgreSQL container
```

Docker solves the problem of local environment differences.

Without Docker, every developer must install and configure dependencies
manually. With Docker, the project can be started with a small set of
commands.

Docker will be used for:

- running API
- running PostgreSQL
- isolating dependencies
- simplifying local setup
- preparing the project for Kubernetes later

This version belongs to release:

```text
v0.4 - Docker
```

---

# 6. Architecture with Redis

Redis is added only when the project has a real caching problem.

```text
Client
  |
  v
CoreBank API
  |
  |---- PostgreSQL
  |---- Redis
```

Redis is not the source of truth.

PostgreSQL remains the source of truth because it stores critical business
data permanently.

Redis can be used for:

- short-lived cache
- frequently requested non-critical data
- temporary operation status
- rate limiting in later versions
- session-like temporary data if needed

Important rule:

```text
Critical money correctness must not depend only on Redis.
```

For example, account balance should not be stored only in Redis. Redis may
cache a balance representation, but the real balance must be stored and
validated in PostgreSQL.

Redis solves performance problems, not data correctness problems.

This version belongs to release:

```text
v0.5 - Redis
```

---

# 7. Architecture with RabbitMQ and Workers

RabbitMQ is added when the system needs asynchronous processing.

```text
Client
  |
  v
CoreBank API
  |
  |---- PostgreSQL
  |---- Redis
  |---- RabbitMQ
            |
            |---- Notification Worker
            |---- Audit Worker
            |---- Analytics Worker
```

Not every task should be done inside the HTTP request.

Some tasks can be moved to background workers:

- sending notifications
- processing analytics events
- exporting reports
- processing non-critical audit pipelines
- simulating external integrations

RabbitMQ helps decouple the API from background work.

The API can publish a message, and a worker can process it later.

Example flow:

```text
User makes transfer
  |
  v
CoreBank API
  |
  |-- performs critical money operation in PostgreSQL
  |-- publishes notification event to RabbitMQ
  |-- publishes analytics event to RabbitMQ
  |
  v
User receives API response

Later:

RabbitMQ
  |
  |---- Notification Worker sends notification
  |---- Analytics Worker processes analytics event
```

Important rule:

```text
Critical balance consistency must not depend on RabbitMQ.
```

RabbitMQ can be used for side effects and background processing, but the
main money operation must be safely completed in PostgreSQL.

This version belongs to release:

```text
v0.6 - RabbitMQ and Workers
```

---

# 8. Planned Components

## 8.1 CoreBank API

CoreBank API is the main backend application.

Responsibilities:

- receive HTTP requests
- validate input data
- execute business logic
- work with PostgreSQL
- use Redis when caching is needed
- publish messages to RabbitMQ
- return API responses
- expose health and metrics endpoints

At the beginning, this is the only application service.

## 8.2 PostgreSQL

PostgreSQL is the main database.

Responsibilities:

- store users
- store accounts
- store cards
- store transfers
- store transaction history
- store audit events
- enforce important constraints
- provide transactional safety

PostgreSQL is the source of truth.

## 8.3 Redis

Redis is an in-memory storage used for cache and temporary data.

Responsibilities:

- cache non-critical frequently requested data
- store short-lived data
- reduce load on PostgreSQL in selected cases
- support future rate limiting or temporary operation state

Redis is not the source of truth.

## 8.4 RabbitMQ

RabbitMQ is the message broker.

Responsibilities:

- receive messages from API
- store messages until workers consume them
- decouple API from background processing
- support asynchronous workflows

RabbitMQ should not be required for the correctness of the main money
transaction.

## 8.5 Notification Worker

Notification Worker processes notification events.

Responsibilities:

- consume notification messages
- prepare notification text
- simulate sending notifications
- record notification processing status if needed

## 8.6 Audit Worker

Audit Worker processes audit-related events.

Responsibilities:

- consume audit events
- enrich audit data if needed
- store or forward audit records
- help investigate important actions

At the early stage, critical audit records can also be written directly to
PostgreSQL inside the main transaction. Later, additional audit processing
can be asynchronous.

## 8.7 Analytics Worker

Analytics Worker processes events for reporting and analysis.

Responsibilities:

- consume analytics events
- aggregate operation data
- prepare data for reports
- help observe business behavior

## 8.8 Traffic Generator

Traffic Generator is a separate service that simulates users and requests.

Responsibilities:

- generate users
- generate accounts
- generate transfers
- create artificial API load
- help test monitoring and performance

---

# 9. Why Not Microservices at the Start

CoreBank does not start as microservices.

Reasons:

- microservices add network complexity
- microservices require distributed tracing earlier
- data consistency becomes harder
- deployment becomes harder
- debugging becomes harder
- many services are unnecessary before the domain is stable
- the project is still in learning and design phase

A modular monolith gives better control at the beginning.

The code can still be organized into clear modules:

- users
- accounts
- cards
- transfers
- transactions
- audit
- notifications
- analytics

If the project later has a real reason to split services, it can be done
based on actual boundaries instead of guessing too early.

---

# 10. Data Ownership

At the beginning, one API owns the main database schema.

```text
CoreBank API
  |
  v
PostgreSQL
```

This is intentional.

Splitting data ownership too early can create unnecessary complexity.

Future workers may have their own tables if needed, but the first version
keeps data ownership simple.

Important principle:

```text
One clear source of truth is better than many unclear sources of truth.
```

---

# 11. Communication Between Components

## 11.1 Synchronous Communication

Synchronous communication means that the caller waits for the response.

Examples:

- client calls CoreBank API
- API calls PostgreSQL
- API calls Redis

Used for:

- operations that must return immediate result
- validation
- reading data
- writing critical data

## 11.2 Asynchronous Communication

Asynchronous communication means that work can happen later.

Examples:

- API publishes event to RabbitMQ
- Worker consumes event from RabbitMQ
- Worker processes notification or analytics

Used for:

- notifications
- analytics
- non-critical background processing
- operations that should not slow down the API response

Important rule:

```text
Do not move critical money consistency into asynchronous processing too early.
```

---

# 12. Request Flow Examples

## 12.1 Health Check

```text
Client
  |
  v
GET /health
  |
  v
CoreBank API
  |
  v
Response: service is alive
```

## 12.2 Create User

```text
Client
  |
  v
POST /users
  |
  v
CoreBank API
  |
  v
PostgreSQL
  |
  v
Response: user created
```

## 12.3 Transfer Money

```text
Client
  |
  v
POST /transfers
  |
  v
CoreBank API
  |
  v
PostgreSQL transaction
  |
  |-- validate accounts
  |-- validate balance
  |-- update balances
  |-- create transfer record
  |-- create transaction records
  |-- create audit event
  |
  v
Commit
  |
  v
Publish events to RabbitMQ
  |
  v
Response: transfer completed
```

---

# 13. Important Architecture Rules

CoreBank architecture follows these rules:

- PostgreSQL is the source of truth.
- Redis is used for cache, not for critical money correctness.
- RabbitMQ is used for asynchronous side effects and background work.
- Critical money operations must be transaction-safe.
- A failed transfer must not partially update balances.
- Every balance change must have a transaction record.
- Important actions must be auditable.
- Technologies are added only when they solve a real problem.
- The project starts as a modular monolith.
- Microservices are not introduced without a real need.

---

# 14. Architecture Evolution

The planned architecture evolution:

```text
Step 1:
Client -> CoreBank API

Step 2:
Client -> CoreBank API -> PostgreSQL

Step 3:
Docker Compose:
  - CoreBank API
  - PostgreSQL

Step 4:
Client -> CoreBank API
               |---- PostgreSQL
               |---- Redis

Step 5:
Client -> CoreBank API
               |---- PostgreSQL
               |---- Redis
               |---- RabbitMQ
                         |---- Workers

Step 6:
Traffic Generator -> CoreBank API

Step 7:
Monitoring:
  - Prometheus
  - Grafana
  - Loki
  - Jaeger

Step 8:
Kubernetes:
  - API Deployment
  - Worker Deployments
  - Services
  - ConfigMaps
  - Secrets
  - Probes
```

---

# 15. Current Architecture Status

Current release:

```text
v0.1 - Architecture and Documentation
```

Current architecture status:

- README is created
- roadmap is created
- architecture is being defined
- domain model is not finalized yet
- database model is not finalized yet
- API endpoints are not finalized yet
- implementation has not started yet

Next documentation steps:

- define database model in docs/database.md
- define first API endpoints in docs/api.md
- record engineering decisions in docs/decisions.md
- create first ADR in docs/adr/
