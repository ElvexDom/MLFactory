import os
import argparse
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlflow.models.signature import infer_signature
from dotenv import load_dotenv

# 1. Chargement du fichier .env
load_dotenv()

# 2. Configuration de l'authentification avec fallback (admin/password1234)
os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv("MLFLOW_TRACKING_USERNAME", "admin")
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv("MLFLOW_TRACKING_PASSWORD", "password1234")

# 3. Connexion au serveur MLflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_URL", "http://localhost:5000"))

def train(model_type="logistic", production=False):
    # Preparation des donnees
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    mlflow.set_experiment("Iris_Training")
    model_name = "IrisClassifier"

    print(f"🚀 [RUN] Starting training: {model_type}")
    with mlflow.start_run():
        if model_type == "logistic":
            model = LogisticRegression(max_iter=200)
            mlflow.log_param("model_type", "LogisticRegression")
        else:
            model = RandomForestClassifier(n_estimators=100)
            mlflow.log_param("model_type", "RandomForestClassifier")
        
        model.fit(X_train, y_train)

        # Enregistrement des performances
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", accuracy)
        print(f"📊 [METRIC] Accuracy: {accuracy:.4f}")

        # Definition de la signature (input/output schema)
        signature = infer_signature(X_train, y_pred)

        # Enregistrement securise via 'skops' (evite le warning pickle)
        import sklearn
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model", 
            signature=signature,
            registered_model_name=model_name,
            serialization_format="skops",
            pip_requirements=[f"scikit-learn=={sklearn.__version__}", "skops"]
        )
        
        version = model_info.registered_model_version
        print(f"📦 [REGISTRY] New version created: v{version}")

        # Gestion de l'alias de production
        if production:
            client = mlflow.MlflowClient()
            client.set_registered_model_alias(model_name, "production", version)
            print(f"🌟 [STATUS] Version v{version} is now the official PRODUCTION reference")
        else:
            print(f"ℹ️ [STATUS] Version v{version} registered (not promoted to production)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="logistic", choices=["logistic", "forest"])
    parser.add_argument("--production", action="store_true")
    
    args = parser.parse_args()
    train(model_type=args.model, production=args.production)