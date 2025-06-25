import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="CMR Gimnasio", layout="wide", page_icon="🏋️‍♂️")

# --- UTILIDADES ---
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'gimnasio_crm.db'))

def get_conn():
    return sqlite3.connect(DB_PATH)

def cargar_usuarios():
    conn = get_conn()
    df = pd.read_sql("SELECT id, nombre, apellidos, email, telefono, direccion, fecha_creacion FROM clientes", conn)
    conn.close()
    return df

def cargar_facturas(cliente_id=None):
    conn = get_conn()
    if cliente_id:
        df = pd.read_sql(f"SELECT * FROM facturas WHERE cliente_id = {cliente_id}", conn)
    else:
        df = pd.read_sql("SELECT * FROM facturas", conn)
    conn.close()
    return df

def registrar_usuario(nombre, apellidos, email, telefono, direccion):
    conn = get_conn()
    cursor = conn.cursor()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute(
            "INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, fecha_creacion) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, apellidos, email, telefono, direccion, fecha)
        )
        conn.commit()
        st.success("✅ Usuario registrado correctamente.")
    except sqlite3.IntegrityError as e:
        st.error(f"❌ Error: {e}")
    finally:
        conn.close()

def crear_factura(cliente_id, descripcion, monto, estado):
    conn = get_conn()
    cursor = conn.cursor()
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
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
    cursor.execute(
        "INSERT INTO facturas (cliente_id, descripcion, monto, estado, fecha_emision) VALUES (?, ?, ?, ?, ?)",
        (cliente_id, descripcion, monto, estado, fecha)
    )
    conn.commit()
    conn.close()
    st.success("✅ Factura creada correctamente.")

def resumen_financiero():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellidos, email FROM clientes")
    usuarios = cursor.fetchall()
    df_usuarios = pd.DataFrame(usuarios, columns=["id", "nombre", "apellidos", "email"])

    modo = st.radio("¿Qué resumen deseas ver?", ["Resumen general", "Buscar usuario"])

    if modo == "Buscar usuario":
        criterio = st.selectbox("Buscar por:", ["Email", "Nombre"])
        valor = st.text_input(f"Ingrese {criterio.lower()} del usuario:")
        if criterio == "Email":
            filtro = df_usuarios["email"].str.contains(valor, case=False, na=False)
        else:
            filtro = df_usuarios["nombre"].str.contains(valor, case=False, na=False)
        usuarios_filtrados = df_usuarios[filtro]
        if not usuarios_filtrados.empty:
            for _, usuario in usuarios_filtrados.iterrows():
                cursor.execute('''
                    SELECT COUNT(*), 
                           COALESCE(SUM(monto), 0),
                           COALESCE(SUM(CASE WHEN estado = 'Pagada' THEN monto ELSE 0 END), 0),
                           COALESCE(SUM(CASE WHEN estado = 'Pendiente' THEN monto ELSE 0 END), 0)
                    FROM facturas
                    WHERE cliente_id = ?
                ''', (usuario["id"],))
                datos = cursor.fetchone()
                st.markdown(f"**Usuario:** {usuario['nombre']} {usuario['apellidos']} ({usuario['email']})")
                st.write(f"- Total facturas: {datos[0]}")
                st.write(f"- Monto total: ${datos[1]:,.2f}")
                st.write(f"- Facturas pagadas: ${datos[2]:,.2f}")
                st.write(f"- Facturas pendientes: ${datos[3]:,.2f}")
                st.markdown("---")
        else:
            st.info("No se encontró ningún usuario con ese criterio.")
    else:
        # Resumen general
        total_usuarios = len(usuarios)
        total_facturas = 0
        ingresos_totales = 0
        ingresos_recibidos = 0
        ingresos_pendientes = 0

        st.markdown("### Resumen por usuario")
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
            with st.expander(f"{usuario[1]} {usuario[2]} ({usuario[3]})"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Facturas", datos[0])
                col2.metric("Total", f"${datos[1]:,.2f}")
                col3.metric("Pagadas", f"${datos[2]:,.2f}")
                col4.metric("Pendientes", f"${datos[3]:,.2f}")
            total_facturas += datos[0]
            ingresos_totales += datos[1]
            ingresos_recibidos += datos[2]
            ingresos_pendientes += datos[3]

        st.markdown("---")
        st.markdown("### Resumen General")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Usuarios", total_usuarios)
        col2.metric("Facturas emitidas", total_facturas)
        col3.metric("Ingresos totales", f"${ingresos_totales:,.2f}")
        col4.metric("Pendientes", f"${ingresos_pendientes:,.2f}")
        st.success(f"💰 Ingresos recibidos: ${ingresos_recibidos:,.2f}")
    conn.close()

# --- CABECERA ---
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between;">
    <div>
        <h1 style="color:#1e90ff;">🏋️‍♂️ CMR GIMNASIO</h1>
        <h4 style="color:#555;">Sistema de Gestión Digital</h4>
    </div>
    <div>
        <img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="80"/>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# --- MENÚ ---
menu = [
    "Ver usuarios",
    "Registrar usuario",
    "Buscar usuario",
    "Crear factura",
    "Ver facturas de usuario",
    "Resumen financiero"
]
opcion = st.sidebar.radio("Menú principal", menu)

# --- PÁGINAS ---
if opcion == "Ver usuarios":
    st.subheader("Usuarios registrados")
    df = cargar_usuarios()
    st.dataframe(df.style.format({"fecha_creacion": lambda x: x[:10]}), use_container_width=True)

elif opcion == "Registrar usuario":
    st.subheader("Registrar nuevo usuario")
    with st.form("form_usuario"):
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        direccion = st.text_input("Dirección")
        submitted = st.form_submit_button("Registrar")
        if submitted:
            if not nombre or not apellidos or not email:
                st.warning("Por favor, completa los campos obligatorios.")
            else:
                registrar_usuario(nombre, apellidos, email, telefono, direccion)

elif opcion == "Buscar usuario":
    st.subheader("Buscar usuario")
    criterio = st.radio("Buscar por:", ["Email", "Nombre"])
    valor = st.text_input(f"Ingrese {criterio.lower()}:")
    if st.button("Buscar"):
        df = cargar_usuarios()
        if criterio == "Email":
            resultado = df[df["email"].str.contains(valor, case=False, na=False)]
        else:
            resultado = df[df["nombre"].str.contains(valor, case=False, na=False)]
        if not resultado.empty:
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("No se encontró ningún usuario.")

elif opcion == "Crear factura":
    st.subheader("Crear factura para usuario")
    df = cargar_usuarios()
    usuario_sel = st.selectbox("Selecciona usuario", df["email"] + " - " + df["nombre"] + " " + df["apellidos"])
    if usuario_sel:
        cliente_id = int(df[df["email"] == usuario_sel.split(" - ")[0]].iloc[0]["id"])
        descripcion = st.text_input("Descripción")
        monto = st.number_input("Monto", min_value=0.0, step=0.01)
        estado = st.selectbox("Estado", ["Pendiente", "Pagada", "Cancelada"])
        if st.button("Crear factura"):
            if not descripcion or monto <= 0:
                st.warning("Completa la descripción y el monto.")
            else:
                crear_factura(cliente_id, descripcion, monto, estado)

elif opcion == "Ver facturas de usuario":
    st.subheader("Facturas de un usuario")
    df = cargar_usuarios()
    usuario_sel = st.selectbox("Selecciona usuario", df["email"] + " - " + df["nombre"] + " " + df["apellidos"])
    if usuario_sel:
        cliente_id = int(df[df["email"] == usuario_sel.split(" - ")[0]].iloc[0]["id"])
        facturas = cargar_facturas(cliente_id)
        if not facturas.empty:
            facturas = facturas.rename(columns={
                "id": "Nº Factura",
                "descripcion": "Descripción",
                "monto": "Monto",
                "estado": "Estado",
                "fecha_emision": "Fecha emisión"
            })
            st.dataframe(facturas[["Nº Factura", "Descripción", "Monto", "Estado", "Fecha emisión"]], use_container_width=True)
        else:
            st.info("Este usuario no tiene facturas.")

elif opcion == "Resumen financiero":
    st.subheader("Resumen financiero por usuario y general")
    resumen_financiero()