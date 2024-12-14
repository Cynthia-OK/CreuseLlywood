import streamlit as st
import pandas as pd
st.title("Bienvenue sur notre page de recherche par acteur")
# Chargement des données
films = pd.read_csv('./donnees/films_genre_colonne.csv', sep="\t", low_memory=False)
acteurs_liste_films = pd.read_csv('./donnees/stat/df_acteurs_liste_films.csv', sep="\t", low_memory=False)
films = films.drop(['Unnamed: 0', 'genres_x'], axis=1)
acteurs_liste_films = acteurs_liste_films.drop(['Unnamed: 0'], axis=1)
films['poster_path'] = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + films['poster_path']

acteurs_liste_films['acteur_lower'] = acteurs_liste_films['acteur'].apply(lambda x: x.lower())

acteur_select = st.text_input('Saisir un acteur')

acteur_select_lower = acteur_select.lower()

if not acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower).any():
    st.write(f"L'acteur' '{acteur_select}' n'est pas dans le dataset.")
if acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower).any() and acteur_select:
    films_acteur_dipo = acteurs_liste_films[acteurs_liste_films['acteur_lower'].str.contains(acteur_select_lower)]
    liste_acteurs_dispo = films_acteur_dipo['acteur'].tolist()
    
    
    if len(liste_acteurs_dispo)>0 :
        acteur_choisi = st.selectbox('la saisie correspond à plusieurs acteurs, veuillez en sélectionner un dans cette liste',liste_acteurs_dispo, index=None)

        if acteur_choisi : 

            films_acteur_select = acteurs_liste_films[acteurs_liste_films['acteur']==acteur_choisi]
            films_acteur_select = films_acteur_select.drop_duplicates()

            # st.dataframe(films_acteur_select)

            films_acteur_select['liste_films'] = films_acteur_select['liste_films'].apply(lambda x : eval(x))
            # for index in films_acteur_select.index :
            liste = films_acteur_select['liste_films'].iloc[0]              
                
            # st.write(liste)
            # for i in liste:
            #     # st.write(i)
            #     # st.write(type(i))
            #     film = films.loc[films['id_tmdb']== i]
            #     index = film.index
            #     # st.write(index)
            #     chemin_image = film['poster_path'].iloc[0]
            #     st.write(chemin_image)
            #     st.image(chemin_image, width=200)


            bloc_films = st.container(border=True)
            bloc_films.header('Films :')
            col1, col2, col3 = bloc_films.columns(3)
            with col1:
                for i in liste[0::3]:
                    film = films.loc[films['id_tmdb']== i]
                    index = film.index
                    chemin_image = film['poster_path'].iloc[0]
                    st.image(chemin_image, width=200)
                    with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer le résumé à partir du DataFrame
                            resum = film['overview'].iloc[0]
                            img = film['poster_path'].iloc[0]
                            titre = film['title'].iloc[0]
                                                            
                            info_html = f"""
                            <table>
                                <tr>
                                    <th colspan="2">{titre}</th>
                                </tr>
                                <tr>
                                    <td style="width:50%">{resum}</td>
                                    <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                </tr>           
                            </table>
                                        """

                            # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                            container.markdown(info_html, unsafe_allow_html=True)
            with col2:
                for i in liste[1::3]:
                    film = films.loc[films['id_tmdb']== i]
                    index = film.index
                    chemin_image = film['poster_path'].iloc[0]
                    st.image(chemin_image, width=200)
                    with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer le résumé à partir du DataFrame
                            resum = film['overview'].iloc[0]
                            img = film['poster_path'].iloc[0]
                            titre = film['title'].iloc[0]
                                                            
                            info_html = f"""
                            <table>
                                <tr>
                                    <th colspan="2">{titre}</th>
                                </tr>
                                <tr>
                                    <td style="width:50%">{resum}</td>
                                    <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                </tr>           
                            </table>
                                        """

                            # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                            container.markdown(info_html, unsafe_allow_html=True)
            with col3:
                for i in liste[2::3]:
                    film = films.loc[films['id_tmdb']== i]
                    index = film.index
                    chemin_image = film['poster_path'].iloc[0]
                    st.image(chemin_image, width=200)
                    with st.popover("En savoir plus sur ce film"):
                            container = st.container(border=True)
                            # Récupérer le résumé à partir du DataFrame
                            resum = film['overview'].iloc[0]
                            img = film['poster_path'].iloc[0]
                            titre = film['title'].iloc[0]
                                                            
                            info_html = f"""
                            <table>
                                <tr>
                                    <th colspan="2">{titre}</th>
                                </tr>
                                <tr>
                                    <td style="width:50%">{resum}</td>
                                    <td style="width:50%"><p style="text-align:center"><img src={img} alt={titre} style="width:200px; "></p></td>
                                </tr>           
                            </table>
                                        """

                            # Afficher le HTML dans Streamlit avec unsafe_allow_html=True
                            container.markdown(info_html, unsafe_allow_html=True)