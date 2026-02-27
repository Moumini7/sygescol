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
            DataViz
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


dft = manager.traitement_dataset(df)

st.markdown(f"""<div/><div/>""", unsafe_allow_html=True)
# Quelque metrique du dataset
#--------------------------------
st.markdown("""
<style>
    /* Style pour les cartes de métriques */
    [data-testid="stMetric"] {
        background-color: #f0f8f7;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #0C907C;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    /* Effet au survol : fond vert et élévation */
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 2px 5px 15px rgba(0,0,0,0.2);
        background-color: #0C907C !important;
        color: white !important;
    }

    /* Forcer le texte en blanc au survol pour tous les éléments internes */
    [data-testid="stMetric"]:hover [data-testid="stMetricLabel"],
    [data-testid="stMetric"]:hover [data-testid="stMetricValue"],
    [data-testid="stMetric"]:hover [data-testid="stMetricDelta"] div {
        color: white !important;
    }
    
    /* Optionnel : changer la couleur de la petite flèche delta en blanc aussi */
    [data-testid="stMetric"]:hover svg {
    fill: white !important;
    }
</style>
""", unsafe_allow_html=True)
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
# ... (tes imports et chargement de données restent identiques jusqu'à l'exploration)

st.subheader("Exploration graphique du dataset")

# --- HISTOGRAMME (Pleine largeur) ---
with st.container(border=True):
    st.markdown("**📊 Histogramme de la distribution des prix**")
    hist = alt.Chart(dft).mark_bar(color="#0C907C").encode(
        x=alt.X("prix:Q", bin=alt.Bin(maxbins=40), title="Prix (CFA)"),
        y=alt.Y('count()', title="Nombre d'articles"),
        tooltip=['count()']
    ).properties(height=300)
    st.altair_chart(hist, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # Petit espacement vertical

# --- PREMIÈRE LIGNE DE GRAPHIQUES (gph1, gph2) ---
gph1, gph2 = st.columns(2)

with gph1:
    with st.container(border=True):
        st.markdown("**📉 Top 10 articles les moins chers**")
        top10 = dft.nsmallest(10, 'prix')
        top_bar = alt.Chart(top10).mark_bar(color="#0D8D87").encode(
            x=alt.X('prix:Q', title='Prix (CFA)'),
            y=alt.Y('categorie:N', sort='-x', title=None),
            tooltip=['categorie', 'prix', 'adresse']
        ).properties(height=350)
        st.altair_chart(top_bar, use_container_width=True)

with gph2:
    with st.container(border=True):
        st.markdown("**📉 Top 10 articles les plus en vogue**")
        top10_cat = dft["categorie"].value_counts().reset_index().head(10)
        top10_cat.columns = ["categorie", "nombre"]
        chart = alt.Chart(top10_cat).mark_bar(color="#0D8D87").encode(
            x=alt.X("nombre:Q", title="Nombre d'articles"),
            y=alt.Y("categorie:N", sort='-x', title=None),
            tooltip=["categorie", "nombre"]
        ).properties(height=350)
        st.altair_chart(chart, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- DEUXIÈME LIGNE DE GRAPHIQUES (gph3, gph4) ---
gph3, gph4 = st.columns(2)

with gph3:
    with st.container(border=True):
        st.markdown("**📉 Top 5 des articles les mieux cotés**")
        top5_quote = dft.nlargest(5, 'prix')[['categorie', 'prix']].copy()
        top5_quote['cote'] = top5_quote['prix']
        
        donut_top5 = alt.Chart(top5_quote).mark_arc(innerRadius=70).encode(
            theta=alt.Theta(field="cote", type="quantitative"),
            color=alt.Color(field="categorie", type="nominal", 
                            legend=alt.Legend(orient="bottom", title=None),
                            scale=alt.Scale(scheme='tableau10')),
            tooltip=["categorie", "prix"]
        ).properties(height=350)
        st.altair_chart(donut_top5, use_container_width=True)

with gph4:
    with st.container(border=True):
        st.markdown("**📈 Focus sur les 3 articles stars**")
        # Correction : nlargest(3) au lieu de 33 pour respecter ton titre
        top3 = dft.nlargest(3, 'prix')[['categorie', 'prix']].copy()
        top3['cote'] = top3['prix']
        
        line_chart = alt.Chart(top3).mark_area(
            line={'color':'#0D8D87'},
            point={'color':'#0D8D87', 'size': 100},
            fillOpacity=0.2,
            color="#0D8D87"
        ).encode(
            x=alt.X('categorie:N', title="Article", sort='-y'),
            y=alt.Y('cote:Q', title="Prix / Cote"),
            tooltip=['categorie', 'prix']
        ).properties(height=350)
        st.altair_chart(line_chart, use_container_width=True)
