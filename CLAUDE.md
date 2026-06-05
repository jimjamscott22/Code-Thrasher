# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Code-Thrasher is a Python learning platform where users solve bite-sized coding challenges in a Monaco editor. Code execution happens **client-side in the browser via Pyodide** (WebAssembly Python), not server-side — the backend only records submission results that the client reports.

## Development Commands

### Backend (`server/`)

```bash
cd server

# Install all dependencies (including dev)
uv pip install -e ".[dev]"

# Start DB only (then run API locally)
docker compose -f ../docker-compose.yml up db -d

# Run API with live reload
uvicorn app.main:app --reload

# Apply migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "describe change"

# Seed exercises
python seed.py
```

Tests use an in-memory SQLite database (`aiosqlite`) — no running Postgres needed:

```bash
pytest              # all tests
pytest -v -x        # verbose, stop on first failure
pytest -k "test_name"
```

### Frontend (`client/`)

```bash
cd client
npm install
npm run dev         # Vite dev server at http://localhost:5173
npm run typecheck   # tsc --noEmit
npm run lint        # ESLint
npm run build       # type-check + Vite production build
```

### Full Stack (Docker)

```bash
docker compose up --build
# First run: docker compose exec api alembic upgrade head
```

## Architecture

### Code Execution Flow

The key non-obvious design: **user code runs in the browser**, not the server.

1. `client/src/services/pyodide.ts` — lazy-loads Pyodide (~10 MB) from CDN, runs Python in a fresh namespace via `exec()`, captures stdout/stderr
2. `ExerciseDetail.tsx` — runs each test case through Pyodide, compares output to `expected_output`, builds `TestCaseResult[]`
3. The frontend calls `POST /api/v1/submit/` with the pre-evaluated results (scores already computed)
4. `server/app/api/v1/endpoints/submit.py` — trusts the client's `test_results`, calculates final score, persists `Submission`

This means the server-side `SANDBOX_*` config settings in `app/core/config.py` are currently unused — there is no server-side execution.

### Backend Structure

- `app/main.py` — FastAPI app, CORS (localhost:5173 only), rate limiting via slowapi, security headers
- `app/core/config.py` — `Settings` loaded from `.env` via pydantic-settings
- `app/db/database.py` — async SQLAlchemy engine + `get_db` dependency
- `app/models/models.py` — ORM models: `User`, `Category`, `Exercise`, `TestCase`, `Submission`
- `app/schemas/schemas.py` — Pydantic v2 request/response schemas
- `app/api/v1/endpoints/` — three routers: `exercises`, `submit`, `progress`
- `alembic/` — migration history; `alembic.ini` points to `server/` as base dir

There is no auth middleware wired into endpoints yet — `user_id` on `Submission` is nullable and the submit endpoint does not require a JWT.

### Frontend Structure

- `src/App.tsx` — two routes: `/` (Dashboard) and `/exercise/:id` (ExerciseDetail)
- `src/api/client.ts` — Axios instance with `baseURL: "/api/v1"` (proxied by Vite)
- `src/store/useProgressStore.ts` — Zustand store, fetches `GET /progress/` to track completion
- `src/services/pyodide.ts` — singleton Pyodide loader; first call downloads ~10 MB
- `src/components/editor/CodeEditor.tsx` — Monaco Editor wrapper

### Data Model

`Exercise` has many `TestCase`s. Each `TestCase` has `input_data`, `expected_output`, `score_weight`, and `is_hidden`. Submissions store the final `score` (0–100) and `status` (`completed` = 100, `failed` = anything less).

## Key Constraints

- **Vite proxy**: The `vite.config.ts` proxies `/api` to `http://localhost:8000`. The CORS allow-list in `app/main.py` is hardcoded to `http://localhost:5173`.
- **Test isolation**: `server/tests/conftest.py` overrides `get_db` with an async SQLite session; every test gets a fresh schema via `autouse` fixture.
- **`asyncio_mode = "auto"`** is set in `pyproject.toml` — all test functions can be `async def` without decorators.
