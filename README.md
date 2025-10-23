🛒 Forecast de Ventas Retail

Aplicación interactiva en Python + Streamlit para generar pronósticos de ventas a 3, 6 y 12 meses utilizando Prophet (Meta).

Ideal para empresas retail tipo Walmart / Costco / Albertsons que quieran anticipar sus ventas y tomar decisiones basadas en datos.

Descripción del Proyecto

Esta app permite:

Cargar automáticamente un CSV de ventas por defecto (ventas_retail_2022_2025.csv) incluido en los Main Files.

Subir tu propio CSV si quieres usar tus propios datos históricos.

Formato requerido del CSV:

Columna	Tipo de dato	Descripción
Sucursal	Texto	Nombre de la sucursal
Departamento	Texto	Nombre del departamento
Categoría	Texto	Categoría de productos
Ventas	Numérico	Monto vendido en USD
Cantidad vendida	Numérico	Unidades vendidas
Fecha	Fecha	Fecha de la venta (YYYY-MM-DD)

⚙️ Funcionalidades Principales

🔄 Carga automática o manual del CSV

📊 Pronósticos a 3, 6 y 12 meses

📈 Visualizaciones interactivas con Plotly

🎯 Filtros por sucursal, departamento y categoría


💾 Descarga de resultados en CSV:

forecast_3m.csv

forecast_6m.csv

forecast_12m.csv

🚀 Cómo Ejecutar

1️⃣ Clonar el repositorio:

git clone https://github.com/tu_usuario/forecast-retail-app.git
cd forecast-retail-app


2️⃣ Instalar dependencias:

pip install -r requirements.txt


3️⃣ Ejecutar la app:

streamlit run forecast-app.py


4️⃣ Uso de la app:

La app intentará cargar automáticamente el CSV por defecto.

Si quieres usar tus propios datos, sube un archivo CSV desde la interfaz.

Aplica filtros, visualiza la evolución de ventas y descarga tus pronósticos.

💡 Tip: El CSV por defecto está diseñado para que puedas probar la app sin necesidad de preparar tus propios datos.
