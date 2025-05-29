"""
Baixamos os dados de: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data
Utilizamos o arquivo games.csv
Esse programa filtra colunas e linhas e salva apenas os dados necessários em um novo dataset
Dessa forma, qualquer manipulação dos dados presentes no dataset se torna mais legível e o carregamento dos dados é mais rápido
"""

import pandas as pd
from os import chdir

chdir("dados")

input_file = "games.csv"  # entrada
output_file = "games_filtrado.csv"  # saida
colunas_escolhidas = [
    "AppID",
    "Name",
    "Release date",
    "Estimated owners",
    "Price",
    "Metacritic score",
    "Positive",
    "Negative",
    "Categories",
    "Genres",
    "Tags",
]
minimo_reviews = 500

# ler arquivo csv
df = pd.read_csv(input_file, index_col=False)
print()
print("Colunas disponiveis:", df.columns.tolist())

# manter apenas colunas escolhidas
df_fil = df[colunas_escolhidas]
print(f"Colunas escolhidas: {colunas_escolhidas}")

# nova coluna para o total de reviews
df_fil["Total Reviews"] = df_fil["Positive"] + df_fil["Negative"]

# remove jogos com menos de 500 reviews
df_fil = df_fil[df_fil["Total Reviews"] >= minimo_reviews]
print()
print(f"Incluindo apenas jogos com mais de {minimo_reviews} reviews")

# nova coluna para a % de reviews positivas
df_fil["Steam Score"] = (df_fil["Positive"] / df_fil["Total Reviews"]).round(2)

# salvar novo arquivo
df_fil.to_csv(output_file, index=False)

print()
print(f"Saida escrita em: {output_file}")
