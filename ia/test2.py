import joblib
import os
from sklearn.metrics import mean_squared_error

os.chdir("dados")

# Carrega modelo e colunas
modelo = joblib.load("ia.pkl")
colunas_modelo = joblib.load("colunas.pkl")

test_x = joblib.load("test_x.pkl")
test_y = joblib.load("test_y.pkl")

pred_y = modelo.predict(test_x)
mse = mean_squared_error(test_y, pred_y)
print(f"Erro quadrático médio: {mse:.2f}")
