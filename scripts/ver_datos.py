import sqlite3

# Ruta a la base de datos
db_path = "database/gimnasio_crm.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, nombre, apellidos, email, telefono, fecha_creacion FROM clientes")
usuarios = cursor.fetchall()

print("Usuarios registrados:")
for usuario in usuarios:
    print(usuario)

conn.close()