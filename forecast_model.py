import pandas as pd
from prophet import Prophet

def preparar_datos(df, sucursal=None, departamento=None, categoria=None):
    data = df.copy()
    if sucursal:
        data = data[data["Sucursal"] == sucursal]
    if departamento:
        data = data[data["Departamento"] == departamento]
    if categoria:
        data = data[data["Categoría"] == categoria]
    
    data = data.groupby("Fecha", as_index=False).agg({"Monto_Venta": "sum"})
    data = data.rename(columns={"Fecha": "ds", "Monto_Venta": "y"})
    return data

def entrenar_y_predecir(df, periodos=90):
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    future = model.make_future_dataframe(periods=periodos)
    forecast = model.predict(future)
    return forecast
