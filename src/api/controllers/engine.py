import pandas as pd
from services.registry import ModelRegistry

class PredictionEngine:
    def __init__(self):
        self.registry = ModelRegistry()

    def compute(self, model_name: str, input_data: dict):
        """Orchestre la récupération du modèle et le calcul de l'inférence."""
        model, version = self.registry.fetch_production_model(model_name)
        
        if not model:
            return None

        # Conversion du dictionnaire en DataFrame Pandas
        df = pd.DataFrame([input_data])
        
        # Exécution de la prédiction
        prediction = model.predict(df)
        
        # Tentative d'extraction des probabilités
        probabilities = None
        if hasattr(model._model_impl, "predict_proba"):
            probabilities = model._model_impl.predict_proba(df)[0].tolist()

        return {
            "model": model_name,
            "version": version,
            "prediction": prediction.tolist()[0],
            "probabilities": probabilities
        }