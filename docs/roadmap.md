COREBANK ROADMAP
================

This document describes the development roadmap for the CoreBank project.

CoreBank is developed step by step. Each release adds one meaningful part
of the system and explains why this part is needed.

The goal is not to add technologies as fast as possible. The goal is to
understand which problem each technology solves and how it changes the
architecture.

======================================================================
RELEASE STRATEGY
======================================================================

CoreBank is developed by releases:

[01] v0.1 - Architecture and Documentation
[02] v0.2 - First API
[03] v0.3 - PostgreSQL
[04] v0.4 - Docker
[05] v0.5 - Redis
[06] v0.6 - RabbitMQ and Workers
[07] v0.7 - Traffic Generator
[08] v0.8 - Monitoring
[09] v0.9 - Kubernetes
[10] v1.0 - Production-like Version

Each release has:

[01] Goal
[02] Why this release exists
[03] Planned work
[04] Done criteria
[05] Learning focus


======================================================================
v0.1 - ARCHITECTURE AND DOCUMENTATION
======================================================================

GOAL
----

Design the project foundation before writing business code.

WHY THIS RELEASE EXISTS
-----------------------

A backend project becomes chaotic when code is written before the domain,
architecture and main rules are understood.

Before writing the first API endpoint, we need to answer several important
questions:

[01] What system are we building?
[02] What problem does the system solve?
[03] What are the main domain entities?
[04] What are the critical business rules?
[05] Which technologies will appear later and why?
[06] How will the project grow step by step?

This release creates the foundation for the whole project.

PLANNED WORK
------------

[01] Create README.md
[02] Create docs/roadmap.md
[03] Create docs/architecture.md
[04] Create docs/database.md
[05] Create docs/api.md
[06] Create docs/decisions.md
[07] Create docs/adr/
[08] Define the first version of the banking domain model
[09] Define important business invariants
[10] Record the first architecture decisions

DONE CRITERIA
-------------

Release v0.1 is done when:

[01] README.md explains the project in English and Russian
[02] docs/roadmap.md describes all planned releases
[03] docs/architecture.md describes the first planned architecture
[04] docs/database.md describes the first domain entities and data rules
[05] docs/api.md describes the first planned API endpoints
[06] docs/decisions.md contains important engineering decisions
[07] At least one ADR exists in docs/adr/
[08] The project can be understood without reading the source code

LEARNING FOCUS
--------------

[01] Project planning
[02] Domain modeling
[03] Architecture thinking
[04] Documentation
[05] Engineering decision making


======================================================================
v0.2 - FIRST API
======================================================================

GOAL
----

Create the first backend service.

WHY THIS RELEASE EXISTS
-----------------------

Before adding a database, cache, message broker or containers, the project
needs a working API.

The first API proves that the backend application can start, receive HTTP
requests and return responses.

At this stage, the API does not need complex business logic. The goal is to
create a clean foundation for future code.

PLANNED WORK
------------

[01] Create backend application structure
[02] Add FastAPI
[03] Add application entry point
[04] Add health check endpoint
[05] Add basic configuration
[06] Add basic error handling approach
[07] Add simple local run instructions
[08] Add first tests

PLANNED ENDPOINTS
-----------------

[01] GET /health
     Checks that the API is running.

[02] GET /version
     Returns project version and basic service information.

DONE CRITERIA
-------------

Release v0.2 is done when:

[01] API starts locally
[02] GET /health returns successful response
[03] GET /version returns service information
[04] Basic project structure is clear
[05] Tests can be run locally
[06] README or docs explain how to start the API

LEARNING FOCUS
--------------

[01] FastAPI basics
[02] HTTP request / response model
[03] Backend project structure
[04] Application configuration
[05] Basic testing


======================================================================
v0.3 - POSTGRESQL
======================================================================

GOAL
----

Add persistent data storage.

WHY THIS RELEASE EXISTS
-----------------------

A banking system cannot keep important data only in memory.

Users, accounts, balances, transfers and transactions must be stored
reliably. PostgreSQL is added when the project needs persistent and
consistent data.

This release introduces the first real business data.

PLANNED WORK
------------

[01] Add PostgreSQL
[02] Add database connection configuration
[03] Add SQLAlchemy or SQLModel
[04] Add Alembic migrations
[05] Design first tables
[06] Implement user creation
[07] Implement account creation
[08] Implement basic balance storage
[09] Implement transaction records
[10] Add tests for database logic

FIRST PLANNED TABLES
--------------------

[01] users
[02] accounts
[03] cards
[04] transfers
[05] transactions
[06] audit_events

IMPORTANT DATA RULES
--------------------

[01] Account balance must not change without a transaction record.
[02] Money transfer must be atomic.
[03] Transfer must not create money from nowhere.
[04] Failed transfer must not partially change balances.
[05] Operation history must be preserved.
[06] Important actions must be auditable.

DONE CRITERIA
-------------

Release v0.3 is done when:

[01] PostgreSQL is connected to the API
[02] Database migrations work
[03] Main tables are created
[04] API can create users
[05] API can create accounts
[06] API can store transaction history
[07] Tests verify basic database behavior

LEARNING FOCUS
--------------

[01] PostgreSQL
[02] Relational modeling
[03] SQL transactions
[04] Migrations
[05] Data consistency
[06] Banking data invariants


======================================================================
v0.4 - DOCKER
======================================================================

GOAL
----

Run the project in containers.

WHY THIS RELEASE EXISTS
-----------------------

Local development becomes harder when the project depends on multiple
services.

Docker helps run the API and PostgreSQL in a predictable environment.

This release makes the project easier to start on another machine.

PLANNED WORK
------------

[01] Add Dockerfile for API
[02] Add docker-compose.yml
[03] Add PostgreSQL service
[04] Add environment variables
[05] Add local development commands
[06] Add database initialization flow
[07] Document Docker-based startup

PLANNED SERVICES
----------------

[01] corebank-api
[02] corebank-postgres

DONE CRITERIA
-------------

Release v0.4 is done when:

[01] Project starts with docker compose
[02] API container starts successfully
[03] PostgreSQL container starts successfully
[04] API can connect to PostgreSQL inside Docker network
[05] Migrations can be applied inside containers
[06] Documentation explains how to run the project with Docker

LEARNING FOCUS
--------------

[01] Dockerfile
[02] Docker images
[03] Docker containers
[04] Docker Compose
[05] Container networking
[06] Environment variables


======================================================================
v0.5 - REDIS
======================================================================

GOAL
----

Add caching where it solves a real problem.

WHY THIS RELEASE EXISTS
-----------------------

Redis should not be added just because it is popular.

Redis appears when the project has data that is read often and does not
need to be recalculated or loaded from PostgreSQL every time.

This release introduces cache thinking.

PLANNED WORK
------------

[01] Add Redis service
[02] Connect API to Redis
[03] Identify safe cache candidates
[04] Add first cache usage
[05] Define cache invalidation rules
[06] Add tests for cached behavior
[07] Document what is cached and why

POSSIBLE CACHE CANDIDATES
-------------------------

[01] User profile summary
[02] Account list for user
[03] Frequently requested reference data
[04] Short-lived operation status

IMPORTANT CACHE RULES
---------------------

[01] Redis is not the source of truth.
[02] PostgreSQL remains the source of truth.
[03] Money balance must not rely only on Redis.
[04] Cache must have clear invalidation rules.
[05] Stale cache must not break critical business logic.

DONE CRITERIA
-------------

Release v0.5 is done when:

[01] Redis runs locally
[02] API can connect to Redis
[03] At least one real cache use case is implemented
[04] Cache invalidation is documented
[05] Critical money operations do not depend on cache as source of truth

LEARNING FOCUS
--------------

[01] Redis basics
[02] Cache patterns
[03] Cache invalidation
[04] Source of truth
[05] Performance vs correctness


======================================================================
v0.6 - RABBITMQ AND WORKERS
======================================================================

GOAL
----

Move part of the work to asynchronous processing.

WHY THIS RELEASE EXISTS
-----------------------

Not every task must be completed inside the API request.

Some tasks can happen later:

[01] Sending notifications
[02] Writing audit events
[03] Preparing analytics
[04] Processing non-critical background work

RabbitMQ is added when synchronous processing starts to make the API slower
or more tightly coupled.

PLANNED WORK
------------

[01] Add RabbitMQ service
[02] Add message producer in API
[03] Add Notification Worker
[04] Add Audit Worker
[05] Add Analytics Worker
[06] Define queues and routing
[07] Add retry strategy
[08] Add error handling for failed messages
[09] Document async processing flow

PLANNED WORKERS
---------------

[01] Notification Worker
     Sends or simulates user notifications.

[02] Audit Worker
     Processes important audit events.

[03] Analytics Worker
     Processes events used for reports and analysis.

DONE CRITERIA
-------------

Release v0.6 is done when:

[01] RabbitMQ runs locally
[02] API can publish messages
[03] Workers can consume messages
[04] At least one business event is processed asynchronously
[05] Failed message behavior is documented
[06] API does not depend on immediate worker execution for critical money consistency

LEARNING FOCUS
--------------

[01] Message brokers
[02] Queues
[03] Producers and consumers
[04] Async processing
[05] Retry strategy
[06] Event-driven thinking


======================================================================
v0.7 - TRAFFIC GENERATOR
======================================================================

GOAL
----

Create artificial load for the system.

WHY THIS RELEASE EXISTS
-----------------------

Monitoring and performance work are useless without traffic.

The traffic generator simulates users and operations so that the system can
be observed under load.

This release helps test the system as if real clients were using it.

PLANNED WORK
------------

[01] Create traffic generator service
[02] Generate users
[03] Generate accounts
[04] Generate transfers
[05] Generate repeated API requests
[06] Add configurable load level
[07] Add documentation for load scenarios

POSSIBLE LOAD SCENARIOS
-----------------------

[01] Many users checking account balances
[02] Many transfers between accounts
[03] Repeated requests to the same endpoint
[04] Background notification load
[05] Audit event load

DONE CRITERIA
-------------

Release v0.7 is done when:

[01] Traffic generator can run locally
[02] It can create realistic API activity
[03] Load level can be configured
[04] System behavior under traffic can be observed
[05] Documentation explains how to run load scenarios

LEARNING FOCUS
--------------

[01] Load simulation
[02] API behavior under pressure
[03] Bottleneck discovery
[04] Test data generation
[05] Production-like thinking


======================================================================
v0.8 - MONITORING
======================================================================

GOAL
----

Make the system observable.

WHY THIS RELEASE EXISTS
-----------------------

A production-like system must be observable.

It is not enough to know that the service is running. We need to understand:

[01] How many requests are processed
[02] How long requests take
[03] How often errors happen
[04] What happens inside workers
[05] Where bottlenecks appear
[06] Which service failed and why

This release adds metrics, logs and tracing.

PLANNED WORK
------------

[01] Add structured logging
[02] Add request metrics
[03] Add business metrics
[04] Add Prometheus
[05] Add Grafana dashboards
[06] Add Loki for logs
[07] Add tracing with OpenTelemetry
[08] Add Jaeger
[09] Document observability setup

PLANNED OBSERVABILITY AREAS
---------------------------

[01] API request count
[02] API request latency
[03] API error count
[04] Transfer count
[05] Failed transfer count
[06] Worker message processing count
[07] Worker errors
[08] Database latency
[09] Queue size

DONE CRITERIA
-------------

Release v0.8 is done when:

[01] Metrics are available
[02] Logs are structured
[03] Traces are available
[04] Grafana dashboard exists
[05] API and workers can be observed
[06] Documentation explains how to inspect the system

LEARNING FOCUS
--------------

[01] Metrics
[02] Logs
[03] Tracing
[04] Prometheus
[05] Grafana
[06] Loki
[07] OpenTelemetry
[08] Jaeger


======================================================================
v0.9 - KUBERNETES
======================================================================

GOAL
----

Deploy the system to local Kubernetes.

WHY THIS RELEASE EXISTS
-----------------------

Docker Compose is useful for local development, but Kubernetes introduces
a more production-like deployment model.

This release helps understand how backend systems are deployed and connected
inside a cluster.

PLANNED WORK
------------

[01] Add Kubernetes manifests
[02] Add API Deployment
[03] Add Worker Deployments
[04] Add PostgreSQL setup for local Kubernetes
[05] Add Redis setup
[06] Add RabbitMQ setup
[07] Add Services
[08] Add ConfigMaps
[09] Add Secrets for local development
[10] Add health probes
[11] Document local Kubernetes startup

PLANNED KUBERNETES OBJECTS
--------------------------

[01] Deployment
[02] Service
[03] ConfigMap
[04] Secret
[05] PersistentVolumeClaim
[06] Ingress
[07] Liveness probe
[08] Readiness probe

DONE CRITERIA
-------------

Release v0.9 is done when:

[01] API runs in local Kubernetes
[02] Workers run in local Kubernetes
[03] Services can communicate inside the cluster
[04] Configuration is moved to ConfigMaps and Secrets
[05] Health probes are configured
[06] Documentation explains how to deploy locally

LEARNING FOCUS
--------------

[01] Kubernetes basics
[02] Deployments
[03] Services
[04] ConfigMaps
[05] Secrets
[06] Probes
[07] Cluster networking
[08] Local Kubernetes workflow


======================================================================
v1.0 - PRODUCTION-LIKE VERSION
======================================================================

GOAL
----

Bring the project to a portfolio-ready backend system.

WHY THIS RELEASE EXISTS
-----------------------

The final release combines all previous stages into a complete
production-like backend project.

The project should be understandable, runnable, documented and useful as a
portfolio example.

PLANNED WORK
------------

[01] Complete core banking functionality
[02] Improve error handling
[03] Improve test coverage
[04] Improve documentation
[05] Review architecture decisions
[06] Review database design
[07] Review API design
[08] Prepare final project demo
[09] Add final README updates

DONE CRITERIA
-------------

Release v1.0 is done when:

[01] Project can be started locally
[02] Main business flows work
[03] API is documented
[04] Database model is documented
[05] Architecture is documented
[06] Docker setup works
[07] Kubernetes setup works locally
[08] Monitoring setup works
[09] Tests can be run
[10] Project is ready to show as portfolio work

LEARNING FOCUS
--------------

[01] Backend system design
[02] Reliability
[03] Documentation
[04] Production-like development
[05] Portfolio preparation


======================================================================
CURRENT POSITION
======================================================================

Current release:

    v0.1 - Architecture and Documentation

Current task order:

[01] README.md
     Status: done

[02] docs/roadmap.md
     Status: current task

[03] docs/architecture.md
     Status: next

[04] docs/database.md
     Status: planned

[05] docs/api.md
     Status: planned

[06] docs/decisions.md
     Status: planned

[07] docs/adr/ADR-001-project-structure.md
     Status: planned


======================================================================
IMPORTANT RULE
======================================================================

CoreBank should grow because of real engineering needs.

Do not add:

[01] Redis before there is a caching problem
[02] RabbitMQ before there is asynchronous work
[03] Kubernetes before Docker Compose is clear
[04] Monitoring before there is traffic
[05] Complex architecture before the domain is understood

First understand the problem. Then add the tool.
