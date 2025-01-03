import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CreuseLlywood", 
    page_icon="https://img.freepik.com/vecteurs-libre/concept-cinema_1284-12713.jpg", 
    layout="wide", 
    initial_sidebar_state="expanded"
)


css = """
<style>
    body {
        background-image: url('https://i.ibb.co/zXHpqqh/fond-films.png');
        background-size: cover; /* Adapte l'image pour couvrir tout l'espace */
        background-repeat: no-repeat; /* Ne répète pas l'image */
        background-position: center; /* Centre l'image */
        opacity: 0.9;
        height: 100vh; /* Assure que le fond couvre toute la fenêtre */
        margin: 0;
    }
</style>
"""

# Injecter le CSS dans l'application Streamlit
st.markdown(css, unsafe_allow_html=True)


# CSS personnalisé
sidebar_css = """
<style>
    [data-testid="stSidebar"] {
        background-image: url('https://i.ibb.co/zmKy2qC/cinema.jpg');
        background-size: cover; /* Adapte l'image pour couvrir tout l'espace */
        background-repeat: no-repeat; /* Ne répète pas l'image */
        background-position: center; /* Centre l'image */
        opacity: 0.9;
    }
    [data-testid="stSidebarNavLink"] {
        background-color: #cbc7c5;
        color: #787574;
    }
    [data-testid="stSidebarNavLink"] span {
        color: #787574;
    }
    [data-testid="stNavSectionHeader"] {
        font-size: 20px;
        color: #97958d;
        font-weight: bold;
    }
    /* Ajout de styles pour le titre personnalisé */
    .custom-title {
        font-size: 24px;
        font-weight: bold;
        color: #4d4b47;
        margin-bottom: 10px;
        text-align: center;
    }
    .custom-text {
        font-size: 16px;
        color: #4d4b47;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
"""

# Injecter le CSS dans l'application Streamlit
st.sidebar.markdown(sidebar_css, unsafe_allow_html=True)

# Ajouter un titre ou un texte au-dessus du menu via HTML
custom_header_html = """
<div>
    <div class="custom-title">Bienvenue sur CreuseLlywood 🎥</div>
    <div class="custom-text">La magie du cinéma à la sauce creusoise</div>
</div>
"""
st.sidebar.markdown(custom_header_html, unsafe_allow_html=True)

# Ajouter une image dans la sidebar
st.sidebar.image('https://i.ibb.co/PcXJqCd/creusellywood.jpg')

# Gestion des pages
pages = {
    "CreuseLlywood": [
        st.Page("./pages/accueil.py", title="Accueil", icon="🏠"),
    ],
    "Statistiques": [
        st.Page("./pages/statistiques.py", title="Page de statistiques", icon="📊"),
    ],
    "Recommandations": [
        st.Page("./pages/recommandation.py", title="Recherche de films similaires par titre", icon="🎞️"),
        st.Page("./pages/recherche_directeur.py", title="Recherche de films par directeur", icon="📽️"),
        st.Page("./pages/recherche_acteur.py", title="Recherche de films par acteur", icon="🎭"),
        st.Page("./pages/recherche_genre.py", title="Recherche de films par genre", icon="💥"),
        st.Page("./pages/recherche_annee.py", title="Recherche de films par année", icon="📅"),
    ],
}

pg = st.navigation(pages)
pg.run()
