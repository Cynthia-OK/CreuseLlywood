import streamlit as st
import pandas as pd

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )
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