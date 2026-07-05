COREBANK
========

Production-like backend project for a simplified banking platform.
Production-like backend-проект упрощенной банковской платформы.

======================================================================
ENGLISH VERSION
======================================================================

1. ABOUT THE PROJECT
--------------------

CoreBank is a production-like backend project that simulates the core
functionality of a banking platform.

The goal is not to build a simple CRUD application. The goal is to
gradually design and implement a backend system that is close to real
industrial development.

The project will include:

[01] Clear architecture
[02] Database design
[03] Transaction-safe money operations
[04] Caching
[05] Message queues
[06] Background workers
[07] Logging
[08] Monitoring
[09] Docker
[10] Kubernetes
[11] CI/CD

CoreBank is used as a practical roadmap for growing backend engineering
skills.

Each technology is added only when it solves a real problem in the
system.


2. PROJECT GOALS
----------------

CoreBank helps practice and demonstrate:

[01] Backend API development
[02] Database modeling
[03] Safe money transfers
[04] Service decomposition
[05] Asynchronous processing
[06] Caching
[07] Containerized development
[08] Kubernetes deployment
[09] Observability
[10] Engineering decision making

The project is built step by step, from a simple API to a production-like
backend system.


3. DOMAIN
---------

CoreBank models a simplified banking system.

Main domain entities:

[01] User
     A person who uses the banking system.

[02] Account
     A bank account owned by a user.

[03] Card
     A card connected to an account.

[04] Balance
     The amount of money available on an account.

[05] Transfer
     A business operation that moves money between accounts.

[06] Transaction
     A technical record of money movement.

[07] Audit Event
     A record of an important action in the system.

[08] Notification
     A message sent to a user about an important event.

[09] Analytics
     Data used for reporting and system analysis.


4. CRITICAL BUSINESS RULE
-------------------------

The most important part of the project is correct money movement.

The system must not allow:

[01] Money withdrawal without deposit
[02] Money deposit without withdrawal
[03] Money creation from nowhere
[04] Lost transaction history
[05] Duplicated transfer execution
[06] Balance changes without audit trail

Because of this, the project pays special attention to:

[01] Database transactions
[02] Data consistency
[03] Idempotency
[04] Audit logs
[05] Error handling
[06] Reliability of background processes


5. PLANNED ARCHITECTURE
-----------------------

The project starts simple.

Initial version:

    Client
      |
      v
    CoreBank API
      |
      v
    PostgreSQL

Future version:

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

The architecture will evolve gradually.

First, the project will have a simple API. Then PostgreSQL will be added.
After that, Docker, Redis, RabbitMQ, workers, monitoring and Kubernetes
will be introduced.

This approach helps understand why each technology exists in the system.


6. PLANNED TECH STACK
---------------------

Backend:

[01] Python
[02] FastAPI
[03] SQLAlchemy or SQLModel
[04] Alembic

Database:

[01] PostgreSQL

Cache:

[01] Redis

Message Broker:

[01] RabbitMQ

Infrastructure:

[01] Docker
[02] Docker Compose
[03] Kubernetes

Observability:

[01] Prometheus
[02] Grafana
[03] Loki
[04] OpenTelemetry
[05] Jaeger

Testing and Code Quality:

[01] Pytest
[02] Ruff
[03] Mypy
[04] CI/CD


7. CURRENT PROJECT STRUCTURE
----------------------------

    corebank/
      docs/
        adr/
        api.md
        architecture.md
        database.md
        decisions.md
        roadmap.md
      README.md

The structure will grow gradually as new parts of the system appear.

Folders are not created in advance without real content. This keeps the
repository clean and easy to understand.


8. DOCUMENTATION
----------------

Project documentation is stored in the docs/ directory.

Main documents:

[01] docs/architecture.md
     System architecture, components, responsibilities and communication
     between parts of the system.

[02] docs/api.md
     API design, planned endpoints, request examples and response examples.

[03] docs/database.md
     Database model, tables, relations and important data rules.

[04] docs/roadmap.md
     Project release plan, learning stages and implementation order.

[05] docs/decisions.md
     Important engineering decisions.

[06] docs/adr/
     Architecture Decision Records. Separate documents explaining important
     architecture choices.

- docs/development.md
  - local development setup
  - API startup commands
  - test commands


9. ROADMAP
----------

The project is developed by releases.


v0.1 - Architecture and Documentation

Goal:
    Design the project foundation before writing business code.

Planned work:
    [01] Define project goals
    [02] Describe planned architecture
    [03] Document the roadmap
    [04] Define the first domain model
    [05] Record key engineering decisions


v0.2 - First API

Goal:
    Create the first backend service.

Planned work:
    [01] Create FastAPI application
    [02] Add health check endpoint
    [03] Define first API endpoints
    [04] Create basic backend project structure


v0.3 - PostgreSQL

Goal:
    Add persistent data storage.

Planned work:
    [01] Add PostgreSQL
    [02] Design users, accounts and transactions tables
    [03] Add database migrations
    [04] Implement basic persistence


v0.4 - Docker

Goal:
    Run the project in containers.

Planned work:
    [01] Create Dockerfile
    [02] Add Docker Compose
    [03] Run API and PostgreSQL locally in containers


v0.5 - Redis

Goal:
    Add caching where it solves a real problem.

Planned work:
    [01] Add Redis
    [02] Define what data can be cached
    [03] Document cache invalidation rules


v0.6 - RabbitMQ and Workers

Goal:
    Move part of the work to asynchronous processing.

Planned work:
    [01] Add RabbitMQ
    [02] Create background workers
    [03] Process notifications
    [04] Process audit events
    [05] Process analytics events


v0.7 - Traffic Generator

Goal:
    Create artificial load for the system.

Planned work:
    [01] Create traffic generator service
    [02] Simulate users
    [03] Simulate transfers
    [04] Prepare the system for monitoring and load testing


v0.8 - Monitoring

Goal:
    Make the system observable.

Planned work:
    [01] Add metrics
    [02] Add logs
    [03] Add tracing
    [04] Connect Prometheus
    [05] Connect Grafana
    [06] Connect Loki
    [07] Connect Jaeger


v0.9 - Kubernetes

Goal:
    Deploy the system to local Kubernetes.

Planned work:
    [01] Create Kubernetes manifests
    [02] Add Deployments
    [03] Add Services
    [04] Add ConfigMaps
    [05] Understand how services communicate inside a cluster


v1.0 - Production-like Version

Goal:
    Bring the project to a portfolio-ready backend system.

Planned work:
    [01] Complete main backend functionality
    [02] Improve reliability
    [03] Update documentation
    [04] Prepare the project for demonstration


10. ENGINEERING PRINCIPLES
--------------------------

CoreBank follows these principles:

[01] Start simple, then evolve.
[02] Do not add technologies without a clear reason.
[03] Understand the problem first, choose the tool second.
[04] Keep business logic understandable.
[05] Treat money operations as critical operations.
[06] Document important decisions.
[07] Do not create empty folders and unnecessary architecture in advance.
[08] Build the project like a real backend system, not like a toy tutorial.


11. CURRENT STATUS
------------------

Current release:

    v0.1 - Architecture and Documentation

Current focus:

[01] Project vision
[02] Banking domain model
[03] Documentation
[04] Architecture decisions
[05] Future API design
[06] Future database model


12. LICENSE
-----------

This project is licensed under the MIT License.


======================================================================
РУССКАЯ ВЕРСИЯ
======================================================================

1. О ПРОЕКТЕ
------------

CoreBank - это production-like backend-проект, который имитирует базовую
функциональность банковской платформы.

Цель проекта - не просто сделать обычное CRUD-приложение. Цель -
постепенно спроектировать и реализовать backend-систему, приближенную к
промышленной разработке.

В проекте будут использоваться:

[01] Понятная архитектура
[02] Проектирование базы данных
[03] Безопасные денежные операции
[04] Кэширование
[05] Очереди сообщений
[06] Фоновые обработчики
[07] Логирование
[08] Мониторинг
[09] Docker
[10] Kubernetes
[11] CI/CD

CoreBank используется как практический roadmap для развития backend-навыков.

Каждая технология добавляется только тогда, когда она решает реальную
проблему в системе.


2. ЦЕЛИ ПРОЕКТА
---------------

CoreBank помогает практиковать и показывать:

[01] Разработку backend API
[02] Моделирование базы данных
[03] Безопасные денежные переводы
[04] Разделение системы на компоненты
[05] Асинхронную обработку задач
[06] Кэширование
[07] Разработку через контейнеры
[08] Деплой в Kubernetes
[09] Наблюдаемость системы
[10] Принятие инженерных решений

Проект строится постепенно: от простого API до production-like
backend-системы.


3. ПРЕДМЕТНАЯ ОБЛАСТЬ
---------------------

CoreBank моделирует упрощенную банковскую систему.

Основные сущности:

[01] User
     Пользователь банковской системы.

[02] Account
     Банковский счет пользователя.

[03] Card
     Карта, привязанная к счету.

[04] Balance
     Количество денег на счете.

[05] Transfer
     Бизнес-операция перевода денег между счетами.

[06] Transaction
     Техническая запись о движении денег.

[07] Audit Event
     Запись о важном действии в системе.

[08] Notification
     Уведомление пользователя о важном событии.

[09] Analytics
     Данные для отчетов и анализа системы.


4. КРИТИЧЕСКОЕ БИЗНЕС-ПРАВИЛО
-----------------------------

Самая важная часть проекта - корректное движение денег.

Система не должна допускать:

[01] Списание денег без зачисления
[02] Зачисление денег без списания
[03] Создание денег из воздуха
[04] Потерю истории операций
[05] Двойное выполнение одного и того же перевода
[06] Изменение баланса без audit-следа

Поэтому в проекте особое внимание уделяется:

[01] Транзакциям базы данных
[02] Согласованности данных
[03] Идемпотентности
[04] Audit-логам
[05] Обработке ошибок
[06] Надежности фоновых процессов


5. ПЛАНИРУЕМАЯ АРХИТЕКТУРА
--------------------------

Проект начинается просто.

Начальная версия:

    Client
      |
      v
    CoreBank API
      |
      v
    PostgreSQL

Будущая версия:

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

Архитектура будет развиваться постепенно.

Сначала в проекте появится простое API. Затем будет добавлен PostgreSQL.
После этого появятся Docker, Redis, RabbitMQ, воркеры, мониторинг и
Kubernetes.

Такой подход помогает понимать, зачем каждая технология существует в системе.


6. ПЛАНИРУЕМЫЙ СТЕК ТЕХНОЛОГИЙ
------------------------------

Backend:

[01] Python
[02] FastAPI
[03] SQLAlchemy или SQLModel
[04] Alembic

База данных:

[01] PostgreSQL

Кэш:

[01] Redis

Брокер сообщений:

[01] RabbitMQ

Инфраструктура:

[01] Docker
[02] Docker Compose
[03] Kubernetes

Наблюдаемость:

[01] Prometheus
[02] Grafana
[03] Loki
[04] OpenTelemetry
[05] Jaeger

Тестирование и качество кода:

[01] Pytest
[02] Ruff
[03] Mypy
[04] CI/CD


7. ТЕКУЩАЯ СТРУКТУРА ПРОЕКТА
----------------------------

    corebank/
      docs/
        adr/
        api.md
        architecture.md
        database.md
        decisions.md
        roadmap.md
      README.md

Структура будет расти постепенно по мере появления новых частей системы.

Папки не создаются заранее без реального содержимого. Это помогает держать
репозиторий чистым и понятным.


8. ДОКУМЕНТАЦИЯ
---------------

Документация проекта хранится в директории docs/.

Основные документы:

[01] docs/architecture.md
     Архитектура системы, компоненты, зоны ответственности и взаимодействие
     частей системы.

[02] docs/api.md
     Проектирование API, планируемые endpoints, примеры запросов и ответов.

[03] docs/database.md
     Модель базы данных, таблицы, связи и важные правила работы с данными.

[04] docs/roadmap.md
     План развития проекта, этапы обучения и порядок реализации.

[05] docs/decisions.md
     Важные инженерные решения.

[06] docs/adr/
     Architecture Decision Records. Отдельные документы с объяснением
     важных архитектурных решений.


9. ROADMAP
----------

Проект разрабатывается по релизам.


v0.1 - Архитектура и документация

Цель:
    Спроектировать основу проекта до написания бизнес-кода.

План работ:
    [01] Определить цели проекта
    [02] Описать планируемую архитектуру
    [03] Задокументировать roadmap
    [04] Определить первую модель предметной области
    [05] Зафиксировать ключевые инженерные решения


v0.2 - Первое API

Цель:
    Создать первый backend-сервис.

План работ:
    [01] Создать FastAPI-приложение
    [02] Добавить health check endpoint
    [03] Определить первые API endpoints
    [04] Создать базовую структуру backend-кода


v0.3 - PostgreSQL

Цель:
    Добавить постоянное хранение данных.

План работ:
    [01] Добавить PostgreSQL
    [02] Спроектировать таблицы пользователей, счетов и транзакций
    [03] Добавить миграции базы данных
    [04] Реализовать базовое сохранение данных


v0.4 - Docker

Цель:
    Запускать проект в контейнерах.

План работ:
    [01] Создать Dockerfile
    [02] Добавить Docker Compose
    [03] Запустить API и PostgreSQL локально в контейнерах


v0.5 - Redis

Цель:
    Добавить кэширование там, где оно решает реальную проблему.

План работ:
    [01] Добавить Redis
    [02] Определить, какие данные можно кэшировать
    [03] Описать правила инвалидации кэша


v0.6 - RabbitMQ и Workers

Цель:
    Вынести часть задач в асинхронную обработку.

План работ:
    [01] Добавить RabbitMQ
    [02] Создать фоновые workers
    [03] Обрабатывать уведомления
    [04] Обрабатывать audit-события
    [05] Обрабатывать события аналитики


v0.7 - Traffic Generator

Цель:
    Создать искусственную нагрузку на систему.

План работ:
    [01] Создать сервис генерации трафика
    [02] Имитировать пользователей
    [03] Имитировать переводы
    [04] Подготовить систему к мониторингу и нагрузочному тестированию


v0.8 - Monitoring

Цель:
    Сделать систему наблюдаемой.

План работ:
    [01] Добавить метрики
    [02] Добавить логи
    [03] Добавить трассировку
    [04] Подключить Prometheus
    [05] Подключить Grafana
    [06] Подключить Loki
    [07] Подключить Jaeger


v0.9 - Kubernetes

Цель:
    Развернуть систему в локальном Kubernetes.

План работ:
    [01] Создать Kubernetes manifests
    [02] Добавить Deployments
    [03] Добавить Services
    [04] Добавить ConfigMaps
    [05] Понять, как сервисы взаимодействуют внутри кластера


v1.0 - Production-like версия

Цель:
    Довести проект до состояния backend-системы, готовой для портфолио.

План работ:
    [01] Завершить основную backend-функциональность
    [02] Улучшить надежность
    [03] Обновить документацию
    [04] Подготовить проект для демонстрации


10. ИНЖЕНЕРНЫЕ ПРИНЦИПЫ
-----------------------

CoreBank следует этим принципам:

[01] Начинать просто, затем постепенно развивать систему.
[02] Не добавлять технологии без понятной причины.
[03] Сначала понять проблему, потом выбрать инструмент.
[04] Держать бизнес-логику понятной.
[05] Считать денежные операции критическими.
[06] Документировать важные решения.
[07] Не создавать пустые папки и лишнюю архитектуру заранее.
[08] Строить проект как реальную backend-систему, а не как игрушечный tutorial.


11. ТЕКУЩИЙ СТАТУС
------------------

Текущий релиз:

    v0.1 - Архитектура и документация

Текущий фокус:

[01] Видение проекта
[02] Банковская предметная область
[03] Документация
[04] Архитектурные решения
[05] Будущий дизайн API
[06] Будущая модель базы данных


12. ЛИЦЕНЗИЯ
------------

Проект распространяется по лицензии MIT.
