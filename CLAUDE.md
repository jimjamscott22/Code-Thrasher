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
uv run pytest       # use if pytest is not on PATH; uv creates/uses server/.venv
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

To rebuild only the production frontend image after changing `client/` files:

```bash
docker compose build --no-cache client
docker compose up -d --no-deps --force-recreate client
```

## Architecture

### Code Execution Flow

**Authoritative grading happens on the server.** Client-side Pyodide is for preview feedback on visible tests only.

1. `client/src/services/pyodide.ts` — Web Worker loads Pyodide from CDN; runs visible test cases for local stdout preview
2. `ExerciseDetail.tsx` — posts `code` + `exercise_id` to `POST /api/v1/submit/` (no client-reported scores)
3. `server/app/services/grading.py` — loads all test cases from DB (including hidden), runs each via `sandbox.py`
4. `server/app/services/sandbox.py` — subprocess runner enforcing `SANDBOX_*` limits from `app/core/config.py`
5. `server/app/api/v1/endpoints/submit.py` — persists `Submission` with server-computed score and updates user stats

Hidden test `expected_output` is never sent to the client (`TestCasePublicOut` in exercise detail responses).

### Backend Structure

- `app/main.py` — FastAPI app, configurable CORS (`CORS_ORIGINS`), rate limiting via slowapi, security + CSP headers
- `app/services/` — grading, sandbox, exercises, progress, user_stats business logic
- `app/core/config.py` — `Settings` loaded from `.env` via pydantic-settings
- `app/db/database.py` — async SQLAlchemy engine + `get_db` dependency
- `app/models/models.py` — ORM models: `User`, `Category`, `Exercise`, `TestCase`, `Submission`
- `app/schemas/schemas.py` — Pydantic v2 request/response schemas
- `app/api/v1/endpoints/` — routers: `auth`, `exercises`, `submit`, `progress`
- `app/api/v1/endpoints/exercises.py` — exercise list/detail plus explicit `GET /exercises/{id}/solution`; default detail responses include `guide` + `has_solution`, never solution text
- `alembic/` — migration history; `alembic.ini` points to `server/` as base dir

JWT auth is required for submit, progress, and solution reveal. `POST /exercises/` requires an admin user (`is_admin` on `User`). Browse endpoints remain public.

### Frontend Structure

- `src/App.tsx` — two routes: `/` (Dashboard) and `/exercise/:id` (ExerciseDetail)
- `src/api/client.ts` — Axios instance with `baseURL: "/api/v1"` (proxied by Vite)
- `src/store/useProgressStore.ts` — Zustand store, fetches `GET /progress/` to track completion
- `src/services/pyodide.ts` — singleton Pyodide loader; first call downloads ~10 MB
- `src/components/editor/CodeEditor.tsx` — Monaco Editor wrapper
- `src/components/exercise/ExerciseGuidePanel.tsx` — progressive guide cards, snippets, and deliberate solution reveal without overwriting editor code

### Data Model

`Exercise` has many `TestCase`s. Each `TestCase` has `input_data`, `expected_output`, `score_weight`, and `is_hidden`. Submissions store the final `score` (0–100) and `status` (`completed` = 100, `failed` = anything less).

`Exercise` keeps legacy `hint`, plus structured `guide` JSON and optional `solution_code` / `solution_explanation`; expose answers only through the solution reveal endpoint.

## Key Constraints

- **Vite proxy**: The `vite.config.ts` proxies `/api` to `http://localhost:8000`. CORS origins default to `http://localhost:5173` via `CORS_ORIGINS` in `.env`.
- **Pyodide CSP**: Pyodide needs `'wasm-unsafe-eval'` in `script-src` for WebAssembly instantiation. Monaco may load `data:` fonts, so keep `font-src` aligned too. CSP is defined in `client/index.html`, `client/vite.config.ts`, `client/nginx.conf`, and `server/app/main.py`; update all four together.
- **Test isolation**: `server/tests/conftest.py` overrides `get_db` with an async SQLite session; every test gets a fresh schema via `autouse` fixture.
- **`asyncio_mode = "auto"`** is set in `pyproject.toml` — all test functions can be `async def` without decorators.
- **Guidance reveal**: `GET /exercises/{id}/solution` requires JWT; reveals are tracked in `solution_reveals`.
- **Frontend validation**: `npm run lint` requires `client/.eslintrc.cjs`; `npm run build` may emit TypeScript build artifacts if not ignored/cleaned.
