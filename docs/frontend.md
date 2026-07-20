# CoreBank Frontend

## Current state

The backend exposes authentication and user-scoped banking endpoints. Accounts
belong to users, outgoing transfers require ownership of the source account,
and transaction history is limited to operations involving the current user's
accounts. Cards do not exist in the domain yet.

## Stack

- React for component-based UI
- TypeScript for API contract safety
- Vite for a small and fast development setup
- Plain CSS for the initial design system
- Native `fetch` for the small current API surface
- Nginx for serving the production build and proxying `/api` to FastAPI
- React Router for public and protected application routes

This keeps the first version compact. TanStack Query and a form library can be
introduced when the application gains more server state and complex forms.

## Implemented

- responsive landing page
- login and registration modes
- client-side form constraints matching FastAPI schemas
- automatic login after registration
- readable mapping for API authentication errors
- persisted bearer session and restoration through `GET /auth/me`
- signed-in state and logout
- Vite development proxy and Nginx production proxy
- Docker Compose web service
- protected `/dashboard` route
- responsive dashboard shell and navigation
- real account balances grouped by currency
- user-scoped account and transaction loading
- account opening in RUB, USD, or EUR
- recent incoming and outgoing transfer history
- guided outgoing transfer flow with client-side validation and confirmation
- recipient lookup by formatted phone number or 16-digit transfer number
- localized business errors and refreshed balances after a successful transfer
- component tests for login, account opening, and transfers
- registration with a unique normalized phone number
- profile prompt for existing users to add a searchable phone number
- Secure HttpOnly cookie sessions with automatic CSRF headers
- Playwright coverage for registration, session restoration, accounts, and transfers
- loading, empty, expired-session, and API error states

## Delivery plan

### 1. Authentication foundation

- Add the landing page and real auth flow (implemented).
- Use secure HttpOnly cookies for browser sessions (implemented).
- Add password recovery and email verification when backend support exists.

### 2. Authenticated application shell

- Add routing and protected routes (implemented).
- Build sidebar/header navigation and a mobile layout (implemented).
- Add a dashboard with balance summary and recent operations (implemented).
- Introduce generated TypeScript types from the OpenAPI schema.

### 3. User-owned banking data

- Add ownership relations and authorization checks in the backend (implemented).
- Show only the current user's accounts (implemented).
- Add transaction history with loading and empty states (implemented).
- Add a dedicated account details route.

### 4. Transfers

- Build a guided transfer form with account selection and amount formatting
  (implemented).
- Add confirmation and a result state (implemented).
- Add backend idempotency support before enabling automatic retries (implemented).
- Add optimistic feedback only where money-operation semantics allow it.

### 5. Cards

- First implement the card model and user ownership in the backend.
- Add card list, details, masking, freeze/unfreeze controls, and limits.

### 6. Quality and production readiness

- Add component tests for authentication and transfers (implemented).
- Add browser-level end-to-end tests for the critical user journeys (implemented).
- Add accessibility checks, analytics, monitoring, and a strict CSP.
- Keep the committed dependency lockfile current and build the frontend in CI.
