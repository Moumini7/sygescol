import streamlit as st
import pandas as pd
import os as os
import altair as alt
from pathlib import Path
from models.models import Styles_manager, Strmlit_DBManager


# Chargement du CSS
Styles_manager.load_css()
manager = Strmlit_DBManager()

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

# Quelque metrique du dataset
#--------------------------------

dft = manager.traitement_dataset(df)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total en base", len(dft))
with col2:
    moyenne = dft["prix"].mean()
    moyenne = f"{moyenne:.0f}" 
    st.metric("Prix moyen", moyenne)
with col3:
    st.metric("Articles différents", dft["categorie"].nunique())

#with st.spinner("Chargement des données..."):
    #dft = df.copy()
    #st.dataframe(dft, use_container_width=True)


st.subheader("Exploration graphique du dataset")

# Colonnes pour afficher 4 graphiques
gph1, gph2 = st.columns(2)
gph3, gph4 = st.columns(2)

# 1️⃣ Boxplot des prix par catégorie
with gph1:
    st.markdown("**Distribution des prix par catégorie (Boxplot)**")
    box = alt.Chart(dft).mark_boxplot().encode(
        x='categorie:N',
        y='prix:Q',
        color='categorie:N',
        tooltip=['categorie', 'prix']
    ).properties(height=400)
    st.altair_chart(box, use_container_width=True)

# 2️⃣ Histogramme des prix
with gph2:
    st.markdown("**Histogramme des prix**")
    hist = alt.Chart(dft).mark_bar().encode(
        x=alt.X("prix:Q", bin=alt.Bin(maxbins=30), title="Prix (CFA)"),
        y='count()',
        tooltip=['count()']
    ).properties(height=400)
    st.altair_chart(hist, use_container_width=True)

st.divider()

# 3️⃣ Nombre d’articles par catégorie
with gph3:
    st.markdown("**Nombre d’articles par catégorie**")
    cat_count = dft['categorie'].value_counts().reset_index()
    cat_count.columns = ['categorie', 'count']
    bar = alt.Chart(cat_count).mark_bar().encode(
        x='categorie:N',
        y='count:Q',
        color='categorie:N',
        tooltip=['categorie', 'count']
    ).properties(height=400)
    st.altair_chart(bar, use_container_width=True)

# 4️⃣ Top 10 articles les plus chers
with gph4:
    st.markdown("**Top 10 articles les plus chers**")
    top10 = dft.nlargest(10, 'prix')
    top_bar = alt.Chart(top10).mark_bar().encode(
        x=alt.X('prix:Q', title='Prix (CFA)'),
        y=alt.Y('categorie:N', sort='-x'),
        color='categorie:N',
        tooltip=['categorie', 'prix', 'adresse']
    ).properties(height=400)
    st.altair_chart(top_bar, use_container_width=True)

st.bar_chart(dft[['prix','categorie']].value_counts().reset_index(name='count'), x='prix', y='count', color='categorie', height=600)
