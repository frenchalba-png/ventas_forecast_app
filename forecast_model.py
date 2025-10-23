import pandas as pd
from prophet import Prophet  # o el modelo que uses

def preparar_datos(df, sucursal=None, departamento=None, categoria=None):
    # --- Filtros opcionales ---
    if sucursal:
        df = df[df["Sucursal"] == sucursal]
    if departamento:
        df = df[df["Departamento"] == departamento]
    if categoria:
        df = df[df["Categoría"] == categoria]

    # --- Verificar que existan las columnas esperadas ---
    if "Fecha" not in df.columns or "Monto_Ventas_USD" not in df.columns:
        raise ValueError("❌ El archivo debe tener las columnas 'Fecha' y 'Monto_Ventas_USD'.")

    # --- Renombrar columnas ---
    df = df.rename(columns={"Fecha": "ds", "Monto_Ventas_USD": "y"})

    # --- Ordenar por fecha ---
    df = df.sort_values("ds")

    # --- Retornar solo las columnas necesarias ---
    return df[["ds", "y"]]


def entrenar_y_predecir(data, dias_prediccion):
    modelo = Prophet()
    modelo.fit(data)
    futuro = modelo.make_future_dataframe(periods=dias_prediccion)
    forecast = modelo.predict(futuro)
    return forecast
