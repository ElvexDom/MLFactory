from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from controllers.engine import PredictionEngine

router = APIRouter()
engine = PredictionEngine()

class FeaturesInput(BaseModel):
    # Utilisation d'un dictionnaire flexible pour accepter n'importe quel modèle
    payload: dict 

@router.get("/health")
def health_check():
    return {"status": "online", "gateway": "mlflow-stack"}

@router.post("/{model_name}/predict")
def predict(
    data: FeaturesInput,
    model_name: str = Path(..., title="Nom du modèle enregistré dans MLflow")
):
    result = engine.compute(model_name, data.payload)
    
    if result is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Le modèle '{model_name}' est introuvable ou n'a pas de version en production."
        )
    
    return result