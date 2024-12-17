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
films_acteurs = pd.read_csv('./donnees/stat/df_films_liste_acteurs.csv', sep="\t", low_memory=False)
films = films.drop(['Unnamed: 0', 'genres_x'], axis=1)
films_acteurs = films_acteurs.drop(['Unnamed: 0'], axis=1)
films['poster_path'] = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + films['poster_path']


if st.session_state.show_content:
    # Entrée utilisateur pour le titre du film
    film_cible = st.text_input('Rentrer un titre')

    # Initialisation des variables 
    liste_image = []
    liste_id = []
    if film_cible:
        film_cible_lower = film_cible.lower()
        films['title'] = films['title'].apply(lambda x: x.lower())

        if not films['title'].str.contains(film_cible_lower).any():
            st.write(f"Le film '{film_cible}' n'est pas dans le dataset.")
        else:
            films_identiques = films['id_tmdb'][films['title'].str.contains(film_cible_lower)]
                   

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
    # st.write(chemin_image)
    resume = film_choisi['overview'][index_choisi]
    titre = film_choisi['title'][index_choisi]
    annee = film_choisi['year'][index_choisi]
    
    film_select = st.container(border=True)
    
    col1, col2 = film_select.columns(2)
    with col1:
        film_select.header("Vous avez sélectionné : ")
    with col2:
        film_select.subheader(titre)
    
    col1, col2, col3 = film_select.columns(3)
    with col1:
        st.image(chemin_image, width=150)
    with col2:
        st.text(f"Résumé : {resume}")
    with col3:
        st.text(f"Année de sortie : {annee}")   
    # Chargement des modèles
    with open('modele_films_NN.pkl', 'rb') as f:
        model_charge = pickle.load(f)
    with open('modele_SN_normalisation.pkl', 'rb') as f:
        SN_charge = pickle.load(f)
        # st.text('film choisi')
        # st.dataframe(film_choisi)

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
                
        # je normalise les infos numériques de mon film choisi et je cherche les films similaires
        from sklearn.preprocessing import MinMaxScaler
        
        caract_film_num_SN = pd.DataFrame(SN_charge.transform(caract_film_num), columns=caract_film_num.columns, index=index)
        caract_film_cat_dummies = pd.get_dummies(caract_film_cat)
        caract_film_encoded = pd.concat([caract_film_num_SN, caract_film_cat_dummies], axis=1)
        distances, indices = model_charge.kneighbors(caract_film_encoded)
        df_resultat = films.iloc[indices[0,1:]].reset_index(drop=True)
        
        # st.text('caract_film_num')
        # st.dataframe(caract_film_num)

        # st.text(' caract_film_cat')
        # st.dataframe( caract_film_cat)


        # st.text('caract_film_encoded')
        # st.dataframe(caract_film_encoded)
        
        # st.text('distances, indices')
        # st.write(distances, indices)

    
        # st.text('df_resultat')
        # st.dataframe(df_resultat)  
    df_affichage = pd.merge(df_resultat,
                            films_acteurs,
                            how='left',
                            on = 'id_tmdb')
    
    # st.write(df_affichage)
    
    bloc_films = st.container(border=True)
    bloc_films.header('Films similaires')
    col1, col2, col3 = bloc_films.columns(3)
    with col1:
        # st.write(df_resultat.iloc[0::3]['poster_path'].values)
        # st.image(liste_chemin[0::3], width=150)
        for i in df_affichage.loc[0::3].index:
            st.image(df_affichage.loc[i ,'poster_path'], width=200)
            with st.popover("En savoir plus sur ce film"):
                container = st.container(border=True)
                resum = df_affichage.loc[i]['overview']
                img = df_affichage.loc[i]['poster_path']
                titre = df_affichage.iloc[i]['title']
                acteurs = str(df_affichage.loc[i]['liste_acteurs'])
                acteurs = acteurs.replace('[','').replace("'","").replace("]","")
                                
                info_html = f"""
                <table>
                    <tr>
                        <th colspan="2">{titre}</th>
                    </tr>
                    <tr>
                        <td style="width:50%">{resum}</td>
                        <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                    </tr>
                    <tr>
                        <td colspan="2"><p style="font-weight:bold; text-decoration:underline;"> Acteurs :</p> {acteurs}</td>
                    </tr>
                    
                </table>
                            """

                # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                container.markdown(info_html, unsafe_allow_html=True)
        # with st.expander("Cliquez ici pour voir plus d'informations"):
        
    with col2:
        # st.write(df_resultat.iloc[1::3]['poster_path'])
        for i in df_resultat.loc[1::3].index:
            st.image(df_resultat.loc[i ,'poster_path'], width=200)
            with st.popover("En savoir plus sur ce film"):
                container = st.container(border=True)
                # col1, col2 = container.columns(2)
                # Récupérer le résumé à partir du DataFrame
                resum = df_affichage.loc[i]['overview']
                img = df_affichage.loc[i]['poster_path']
                titre = df_affichage.iloc[i]['title']
                acteurs = str(df_affichage.loc[i]['liste_acteurs'])
                acteurs = acteurs.replace('[','').replace("'","")
                                
                info_html = f"""
                <table>
                    <tr>
                        <th colspan="2">{titre}</th>
                    </tr>
                    <tr>
                        <td style="width:50%">{resum}</td>
                        <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                    </tr>
                    <tr>
                        <td colspan="2"><p style="font-weight:bold; text-decoration:underline;"> Acteurs :</p> {acteurs}</td>
                    </tr>
                    
                </table>
                            """

                # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                container.markdown(info_html, unsafe_allow_html=True)
    with col3:
        for i in df_resultat.loc[2::3].index:
            st.image(df_resultat.loc[i ,'poster_path'], width=200)
            with st.popover("En savoir plus sur ce film"):
                container = st.container(border=True)
                # col1, col2 = container.columns(2)
                # Récupérer le résumé à partir du DataFrame
                resum = df_affichage.loc[i]['overview']
                img = df_affichage.loc[i]['poster_path']
                titre = df_affichage.iloc[i]['title']
                acteurs = str(df_affichage.loc[i]['liste_acteurs'])
                acteurs = acteurs.replace('[','').replace("'","")
                                
                info_html = f"""
                <table>
                    <tr>
                        <th colspan="2">{titre}</th>
                    </tr>
                    <tr>
                        <td style="width:50%">{resum}</td>
                        <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                    </tr>
                    <tr>
                        <td colspan="2"><p style="font-weight:bold; text-decoration:underline;"> Acteurs :</p> {acteurs}</td>
                    </tr>
                    
                </table>
                            """

                # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                container.markdown(info_html, unsafe_allow_html=True)
     
    
      
    
    retour = st.button("Revenir à la recherche")
    if retour:
        st.session_state.show_content = True
        st.session_state.clear()
        st.rerun()  # Refresh immediately

