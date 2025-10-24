import streamlit as st
import pandas as pd
import plotly.express as px
from forecast_model import preparar_datos, entrenar_y_predecir
import os

# --- Configuración inicial ---
st.set_page_config(page_title="Forecast de Ventas Retail", layout="wide")
st.title("📈 Forecast de Ventas - Supermercado")

# --- Intentar cargar CSV por defecto ---
default_csv = "ventas_retail_2022_2025.csv"
df = None

uploaded_file = st.file_uploader("📂 Sube el archivo CSV de ventas (opcional)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Fecha"])
    st.success("✅ CSV cargado correctamente desde tu archivo.")
elif os.path.exists(default_csv):
    df = pd.read_csv(default_csv, parse_dates=["Fecha"])
    st.info(f"📄 CSV cargado automáticamente desde '{default_csv}'.")
else:
    st.warning("⬆️ No se encontró el archivo por defecto. Por favor sube tu CSV para comenzar.")

# --- Procesar datos si df existe ---
if df is not None:
    # 📋 Mostrar columnas detectadas dentro de un expander (oculto por defecto)
    with st.expander("📋 Ver columnas detectadas"):
        st.write(list(df.columns))

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

    # --- Rango de fechas con calendario ---
    fecha_min, fecha_max = data["ds"].min(), data["ds"].max()
    rango = st.date_input(
        "📅 Selecciona el rango de fechas a mostrar",
        value=(fecha_min.date(), fecha_max.date()),
        min_value=fecha_min.date(),
        max_value=fecha_max.date()
    )

    # Validar rango
    if isinstance(rango, (list, tuple)) and len(rango) == 2:
        inicio, fin = pd.to_datetime(rango[0]), pd.to_datetime(rango[1])
        data_filtrada = data[(data["ds"] >= inicio) & (data["ds"] <= fin)]
    else:
        # En caso el usuario elija una sola fecha, usar todo el rango original
        data_filtrada = data.copy()

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

    # Crear tabla para mostrar (sin índice) y mostrarla con HTML para asegurar que no aparece el índice
    tabla_filtrada_html = data_mostrar[["Fecha", "Monto de Venta (USD)"]].to_html(index=False, justify="left")
    st.markdown(tabla_filtrada_html, unsafe_allow_html=True)

    # --- Sección de Forecasts ---
    st.subheader("Pronósticos de Ventas Futuras")

    def mostrar_forecast(forecast, label):
        forecast_formateado = forecast.copy()
        forecast_formateado["Fecha"] = pd.to_datetime(forecast_formateado["ds"]).dt.strftime("%b-%Y")
        forecast_formateado["Monto Pronosticado (USD)"] = forecast_formateado["yhat"].apply(lambda x: f"$ {x:,.2f}")

        # Asegurarnos que el CSV no tenga índice
        csv = forecast_formateado[["Fecha", "Monto Pronosticado (USD)"]].to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"⬇️ Descargar forecast {label}",
            data=csv,
            file_name=f"forecast_{label}.csv",
            mime="text/csv"
        )

        # Mostrar resumen (promedio de últimos valores pronosticados)
        promedio = forecast_formateado["yhat"].tail().mean()
        st.markdown(f"**📅 Pronóstico a {label}:** Venta promedio proyectada = `$ {promedio:,.2f}`")

        # Mostrar tabla sin índice usando HTML (to_html index=False)
        tabla_forecast_html = forecast_formateado[["Fecha", "Monto Pronosticado (USD)"]].tail(10).to_html(index=False, justify="left")
        st.markdown(tabla_forecast_html, unsafe_allow_html=True)

    mostrar_forecast(forecast_3m, "3 meses")
    mostrar_forecast(forecast_6m, "6 meses")
    mostrar_forecast(forecast_12m, "12 meses")









