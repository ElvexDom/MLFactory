FROM python:3.11.9-slim

# Initialisation des répertoires
WORKDIR /app
RUN mkdir -p /data

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Installation de MLflow et des drivers
RUN pip install --no-cache-dir \
    mlflow[genai,extras,auth]==3.10.0 \
    psycopg2

# Configuration des scripts
COPY start.sh .
RUN chmod +x start.sh

# Déclaration du volume persistant
VOLUME ["/data"]
WORKDIR /data

EXPOSE 5000

ENTRYPOINT ["/app/start.sh"]