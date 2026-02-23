from pathlib import Path

import streamlit as st
from models.models import Styles_manager

Styles_manager.load_css()

st.markdown(f"""
<div class="metric-card metric-card-green">
        <h1 style="margin-bottom: 10px; margin-bottom: -15px;">
            À Propos de SYGESCOL
        </h1> 
        <span style="margin-rigth: 10px;"> 
            À Propos de l’Application SYGESCOL : Système de Gestion de Collect et d'Exploration de Données  
        </span>
</div>
""", unsafe_allow_html=True)

st.header("A Propos de l'Application SYGESCOL")
# ----------------------------------------------------
# 1 Présentation Générale
# ----------------------------------------------------
with st.expander("Présentation Générale"):
    st.markdown("""
    Cette application a été développée dans le cadre d’un projet de Data Collection et d’analyse de données.
    Elle permet de collecter, centraliser, nettoyer et analyser des datasets issus du plugin Web Scraping 
    et de la bibliothèque BeautifulSoup, BeautifulSoup à travers une interface interactive et structurée.

    **Problématique adressée :**
    - Centralisation des données collectées
    - Organisation des fichiers
    - Simplification de l’analyse exploratoire
    """)

# ----------------------------------------------------
# 2 Objectifs du Projet
# ----------------------------------------------------
with st.expander("Objectifs du Projet"):
    st.markdown("""
    De manière général l'objection est de faire une retrospective complète 
    des technologies et méthodologies utilisées pour la collecte et le traitement de données, 
    l'organisation et l'analyse de données à travers une application interactive avec le framework [Streamlit](https://streamlit.io) en :
                
    - Automatisant la collecte de données via BeautifulSoup ou Selenium
    - Visualisant les brutes datasets collectés de manière interactive avec Web Scraper  
    - Centralisant les datasets dans une structure organisée  
    - Facilitant le nettoyage et la préparation des données  
    - Améliorerant la qualité et la fiabilité des analyses  
    - Offrant un tableau de bord interactif pour la visualisation  
    """)

# ----------------------------------------------------
# 3 Fonctionnalités Principales
# ----------------------------------------------------
with st.expander("Fonctionnalités Principales"):
    st.markdown("""
    ### Gestion des Datasets
    - Collecte automatique et interactifs de datasets sur le site [Coin Afrique](https://www.coinafrique.com) 
    - Téléversement de fichiers CSV  
    - Suppression sécurisée avec confirmation  
    - Organisation automatique des données 
    - sauvegarder des données collecter dans une base de données 

    ### Analyse de Données
    - Nettoyage des données  
    - Gestion des valeurs manquantes  
    - Visualisations statistiques  

    ### Dashboard
    - Indicateurs clés  
    - Statistiques dynamiques  
    - Synthèse des datasets  
    """)

# ----------------------------------------------------
# 4 Architecture Technique
# ----------------------------------------------------
with st.expander("Architecture Technique"):
    st.markdown("""
    **Technologies et Bibliothèque utilisées :**
    - Python  
    - Streamlit  
    - Pandas  
    - BeautifulSoup  
    - Selenium  
    - os 
    - sys
    - time
    - pathlib
    - Scikit-learn  

    **Organisation du projet :**
    - Dossier structuré par modules  
    - Séparation logique des pages  
    - Gestion centralisée des données  
    """)


    {
  "Organisation du projet : SYGESCO_APP": {
    "data": {
      "data_bs": {},
      "data_ws": {},
      "streamlit_.db": "file"
    },
    "models": {
      "models.py": "file"
    },
    "pages": {
      "1_Sracping avec BeautifulSou.py": "file",
      "2_Afficher datasets de Web S..py": "file",
      "3_Visualiser les Datasets de ..py": "file",
      "4_Feedback.py": "file",
      "5_A Propos.py": "file",
      "README.md": "file"
    },
    "utils": {
      "styles.css": "file"
    },
    "app.py": "file",
    "models.py": "file",
    "README.md": "file",
    "requirements.txt": "file",
  }
}
# ----------------------------------------------------
# 5 Auteur
# ----------------------------------------------------
with st.expander("Auteur"):
    st.markdown("""
    Projet développé dans le cadre académique en Master 1 Intelligence  Artificielle pour le cours de Data Collection.
    
    **Auteur :** [SAWADOGO Moumini]
    **Email :** [moumini.sawadogo@mail.dit.sn]
    """)

with st.expander("Licence"):
    st.markdown("""© 2026 SYGESCOL. Tous droits réservés.""", unsafe_allow_html=True)




st.header("Implementation Technique")

# ----------------------------------------------------
# 1. Gestion de la Base de Données
# ----------------------------------------------------
with st.expander("Gestion modularisée du code et de la structure du projet"):
    st.write("Cette classe  toutes les fonctions liées à la gestion de la base de données SQLite utilisée pour stocker les données collectées.")

    st.code("""
class Strmlit_DBManager:
    def __init__(self, db_name="streamlit_.db"):
        current_dir = Path(__file__).resolve().parent.parent
        data_dir = current_dir / "data"
        data_dir.mkdir(exist_ok=True)

        self.db_name = str(data_dir / db_name)
        self.data_folder = data_dir / "data_bs"
    """, language="python")

    st.info(""" Elle permet de :
    - Créer la base de données et les tables nécessaires
    - Utilision un chemin absolu pour éviter les erreurs d’accès aux fichiers  
    - Crée automatiquement le dossier data s’il n’existe pas  
    - Centralise les ressources (BD + CSV)
    """)

# ----------------------------------------------------
# 2. Création de la base de données
# ----------------------------------------------------
with st.expander("Création de la base de données"):
    
    st.code("""
    def create_streamlit_bd(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS strml_td (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categorie TEXT,
                type TEXT,
                prix REAL,
                adresse TEXT,
                lien TEXT,
                date_collecte TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        \"\"\")
        conn.commit()
        conn.close()
    """, language="python")

    st.info("""
    - Création d’une table `strml_td` pour stocker les données collectées
    - Utilisation de types de données appropriés pour chaque champ
    """)

# ----------------------------------------------------
# 3. Traitement des Données
# ----------------------------------------------------
with st.expander("Initialisation de la base de données"):
    st.write("Les données collectées sont nettoyées avant analyse.")

    st.code("""
# Vérifier si la base de données existe
def db_exists(self):
    return os.path.exists(self.db_name)


# Initialiser la connexion à la base SQLite
def init_streamlit_bd(self):

    # Vérifie l'existence de la base
    if not self.db_exists():
        # Création automatique si absente
        self.create_streamlit_bd()

    # Ouverture de la connexion
    return sqlite3.connect(self.db_name)
            

# Lire toutes les données de la BD
  def read_streamlit_bd(self):
      try:
          conn = self.init_streamlit_bd()
          data_read = pd.read_sql_query("SELECT * FROM strml_td", conn)
          conn.close()
          return data_read if not data_read.empty else "La table est vide."
      except sqlite3.Error as e:
          return f"Erreur BD : {e}"
""", language="python")

    st.info("""
    Fonctionnement global :

    - db_exists() vérifie si le fichier de base SQLite est présent  
    - Si la base n’existe pas → elle est créée automatiquement  
    - La fonction retourne ensuite une connexion prête à l’emploi  
    - Évite toute erreur lors du premier lancement de l’application
    - read_streamlit_bd() utilise cette connexion pour lire les données et les retourner sous forme de DataFrame  

    Ce mécanisme rend l’application autonome : aucune configuration
    manuelle de la base n’est nécessaire.
    """)

# ----------------------------------------------------
# 4. Collecte de données avec BeautifulSoup
# ----------------------------------------------------
with st.expander("La methode centrale de scraping"):
    st.write(" Cette fonction permet la collectte effective des données.")

    st.code('''
def chargementData(self, categorie, nombre_pages):
    # Initialisation
    conn = self.init_streamlit_bd()
    cursor = conn.cursor()
    base_url = "https://sn.coinafrique.com/categorie/"
    items = []

    for i in range(nombre_pages):
        page_url = f"{base_url}{categorie}?page={i+1}"
        try:
            res = get(page_url, timeout=30)
            soup = bs(res.content, "html.parser")
            containers = soup.find_all("div", class_="col s6 m4 l3")
        except Exception:
            break

        if not containers:
            break

        for container in containers:
            try:
                # Extraction des données
                type_habit = container.find("p", class_="ad__card-description").get_text(strip=True)
                prix_text = container.find("p", class_="ad__card-price").get_text(strip=True)
                
                # Nettoyage robuste du prix (enlève CFA, les espaces classiques et insécables)
                prix_clean = prix_text.replace("CFA", "").replace(" ", "").replace("\\xa0", "")
                prix = float(prix_clean)
                
                adresse = container.find("p", class_="ad__card-location").get_text(strip=True)
                
                # Récupération de l'image
                img_tag = container.find("img", class_="ad__card-img")
                lien = img_tag["src"] if img_tag else "Pas d'image"

                # Insertion SQL
                cursor.execute("""
                    INSERT INTO strml_td (categorie, type, prix, adresse, lien)
                    VALUES (?, ?, ?, ?, ?)
                """, (categorie, type_habit, prix, adresse, lien))

                items.append({
                    "categorie": categorie,
                    "type": type_habit,
                    "prix": prix,
                    "adresse": adresse,
                    "lien": lien
                })

            except (AttributeError, ValueError, TypeError):
                continue # Passe à l'annonce suivante en cas d'erreur de parsing

    # Finalisation
    conn.commit()
    conn.close()

    if items:
        df = pd.DataFrame(items)
        # Sauvegarde CSV
        filename = self.data_folder / f"{categorie}_data.csv" # Ajout du prefixe 'ws' comme demandé plus tôt
        df.to_csv(filename, index=False)
        return df
    else:
        return pd.DataFrame() # Retourne un DF vide si rien n'est trouvé
''', language="python")
    st.info("""
    Fonctionnement global :

    - Récupère les annonces depuis le site CoinAfrique  
    - Parcourt plusieurs pages de résultats  
    - Extrait les informations essentielles :
       • catégorie    
       • prix  
       • localisation  
       • image  

    - Insère les données dans la base SQLite  
    - Construit un DataFrame Pandas  
    - Sauvegarde les données en fichier CSV  
    - Retourne les données pour affichage immédiat  

    Elle implement les méthodes citées plus haut. La collecte s’arrête automatiquement si aucune annonce n’est trouvée.
    """)

# ----------------------------------------------------
# 5. Interface et Styles
# ----------------------------------------------------
with st.expander("Personnalisation de l’interface"):
    st.write("Gestion du style et de l’identité visuelle.")

    st.code("""
class Styles_manager:

    @staticmethod
    def load_css():

        # 1️ Configuration de la page (DOIT ÊTRE EN PREMIER)
        st.set_page_config(
            page_title="Système de Gestion de collecte de Données",
            layout="wide",
            page_icon="🧊"
        )

        # 2️ Chargement de bibliothèques externes (icônes, fonts)
        st.markdown(\"\"\"
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        \"\"\", unsafe_allow_html=True)

        # 3️ Logo personnalisé
        LOGO_PATH = "images/sygescol_ltd.png"

        st.markdown(f\"\"\"
            <style>
                [data-testid="stLogo"] {{ height: 5rem; width: auto; }}
            </style>
        \"\"\", unsafe_allow_html=True)

        st.logo(LOGO_PATH, icon_image=LOGO_PATH, size="large")

        # 4️ Chargement d'un CSS externe
        current_dir = Path(__file__).resolve().parent.parent
        css_file = current_dir / "utils" / "styles.css"

        if css_file.exists():
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            st.warning(f"Le fichier CSS est introuvable : {css_file}")
""", language="python")

    st.info("""
    Fonctionnement détaillé :

    1️ `st.set_page_config()` configure le titre, l’icône et le layout  
    2️ Font Awesome est chargé pour utiliser des icônes facilement  
    3️ Le logo est ajouté avec une taille personnalisée grâce à un petit hack CSS  
    4️ Un fichier CSS externe (`styles.css`) est appliqué pour styliser l’interface  
    5️ Vérification de l’existence du fichier CSS pour éviter les erreurs  

    Résultat : une interface responsive, esthétique et brandée, prête pour le dashboard.
    """)