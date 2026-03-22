# 🚀 MLOps Project: The ML Factory

## 🎯 Vision du projet

L'objectif est de construire une infrastructure **Zero-Downtime** où le
modèle de Machine Learning est totalement découplé de l'application qui
le consomme.

Grâce à l'utilisation d'un **Model Registry (MLflow)** et d'un **Object
Storage (MinIO)**, il est possible de mettre à jour le modèle en
production sans redémarrer les conteneurs.

------------------------------------------------------------------------

## 🏗️ Architecture du projet

Chaque composant est isolé dans son propre service Docker.

    ml-factory-project/
    ├── data/
    │   └── iris_test.csv        <-- Dataset de test avec colonne 'target'
    ├── src/
    │   ├── api/                 (FastAPI + Dockerfile)
    │   ├── front/               (Streamlit + Dockerfile)
    │   ├── mlops/               (Dockerfile)
    │   └── train/
    │       └── train.py
    ├── docker-compose.yml
    ├── pyproject.toml
    ├── uv.lock
    └── .env

------------------------------------------------------------------------

## 🔧 Services

-   **MinIO** → stockage des artefacts (S3 local)\
-   **MLflow** → registry des modèles\
-   **API (FastAPI)** → sert les prédictions\
-   **Front (Streamlit)** → interface utilisateur (mapping ID -\>
    Espèce)

------------------------------------------------------------------------

## ⚙️ Configuration & Lancement

### 1. Préparation du fichier `.env`

Copiez le fichier d'exemple et adaptez les valeurs si nécessaire :

``` bash
cp .env.example .env
```

### 2. Lancement des conteneurs

``` bash
docker-compose up --build -d
```

### 3. Initialisation du stockage (Crucial)

Avant tout entraînement, vous devez créer l'espace de stockage pour les
modèles :

1.  Accédez à MinIO UI : http://localhost:9001\
    Login : **minio_user_**\
    Mot de passe : **minio_password**

2.  Aller dans l'onglet **Buckets**

3.  Cliquer sur **Create Bucket**

4.  Nommer le bucket :

```
mlflow
```

------------------------------------------------------------------------

## 🧪 Entraînement et Déploiement

Les scripts d'entraînement sont exécutés hors Docker via **uv**.\
Le script supporte l'option `--production` pour un déploiement immédiat.

### Usage

#### Entraînement simple

(Enregistre dans MLflow mais ne publie pas)

``` bash
uv run python src/train/train.py --model logistic
```

#### Entraînement + Mise en production immédiate

``` bash
uv run python src/train/train.py --model logistic --production
```

------------------------------------------------------------------------

## 🔄 Scénario de validation (Zero-Downtime)

### ⚡ Phase 1 : Déploiement Direct

``` bash
uv run python src/train/train.py --model logistic --production
```

✔️ Résultat :\
Le modèle **v1 (Logistique)** est actif sur Streamlit.

------------------------------------------------------------------------

### 👨‍🍳 Phase 2 : Entraînement en arrière-plan

``` bash
uv run python src/train/train.py --model forest
```

✔️ Résultat :\
La **v2** est enregistrée dans MLflow, mais Streamlit utilise toujours
la **v1**.\
Preuve du **Zero-Downtime**.

------------------------------------------------------------------------

### 🎯 Étape finale : Bascule à chaud

1.  Aller sur MLflow :

```
http://localhost:5000
```
2.  Sélectionner la **Version 2**

3.  Lui attribuer l'alias :

```
production
```


✔️ Résultat :\
Streamlit bascule sur le nouveau modèle instantanément **sans
redémarrage**.

------------------------------------------------------------------------

## 🌐 Accès aux services

| Service | URL                    | Login        | Mot de passe     | Note                     |
|---------|------------------------|--------------|------------------|--------------------------|
| Front   | http://localhost:8501  | —            | —                | Interface Utilisateur     |
| API     | Interne Docker         | —            | —                | Port 8000 (Backend)      |
| MLflow  | http://localhost:5000  | admin        | password1234     | Registry des modèles      |
| MinIO   | http://localhost:9001  | minio_user   | minio_password   | Console S3                |

### 💡 Rappel

- **Front** : Interface pour tester les prédictions  
- **API** : Service backend exposant les endpoints  
- **MLflow** : Gestion des versions et promotion des modèles  
- **MinIO** : Stockage des artefacts et modèles