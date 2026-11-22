from capa_negocio import (
    NOMBRE_BD, ARCHIVO_TXT, ARCHIVO_BIN,
    limpiar_texto, crear_contador,
    autenticar_usuario, crear_nuevo_usuario, obtener_historial_auditoria,
    cargar_pacientes_desde_bd, registrar_mascota_negocio, buscar_mascota_negocio,
    modificar_mascota_negocio, eliminar_mascota_negocio,
    ordenar_por_nombre_burbuja, ordenar_por_especie_seleccion,
    ejecutar_consulta_recursiva, exportar_txt_negocio, exportar_bin_negocio
)

nombres = []
especies = []
duenos = []
mascotas = []
registros_combinados = []
contador_total = 0
mi_contador = crear_contador()
usuario_actual = None
rol_actual = None

def pantalla_autenticacion():
    global usuario_actual, rol_actual
    while True:
        print("\n" + "=" * 65)
        print("           VETERINARIA - INICIO DE SESIÓN")
        print("=" * 65)
        print("1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        op = input("Seleccione una opción (1-3): ").strip()

        if op == "1":
            intentos = 3
            while intentos > 0:
                print("\n--- AUTENTICACIÓN DE USUARIO ---")
                user = input("Usuario: ").strip()
                clave = input("Contraseña: ").strip()
                res = autenticar_usuario(user, clave)
                if res is not None:
                    usuario_actual, rol_actual = res
                    print(f"\n-> ¡Bienvenido, {usuario_actual} ({rol_actual})!")
                    return True
                intentos -= 1
                print(f"Error: Usuario o contraseña incorrectos. Intentos restantes: {intentos}")
            print("Se agotaron los intentos de inicio de sesión.")
        elif op == "2":
            print("\n--- REGISTRO DE NUEVO USUARIO ---")
            nuevo_user = input("Nuevo nombre de usuario: ").strip()
            nueva_clave = input("Nueva contraseña: ").strip()
            rol = input("Rol (Enter para 'Recepcionista'): ").strip() or "Recepcionista"
            ok, msg = crear_nuevo_usuario(nuevo_user, nueva_clave, rol)
            print(f"-> {msg}")
        elif op == "3":
            print("Saliendo del sistema veterinario...")
            return False
        else:
            print("Opción inválida. Intenta nuevamente.")

def mostrar_menu():
    print("\n" + "=" * 65)
    print("               VETERINARIA - SISTEMA DE REGISTRO")
    print(f"       Usuario activo: {usuario_actual} ({rol_actual})")
    print("=" * 65)
    print("1. Registrar mascotas")
    print("2. Mostrar todos")
    print("3. Buscar mascota (por nombre o especie)")
    print("4. Modificar mascota")
    print("5. Eliminar mascota")
    print("6. Ordenar por nombre")
    print("7. Ordenar por especie")
    print("8. Consultas (Conteo y búsqueda por código)")
    print("9. Exportar resultados a archivos")
    print("10. Ver historial de auditoría")
    print("11. Salir")

def registrar():
    global contador_total
    try:
        cantidad = int(input("¿Cuántas mascotas deseas registrar?: "))
        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("Error: Debes escribir un número entero válido.")
        return

    for i in range(cantidad):
        print(f"\n--- Mascota {i + 1} de {cantidad} ---")
        nombre = limpiar_texto(input("Nombre de la mascota: "))
        especie = limpiar_texto(input("Especie (ej. Perro, Gato): "))
        dueno = limpiar_texto(input("Nombres y apellidos del dueño: "))
        if nombre == "" or especie == "" or dueno == "":
            print("Error: Nombre, especie y dueño son obligatorios. Registro omitido.")
        else:
            reg, num_hist, contador_total = registrar_mascota_negocio(
                usuario_actual, nombre, especie, dueno,
                nombres, especies, duenos, mascotas, registros_combinados,
                mi_contador, contador_total
            )
            print(f"-> Registrado N° {num_hist} (Código: {reg['codigo']}) | "
                  f"Primer nombre del dueño: {reg['primer_nombre_dueño']} | "
                  f"Total activas: {contador_total} (Guardado en SQLite)")

def mostrar():
    if not mascotas:
        print("No hay mascotas registradas actualmente.")
        return
    print("\n--- A) LISTAS ---")
    for i in range(len(nombres)):
        print(f"[{i}] Mascota: {nombres[i].title():10s} | Especie: {especies[i]:8s} | Dueño: {duenos[i]}")
    print("\n--- B) MATRIZ ---")
    print(f"  | {'NOMBRE':12s} | {'ESPECIE':10s} | {'DUEÑO':16s} |")
    print("  " + "-" * 47)
    for fila in range(len(mascotas)):
        print("  |", end="")
        for col in range(len(mascotas[fila])):
            anchos = [12, 10, 16]
            print(f" {mascotas[fila][col]:{anchos[col]}s} |", end="")
        print()
    print("\n--- C) ESTRUCTURA ---")
    for reg in registros_combinados:
        print(f"  Código: {reg['codigo']} | Nombre: {reg['nombre']} | "
              f"Especie: {reg['especie']} | Dueño: {reg['dueño']}")

def buscar():
    if not mascotas:
        print("No hay registros para buscar.")
        return
    termino = limpiar_texto(input("Ingrese el nombre o especie a buscar: "))
    if termino == "":
        print("Error: El término de búsqueda no puede estar vacío.")
        return
    resultados = buscar_mascota_negocio(
        usuario_actual, termino, nombres, especies, registros_combinados
    )
    print(f"\nResultados de búsqueda para '{termino}':")
    if resultados:
        for idx, reg in resultados:
            print(f"  - Encontrado en posición [{idx}]: {reg}")
    else:
        print("  No se encontraron coincidencias.")

def modificar():
    if not mascotas:
        print("No hay registros para modificar.")
        return
    mostrar()
    try:
        pos = int(input("\nPosición a modificar: "))
        if 0 <= pos < len(nombres):
            nuevo_nombre = limpiar_texto(input("Nuevo nombre (Enter para mantener actual): "))
            nueva_especie = limpiar_texto(input("Nueva especie (Enter para mantener actual): "))
            nuevo_dueno = limpiar_texto(input("Nuevo dueño (Enter para mantener actual): "))
            actualizado = modificar_mascota_negocio(
                usuario_actual, pos, nuevo_nombre, nueva_especie, nuevo_dueno,
                nombres, especies, duenos, mascotas, registros_combinados
            )
            print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
            print(f"¡Registro modificado correctamente en la aplicación, SQLite y .txt! "
                  f"(Código actual: {actualizado['codigo']})")
        else:
            print("Posición fuera de rango.")
    except ValueError:
        print("Error: Debes ingresar un número entero.")

def eliminar():
    global contador_total
    if not mascotas:
        print("No hay registros para eliminar.")
        return
    mostrar()
    try:
        pos = int(input("\nPosición a eliminar: "))
        if 0 <= pos < len(nombres):
            eliminado, contador_total = eliminar_mascota_negocio(
                usuario_actual, pos,
                nombres, especies, duenos, mascotas, registros_combinados, contador_total
            )
            print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
            print(f"¡Mascota '{eliminado}' eliminada de la aplicación, SQLite y .txt! "
                  f"Total activas: {contador_total}")
        else:
            print("Posición fuera de rango.")
    except ValueError:
        print("Error: Debes ingresar un número entero.")

def ordenar_nombre():
    if not mascotas:
        print("No hay registros para ordenar.")
        return
    ordenar_por_nombre_burbuja(usuario_actual, nombres, especies, duenos, mascotas, registros_combinados)
    print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
    print("\n-> Lista ordenada alfabéticamente por Nombre:")
    mostrar()

def ordenar_especie():
    if not mascotas:
        print("No hay registros para ordenar.")
        return
    ordenar_por_especie_seleccion(usuario_actual, nombres, especies, duenos, mascotas, registros_combinados)
    print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
    print("\n-> Lista ordenada alfabéticamente por Especie:")
    mostrar()

def consultas_recursivas():
    if not mascotas:
        print("No hay registros para consultar.")
        return
    print("\n--- CONSULTAS ---")
    esp = limpiar_texto(input("Ingrese la especie a contar (ej. Perro, Gato, Ave): "))
    if esp == "":
        print("Error: Debe escribir una especie válida.")
        return
    cod = input("Ingrese el código único a buscar (ej. LUN-GAT-01): ").strip().upper()
    if cod == "":
        print("Error: El código no puede estar vacío.")
        return
    total_rec, total_ite, encontrado = ejecutar_consulta_recursiva(
        usuario_actual, especies, registros_combinados, esp, cod
    )
    print(f"-> Total de '{esp}' (Búsqueda Progresiva): {total_rec}")
    print(f"-> Total de '{esp}' (Revisión una por una): {total_ite}")
    if encontrado is not None:
        print(f"-> Paciente encontrado: {encontrado}")
    else:
        print("-> No existe ningún paciente con ese código.")

def mostrar_lectura_txt(filas):
    if filas is None:
        print("-> El archivo de texto aún no ha sido generado.")
        return
    print(f"\n--- LECTURA DEL ARCHIVO DE TEXTO EXPORTADO ({ARCHIVO_TXT}) ---")
    print(f"{'Código':<12} | {'Mascota':<12} | {'Especie':<10} | {'Dueño'}")
    print("-" * 55)
    for datos in filas:
        print(f"{datos[0]:<12} | {datos[1]:<12} | {datos[2]:<10} | {datos[3]}")

def gestionar_exportacion():
    global contador_total
    print("\n--- FLUJO DB SQLITE -> APLICACIÓN -> EXPORTACIÓN ---")
    print(f"1. Consultar y recargar datos desde Base de Datos SQLite ({NOMBRE_BD})")
    print("2. Exportar datos procesados a Archivo de Texto (.txt)")
    print("3. Exportar datos procesados a Archivo Binario (.bin)")
    print("4. Exportar en ambos formatos (.txt y .bin) y mostrar contenido")
    sub_op = input("Seleccione una opción (1-4): ").strip()

    if sub_op == "1":
        contador_total = cargar_pacientes_desde_bd(
            nombres, especies, duenos, mascotas, registros_combinados, mi_contador
        )
        print(f"-> [SQLite] Base de datos '{NOMBRE_BD}' consultada: {contador_total} paciente(s) cargado(s).")
        mostrar()
    elif sub_op == "2":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        filas = exportar_txt_negocio(usuario_actual, registros_combinados)
        print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
        mostrar_lectura_txt(filas)
    elif sub_op == "3":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        datos = exportar_bin_negocio(usuario_actual, registros_combinados)
        print(f"-> Estructura combinada exportada en archivo binario '{ARCHIVO_BIN}'.")
        print(f"-> Datos recuperados desde '{ARCHIVO_BIN}':")
        for reg in datos:
            print("  ", reg)
    elif sub_op == "4":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        filas = exportar_txt_negocio(usuario_actual, registros_combinados)
        print(f"-> Datos exportados correctamente en '{ARCHIVO_TXT}'.")
        mostrar_lectura_txt(filas)
        print()
        datos = exportar_bin_negocio(usuario_actual, registros_combinados)
        print(f"-> Estructura combinada exportada en archivo binario '{ARCHIVO_BIN}'.")
        print(f"-> Datos recuperados desde '{ARCHIVO_BIN}':")
        for reg in datos:
            print("  ", reg)
    else:
        print("Opción no válida.")

def ver_auditoria():
    filas = obtener_historial_auditoria()
    if not filas:
        print("No hay eventos registrados en la auditoría.")
        return
    print("\n--- AUDITORÍA - HISTORIAL DE CAMBIOS ---")
    print(f"{'ID':<4} | {'Usuario':<12} | {'Acción':<15} | {'Fecha y Hora':<19} | {'Detalle'}")
    print("-" * 92)
    for id_ev, user, accion, detalle, fecha_hora in filas:
        print(f"{id_ev:<4} | {user:<12} | {accion:<15} | {fecha_hora:<19} | {detalle}")

def main():
    global contador_total
    if not pantalla_autenticacion():
        return

    contador_total = cargar_pacientes_desde_bd(
        nombres, especies, duenos, mascotas, registros_combinados, mi_contador
    )
    print(f"-> [SQLite] Base de datos '{NOMBRE_BD}' consultada: {contador_total} paciente(s) cargado(s).")

    opcion = ""
    while opcion != "11":
        mostrar_menu()
        opcion = input("Elige una opción (1-11): ").strip()
        if opcion == "1":
            registrar()
        elif opcion == "2":
            mostrar()
        elif opcion == "3":
            buscar()
        elif opcion == "4":
            modificar()
        elif opcion == "5":
            eliminar()
        elif opcion == "6":
            ordenar_nombre()
        elif opcion == "7":
            ordenar_especie()
        elif opcion == "8":
            consultas_recursivas()
        elif opcion == "9":
            gestionar_exportacion()
        elif opcion == "10":
            ver_auditoria()
        elif opcion == "11":
            print("Saliendo del sistema veterinario...")
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()