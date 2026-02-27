import streamlit as st
import time
from pathlib import Path
from models.models import Strmlit_DBManager, Styles_manager, DataStats

db_manager = Strmlit_DBManager()
Styles_manager.load_css()



st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            Paramètres
        </h1> 
        <span style="margin-rigth: 10px;"> 
            Configuration des paramètres de collecte des données avec BeautifulSoup  
        </span>
</div>
""", unsafe_allow_html=True)



# uploader un nouveau dataset
#--------------------------------
st.subheader("Téléversez un dataset collécté avec Web Scraper")

uploaded_files = st.file_uploader(
    "Téléverser",
    type=["csv"],
    accept_multiple_files=True
)

# parent.parent -> sygesco_app
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "data_ws"
DATA_DIR.mkdir(exist_ok=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = DATA_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.rerun()
    st.success(f"{len(uploaded_files)} fichier(s) téléversé(s) avec succès !")

st.divider()


# Supprimer un dataset
#--------------------------------
st.subheader("Supprimer un dataset")
files = list(DATA_DIR.glob("*.csv"))

if not files:
    st.warning("Aucun fichier disponible.")
else:
    file_names = [f.name for f in files]
    selected_file = st.selectbox(
        "Sélectionner un dataset à supprimer",
        file_names
    )
    st.error(f"Attention : Cette action supprimera définitivement le fichier '{selected_file}' du dossier data_ws.")
    if st.button("Supprimer le fichier", type="primary", icon="🗑️"):
        @st.dialog("Confirmation de suppression")
        def confirm_delete():
            st.warning(f"Voulez-vous vraiment supprimer : {selected_file} ?")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Oui, supprimer", type="primary"):
                    file_path = DATA_DIR / selected_file
                    file_path.unlink()
                    st.success("Fichier supprimé avec succès.")
                    st.rerun()

            with col2:
                if st.button("Annuler"):
                    st.rerun()
        confirm_delete()

st.divider()

# Vider la base de données
#--------------------------------
st.subheader("Gestion de la Base de Données")
st.error("Cette action supprimera toutes les lignes stockées dans la table SQL.")

if st.button("Vider la base de données", type="primary", icon="🗑️"):
    
    @st.dialog("Confirmation de vidange")
    def confirm_clear_db():
        st.error("Êtes-vous sûr de vouloir supprimer TOUTES les données de la base ? Cette action est irréversible.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmer la vidange", type="primary", use_container_width=True):
                success = DataStats.clear_database() # Appel de la fonction créée plus haut
                success
                if success:
                    st.success("La base de données a été vidée.")
                    st.rerun()
                else:
                    st.error("Une erreur est survenue.")
        
        with col2:
            if st.button("Annuler", use_container_width=True):
                st.rerun()
    
    confirm_clear_db()