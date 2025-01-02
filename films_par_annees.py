import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



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
for index, row in top_films.iterrows():
    #st.image(row['poster_path'], caption=row['title'], width=200)
    st.write(index)
    st.image(row['poster_path'],width=200)
# Plus : 
#st.write("Résumé des films :")
#st.dataframe(top_films.head(10))


   # Afficher un graphique des notes des films
plt.figure(figsize=(10, 6))
sns.barplot(x='title', y='vote_average', data=top_films, palette="Blues_d")
plt.xticks(rotation=45, ha='right')
plt.title(f"Top 10 des films les mieux notés de l'année {annee}")
plt.xlabel("Film")
plt.ylabel("Note moyenne")
st.pyplot(plt)  # Affiche le graphique


#st.image ('C:/Users/filiz/Desktop/image cine.jpg')