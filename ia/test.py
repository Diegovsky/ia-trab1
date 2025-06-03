import joblib
import os
import json
import pandas as pd
from ia.common import EntryTest
from datetime import datetime

os.chdir("dados")

# Carrega modelo e colunas
modelo = joblib.load("ia.pkl")
colunas_modelo = joblib.load("colunas.pkl")


def transformar_entryout(entry: dict) -> pd.DataFrame:
    """
    Converte um dicionário EntryOut em DataFrame com colunas idênticas ao treino.
    """

    # Processar release_date
    try:
        data = datetime.strptime(entry["release_date"], "%b %d, %Y")
        release_year = data.year
        release_month = data.month
    except:
        release_year = None
        release_month = None

    # Variáveis base
    base = {
        "price": entry["price"],
        "release_year": release_year,
        "release_month": release_month,
    }

    # Binarização manual (precisa seguir o mesmo encoding do treino)
    bin_cols = {}

    def binarizar_lista(prefixo, lista_original):
        for coluna in colunas_modelo:
            if coluna.startswith(f"{prefixo}_"):
                valor = int(coluna.split("_")[1])
                bin_cols[coluna] = 1 if valor in lista_original else 0

    binarizar_lista("categories", entry.get("categories", []))
    binarizar_lista("genres", entry.get("genres", []))
    binarizar_lista("tags", entry.get("tags", []))

    # Combinar tudo em um DataFrame
    row = {**base, **bin_cols}
    df = pd.DataFrame([row])

    # Garantir a mesma ordem e colunas
    df = df.reindex(columns=colunas_modelo, fill_value=0)
    return df


# ---------- EXEMPLO DE USO ----------

if __name__ == "__main__":
    # Exemplo de entrada EntryOut
    with open("test.json") as f:
        entry = json.load(f)

    entry = EntryTest(**entry)
    entry = entry.model_dump()
    print(entry)

    df = transformar_entryout(entry)
    pred = modelo.predict(df) * 100
    print(f"Predição do steam_score: {pred[0]:.2f}")
