# SyGesCo_App
#Collecte, Stockage et Analyse de Données d’Annonces en Ligne

## Projet académique — Master Intelligence Artificielle / Data Science
---
## Description du projet
Ce projet consiste à concevoir un système complet de collecte automatisée, de collect, stockage et d’analyse de données issues d’annonces en ligne .  
- url1 : https://sn.coinafrique.com/categorie/vetements-homme
- url2 : https://sn.coinafrique.com/categorie/vetements-enfants
- url3 : https://sn.coinafrique.com/categorie/chaussures-homme
- url4 : https://sn.coinafrique.com/categorie/chaussures-enfants

L’objectif est de démontrer la maîtrise des techniques de :
- Web scraping
- Prétraitement de données
- Stockage en base de données
- Analyse statistique
- Visualisation interactive
- Développement d’une application data

L’application permet d’extraire des annonces par catégorie, de les enregistrer dans une base SQLite persistante et de produire des analyses visuelles à l’aide d’une interface interactive.
---

## Objectifs pédagogiques
- Acquisition automatisée de données non structurées
- Nettoyage et transformation de données
- Modélisation d’une base de données relationnelle
- Manipulation de données avec Pandas
- Visualisation de données
- Développement d’une application interactive
- Reproductibilité expérimentale

---

## Méthodologie

1. Collecte des données (web scraping multi‑pages)  
2. Prétraitement et nettoyage  
3. Stockage en base SQLite  
4. Analyse exploratoire  
5. Visualisation interactive  

---

## Architecture du système
"Organisation du projet : SYGESCO_APP":{
	"data":{
		"data_bs":{}
		"data_ws":{}
		"streamlit_.db":"file"
	}
	"models":{
		"models.py":"file"
	}
	"images":{
		"sygescol.png":"file"
	}
	"pages":{
		"1_Sracping avec BeautifulSou.py":"file"
		"2_Afficher datasets de Web S..py":"file"
		"3_Visualiser les Datasets de ..py":"file"
		"4_Feedback.py":"file"
		"5_A Propos.py":"file"
		"README.md":"file"
		}
	"utils":{
		"styles.css":"file"
	}
	"app.py":"file"
	"README.md":"file"
	"requirements.txt":"file"
}


---

## 🗄Modèle de données

Table principale : strml_td

| Champ         | Type      | Description |
|--------------|-----------|-------------|
| id           | INTEGER   | Identifiant |
| categorie    | TEXT      | Catégorie   |
| type         | TEXT      | Description |
| prix         | REAL      | Prix        |
| adresse      | TEXT      | Localisation|
| lien         | TEXT      | Lien/image  |
| date_collecte| TIMESTAMP | Date        |

---

## Technologies utilisées

- Python 3.x
- Streamlit
- SQLite
- Pandas
- BeautifulSoup
- Requests

---

## Installation

pip install -r requirements.txt

---

## ▶Lancer l’application

streamlit run app.py

---

## Analyses possibles

- Distribution des prix
- Annonces par catégorie
- Prix moyen et médian
- Comparaisons entre catégories

---

## Reproductibilité

- Base : data/streamlit_.db
- CSV : data/data_bs/
- CSV : data/data_ws/

---

## Limites

- Données dépendantes du site source
- Base locale uniquement
- Pas de déduplication avancée

---

## Perspectives

- Machine Learning prédictif
- Déploiement cloud
- Dashboard avancé
- Collecte automatisée

---

## Cadre académique

Projet réalisé dans le cadre du Master Intelligence Artificielle / Data Science.

---

## Master I

Usage académique.
