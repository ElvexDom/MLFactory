#!/bin/bash
set -e

# --- Sécurité : Gestion de la KEK_PASSPHRASE ---
KEK_FILE="/data/.mlflow.kek"
if [ -n "$MLFLOW_CRYPTO_KEK_PASSPHRASE" ]; then
    echo "🔐 Sécurité : Kek Passphrase chargée depuis l'environnement."
else
    if [ ! -f "$KEK_FILE" ]; then
        echo "🔐 Sécurité : Kek Passphrase générée dans $KEK_FILE"
        GENERATED_KEY=$(openssl rand -base64 32)
        echo "MLFLOW_CRYPTO_KEK_PASSPHRASE=\"$GENERATED_KEY\"" > "$KEK_FILE"
        chmod 600 "$KEK_FILE"
    fi
    echo "🔐 Sécurité : Kek Passphrase chargée depuis $KEK_FILE"
    source "$KEK_FILE"
fi
export MLFLOW_CRYPTO_KEK_PASSPHRASE

# --- Sécurité : Génération de la SECRET_KEY ---
export MLFLOW_FLASK_SERVER_SECRET_KEY="$(openssl rand -base64 32)"
echo "🔐 Sécurité : Flask Secret Key générée pour cette session."

# --- Gestion de la base de données ---
if [ -n "$PGHOST" ]; then
    export MLFLOW_BACKEND_STORE_URI="postgresql+psycopg2://"
    MLFLOW_DATABASE_URI="postgresql+psycopg2://"
    echo "📑 Base de données : PostgreSQL ($PGHOST)"
else
    export MLFLOW_BACKEND_STORE_URI="sqlite:////data/mlflow.db"
    MLFLOW_DATABASE_URI="sqlite:////data/basic_auth.db"
    echo "📑 Base de données : SQLite (mlflow.db | basic_auth.db)"
fi

# --- Gestion du stockage ---
if [[ -n "$MLFLOW_S3_ENDPOINT_URL" ]]; then
    export MLFLOW_ARTIFACTS_DESTINATION="s3://mlflow/"
    echo "📦 Stockage : MinIO ($MLFLOW_S3_ENDPOINT_URL)"
else
    export MLFLOW_ARTIFACTS_DESTINATION="/data/mlartifacts"
    echo "📦 Stockage : FileStore (mlartifacts)"
fi

# Génération du fichier d'authentification
export MLFLOW_AUTH_CONFIG_PATH="/app/basic_auth.ini"
echo "[mlflow]
default_permission = ${MLFLOW_DEFAULT_PERMISSION:-READ}
database_uri = ${MLFLOW_DATABASE_URI}
admin_username = ${MLFLOW_ADMIN_USERNAME:-admin}
admin_password = ${MLFLOW_ADMIN_PASSWORD:-password1234}
authorization_function = ${MLFLOW_AUTHORIZATION_FUNCTION:-mlflow.server.auth:authenticate_request_basic_auth}
grant_default_workspace_access = ${MLFLOW_GRANT_DEFAULT_WORKSPACE_ACCESS:-false}
workspace_cache_max_size = ${MLFLOW_WORKSPACE_CACHE_MAX_SIZE:-10000}
workspace_cache_ttl_seconds = ${MLFLOW_WORKSPACE_CACHE_TTL_SECONDS:-3600}" \
> "$MLFLOW_AUTH_CONFIG_PATH"

# --- Lancement ---
echo "🚀 Démarrage de mlflow-server..."
exec mlflow server \
    --app-name "${MLFLOW_APP_NAME:-basic-auth}" \
    --host "${MLFLOW_INTERNAL_HOST:-0.0.0.0}" \
    --port "${MLFLOW_INTERNAL_PORT:-5000}" \
    --workers "${MLFLOW_WORKERS:-1}" \
    --backend-store-uri "${MLFLOW_BACKEND_STORE_URI}" \
    --artifacts-destination "${MLFLOW_ARTIFACTS_DESTINATION}" \
    --serve-artifacts \
    --allowed-hosts "${MLFLOW_ALLOWED_HOSTS:-*}" \
    --cors-allowed-origins "${MLFLOW_CORS_ALLOWED_ORIGINS:-*}"