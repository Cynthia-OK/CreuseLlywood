import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt




st.set_page_config(
    page_title="Recommandation Film", 
    page_icon="https://img.freepik.com/vecteurs-libre/concept-cinema_1284-12713.jpg", 
    layout="wide", 
    initial_sidebar_state="expanded"  
)



films = pd.read_csv("./donnees/films_genre_colonne.csv", sep='\t', low_memory=False)
df_acteur_genre = pd.read_csv("./donnees/df_acteur_genre (1).csv", sep='\t', low_memory=False)
df_acteur_genre = df_acteur_genre.drop('Unnamed: 0',axis=1)
acteur_nombre_films = pd.read_csv("./donnees/acteur_nombre_films.csv", sep='\t', low_memory=False)
acteur_nombre_films = acteur_nombre_films.drop('Unnamed: 0',axis=1)
#df_acteur_genre.sort_values('nombre',ascending=False, inplace=True)
#df_acteur_genre = df_acteur_genre.head(50)
budget = pd.read_csv("./donnees/budget.csv",low_memory=False)
revenue = pd.read_csv("./donnees/revenue.csv",low_memory=False)
#budget = budget.astype('int64')
                              
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

# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://media.istockphoto.com/id/1191001701/fr/photo/pop-corn-et-clapperboard.jpg?s=612x612&w=0&k=20&c=AHQ7hOMdCMRfAya18h3rznNEflqmFS3Q90UznAbNfzM=");
#     }
#    </style>
#     """,
#     unsafe_allow_html=True
# )



st.markdown(
    """
    <style>
    .reportview-container {
        background-image: url('https://dacobello.com/cdn/shop/articles/Recette-14-Pop-corn-au-cheddar-scaled_1536x.jpg?v=1666189676'); /* Remplacez par l'URL ou le chemin de votre image */
        background-size: cover;
        background-position: center;
        height: 100%;
        padding: 0;
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.8); /* Rendre la barre latérale semi-transparente si nécessaire */
    }
    </style>
    """, 
    unsafe_allow_html=True
)
# Contenu de votre section statistique avec le fond d'écran
with st.container():
    st.markdown('<div class="stat-container">', unsafe_allow_html=True)
    st.subheader('Statistiques')
    st.write('Ici, vous pouvez afficher vos données statistiques.')
    # Ajoutez ici vos graphiques et autres éléments
    st.markdown('</div>', unsafe_allow_html=True)


with st.sidebar:
   selection = option_menu(
            menu_title=None,
            options = ["Statistiques", "films"]
        )

if selection == "Statistiques":
    st.write("Et si on faisait des graphiques amusants!")

    acteur_cible = st.text_input(' 🔍 choisis ton acteur préféré')
    if acteur_cible:
        if not df_acteur_genre['acteur'].str.contains(acteur_cible,case=False).any():
            st.write("ton acteur n'est pas ici, essaie un autre")
        else:
            acteur_pref = df_acteur_genre[df_acteur_genre['acteur'].str.contains(acteur_cible,case=False)]
            #je choisi les acteurs uniques en les mettant dans une liste 
            liste_acteur = acteur_pref['acteur'].unique().tolist()
            acteur_choisi = st.selectbox('Choisis un acteur', options=liste_acteur)
            data = df_acteur_genre[df_acteur_genre['acteur']==acteur_choisi]
            # affichage graphique et métrique
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.bar(data, x='genre', y='Nombre', title="Le nombre de films par genre")
                st.plotly_chart(fig,use_container_width=True)
            #nombre total de films par l'acteur choisi
            with col2:
                if acteur_choisi in acteur_nombre_films['acteur'].values:
                    totals_films = acteur_nombre_films[acteur_nombre_films['acteur']==acteur_choisi]['nombre'].values[0]
                else:
                    totals_films = 0
                st.metric(" 🎬 Nombre total de films ", totals_films)
    #graphique sur ladurée des films
films.sort_values('year',ascending=True, inplace=True)
fig = px.histogram(films, x='runtime' , title='Duréee des films aux fils des années', animation_frame = 'year')
fig.update_layout(bargap=0.2)
fig.update_yaxes(range=[0,100])
st.plotly_chart(fig)

#graphique sur le budget
import plotly.graph_objects as go
fig = go.Figure()

# Ajouter les barres pour le budget maximum
fig.add_trace(go.Bar(
    x=budget['year'],
    y=budget['budget_max'],
    name='Budget Max',
    marker_color='blue'  # Couleur des barres
))
# Ajouter la courbe pour le budget moyen
fig.add_trace(go.Scatter(
    x=budget['year'],
    y=budget['budget_moyen'],
    name='Budget Moyen',
    mode='lines+markers',  # Ligne avec des marqueurs
    line=dict(color='red', width=3),  # Couleur et largeur de la ligne
    marker=dict(symbol='circle', size=8)  # Personnalisation des marqueurs
))
fig.update_layout(
    title='Budget Max vs Budget Moyen par Année',
    xaxis_title='Année',
    yaxis_title='Montant du Budget (en millions)',
    barmode='group',  # Mode de regroupement des barres
)
# fig= px.bar(budget,x='year', y=['budget_max','budget_moyen'],title='Budget max et moyen par année')
st.plotly_chart(fig)

#graphique sur le revenue
fig= px.line(revenue,x='year', y=['revenu_max','revenu_moyen'],title='Revenu max et moyen par année')
st.plotly_chart(fig)




# graphique sur le profit
profit = pd.read_csv("./donnees/profit.csv")
fig= px.line(profit,x='year', y=['profit_max','profit_moyen'],title='profit max et moyen par année')
st.plotly_chart(fig)



if selection == "films":
    st.write("Bienvenue sur mon site de recommandation")
    st.text_input('Mets ici ton titre de film préféré')
    st.checkbox('Appuis maintenant ici')
