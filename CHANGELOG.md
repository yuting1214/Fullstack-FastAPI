# Changelog

All notable changes to this project will be documented in this file.

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
