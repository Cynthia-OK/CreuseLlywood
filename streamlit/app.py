import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CreuseLlywood", 
    page_icon="https://img.freepik.com/vecteurs-libre/concept-cinema_1284-12713.jpg", 
    layout="wide", 
    initial_sidebar_state="expanded"
) 


pages = {
    "Accueil" : [
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

st.sidebar.image("https://i.ibb.co/zmKy2qC/cinema.jpg")

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
        font-size : 20px;
        color: #97958d;
        font-weight : bold;
    }


</style>
"""

# Injecter le CSS dans l'application Streamlit
st.markdown(sidebar_css, unsafe_allow_html=True)


