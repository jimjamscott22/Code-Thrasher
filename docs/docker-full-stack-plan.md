# Docker Full-Stack Containerization Plan

**Project:** Code-Thrasher  
**Goal:** Run the entire application (frontend, backend, and database) via Docker Compose with a single command.  
**Status:** Implemented. This document is retained as the original implementation plan and verification reference.

---

## 1. Current State

Today, Docker Compose runs **PostgreSQL** and the **FastAPI API** only. The React frontend is started separately on the host with `npm run dev`.

| Service | Containerized? | Notes |
| --- | --- | --- |
| `db` | Yes | PostgreSQL 16 (`docker-compose.yml`) |
| `api` | Yes | Built from `server/Dockerfile`; bind-mounts `./server` with `--reload` (dev-oriented) |
| `client` | No | Vite dev server on `http://localhost:5173` |

The frontend calls the API via a relative base URL (`/api/v1` in `client/src/api/client.ts`). In local dev, Vite proxies `/api` to `http://localhost:8000`. That same pattern maps cleanly to a reverse proxy in Docker.

Pyodide loads from `cdn.jsdelivr.net` in the browser, so containerizing the stack does not block in-browser Python preview.

---

## 2. Target Architecture

Add a third Compose service for the frontend. Keep PostgreSQL as its own container (recommended — do not bundle the database into the app image).

```text
┌─────────────┐     /api/*      ┌─────────────┐
│   client    │ ──────────────► │     api     │
│ nginx/vite  │                 │   FastAPI   │
└─────────────┘                 └──────┬──────┘
                                       │
                                       ▼
                                 ┌─────────────┐
                                 │     db      │
                                 │  Postgres   │
                                 └─────────────┘
```

**Production path:** Build the React app to static assets, serve them with **nginx**, and proxy `/api` to `http://api:8000`.

**Optional dev-in-Docker path:** Run the Vite dev server in a container with its proxy target set to `http://api:8000` instead of `localhost:8000`.

---

## 3. Approaches Considered

### Option A — Multi-container Compose (recommended)

Three services: `db`, `api`, `client`.

- Matches current repo layout (`client/` + `server/`).
- Each service scales and updates independently.
- Standard production pattern (nginx + API + Postgres).

### Option B — Single app image (API serves built frontend)

One image builds the React app, copies `client/dist` into the Python image, and mounts static files in FastAPI (e.g. `StaticFiles`) while keeping API routes under `/api`.

- Fewer running containers.
- Requires FastAPI static-file wiring and a multi-stage Dockerfile spanning both apps.
- Postgres should still run as a separate container.

### Option C — Literally one container for everything

Possible (e.g. supervisord running nginx, uvicorn, and postgres together) but **not recommended**: harder to scale, back up, and upgrade.

---

## 4. Implementation Tasks

### 4.1 New `client/Dockerfile` (production)

Multi-stage build:

1. **Build stage:** Node 20+, `npm ci`, `npm run build` → `dist/`.
2. **Run stage:** `nginx:alpine`, copy `dist/` and an nginx config.

### 4.2 Nginx configuration

- Serve static files from `/` (SPA fallback to `index.html` for client-side routing).
- Proxy `/api` to `http://api:8000` (preserve headers for JWT auth).
- Apply CSP headers consistent with `server/app/main.py` and `client/vite.config.ts` (Pyodide CDN, Google Fonts, workers).

### 4.3 Update `docker-compose.yml`

Add a `client` service:

- **Build:** `context: ./client`, `dockerfile: Dockerfile`.
- **Ports:** e.g. `8080:80` (single entry point for users).
- **Depends on:** `api` (and optionally wait for API health).
- **Networks:** same default network as `api` and `db`.

Adjust the `api` service for production use:

- Remove the `./server:/app` bind mount (or gate it behind a Compose profile for local dev).
- Remove `--reload` from the default command.
- Optionally run `alembic upgrade head` on startup or via an init container.

### 4.4 Vite proxy (dev-in-Docker only)

If supporting Vite inside Docker for development:

- Change proxy target from `http://localhost:8000` to `http://api:8000` (env-driven in `vite.config.ts` is preferable).

### 4.5 CORS and environment

- With nginx on one origin serving both UI and proxied API, browser CORS is less of a concern for the main UI.
- Still configure `CORS_ORIGINS` in `.env` if the frontend and API are exposed on different host/port pairs.
- Document required `.env` variables in README (unchanged: `SECRET_KEY`, Postgres credentials, etc.).

### 4.6 Migrations and seed data

- Automate `alembic upgrade head` on first API start (entrypoint script) or document a one-time `docker compose exec api alembic upgrade head`.
- Optionally document `docker compose exec api python seed.py` for demo data.

### 4.7 Documentation

- Update `README.md` Quick Start: `docker compose up --build` serves the full app at e.g. `http://localhost:8080`.
- Keep a “local frontend dev” section for contributors who prefer `npm run dev` on the host.

---

## 5. Suggested File Additions

```text
client/
├── Dockerfile              # multi-stage: build + nginx
└── nginx.conf              # static SPA + /api reverse proxy

docker-compose.yml          # add client service; prod-oriented api defaults
docker-compose.dev.yml      # optional override: bind mounts + --reload + vite
```

---

## 6. Verification Checklist

After implementation:

- [ ] `docker compose up --build` starts `db`, `api`, and `client` without manual steps.
- [ ] UI loads at the published client port (e.g. `http://localhost:8080`).
- [ ] Register, login, browse exercises, submit code, and view progress work end-to-end.
- [ ] Pyodide preview runs (CDN allowed by CSP).
- [ ] API docs remain reachable (via proxy at `/api/docs` or direct port `8000` if exposed).
- [ ] Migrations apply cleanly on fresh volume.
- [ ] Existing pytest suite still passes (tests use in-memory SQLite, unchanged).

---

## 7. Out of Scope (for this plan)

- Kubernetes / cloud deployment manifests.
- TLS termination (assume reverse proxy or platform handles HTTPS in production).
- Changing grading, auth, or Pyodide execution model.

---

## 8. Summary

The app **can** run entirely in Docker. The backend and database already do; the missing piece is a **containerized frontend** (nginx serving the Vite build) plus Compose wiring so `/api` proxies to FastAPI. Multi-service Compose is the recommended approach; a single combined image is possible but optional.
