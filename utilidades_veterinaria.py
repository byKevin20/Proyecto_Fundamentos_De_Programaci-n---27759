import sqlite3
import os
import pickle

NOMBRE_BD = "veterinaria.db"
ARCHIVO_TXT = "pacientes_veterinaria.txt"
ARCHIVO_BIN = "pacientes_veterinaria.bin"

def inicializar_bd():
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

def consultar_datos_sqlite(nombres, especies, duenos, mascotas, registros_combinados, mi_contador):
    inicializar_bd()
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute('SELECT "Código", "Nombre", "Especie", "Dueño", "Primer - Nombre - Dueño" FROM pacientes')
    filas = cursor.fetchall()
    conexion.close()
    nombres.clear()
    especies.clear()
    duenos.clear()
    mascotas.clear()
    registros_combinados.clear()
    total_cargados = 0
    for fila in filas:
        codigo, nombre, especie, dueno, primer_nombre = fila[0], fila[1], fila[2], fila[3], fila[4]
        agregar_a_listas(nombres, especies, duenos, nombre, especie, dueno)
        mascotas.append([nombre, especie, dueno])
        mi_contador()
        total_cargados = incrementar(total_cargados)
        registros_combinados.append({
            "codigo": codigo,
            "nombre": nombre,
            "especie": especie,
            "dueño": dueno,
            "primer_nombre_dueño": primer_nombre
        })
    print(f"-> [SQLite] Base de datos '{NOMBRE_BD}' consultada: {total_cargados} paciente(s) cargado(s).")
    return total_cargados

def limpiar_texto(texto):
    texto_limpio = texto.strip().replace("-", " ")
    return texto_limpio.title()

def generar_codigo_mascota(nombre, especie, numero):
    sub_nombre = nombre[0:3].upper()
    sub_especie = especie[0:3].upper()
    return f"{sub_nombre}-{sub_especie}-{numero:02d}"

def agregar_a_listas(lista_n, lista_e, lista_d, nombre, especie, dueno):
    lista_n.append(nombre)
    lista_e.append(especie)
    lista_d.append(dueno)

def incrementar(numero):
    numero = numero + 1
    return numero

def decrementar(numero):
    if numero > 0:
        numero = numero - 1
    return numero

def crear_contador():
    conteo = 0

    def contar():
        nonlocal conteo
        conteo += 1
        return conteo

    return contar

def contar_especie_recursivo(lista_especies, especie_buscada, indice=0):
    if indice >= len(lista_especies):
        return 0
    coincidencia = 1 if lista_especies[indice].lower() == especie_buscada.lower() else 0
    return coincidencia + contar_especie_recursivo(lista_especies, especie_buscada, indice + 1)

def contar_especie_iterativo(lista_especies, especie_buscada):
    contador = 0
    for esp in lista_especies:
        if esp.lower() == especie_buscada.lower():
            contador += 1
    return contador

def buscar_por_codigo_recursivo(registros_combinados, codigo_buscado, indice=0):
    if indice >= len(registros_combinados):
        return None
    if registros_combinados[indice]["codigo"].upper() == codigo_buscado.upper():
        return registros_combinados[indice]
    return buscar_por_codigo_recursivo(registros_combinados, codigo_buscado, indice + 1)

def exportar_pacientes_txt(registros_combinados):
    archivo = open(ARCHIVO_TXT, "w", encoding="utf-8")
    for reg in registros_combinados:
        linea = f"{reg['codigo']},{reg['nombre']},{reg['especie']},{reg['dueño']}\n"
        archivo.write(linea)
    archivo.close()
    print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")

def agregar_ultimo_paciente_txt(registro):
    with open(ARCHIVO_TXT, "a", encoding="utf-8") as archivo:
        archivo.write(f"{registro['codigo']},{registro['nombre']},{registro['especie']},{registro['dueño']}\n")

def leer_pacientes_txt():
    if not os.path.exists(ARCHIVO_TXT):
        print("-> El archivo de texto aún no ha sido generado.")
        return
    print(f"\n--- LECTURA DEL ARCHIVO DE TEXTO EXPORTADO ({ARCHIVO_TXT}) ---")
    print(f"{'Código':<12} | {'Mascota':<12} | {'Especie':<10} | {'Dueño'}")
    print("-" * 55)
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) == 4:
                print(f"{datos[0]:<12} | {datos[1]:<12} | {datos[2]:<10} | {datos[3]}")

def exportar_y_leer_binario(registros_combinados):
    with open(ARCHIVO_BIN, "wb") as bin_out:
        pickle.dump(registros_combinados, bin_out)
    print(f"-> Estructura combinada exportada en archivo binario '{ARCHIVO_BIN}'.")
    with open(ARCHIVO_BIN, "rb") as bin_in:
        datos_recuperados = pickle.load(bin_in)
    print(f"-> Datos recuperados desde '{ARCHIVO_BIN}':")
    for reg in datos_recuperados:
        print("  ", reg)