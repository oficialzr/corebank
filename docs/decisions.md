# CoreBank Engineering Decisions

This document contains important engineering decisions made during the
CoreBank project design.

Detailed architecture decisions can be stored separately in:

```text
docs/adr/
```

This file is a short summary of the most important decisions.

---

# 1. Start with Documentation Before Code

## Decision

CoreBank starts with documentation before business code.

Initial documentation includes:

- README.md
- docs/roadmap.md
- docs/architecture.md
- docs/database.md
- docs/api.md
- docs/decisions.md
- docs/adr/

## Reason

The project is not a small random CRUD application. It is a production-like
backend learning project.

Before writing code, we need to understand:

- what system we are building
- what the main domain entities are
- which operations are critical
- how money should move
- which technologies will be added later
- why each technology is needed

## Consequences

Positive:

- project direction is clear
- architecture is easier to explain
- future code will have a stronger foundation
- the repository looks more professional

Negative:

- implementation starts later
- documentation may need updates after real coding starts

## Current Status

Accepted.

---

# 2. Use One Repository

## Decision

CoreBank uses one repository.

All project parts will be stored in the same repository:

- API
- workers
- documentation
- Docker files
- Kubernetes manifests
- monitoring configuration
- tests

## Reason

At the current stage, one repository is simpler and more useful.

The project is still small. Splitting it into many repositories would add
unnecessary complexity.

One repository makes it easier to:

- understand the whole system
- refactor code
- update documentation
- run the project locally
- show the project as portfolio work

## Consequences

Positive:

- easier local development
- easier learning process
- easier project navigation
- easier documentation

Negative:

- repository may become larger over time
- clear folder structure will be important

## Current Status

Accepted.

---

# 3. Start with Modular Monolith, Not Microservices

## Decision

CoreBank starts as a modular monolith.

The first backend application will contain separate logical modules, but it
will be deployed as one API service.

Possible modules:

- users
- accounts
- cards
- transfers
- transactions
- audit
- notifications
- analytics

## Reason

Microservices are not needed at the beginning.

Starting with microservices too early would add complexity:

- service-to-service communication
- distributed transactions
- deployment complexity
- debugging complexity
- tracing complexity
- data ownership problems
- network failures

The domain is not stable yet. It is better to first understand the business
model inside one application.

## Consequences

Positive:

- easier development
- easier debugging
- easier transaction handling
- easier refactoring
- better for learning fundamentals

Negative:

- boundaries must be kept clean manually
- future service splitting may require refactoring

## Current Status

Accepted.

---

# 4. PostgreSQL Is the Source of Truth

## Decision

PostgreSQL is the main database and the source of truth.

Critical data will be stored in PostgreSQL:

- users
- accounts
- cards
- balances
- transfers
- transactions
- audit events

## Reason

CoreBank works with money-like operations.

The system needs:

- reliable data storage
- transactions
- constraints
- relational model
- consistency
- durable operation history

PostgreSQL is a good fit for this because it provides strong relational
database features and transaction support.

## Consequences

Positive:

- data consistency is easier to protect
- transfers can be executed inside database transactions
- constraints can protect invalid data
- transaction history can be stored reliably

Negative:

- database schema design becomes important
- migrations must be managed carefully
- incorrect transaction logic can still break business rules

## Current Status

Accepted.

---

# 5. Redis Is Cache, Not Source of Truth

## Decision

Redis may be added later, but only as cache or temporary storage.

Redis must not become the source of truth for critical banking data.

## Reason

Redis is fast, but CoreBank's critical data must be durable and consistent.

Account balance, transfers and transaction history must be stored in
PostgreSQL.

Redis can be useful for:

- caching frequently requested non-critical data
- temporary operation status
- rate limiting
- short-lived values

Redis should not decide whether money exists.

## Consequences

Positive:

- performance can be improved later
- critical correctness stays in PostgreSQL
- cache can be rebuilt if lost

Negative:

- cache invalidation rules must be documented
- stale cache must not break business logic

## Current Status

Accepted.

---

# 6. RabbitMQ Is for Asynchronous Side Effects

## Decision

RabbitMQ may be added later for asynchronous processing.

It should be used for background work such as:

- notifications
- analytics events
- non-critical audit processing
- integration-like workflows

RabbitMQ must not be required for the core money transfer to be correct.

## Reason

Money movement must be completed safely in PostgreSQL.

If the transfer changes balances, this must happen inside one database
transaction.

RabbitMQ is useful after the critical operation is completed, for example:

- send notification after transfer
- process analytics event after transfer
- trigger background worker after transfer

## Consequences

Positive:

- API can stay faster
- background processing becomes decoupled
- workers can be scaled separately later
- failures in notification logic do not break completed transfer

Negative:

- message delivery and retries must be handled
- duplicate messages are possible
- workers must be idempotent
- async flows are harder to debug than direct calls

## Current Status

Accepted.

---

# 7. Money Operations Must Be Transaction-Safe

## Decision

Money transfers must be executed inside a database transaction.

A transfer should update all related data atomically:

- source account balance
- destination account balance
- transfer record
- transaction history
- audit event

If one part fails, all changes must be rolled back.

## Reason

A banking system must not allow partial money movement.

Invalid example:

```text
source account decreased
destination account not increased
```

This must never happen.

## Consequences

Positive:

- balance consistency is protected
- failed transfers do not partially update data
- transaction history stays connected to balance changes

Negative:

- implementation must carefully handle locks and errors
- concurrent transfers require correct row locking
- tests must cover failure scenarios

## Current Status

Accepted.

---

# 8. Every Balance Change Must Have Transaction History

## Decision

Account balance must not change without a transaction record.

Every completed transfer should create transaction records:

- debit transaction for source account
- credit transaction for destination account

## Reason

Balance alone is not enough.

The system must be able to answer:

- why did the balance change?
- when did it change?
- which operation caused the change?
- what was the balance before?
- what was the balance after?

This is necessary for debugging, audit and user history.

## Consequences

Positive:

- account history is explainable
- money movement can be investigated
- balance changes are not silent

Negative:

- write operations become more complex
- transaction table can grow quickly
- indexes and pagination will be needed

## Current Status

Accepted.

---

# 9. Use Idempotency for Transfers

## Decision

Transfer creation must use idempotency.

The API should require an idempotency key for:

```text
POST /transfers
```

## Reason

A client can send the same request more than once.

Examples:

- network timeout
- user double-clicks send button
- frontend retries request
- mobile client loses connection and retries

Without idempotency, the same transfer may be executed twice.

## Consequences

Positive:

- duplicate transfer execution can be prevented
- retry behavior becomes safer
- API is closer to real financial systems

Negative:

- idempotency storage must be designed
- repeated requests must return predictable result
- edge cases with failed transfers must be handled explicitly

## Current Status

Accepted.

---

# 10. Do Not Store Real Card Data

## Decision

CoreBank must not store real card numbers, CVV codes or sensitive payment
card data.

Only fake or masked test card data is allowed.

## Reason

Real card data requires strict security and compliance rules.

This project is educational and portfolio-oriented. It should not handle
real payment card data.

## Consequences

Positive:

- safer project
- simpler implementation
- no false impression of PCI DSS compliance

Negative:

- card functionality is only simulated
- real payment processing is out of scope

## Current Status

Accepted.

---

# 11. Authentication Is Postponed

## Decision

Authentication is not part of the first implementation stage.

The first stages focus on:

- project structure
- API basics
- database model
- transfer correctness
- Docker
- infrastructure fundamentals

Authentication will be added later when the core domain is clearer.

## Reason

Authentication is important, but adding it too early can distract from the
main learning goal: safe backend and banking domain design.

The API should still be designed with future authorization in mind.

## Consequences

Positive:

- faster start for core API and database logic
- focus stays on money movement and data model
- less initial complexity

Negative:

- early API will not be production-secure
- future authorization rules must be added carefully
- docs must clearly state that auth is postponed

## Current Status

Accepted.

---

# 12. Add Technologies Only When They Solve a Real Problem

## Decision

Technologies are added gradually.

CoreBank should not add tools only because they are popular.

## Reason

The project is designed for deep understanding.

Correct order:

```text
problem -> reason -> technology -> implementation
```

Incorrect order:

```text
technology -> forced usage -> unnecessary complexity
```

Examples:

- Redis appears when there is a caching problem
- RabbitMQ appears when there is async work
- monitoring appears when there is traffic
- Kubernetes appears after Docker is clear

## Consequences

Positive:

- architecture stays understandable
- every technology has a purpose
- learning is deeper
- project avoids fake complexity

Negative:

- some popular tools appear later
- early project may look simple
- patience is required

## Current Status

Accepted.

---

# 13. Current Decisions Summary

Accepted decisions:

- start with documentation before code
- use one repository
- start with modular monolith, not microservices
- use PostgreSQL as source of truth
- use Redis only as cache or temporary storage
- use RabbitMQ for asynchronous side effects
- keep money operations transaction-safe
- require transaction history for balance changes
- use idempotency for transfers
- do not store real card data
- postpone authentication
- add technologies only when they solve real problems

---

# 14. Next Decisions to Document

Future decisions:

- exact backend project structure
- SQLAlchemy vs SQLModel
- money amount type
- migration strategy
- testing strategy
- Docker Compose structure
- Redis cache invalidation rules
- RabbitMQ retry strategy
- worker idempotency strategy
- Kubernetes deployment structure
- monitoring stack details
