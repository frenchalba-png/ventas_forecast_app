import streamlit as st
import pandas as pd
from forecast_model import preparar_datos, entrenar_y_predecir
import plotly.express as px

st.set_page_config(page_title="Forecast de Ventas Retail", layout="wide")

st.title("📈 Forecast de Ventas - Supermercado")

# --- Subir archivo ---
uploaded_file = st.file_uploader("Sube el archivo CSV de ventas", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Fecha"])
    
    st.sidebar.header("Filtros")
    sucursales = [None] + sorted(df["Sucursal"].unique().tolist())
    departamentos = [None] + sorted(df["Departamento"].unique().tolist())
    categorias = [None] + sorted(df["Categoría"].unique().tolist())

    sucursal = st.sidebar.selectbox("Sucursal", sucursales)
    departamento = st.sidebar.selectbox("Departamento", departamentos)
    categoria = st.sidebar.selectbox("Categoría", categorias)
    dias_prediccion = st.sidebar.slider("Días a predecir", 30, 365, 90)

    data = preparar_datos(df, sucursal, departamento, categoria)
    forecast = entrenar_y_predecir(data, dias_prediccion)

    # --- Gráfico ---
    fig = px.line(forecast, x="ds", y="yhat", title="Predicción de Ventas", labels={"ds": "Fecha", "yhat": "Monto Predicho"})
    fig.add_scatter(x=data["ds"], y=data["y"], mode="lines", name="Ventas Reales")

    st.plotly_chart(fig, use_container_width=True)

    # --- Mostrar tabla ---
    st.subheader("Predicciones futuras")
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))

    # --- KPIs ---
    st.metric("Promedio proyectado", f"${forecast['yhat'].tail(dias_prediccion).mean():,.2f}")
    st.metric("Máximo proyectado", f"${forecast['yhat'].tail(dias_prediccion).max():,.2f}")
    st.metric("Mínimo proyectado", f"${forecast['yhat'].tail(dias_prediccion).min():,.2f}")

else:
    st.info("⬆️ Sube un archivo CSV para comenzar el análisis.")

