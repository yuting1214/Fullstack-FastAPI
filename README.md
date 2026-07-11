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

- **FastAPI** with ORJSONResponse for fast serialization
- **Fully async** — endpoints, CRUD, and database layer
- **SQLAlchemy 2.0** with async engine and `select()` style queries
- **Pydantic v2** for request/response validation and settings management
- **Pure ASGI middleware** for doc protection (no `BaseHTTPMiddleware` overhead)
- **Typed lifespan state** with proper startup/shutdown lifecycle
- **uvloop + httptools** for maximum ASGI performance
- **GZIP compression** for responses > 1KB
- **Session-based auth** protecting `/docs` and `/redoc`
- **uv** for fast, reproducible dependency management
- **Locust** load testing included
- **Docker** multi-stage build ready

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
├── tests/                       # Async test suite
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
| `GET` | `/` | Health check |
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

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [FastAPI Tips](https://github.com/Kludex/fastapi-tips)
