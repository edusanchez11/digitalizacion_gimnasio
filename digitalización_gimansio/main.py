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
    # Función para registrar un nuevo usuario en la base de datos
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
        print("Usuario registrado correctamente")
    except Exception as e:
        print("Error al conectar o escribir en la base de datos:", e)

def buscar_usuario():
    # funcion para buscar un usuario por nombre o email
    print("Busqueda de usuario: ")
    print("1. Busqueda por email")
    print("2. Busqueda por nombre")
    opcion = input("Seleccione una opción: ")

    # Ruta absoluta a la base de datos en la raíz del proyecto
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if opcion == "1":
        email = input("Ingrese email: ")
        cursor.execute("SELECT id, nombre, apellidos, email, telefono, direccion, fecha_creacion FROM clientes WHERE email = ?", (email,))
        usuario = cursor.fetchone()
    elif opcion == "2":
        nombre = input("Ingrese nombre: ")
        cursor.execute("SELECT id, nombre, apellidos, email, telefono, direccion, fecha_creacion FROM clientes WHERE nombre LIKE ?", ('%' + nombre + '%',))
        usuario = cursor.fetchall()
    else:
        print("Opción no válida.")
        conn.close()
        return
    
    if usuario:
        print("Usuario encontrado:")
        print(f"ID: {usuario[0]}")
        print(f"Nombre: {usuario[1]} {usuario[2]}")
        print(f"Email: {usuario[3]}")
        print(f"Teléfono: {usuario[4]}")
        print(f"Dirección: {usuario[5]}")
        print(f"Fecha de creación: {usuario[6]}")
    else:
        print("No se encontró ningún usuario con esos datos.")
    conn.close()

'''
Función para crear una factura para un usuario existente.
Esta función solicita el email del usuario, busca su información en la base de datos,
'''

def crear_factura():
    print("CREAR FACTURA")
    email = input("Ingrese email del usuario: ").strip()

    # Ruta absoluta a la base de datos
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Buscar usuario por email
    cursor.execute("SELECT id, nombre, apellidos FROM clientes WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Usuario no encontrado.")
        conn.close()
        return
    
    print(f"Usuario encontrado: {usuario[1]} {usuario[2]} ")
    descripcion = input("Descripción del servicio: ").strip()
    monto = input("Monto de la factura: ")
    while True:
        print("Seleccione el estado de la factura:" )
        print("1. Pendiente")
        print("2. Pagada")
        print("3. Cancelada")
        estado_opcion = input("Estado de la factura: ")
        if estado_opcion == "1":
            estado = "Pendiente"
            break
        elif estado_opcion == "2":
            estado = "Pagada"
            break
        elif estado_opcion == "3":
            estado = "Cancelada"
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
    fecha_emision = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #crear factura en la base de datos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            descripcion TEXT,
            monto REAL,
            estado TEXT,
            fecha_emision TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')

    # Insertar factura
    cursor.execute('''
        INSERT INTO facturas (cliente_id, descripcion, monto, estado, fecha_emision)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario[0], descripcion, float(monto), estado, fecha_emision))
    conn.commit()

    # Obtener el número de factura recién creada
    factura_id = cursor.lastrowid
    print("Factura creada exitosamente!")
    print(f"Número de factura: FAC{factura_id:03d}")
    print(f"Fecha de emisión: {fecha_emision}")
    print(f"Cliente: {usuario[1]} {usuario[2]}")
    print(f"Descripción: {descripcion}")
    print(f"Monto: ${float(monto):.2f}")
    print(f"Estado: {estado}")

    conn.close()

def mostras_todos_usuarios():
    '''
    Esta función muestra todos los usuarios registrados en el sistema.
    Se conecta a la base de datos y recupera la información de los usuarios.
    '''
    print("LISTA DE USUARIOS")

    # Ruta absoluta a la base de datos
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellidos, email, telefono, fecha_creacion FROM clientes")
    usuarios = cursor.fetchall()
    for idx, usuario in enumerate(usuarios, 1):
        print(f"Usuario #{idx}:")
        print(f"ID: USR{usuario[0]:03d}")
        print(f"Nombre: {usuario[1]} {usuario[2]}")
        print(f"Email: {usuario[3]}")
        print(f"Teléfono: {usuario[4] if usuario[4] else 'No especificado'}")
        print(f"Fecha de registro: {usuario[5][:10]}")
    print(f"Total de usuarios registrados: {len(usuarios)}")
    conn.close()

def mostrar_facturas_usuario(email):
    '''
    Esta función muestra las facturas de un usuario específico.
    Se conecta a la base de datos y recupera las facturas asociadas al email proporcionado.
    '''
    print("FACTURAS POR USUARIO")
    email = input("Ingrese email del usuario: ")

    # Ruta absoluta a la base de datos
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # buscar usuario
    cursor.execute("SELECT id, nombre, apellidos FROM clientes WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Usuario no encontrado.")
        conn.close()
        return

    print(f"--- FACTURAS DE {usuario[1]} {usuario[2]} ---")
    cursor.execute('''
        SELECT id, fecha_emision, descripcion, monto, estado
        FROM facturas
        WHERE cliente_id = ?
        ORDER BY fecha_emision
    ''', (usuario[0],))
    facturas = cursor.fetchall()

    if not facturas:
        print("No hay facturas para este usuario.")
        conn.close()
        return
    
    total_facturado = 0
    total_pendiente = 0
    for idx, factura in enumerate(facturas, 1):
        print(f"Factura #{idx}:")
        print(f" Número: FAC{factura[0]:03d}")
        print(f" Fecha: {factura[1]}")
        print(f" Descripción: {factura[2]}")
        print(f" Monto: ${factura[3]:.2f}")
        print(f" Estado: {factura[4]}")
        total_facturado += factura[3]
        if factura[4] == "Pendiente":
            total_pendiente += factura[3]
    print(f"Total de facturas: {len(facturas)}")
    print(f"Monto total facturado: ${total_facturado:,.2f}")
    print(f"Monto pendiente: ${total_pendiente:,.2f}")
    conn.close()

def resumen_financiero_usuario():
    '''
    Esta función genera un resumen financiero para un usuario específico,
    permitiendo buscar por email o por nombre.
    '''
    print("RESUMEN FINANCIERO POR USUARIO")
    print("1. Buscar por email")
    print("2. Buscar por nombre")
    opcion = input("Seleccione una opción: ")

    # Ruta absoluta a la base de datos
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
    db_path = os.path.join(db_folder, 'gimnasio_crm.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if opcion == "1":
        valor = input("Ingrese el email del usuario: ").strip()
        cursor.execute("SELECT id, nombre, apellidos, email FROM clientes WHERE email = ?", (valor,))
    elif opcion == "2":
        valor = input("Ingrese el nombre (o parte) del usuario: ").strip()
        cursor.execute("SELECT id, nombre, apellidos, email FROM clientes WHERE nombre LIKE ?", ('%' + valor + '%',))
    else:
        print("Opción no válida.")
        conn.close()
        return

    usuarios = cursor.fetchall()
    if not usuarios:
        print("No se encontró ningún usuario con esos datos.")
        conn.close()
        return

    for usuario in usuarios:
        cursor.execute('''
            SELECT COUNT(*), 
                   COALESCE(SUM(monto), 0),
                   COALESCE(SUM(CASE WHEN estado = 'Pagada' THEN monto ELSE 0 END), 0),
                   COALESCE(SUM(CASE WHEN estado = 'Pendiente' THEN monto ELSE 0 END), 0)
            FROM facturas
            WHERE cliente_id = ?
        ''', (usuario[0],))
        datos = cursor.fetchone()
        print(f"Usuario: {usuario[1]} {usuario[2]} ({usuario[3]})")
        print(f"Total facturas: {datos[0]}")
        print(f"Monto total facturado: ${datos[1]:,.2f}")
        print(f"Facturas pagadas: ${datos[2]:,.2f}")
        print(f"Facturas pendientes: ${datos[3]:,.2f}")
        print("-" * 40)
    conn.close()

'''
Este menu muestra las 
opciones disponibles en el sistema de gestión del gimnasio.
'''

def mostrar_menu():
    print("""
*** CMR GIMNASIO ***
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
            buscar_usuario()
        elif opcion == "3":
            # Lógica para crear factura
            crear_factura()
        elif opcion == "4":
            # Lógica para mostrar todos los usuarios
            mostras_todos_usuarios()
        elif opcion == "5":
            # Lógica para mostrar facturas de un usuario
            mostrar_facturas_usuario()
        elif opcion == "6":
            # Lógica para resumen financiero
            resumen_financiero_usuario()
        elif opcion == "7":
            print("Gracias por usar el sistema del gimnasio. Hasta pronto")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()