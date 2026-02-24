import streamlit as st
import pandas as pd
import time
from models.models import Strmlit_DBManager, Styles_manager

db_manager = Strmlit_DBManager()
Styles_manager.load_css()

st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            BeautifulSoup
        </h1> 
        <span style="margin-rigth: 10px;"> 
            Collecte des données avec la biliothèque BeautifulSoup  
        </span>
</div>
""", unsafe_allow_html=True)


CATEGORIES = {
    "Vêtements pour hommes": "vetements-homme",
    "Chaussures pour hommes": "chaussures-homme",
    "Vêtements pour enfants": "vetements-enfants",
    "Chaussures pour enfants": "chaussures-enfants"
}

# Sélection des critères de scraping
st.subheader(" Ctritères de Scraping ")
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    categorie_label = st.selectbox(
        "Catégorie",
        list(CATEGORIES.keys())
    )

with col2:
    nb_pages = st.number_input(
        "Nombre de pages à scraper",
        min_value=1,
        max_value=50,
        value=5,
        step=1
    )


with col3:
    st.markdown("""<br/>""", unsafe_allow_html=True)
    lancer_scraping = st.button(
        "Démarrer le Scraping",
        use_container_width=True,
        key="lancer_scraping_button",
        type="primary"
    )

categorie_slug = CATEGORIES[categorie_label]

st.divider()
st.subheader(" Scraping en temps réel ")

# Scraping en temps réel avec BeautifulSoup
if lancer_scraping:
    with st.spinner(f"Scraping en cours : {categorie_label}"):
        df = db_manager.chargementData(categorie_slug, nb_pages)

    st.success("Scraping terminé")

    if not df.empty:
       
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total en base", len(df))
        with col2:
            moyenne = df["prix"].mean()
            moyenne = f"{moyenne:.0f}" 
            st.metric("Prix moyen", moyenne)
        with col3:
            st.metric("Catégories", df["categorie"].nunique())
        with col4:
            st.metric("Types d'articles", df["type"].nunique())

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aucune donnée récupérée en temps réel.")
else:
    st.info("Aucune donnée collectées.")


# Données disponibles dans la base de données
st.divider()
st.subheader(" Données déjà disponibles en base de données ")

df_read = db_manager.read_streamlit_bd()

if isinstance(df_read, pd.DataFrame) and not df_read.empty:

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total en base", len(df_read))
    with col2:
        moyenne = df_read["prix"].mean()
        moyenne = f"{moyenne:.0f}" 
        st.metric("Prix moyen", moyenne)
    with col3:
        st.metric("Catégories", df_read["categorie"].nunique())
    with col4:
        st.metric("Types d'articles", df_read["type"].nunique())
        
    st.dataframe(df_read, use_container_width=True)
else:
    st.info("Aucune donnée dans la base de données.")
