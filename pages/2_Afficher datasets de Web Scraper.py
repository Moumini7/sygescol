import streamlit as st
import pandas as pd
import os as os
from pathlib import Path
from models.models import Styles_manager


# Chargement du CSS
Styles_manager.load_css()

st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            Web Scraper
        </h1> 
        <span style="margin-rigth: 10px;"> 
            Exploration des données collectées avec le plugin Web Scraper  
        </span>
</div>
""", unsafe_allow_html=True)

# parent.parent -> sygesco_app
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "data_ws"
DATA_DIR.mkdir(exist_ok=True)

# Récupération de la liste des fichier csv dans le dossier -> data_ws
csv_files = sorted(DATA_DIR.glob("*.csv"))
if not csv_files:
    st.warning("Aucun fichier CSV trouvé dans le dossier data_ws.")
    st.stop()


# Chargement du dataset depuis le dossier data_ws
#--------------------------------------------------
st.subheader("Sélectionner un dataset")
selected_file = st.selectbox(
    "Choisissez un fichier",
    [f.name for f in csv_files]
)
file_path = DATA_DIR / selected_file


# Lecture des fichiers CSV
#--------------------------------
try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.stop()

st.markdown(f"""<div/><div/><div/><div/>""", unsafe_allow_html=True)

# Détails du dataset
#--------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Lignes", df.shape[0])

with col2:
    st.metric("Colonnes", df.shape[1])

with col3:
    size_kb = file_path.stat().st_size / 1024
    st.metric("Taille", f"{size_kb:.2f} KB")


# Apperçu du dataset selectionné
#--------------------------------
st.markdown(f"""<div/><div/><div/><div/>""", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)


