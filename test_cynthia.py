import pandas as pd

tmdb_1000 = pd.read_csv("./Data/TMDB/tmdb_full.csv", nrows=1000)

print(tmdb_1000)

title_akas = pd.read_csv("./Data/IMDb/title.akas.tsv/title.akas.tsv", 
                         nrows=1000, sep="\t")
print(title_akas)

title_basics = pd.read_csv("./Data/IMDb/title.basics.tsv/title.basics.tsv", 
                         nrows=1000, sep="\t")
print(title_basics)


title_crew = pd.read_csv("./Data/IMDb/title.crew.tsv/title.crew.tsv", 
                         nrows=1000, sep="\t")
print(title_crew)


title_episode = pd.read_csv("./Data/IMDb/title.episode.tsv/title.episode.tsv", 
                         nrows=1000, sep="\t")
print(title_episode)


title_principals = pd.read_csv("./Data/IMDb/title.principals.tsv/title.principals.tsv", 
                         nrows=1000, sep="\t")
print(title_principals)


title_ratings = pd.read_csv("./Data/IMDb/title.ratings.tsv/title.ratings.tsv", 
                         nrows=1000, sep="\t")
print(title_ratings)


name_basics = pd.read_csv("./Data/IMDb/name.basics.tsv/name.basics.tsv", 
                         nrows=1000, sep="\t")
print(name_basics)
