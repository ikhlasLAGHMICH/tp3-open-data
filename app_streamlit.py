import streamlit as st
import pandas as pd
from pathlib import Path
from utils.chatbot import DataChatbot

# Import des modules locaux
from utils.data import load_data, filter_data, get_data_summary
from utils.charts import (
    create_bar_chart, create_pie_chart, 
    create_scatter_plot, create_histogram
)

# Configuration de la page
st.set_page_config(
    page_title="Open Data Explorer",
    page_icon="📊",
    layout="wide"
)

# --- Chargement des données ---
@st.cache_data
def get_data():
    """Charge les données avec cache."""
    # Adapter le chemin à votre dataset
    data_path = Path("data/processed")
    parquet_files = list(data_path.glob("*.parquet"))
    
    if not parquet_files:
        st.error("Aucun fichier Parquet trouvé dans data/processed/")
        st.stop()
    
    return load_data(parquet_files[0])

df = get_data()

# --- Header ---
st.title("📊 Open Data Explorer")
st.markdown("*Explorez vos données Open Data de manière interactive*")

# --- Sidebar : Filtres ---
st.sidebar.header("🔍 Filtres")

# Filtre dynamique basé sur les colonnes catégorielles
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
filters = {}

for col in categorical_cols[:3]:  # Limiter à 3 filtres
    unique_values = df[col].dropna().unique().tolist()
    if len(unique_values) <= 50:  # Seulement si pas trop de valeurs
        selected = st.sidebar.multiselect(
            f"Filtrer par {col}",
            options=unique_values,
            default=[]
        )
        if selected:
            filters[col] = selected

# Appliquer les filtres
df_filtered = filter_data(df, filters) if filters else df

# --- Métriques ---
st.header("📈 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total lignes", f"{len(df_filtered):,}")
with col2:
    st.metric("Colonnes", len(df_filtered.columns))
with col3:
    numeric_cols = df_filtered.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        st.metric(f"Moyenne {numeric_cols[0]}", f"{df_filtered[numeric_cols[0]].mean():.2f}")
with col4:
    st.metric("Filtres actifs", len(filters))

# --- Visualisations ---
st.header("📊 Visualisations")

tab1, tab2, tab3 = st.tabs(["Distribution", "Comparaison", "Corrélation"])

with tab1:
    st.subheader("Distribution des valeurs")
    
    # Sélecteur de colonne
    numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Choisir une colonne", numeric_cols)
        fig = create_histogram(df_filtered, x=selected_col, title=f"Distribution de {selected_col}")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Comparaison par catégorie")
    
    if categorical_cols and numeric_cols:
        cat_col = st.selectbox("Catégorie", categorical_cols, key="cat")
        num_col = st.selectbox("Valeur", numeric_cols, key="num")
        
        agg_df = df_filtered.groupby(cat_col)[num_col].mean().reset_index()
        agg_df = agg_df.nlargest(15, num_col)
        
        fig = create_bar_chart(agg_df, x=cat_col, y=num_col, 
                               title=f"Moyenne de {num_col} par {cat_col}")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Matrice de corrélation")
    
    if len(numeric_cols) >= 2:
        from utils.charts import create_heatmap
        fig = create_heatmap(df_filtered)
        st.plotly_chart(fig, use_container_width=True)

# --- Ajouter après les visualisations ---

st.header("🤖 Assistant Data")

# Initialiser le chatbot (avec cache de session)
if "chatbot" not in st.session_state:
    st.session_state.chatbot = DataChatbot(df)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Posez une question sur les données..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtenir la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            response = st.session_state.chatbot.chat(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Bouton pour réinitialiser
if st.button("🔄 Nouvelle conversation"):
    st.session_state.chatbot.reset()
    st.session_state.messages = []
    st.rerun()
# --- Données brutes ---
st.header("🗃️ Données")

with st.expander("Voir les données brutes"):
    st.dataframe(df_filtered.head(100), use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("*Application créée dans le cadre du module Open Data & IA - IPSSI*")