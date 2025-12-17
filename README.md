
```markdown
# 📊 Open Data Explorer (TP3)



Application Data Interactive permettant d'explorer, de visualiser et d'interroger en langage naturel des datasets issus d'OpenFoodFacts.

Ce projet est le "Frontend" (interface utilisateur) qui consomme les données nettoyées par le pipeline ETL du TP2.

## 🌟 Fonctionnalités

- **📈 Visualisations Interactives** : 
  - Histogrammes, Bar Charts, Scatter Plots (Plotly).
  - Matrices de corrélation.
  - Cartes interactives (si données géocodées).
- **🔍 Filtres Dynamiques** : Filtrage en temps réel par marques, catégories, nutriscore, etc.
- **🤖 Assistant IA Local** : 
  - Chatbot intégré utilisant **Ollama (Mistral)**.
  - Répond aux questions sur les statistiques du dataset.
  - Fonctionne 100% en local sans clé API payante.
- **📋 Explorateur de Données** : Tableau interactif des données brutes filtrées.

## 🏗️ Architecture

```text
tp3-app/
├── app_streamlit.py    # Point d'entrée de l'application
├── .env                # Configuration (clés API optionnelles)
├── data/
│   └── processed/      # Fichiers Parquet (issus du TP2)
├── utils/
│   ├── data.py         # Chargement optimisé (DuckDB)
│   ├── charts.py       # Génération des graphiques
│   └── chatbot.py      # Module IA (Litellm + Ollama)
└── README.md
```

## 🚀 Installation

### 1. Prérequis
- Python 3.10 ou plus.
- [Ollama](https://ollama.com/) installé et lancé.

### 2. Initialisation
```bash
# Aller dans le dossier
cd tp3-app

# Installer les dépendances avec uv
uv sync
# OU avec pip
pip install streamlit pandas plotly duckdb litellm python-dotenv
```

### 3. Préparation de l'IA (Ollama)
Assurez-vous d'avoir téléchargé le modèle Mistral :
```bash
ollama pull mistral
```
*Laissez l'application Ollama tourner en arrière-plan.*

### 4. Données
Copiez vos fichiers `.parquet` générés lors du TP2 dans le dossier `data/processed/`.

## 🖥️ Utilisation

Lancer l'application Streamlit :

```bash
uv run streamlit run app_streamlit.py
```

L'interface s'ouvrira automatiquement dans votre navigateur (http://localhost:8501).

## 🤖 Comment utiliser le Chatbot ?

Allez dans l'onglet **"🤖 Chatbot IA"** et posez des questions comme :
- *"Quel est le produit le plus sucré ?"*
- *"Quelle est la moyenne des additifs ?"*
- *"Combien y a-t-il de produits Nutriscore A ?"*

Le chatbot utilise le contexte des données filtrées pour répondre précisément.

## 👤 Auteur
**Ikhlas LAGHMICH** 