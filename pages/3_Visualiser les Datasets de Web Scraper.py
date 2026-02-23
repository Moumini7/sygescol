import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from models.models import Strmlit_DBManager, Styles_manager
Styles_manager.load_css()


Styles_manager.load_css()

st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            DataViz
        </h1> 
        <span style="margin-rigth: 10px;"> 
            Visualisation des données collectées avec le plugin Web Scraper  
        </span>
</div>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "data_ws"

sys.path.append(str(BASE_DIR))

# Instanciation de la classe
manager = Strmlit_DBManager()

csv_files = sorted(DATA_DIR.glob("ws*.csv"))

if not csv_files:
    st.warning("Aucun dataset disponible...")
    st.stop()

selected_file = st.selectbox(
    "Choisissez un fichier",
    [f.name for f in csv_files]
)

file_path = DATA_DIR / selected_file


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


df_raw = load_data(file_path)
df = manager.traitement_dataset(df_raw)

# ==================================================
# INDICATEURS CLÉS
# ==================================================

st.subheader("Indicateurs clés")
col1, col2, col3, col4 = st.columns(4)
with col1:st.metric("Total entrées", len(df))
with col2:st.metric("Prix moyen", round(df["prix"].mean(), 2))
with col3:st.metric("Prix max", df["prix"].max())
with col4:st.metric("Prix min", df["prix"].min())

import streamlit as st
import pandas as pd
import numpy as np

with st.spinner(f"Visualisation des données pour {selected_file}"):
    st.line_chart(df["prix"])
    st.bar_chart(df["prix"])


