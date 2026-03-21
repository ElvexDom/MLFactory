import os
import mlflow
from mlflow.tracking import MlflowClient

class ModelRegistry:
    def __init__(self):
            # Configuration de l'authentification MLflow
            os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv("MLFLOW_ADMIN_USERNAME", "admin")
            os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv("MLFLOW_ADMIN_PASSWORD", "password1234")
            
            # Initialisation du client Tracking
            self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
            self.client = MlflowClient(tracking_uri=self.tracking_uri)
            mlflow.set_tracking_uri(self.tracking_uri)
            
            # Cache multi-modèles
            self._cache = {}

    def fetch_production_model(self, model_name: str):
        """Récupère le modèle 'production' depuis MLflow avec mise en cache."""
        try:
            # Récupération de la version liée à l'alias 'production'
            alias_info = self.client.get_model_version_by_alias(model_name, "production")
            current_version = alias_info.version

            # Chargement si absent du cache ou si une nouvelle version est dispo
            if model_name not in self._cache or self._cache[model_name]["version"] != current_version:
                print(f"📦 [Registry] Chargement : {model_name} (v{current_version})")
                model_uri = f"models:/{model_name}@production"
                
                self._cache[model_name] = {
                    "object": mlflow.pyfunc.load_model(model_uri),
                    "version": current_version
                }
            
            return self._cache[model_name]["object"], current_version
        except Exception as e:
            print(f"❌ [Registry] Erreur sur {model_name} : {e}")
            return None, None