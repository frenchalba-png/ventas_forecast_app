import pandas as pd
from prophet import Prophet

def preparar_datos(df, sucursal=None, departamento=None, categoria=None):
    """
    Prepara los datos para el modelo Prophet.
    Aplica filtros opcionales y renombra columnas.
    """

    # --- Filtros opcionales ---
    if sucursal:
        df = df[df["Sucursal"] == sucursal]
    if departamento:
        df = df[df["Departamento"] == departamento]
    if categoria:
        df = df[df["Categoría"] == categoria]

    # --- Verificar columnas esperadas ---
    if "Fecha" not in df.columns or "Monto_Venta_USD" not in df.columns:
        raise ValueError("❌ El archivo debe tener las columnas 'Fecha' y 'Monto_Venta_USD'.")

    # --- Renombrar columnas ---
    df = df.rename(columns={"Fecha": "ds", "Monto_Venta_USD": "y"})

    # --- Ordenar por fecha ---
    df = df.sort_values("ds")

    # --- Retornar solo las columnas necesarias ---
    return df[["ds", "y"]]


def entrenar_y_predecir(data, dias_prediccion):
    """
    Entrena un modelo Prophet y genera el forecast.
    """
    modelo = Prophet()
    modelo.fit(data)

    # Crear dataframe futuro para predicciones
    futuro = modelo.make_future_dataframe(periods=dias_prediccion)
    forecast = modelo.predict(futuro)

    return forecast
