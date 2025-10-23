import pandas as pd
from prophet import Prophet  # o el modelo que uses

def preparar_datos(df, sucursal=None, departamento=None, categoria=None):
    if sucursal:
        df = df[df["Sucursal"] == sucursal]
    if departamento:
        df = df[df["Departamento"] == departamento]
    if categoria:
        df = df[df["Categoría"] == categoria]

    # Renombrar columnas para Prophet o el modelo de forecast
    df = df.rename(columns={"Fecha": "ds", "Monto_Ventas_USD": "y"})
    df = df.sort_values("ds")
    return df[["ds", "y"]]

def entrenar_y_predecir(data, dias_prediccion):
    modelo = Prophet()
    modelo.fit(data)
    futuro = modelo.make_future_dataframe(periods=dias_prediccion)
    forecast = modelo.predict(futuro)
    return forecast
