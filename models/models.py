import os
import sqlite3
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
from pathlib import Path
import streamlit as st
import time

class Strmlit_DBManager:

    '''
        Le grand soucis pour cette partie était le chémin rélatif et chemin absolu
        nous avons choisi l'option du chemin absolu car nous avons réparqué que quant 
        option est mis sur chémin rélatif, il indexe mal les ressources(fichiers et dossiers)
    '''
    def __init__(self, db_name="streamlit_.db"):
            # On récupère le nom du dossier actuel et on crée un chemin vers /data (data_dir) -> pour les csv
            current_dir = Path(__file__).resolve().parent.parent
            data_dir = current_dir / "data"  
            data_dir.mkdir(exist_ok=True) #On crée le dossier s'il n'existe pas
            
            # pour la BD
            self.db_name = str(data_dir / db_name)
            
            # Pour les CSV 
            self.data_folder = data_dir / "data_bs"

    # Vérifier si la BD existe
    def db_exists(self):
        return os.path.exists(self.db_name)

    # Créer la BD et la table
    def create_streamlit_bd(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strml_td (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categorie TEXT,
                type TEXT,
                prix REAL,
                adresse TEXT,
                lien TEXT,
                date_collecte TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    # Initialiser la connexion
    def init_streamlit_bd(self):
        if not self.db_exists():
            self.create_streamlit_bd()
        return sqlite3.connect(self.db_name)

    # Lire les données
    # Lire toutes les données de la BD
    def read_streamlit_bd(self):
        try:
            conn = self.init_streamlit_bd()
            data_read = pd.read_sql_query("SELECT * FROM strml_td", conn)
            conn.close()
            return data_read if not data_read.empty else "La table est vide."
        except sqlite3.Error as e:
            return f"Erreur BD : {e}"

    # Traitement de données
    def traitement_dataset(self, df):

        df = df.copy()

        # Nettoyage prix
        df["prix"] = (df["prix"].astype(str).str.replace(r"[^\d]", "", regex=True))
        df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
        
        # Remplacer NaN par la médiane pour éviter les problèmes de type et de valeurs aberrantes
        df["prix"] = df["prix"].fillna(df["prix"].median())

        # Suppression valeurs aberrantes (méthode robuste)
        df["prix"] = df["prix"].clip(
            lower=df["prix"].quantile(0.01),
            upper=df["prix"].quantile(0.99)
        )

        df["prix"] = df["prix"].astype(int)

        # Adresse
        df["adresse"] = df["adresse"].fillna(df["adresse"].mode()[0])

        # Suppression colonnes inutiles
        df = df.drop(
            columns=["web_scraper_order", "web_scraper_start_url"],
            errors="ignore"
        )

        df.rename(columns={df.columns[0]: "categorie"}, inplace=True)

        return df.reset_index(drop=True)

    # Scraping + insertion
    def chargementData(self, categorie, nombre_pages):
            
        conn = self.init_streamlit_bd()
        cursor = conn.cursor()
        base_url = 'https://sn.coinafrique.com/categorie/'
        items = []

        for i in range(nombre_pages):
            page_url = f"{base_url}{categorie}?page={i+1}"
            res = get(page_url, timeout=60)
            soup = bs(res.content, 'html.parser')
            containers = soup.find_all('div', class_='col s6 m4 l3')

            if not containers:
                break

            for container in containers:
                try:
                    type_habit = container.find('p', class_='ad__card-description').get_text(strip=True)
                    prix_text = container.find('p', class_='ad__card-price').get_text(strip=True)
                    prix = float(prix_text.replace('CFA', '').replace(' ', ''))
                    adresse = container.find('p', class_='ad__card-location').get_text(strip=True)

                    lien = container.find('img', class_='ad__card-img')['src']

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

                except (AttributeError, ValueError):
                    continue
            
            #pour les anti blocage du site
            time.sleep(2)

        conn.commit()
        conn.close()
        df = pd.DataFrame(items)

        #filename = f"streamlit_collect/data/{categorie}_data_collected.csv"
        
        filename = self.data_folder / f"{categorie}_data_collected.csv"
        df.to_csv(filename, index=False)
        return df


class Styles_manager:

    @staticmethod
    def load_css():
        # 1. DOIT ÊTRE EN PREMIER
        st.set_page_config(
            page_title="Système de Gestion de collecte de Données",
            layout="wide",
            page_icon="🧊"
        )
        
        # 2. Ensuite les autres composants
        st.markdown("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            """, unsafe_allow_html=True)
        
        LOGO_PATH = "images/sygescol_ltd.png"
        st.logo(LOGO_PATH, icon_image=LOGO_PATH, size="large")
        
        current_dir = Path(__file__).resolve().parent.parent
        css_file = current_dir / "utils" / "styles.css"

        if css_file.exists():
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            st.warning(f"Le fichier CSS est introuvable : {css_file}")


class DataStats:
    @st.cache_data(ttl=120)
    @staticmethod
    def count_files(folder_path):
        try:
            return len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        except FileNotFoundError:
            return 0

    @staticmethod
    @st.cache_data(ttl=120)
    def total_rows(folder_path):
        total = 0
        try:
            for f in os.listdir(folder_path):
                file_path = os.path.join(folder_path, f)
                if os.path.isfile(file_path) and f.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    total += len(df)
            return total
        except Exception as e:
            return 0

    @staticmethod
    @st.cache_data(ttl=120)
    def get_table_data(db_name="streamlit_.db", table_name="strml_td"): # Mis à jour en 'tb'
        current_dir = Path(__file__).resolve().parent.parent
        data_dir = current_dir / "data"  
        db_path = os.path.join(data_dir, db_name)
        
        if not os.path.exists(db_path):
            return f"Erreur : Le fichier {db_path} est introuvable."

        try:
            with sqlite3.connect(db_path) as conn:
                query = f"SELECT * FROM {table_name}"
                return pd.read_sql_query(query, conn)
        except Exception as e:
            return f"Une erreur est survenue : {e}"
    
    @staticmethod
    def clear_database(db_name="streamlit_.db", table_name="strml_td"):
        current_dir = Path(__file__).resolve().parent.parent
        data_dir = current_dir / "data"
        db_path = os.path.join(data_dir, db_name)

        if not os.path.exists(db_path):
            return False

        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table_name}")
                conn.commit()
                st.cache_data.clear() 
                return True
        except Exception as e:
            print(f"Erreur lors de la vidange : {e}")
            return False