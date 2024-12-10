import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pickle
from sklearn.preprocessing import MinMaxScaler

films = pd.read_csv("./donnees/films_genre_colonne.csv", sep='\t', low_memory=False)
# Charger le modèle
with open('modele_films_nn.pkl', 'rb') as f: #là vous mettez l'emplacement et le nom de votre fichier pkl
    model_charge = pickle.load(f)
caracteristiques = ['popularity','vote_average', 'genre_Drama', 'genre_Horror',
       'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
       'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
       'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
       'genre_War', 'genre_Documentary', 'genre_History',
       'genre_Science Fiction']

def films_similaires(tmdb):
  films_cible = films[films['id_tmdb'] == tmdb]
  caract_film = films[films['id_tmdb']==tmdb][[ 'popularity', 'vote_average', 'genre_Drama', 'genre_Horror',
       'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
       'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
       'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
       'genre_War', 'genre_Documentary', 'genre_History',
       'genre_Science Fiction']]
  index = caract_film.index
  caract_film_num = caract_film[['popularity','vote_average']]
  caract_film_cat = caract_film[[ 'genre_Drama', 'genre_Horror',
       'genre_Thriller', 'genre_Crime', 'genre_Animation', 'genre_Mystery',
       'genre_Family', 'genre_Western', 'genre_Adventure', 'genre_Action',
       'genre_Fantasy', 'genre_Comedy', 'genre_Music', 'genre_Romance',
       'genre_War', 'genre_Documentary', 'genre_History',
       'genre_Science Fiction']]
  from sklearn.preprocessing import MinMaxScaler
  SN = MinMaxScaler()
  caract_film_num_SN = pd.DataFrame(SN.fit_transform(caract_film_num), columns=caract_film_num.columns, index=index)

  caract_film_cat_dummies = pd.get_dummies(caract_film_cat)
  caract_film_encoded = pd.concat([caract_film_num_SN, caract_film_cat_dummies], axis=1)




  # Vérifier si le film existe dans le dataset
  if tmdb not in films['id_tmdb'].values:
      return f"Le film {tmdb} n'est pas dans le dataset."

  # Récupérer les caractéristiques du film
  film_cible = films[films['id_tmdb'] == tmdb]

  caract_film = films[films['id_tmdb'] == tmdb][caracteristiques]

  distances, indices = model_charge.kneighbors(caract_film_encoded)
  return films.iloc[indices[0,1:]].reset_index(drop=True)

st.title('moi')