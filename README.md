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
├── scripts/
│   ├── importar_excel.py       # Script para importar usuarios desde Excel
│   └── ver_datos.py            # Script para visualizar usuarios en tabla
│
└── README.md                   # Este archivo

## Requisitos
- Python 3.8 o superior
- Paquetes: pandas, sqlite3, openpyxl (para importar Excel)

  Instala dependencias con:
  ´´
  pip install pandas openpyxl
