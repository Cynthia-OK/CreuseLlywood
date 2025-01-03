import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from st_clickable_images import clickable_images
import pickle

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


# Initialisation des états de session
if "show_content" not in st.session_state:
    st.session_state.show_content = True
if "clicked" not in st.session_state:
    st.session_state.clicked = -1

def custom_clickable_images(liste_image, titles=None, div_style={}, img_style={}):
  clicked_index = clickable_images(liste_image, titles=titles, div_style=div_style, img_style=img_style)
  if clicked_index != -1:
    st.session_state.show_content = False  # Cacher le contenu
    st.session_state.clicked = clicked_index  # Update clicked dans etat de session
    st.rerun()  # Refresh immediately
  return clicked_index


# Titre de l'application
st.title('Bienvenue sur notre page de recommandation de films')

# Chargement des données
films = pd.read_csv('./donnees/films_selectionnes.csv', sep="\t", low_memory=False)





if st.session_state.show_content:
    # Entrée utilisateur pour le titre du film
    film_cible = st.text_input('Rentrer un titre')

    # Initialisation des variables 
    liste_image = []
    liste_id = []
    if film_cible:
        film_cible_lower = film_cible.lower()
        films['original_title'] = films['original_title'].apply(lambda x: x.lower())

        if not films['original_title'].str.contains(film_cible_lower).any():
            st.write(f"Le film '{film_cible}' n'est pas disponible.")
        else:
            films_identiques = films['id_tmdb'][films['original_title'].str.contains(film_cible_lower)]
                   

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
                st.session_state.show_content = False  # Masquer le contenu

if st.session_state.show_content == False :
    # st.write({st.session_state.clicked})
    id = int(st.session_state.liste_id[st.session_state.clicked])
    # st.write(f"id = {id}")
    film_choisi = films[films['id_tmdb'] == id]
    index_choisi = films[films['id_tmdb']==id].index
    index_choisi = index_choisi[0]
    chemin_image = film_choisi['poster_path'][index_choisi]          
    # st.write(film_choisi)
    resume = film_choisi['overview'][index_choisi]
    titre = film_choisi['original_title'][index_choisi]
    annee = film_choisi['year'][index_choisi]
    note = film_choisi['vote_average'][index_choisi]
    directeurs = film_choisi['liste_directeurs_noms'][index_choisi]
    directeurs = directeurs.replace("[","").replace("]","").replace("'","")
    acteurs = film_choisi['liste_acteurs_noms'][index_choisi]
    acteurs = acteurs.replace("{","").replace("}","").replace("'","")
    genres = film_choisi['genres'][index_choisi]
    genres = genres.replace("[","").replace("]","").replace("'","")
    duree = film_choisi['runtime'][index_choisi]
    # st.write(directeurs)
    # st.write(acteurs)
    # st.write(genres)
    # st.write(duree)
    film_select = st.container(border=True)
    
    film_select.header("Vous avez sélectionné : ")
    # film_select.subheader(titre)
    film_html = f"""
                <table>
                    <tr>
                        <th colspan="3" style="font-weight:bold; font-size:22px; ">{titre}</th>
                    </tr>
                    <tr>
                        <td  style="width:50%"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline; "> Résumé : </span>{resume}</p></td>
                        <td colspan="2" style="width:50%"><div style="text-align:center"><img src={chemin_image} alt={titre} style="width:200px;"></div></td>
                    </tr>
                    <tr>
                        <td colspan="3"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline;"> Acteurs : </span> {acteurs}</p></td>
                    </tr>
                    <tr>
                        <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Directeurs : </span> {directeurs}</td>
                    </tr>
                    <tr>
                        <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Genres : </span> {genres}</td>
                    </tr>
                     <tr>
                        <td style="width:40%"><span style="font-weight:bold; text-decoration:underline;"> Année de sortie : </span>{annee}</td>
                        <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Note : </span>{note}</td>
                        <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Durée : </span>{duree}</td>
                    </tr>
                    
                </table>
                            """

                # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
    film_select.markdown(film_html, unsafe_allow_html=True)
    col1, col2, col3 = film_select.columns(3)
    # Chargement des modèles
    with open('./modeles/modele_films_NN.pkl', 'rb') as f:
            model_charge = pickle.load(f)
    with open('./modeles/modele_SN_normalisation.pkl', 'rb') as f:
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
            # st.write(indices)
            # st.write(indices[0,1:])
            # st.write(films.iloc[161])
            df_resultat = films.iloc[indices[0,1:]].reset_index(drop=True)
            
            
    bloc_films = st.container(border=True)
    bloc_films.header('Films similaires')
    col1, col2, col3 = bloc_films.columns(3)
    with col1:
            # st.write(df_resultat.iloc[0::3]['poster_path'].values)
            # st.image(liste_chemin[0::3], width=150)
            for i in df_resultat.loc[0::3].index:
                st.image(df_resultat.loc[i ,'poster_path'], width=200)
                with st.popover("En savoir plus sur ce film"):
                    container = st.container(border=True)
                    resume = df_resultat.loc[i]['overview']
                    chemin_image = df_resultat.loc[i]['poster_path']
                    titre = df_resultat.iloc[i]['original_title']
                    acteurs = str(df_resultat.loc[i]['liste_acteurs_noms'])
                    acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                    annee = df_resultat.iloc[i]['year']
                    note = df_resultat.iloc[i]['vote_average']
                    directeurs = df_resultat.iloc[i]['liste_directeurs_noms']
                    directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                    genres = df_resultat.iloc[i]['genres']
                    genres = genres.replace("[","").replace("]","").replace("'","")
                    duree = df_resultat.iloc[i]['runtime']              
                    info_html = f"""
                    <table>
                        <tr>
                            <th colspan="3" style="font-weight:bold; font-size:22px; ">{titre}</th>
                        </tr>
                        <tr>
                            <td  style="width:50%"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline; "> Résumé : </span>{resume}</p></td>
                            <td colspan="2" style="width:50%"><div style="text-align:center"><img src={chemin_image} alt={titre} style="width:200px;"></div></td>
                        </tr>
                        <tr>
                            <td colspan="3"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline;"> Acteurs : </span> {acteurs}</p></td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Directeurs : </span> {directeurs}</td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Genres : </span> {genres}</td>
                        </tr>
                        <tr>
                            <td style="width:40%"><span style="font-weight:bold; text-decoration:underline;"> Année de sortie : </span>{annee}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Note : </span>{note}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Durée : </span>{duree}</td>
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
                    resume = df_resultat.loc[i]['overview']
                    chemin_image = df_resultat.loc[i]['poster_path']
                    titre = df_resultat.iloc[i]['original_title']
                    acteurs = str(df_resultat.loc[i]['liste_acteurs_noms'])
                    acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                    annee = df_resultat.iloc[i]['year']
                    note = df_resultat.iloc[i]['vote_average']
                    directeurs = df_resultat.iloc[i]['liste_directeurs_noms']
                    directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                    acteurs = df_resultat.iloc[i]['liste_acteurs_noms']
                    acteurs = acteurs.replace("{","").replace("}","").replace("'","")
                    genres = df_resultat.iloc[i]['genres']
                    genres = genres.replace("[","").replace("]","").replace("'","")
                    duree = df_resultat.iloc[i]['runtime']              
                    info_html = f"""
                    <table>
                        <tr>
                            <th colspan="3" style="font-weight:bold; font-size:22px; ">{titre}</th>
                        </tr>
                        <tr>
                            <td  style="width:50%"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline; "> Résumé : </span>{resume}</p></td>
                            <td colspan="2" style="width:50%"><div style="text-align:center"><img src={chemin_image} alt={titre} style="width:200px;"></div></td>
                        </tr>
                        <tr>
                            <td colspan="3"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline;"> Acteurs : </span> {acteurs}</p></td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Directeurs : </span> {directeurs}</td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Genres : </span> {genres}</td>
                        </tr>
                        <tr>
                            <td style="width:40%"><span style="font-weight:bold; text-decoration:underline;"> Année de sortie : </span>{annee}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Note : </span>{note}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Durée : </span>{duree}</td>
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
                    resume = df_resultat.loc[i]['overview']
                    chemin_image = df_resultat.loc[i]['poster_path']
                    titre = df_resultat.iloc[i]['original_title']
                    acteurs = str(df_resultat.loc[i]['liste_acteurs_noms'])
                    acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                    annee = df_resultat.iloc[i]['year']
                    note = df_resultat.iloc[i]['vote_average']
                    directeurs = df_resultat.iloc[i]['liste_directeurs_noms']
                    directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                    acteurs = df_resultat.iloc[i]['liste_acteurs_noms']
                    acteurs = acteurs.replace("{","").replace("}","").replace("'","")
                    genres = df_resultat.iloc[i]['genres']
                    genres = genres.replace("[","").replace("]","").replace("'","")
                    duree = df_resultat.iloc[i]['runtime']              
                    info_html = f"""
                    <table>
                        <tr>
                            <th colspan="3" style="font-weight:bold; font-size:22px; ">{titre}</th>
                        </tr>
                        <tr>
                            <td  style="width:50%"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline; "> Résumé : </span>{resume}</p></td>
                            <td colspan="2" style="width:50%"><div style="text-align:center"><img src={chemin_image} alt={titre} style="width:200px;"></div></td>
                        </tr>
                        <tr>
                            <td colspan="3"><p style="text-align:justify;"><span style="font-weight:bold; text-decoration:underline;"> Acteurs : </span> {acteurs}</p></td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Directeurs : </span> {directeurs}</td>
                        </tr>
                        <tr>
                            <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Genres : </span> {genres}</td>
                        </tr>
                        <tr>
                            <td style="width:40%"><span style="font-weight:bold; text-decoration:underline;"> Année de sortie : </span>{annee}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Note : </span>{note}</td>
                            <td style="width:30%"><span style="font-weight:bold; text-decoration:underline;"> Durée : </span>{duree}</td>
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
