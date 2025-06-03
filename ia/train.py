import json
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MultiLabelBinarizer
from os import chdir

chdir("dados")

with open("ia.json") as f:
    j = json.load(f)
df = pd.DataFrame(list(j.values()))

# --------------------
# Pré-processamento
# --------------------

# Extrair ano e mês da data
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year
df["release_month"] = df["release_date"].dt.month

# Alvo
y = df["steam_score"]

# Colunas para processamento
numericas = ["price", "release_year", "release_month"]
listas = ["categories", "genres", "tags"]

# Aplicar MultiLabelBinarizer nas listas
mlb_cols = {}
for col in listas:
    mlb = MultiLabelBinarizer()
    X_mlb = mlb.fit_transform(df[col])
    mlb_df = pd.DataFrame(X_mlb, columns=[f"{col}_{cls}" for cls in mlb.classes_])
    mlb_cols[col] = mlb_df

# Combinar colunas
X = df[numericas].copy()
for mlb_df in mlb_cols.values():
    X = pd.concat([X, mlb_df], axis=1)

X, X_test, y, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
assert isinstance(X, pd.DataFrame)
assert isinstance(X_test, pd.DataFrame)
assert isinstance(y, pd.Series)
assert isinstance(y_test, pd.Series)

# Pipeline para normalizar os dados numéricos
numeric_pipeline = Pipeline(
    [("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]
)

# Aplicar normalização apenas nas colunas numéricas
preprocessor = ColumnTransformer(
    [("num", numeric_pipeline, numericas)], remainder="passthrough"
)

# Modelo final
modelo = Pipeline(
    [
        ("preprocess", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]
)

# Treinar
modelo.fit(X, y)

joblib.dump(modelo, "ia.pkl")
joblib.dump(X.columns.to_list(), "colunas.pkl")
joblib.dump(X_test, "test_x.pkl")
joblib.dump(y_test, "test_y.pkl")
