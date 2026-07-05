# CoreBank API Design

This document describes the planned API contract for the CoreBank project.

The API will be implemented gradually. This document defines the direction,
main resources, planned endpoints and important behavior rules.

The first goal is not to create a large API. The first goal is to design a
clear and safe API for core banking operations.

---

# 1. API Goals

CoreBank API should provide:

- clear HTTP endpoints
- predictable request and response format
- safe money transfer behavior
- validation of input data
- useful error responses
- idempotent transfer creation
- access to users, accounts, cards and transactions
- foundation for future authentication and authorization

The API starts simple and grows step by step.

---

# 2. API Style

CoreBank will use REST-like HTTP API.

Main principles:

- resources are represented by nouns
- HTTP methods describe actions
- JSON is used for request and response bodies
- HTTP status codes describe result type
- errors have a consistent format
- critical operations use idempotency where needed

Examples of resources:

- users
- accounts
- cards
- transfers
- transactions
- audit events

---

# 3. Base URL

For local development:

```text
http://localhost:8000
```

Future Docker development:

```text
http://localhost:8000
```

Future Kubernetes development may use Ingress or port-forwarding.

---

# 4. Common Response Format

Successful responses should return JSON.

Example:

```json
{
  "id": "123",
  "status": "active"
}
```

For list responses:

```json
{
  "items": [],
  "total": 0
}
```

For error responses:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request data",
    "details": {}
  }
}
```

Common error fields:

- code
  - stable machine-readable error code

- message
  - human-readable explanation

- details
  - optional object with additional error context

---

# 5. Common HTTP Status Codes

Planned status codes:

- 200 OK
  - request completed successfully

- 201 Created
  - resource was created successfully

- 400 Bad Request
  - request is syntactically valid but contains invalid business data

- 401 Unauthorized
  - authentication is required

- 403 Forbidden
  - authenticated user has no permission for this action

- 404 Not Found
  - requested resource does not exist

- 409 Conflict
  - request conflicts with current state
  - example: duplicate idempotency key, blocked account, insufficient funds

- 422 Unprocessable Entity
  - request validation failed

- 500 Internal Server Error
  - unexpected server error

---

# 6. Versioning

The first API version will not use URL versioning immediately.

Initial endpoints:

```text
/health
/version
/users
/accounts
/cards
/transfers
/transactions
```

Possible future versioning:

```text
/api/v1/users
/api/v1/accounts
/api/v1/transfers
```

Versioning can be added when the API contract becomes more stable.

---

# 7. Health and Service Endpoints

## 7.1 GET /health

Checks that the API is alive.

Request:

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

Status code:

```text
200 OK
```

Purpose:

- used for local checks
- used by Docker healthchecks later
- used by Kubernetes probes later

---

## 7.2 GET /version

Returns service version and basic information.

Request:

```text
GET /version
```

Response:

```json
{
  "service": "corebank-api",
  "version": "0.1.0",
  "environment": "local"
}
```

Status code:

```text
200 OK
```

Purpose:

- verify which service version is running
- help during debugging
- help during deployment checks

---

# 8. Users API

Users represent clients of the banking system.

## 8.1 POST /users

Creates a new user.

Request:

```text
POST /users
Content-Type: application/json
```

Body:

```json
{
  "email": "user@example.com",
  "phone": "+79990000000",
  "first_name": "Ivan",
  "last_name": "Ivanov"
}
```

Response:

```json
{
  "id": "user_123",
  "email": "user@example.com",
  "phone": "+79990000000",
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "status": "active",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
201 Created
```

Validation rules:

- email must be valid
- email should be unique
- phone should be valid if provided
- first_name must not be empty
- last_name must not be empty

Possible errors:

- validation_error
- user_email_already_exists

---

## 8.2 GET /users/{user_id}

Returns user by id.

Request:

```text
GET /users/{user_id}
```

Response:

```json
{
  "id": "user_123",
  "email": "user@example.com",
  "phone": "+79990000000",
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "status": "active",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
200 OK
```

Possible errors:

- user_not_found

---

# 9. Accounts API

Accounts represent bank accounts owned by users.

## 9.1 POST /users/{user_id}/accounts

Creates a new account for user.

Request:

```text
POST /users/{user_id}/accounts
Content-Type: application/json
```

Body:

```json
{
  "currency": "RUB"
}
```

Response:

```json
{
  "id": "account_123",
  "user_id": "user_123",
  "account_number": "40817810000000000001",
  "currency": "RUB",
  "balance": "0.00",
  "status": "active",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
201 Created
```

Validation rules:

- user must exist
- user must be active
- currency must be supported

Possible errors:

- user_not_found
- user_blocked
- unsupported_currency

---

## 9.2 GET /users/{user_id}/accounts

Returns accounts owned by user.

Request:

```text
GET /users/{user_id}/accounts
```

Response:

```json
{
  "items": [
    {
      "id": "account_123",
      "account_number": "40817810000000000001",
      "currency": "RUB",
      "balance": "1000.00",
      "status": "active"
    }
  ],
  "total": 1
}
```

Status code:

```text
200 OK
```

Possible errors:

- user_not_found

---

## 9.3 GET /accounts/{account_id}

Returns account information.

Request:

```text
GET /accounts/{account_id}
```

Response:

```json
{
  "id": "account_123",
  "user_id": "user_123",
  "account_number": "40817810000000000001",
  "currency": "RUB",
  "balance": "1000.00",
  "status": "active",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
200 OK
```

Possible errors:

- account_not_found

---

# 10. Cards API

Cards represent payment cards linked to accounts.

This project does not store real card data.

Only masked fake test card data is allowed.

## 10.1 POST /accounts/{account_id}/cards

Creates a card for account.

Request:

```text
POST /accounts/{account_id}/cards
Content-Type: application/json
```

Body:

```json
{
  "card_type": "debit"
}
```

Response:

```json
{
  "id": "card_123",
  "account_id": "account_123",
  "card_number_masked": "5555 **** **** 1234",
  "card_type": "debit",
  "status": "active",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
201 Created
```

Validation rules:

- account must exist
- account must be active
- card_type must be supported

Possible errors:

- account_not_found
- account_blocked
- unsupported_card_type

---

## 10.2 GET /accounts/{account_id}/cards

Returns cards linked to account.

Request:

```text
GET /accounts/{account_id}/cards
```

Response:

```json
{
  "items": [
    {
      "id": "card_123",
      "card_number_masked": "5555 **** **** 1234",
      "card_type": "debit",
      "status": "active"
    }
  ],
  "total": 1
}
```

Status code:

```text
200 OK
```

Possible errors:

- account_not_found

---

# 11. Transfers API

Transfers are the most important part of CoreBank API.

A transfer moves money from one account to another account.

Transfer creation must be safe and idempotent.

---

## 11.1 POST /transfers

Creates and executes money transfer.

Request:

```text
POST /transfers
Content-Type: application/json
Idempotency-Key: 7f7b6e9a-1b4b-42b4-90a9-8fd45b0d85c2
```

Body:

```json
{
  "source_account_id": "account_123",
  "destination_account_id": "account_456",
  "amount": "100.00",
  "currency": "RUB",
  "description": "Test transfer"
}
```

Response:

```json
{
  "id": "transfer_123",
  "source_account_id": "account_123",
  "destination_account_id": "account_456",
  "amount": "100.00",
  "currency": "RUB",
  "status": "completed",
  "description": "Test transfer",
  "created_at": "2026-07-05T12:00:00Z",
  "completed_at": "2026-07-05T12:00:01Z"
}
```

Status code:

```text
201 Created
```

Validation rules:

- idempotency key is required
- source account must exist
- destination account must exist
- source account must not equal destination account
- source account must be active
- destination account must be active
- amount must be greater than zero
- currency must match source account currency
- currency must match destination account currency
- source account must have enough money

Possible errors:

- idempotency_key_required
- duplicate_idempotency_key
- source_account_not_found
- destination_account_not_found
- same_source_and_destination_account
- source_account_blocked
- destination_account_blocked
- unsupported_currency
- currency_mismatch
- insufficient_funds
- transfer_failed

Important behavior:

- same idempotency key must not execute transfer twice
- completed transfer must not be completed again
- failed transfer behavior must be explicitly documented before implementation
- balance changes must happen inside one database transaction
- transaction history must be created for both accounts

---

## 11.2 GET /transfers/{transfer_id}

Returns transfer by id.

Request:

```text
GET /transfers/{transfer_id}
```

Response:

```json
{
  "id": "transfer_123",
  "source_account_id": "account_123",
  "destination_account_id": "account_456",
  "amount": "100.00",
  "currency": "RUB",
  "status": "completed",
  "description": "Test transfer",
  "created_at": "2026-07-05T12:00:00Z",
  "completed_at": "2026-07-05T12:00:01Z"
}
```

Status code:

```text
200 OK
```

Possible errors:

- transfer_not_found

---

## 11.3 GET /accounts/{account_id}/transfers

Returns transfers related to account.

Request:

```text
GET /accounts/{account_id}/transfers
```

Response:

```json
{
  "items": [
    {
      "id": "transfer_123",
      "source_account_id": "account_123",
      "destination_account_id": "account_456",
      "amount": "100.00",
      "currency": "RUB",
      "status": "completed",
      "created_at": "2026-07-05T12:00:00Z"
    }
  ],
  "total": 1
}
```

Status code:

```text
200 OK
```

Possible errors:

- account_not_found

---

# 12. Transactions API

Transactions represent account history records.

A transfer usually creates two transactions:

- debit transaction for source account
- credit transaction for destination account

---

## 12.1 GET /accounts/{account_id}/transactions

Returns transaction history for account.

Request:

```text
GET /accounts/{account_id}/transactions
```

Response:

```json
{
  "items": [
    {
      "id": "transaction_123",
      "transfer_id": "transfer_123",
      "account_id": "account_123",
      "type": "debit",
      "amount": "100.00",
      "currency": "RUB",
      "balance_before": "1000.00",
      "balance_after": "900.00",
      "created_at": "2026-07-05T12:00:00Z"
    }
  ],
  "total": 1
}
```

Status code:

```text
200 OK
```

Possible errors:

- account_not_found

Important behavior:

- transaction history is append-only
- transaction records should not be edited
- every balance change must have a transaction record

---

## 12.2 GET /transactions/{transaction_id}

Returns one transaction by id.

Request:

```text
GET /transactions/{transaction_id}
```

Response:

```json
{
  "id": "transaction_123",
  "transfer_id": "transfer_123",
  "account_id": "account_123",
  "type": "debit",
  "amount": "100.00",
  "currency": "RUB",
  "balance_before": "1000.00",
  "balance_after": "900.00",
  "created_at": "2026-07-05T12:00:00Z"
}
```

Status code:

```text
200 OK
```

Possible errors:

- transaction_not_found

---

# 13. Audit API

Audit events are important for investigation and debugging.

In early versions, audit may not be exposed through public API.

It can be available as internal or admin endpoint later.

---

## 13.1 GET /audit-events

Returns audit events.

Request:

```text
GET /audit-events
```

Possible query parameters:

```text
user_id
entity_type
entity_id
event_type
from
to
limit
offset
```

Response:

```json
{
  "items": [
    {
      "id": "audit_123",
      "user_id": "user_123",
      "event_type": "transfer_completed",
      "entity_type": "transfer",
      "entity_id": "transfer_123",
      "created_at": "2026-07-05T12:00:00Z"
    }
  ],
  "total": 1
}
```

Status code:

```text
200 OK
```

Important note:

This endpoint should not be public in a real system.

It is planned for learning, debugging and admin-like scenarios.

---

# 14. Idempotency

Idempotency is required for transfer creation.

Reason:

A user or client can accidentally send the same request twice.

Example:

```text
Client sends transfer request
Network timeout happens
Client retries the same request
```

Without idempotency, the system may execute the same transfer twice.

Required header:

```text
Idempotency-Key: <unique-key>
```

Rules:

- idempotency key is required for POST /transfers
- same idempotency key must not execute the transfer twice
- if request with same key is repeated, API should return previous result
- idempotency key should be stored with transfer
- idempotency key should be unique

Possible future rule:

```text
unique(user_id, idempotency_key)
```

---

# 15. Pagination

List endpoints should support pagination.

Possible query parameters:

```text
limit
offset
```

Example:

```text
GET /accounts/{account_id}/transactions?limit=50&offset=0
```

Default behavior:

- default limit: 50
- max limit: 100
- default offset: 0

Example response:

```json
{
  "items": [],
  "total": 0,
  "limit": 50,
  "offset": 0
}
```

Pagination prevents large responses and protects the API from heavy queries.

---

# 16. Sorting

List endpoints may support sorting later.

Possible query parameter:

```text
sort
```

Examples:

```text
created_at_desc
created_at_asc
amount_desc
amount_asc
```

Initial version can start with default sorting:

```text
created_at_desc
```

---

# 17. Filtering

Some list endpoints should support filters.

Examples:

```text
GET /accounts/{account_id}/transactions?type=debit
GET /accounts/{account_id}/transfers?status=completed
GET /audit-events?event_type=transfer_completed
```

Filtering should be added only when needed by use cases.

---

# 18. Authentication and Authorization

Authentication is not part of the first implementation stage.

Reason:

The first stages focus on:

- API structure
- database model
- transfer correctness
- transaction safety
- Docker and infrastructure basics

Authentication will be added later.

Future authentication options:

- JWT access tokens
- refresh tokens
- user sessions
- internal service tokens

Future authorization rules:

- user can see only own accounts
- user can create transfer only from own account
- admin can inspect audit events
- workers can use internal access

Important note:

Even if authentication is not implemented at the beginning, API design should
not assume that every user can access everything forever.

---

# 19. Security Notes

CoreBank is an educational project, but it should still follow safe design
principles.

Rules:

- do not store real card numbers
- do not store CVV
- do not store real personal data in demo data
- do not expose secrets in responses
- do not put passwords or tokens into repository
- validate input data
- avoid returning internal stack traces to clients
- use environment variables for configuration
- use Docker secrets or Kubernetes secrets later where appropriate

---

# 20. Planned First Implementation Order

Recommended order for API implementation:

- GET /health
- GET /version
- POST /users
- GET /users/{user_id}
- POST /users/{user_id}/accounts
- GET /users/{user_id}/accounts
- GET /accounts/{account_id}
- POST /accounts/{account_id}/cards
- GET /accounts/{account_id}/cards
- POST /transfers
- GET /transfers/{transfer_id}
- GET /accounts/{account_id}/transactions

This order starts simple and gradually moves toward the most critical part:
money transfers.

---

# 21. Current Status

Current release:

```text
v0.1 - Architecture and Documentation
```

Current API status:

- API is not implemented yet
- first endpoints are planned
- request and response contracts are drafted
- transfer idempotency is required by design
- authentication is intentionally postponed

Next steps:

- record engineering decisions in docs/decisions.md
- create first ADR in docs/adr/
- after v0.1, start implementation with GET /health and GET /version
