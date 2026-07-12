# API Documentation — Phase 1 (Foundation)

Base URL: `http://localhost:8000/api/v1`

Only foundation endpoints exist in Phase 1. Chat, memory, notes, tasks,
reminders, and file endpoints are added in later phases (see
`CLAUDE_BUILD_PROMPT.md` for the phase plan); their route modules already
exist as placeholders under `backend/app/api/routes/` but are not yet wired
into the application.

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

## Interactive docs

FastAPI serves auto-generated OpenAPI docs while the backend is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
