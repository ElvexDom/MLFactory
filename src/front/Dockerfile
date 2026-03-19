FROM python:3.11-slim-bookworm

# 1. Installation de UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. On indique à uv d'utiliser le Python système (pas de venv)
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# 3. Dépendances système nécessaires pour Streamlit et ses packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# 5. Installation des dépendances Python
RUN uv pip install --system --no-cache -r pyproject.toml

# 6. Copier le code source
COPY . .

# 7. Exposer le port Streamlit
EXPOSE 8501

# 8. Lancer Streamlit
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]