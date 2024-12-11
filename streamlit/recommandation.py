import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from st_clickable_images import clickable_images
import pickle

# Initialisation des états de session
if "show_content" not in st.session_state:
    st.session_state.show_content = True
if "clicked" not in st.session_state:
    st.session_state.clicked = -1

def custom_clickable_images(liste_image, titles=None, div_style={}, img_style={}):
  clicked_index = clickable_images(liste_image, titles=titles, div_style=div_style, img_style=img_style)
  if clicked_index != -1:
    st.session_state.show_content = False  # Hide content immediately
    st.session_state.clicked = clicked_index  # Update clicked state
    st.rerun()  # Refresh immediately
  return clicked_index


# Titre de l'application
st.title('Bienvenue sur notre page de recommandation de films')

# Chargement des données
films = pd.read_csv('./donnees/films_genre_colonne.csv', sep="\t", low_memory=False)
films = films.drop(['Unnamed: 0', 'genres_x'], axis=1)

# Chargement du modèle
with open('modele_films_NN.pkl', 'rb') as f:
    model_charge = pickle.load(f)

# Entrée utilisateur pour le titre du film
film_cible = st.text_input('Rentrer un titre')

# Initialisation des variables globales
liste_image = []
liste_id = []
if film_cible:
    film_cible_lower = film_cible.lower()
    films['title'] = films['title'].apply(lambda x: x.lower())

    if not films['title'].str.contains(film_cible_lower).any():
        st.write(f"Le film '{film_cible}' n'est pas dans le dataset.")
    else:
        films_identiques = films['id_tmdb'][films['title'].str.contains(film_cible_lower)]
        films['poster_path'] = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + films['poster_path']

        if st.session_state.show_content:
            for i in films_identiques.index:
                link = films['poster_path'].loc[i]
                liste_image.append(link)
                liste_id.append(str(films['id_tmdb'].loc[i]))
            
            clicked = custom_clickable_images(
                liste_image,
                titles=liste_id,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},
            )

            st.session_state.clicked = clicked
            st.session_state.liste_id = liste_id
            
            if clicked != -1 and st.session_state.clicked != clicked:
            # Mettre à jour l'état et recharger immédiatement
            # st.session_state.clicked = clicked
                st.session_state.show_content = False  # Masquer le contenu

if st.session_state.show_content == False :
    # st.write('coucou')
    # st.write({st.session_state.clicked})
    id = int(st.session_state.liste_id[st.session_state.clicked])
    # st.write(f"id = {id}")
    film_choisi = films[films['id_tmdb'] == id]
    index_choisi = films[films['id_tmdb']==id].index
    index_choisi = index_choisi[0]
    chemin_image = film_choisi['poster_path'][index_choisi]          
    
    resume = film_choisi['overview'][index_choisi]
    
    annee = film_choisi['year'][index_choisi]
    

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(chemin_image, width=150)
    with col2:
        st.text(f"Résumé : {resume}")
    with col3:
        st.text(f"Année de sortie : {annee}")


    caract_film = film_choisi[['popularity', 'vote_average', 'genre_Drama', 'genre_Horror',
        'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
        'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
        'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
        'genre_War', 'genre_Documentary', 'genre_History',
        'genre_Science Fiction']]

    SN = MinMaxScaler()
    caract_film_encoded = pd.DataFrame(SN.fit_transform(caract_film), columns=caract_film.columns)
    distances, indices = model_charge.kneighbors(caract_film_encoded)

    df_resultat = films.iloc[indices[0, 1:]].reset_index(drop=True)
    st.dataframe(film_choisi)
    st.dataframe(df_resultat)
    #         # else:
    #         #     st.text("Cliquer sur une image pour afficher la description du film et les films similaires")
else:
        st.text("Veuillez saisir un titre")
