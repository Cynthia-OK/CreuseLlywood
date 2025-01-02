import streamlit as st
import pandas as pd
st.title("Bienvenue sur notre page de recherche par directeur")


# Chargement des données
films = pd.read_csv('./donnees/films_selectionnes.csv', sep="\t", low_memory=False)
directeur_liste_films = pd.read_csv('./donnees/stat/df_directeur_liste_films.csv', sep="\t", low_memory=False)

# st.dataframe(directeur_liste_films)
#on met les noms en minuscule
directeur_liste_films['directeur_lower'] = directeur_liste_films['directeur'].apply(lambda x: x.lower())

#Saisie d'un directeur par l'utilisateur
directeur_select = st.text_input('Saisir un directeur')
#on met la saisie en minuscule
directeur_select_lower = directeur_select.lower()
# st.write(directeur_select_lower)
#vérifier que la saisie est dans la liste si oui on affiche la liste des directeurs correspondant dans la liste disponible
if not directeur_liste_films['directeur_lower'].str.contains(directeur_select_lower).any():
    st.write(f"Le directeur '{directeur_select}' n'est pas dans le dataset.")
if directeur_liste_films['directeur_lower'].str.contains(directeur_select_lower).any() and directeur_select:
    films_directeur_dispo = directeur_liste_films[directeur_liste_films['directeur_lower'].str.contains(directeur_select_lower)]
    liste_directeur_dispo = films_directeur_dispo['directeur'].tolist()
    
    
    if len(liste_directeur_dispo)>0 :
        directeur_choisi = st.selectbox('Voici les directeurs correspondant à votre saisie',liste_directeur_dispo, index=None)
        # on cherche les films du directeur choisi
        if directeur_choisi : 

            films_directeur_select = directeur_liste_films[directeur_liste_films['directeur']==directeur_choisi]
            films_directeur_select = films_directeur_select.drop_duplicates()
            # st.dataframe(films_directeur_select)
            films_directeur_select['liste_films'] = films_directeur_select['liste_films'].apply(lambda x : eval(x))
            # on récupère la liste des films :
            liste = films_directeur_select['liste_films'].iloc[0]              
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
                title = films['title'].loc[films['id_tmdb']== i].iloc[0]
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