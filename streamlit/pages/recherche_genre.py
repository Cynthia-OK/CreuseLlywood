import streamlit as st
import pandas as pd
st.title("Bienvenue sur notre page de recherche par genre")


# Chargement des données
films = pd.read_csv('./donnees/films_selectionnes.csv', sep="\t", low_memory=False)


# st.dataframe(films)
liste_genres = ['Comedy', 'Thriller', 'Mystery',
       'Drama', 'War', 'Music', 'Horror',
       'Fantasy', 'Animation', 'Science Fiction',
       'Family', 'Adventure', 'Romance', 'Crime',
       'Documentary', 'History', 'Action', 'Western']



genre_choisi = st.multiselect('choisir un genre', liste_genres, max_selections=4)
# st.write('max 3 genres')

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
    films_selection = pd.DataFrame(columns=['id_tmdb','overview','poster','title','note'])
    #on parcourt la liste et on remplit le DataFrame 
    for i in films_genre_select.index:
        # st.write(i)
            id = films_genre_select['id_tmdb'][i]
            overview = films_genre_select['overview'][i]
            poster = films_genre_select['poster_path'][i]
            title = films_genre_select['title'][i]
            note = films_genre_select['vote_average'][i]
            annee = films_genre_select['year'][i]
            genres = films_genre_select['genre_liste'][i]
            # st.write(genres)
            new_row = pd.DataFrame([{'id_tmdb': id,
                                            'overview': overview,
                                            'poster': poster,
                                            'title': title,
                                            'note': note,
                                            'annee': int(annee),
                                            'genres': genres}])
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
                        resum = films_selection_n.loc[i]['overview']
                        img = films_selection_n.loc[i]['poster']
                        titre = films_selection_n.iloc[i]['title']
                        eval = films_selection_n.iloc[i]['note']
                        sortie = int(films_selection_n.iloc[i]['annee'])
                        genres = films_selection_n.iloc[i]['genres']
                        genres = str(genres).replace('[','').replace(']','').replace("'","")
                        # Créer le html qui s'affichera dans la popup                                    
                        info_html = f"""
                            <table>
                                        <tr>
                                            <th colspan="2">Titre : {titre}</th>
                                        </tr>
                                        <tr>
                                            <td style="width:50%">{resum}</td>
                                            <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Année de sortie :</p><p> {sortie} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Note :</p><p> {eval} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:Genres; text-decoration:underline;">Note :</p><p> {genres} </p>
                                            </td>
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
                        resum = films_selection_n.loc[i]['overview']
                        img = films_selection_n.loc[i]['poster']
                        titre = films_selection_n.iloc[i]['title']
                        eval = films_selection_n.iloc[i]['note']
                        sortie = int(films_selection_n.iloc[i]['annee'])
                        genres = films_selection_n.iloc[i]['genres']
                        # Créer le html qui s'affichera dans la popup                                    
                        info_html = f"""
                            <table>
                                        <tr>
                                            <th colspan="2">Titre : {titre}</th>
                                        </tr>
                                        <tr>
                                            <td style="width:50%">{resum}</td>
                                            <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Année de sortie :</p><p> {sortie} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Note :</p><p> {eval} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Note :</p><p> {genres} </p>
                                            </td>
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
                        resum = films_selection_n.loc[i]['overview']
                        img = films_selection_n.loc[i]['poster']
                        titre = films_selection_n.iloc[i]['title']
                        eval = films_selection_n.iloc[i]['note']
                        sortie = int(films_selection_n.iloc[i]['annee'])
                        genres = films_selection_n.iloc[i]['genres']
                        # Créer le html qui s'affichera dans la popup                                    
                        info_html = f"""
                            <table>
                                        <tr>
                                            <th colspan="2">Titre : {titre}</th>
                                        </tr>
                                        <tr>
                                            <td style="width:50%">{resum}</td>
                                            <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Année de sortie :</p><p> {sortie} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Note :</p><p> {eval} </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"><p style="font-weight:bold; text-decoration:underline;">Note :</p><p> {genres} </p>
                                            </td>
                                        </tr>
                            </table>
                                                """

                        # Afficher le HTML dans Streamlit avec unsafe_allow_html=True                                                   
                        container.markdown(info_html, unsafe_allow_html=True)