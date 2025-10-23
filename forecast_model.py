import streamlit as st
import pandas as pd
import plotly.express as px
import io
from forecast_model import preparar_datos, entrenar_y_predecir

# Configuración general
st.set_page_config(page_title="Forecast de Ventas Retail", layout="wide")
st.title("📈 Forecast de Ventas - Supermercado")

# --- Subir archivo ---
uploaded_file = st.file_uploader("Sube el archivo CSV de ventas", type=["csv"])

if uploaded_file:
    # Leer CSV
    df = pd.read_csv(uploaded_file, parse_dates=["Fecha"])

    # --- Filtros laterales ---
    st.sidebar.header("Filtros")
    sucursales = [None] + sorted(df["Sucursal"].unique().tolist())
    departamentos = [None] + sorted(df["Departamento"].unique().tolist())
    categorias = [None] + sorted(df["Categoría"].unique().tolist())
    años = [None] + sorted(df["Fecha"].dt.year.unique().tolist())

    sucursal = st.sidebar.selectbox("Sucursal", sucursales)
    departamento = st.sidebar.selectbox("Departamento", departamentos)
    categoria = st.sidebar.selectbox("Categoría", categorias)
    año = st.sidebar.selectbox("Año", años)
    dias_prediccion = st.sidebar.slider("Días a predecir", 30, 365, 90)

    # --- Preparar datos ---
    data = preparar_datos(df, sucursal, departamento, categoria)

    # Filtrar por año si se selecciona
    if año:
        data = data[data["ds"].dt.year == año]

    if data.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
    else:
        # --- Entrenar modelo y generar forecast ---
        forecast = entrenar_y_predecir(data, dias_prediccion)

        # --- Gráfico interactivo ---
        fig = px.line(forecast, x="ds", y="yhat", title="Predicción de Ventas",
                      labels={"ds": "Fecha", "yhat": "Monto Predicho"})
        fig.add_scatter(x=data["ds"], y=data["y"], mode="lines", name="Ventas Reales")

        st.plotly_chart(fig, use_container_width=True)

        # --- Mostrar data seleccionada ---
        st.subheader("🧾 Datos originales filtrados")
        st.dataframe(data)

        # --- Forecasts: 3, 6 y 12 meses ---
        st.subheader("📊 Proyecciones futuras")

        def generar_forecast_y_excel(periodos):
            f = entrenar_y_predecir(data, periodos)
            promedio = f["yhat"].tail(periodos).mean()
            total = f["yhat"].tail(periodos).sum()
            minimo = f["yhat"].tail(periodos).min()
            maximo = f["yhat"].tail(periodos).max()
            output = io.BytesIO()
            f.to_excel(output, index=False)
            return promedio, total, minimo, maximo, output.getvalue()

        # Función auxiliar para mostrar métricas en columnas
        def mostrar_bloque_forecast(titulo, dias, archivo, color="#E8F0FE"):
            st.markdown(f"### {titulo}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Promedio proyectado", f"${archivo[0]:,.2f}")
            col2.metric("Total proyectado", f"${archivo[1]:,.2f}")
            col3.metric("Máximo proyectado", f"${archivo[3]:,.2f}")
            col4.metric("Mínimo proyectado", f"${archivo[2]:,.2f}")

            st.download_button(
                label=f"📥 Descargar forecast {titulo.lower()}",
                data=archivo[4],
                file_name=f"forecast_{titulo.replace(' ', '_').lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown("---")

        # --- 3 meses ---
        archivo_3m = generar_forecast_y_excel(90)
        mostrar_bloque_forecast("3 meses", 90, archivo_3m)

        # --- 6 meses ---
        archivo_6m = generar_forecast_y_excel(180)
        mostrar_bloque_forecast("6 meses", 180, archivo_6m)

        # --- 12 meses ---
        archivo_12m = generar_forecast_y_excel(365)
        mostrar_bloque_forecast("12 meses", 365, archivo_12m)

else:
    st.info("⬆️ Sube un archivo CSV para comenzar el análisis.")




