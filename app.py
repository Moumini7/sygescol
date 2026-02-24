import streamlit as st
import pandas as pd
from pathlib import Path
from models.models import Strmlit_DBManager, Styles_manager, DataStats
import streamlit as st

Styles_manager.load_css()
db_manager = Strmlit_DBManager()

st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            TABLEAU DE BORD SYGESCOL
        </h1> 
        <span style="margin-rigth: 10px;"> 
            Système de Gestion de Collect et d'exploration de Données  
        </span>
</div>
""", unsafe_allow_html=True)

folder_ws = "./data/data_ws"
folder_bs = "./data/data_bs"

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_datasets_ws = DataStats.count_files(folder_ws)
    st.markdown(f"""
    <div class="metric-card metric-card-green"
         style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="metric-title">
                 Datasets Web Scraper
            </div>
            <div class="metric-value">
                {total_datasets_ws}
            </div>
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
            <div class="metric-title">
                Datasets BeautifulSoup
            </div>
            <div class="metric-value">
                {total_datasets_bs}
            </div>
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
            <div class="metric-title">
                Entrées Web Scraper
            </div>
            <div class="metric-value">
                {total_rows_ws}
            </div>
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
            <div class="metric-title">
                Entrées BeautifulSoup
            </div>
            <div class="metric-value">
                {total_rows_bs}
            </div>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:12px; border-radius:12px;">
            <i class="fa-solid fa-table" style="font-size:25px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
df = db_manager.read_streamlit_bd()

st.subheader("Répartition des prix collectés")
st.bar_chart(df[['prix','categorie']].value_counts().reset_index(name='count'), x='prix', y='count', color='categorie', height=600)


