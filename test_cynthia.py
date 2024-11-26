import pandas as pd

# echantillon des différentes tables

# tmdb_1000 = pd.read_csv("./Data/TMDB/tmdb_full.csv", nrows=1000)

# # print(tmdb_1000)

# title_akas = pd.read_csv("./Data/IMDb/title.akas.tsv/title.akas.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_akas)

# title_basics_1000 = pd.read_csv("./Data/IMDb/title.basics.tsv/title.basics.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_basics_1000)


# title_crew_1000 = pd.read_csv("./Data/IMDb/title.crew.tsv/title.crew.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_crew_1000)


# title_episode_1000 = pd.read_csv("./Data/IMDb/title.episode.tsv/title.episode.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_episode_1000)


# title_principals_1000 = pd.read_csv("./Data/IMDb/title.principals.tsv/title.principals.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_principals_1000)


# title_ratings_1000 = pd.read_csv("./Data/IMDb/title.ratings.tsv/title.ratings.tsv", 
#                          nrows=1000, sep="\t")
# # print(title_ratings_1000)


# name_basics_1000 = pd.read_csv("./Data/IMDb/name.basics.tsv/name.basics.tsv", 
#                          nrows=1000, sep="\t")
# print(name_basics_1000)

# tables entières

tmdb = pd.read_csv("./Data/TMDB/tmdb_full.csv", low_memory=False)

# title_akas = pd.read_csv("./Data/IMDb/title.akas.tsv/title.akas.tsv", sep="\t", low_memory=False)


# title_basics = pd.read_csv("./Data/IMDb/title.basics.tsv/title.basics.tsv", sep="\t", low_memory=False)


# title_crew = pd.read_csv("./Data/IMDb/title.crew.tsv/title.crew.tsv", sep="\t", low_memory=False)


# title_episode = pd.read_csv("./Data/IMDb/title.episode.tsv/title.episode.tsv", sep="\t", low_memory=False)


# title_principals = pd.read_csv("./Data/IMDb/title.principals.tsv/title.principals.tsv", sep="\t", low_memory=False)


# title_ratings = pd.read_csv("./Data/IMDb/title.ratings.tsv/title.ratings.tsv", sep="\t", low_memory=False)


# name_basics = pd.read_csv("./Data/IMDb/name.basics.tsv/name.basics.tsv", sep="\t", low_memory=False)


# types_akas = title_akas['types'].value_counts()
# print(types_akas)
# types_akas.to_csv('types_akas.csv')

# genres_basics = title_basics['genres'].value_counts()
# print(genres_basics)
# genres_basics.to_csv('genres_basics.csv')


# region_akas = title_akas['region'].value_counts()
# print(region_akas)
# region_akas.to_csv('region_akas.csv')

# title_akas_FR = title_akas[title_akas['region']=='FR']
# title_akas_FR.to_csv('title_akas_FR.csv')

# tmdb_genres = tmdb['genres'].value_counts()
# tmdb_genres.to_csv('tmdb_genres.csv')

# tmdb_production_countries = tmdb['production_countries'].value_counts()

tmdb_filtre_action = tmdb[tmdb['genres'].str.contains('Action')]
tmdb_filtre_FR = tmdb[tmdb['production_countries'].str.contains('FR')]
tmdb_filtre = tmdb[(tmdb['genres'].str.contains('Action'))|(tmdb['production_countries'].str.contains('FR'))]

test