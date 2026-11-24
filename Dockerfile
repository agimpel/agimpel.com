
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# System dependencies and uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
    && pip install --no-cache-dir uv \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN groupadd -r appuser \
    && useradd --no-log-init -r -g appuser appuser \
    && mkdir -p /app

WORKDIR /app

# Copy dependency metadata
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY . .

# Install project
RUN uv sync --frozen --no-dev

# Permissions
RUN chown -R appuser:appuser /app \
    && chmod -R u=rwX,g=rX,o= /app

EXPOSE 8000

USER appuser

# Start Gunicorn
CMD ["gunicorn", \
     "--bind=0.0.0.0:8000", \
     "--workers=2", \
     "--worker-class=gthread", \
     "--threads=2", \
     "--max-requests=5000", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "agimpel_com.wsgi:application"]