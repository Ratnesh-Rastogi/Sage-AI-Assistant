# Sage — Personal AI Assistant

Sage is a privacy-first, self-hosted personal AI assistant: long-term memory,
multi-step agent planning, tool execution, web research, scam detection,
document understanding, productivity management, and professional writing
assistance — all running locally, under the user's control.

Full specification: [`docs/SAGE_BLUEPRINT.md`](docs/SAGE_BLUEPRINT.md).

> **Status: Phase 1 — Foundation.** This repository currently contains the
> repository structure, backend skeleton, frontend skeleton, PostgreSQL
> integration, Docker configuration, environment configuration, and logging
> system. The AI agent, memory, tools, and full chat UI arrive in later
> phases per `docs/CLAUDE_BUILD_PROMPT.md`.

## Features (target, full Version 1)

- Natural conversations with long-term memory
- Multi-step agent planning and automatic tool selection
- Web research with citations (Tavily)
- Scam detection for URLs, emails, job offers, and messages
- Document understanding (PDF, DOCX, TXT, CSV, XLSX, images)
- Notes, tasks, and reminders
- Professional email drafting
- Daily briefings
- Multi-provider AI support (Gemini, OpenAI, Claude, OpenRouter)

## What's working right now (Phase 1)

- FastAPI backend that starts and serves `/api/v1/health` and `/api/v1/health/db`
- React + TypeScript + Tailwind frontend shell that reports backend/database status
- PostgreSQL via Docker Compose, with Alembic migrations (`users` table)
- Structured logging with daily rotation
- Environment-based configuration (no hardcoded secrets)
- Unit tests for backend (pytest) and frontend (Vitest), plus integration and
  e2e test scaffolding

## Technology stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Backend    | Python 3.12, FastAPI                     |
| Frontend   | React, TypeScript, TailwindCSS, Vite     |
| Database   | PostgreSQL 16, SQLAlchemy 2.x, Alembic   |
| Scheduler  | APScheduler (from Phase 4)               |
| AI         | Gemini / OpenAI / Claude / OpenRouter (from Phase 2) |
| Search     | Tavily (from Phase 5)                    |
| Deployment | Docker, Docker Compose                   |

## Installation

```bash
git clone <this-repo>
cd sage
cp .env.example .env
# edit .env with a real POSTGRES_PASSWORD and (later) provider API keys
```

## Configuration

All configuration lives in `.env` (never committed — see `.env.example` for
the full list of variables). At minimum for Phase 1 you need:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `DATABASE_URL` (defaults to the values above, pointed at the `postgres` service)

## Running locally (Docker)

```bash
docker compose up --build
```

This starts:

- `postgres` on `localhost:5432`
- `backend` (FastAPI) on `localhost:8000`
- `frontend` (nginx-served React build) on `localhost:5173`

Then open `http://localhost:5173` — you should see both services reported
as online.

Redis is optional and not started by default:

```bash
docker compose --profile with-redis up --build
```

### Applying database migrations

```bash
docker compose exec backend alembic upgrade head
```

## Running locally (without Docker)

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```
Settings load `.env` from the repo root automatically, whether you run
`uvicorn` from `backend/` (as above) or from the repo root — no need to
copy or symlink it.

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
The dev server proxies `/api` to `http://localhost:8000`, so this works
whether the backend above is a local `uvicorn` process or a Compose
container (Compose publishes it to `localhost:8000` on the host either way).

## Testing

```bash
cd backend && pytest         # backend unit tests
cd frontend && npm test      # frontend unit tests
cd frontend && npm run test:e2e   # e2e tests (requires the full stack running)
```

See [`tests/README.md`](tests/README.md) for integration and e2e tests.

## Documentation

- [`docs/SAGE_BLUEPRINT.md`](docs/SAGE_BLUEPRINT.md) — full product & architecture spec (frozen)
- [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md) — folder structure reference
- [`docs/CLAUDE_BUILD_PROMPT.md`](docs/CLAUDE_BUILD_PROMPT.md) — phase-by-phase build instructions
- [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) — current API reference
- [`docs/DEVELOPMENT_GUIDE.md`](docs/DEVELOPMENT_GUIDE.md) — how to extend Sage

## Usage examples (future phases)

Once later phases land, Sage will understand things like:

```
"Remember that I prefer detailed explanations."
"Create a task to finish my portfolio, high priority, due Friday."
"Is this website legitimate? https://example.com"
"Search for GATE scholarships and save the important ones as notes."
```

## Future improvements

Explicitly out of scope for Version 1 (Section 3): voice interaction, mobile
app, multi-user support, authentication, cloud sync, browser extension,
automatic email sending, autonomous browsing, social media integrations.

## License

See [`LICENSE`](LICENSE).
