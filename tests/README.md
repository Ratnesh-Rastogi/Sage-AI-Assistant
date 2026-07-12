# Tests

Sage keeps two kinds of tests in two places, matching PROJECT_STRUCTURE.md
Section 10 and SAGE_BLUEPRINT.md Section 106:

- **Unit tests** live next to the code they test:
  - Backend: `backend/app/tests/`
  - Frontend: `frontend/src/tests/`
  These run fast, without Docker, and are what `pytest` / `npm test` execute
  by default.

- **Cross-cutting tests** live here, at the repository root:
  - `tests/integration/` — exercises multiple layers together (e.g. API route
    through to a real PostgreSQL connection). Requires
    `docker compose up postgres`.
  - `tests/e2e/` — Playwright browser tests against the full running stack.
    Requires `docker compose up`.
  - `tests/backend/` and `tests/frontend/` are reserved for future
    cross-service test suites that don't belong to a single package.

## Running tests

```bash
# Backend unit tests
cd backend && pytest

# Frontend unit tests
cd frontend && npm test

# Integration tests (needs Postgres running)
docker compose up -d postgres
cd backend && pytest ../tests/integration

# End-to-end tests (needs the full stack running)
docker compose up -d
npx playwright test tests/e2e
```
