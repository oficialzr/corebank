# ADR-001: Project Structure and Initial Architecture Approach

Status: Accepted

Date: 2026-07-05

---

# Context

CoreBank is a production-like backend learning project.

The project is planned to include:

- API
- PostgreSQL
- Redis
- RabbitMQ
- background workers
- traffic generator
- monitoring
- Docker
- Kubernetes
- documentation
- tests

At the beginning, the project domain is still being designed.

The main entities are planned, but not implemented yet:

- User
- Account
- Card
- Transfer
- Transaction
- AuditEvent

The project needs a structure that is simple enough for early development,
but also flexible enough to grow into a production-like backend system.

There are two important architecture questions:

- Should the project use one repository or many repositories?
- Should the project start as a modular monolith or as microservices?

---

# Decision

CoreBank will start with:

- one repository
- modular monolith architecture
- documentation-first project structure
- gradual infrastructure growth

The first implementation will not start with microservices.

The first backend application will be one API service with internal modules.

Possible future modules:

- users
- accounts
- cards
- transfers
- transactions
- audit
- notifications
- analytics

The project may later add separate worker services, but the core API will
start as one application.

---

# Repository Structure

Initial repository structure:

```text
corebank/
  docs/
    adr/
    api.md
    architecture.md
    database.md
    decisions.md
    roadmap.md
  README.md
```

Future structure may become:

```text
corebank/
  apps/
    api/
    workers/
    traffic-generator/
  docs/
    adr/
    api.md
    architecture.md
    database.md
    decisions.md
    roadmap.md
  docker/
  k8s/
  monitoring/
  tests/
  README.md
```

The future structure is not created immediately.

Folders should appear only when they contain real project content.

---

# Reason

## Why one repository?

One repository is better for the current stage because:

- the project is still small
- the domain model is still changing
- local development is easier
- documentation is easier to keep close to code
- refactoring is easier
- the whole system is easier to understand
- it is better for a portfolio project
- it avoids unnecessary DevOps complexity at the beginning

Multiple repositories would add problems too early:

- more setup work
- harder local development
- harder documentation synchronization
- harder refactoring
- more CI/CD complexity
- more repository management

At this stage, these problems do not bring useful value.

## Why modular monolith?

A modular monolith is better at the beginning because:

- business boundaries are not stable yet
- money transfer logic needs strong consistency
- database transactions are easier inside one application
- debugging is easier
- deployment is easier
- testing is easier
- learning is more focused
- infrastructure complexity stays lower

Microservices would add complexity too early:

- network calls between services
- distributed tracing
- distributed failures
- service discovery
- separate deployments
- data ownership problems
- harder transaction consistency
- harder debugging

CoreBank should first become correct and understandable.

Only after that it may become distributed if there is a real reason.

---

# Consequences

## Positive consequences

This decision gives:

- simpler start
- cleaner learning process
- easier local development
- easier debugging
- easier refactoring
- clearer documentation
- better focus on domain logic
- safer implementation of money transfers
- lower infrastructure complexity

The project can still grow gradually.

Workers, Docker, Kubernetes and monitoring can be added later without
starting with unnecessary complexity.

## Negative consequences

This decision also has trade-offs:

- the API application can become too large if modules are not separated well
- module boundaries must be protected manually
- future service extraction may require refactoring
- one repository can become large over time
- discipline is required to keep structure clean

These trade-offs are acceptable for the current stage.

---

# Rules

The project should follow these rules:

- do not create empty folders without real content
- do not split into microservices without a real reason
- keep modules logically separated
- keep PostgreSQL as the source of truth
- keep money transfer logic transaction-safe
- keep documentation updated when decisions change
- add Redis only when caching is needed
- add RabbitMQ only when asynchronous processing is needed
- add Kubernetes only after Docker Compose is clear
- add monitoring when there is traffic to observe

---

# Alternatives Considered

## Alternative 1: Start with microservices

Rejected.

Reason:

Microservices would make the project harder before the domain is stable.

Problems:

- too much infrastructure too early
- more difficult debugging
- harder local startup
- harder data consistency
- more complex deployment
- more difficult tests

Microservices may be considered later if real boundaries appear.

## Alternative 2: Use multiple repositories

Rejected.

Reason:

Multiple repositories would make development and learning slower at the
current stage.

Problems:

- harder navigation
- harder refactoring
- harder local setup
- more CI/CD work
- more repository management

One repository is enough for now.

## Alternative 3: Start with only code and no documentation

Rejected.

Reason:

The project is designed as a production-like learning project.

Without documentation, architectural decisions would be lost or unclear.

Documentation helps explain:

- what is being built
- why it is being built this way
- what each technology is responsible for
- what the future plan is

---

# Final Decision

CoreBank starts as a single-repository modular monolith.

This is the best fit for the current stage because it keeps the project
simple, understandable and safe for learning.

The project can evolve later, but only when real engineering needs appear.
