import streamlit as st
import pandas as pd
from PIL import Image

# st.title("Bienvenue sur notre application de recommandation de films")

import base64


# Ne marche pas : st.write_stream('Notre application vous permet de rechercher un film selon un directeur, un acteur, un film ...' )

# def create_container_with_color(image):
bloc_image = st.container()
with bloc_image:
    # Code HTML avec style en ligne pour l'image de fond
    image_html_code = """
                            <style>
                                .button_large {
                                    border: solid;
                                    border-color: rgba(232, 229, 228);
                                    color: black;
                                    padding: 4% 5px;
                                    text-align: center;
                                    display: inline-block;
                                    font-size: 24px;
                                    font_weigt:bold;
                                    margin: 10px 20px 10px 20px ;
                                    cursor: pointer;
                                    border-radius: 20px;
                                    width : 650px;
                                    height : 100px;
                                    border-style: ridge;
                                    text-shadow: 1px 1px 2px grey;
                                    background-color: rgba(232, 229, 228, 0.5);
                                }
                                .button_small {
                                    border: solid;
                                    border-color: rgba(232, 229, 228);
                                    color: black;
                                    padding: 10px 20px 10px 20px;
                                    text-align: center;
                                    display: inline-block;
                                    font-size: 20px;
                                    font_weigt:bold;
                                    margin: 10px 5px 10px 5px;
                                    cursor: pointer;
                                    border-radius: 25px;
                                    width : 160px;
                                    height : 100px;
                                    border-style: ridge;
                                    text-shadow: 1px 1px 2px grey;
                                    background-color: rgba(232, 229, 228, 0.5);
                                }
                                .div_image {
                                    background-image: url('https://i.ibb.co/rH2JPL9/DALL-E-2025-01-02-09-36-44-A-cozy-living-room-scene-designed-for-a-movie-night-The-setup-includes-a.webp" alt="DALL-E-2025-01-02-09-36-44-A-cozy-living-room-scene-designed-for-a-movie-night-The-setup-includes-a');
                                    height: 700px;
                                    width:700px;
                                    background-size: cover;
                                    border: 2px solid #000;

                                    /* Flexbox configuration */
                                    display: flex;
                                    flex-direction: column;
                                    justify-content: flex-end; /* Mettre le contenu en bas */
                                    align-items: center; /* Centrer les boutons horizontalement */
                                    
                                }
                                #link {
                                color: black;
                                text-decoration: none;
                                }

                                h1{
                                text-align: center;
                                }

                                bouttons{
                                text-align: center;
                                }
                            </style>

                        <h1>Bienvenue sur notre application de recommandation de films</h1>
                        <div class=div_image>
                        <p class = bouttons>
                        <a id="link" href="./recommandation" class="button_large">Rechercher des films similaires</a><p>
                        <p class = bouttons>
                        <a id="link" href="./recherche_directeur" class="button_small">Rechercher par directeur</a>
                        <a id="link" href="./recherche_acteur" class="button_small">Rechercher par acteur</a>
                        <a id="link" href="./recherche_genre" class="button_small">Rechercher par genre</a>
                        <a id="link" href="./recherche_annee" class="button_small">Rechercher par année</a></p>
                        
                        </div>"""
    bloc_image.markdown(image_html_code, unsafe_allow_html=True)
        
# <a id="link" href="./statistiques.py" class="button_small">Statistiques sur nos données</a>





# col1,col2,col3 =st.columns([0.2, 0.6, 0.2])
# with col1:
#     st.write("")
# with col2:
#     st.image("streamlit\images\image_avec_texte.png", width=500)
# with col3:
#     st.write("")

# st.link_button("Par film", "./recommandation", use_container_width = True)

# col1,col2 =st.columns(2)
# with col1:
#     st.link_button("Par directeur", "./recherche_directeur", use_container_width = True)
#     st.link_button("Par acteur", "./recherche_acteur", use_container_width = True)
# with col2:
#     st.link_button("Par genre", "./recherche_genre", use_container_width = True)
#     st.link_button("Par année", "./recherche_annee", use_container_width = True)


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