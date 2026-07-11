---
title: FastAPI
description: A FastAPI server
tags:
  - fastapi
  - uvicorn
  - python
  - postgresql
---

<!-- LINK GROUP -->
[deploy-on-zeabur-button-image]: https://zeabur.com/button.svg
[deploy-on-zeabur-link]: https://zeabur.com/templates/A2TNYB

# FastAPI Fullstack Template

A production-ready [FastAPI](https://fastapi.tiangolo.com/) template with [PostgreSQL](https://www.postgresql.org/), fully async, and modern Python tooling.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/IhHgYS?referralCode=jk_FgY)
[![][deploy-on-zeabur-button-image]][deploy-on-zeabur-link]

> **[CHANGELOG](./CHANGELOG.md)** — See what's changed between versions.

## Features

- **FastAPI 0.139+** — JSON serialized natively by pydantic-core (Rust)
- **Fully async** — endpoints, CRUD, and database layer
- **SQLAlchemy 2.0** with async engine and `select()` style queries
- **UUIDv7 primary keys** — time-ordered for B-tree locality (native in PostgreSQL 18)
- **Alembic** async migrations included
- **Pydantic v2** for request/response validation and settings management
- **Pure ASGI middleware** for doc protection (no `BaseHTTPMiddleware` overhead)
- **Typed lifespan state** with proper startup/shutdown lifecycle
- **uvloop + httptools** for maximum ASGI performance
- **GZIP compression** for responses > 1KB
- **Session-based auth** protecting `/docs` and `/redoc`
- **`/health` endpoint** for platform healthchecks
- **uv** for fast, reproducible dependency management
- **Locust** load testing included
- **Memory-tuned Docker image** — multi-stage build, ~62MB idle (Railway bills by memory)

## Project Structure

```
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/v1/endpoints/    # Route handlers
│   │   ├── core/                # Config, lifespan, middleware, routers
│   │   ├── crud/                # Service layer (async CRUD)
│   │   ├── dependencies/        # Database setup, DI
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── security/            # Authentication
│   │   └── data/                # Seed data
│   └── frontend/
│       └── login/               # Login page templates & static files
├── migrations/                  # Alembic async migrations
├── tests/                       # Async test suite
├── alembic.ini                  # Alembic config (URL comes from app settings)
├── pyproject.toml               # Dependencies & project config
├── Dockerfile                   # Multi-stage build with uv
├── locustfile.py                # Load testing
└── .env.example                 # Environment variable template
```

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yuting1214/Fullstack-FastAPI.git
cd Fullstack-FastAPI

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your values

# Run in development mode (SQLite, auto-reload)
uv run python -m src.backend.main

# Run in production mode (PostgreSQL)
ENV_MODE=prod HOST=0.0.0.0 uv run python -m src.backend.main
```

### Database Migrations

Tables are auto-created on startup, so the one-click deploy needs no manual step.
For controlled schema evolution, use Alembic (the URL is resolved from the same
`ENV_MODE` / `DATABASE_URL` settings the app uses):

```bash
uv run alembic upgrade head                          # apply migrations
uv run alembic revision --autogenerate -m "change"   # generate a new migration
```

### Running Tests

```bash
uv sync --extra dev
uv run pytest
```

> **Note:** Tests use `httpx.AsyncClient` via `ASGITransport`, which does not trigger FastAPI's lifespan events. The shared `tests/conftest.py` handles DB table creation and teardown automatically. If you add new tests, the `setup_db` fixture runs via `autouse` — no manual setup needed.

### Load Testing

```bash
uv run locust
# Open http://localhost:8089
```

### Docker

```bash
docker build -t fullstack-fastapi .
docker run -p 5000:5000 fullstack-fastapi
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Onboarding message |
| `GET` | `/health` | Liveness probe (healthchecks) |
| `GET` | `/login` | Login page |
| `POST` | `/login` | Authenticate |
| `GET` | `/logout` | Clear session |
| `POST` | `/api/v1/messages/` | Create message |
| `GET` | `/api/v1/messages/` | List messages |
| `GET` | `/api/v1/messages/{id}` | Get message |
| `PUT` | `/api/v1/messages/{id}` | Update message |
| `DELETE` | `/api/v1/messages/{id}` | Delete message |

## Environment Variables

See [`.env.example`](./.env.example) for all available configuration options.

Runtime behavior is controlled by env vars (no CLI flags), so the app also runs
under plain `uvicorn src.backend.main:app`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ENV_MODE` | `dev` | `dev` = SQLite + auto-reload, `prod` = PostgreSQL |
| `HOST` | `127.0.0.1` | Bind address (`0.0.0.0` in the Docker image) |
| `PORT` | `5000` | Listen port (set automatically by Railway) |
| `DATABASE_URL` | — | PostgreSQL URL in prod (injected by Railway) |

## Memory Footprint

Railway bills by memory per minute, so the image is tuned for a low idle
footprint — **~62MB idle** (measured via cgroup in Docker), down from ~150MB:

- The container execs the venv Python directly — no resident `uv run` wrapper process
- `MALLOC_ARENA_MAX=2` + `MALLOC_TRIM_THRESHOLD_` cap glibc arena bloat
- Bytecode is precompiled at build time (`UV_COMPILE_BYTECODE=1`) for faster, leaner cold starts
- Multi-stage build ships only the venv and `src/` — no build tools in the final image

**Tip:** if your traffic is bursty, enable Railway's
[App Sleeping](https://docs.railway.com/reference/app-sleeping) on the service —
compute cost drops to ~$0 while idle, and this template's single-process design
is compatible with it.

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [FastAPI Tips](https://github.com/Kludex/fastapi-tips)
