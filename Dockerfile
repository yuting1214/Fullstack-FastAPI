FROM python:3.12-slim AS builder

# Compile .pyc at install time: faster cold start, lower peak RSS on boot
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev --no-editable

# Cap glibc malloc arenas and return freed memory to the OS sooner.
# Railway bills by memory per minute; these cut idle RSS 10-30MB for free.
ENV MALLOC_ARENA_MAX=2
ENV MALLOC_TRIM_THRESHOLD_=100000

# Exec the venv python directly: `uv run` would keep a ~25MB wrapper process
# resident in the container, which counts toward billed memory.
CMD ["/app/.venv/bin/python", "-m", "src.backend.main", "--mode", "prod", "--host", "0.0.0.0"]
