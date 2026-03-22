# Stage 1: builder — installs dependencies using uv
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy uv binary from official image (no pip install needed)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency manifest and lock file
COPY pyproject.toml uv.lock ./

# Install production deps only into the project venv
RUN uv sync --no-dev --frozen

# Stage 2: runtime — lean image with only what's needed to run
FROM python:3.13-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN useradd --create-home appuser

# Copy venv from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy app source
COPY --chown=appuser:appuser app/ /app/app/

USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
