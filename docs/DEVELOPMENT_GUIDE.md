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
│   ├── schemas/        # Pydantic request/response models
│   ├── repositories/   # DB access — the only layer allowed to query Postgres
│   ├── services/       # Business logic (ConversationService, UserService)
│   ├── agent/          # Planner, runtime, context, execution — Phase 2, done
│   ├── tools/          # Individual tools — mechanism done (Phase 2), real tools in Phase 5
│   ├── providers/      # LLM provider adapters — Phase 2, done
│   ├── memory/         # Long-term memory — interface stubbed (Phase 2), persistence in Phase 3
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

## Agent Runtime architecture (Phase 2)

`agent/runtime/agent.py`'s `AgentRuntime.handle_message()` is the pipeline
entry point (Section 19):

```
Intent Analyzer -> Planner -> Execution Manager -> Context Builder
-> Memory Manager (read) -> Provider Interface -> Response Validator
-> Response Formatter
```

Each stage is independently testable and swappable:

- **Intent Analyzer** (`agent/runtime/intent_analyzer.py`) — keyword-based
  for now; the interface (`analyze(message) -> IntentAnalysisResult`) can
  take an LLM-based implementation later without touching the Planner.
- **Planner** (`agent/planner/planner.py`) — maps each intent to a
  *capability* (e.g. `web_search`), asks the Tool Registry who satisfies it,
  and never hardcodes a tool name. Add a tool and the Planner's behavior
  changes automatically.
- **Execution Manager** (`agent/execution/tool_executor.py`) — the only
  component allowed to call `tool.execute()`. Runs independent tool steps
  with `asyncio.gather`, logs every execution to `tool_executions`, and
  never lets a broken tool crash the request.
- **Context Builder** (`agent/context/context_manager.py`) — assembles the
  provider prompt by priority (current message > tool results > memory >
  recent history).
- **Provider Interface** (`providers/`) — `providers/factory.get_provider()`
  is the only thing the runtime calls; it resolves `settings.DEFAULT_AI_PROVIDER`
  to a concrete adapter. `AgentRuntime(provider=...)` can also inject one
  directly, which is how tests avoid needing a real API key or network call.

## Adding a new AI provider

1. Implement `BaseProvider` (`providers/base.py`) in a new file under
   `providers/`, following the existing adapters' shape: a private
   `_build_request()` that raises `ProviderException` if its API key is
   missing, and a `generate()` that calls the API and normalizes the result
   into a `ProviderResponse`.
2. Register it in `providers/factory.py`'s `_REGISTRY` dict.
3. Add a settings field for its API key in `config/settings.py` and
   `.env.example`.
4. Write tests mirroring `tests/test_providers.py` — no real network calls;
   test `_build_request()`'s output directly.

No changes to `AgentRuntime` are required (Section 27).

## Adding a new tool

Per Section 51/62 (the `system_time` tool under `backend/app/tools/system_time/`
is a working reference example of every step below):

1. Implement the tool under `backend/app/tools/<tool_name>/` with `tool.py`
   (a `BaseTool` subclass + a manifest), `schemas.py`, `service.py`, and
   `tests/`.
2. Register it: add one line to `tools/bootstrap.py`'s `bootstrap_tools()`.
3. Write unit tests (valid input, invalid input, failure, edge cases, plus
   a registry-integration test).

No changes to the Planner or Execution Manager should be required — as
long as your tool's manifest declares the capability the Planner already
looks for (see `_INTENT_CAPABILITY_MAP` in `agent/planner/planner.py`).

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
