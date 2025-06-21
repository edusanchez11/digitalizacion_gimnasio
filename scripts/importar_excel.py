import sqlite3
import pandas as pd
from datetime import datetime
import os

# cargar el archivo excel
df = pd.read_excel(r"C:\Users\eduar\digitalizacion_gimnasio\data\clientes.xlsx")

# añadir columna fecha actual
df['fecha_creacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Conectar a la base de datos SQLite
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'gimnasio_crm.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT UNIQUE NOT NULL,
    direccion TEXT,
    fecha_creacion TEXT NOT NULL
)
''')

# Insertar los datos del DataFrame en la tabla
for _, row in df.iterrows():
    try:
        cursor.execute('''
            INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['nombre'], row['apellidos'], row['email'], row['telefono'], row['direccion'], row['fecha_creacion']))
    except Exception as e:
        print(f"Error al insertar el cliente {row['nombre']} {row['apellidos']}: {e}")

conn.commit()
conn.close()
print("Datos importados correctamente a la base de datos.")