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
├── scripts/
│   ├── importar_excel.py       # Script para importar usuarios desde Excel
│   └── ver_datos.py            # Script para visualizar usuarios en tabla
│
└── README.md                   # Este archivo
`````

## Requisitos
- Python 3.8 o superior
- Paquetes: pandas, sqlite3, openpyxl (para importar Excel)

  Instala dependencias con:
  ````bash
  pip install pandas openpyxl
``

Uso
1. Inicializa la base de datos (opcional)
Si partes de cero, ejecuta el script de importación para crear la base de datos y cargar usuarios desde un Excel:

````bash
python scripts/importar_excel.py
````

2. Ejecuta el sistema principal
```bash
python digitalización_gimansio/main.py
````

3. Navega por el menú
El sistema te mostrará un menú interactivo:

````bash
*** CMR GIMNASIO ***
1. Registrar nuevo usuario
2. Buscar usuario
3. Crear factura para usuario
4. Mostrar todos los usuarios
5. Mostrar facturas de un usuario
6. Resumen financiero por usuario
7. Salir
````
## 🧾 Funcionalidades detalladas

1. Registrar nuevo usuario
Solicita: nombre, apellidos, email, teléfono y dirección.

Valida que el email tenga formato correcto y no esté duplicado.

2. Buscar usuario
Permite buscar por email o por nombre (completo o parcial).

Muestra los datos completos del usuario.

3. Crear factura para usuario
Solicita el email, descripción, monto y estado de la factura.

Asocia y guarda la factura en la base de datos.

4. Mostrar todos los usuarios
Lista todos los usuarios registrados con información básica.

5. Mostrar facturas de un usuario
Solicita el email del usuario.

Muestra todas las facturas asociadas con número, fecha, descripción, monto y estado.

Calcula el total facturado y el total pendiente.

6. Resumen financiero por usuario
Permite buscar por email o nombre.

Muestra el total de facturas, monto total, pagado y pendiente.

7. Salir
Finaliza el programa.

## 🧪 Ejemplo de uso

````bash
Seleccione una opción: 1
Registrar nuevo usuario
Nombre: Juan
Apellidos: Pérez García
Email: juan.perez@email.com
Teléfono: 555-1234
Dirección: Calle Mayor 1
Usuario registrado correctamente
````

Autor: Eduardo Sánchez


