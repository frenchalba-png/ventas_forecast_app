import streamlit as st
import pandas as pd
import plotly.express as px
from forecast_model import preparar_datos, entrenar_y_predecir

# --- Configuración inicial ---
st.set_page_config(page_title="Forecast de Ventas Retail", layout="wide")

st.title("📈 Forecast de Ventas - Supermercado")

# --- Subir archivo ---
uploaded_file = st.file_uploader("📂 Sube el archivo CSV de ventas", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Fecha"])
    st.write("✅ Columnas detectadas:", list(df.columns))

    # --- Sidebar: filtros ---
    st.sidebar.header("🎯 Filtros")
    sucursales = [None] + sorted(df["Sucursal"].unique().tolist())
    departamentos = [None] + sorted(df["Departamento"].unique().tolist())
    categorias = [None] + sorted(df["Categoría"].unique().tolist())

    sucursal = st.sidebar.selectbox("Sucursal", sucursales)
    departamento = st.sidebar.selectbox("Departamento", departamentos)
    categoria = st.sidebar.selectbox("Categoría", categorias)

    # --- Preparar datos ---
    data = preparar_datos(df, sucursal, departamento, categoria)

    # --- Rango de fechas ---
    fecha_min, fecha_max = data["ds"].min(), data["ds"].max()
    rango = st.slider(
        "📅 Selecciona el rango de fechas a mostrar",
        min_value=fecha_min.to_pydatetime(),
        max_value=fecha_max.to_pydatetime(),
        value=(fecha_min.to_pydatetime(), fecha_max.to_pydatetime()),
        format="MMM YYYY"
    )

    data_filtrada = data[(data["ds"] >= rango[0]) & (data["ds"] <= rango[1])]

    # --- Entrenar modelo y predecir ---
    forecast_3m = entrenar_y_predecir(data, 90)
    forecast_6m = entrenar_y_predecir(data, 180)
    forecast_12m = entrenar_y_predecir(data, 365)

    # --- Gráfico interactivo ---
    st.subheader("📊 Evolución y Pronóstico de Ventas")
    fig = px.line(
        forecast_12m, x="ds", y="yhat",
        title="Predicción de Ventas",
        labels={"ds": "Fecha", "yhat": "Monto Pronosticado (USD)"}
    )
    fig.add_scatter(x=data_filtrada["ds"], y=data_filtrada["y"], mode="lines", name="Ventas Reales")
    st.plotly_chart(fig, use_container_width=True)

    # --- Mostrar datos seleccionados ---
    st.subheader("📅 Datos Filtrados")
    data_mostrar = data_filtrada.copy()
    data_mostrar["Fecha"] = pd.to_datetime(data_mostrar["ds"]).dt.strftime("%b-%Y")
    data_mostrar["Monto de Venta (USD)"] = data_mostrar["y"].apply(lambda x: f"$ {x:,.2f}")
    st.dataframe(data_mostrar[["Fecha", "Monto de Venta (USD)"]], use_container_width=True)

    # --- Sección de Forecasts ---
    st.subheader("Pronósticos de Ventas Futuras")

    def mostrar_forecast(forecast, label):
        forecast_formateado = forecast.copy()
        forecast_formateado["Fecha"] = pd.to_datetime(forecast_formateado["ds"]).dt.strftime("%b-%Y")
        forecast_formateado["Monto Pronosticado (USD)"] = forecast_formateado["yhat"].apply(lambda x: f"$ {x:,.2f}")

        # Mostrar resumen y link de descarga
        promedio = forecast_formateado["yhat"].tail().mean()
        st.markdown(f"**📅 Pronóstico a {label}:** Venta promedio proyectada = `$ {promedio:,.2f}`")
        
        csv = forecast_formateado[["Fecha", "Monto Pronosticado (USD)"]].to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"⬇️ Descargar forecast {label}",
            data=csv,
            file_name=f"forecast_{label}.csv",
            mime="text/csv"
        )

        st.dataframe(forecast_formateado[["Fecha", "Monto Pronosticado (USD)"]].tail(10), use_container_width=True)

    mostrar_forecast(forecast_3m, "3 meses")
    mostrar_forecast(forecast_6m, "6 meses")
    mostrar_forecast(forecast_12m, "12 meses")

else:
    st.info("⬆️ Sube un archivo CSV para comenzar el análisis.")





