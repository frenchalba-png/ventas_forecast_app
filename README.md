🛒 Forecast de Ventas Retail

Aplicación interactiva en Python y Streamlit para generar pronósticos de ventas a 3, 6 y 12 meses usando Prophet (Meta).

Descripción del Proyecto

Esta app simula un entorno de retail tipo Walmart / Costco / Albertsons y permite generar pronósticos automáticos a partir de datos históricos.

Cómo funciona la carga de datos:

La app intenta leer automáticamente el CSV por defecto:
ventas_retail_2022_2025.csv (ya incluido en los Main Files).

Si quieres usar tus propios datos, puedes subir un CSV desde la interfaz.

El CSV debe contener estas columnas mínimas:

🏬 Sucursal

🗂️ Departamento

🛍️ Categoría

💰 Ventas (USD)

📦 Cantidad vendida

📅 Fecha

⚙️ Funcionalidades

Carga automática de CSV o subida manual.

Pronósticos automáticos a 3, 6 y 12 meses.

Visualizaciones interactivas con Plotly.

Filtros por sucursal, departamento y categoría.

Descarga de resultados en CSV:

forecast_3m.csv

forecast_6m.csv

forecast_12m.csv

🚀 Cómo Ejecutar

Clona el repositorio:

git clone https://github.com/tu_usuario/forecast-retail-app.git
cd forecast-retail-app


Instala dependencias:

pip install -r requirements.txt


Ejecuta la app:

streamlit run forecast-app.py


La app cargará automáticamente el CSV por defecto si está disponible.

Si quieres usar tus propios datos, sube tu CSV desde la interfaz.
