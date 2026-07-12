# Development Guide

## Folder structure

The layout is frozen by `SAGE_BLUEPRINT.md` Section 15 and mirrored in
`PROJECT_STRUCTURE.md`. The short version:

```
sage/
├── backend/app/
│   ├── main.py         # FastAPI entry point — no business logic here
│   ├── api/            # Routes + DI dependencies
│   ├── core/           # Exceptions, constants
│   ├── config/         # Pydantic Settings
│   ├── database/       # Engine, session, Alembic migrations
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic request/response models (Phase 2+)
│   ├── repositories/   # DB access — the only layer allowed to query Postgres
│   ├── services/       # Business logic (Phase 2+)
│   ├── agent/          # Planner, runtime, context, execution (Phase 2)
│   ├── tools/           # Individual tools (Phase 5)
│   ├── providers/      # LLM provider adapters (Phase 2)
│   ├── memory/         # Long-term memory (Phase 3)
│   ├── scheduler/      # APScheduler jobs (Phase 4)
│   ├── logging/        # Structured logging setup
│   ├── utils/
│   └── tests/          # Unit tests
├── frontend/src/        # React + TypeScript + Tailwind
├── database/            # Seeds, backups (migrations live in backend/app/database/migrations)
├── docker/              # Per-service Dockerfiles + nginx/postgres config
├── docs/
├── storage/files/       # Uploaded file storage (Phase 5)
└── tests/               # Integration + E2E tests
```

Dependencies must always point downward: Frontend → API → Agent → Tools →
Database. Never the reverse (Section 16).

## Adding a new tool (Phase 5+)

Per Section 51/62:

1. Implement the tool under `backend/app/tools/<tool_name>/` with `tool.py`,
   `schemas.py`, `service.py`, and `tests/`.
2. Register its capability manifest in the Tool Registry.
3. Write unit tests (valid input, invalid input, failure, edge cases).

No changes to the Planner should be required.

## Adding a new API route

1. Add the route module under `backend/app/api/routes/`.
2. Keep it thin — validate input, call a service, format the response. No
   direct database or provider calls (Section 91).
3. Register the router in `backend/app/main.py`.
4. Add tests in `backend/app/tests/`.

## Database migrations

Migrations are managed with Alembic from inside `backend/`:

```bash
cd backend
alembic revision --autogenerate -m "add notes table"
alembic upgrade head
```

Never modify the database schema directly in production (Section 64).

## Running tests

See `tests/README.md` for the full breakdown of unit vs. integration vs. e2e.

```bash
cd backend && pytest        # backend unit tests
cd frontend && npm test     # frontend unit tests
```

## Code style

- Backend: type-annotated Python, one responsibility per module, repository
  pattern for all DB access, dependency injection via FastAPI `Depends`.
- Frontend: components stay presentation-only; all API calls go through
  `src/services/*.ts`.
