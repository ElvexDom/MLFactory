import os
import streamlit as st
import requests
import pandas as pd

# ----------------------------
# CONFIGURATION
# ----------------------------
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
MODEL_NAME = "IrisClassifier"
DATA_PATH = "/app/data/iris_test.csv"

st.set_page_config(page_title="Iris Prediction", layout="wide")

st.title("🚀 Iris Prediction Gateway")
st.caption(f"Modèle cible : {MODEL_NAME}")

# ----------------------------
# ENTRÉE DES DONNÉES
# ----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    mode = st.radio(
        "Source des données",
        ["Saisie manuelle", "Dataset de test (CSV)"]
    )

    features = {}
    
    if mode == "Dataset de test (CSV)":
        try:
            df = pd.read_csv(DATA_PATH)
            row_index = st.selectbox("Choisir une ligne", df.index)
            selected_row = df.loc[row_index]
            
            # Dictionnaire de correspondance (Mapping)
            mapping_fleurs = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
            
            # Conversion en dictionnaire
            features = selected_row.to_dict()
            
            # On extrait la target pour l'affichage
            target_value = features.pop("target", None)
            
            st.write("**Données envoyées à l'API :**")
            st.json(features)
            
            if target_value is not None:
                # On utilise le mapping pour afficher le nom au lieu du chiffre
                nom_fleur_reel = mapping_fleurs.get(int(target_value), "Inconnue")
                st.info(f"🎯 **Espèce réelle (CSV) :** {nom_fleur_reel}")
                
        except Exception as e:
            st.error(f"Erreur de chargement CSV : {e}")
            st.stop()
    else:
        # Correspondance exacte avec les noms de colonnes attendus par le modèle
        features["sepal length (cm)"] = st.number_input("Sepal Length", 0.0, 10.0, 5.1)
        features["sepal width (cm)"] = st.number_input("Sepal Width", 0.0, 10.0, 3.5)
        features["petal length (cm)"] = st.number_input("Petal Length", 0.0, 10.0, 1.4)
        features["petal width (cm)"] = st.number_input("Petal Width", 0.0, 10.0, 0.2)

# ----------------------------
# APPEL API & RÉSULTATS
# ----------------------------
with col2:
    st.subheader("Résultat de l'inférence")
    
    if st.button("Lancer la prédiction", use_container_width=True):
        # On encapsule les features dans la clé "payload"
        full_payload = {"payload": features}
        
        try:
            endpoint = f"{API_BASE_URL}/{MODEL_NAME}/predict"
            
            with st.spinner(f"Calcul en cours pour {MODEL_NAME}..."):
                response = requests.post(endpoint, json=full_payload)
                response.raise_for_status()
                
            data = response.json()
            
            # Extraction des résultats
            class_names = ["Setosa", "Versicolor", "Virginica"]
            pred_idx = int(data["prediction"]) # On s'assure que c'est un entier
            version = data.get("version", "Inconnue")
            
            st.success(f"### Classe prédite : **{class_names[pred_idx]}**")
            st.write(f"Index prédit : `{pred_idx}`")
            st.info(f"Version du modèle : v{version}")

            # Affichage des probabilités
            if data.get("probabilities"):
                st.write("---")
                st.write("**Confiance du modèle :**")
                prob_df = pd.DataFrame({
                    "Classe": class_names,
                    "Probabilité": data["probabilities"]
                })
                st.bar_chart(prob_df.set_index("Classe"))

        except requests.exceptions.HTTPError as e:
            st.error(f"Erreur API ({e.response.status_code}): {e.response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")