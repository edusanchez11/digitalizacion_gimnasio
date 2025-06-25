# 🏋️‍♂️ CMR GIMNASIO - Sistema de Gestión Digital

Este proyecto es un sistema de gestión para gimnasios, desarrollado en Python, que permite registrar usuarios, gestionar facturas, consultar información y obtener resúmenes financieros de manera sencilla y eficiente.

## 🚀 Características principales
- Registro de usuarios con validación de datos.
- Búsqueda de usuarios por email o nombre.
- Creación de facturas para usuarios existentes.
- Listado de todos los usuarios registrados.
- Consulta de facturas por usuario.
- Resumen financiero por usuario (por email o nombre).
- Resumen general de facturación e ingresos.
- Persistencia de datos en SQLite.

## Estructura del proyecto
````bash
digitalizacion_gimnasio/
│
├── database/
│   └── gimnasio_crm.db         # Base de datos SQLite
│
├── data/
│   └── clientes.xlsx           # (Opcional) Archivo Excel para importación masiva
│
├── digitalización_gimansio/
│   └── main.py                 # Script principal del sistema
│
├── app.py                      # Aplicación visual Streamlit
├── requirements.txt            # Dependencias del proyecto
│
├── scripts/
│   ├── importar_excel.py       # Script para importar usuarios desde Excel
│   └── ver_datos.py            # Script para visualizar usuarios en tabla
│
└── README.md                   # Este archivo
`````

## 🚀 Ejecución de la aplicación visual (Streamlit)
1. Instala las dependencias
Asegúrate de tener Python 3.8 o superior.
Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
````
2. Verifica la base de datos
Asegúrate de tener el archivo de base de datos en gimnasio_crm.db.
Si no existe, puedes crearlo ejecutando el script de importación o registrando usuarios desde la app.

3. Ejecuta la aplicación Streamlit
Desde la raíz del proyecto, ejecuta:

```bash
streamlit run app.py
````
Esto abrirá la aplicación en tu navegador en http://localhost:8501.

## 📋 Funcionalidades principales
- Ver usuarios: Visualiza todos los usuarios registrados en formato tabla.
- Registrar usuario: Añade nuevos usuarios al sistema.
- Buscar usuario: Busca usuarios por email o nombre.
- Crear factura: Genera facturas para usuarios existentes.
- Ver facturas de usuario: Consulta todas las facturas asociadas a un usuario.
- Resumen financiero:
- Resumen general: Muestra métricas agregadas de todos los usuarios y facturas.
- Buscar usuario: Permite ver el resumen financiero de un usuario específico, filtrando por email o nombre.

## 📊 Resumen financiero (general y por usuario)

En la sección Resumen financiero puedes:
- Ver un resumen general de todos los usuarios, facturas e ingresos del gimnasio.
- Buscar el resumen financiero de un usuario específico filtrando por email o por nombre.

¿Cómo funciona?

1. Ve al menú lateral y selecciona "Resumen financiero".
2. Elige si deseas ver el Resumen general o Buscar usuario.
- Si seleccionas Buscar usuario, puedes buscar por email o por nombre (parcial o completo).
- Se mostrará el total de facturas, monto total, pagado y pendiente para el usuario seleccionado.
3. El Resumen general muestra métricas agregadas de todos los usuarios y facturas, incluyendo:
- Total de usuarios
- Total de facturas emitidas
- Ingresos totales
- Ingresos recibidos
- Ingresos pendientes

## 💡 Notas
Puedes personalizar la app modificando el archivo app.py.
Si quieres añadir más funcionalidades visuales (gráficos, filtros, exportar datos), Streamlit lo permite fácilmente.

Autor: Eduardo Sánchez


