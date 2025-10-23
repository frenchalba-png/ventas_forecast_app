# forecast_model.py
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def make_forecast(df, periods=3):
    """
    Genera un forecast de ventas mensuales usando ARIMA.
    
    Parámetros:
    df : DataFrame con columnas ['Fecha', 'Venta_USD']
    periods : int - cantidad de meses a proyectar
    
    Retorna:
    DataFrame con las fechas futuras y el forecast de ventas
    """
    # Asegurar que la fecha sea tipo datetime
    df = df.copy()
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df = df.sort_values('Fecha')

    # Agrupar por mes en caso de que haya varias filas por mes
    df = df.groupby('Fecha', as_index=False)['Venta_USD'].sum()

    # Definir la serie temporal
    ts = df.set_index('Fecha')['Venta_USD']
    ts = ts.asfreq('MS')  # Frecuencia mensual

    # Entrenar modelo ARIMA
    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast futuro
    forecast = model_fit.forecast(steps=periods)

    # Convertir a DataFrame con fechas
    forecast_df = pd.DataFrame({
        'Fecha': pd.date_range(ts.index[-1] + pd.offsets.MonthBegin(1), periods=periods, freq='MS'),
        'Forecast_USD': forecast.values
    })
    return forecast_df
