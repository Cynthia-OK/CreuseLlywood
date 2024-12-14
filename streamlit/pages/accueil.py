import streamlit as st
import pandas as pd

st.title("Bienvenue sur notre application de recommandation de films")


# Ne marche pas : st.write_stream('Notre application vous permet de rechercher un film selon un directeur, un acteur, un film ...' )




# pages = {
#     "Accueil" : [
#         st.Page("./accueil.py", title="Accueil", icon="🏠"),
#         ],
#     "Statistiques": [
#         st.Page("./pages/statistiques.py", title="Page de statistiques", icon="📊"),
#     ],
#     "Recommandations": [
#         st.Page("./pages/recommandation.py", title="Recherche de films similaires par titre", icon="🎞️"),
#         st.Page("./pages/recherche_directeur.py", title="Recherche de films par directeur", icon="📽️"),
#         st.Page("./pages/recherche_acteur.py", title="Recherche de films par acteur", icon="🎭"),
#         st.Page("./pages/recherche_genre.py", title="Recherche de films par genre", icon="💥"),
#         st.Page("./pages/recherche_annee.py", title="Recherche de films par année", icon="📅"),
        
#     ],
# }

# pg = st.navigation(pages)
# pg.run()

st.image("dossier_a_ignorer\images\image_avec_texte.png")

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