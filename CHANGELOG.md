# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-07-11

### Memory & Deployment (Railway bills by memory)
- **Idle container memory ~62MB, down from ~150MB** (measured via cgroup against PostgreSQL): the container now execs the venv Python directly instead of keeping a `uv run` wrapper process resident, caps glibc malloc arenas (`MALLOC_ARENA_MAX=2`, `MALLOC_TRIM_THRESHOLD_=100000`), and precompiles bytecode at build time (`UV_COMPILE_BYTECODE=1`).
- **Genuinely multi-stage Dockerfile**: the final image contains only the venv and `src/` — no uv binary, no build context.
- **Added `.dockerignore`**: host `.venv`, `.git`, `dev.db`, tests, and caches no longer enter the build context.

### FastAPI 0.139 Upgrade
- **Upgraded FastAPI 0.129 → 0.139**: JSON responses now serialize through pydantic-core (Rust); removed the deprecated `ORJSONResponse` and the `orjson` dependency.
- **Replaced `fastapi[standard]` with explicit deps** (`fastapi`, `jinja2`, `python-multipart`): fastapi-cli, httpx, and email-validator were never imported at runtime.
- Note: FastAPI 0.132+ rejects JSON requests with an incorrect `Content-Type` by default.

### Database
- **UUIDv7 primary keys**: time-ordered IDs (via `uuid-utils`) replace random uuid4 for B-tree insert locality; PostgreSQL 18's native `uuidv7()` server default is documented as an alternative.
- **Alembic async migrations**: `migrations/` scaffolding with `env.py` wired to app settings; initial revision included. Startup `create_all` is kept so one-click deploys stay zero-step.
- **Removed unused `psycopg2-binary`**; the data layer is asyncpg-only.

### Configuration
- **Env-var-driven settings** (`ENV_MODE`, `HOST`, `PORT`) replace module-level argparse — the app now also runs under plain `uvicorn src.backend.main:app` and gunicorn.

### API
- **Added `GET /health`** liveness endpoint for Railway healthchecks.

### Security
- **Docs credentials always required**: `USER_NAME`/`PASSWORD` are prompted during Railway onboarding; if left unset, they are auto-generated and printed once in the startup logs. Previously, unset credentials meant an empty login form authenticated successfully.
- **Constant-time credential comparison** (`secrets.compare_digest`) prevents timing-based probing.
- **`SECRET_KEY` auto-generates** when unset (set a stable value to keep sessions across restarts).

### Login UI
- **Redesigned the auth page**: modern card layout with dark-mode support (`prefers-color-scheme`), accessible focus states, and reduced-motion fallbacks — replacing the legacy fake-modal design.
- **htmx-enhanced login** (vendored `htmx.min.js` 2.0.10, no CDN): failed logins swap only the card fragment; successful logins redirect via `HX-Redirect`. Plain form POST still works without JavaScript.

### Housekeeping
- Moved `ruff` to the dev dependency group; refreshed all locked dependencies.

## [0.1.0] - 2026-02-20

### Project Structure
- **Reorganized to `src/` layout**: Moved from `backend/fastapi/` to `src/backend/`, `frontend/` to `src/frontend/`, and tests to root `tests/` directory. Eliminates redundant nesting and follows standard Python project conventions.
- **Removed dead files**: Deleted empty `constants.py`, `authorization.py`, and root `__init__.py`.

### Package Management
- **Migrated from `requirements.txt` to `uv`**: Added `pyproject.toml` with proper dependency groups (core vs dev). Removed `requirements.txt` and `pytest.ini`.
- **Added `.python-version`**: Pins project to Python 3.12.
- **Removed unused dependencies**: Dropped `trio`, `databases` (SQLAlchemy async handles everything natively).
- **Added `uvloop`**: Platform-conditional dependency for faster event loop on Linux/macOS (Tip #1 from [fastapi-tips](https://github.com/Kludex/fastapi-tips)).

### Environment & Security
- **Replaced `.env` with `.env.example`**: Secrets are no longer tracked in git. Added `.env` and `.env.*` patterns to `.gitignore`.
- **Fixed hardcoded `SECRET_KEY`**: Session middleware now reads `SECRET_KEY` from environment/settings instead of using `"your_secret_key"`.
- **Authentication uses settings**: `authenticate_user()` now reads from `pydantic-settings` instead of raw `os.getenv()` calls.

### FastAPI Best Practices
- **Fully async endpoints & CRUD**: All endpoints converted from `def` to `async def`, eliminating thread pool overhead (Tip #2, #9 from [fastapi-tips](https://github.com/Kludex/fastapi-tips)).
- **Removed sync database engine**: Dropped `create_engine`, `SyncSessionLocal`, and `get_sync_db`. The entire data layer is now async-only.
- **SQLAlchemy 2.0 style**: Migrated from legacy `session.query()` to `select()` statements. Models use `Mapped`/`mapped_column` instead of `Column()`.
- **Portable UUID**: Replaced PostgreSQL-specific `UUID(as_uuid=True)` column with `String(36)` for cross-database compatibility (dev SQLite + prod PostgreSQL).
- **Pure ASGI middleware**: Replaced `@app.middleware("http")` (wraps `BaseHTTPMiddleware`) with a pure ASGI `DocProtectMiddleware` class for better performance (Tip #8 from [fastapi-tips](https://github.com/Kludex/fastapi-tips)).
- **Typed lifespan state**: Lifespan now yields a typed `AppState` dict containing the session factory, following the recommended pattern over `app.state` (Tip #6 from [fastapi-tips](https://github.com/Kludex/fastapi-tips)).
- **Async database initialization**: `init_db()` uses the async engine (`conn.run_sync(Base.metadata.create_all)`) instead of blocking the event loop with the sync engine.
- **Proper engine disposal**: Async engine is disposed on shutdown via the lifespan context manager.
- **Declarative base update**: Migrated from `declarative_base()` to `DeclarativeBase` class (SQLAlchemy 2.0).
- **`async_sessionmaker`**: Replaced `sessionmaker(..., class_=AsyncSession)` with the dedicated `async_sessionmaker`.

### Testing
- **All-async test suite**: Tests use `httpx.AsyncClient` with `pytest-anyio` instead of `TestClient` (Tip #5, #10 from [fastapi-tips](https://github.com/Kludex/fastapi-tips)).
- **Shared `conftest.py` with DB lifecycle**: `ASGITransport` does not trigger FastAPI's lifespan events, so `tests/conftest.py` manages DB table creation/teardown via an `autouse` fixture. This ensures tests work without depending on the app lifespan and provides clean state between tests.
- **Removed duplicate `/messages/async` endpoint**: Since all endpoints are now async, the separate async endpoint is no longer needed.
- **Consolidated test files**: Merged `test_api_sync.py` and `test_api_async.py` into a single `test_api.py`.

### Deployment
- **Updated Dockerfile**: Uses Python 3.12, installs dependencies via `uv` instead of `pip`, references new `src.backend.main` module path. Requires `[tool.hatch.build.targets.wheel] packages = ["src"]` in `pyproject.toml` so hatchling knows where to find the source packages in the `src/` layout.
- **Updated locustfile**: Removed `/messages/async` endpoint tests (endpoint removed), cleaned up unused imports.

## [0.0.1] - Previous

### Features (from `optimized-version` branch)
- ORJSONResponse for fast JSON serialization
- Increased thread pool to 100 (from default 40)
- GZIP compression middleware
- Locust load testing configuration
- Session-based doc protection (login required for `/docs`, `/redoc`)
- Async + sync endpoint support with SQLAlchemy
