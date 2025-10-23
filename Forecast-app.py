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
        st.subheader("Datos originales filtrados")
        st.dataframe(data)

        # --- Forecasts: 3, 6 y 12 meses ---
        st.subheader("📊 Proyecciones futuras")

        def generar_forecast_y_excel(periodos):
            f = entrenar_y_predecir(data, periodos)
            promedio = f["yhat"].tail(periodos).mean()
            output = io.BytesIO()
            f.to_excel(output, index=False)
            return promedio, output.getvalue()

        # --- 3 meses ---
        promedio_3m, excel_3m = generar_forecast_y_excel(90)
        st.markdown(f"**🔹 En 3 meses, la venta proyectada promedio es de:** ${promedio_3m:,.2f}")
        st.download_button(
            label="📥 Descargar forecast 3 meses",
            data=excel_3m,
            file_name="forecast_3_meses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # --- 6 meses ---
        promedio_6m, excel_6m = generar_forecast_y_excel(180)
        st.markdown(f"**🔹 En 6 meses, la venta proyectada promedio es de:** ${promedio_6m:,.2f}")
        st.download_button(
            label="📥 Descargar forecast 6 meses",
            data=excel_6m,
            file_name="forecast_6_meses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # --- 12 meses ---
        promedio_12m, excel_12m = generar_forecast_y_excel(365)
        st.markdown(f"**🔹 En 12 meses, la venta proyectada promedio es de:** ${promedio_12m:,.2f}")
        st.download_button(
            label="📥 Descargar forecast 12 meses",
            data=excel_12m,
            file_name="forecast_12_meses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("⬆️ Sube un archivo CSV para comenzar el análisis.")



