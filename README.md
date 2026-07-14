# Sage — Personal AI Assistant

Sage is a privacy-first, self-hosted personal AI assistant: long-term memory,
multi-step agent planning, tool execution, web research, scam detection,
document understanding, productivity management, and professional writing
assistance — all running locally, under the user's control.

Full specification: [`docs/SAGE_BLUEPRINT.md`](docs/SAGE_BLUEPRINT.md).

> **Status: Phase 2 — AI Agent Core.** Foundation (Phase 1) plus the full
> agent runtime are now in place: intent analysis, planning, tool registry +
> execution, context building, multi-provider AI support, and conversation
> persistence, all wired to a working `POST /chat` endpoint. Long-term
> memory, productivity tools (notes/tasks/reminders), web search, scam
> detection, file processing, email drafting, and the full chat UI arrive in
> later phases per `docs/CLAUDE_BUILD_PROMPT.md`.

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

## What's working right now (Phase 1 + 2)

**Phase 1 — Foundation:**
- FastAPI backend that starts and serves `/api/v1/health` and `/api/v1/health/db`
- React + TypeScript + Tailwind frontend shell that reports backend/database status
- PostgreSQL via Docker Compose, with Alembic migrations
- Structured logging with daily rotation
- Environment-based configuration (no hardcoded secrets)

**Phase 2 — AI Agent Core:**
- `POST /api/v1/chat` — send a message, get a response, with conversation
  history persisted across turns
- **Intent Analyzer** — classifies messages into one or more intents
  (conversation, web search, note/task/reminder management, memory
  operations, email drafting, scam detection, file analysis)
- **Planner** — turns detected intent into an execution plan using the Tool
  Registry's capability-based discovery (never hardcodes tool names)
- **Execution Manager** — runs tool steps (parallel when independent),
  logs every execution to the `tool_executions` table, and treats failures
  as non-critical so one broken tool can't take down a response
- **Tool Registry** — capability-based tool discovery; ships with one
  reference tool (`system_time`) that proves the register → discover →
  execute pipeline end to end
- **Context Builder** — assembles the provider prompt from the current
  message, tool outputs, relevant memory, and recent conversation history,
  by priority
- **Provider Interface** — one abstraction over four adapters (Gemini,
  OpenAI, Claude, OpenRouter); switching providers is a config change, not a
  code change
- **Conversation Manager** — persists conversations and messages
  (`conversations`, `messages`, `conversation_summaries` tables)
- **Response Validator/Formatter** — rejects empty provider responses,
  flags unbalanced markdown, and keeps the internal reasoning trace hidden
  unless `debug: true` is requested
- Memory retrieval has a stable interface (`MemoryManager.retrieve_relevant`)
  that always returns `[]` for now — full persistence is Phase 3
- Unit tests for backend (pytest) and frontend (Vitest), plus integration
  and e2e test scaffolding

## Technology stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Backend    | Python 3.12, FastAPI                     |
| Frontend   | React, TypeScript, TailwindCSS, Vite     |
| Database   | PostgreSQL 16, SQLAlchemy 2.x, Alembic   |
| Scheduler  | APScheduler (from Phase 4)               |
| AI         | Gemini / OpenAI / Claude / OpenRouter — implemented in Phase 2 |
| Search     | Tavily (from Phase 5)                    |
| Deployment | Docker, Docker Compose                   |

## Installation

```bash
git clone <this-repo>
cd sage
cp .env.example .env
# edit .env with a real POSTGRES_PASSWORD, and at least one provider API key
# (GEMINI_API_KEY, OPENAI_API_KEY, CLAUDE_API_KEY, or OPENROUTER_API_KEY)
```

## Configuration

All configuration lives in `.env` (never committed — see `.env.example` for
the full list of variables). At minimum you need:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `DATABASE_URL` (defaults to the values above, pointed at the `postgres` service)
- `DEFAULT_AI_PROVIDER` (`gemini` | `openai` | `claude` | `openrouter`) and the
  matching `*_API_KEY` — required to actually get a response from `/chat`;
  everything else in the pipeline (intent analysis, planning, tool
  execution, persistence) runs without one

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
Runs both migrations: `0001` (users) and `0002` (conversations, messages,
conversation_summaries, tool_executions).

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

## Usage examples

**Works today**, via `POST /api/v1/chat`:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is polymorphism?"}'
```

The agent classifies intent, checks the Tool Registry, builds context from
conversation history, calls your configured provider, and persists both
messages — even for intents with no tool registered yet (e.g. "search for
X" gets a real response plus an honest note that web search isn't wired up
yet, rather than a fabricated answer).

**Future phases** will add real handling for:

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
