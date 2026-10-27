import pandas as pd

df = pd.read_csv("data.csv", encoding="ISO-8859-1")

# Métricas sobre Quantity y UnitPrice
stats = {
    "Variable": ["Quantity", "UnitPrice"],
    "Media": [df["Quantity"].mean(), df["UnitPrice"].mean()],
    "Mediana": [df["Quantity"].median(), df["UnitPrice"].median()],
    "Moda": [df["Quantity"].mode()[0], df["UnitPrice"].mode()[0]],
    "Desviación Estándar": [df["Quantity"].std(), df["UnitPrice"].std()],
}

resumen = pd.DataFrame(stats)
print(resumen)
