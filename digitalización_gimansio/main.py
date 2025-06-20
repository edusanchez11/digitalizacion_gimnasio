import sqlite3

def mostrar_menu():
    print("""
=== SISTEMA CRM ===
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
            # Lógica para registrar usuario
            pass
        elif opcion == "2":
            # Lógica para buscar usuario
            pass
        elif opcion == "3":
            # Lógica para crear factura
            pass
        elif opcion == "4":
            # Lógica para mostrar todos los usuarios