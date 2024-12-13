import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
st.title('Bienvenue sur notre page de recommandation de films')
films = pd.read_csv('./donnees/films_genre_colonne.csv', sep="\t", low_memory=False)
films =films.drop(['Unnamed: 0','genres_x'], axis=1)
import pickle
# Charger le modèle
with open('modele_films_NN.pkl', 'rb') as f: #là vous mettez l'emplacement et le nom de votre fichier pkl
    model_charge = pickle.load(f)
film_cible = st.text_input('rentrer un titre')
if film_cible:
    film_cible_lower = film_cible.lower()
    films['title']=films['title'].apply(lambda x: x.lower())
    
    
    # Vérifier si le film existe dans le dataset
    if not films['title'].str.contains(film_cible_lower).any():
        st.write(f"Le film '{film_cible}' n'est pas dans le dataset.")
    else :
        #je modifie le lien vers le poster pour qu'il fonctionne
        films_identiques = films['id_tmdb'][films['title'].str.contains(film_cible_lower)]
        films['poster_path'] = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' +films['poster_path']
        # je liste les chemins et les id des films correspondant au titre
        liste_image = []
        liste_id = []
        for i in films_identiques.index:
            link = films['poster_path'].loc[i]
            liste_image.append(link)
            liste_id.append(str(films['id_tmdb'].loc[i]))
        
         
        #j'affiche les images correspondant au titre
        from st_clickable_images import clickable_images
        clicked = clickable_images(
            liste_image,
            titles=[liste_id],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
                )
        # st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        # st.write(f"lien_image: {liste_image[clicked]}")
        # st.write(f"id_tmdb : {liste_id[clicked]}")
        if clicked > -1 :
            #je récupère id du film sélectionné
            id = int(liste_id[clicked])
            #je cherche le film choisi dans la table des films
            film_choisi = films[films['id_tmdb'] == id]
            # Récupérer les caractéristiques du film
            caract_film = film_choisi[['popularity','vote_average', 'genre_Drama', 'genre_Horror',
                    'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
                    'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
                    'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
                    'genre_War', 'genre_Documentary', 'genre_History',
                    'genre_Science Fiction']]
            index = caract_film.index
            caract_film_num = caract_film[['popularity',  'vote_average']]
            caract_film_cat = caract_film[['genre_Drama', 'genre_Horror',
                    'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
                    'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
                    'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
                    'genre_War', 'genre_Documentary', 'genre_History',
                    'genre_Science Fiction']]
                
            # je normalise les infos de mon film choisi et je cherche les films similaires
            from sklearn.preprocessing import MinMaxScaler
            SN = MinMaxScaler()
            caract_film_num_SN = pd.DataFrame(SN.fit_transform(caract_film_num), columns=caract_film_num.columns, index=index)
            caract_film_cat_dummies = pd.get_dummies(caract_film_cat)
            caract_film_encoded = pd.concat([caract_film_num_SN, caract_film_cat_dummies], axis=1)
            distances, indices = model_charge.kneighbors(caract_film_encoded)
            df_resultat = films.iloc[indices[0,1:]].reset_index(drop=True)
            st.dataframe(films[films['id_tmdb'] == id])
            st.dataframe(df_resultat)
        else:
            st.text("Cliquer sur une image pour afficher la description du film et les films similaires")
else:
    st.text('Veuillez saisir un titre')