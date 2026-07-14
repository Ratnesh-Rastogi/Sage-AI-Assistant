# API Documentation — Phase 1 + 2

Base URL: `http://localhost:8000/api/v1`

Health and chat endpoints are live. Memory, notes, tasks, reminders, and
file endpoints are added in later phases (see `CLAUDE_BUILD_PROMPT.md` for
the phase plan); their route modules already exist as placeholders under
`backend/app/api/routes/` but are not yet wired into the application.

## `POST /api/v1/chat`

Sends a message to Sage and returns the Agent Runtime's response. Runs the
full pipeline: Intent Analyzer → Planner → Execution Manager (tools) →
Context Builder → Memory Manager (read-only in Phase 2) → Provider →
Response Validator → Response Formatter, persisting both the user and
assistant messages either way.

**Request**
```json
{
  "message": "What is polymorphism?",
  "conversation_id": null,
  "provider": null,
  "debug": false
}
```

| Field             | Type            | Required | Notes                                                             |
|-------------------|-----------------|----------|--------------------------------------------------------------------|
| `message`         | string          | yes      | 1–8000 characters                                                  |
| `conversation_id` | UUID or null    | no       | Omit/null to start a new conversation                              |
| `provider`        | string or null  | no       | Override `DEFAULT_AI_PROVIDER` for this call: `gemini`\|`openai`\|`claude`\|`openrouter` |
| `debug`           | boolean         | no       | Include the internal reasoning trace in the response (Section 30)  |

**Response `200`**
```json
{
  "response": "Polymorphism means...",
  "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "tools_used": [],
  "trace": null
}
```

With `"debug": true`, `trace` is populated instead of `null`:
```json
{
  "trace": {
    "intents": ["question_answering"],
    "tools_used": [],
    "unavailable_capabilities": [],
    "warnings": [],
    "provider": "gemini",
    "model": "gemini-2.0-flash"
  }
}
```

**Response `422`** — validation error (empty/missing `message`, body isn't valid JSON, etc.), FastAPI's standard error shape.

**Response `400`** — application error (e.g. `conversation_id` doesn't exist), using the standard error envelope below.

Notes:
- If the requested intent needs a tool that isn't registered yet (Phase 2
  ships only a `system_time` reference tool — real tools arrive in Phases
  4–5), the response says so honestly rather than fabricating the action;
  check `trace.unavailable_capabilities` with `debug: true` to see exactly
  which capability was missing.
- Streaming (`WS /chat/stream`) isn't implemented yet — that's Phase 6.

## `GET /api/v1/health`

Liveness check. Does not touch the database.

**Response `200`**
```json
{
  "status": "ok",
  "service": "sage-backend"
}
```

## `GET /api/v1/health/db`

Readiness check. Verifies the PostgreSQL connection.

**Response `200` (connected)**
```json
{
  "status": "ok",
  "database": "connected"
}
```

**Response `200` (unreachable)**
```json
{
  "status": "error",
  "database": "unreachable",
  "detail": "..."
}
```

## Error format

All application-raised errors follow this envelope (Section 101 of the
blueprint):

```json
{
  "success": false,
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Connection refused"
  }
}
```

Relevant error codes introduced in Phase 2: `PROVIDER_ERROR` (provider
misconfigured or unreachable), `NOT_FOUND` (unknown `conversation_id`),
`VALIDATION_ERROR` (invalid message role — internal, shouldn't surface from
the API directly).

## Interactive docs

FastAPI serves auto-generated OpenAPI docs while the backend is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
