import os
import sqlite3
import re
from datetime import datetime

'''
Este script es parte del sistema de gestión digital del gimnasio.
Permite registrar nuevos usuarios, validar sus datos y gestionar la base de datos.
'''

def email_valido(email):
    # Validación básica de email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def registrar_usuario():
    print("Registrar nuevo usuario")
    nombre = input("Nombre: ").strip()
    apellidos = input("Apellidos: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    direccion = input("Dirección: ").strip()

    # verificar nombre, apellidos y email
    if not nombre or not apellidos or not email:
        print("Nombre, apellidos y email son obligatorios.")
        return
    if not email_valido(email):
        print("Email con formato no válido.")
        return

    # Ruta absoluta a la base de datos en la raíz del proyecto
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    print("Ruta de la base de datos:", db_path)  # Para depuración

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
        if cursor.fetchone():
            print("Ya existe un usuario con ese email.")
            conn.close()
            return

        fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO clientes (nombre, apellidos, email, telefono, fecha_creacion) VALUES (?, ?, ?, ?, ?)",
            (nombre, apellidos, email, telefono, fecha_creacion)
        )
        conn.commit()
        conn.close()
        print("Usuario registrado correctamente.\n")
    except Exception as e:
        print("Error al conectar o escribir en la base de datos:", e)

def mostrar_menu():
    print("""
=== SISTEMA DIGITAL GIMNASIO ===
1. Registrar nuevo usuario
2. Buscar usuario
3. Crear factura para usuario
4. Mostrar todos los usuarios
5. Mostrar facturas de un usuario
6. Resumen financiero por usuario
7. Salir
""")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            # Lógica para buscar usuario
            pass
        elif opcion == "3":
            # Lógica para crear factura
            pass
        elif opcion == "4":
            # Lógica para mostrar todos los usuarios
            pass
        elif opcion == "5":
            # Lógica para mostrar facturas de un usuario
            pass
        elif opcion == "6":
            # Lógica para resumen financiero
            pass
        elif opcion == "7":
            print("Gracias por usar el sistema del gimnasio. Hasta pronto")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()