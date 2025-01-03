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

films = pd.read_csv("./donnees/films_selectionnes.csv",sep='\t')

st.title('Afficher les films sur ces dernières années') 

annee = st.slider ("Sélectionnez une année :",
           min_value=2000,
           max_value= 2023,         
          )


#st.write(annee)

if annee > 1999 : 
# trier par ordre de note, afficher les 10 films les mieux notés

# 1-trier la table films : 
    films_trie_par_notes = films.sort_values(by= 'vote_average', ascending =False)
    #st.dataframe(films_trie_par_notes)

# prendre que les films selectionné dans le slider : 
 
    films_selec_par_annee  = films_trie_par_notes[films_trie_par_notes['year']== annee]
    #st.dataframe(films_selec_par_annee)
 # Afficher que les 10 premiers : 
    top_films = films_selec_par_annee.sort_values(by='vote_average', ascending = False).head(10)
    #st.dataframe(top_films)




# Afficher les 10 meilleurs films : 
st.write("Affiches des 10 meilleurs films :")

    #st.image(row['poster_path'], caption=row['title'], width=200)
st.write()
for index, row in top_films.iterrows():
    col1, col2= st.columns(2)
    with col1:
        st.image(row['poster_path'],width=200)
    with col2:
    #for index, row in top_films.iterrows():
        st.write(row['overview'],width=200)   
    st.write("---------------------------------------------------------")
       


   # Afficher un graphique des notes des films
# plt.figure(figsize=(10, 6))
# sns.barplot(x='title', y='vote_average', data=top_films, palette="Blues_d")
# plt.xticks(rotation=45, ha='right')
# plt.title(f"Top 10 des films les mieux notés de l'année {annee}")
# plt.xlabel("Film")
# plt.ylabel("Note moyenne")
# st.pyplot(plt)  # Affiche le graphique


#st.image ('C:/Users/filiz/Desktop/image cine.jpg')

