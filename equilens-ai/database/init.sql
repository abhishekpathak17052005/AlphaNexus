-- EquiLens AI – PostgreSQL Initialization Script
-- Runs once when the Docker postgres container is first created.
-- Enables required extensions for the EquiLens AI data platform.

-- pgvector: required for document chunk embeddings and semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- uuid-ossp: UUID generation (v4) for primary keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pg_trgm: fuzzy text search for company name/symbol search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- unaccent: accent-insensitive search (useful for Indian company names)
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Confirm
SELECT 'EquiLens AI database initialized with extensions: vector, uuid-ossp, pg_trgm, unaccent' AS status;
