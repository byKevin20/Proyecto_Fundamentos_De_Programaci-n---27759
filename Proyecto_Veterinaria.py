from utilidades_veterinaria import (
    inicializar_bd, guardar_en_sqlite, consultar_datos_sqlite,
    limpiar_texto, generar_codigo_mascota, agregar_a_listas,
    incrementar, decrementar, crear_contador,
    contar_especie_recursivo, contar_especie_iterativo, buscar_por_codigo_recursivo,
    exportar_pacientes_txt, agregar_ultimo_paciente_txt, leer_pacientes_txt, exportar_y_leer_binario
)

nombres = []
especies = []
duenos = []
mascotas = []
registros_combinados = []
contador_total = 0
mi_contador = crear_contador()

def mostrar_menu():
    print("\n" + "=" * 65)
    print("               VETERINARIA - SISTEMA DE REGISTRO")
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
    print("10. Salir")

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
            agregar_a_listas(nombres, especies, duenos, nombre, especie, dueno)
            mascotas.append([nombre, especie, dueno])
            num_historico = mi_contador()
            contador_total = incrementar(contador_total)
            codigo = generar_codigo_mascota(nombre, especie, num_historico)
            partes_dueno = dueno.split(" ")
            primer_nombre_dueno = partes_dueno[0]
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
            print(f"-> Registrado N° {num_historico} (Código: {codigo}) | "
                  f"Primer nombre del dueño: {primer_nombre_dueno} | "
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
    encontrado = False
    print(f"\nResultados de búsqueda para '{termino}':")
    for i in range(len(nombres)):
        pos_nombre = nombres[i].lower().find(termino.lower())
        pos_especie = especies[i].lower().find(termino.lower())
        if pos_nombre != -1 or pos_especie != -1:
            print(f"  - Encontrado en posición [{i}]: {registros_combinados[i]}")
            encontrado = True
    if not encontrado:
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
                numero_original = int(registros_combinados[pos]["codigo"].split("-")[-1])
                nuevo_codigo = generar_codigo_mascota(
                    registros_combinados[pos]["nombre"],
                    registros_combinados[pos]["especie"],
                    numero_original
                )
                registros_combinados[pos]["codigo"] = nuevo_codigo

            guardar_en_sqlite(registros_combinados)
            exportar_pacientes_txt(registros_combinados)
            print(f"¡Registro modificado correctamente en la aplicación, SQLite y .txt! "
                  f"(Código actual: {registros_combinados[pos]['codigo']})")
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
            eliminado = nombres.pop(pos)
            especies.pop(pos)
            duenos.pop(pos)
            mascotas.pop(pos)
            registros_combinados.pop(pos)
            contador_total = decrementar(contador_total)
            guardar_en_sqlite(registros_combinados)
            exportar_pacientes_txt(registros_combinados)
            print(f"¡Mascota '{eliminado}' eliminada de la aplicación, SQLite y .txt! "
                  f"Total activas: {contador_total}")
        else:
            print("Posición fuera de rango.")
    except ValueError:
        print("Error: Debes ingresar un número entero.")

def intercambiar_registros(i, j):
    nombres[i], nombres[j] = nombres[j], nombres[i]
    especies[i], especies[j] = especies[j], especies[i]
    duenos[i], duenos[j] = duenos[j], duenos[i]
    mascotas[i], mascotas[j] = mascotas[j], mascotas[i]
    registros_combinados[i], registros_combinados[j] = registros_combinados[j], registros_combinados[i]

def ordenar_nombre():
    if not mascotas:
        print("No hay registros para ordenar.")
        return
    n = len(nombres)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if nombres[j] > nombres[j + 1]:
                intercambiar_registros(j, j + 1)
    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    print("\n-> Lista ordenada alfabéticamente por Nombre: ")
    mostrar()

def ordenar_especie():
    if not mascotas:
        print("No hay registros para ordenar.")
        return
    n = len(especies)
    for i in range(n - 1):
        min_id = i
        for j in range(i + 1, n):
            if especies[j] < especies[min_id]:
                min_id = j
        if min_id != i:
            intercambiar_registros(i, min_id)
    guardar_en_sqlite(registros_combinados)
    exportar_pacientes_txt(registros_combinados)
    print("\n-> Lista ordenada alfabéticamente por Especie: ")
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
    total_rec = contar_especie_recursivo(especies, esp)
    total_ite = contar_especie_iterativo(especies, esp)
    print(f"-> Total de '{esp}' (Búsqueda Progresiva): {total_rec}")
    print(f"-> Total de '{esp}' (Revisión una por una): {total_ite}")
    cod = input("\nIngrese el código único a buscar (ej. LUN-GAT-01): ").strip().upper()
    if cod == "":
        print("Error: El código no puede estar vacío.")
        return
    encontrado = buscar_por_codigo_recursivo(registros_combinados, cod)
    if encontrado is not None:
        print(f"-> Paciente encontrado: {encontrado}")
    else:
        print("-> No existe ningún paciente con ese código.")

def gestionar_exportacion():
    global contador_total
    print("\n--- FLUJO DB SQLITE -> APLICACIÓN -> EXPORTACIÓN ---")
    print("1. Consultar y recargar datos desde Base de Datos SQLite (veterinaria.db)")
    print("2. Exportar datos procesados a Archivo de Texto (.txt)")
    print("3. Exportar datos procesados a Archivo Binario (.bin)")
    print("4. Exportar en ambos formatos (.txt y .bin) y mostrar contenido")
    sub_op = input("Seleccione una opción (1-4): ").strip()
    if sub_op == "1":
        contador_total = consultar_datos_sqlite(
            nombres, especies, duenos, mascotas, registros_combinados, mi_contador
        )
        mostrar()
    elif sub_op == "2":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        exportar_pacientes_txt(registros_combinados)
        leer_pacientes_txt()
    elif sub_op == "3":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        exportar_y_leer_binario(registros_combinados)
    elif sub_op == "4":
        if not mascotas:
            print("No hay registros para exportar.")
            return
        exportar_pacientes_txt(registros_combinados)
        leer_pacientes_txt()
        print()
        exportar_y_leer_binario(registros_combinados)
    else:
        print("Opción no válida.")

def main():
    global contador_total
    contador_total = consultar_datos_sqlite(
        nombres, especies, duenos, mascotas, registros_combinados, mi_contador
    )

    opcion = ""
    while opcion != "10":
        mostrar_menu()
        opcion = input("Elige una opción (1-10): ").strip()
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
            print("Saliendo del sistema veterinario...")
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()