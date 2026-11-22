import sqlite3
import os
import pickle
from datetime import datetime

NOMBRE_BD = "veterinaria.db"
ARCHIVO_TXT = "pacientes_veterinaria.txt"
ARCHIVO_BIN = "pacientes_veterinaria.bin"

def inicializar_bd():
    """Inicializa la base de datos SQLite con las tablas pacientes, usuarios y auditoria."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()

    columnas_esperadas = ["Código", "Nombre", "Especie", "Dueño", "Primer - Nombre - Dueño"]
    cursor.execute("PRAGMA table_info(pacientes)")
    columnas_actuales = [col[1] for col in cursor.fetchall()]

    if columnas_actuales and columnas_actuales != columnas_esperadas:
        cursor.execute("SELECT * FROM pacientes")
        filas_existentes = cursor.fetchall()
        cursor.execute("DROP TABLE pacientes")
        cursor.execute("""
            CREATE TABLE pacientes (
                "Código" TEXT,
                "Nombre" TEXT,
                "Especie" TEXT,
                "Dueño" TEXT,
                "Primer - Nombre - Dueño" TEXT
            )
        """)
        for fila in filas_existentes:
            cursor.execute(
                'INSERT INTO pacientes ("Código", "Nombre", "Especie", "Dueño", "Primer - Nombre - Dueño") VALUES (?, ?, ?, ?, ?)',
                fila[:5]
            )
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                "Código" TEXT,
                "Nombre" TEXT,
                "Especie" TEXT,
                "Dueño" TEXT,
                "Primer - Nombre - Dueño" TEXT
            )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            "Usuario" TEXT PRIMARY KEY,
            "Contraseña" TEXT NOT NULL,
            "Rol" TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            'INSERT INTO usuarios ("Usuario", "Contraseña", "Rol") VALUES (?, ?, ?)',
            ("admin", "1234", "Administrador")
        )
        cursor.execute(
            'INSERT INTO usuarios ("Usuario", "Contraseña", "Rol") VALUES (?, ?, ?)',
            ("recepcion", "vet2026", "Recepcionista")
        )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Usuario" TEXT NOT NULL,
            "Acción" TEXT NOT NULL,
            "Detalle" TEXT,
            "Fecha y Hora" TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

def guardar_en_sqlite(registros_combinados):
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pacientes")
    for reg in registros_combinados:
        cursor.execute(
            'INSERT INTO pacientes ("Código", "Nombre", "Especie", "Dueño", "Primer - Nombre - Dueño") VALUES (?, ?, ?, ?, ?)',
            (reg["codigo"], reg["nombre"], reg["especie"], reg["dueño"], reg["primer_nombre_dueño"])
        )
    conexion.commit()
    conexion.close()

def consultar_filas_sqlite():
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute('SELECT "Código", "Nombre", "Especie", "Dueño", "Primer - Nombre - Dueño" FROM pacientes')
    filas = cursor.fetchall()
    conexion.close()
    return filas

def verificar_usuario_sqlite(usuario, contrasena):
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute(
        'SELECT "Usuario", "Rol" FROM usuarios WHERE "Usuario" = ? AND "Contraseña" = ?',
        (usuario, contrasena)
    )
    fila = cursor.fetchone()
    conexion.close()
    return fila  

def registrar_usuario_sqlite(usuario, contrasena, rol="Recepcionista"):
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            'INSERT INTO usuarios ("Usuario", "Contraseña", "Rol") VALUES (?, ?, ?)',
            (usuario, contrasena, rol)
        )
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()

def registrar_auditoria_sqlite(usuario, accion, detalle=""):
    inicializar_bd()
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute(
        'INSERT INTO auditoria ("Usuario", "Acción", "Detalle", "Fecha y Hora") VALUES (?, ?, ?, ?)',
        (usuario, accion, detalle, fecha_hora)
    )
    conexion.commit()
    conexion.close()

def consultar_auditoria_sqlite():
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute('SELECT "ID", "Usuario", "Acción", "Detalle", "Fecha y Hora" FROM auditoria ORDER BY "ID" ASC')
    filas = cursor.fetchall()
    conexion.close()
    return filas

def exportar_pacientes_txt(registros_combinados):
    archivo = open(ARCHIVO_TXT, "w", encoding="utf-8")
    for reg in registros_combinados:
        linea = f"{reg['codigo']},{reg['nombre']},{reg['especie']},{reg['dueño']}\n"
        archivo.write(linea)
    archivo.close()

def agregar_ultimo_paciente_txt(registro):
    with open(ARCHIVO_TXT, "a", encoding="utf-8") as archivo:
        archivo.write(f"{registro['codigo']},{registro['nombre']},{registro['especie']},{registro['dueño']}\n")

def leer_lineas_txt():
    if not os.path.exists(ARCHIVO_TXT):
        return None
    filas = []
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) == 4:
                filas.append(datos)
    return filas

def exportar_y_leer_binario_datos(registros_combinados):
    with open(ARCHIVO_BIN, "wb") as bin_out:
        pickle.dump(registros_combinados, bin_out)
    with open(ARCHIVO_BIN, "rb") as bin_in:
        datos_recuperados = pickle.load(bin_in)
    return datos_recuperados