-- Initial database setup for Sage.
-- pgvector is enabled ahead of time since SAGE_BLUEPRINT.md Sections 42 and 141
-- identify it as the planned future engine for semantic memory/document search.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";
