import streamlit as st
import pandas as pd
import time 


# if 'first_run' not in st.session_state:
#     st.session_state.first_run = True
#     # time.sleep(3)
#     st.rerun()
# else:
#     st.session_state.first_run = False


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


# Conteneur pour la vidéo
bloc_video = st.empty()  # Crée un conteneur vide

# Afficher la vidéo
with bloc_video.container():
    st.markdown("""
    <style>
    #video-container {
        display: flex;
        justify-content: center;  
        align-items: center;      
        height: 100vh;            
    }

    </style>
    <div id="video-container">
        <iframe width="1120" height="630"
            src="https://www.youtube.com/embed/XVEflECtfBM?enablejsapi=1&autoplay=1&controls=0&si=rKe9e2NgaHpaMHpG" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            referrerpolicy="strict-origin-when-cross-origin" 
            allowfullscreen>
        </iframe>
    </div>
        """, unsafe_allow_html=True)
    

# Attendre 10 secondes
time.sleep(10)

# Vider le conteneur (supprime la vidéo)
bloc_video.empty()


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
                                    height: 550px;
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
                                h2{
                                text-align: center;
                                }

                                bouttons{
                                text-align: center;
                                }
                            </style>
                        <h1>CreuseLlywood</h1>
                        <h2>La magie du cinéma à la sauce creusoise</h2>
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

