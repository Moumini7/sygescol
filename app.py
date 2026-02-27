import streamlit as st
import pandas as pd
import altair as alt
from models.models import Strmlit_DBManager, Styles_manager, DataStats

# Charger le CSS
Styles_manager.load_css()
db_manager = Strmlit_DBManager()

# Titre du dashboard
st.markdown("""
<div class="metric-card metric-card-green">
    <h1 style="margin-bottom: -15px;">
        TABLEAU DE BORD SYGESCOL
    </h1> 
    <span style="margin-right: 10px;"> 
        Système de Gestion de Collect et d'exploration de Données  
    </span>
</div>
""", unsafe_allow_html=True)

# Dossiers des données
folder_ws = "./data/data_ws"
folder_bs = "./data/data_bs"

st.divider()

# Affichage des métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_datasets_ws = DataStats.count_files(folder_ws)
    st.markdown(f"""
    <div class="metric-card metric-card-green"
         style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="metric-title">Datasets Web Scraper</div>
            <div class="metric-value">{total_datasets_ws}</div>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:12px; border-radius:12px;">
            <i class="fa-solid fa-database" style="font-size:25px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_datasets_bs = DataStats.count_files(folder_bs)
    st.markdown(f"""
    <div class="metric-card metric-card-blue"
         style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="metric-title">Datasets BeautifulSoup</div>
            <div class="metric-value">{total_datasets_bs}</div>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:12px; border-radius:12px;">
            <i class="fa-solid fa-layer-group" style="font-size:25px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_rows_ws = DataStats.total_rows(folder_ws)
    st.markdown(f"""
    <div class="metric-card metric-card-yellow"
         style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="metric-title">Entrées Web Scraper</div>
            <div class="metric-value">{total_rows_ws}</div>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:12px; border-radius:12px;">
            <i class="fa-solid fa-table" style="font-size:25px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_rows_bs = DataStats.total_rows(folder_bs)
    st.markdown(f"""
    <div class="metric-card metric-card-red"
         style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="metric-title">Entrées BeautifulSoup</div>
            <div class="metric-value">{total_rows_bs}</div>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:12px; border-radius:12px;">
            <i class="fa-solid fa-table" style="font-size:25px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Lecture du DataFrame depuis la base
df = db_manager.read_streamlit_bd()

# S'assurer que df est bien un DataFrame
if not isinstance(df, pd.DataFrame) or df.empty:
    st.info("Aucune donnée disponible pour les visualisations.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if "type" in df.columns:
            t_recent = df["type"].value_counts().head(10).reset_index()
            t_recent.columns = ["Produit", "Occurrences"]
            chart = alt.Chart(t_recent).mark_bar(color="#107584").encode(
                x=alt.X("Produit", sort="-y"),
                y="Occurrences"
            )
            st.subheader("Top 10 des produits les plus récurrents")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Colonne 'type' manquante pour le graphique.")

    with col2:
        if "adresse" in df.columns and "prix" in df.columns:
            t_mcher = df.groupby("adresse")["prix"].mean().sort_values().head(5).reset_index()
            st.subheader("Top 5 des adresses les moins chères (prix moyen)")
            st.dataframe(t_mcher)
        else:
            st.warning("Colonnes 'adresse' ou 'prix' manquantes pour le tableau.")
