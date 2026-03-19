FROM python:3.11-slim-bookworm

# Installer UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Installer dépendances système pour MLflow et cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances Python
RUN uv pip install --system --no-cache -r pyproject.toml

# Copier le code source
COPY . .

EXPOSE 8000

# Run the API
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
