# CoreBank Database Design

This document describes the planned database model for the CoreBank project.

The database model starts simple and will evolve together with the project.
The first goal is not to design a perfect banking database. The first goal
is to define clear entities, relationships and rules that protect money
operations from incorrect behavior.

PostgreSQL will be the main database and the source of truth.

---

# 1. Database Goals

The CoreBank database must provide:

- reliable data storage
- clear relationships between entities
- transaction-safe money operations
- operation history
- audit trail
- data consistency
- support for future API, workers and analytics

The most important rule:

```text
Money must not move without a recorded reason.
```

Any balance change must be connected to a business operation and transaction
history.

---

# 2. Source of Truth

PostgreSQL is the source of truth for CoreBank.

This means:

- users are stored in PostgreSQL
- accounts are stored in PostgreSQL
- cards are stored in PostgreSQL
- balances are stored in PostgreSQL
- transfers are stored in PostgreSQL
- transaction history is stored in PostgreSQL
- audit events are stored in PostgreSQL

Redis can be added later for caching, but Redis must not become the source
of truth for critical banking data.

RabbitMQ can be added later for asynchronous processing, but RabbitMQ must
not be required to complete the critical money movement itself.

---

# 3. Main Domain Entities

CoreBank uses the following main domain entities:

- User
- Account
- Card
- Transfer
- Transaction
- AuditEvent
- Notification
- AnalyticsEvent

The first database version will focus on the core banking model:

- users
- accounts
- cards
- transfers
- transactions
- audit_events

Notification and analytics tables can be added later when workers appear.

---

# 4. User

A user represents a person who uses the banking system.

A user can have multiple accounts.

Planned table:

```text
users
```

Planned fields:

```text
id
email
phone
first_name
last_name
status
created_at
updated_at
```

Field meaning:

- id
  - internal unique user identifier

- email
  - user email
  - should be unique if used for login or identification

- phone
  - user phone number
  - can be unique if used for login or notifications

- first_name
  - user first name

- last_name
  - user last name

- status
  - current user status
  - example values: active, blocked, deleted

- created_at
  - record creation timestamp

- updated_at
  - last update timestamp

Important rules:

- user id must be stable
- active user can own accounts
- blocked user should not be able to perform transfers
- deleted user should usually not be physically removed if financial history exists

Possible statuses:

```text
active
blocked
deleted
```

---

# 5. Account

An account represents a bank account owned by a user.

A user can have multiple accounts.

Planned table:

```text
accounts
```

Planned fields:

```text
id
user_id
account_number
currency
balance
status
created_at
updated_at
```

Field meaning:

- id
  - internal unique account identifier

- user_id
  - reference to users.id

- account_number
  - human-readable account number
  - should be unique

- currency
  - account currency
  - example values: RUB, USD, EUR

- balance
  - current account balance
  - should be stored as integer minor units or decimal with strict precision

- status
  - current account status
  - example values: active, blocked, closed

- created_at
  - record creation timestamp

- updated_at
  - last update timestamp

Important rules:

- account belongs to exactly one user
- account number must be unique
- account balance must not be negative in the first version
- account balance must not change without transaction records
- closed account should not participate in new transfers
- blocked account should not send money

Possible statuses:

```text
active
blocked
closed
```

Currency rule:

```text
In the first version, transfers are allowed only between accounts with the
same currency.
```

Why:

Currency conversion adds extra complexity:

- exchange rates
- conversion fees
- rounding
- rate history
- legal and financial rules

This can be added later as a separate feature.

---

# 6. Card

A card represents a payment card linked to an account.

One account can have multiple cards.

Planned table:

```text
cards
```

Planned fields:

```text
id
account_id
card_number_masked
card_type
status
created_at
updated_at
```

Field meaning:

- id
  - internal unique card identifier

- account_id
  - reference to accounts.id

- card_number_masked
  - masked card number
  - example: 5555 **** **** 1234

- card_type
  - type of card
  - example values: debit, virtual

- status
  - current card status
  - example values: active, blocked, expired, closed

- created_at
  - record creation timestamp

- updated_at
  - last update timestamp

Important rules:

- card belongs to exactly one account
- card must not store full raw card number in this project
- blocked card should not be used for operations
- closed card should not be reactivated without a separate business decision

Possible statuses:

```text
active
blocked
expired
closed
```

Security note:

This project must not store real card numbers, CVV codes or sensitive card
data.

Only masked or fake test card data should be used.

---

# 7. Transfer

A transfer is a business operation that moves money from one account to
another account.

A transfer is what the user wants to do.

Planned table:

```text
transfers
```

Planned fields:

```text
id
source_account_id
destination_account_id
amount
currency
status
idempotency_key
description
created_at
updated_at
completed_at
failed_reason
```

Field meaning:

- id
  - internal unique transfer identifier

- source_account_id
  - account from which money is withdrawn

- destination_account_id
  - account to which money is deposited

- amount
  - transfer amount

- currency
  - transfer currency

- status
  - current transfer status

- idempotency_key
  - unique key that protects from duplicate transfer execution

- description
  - optional user-visible transfer description

- created_at
  - transfer creation timestamp

- updated_at
  - last update timestamp

- completed_at
  - timestamp when transfer was completed

- failed_reason
  - reason why transfer failed, if it failed

Possible statuses:

```text
pending
completed
failed
cancelled
```

Important rules:

- source account and destination account must be different
- source account must exist
- destination account must exist
- source account must be active
- destination account must be active
- source and destination accounts must have the same currency in the first version
- amount must be greater than zero
- source account must have enough money
- transfer must be executed atomically
- same idempotency key must not execute transfer twice
- completed transfer must not be completed again

---

# 8. Transaction

A transaction is a technical record of money movement.

A transfer usually creates two transaction records:

- debit transaction for the source account
- credit transaction for the destination account

Transfer answers the question:

```text
What business operation happened?
```

Transaction answers the question:

```text
How exactly did money move in account history?
```

Planned table:

```text
transactions
```

Planned fields:

```text
id
transfer_id
account_id
type
amount
currency
balance_before
balance_after
created_at
```

Field meaning:

- id
  - internal unique transaction identifier

- transfer_id
  - reference to transfers.id

- account_id
  - account affected by this transaction

- type
  - transaction type
  - example values: debit, credit

- amount
  - transaction amount

- currency
  - transaction currency

- balance_before
  - account balance before this transaction

- balance_after
  - account balance after this transaction

- created_at
  - transaction creation timestamp

Possible types:

```text
debit
credit
```

Important rules:

- transaction must belong to an account
- transaction should usually belong to a transfer
- transaction amount must be greater than zero
- debit decreases balance
- credit increases balance
- balance_before and balance_after must reflect real balance change
- transaction records must not be edited after creation
- transaction history is append-only

Example:

A transfer of 100 RUB from Account A to Account B creates:

```text
Transfer:
  amount = 100 RUB
  status = completed

Transaction 1:
  account = Account A
  type = debit
  amount = 100 RUB

Transaction 2:
  account = Account B
  type = credit
  amount = 100 RUB
```

This allows the system to show account history and investigate money movement.

---

# 9. Audit Event

An audit event records important actions in the system.

Audit is not the same as transaction history.

Transaction history explains money movement.

Audit history explains important system actions.

Planned table:

```text
audit_events
```

Planned fields:

```text
id
user_id
event_type
entity_type
entity_id
payload
created_at
```

Field meaning:

- id
  - internal unique audit event identifier

- user_id
  - user who caused the action, if known

- event_type
  - type of action

- entity_type
  - type of entity affected by the action

- entity_id
  - id of affected entity

- payload
  - additional event data in JSON format

- created_at
  - event creation timestamp

Possible event types:

```text
user_created
account_created
card_created
transfer_created
transfer_completed
transfer_failed
account_blocked
card_blocked
```

Important rules:

- important actions should create audit events
- audit events should be append-only
- audit events should not be silently deleted
- audit event payload should not contain secrets
- audit events help investigate what happened in the system

---

# 10. First Relationship Model

Planned relationships:

```text
User 1 ---- N Account

Account 1 ---- N Card

Account 1 ---- N Transaction

Transfer 1 ---- N Transaction

User 1 ---- N AuditEvent
```

Meaning:

- one user can have many accounts
- one account can have many cards
- one account can have many transactions
- one transfer can create multiple transactions
- one user can cause many audit events

---

# 11. Transfer Execution Model

Transfer execution should happen inside one database transaction.

Planned flow:

```text
Start database transaction

  1. Find source account
  2. Find destination account
  3. Lock both accounts for update
  4. Check account statuses
  5. Check currency
  6. Check amount
  7. Check source balance
  8. Create transfer record
  9. Decrease source account balance
  10. Increase destination account balance
  11. Create debit transaction
  12. Create credit transaction
  13. Create audit event
  14. Mark transfer as completed

Commit database transaction
```

If any step fails:

```text
Rollback database transaction
```

This protects the system from partial money movement.

Example of a dangerous partial operation:

```text
source account decreased
destination account not increased
```

This must never happen.

---

# 12. Account Locking

When two transfers try to change the same account at the same time, the
system must avoid race conditions.

Example problem:

```text
Account balance = 100

Transfer A wants to send 80
Transfer B wants to send 80
```

If both transfers read the balance at the same time, both may think there is
enough money.

Incorrect result:

```text
Transfer A completed
Transfer B completed
Final balance = -60
```

This is wrong for the first version.

To prevent this, the database should lock account rows during transfer
execution.

Planned approach:

```text
SELECT accounts FOR UPDATE
```

This means that while one transaction is changing the account, another
transaction must wait.

Important rule:

```text
Balance check and balance update must happen inside the same database
transaction.
```

---

# 13. Idempotency

Idempotency protects the system from duplicate operations.

Example problem:

```text
User clicks "Send" button
Network timeout happens
User clicks "Send" again
```

Without idempotency, the same transfer may be executed twice.

Planned solution:

The client sends an idempotency key with transfer request.

Example:

```text
Idempotency-Key: 7f7b6e9a-1b4b-42b4-90a9-8fd45b0d85c2
```

The system stores this key in the transfers table.

Important rule:

```text
The same idempotency key must not create two completed transfers.
```

Possible behavior:

- if the key is new, create and execute transfer
- if the key already exists, return previous transfer result
- if the key exists with failed status, decide behavior explicitly later

Planned database constraint:

```text
unique(idempotency_key)
```

In the future, idempotency may also include user_id to avoid conflicts
between users:

```text
unique(user_id, idempotency_key)
```

---

# 14. Balance Storage Strategy

In the first version, account balance is stored in the accounts table.

```text
accounts.balance
```

This makes reads simple.

But balance correctness must be protected by transaction history.

Important rule:

```text
accounts.balance and transactions history must not contradict each other.
```

Possible future improvement:

- calculate balance from transaction history
- store current balance as optimized snapshot
- periodically verify balance consistency

For the first version, stored balance is acceptable because it is easier to
understand and implement.

But every balance update must be done carefully.

---

# 15. Amount Type

Money should not be stored as floating-point number.

Bad idea:

```text
float
double
```

Reason:

Floating-point numbers can produce precision errors.

Preferred options:

```text
integer minor units
numeric with strict precision
```

Examples:

Option 1:

```text
amount_minor_units = 1050
currency = RUB
```

This means:

```text
10.50 RUB
```

Option 2:

```text
amount = numeric(18, 2)
currency = RUB
```

For this project, the planned approach is:

```text
numeric(18, 2)
```

Reason:

- easy to read
- easy to understand
- good enough for educational project
- supported by PostgreSQL

Important rule:

```text
Do not use float or double for money.
```

---

# 16. Planned Constraints

Planned database constraints:

users:

- email should be unique
- status should be from allowed values
- created_at should not be null

accounts:

- user_id should reference users.id
- account_number should be unique
- balance should be greater than or equal to zero
- currency should not be empty
- status should be from allowed values

cards:

- account_id should reference accounts.id
- card_number_masked should not contain full real card number
- status should be from allowed values

transfers:

- source_account_id should reference accounts.id
- destination_account_id should reference accounts.id
- source_account_id should not equal destination_account_id
- amount should be greater than zero
- idempotency_key should be unique
- status should be from allowed values

transactions:

- transfer_id should reference transfers.id
- account_id should reference accounts.id
- amount should be greater than zero
- type should be from allowed values
- balance_before should not be null
- balance_after should not be null

audit_events:

- event_type should not be empty
- entity_type should not be empty
- created_at should not be null

---

# 17. Planned Indexes

Indexes will be added for common queries.

Planned indexes:

users:

- email

accounts:

- user_id
- account_number

cards:

- account_id

transfers:

- source_account_id
- destination_account_id
- idempotency_key
- created_at
- status

transactions:

- account_id
- transfer_id
- created_at

audit_events:

- user_id
- entity_type, entity_id
- created_at

Indexes should be added when there is a clear query pattern.

Important rule:

```text
Do not add random indexes without understanding queries.
```

Indexes speed up reads, but they also add cost to writes.

---

# 18. First Planned API Use Cases Supported by Database

The first database model should support these use cases:

- create user
- create account for user
- create card for account
- get user accounts
- get account balance
- get account transaction history
- transfer money between accounts
- get transfer status
- record audit events

These use cases are enough for the first serious version of CoreBank.

---

# 19. What Is Intentionally Not Included Yet

The first database version does not include:

- real authentication tables
- password storage
- external payment systems
- currency exchange
- overdraft
- credit products
- loans
- deposits
- real card processing
- PCI DSS logic
- fraud detection
- complex limits
- multi-bank settlement
- chargebacks

These features are intentionally excluded to keep the first version focused.

The first goal is to understand the core model:

```text
User -> Account -> Transfer -> Transaction history
```

---

# 20. Current Status

Current release:

```text
v0.1 - Architecture and Documentation
```

Current database status:

- database is not implemented yet
- PostgreSQL is planned for release v0.3
- entities are being designed
- constraints are being defined
- first API use cases are being prepared

Next steps:

- define first API endpoints in docs/api.md
- record engineering decisions in docs/decisions.md
- create first ADR about project structure and architecture approach
