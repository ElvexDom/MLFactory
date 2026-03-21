from fastapi import FastAPI
from routes.endpoints import router as api_router
from dotenv import load_dotenv

# Charge les variables (MLFLOW_TRACKING_URI, credentials S3, etc.)
load_dotenv()

app = FastAPI(
    title="MLOps Prediction Gateway",
    description="Interface unifiée pour servir les modèles du registre MLflow",
    version="1.0.0"
)

# Inclusion des routes sans préfixe pour garder l'URL /{model_name}/predict
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)