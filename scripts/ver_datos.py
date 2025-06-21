import sqlite3
import os
import pandas as pd

# Ruta absoluta a la base de datos
db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, 'gimnasio_crm.db')
print("Ruta de la base de datos:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, nombre, apellidos, email, telefono, direccion, fecha_creacion FROM clientes")
usuarios = cursor.fetchall()

# Mostrar en formato tabla con pandas
df = pd.DataFrame(usuarios, columns=["ID", "Nombre", "Apellidos", "Email", "Teléfono", "Dirección", "Fecha de Creación"])
print("Usuarios registrados:")
print(df)

conn.close()