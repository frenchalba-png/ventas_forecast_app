import streamlit as st
import pandas as pd
from prophet import Prophet
from forecast_model import preparar_datos, entrenar_y_predecir

st.set_page_config(page_title="📈 Forecast de Ventas", layout="wide")

st.title("📊 Forecast de Ventas con Prophet")

# --- Subida del archivo ---
archivo = st.file_uploader("📂 Carga tu archivo CSV o Excel", type=["csv", "xlsx"])

if archivo:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    # --- Sección colapsable de filtros ---
    with st.expander("⚙️ Configuración y filtros de datos", expanded=False):
        sucursal = st.selectbox("Sucursal", ["Todas"] + sorted(df["Sucursal"].dropna().unique().tolist()))
        departamento = st.selectbox("Departamento", ["Todos"] + sorted(df["Departamento"].dropna().unique().tolist()))
        categoria = st.selectbox("Categoría", ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist()))

        # --- Filtro de rango de fechas tipo calendario ---
        fechas = pd.to_datetime(df["Fecha"])
        min_fecha, max_fecha = fechas.min(), fechas.max()
        rango_fechas = st.date_input(
            "📅 Rango de fechas",
            value=(min_fecha, max_fecha),
            min_value=min_fecha,
            max_value=max_fecha
        )

    # --- Aplicar filtros ---
    data_filtrada = df.copy()
    if sucursal != "Todas":
        data_filtrada = data_filtrada[data_filtrada["Sucursal"] == sucursal]
    if departamento != "Todos":
        data_filtrada = data_filtrada[data_filtrada["Departamento"] == departamento]
    if categoria != "Todas":
        data_filtrada = data_filtrada[data_filtrada["Categoría"] == categoria]

    data_filtrada = data_filtrada[
        (pd.to_datetime(data_filtrada["Fecha"]) >= pd.to_datetime(rango_fechas[0])) &
        (pd.to_datetime(data_filtrada["Fecha"]) <= pd.to_datetime(rango_fechas[1]))
    ]

    # --- Preparar datos ---
    data_preparada = preparar_datos(data_filtrada)
    data_preparada = data_preparada.reset_index(drop=True)  # quita índice

    # --- Mostrar datos filtrados ---
    st.subheader("📅 Datos Filtrados")
    data_mostrar = data_preparada.copy()
    data_mostrar["Fecha"] = pd.to_datetime(data_mostrar["ds"]).dt.strftime("%b-%Y")
    data_mostrar["Monto de Venta (USD)"] = data_mostrar["y"].apply(lambda x: f"$ {x:,.2f}")
    data_mostrar = data_mostrar.reset_index(drop=True)
    st.dataframe(
        data_mostrar[["Fecha", "Monto de Venta (USD)"]],
        use_container_width=True
    )

    # --- Entrenar y mostrar pronósticos ---
    st.subheader("🔮 Pronóstico de Ventas")
    for meses in [3, 6, 12]:
        st.markdown(f"### ⏳ Forecast {meses}M")

        forecast = entrenar_y_predecir(data_preparada, dias_prediccion=meses * 30)
        forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast["Fecha"] = pd.to_datetime(forecast["ds"]).dt.strftime("%b-%Y")
        forecast["Monto Estimado (USD)"] = forecast["yhat"].apply(lambda x: f"$ {x:,.2f}")
        forecast["Rango Inferior (USD)"] = forecast["yhat_lower"].apply(lambda x: f"$ {x:,.2f}")
        forecast["Rango Superior (USD)"] = forecast["yhat_upper"].apply(lambda x: f"$ {x:,.2f}")

        # 🔹 Eliminar índice antes de mostrar
        forecast = forecast.reset_index(drop=True)

        st.dataframe(
            forecast[["Fecha", "Monto Estimado (USD)", "Rango Inferior (USD)", "Rango Superior (USD)"]],
            use_container_width=True
        )
else:
    st.info("📥 Carga un archivo para comenzar.")











