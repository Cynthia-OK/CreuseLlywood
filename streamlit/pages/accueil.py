import streamlit as st
import pandas as pd
from PIL import Image

st.title("Bienvenue sur notre application de recommandation de films")


# Ne marche pas : st.write_stream('Notre application vous permet de rechercher un film selon un directeur, un acteur, un film ...' )


col1,col2,col3 =st.columns([0.2, 0.6, 0.2])
with col1:
    st.write("")
with col2:
    st.image("streamlit\images\image_avec_texte.png", width=500)
with col3:
    st.write("")

st.link_button("Par film", "./recommandation", use_container_width = True)

col1,col2 =st.columns(2)
with col1:
    st.link_button("Par directeur", "./recherche_directeur", use_container_width = True)
    st.link_button("Par acteur", "./recherche_acteur", use_container_width = True)
with col2:
    st.link_button("Par genre", "./recherche_genre", use_container_width = True)
    st.link_button("Par année", "./recherche_annee", use_container_width = True)


# # Fonction pour lire le contenu HTML
# def lire_html(fichier):
#     with open(fichier, 'r', encoding='utf-8') as f:
#         return f.read()

# # Lire le fichier HTML
# contenu_html = lire_html(r"Live Streamlit WCS 2\pages\fichier.html")

# # Afficher le contenu HTML dans Streamlit
# st.markdown(contenu_html, unsafe_allow_html=True)

# # HTML avec la classe CSS appliquée
# st.markdown('<div class="custom-css">Texte avec CSS personnalisé 1</div>', unsafe_allow_html=True)

# st.markdown('<div class="custom-css2">Texte avec CSS personnalisé 2</div>', unsafe_allow_html=True)