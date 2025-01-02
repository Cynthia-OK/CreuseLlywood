import streamlit as st
import pandas as pd

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
                                    margin-left: auto;
                                    margin-right: auto;
                                    border-radius: 25px;

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
        

# CSS personnalisé
sidebar_css = """
<style>
    [data-testid="stSidebar"] {
        background-image: url('http://blog.ac-versailles.fr/cineblog/public/cinema.jpg');
        background-size: cover; /* Adapte l'image pour couvrir tout l'espace */
        background-repeat: no-repeat; /* Ne répète pas l'image */
        background-position: center; /* Centre l'image */
        color: blue;
    }

</style>
"""

# Injecter le CSS dans l'application Streamlit
st.markdown(sidebar_css, unsafe_allow_html=True)


# CSS pour personnaliser les liens dans la sidebar uniquement
sidebar_link_css = """
<style>
    [data-testid="stSidebar"] a {
        color: #F39C12; /* Couleur des liens dans la sidebar */
        text-decoration: none; /* Supprime le soulignement */
    }
    [data-testid="stSidebar"] a:hover {
        color: #FF5733; /* Couleur lors du survol dans la sidebar */
    }
</style>
"""

# Injecter le CSS
st.markdown(sidebar_link_css, unsafe_allow_html=True)