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

st.title("Bienvenue sur notre page de recherche par genre")
st.text("Notre application contient les films français ou d’action sortis à partir de 2000 avec une note supérieure à la moyenne")

# Chargement des données
films = pd.read_csv('./donnees/films_selectionnes.csv', sep="\t", low_memory=False)


# st.dataframe(films)
liste_genres = ['Comedy', 'Thriller', 'Mystery',
       'Drama', 'War', 'Music', 'Horror',
       'Fantasy', 'Animation', 'Science Fiction',
       'Family', 'Adventure', 'Romance', 'Crime',
       'Documentary', 'History', 'Action', 'Western']



genre_choisi = st.multiselect('choisir un genre', liste_genres)


# on cherche les films du genre choisi
if len(genre_choisi) == 0 or len(genre_choisi) > 3 :
    st.text('Veuillez choisir entre 1 et 3 genres')
else :
    if len(genre_choisi) == 1:
        films_genre_select = films[(films[f'genre_{genre_choisi[0]}']== True)]
    elif len(genre_choisi) == 2:
        films_genre_select = films[(films[f'genre_{genre_choisi[0]}']== True)&(films[f'genre_{genre_choisi[1]}']== True)]
    elif len(genre_choisi) == 3:
        films_genre_select = films[(films[f'genre_{genre_choisi[0]}']== True)&(films[f'genre_{genre_choisi[1]}']== True)&(films[f'genre_{genre_choisi[2]}']== True)]

    films_genre_select = films_genre_select.drop_duplicates()
    # st.dataframe(films_genre_select)

    #créer un DataFrame vide pour stocker les infos sur les films de la liste
    films_selection = pd.DataFrame(columns=['id_tmdb','overview','poster','title','note','annee',
                                         'acteurs','directeurs','genres','duree'])
    #on parcourt la liste et on remplit le DataFrame 
    for i in films_genre_select.index:
        # st.write(i)
            id = films_genre_select['id_tmdb'][i]
            poster = films_genre_select['poster_path'][i]          
            # st.write(films_genre_select)
            overview = films_genre_select['overview'][i]
            title = films_genre_select['original_title'][i]
            annee = films_genre_select['year'][i]
            note = films_genre_select['vote_average'][i]
            directeurs = films_genre_select['liste_directeurs_noms'][i]
            directeurs = directeurs.replace("[","").replace("]","").replace("'","")
            acteurs = films_genre_select['liste_acteurs_noms'][i]
            acteurs = acteurs.replace("{","").replace("}","").replace("'","")
            genres = films_genre_select['genres'][i]
            genres = genres.replace("[","").replace("]","").replace("'","")
            duree = films_genre_select['runtime'][i]
            # st.write(genres)
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
    # st.write(f'len selection : {len(films_selection)}')
    
    if len(films_selection) == 0 and len(genre_choisi)>0 :
        st.text("Aucun film ne correspond à ces genres")
    elif len(films_selection) >0 :
            # on trie le DataFrame par note pour afficher les mieux notés en premier
        films_selection = films_selection.sort_values(by=['note','annee'], ascending=False)
        films_selection = films_selection.reset_index(drop=True)
        films_selection = films_selection[0:24]
        # st.dataframe(films_selection)
        if len(films_selection) < 4 :
            n = len(films_selection)
        elif len(films_selection) >24 :
            n = 24
        else :
        # L'utilisateur choisit le nombre de films à afficher s'il y a plus de 3 films
            n = st.slider('Nombre de films',min_value=0, max_value=24,step=1)
                    
        # Sélectionner le nombre de films indiqués par l'utilisateur
        films_selection_n = films_selection[0:n:1]
        if n>0 :
            # Créer un bloc pour contenir les films
            bloc_films = st.container(border=True)
            bloc_films.header('Films :')
            bloc_films.text('Les films sont rangés par note et année de sortie décroissantes')
            bloc_films.text('Nombre maximum de films = 24')
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

