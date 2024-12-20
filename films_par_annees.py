import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



films = pd.read_csv("./donnees/export_films.csv",sep='\t')

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
    st.dataframe(films_trie_par_notes)

# prendre que les films selectionné dans le slider : 
 
    films_selec_par_annee  = films_trie_par_notes[films_trie_par_notes['year']== annee]
    #st.dataframe(films_selec_par_annee)
 # Afficher que les 10 premiers : 
    top_films = films_selec_par_annee.sort_values(by='vote_average', ascending = False).head(10)
    #st.dataframe(top_films)

# Avisuel des  10 premiers films :
st.bar_chart(top_films.head(10).set_index('title')['vote_average'])

# Plus : 
st.write("Résumé des films :")
st.dataframe(top_films.head(10))