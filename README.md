# 🚀 MLOps Project: The ML Factory

## 🎯 Vision du projet

L'objectif est de construire une infrastructure **Zero-Downtime** où le modèle de Machine Learning est totalement découplé de l'application qui le consomme.

Grâce à l'utilisation d'un **Model Registry (MLflow)** et d'un **Object Storage (MinIO)**, il est possible de mettre à jour le modèle en production **sans redémarrer les conteneurs**.

---

## 🏗️ Architecture du projet

Chaque composant est isolé dans son propre service Docker.

```
ml-factory-project/
├── data/ iris_test.csv  
├── src/
│   ├── api/ (FastAPI + Dockerfile)
│   ├── front/ (Streamlit + Dockerfile)
│   └── train/ (train.py)
├── docker-compose.yml   
├── pyproject.toml       
└── .env                 
```

### 🔧 Services

- **MinIO** → stockage des artefacts (S3 local)
- **MLflow** → registry des modèles
- **API (FastAPI)** → sert les prédictions
- **Front (Streamlit)** → interface utilisateur

---

## ⚙️ Configuration

### 1. Fichier `.env`

Créer un fichier `.env` à la racine :

```env
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin

DOCKER_MLFLOW_S3_ENDPOINT_URL=http://minio:9000
DOCKER_MLFLOW_TRACKING_URI=http://mlflow:5000

API_URL=http://api:8000
```

---

## 🐳 Lancer le projet avec Docker Compose

### ▶️ Build + lancement

```bash
docker-compose up --build -d
```

### 📊 Vérifier les conteneurs

```bash
docker ps
```

---

## 🌐 Accès aux services

| Service   | URL                   |
|----------|-----------------------|
| Front    | http://localhost:8501 |
| API      | http://localhost:8000 |
| MLflow   | http://localhost:5000 |
| MinIO UI | http://localhost:9001 |

---

## 🧠 Développement API (FastAPI)

L’API :

- Interroge **MLflow** pour récupérer le modèle en production
- Recharge automatiquement le modèle si l’alias change
- Retourne :
  - la prédiction
  - la version du modèle

---

## 🎨 Interface Streamlit

Permet de :

- Tester des prédictions
- Charger des données (`iris_test.csv`)
- Voir la version du modèle actif
- Visualiser les probabilités

---

## 🧪 Entraînement des modèles

Les scripts d'entraînement sont exécutés **hors Docker** :

```bash
uv run python src/train/train.py
```

---

## 🔄 Scénario de validation (Zero-Downtime)

### ⚡ Phase 1 : Déploiement Automatisé (Régression Logistique)

Entraînez et passez automatiquement le modèle en production :

```bash
uv run python src/train/train.py --model logistic --auto-publish
```

✔️ Résultat attendu :

- Le modèle est enregistré dans MLflow
- L’alias **Production** est automatiquement assigné
- La Vitrine (Streamlit) affiche :
  - **Version 1**
  - Modèle : **Logistic Regression**

---

### 👨‍🍳 Phase 2 : Validation Manuelle (Random Forest)

Entraînez un modèle plus complexe sans le publier immédiatement :

```bash
uv run python src/train/train.py --model forest
```

✔️ Résultat attendu :

- Le modèle est bien enregistré (Version 2)
- **Aucun changement côté utilisateur**
- La Vitrine continue d’utiliser :
  - **Version 1**
  - 👉 preuve du **Zero-Downtime**

---

### 🎯 Étape finale (optionnelle)

1. Aller sur MLflow : http://localhost:5000  
2. Sélectionner la Version 2  
3. Lui attribuer l’alias **Production**  

✔️ Résultat :

- Changement instantané dans Streamlit
- Aucun redémarrage des conteneurs

---

## 🔧 Commandes utiles

### Logs

```bash
docker logs ml_api
docker logs ml_front
```

### Stop

```bash
docker-compose down
```

### Rebuild propre

```bash
docker-compose down -v
docker-compose up --build
```

---

## 💡 Points clés

- Architecture découplée
- Zéro interruption de service
- MLflow = source de vérité
- MinIO = stockage persistant
- API dynamique
- Front = visibilité temps réel
