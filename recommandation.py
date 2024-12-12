import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

films = pd.read_csv("./donnees/films_genre_colonne.csv", sep='\t', low_memory=False)
df_acteur_genre = pd.read_csv("./donnees/df_acteur_genre.csv", sep='\t', low_memory=False)
df_acteur_genre = df_acteur_genre.drop('Unnamed: 0',axis=1)
df_acteur_genre.sort_values('nombre',ascending=False, inplace=True)
df_acteur_genre = df_acteur_genre.head(50)
budget = pd.read_csv("./donnees/budget.csv",low_memory=False)
budget = budget.astype('int64')
                              
# Charger le modèle
import pickle
with open('modele_films_nn.pkl', 'rb') as f: 
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


# st.markdown(
#     """
#     <link rel="stylesheet" type="text/css" href="https://www.example.com/style.css">
#     """,
#     unsafe_allow_html=True
# )

st.header('Bienvuenu sur notre site de recommandation de films')

with st.sidebar:
   selection = option_menu(
            menu_title=None,
            options = ["Statistiques", "films"]
        )

if selection == "Statistiques":
    st.write("Et si on faisait des graphiques amusants!")

    liste = df_acteur_genre['acteur']
    choix = st.selectbox('choisis ton acteur préféré:',liste)
    acteur = df_acteur_genre[df_acteur_genre['acteur']==choix]
    fig = px.bar(acteur, x='genre', y='nombre', hover_data=('genre','nombre'))
    st.plotly_chart(fig,use_container_width=True)

    # fig = px.scatter(df_acteur_genre, x='acteur', y='genre', size="nombre")
    # st.plotly_chart(fig,use_container_width=True)

    # st.area_chart(df_acteur_genre, x='acteur', y='nombre', color='genre')

    #graphique pour le budget ax,min et moyen
    #import plotly.figure_factory as ff
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    #group_labels = ['max', 'min', 'moyen']
    #fig = px.histogram(budget, x='budget_max', y='budget_min', color='budget_moyen')
    #fig = px.histogram(budget, x='year', y='budget_min')
    fig  =  make_subplots ( specs = [[{ "secondary_y" :  True }]])

    fig . add_trace ( 
    go . Scatter ( x = budget['year'],  y = budget['budget_max'],  name = "max" ), 
    secondary_y = False , )

    fig . add_trace ( 
    go . Scatter ( x = budget['year'],  y = budget['budget_moyen'],  name = "moyen" ), 
    secondary_y = True , )

    st.plotly_chart(fig,use_container_width=True)
    
    #le graphique du revenue
    revenue = pd.read_csv("./donnees/revenue.csv",low_memory=False)
    fig  =  make_subplots ( specs = [[{ "secondary_y" :  True }]])

    fig . add_trace ( 
    go . Scatter ( x = revenue['year'],  y = revenue['revenu_max'],  name = "max" ), 
    secondary_y = False , )

    fig . add_trace ( 
    go . Scatter ( x = revenue['year'],  y = revenue['revenu_moyen'],  name = "moyen" ), 
    secondary_y = True , )

    st.plotly_chart(fig,use_container_width=True)



elif selection == "films":
    st.write("Bienvenue sur mon site de recommandation")
    st.text_input('Mets ici ton titre de film préféré')
    st.checkbox('Appuis maintenant ici')
