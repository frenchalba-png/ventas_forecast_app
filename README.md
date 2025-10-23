# 🛒 Forecast de Ventas Retail

Aplicación interactiva desarrollada en **Python y Streamlit** para generar pronósticos de ventas a **3, 6 y 12 meses** usando modelos estadísticos de series de tiempo basados en **Prophet (Meta)**.

---

## Descripción del Proyecto

Este proyecto simula el entorno de una empresa retail tipo **Walmart / Costco / Albertsons**, permitiendo cargar datos históricos de ventas y generar proyecciones automáticas actualizadas mensualmente.

El dataset base contiene información de ventas desde **enero 2022 hasta octubre 2025**, con:
- 🏬 Sucursales  
- 🗂️ Departamentos  
- 🛍️ Categorías  
- 💰 Ventas (en USD)  
- 📦 Cantidades vendidas  

---

## ⚙️ Funcionalidades Principales

- Carga de archivo CSV con ventas históricas.  
- Pronóstico automático de ventas (3, 6 y 12 meses).  
- Visualización interactiva con **Plotly**.  
- Filtros por **sucursal, departamento y categoría**.  
- Descarga de los resultados en tres archivos Excel:
  - `forecast_3m.xlsx`
  - `forecast_6m.xlsx`
  - `forecast_12m.xlsx`

---

## 🚀 Cómo Ejecutar la App

### Opción 1: Localmente
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/forecast-retail-app.git
   cd forecast-retail-app
