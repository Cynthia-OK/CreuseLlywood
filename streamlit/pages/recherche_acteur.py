import streamlit as st
import pandas as pd

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

st.title("Bienvenue sur notre page de recherche par acteur")
st.text("Notre application contient les films français ou d’action sortis à partir de 2000 avec une note supérieure à la moyenne")
# Chargement des données
films = pd.read_csv('./donnees/films_selectionnes.csv', sep="\t", low_memory=False)
acteurs_liste_films = pd.read_csv('./donnees/stat/df_acteurs_liste_films.csv', sep="\t", low_memory=False)

#on met les noms en minuscule
acteurs_liste_films['acteur_lower'] = acteurs_liste_films['acteur'].apply(lambda x: x.lower())

#Saisie d'un acteur par l'utilisateur
acteur_select = st.text_input('Saisir un acteur')
#on met la saisie en minuscule
acteur_select_lower = acteur_select.lower()
#vérifier que la saisie est dans la liste si oui on affiche la liste des acteurs correspondant dans la liste disponible
if not acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower).any():
    st.write(f"L'acteur' '{acteur_select}' n'est pas disponible.")
if acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower).any() and acteur_select:
    films_acteur_dipo = acteurs_liste_films[acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower)]
    liste_acteurs_dispo = films_acteur_dipo['acteur'].tolist()
    
    
    if len(liste_acteurs_dispo)>0 :
        acteur_choisi = st.selectbox('Voici les acteurs correspondant à votre saisie',liste_acteurs_dispo, index=None)
        # on cherche les films de l'acteur choisi
        if acteur_choisi : 

            films_acteur_select = acteurs_liste_films[acteurs_liste_films['acteur']==acteur_choisi]
            films_acteur_select = films_acteur_select.drop_duplicates()
            # st.dataframe(films_acteur_select)
            films_acteur_select['liste_films'] = films_acteur_select['liste_films'].apply(lambda x : eval(x))
            # on récupère la liste des films :
            liste = films_acteur_select['liste_films'].iloc[0]              
            # st.write(liste)

            #créer un DataFrame vide pour stocker les infos sur les films de la liste
            films_selection = pd.DataFrame(columns=['id_tmdb','overview','poster','title','note','annee',
                                         'acteurs','directeurs','genres','duree'])
            #on parcourt la liste et on remplit le DataFrame           
            for i in liste:
                # st.write(i)
                # film = films.loc[films['id_tmdb']== i]
                overview = films['overview'].loc[films['id_tmdb']== i].iloc[0]
                poster = films['poster_path'].loc[films['id_tmdb']== i].iloc[0]
                title = films['original_title'].loc[films['id_tmdb']== i].iloc[0]
                note = films['vote_average'].loc[films['id_tmdb']== i].iloc[0]
                annee = films['year'].loc[films['id_tmdb']== i].iloc[0]
                acteurs = films['liste_acteurs_noms'].loc[films['id_tmdb']== i].iloc[0]
                directeurs = films['liste_directeurs_noms'].loc[films['id_tmdb']== i].iloc[0]
                genres = films['genres'].loc[films['id_tmdb']== i].iloc[0]
                duree = films['runtime'].loc[films['id_tmdb']== i].iloc[0]
                # st.write(title)
                new_row = pd.DataFrame([{'id_tmdb': i,
                                         'overview': overview,
                                         'poster': poster,
                                         'title': title,
                                         'note': note,
                                         'annee' : int(annee),
                                         'acteurs':acteurs,
                                         'directeurs' : directeurs,
                                         'genres' : genres,
                                         'duree':duree}])
                films_selection = pd.concat([films_selection, new_row],
                                            ignore_index=True)
                # on trie le DataFrame par note pour afficher les mieux notés en premier
                films_selection = films_selection.sort_values('note', ascending=False)
                films_selection = films_selection.reset_index(drop=True)
            # st.write(films_selection)
            if len(films_selection) < 4 :
                n = len(films_selection)
            else :
            # L'utilisateur choisit le nombre de films à afficher s'il y a plus de 3 films
                n = st.slider('Nombre de films',min_value=0, max_value=len(films_selection),step=1)
            
            # Sélectionner le nombre de films indiqués par l'utilisateur
            films_selection_n = films_selection[0:n:1]
            if n>0 :
                # Créer un bloc pour contenir les films
                bloc_films = st.container(border=True)
                bloc_films.header('Films :')
                bloc_films.text('les films sont rangés par note décroissante')
                col1, col2, col3 = bloc_films.columns(3)
                with col1:
                    # pour la colonne 1 on sélectionne les films avec un indice entre 0 et le nombre choisi par l'utilisateur avec un pas de 3
                    for i in range(0, n, 3):
                        st.image(films_selection_n.loc[i,'poster'], width=200)
                        with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer les informations que nous allons afficher dans la popup à partir du DataFrame
                            titre = films_selection_n.iloc[i]['title']
                            resume = films_selection_n.loc[i]['overview']
                            chemin_image = films_selection_n.loc[i]['poster']
                            acteurs = str( films_selection_n.loc[i]['acteurs'])
                            acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                            annee =  films_selection_n.iloc[i]['annee']
                            note = films_selection_n.iloc[i]['note']
                            directeurs =  films_selection_n.iloc[i]['directeurs']
                            directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                            genres =  films_selection_n.iloc[i]['genres']
                            genres = genres.replace("[","").replace("]","").replace("'","")
                            duree =  films_selection_n.iloc[i]['duree']

                            
                            # Créer le html qui s'affichera dans la popup                                    
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
                                        <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Réalisateurs : </span> {directeurs}</td>
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
                with col2:
                    # pour la colonne 2 on sélectionne les films avec un indice entre 1 et le nombre choisi par l'utilisateur avec un pas de 3
                    for i in range(1, n, 3):
                        st.image(films_selection_n.loc[i,'poster'], width=200)
                        with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer les informations que nous allons afficher dans la popup à partir du DataFrame
                            titre = films_selection_n.iloc[i]['title']
                            resume = films_selection_n.loc[i]['overview']
                            chemin_image = films_selection_n.loc[i]['poster']
                            acteurs = str( films_selection_n.loc[i]['acteurs'])
                            acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                            annee =  films_selection_n.iloc[i]['annee']
                            note = films_selection_n.iloc[i]['note']
                            directeurs =  films_selection_n.iloc[i]['directeurs']
                            directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                            genres =  films_selection_n.iloc[i]['genres']
                            genres = genres.replace("[","").replace("]","").replace("'","")
                            duree =  films_selection_n.iloc[i]['duree']

                            
                            # Créer le html qui s'affichera dans la popup                                    
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
                                        <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Réalisateurs : </span> {directeurs}</td>
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
                    # pour la colonne 3 on sélectionne les films avec un indice entre 2 et le nombre choisi par l'utilisateur avec un pas de 3
                    for i in range(2, n, 3):
                        st.image(films_selection_n.loc[i,'poster'], width=200)
                        with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer les informations que nous allons afficher dans la popup à partir du DataFrame
                            titre = films_selection_n.iloc[i]['title']
                            resume = films_selection_n.loc[i]['overview']
                            chemin_image = films_selection_n.loc[i]['poster']
                            acteurs = str( films_selection_n.loc[i]['acteurs'])
                            acteurs = acteurs.replace('{','').replace("'","").replace("}","")
                            annee =  films_selection_n.iloc[i]['annee']
                            note = films_selection_n.iloc[i]['note']
                            directeurs =  films_selection_n.iloc[i]['directeurs']
                            directeurs = directeurs.replace("[","").replace("]","").replace("'","")
                            genres =  films_selection_n.iloc[i]['genres']
                            genres = genres.replace("[","").replace("]","").replace("'","")
                            duree =  films_selection_n.iloc[i]['duree']

                            
                            # Créer le html qui s'affichera dans la popup                                    
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
                                        <td colspan="3"><span style="font-weight:bold; text-decoration:underline;"> Réalisateurs : </span> {directeurs}</td>
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


            # bloc_films = st.container(border=True)
            # bloc_films.header('Films :')
            # col1, col2, col3 = bloc_films.columns(3)
            # with col1:
            #     for i in liste[0::3]:
            #         film = films.loc[films['id_tmdb']== i]
            #         # index = film.index
            #         chemin_image = film['poster_path'].iloc[0]
            #         st.image(chemin_image, width=200)
            #         with st.popover("En savoir plus sur ce film"):
            #                 container = st.container(border=True)
            #                 # Récupérer le résumé à partir du DataFrame
            #                 resum = film['overview'].iloc[0]
            #                 img = film['poster_path'].iloc[0]
            #                 titre = film['title'].iloc[0]
                                                            
            #                 info_html = f"""
            #                 <table>
            #                     <tr>
            #                         <th colspan="2">{titre}</th>
            #                     </tr>
            #                     <tr>
            #                         <td style="width:50%">{resum}</td>
            #                         <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
            #                     </tr>           
            #                 </table>
            #                             """

            #                 # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
            #                 container.markdown(info_html, unsafe_allow_html=True)
            # with col2:
            #     for i in liste[1::3]:
            #         film = films.loc[films['id_tmdb']== i]
            #         index = film.index
            #         chemin_image = film['poster_path'].iloc[0]
            #         st.image(chemin_image, width=200)
            #         with st.popover("En savoir plus sur ce film"):
            #                 container = st.container(border=True)
            #                 # Récupérer le résumé à partir du DataFrame
            #                 resum = film['overview'].iloc[0]
            #                 img = film['poster_path'].iloc[0]
            #                 titre = film['title'].iloc[0]
                                                            
            #                 info_html = f"""
            #                 <table>
            #                     <tr>
            #                         <th colspan="2">{titre}</th>
            #                     </tr>
            #                     <tr>
            #                         <td style="width:50%">{resum}</td>
            #                         <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
            #                     </tr>           
            #                 </table>
            #                             """

            #                 # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
            #                 container.markdown(info_html, unsafe_allow_html=True)
            # with col3:
            #     for i in liste[2::3]:
            #         film = films.loc[films['id_tmdb']== i]
            #         index = film.index
            #         chemin_image = film['poster_path'].iloc[0]
            #         st.image(chemin_image, width=200)
            #         with st.popover("En savoir plus sur ce film"):
            #                 container = st.container(border=True)
            #                 # Récupérer le résumé à partir du DataFrame
            #                 resum = film['overview'].iloc[0]
            #                 img = film['poster_path'].iloc[0]
            #                 titre = film['title'].iloc[0]
                                                            
            #                 info_html = f"""
            #                 <table>
            #                     <tr>
            #                         <th colspan="2">{titre}</th>
            #                     </tr>
            #                     <tr>
            #                         <td style="width:50%">{resum}</td>
            #                         <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
            #                     </tr>           
            #                 </table>
            #                             """

            #                 # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
            #                 container.markdown(info_html, unsafe_allow_html=True)