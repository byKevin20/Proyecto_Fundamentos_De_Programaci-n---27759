from capa_datos import (
    NOMBRE_BD, ARCHIVO_TXT, ARCHIVO_BIN,
    inicializar_bd, guardar_en_sqlite, consultar_filas_sqlite,
    verificar_usuario_sqlite, registrar_usuario_sqlite,
    registrar_auditoria_sqlite, consultar_auditoria_sqlite,
    exportar_pacientes_txt, agregar_ultimo_paciente_txt,
    leer_lineas_txt, exportar_y_leer_binario_datos
)

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
    return numero + 1

def decrementar(numero):
    if numero > 0:
        return numero - 1
    return numero

def crear_contador():
    conteo = 0

    def contar():
        nonlocal conteo
        conteo += 1
        return conteo

    return contar

def autenticar_usuario(usuario, contrasena):
    usuario_limpio = usuario.strip()
    contrasena_limpia = contrasena.strip()
    resultado = verificar_usuario_sqlite(usuario_limpio, contrasena_limpia)
    if resultado is not None:
        user, rol = resultado
        registrar_auditoria_sqlite(user, "Iniciar sesión", f"Ingreso exitoso ({rol})")
        return user, rol
    return None

def crear_nuevo_usuario(usuario, contrasena, rol="Recepcionista"):
    usuario_limpio = usuario.strip()
    contrasena_limpia = contrasena.strip()
    if usuario_limpio == "" or contrasena_limpia == "":
        return False, "El usuario y la contraseña no pueden estar vacíos."
    creado = registrar_usuario_sqlite(usuario_limpio, contrasena_limpia, rol)
    if creado:
        registrar_auditoria_sqlite(usuario_limpio, "Insertar", f"Nuevo usuario registrado ({rol})")
        return True, f"Usuario '{usuario_limpio}' creado correctamente."
    return False, f"El usuario '{usuario_limpio}' ya existe."

def obtener_historial_auditoria():
    return consultar_auditoria_sqlite()

def cargar_pacientes_desde_bd(nombres, especies, duenos, mascotas, registros_combinados, mi_contador):
    filas = consultar_filas_sqlite()
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
    return total_cargados

def registrar_mascota_negocio(
    usuario_activo, nombre, especie, dueno,
    nombres, especies, duenos, mascotas, registros_combinados,
    mi_contador, contador_total
):
    agregar_a_listas(nombres, especies, duenos, nombre, especie, dueno)
    mascotas.append([nombre, especie, dueno])
    num_historico = mi_contador()
    contador_total = incrementar(contador_total)
    codigo = generar_codigo_mascota(nombre, especie, num_historico)
    primer_nombre_dueno = dueno.split(" ")[0]

    nuevo_registro = {
        "codigo": codigo,
        "nombre": nombre,
        "especie": especie,
        "dueño": dueno,
        "primer_nombre_dueño": primer_nombre_dueno
    }
    registros_combinados.append(nuevo_registro)

    guardar_en_sqlite(registros_combinados)
    agregar_ultimo_paciente_txt(nuevo_registro)
    registrar_auditoria_sqlite(
        usuario_activo,
        "Insertar",
        f"Mascota '{nombre}' ({especie}) - Código: {codigo}"
    )
    return nuevo_registro, num_historico, contador_total

def buscar_mascota_negocio(usuario_activo, termino, nombres, especies, registros_combinados):
    resultados = []
    for i in range(len(nombres)):
        pos_nombre = nombres[i].lower().find(termino.lower())
        pos_especie = especies[i].lower().find(termino.lower())
        if pos_nombre != -1 or pos_especie != -1:
            resultados.append((i, registros_combinados[i]))
    registrar_auditoria_sqlite(
        usuario_activo,
        "Buscar",
        f"Término '{termino}' -> {len(resultados)} coincidencia(s)"
    )
    return resultados

def modificar_mascota_negocio(
    usuario_activo, pos, nuevo_nombre, nueva_especie, nuevo_dueno,
    nombres, especies, duenos, mascotas, registros_combinados
):
    codigo_anterior = registros_combinados[pos]["codigo"]

    if nuevo_nombre != "":
        nombres[pos] = nuevo_nombre
        mascotas[pos][0] = nuevo_nombre
        registros_combinados[pos]["nombre"] = nuevo_nombre

    if nueva_especie != "":
        especies[pos] = nueva_especie
        mascotas[pos][1] = nueva_especie
        registros_combinados[pos]["especie"] = nueva_especie

    if nuevo_dueno != "":
        duenos[pos] = nuevo_dueno
        mascotas[pos][2] = nuevo_dueno
        registros_combinados[pos]["dueño"] = nuevo_dueno
        registros_combinados[pos]["primer_nombre_dueño"] = nuevo_dueno.split(" ")[0]

    if nuevo_nombre != "" or nueva_especie != "":
        numero_original = int(codigo_anterior.split("-")[-1])
        nuevo_codigo = generar_codigo_mascota(
            registros_combinados[pos]["nombre"],
            registros_combinados[pos]["especie"],
            numero_original
        )
        registros_combinados[pos]["codigo"] = nuevo_codigo

    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    registrar_auditoria_sqlite(
        usuario_activo,
        "Modificar",
        f"Pos [{pos}] {codigo_anterior} -> {registros_combinados[pos]['codigo']} ({registros_combinados[pos]['nombre']})"
    )
    return registros_combinados[pos]

def eliminar_mascota_negocio(
    usuario_activo, pos,
    nombres, especies, duenos, mascotas, registros_combinados, contador_total
):
    codigo_eliminado = registros_combinados[pos]["codigo"]
    eliminado = nombres.pop(pos)
    especies.pop(pos)
    duenos.pop(pos)
    mascotas.pop(pos)
    registros_combinados.pop(pos)
    contador_total = decrementar(contador_total)

    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    registrar_auditoria_sqlite(
        usuario_activo,
        "Eliminar",
        f"Mascota '{eliminado}' ({codigo_eliminado})"
    )
    return eliminado, contador_total

def intercambiar_registros(i, j, nombres, especies, duenos, mascotas, registros_combinados):
    nombres[i], nombres[j] = nombres[j], nombres[i]
    especies[i], especies[j] = especies[j], especies[i]
    duenos[i], duenos[j] = duenos[j], duenos[i]
    mascotas[i], mascotas[j] = mascotas[j], mascotas[i]
    registros_combinados[i], registros_combinados[j] = registros_combinados[j], registros_combinados[i]

def ordenar_por_nombre_burbuja(usuario_activo, nombres, especies, duenos, mascotas, registros_combinados):
    n = len(nombres)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if nombres[j] > nombres[j + 1]:
                intercambiar_registros(j, j + 1, nombres, especies, duenos, mascotas, registros_combinados)
    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    registrar_auditoria_sqlite(usuario_activo, "Modificar", "Ordenamiento alfabético por nombre")

def ordenar_por_especie_seleccion(usuario_activo, nombres, especies, duenos, mascotas, registros_combinados):
    n = len(especies)
    for i in range(n - 1):
        min_id = i
        for j in range(i + 1, n):
            if especies[j] < especies[min_id]:
                min_id = j
        if min_id != i:
            intercambiar_registros(i, min_id, nombres, especies, duenos, mascotas, registros_combinados)
    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    registrar_auditoria_sqlite(usuario_activo, "Modificar", "Ordenamiento alfabético por especie")

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

def ejecutar_consulta_recursiva(usuario_activo, especies, registros_combinados, esp, cod):
    total_rec = contar_especie_recursivo(especies, esp)
    total_ite = contar_especie_iterativo(especies, esp)
    encontrado = buscar_por_codigo_recursivo(registros_combinados, cod)
    registrar_auditoria_sqlite(
        usuario_activo,
        "Buscar",
        f"Consulta recursiva especie='{esp}' ({total_rec}) y código='{cod}'"
    )
    return total_rec, total_ite, encontrado

def exportar_txt_negocio(usuario_activo, registros_combinados):
    exportar_pacientes_txt(registros_combinados)
    filas = leer_lineas_txt()
    registrar_auditoria_sqlite(usuario_activo, "Exportar", f"Exportación a {ARCHIVO_TXT}")
    return filas

def exportar_bin_negocio(usuario_activo, registros_combinados):
    datos = exportar_y_leer_binario_datos(registros_combinados)
    registrar_auditoria_sqlite(usuario_activo, "Exportar", f"Exportación a {ARCHIVO_BIN}")
    return datos