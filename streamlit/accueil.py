import streamlit as st
import pandas as pd

st.title("Bienvenue sur notre application de recommandation de films")


st.write_stream('Notre application vous permet de rechercher un film selon un directeur, un acteur, un film ...' )

st.image("dossier_a_ignorer\images\image_avec_texte.png")


pages = {
    "Statistiques": [
        st.Page("statistiques.py", title="Page de statistiques"),
    ],
    "Recommandations": [
        st.Page("recommandation.py", title="Recherche de films similaires par titre"),
        st.Page("recherche_directeur.py", title="Recherche de films par directeur"),
        st.Page("recherche_acteur.py", title="Recherche de films par acteur"),
        st.Page("recherche_genre.py", title="Recherche de films par acteur"),
        st.Page("recherche_annee.py", title="Recherche de films par acteur"),
        
    ],
}

pg = st.navigation(pages)
pg.run()



# Fonction pour lire le contenu HTML
def lire_html(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Lire le fichier HTML
contenu_html = lire_html(r"Live Streamlit WCS 2\pages\fichier.html")

# Afficher le contenu HTML dans Streamlit
st.markdown(contenu_html, unsafe_allow_html=True)

# HTML avec la classe CSS appliquée
st.markdown('<div class="custom-css">Texte avec CSS personnalisé 1</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-css2">Texte avec CSS personnalisé 2</div>', unsafe_allow_html=True)