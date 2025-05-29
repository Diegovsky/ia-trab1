import pandas as pd
from os import chdir

chdir("dados")

input_file = "games_filtrado.csv"  # entrada

# ler arquivo csv
df = pd.read_csv(input_file, index_col=False)

# cortar listas
df["Categories_List"] = df["Categories"].str.split(",")
df["Genres_List"] = df["Genres"].str.split(",")
df["Tags_List"] = df["Tags"].str.split(",")
