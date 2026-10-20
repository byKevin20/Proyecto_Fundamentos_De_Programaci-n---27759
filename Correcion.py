nombres = []
especies = []
duenos = []
mascotas = []               
registros_combinados = []   

contador_total = 0         

def mostrar_menu():
    print("\n" + "=" * 60)
    print("      VETERINARIA - SISTEMA DE REGISTRO")
    print("=" * 60)
    print("1. Registrar mascotas")
    print("2. Mostrar todos")
    print("3. Buscar mascota")
    print("4. Modificar mascota")
    print("5. Eliminar mascota")
    print("6. Ordenar por nombre")
    print("7. Ordenar por especie")
    print("8. Salir")

def limpiar_texto(texto):
    texto_limpio = " ".join(texto.replace("-", " ").split())
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

mi_contador = crear_contador()

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
        dueno = limpiar_texto(input("Nombre y apellido del dueño: "))

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

            registros_combinados.append({
                "codigo": codigo,
                "numero": num_historico,
                "nombre": nombre,
                "especie": especie,
                "dueno": dueno,
                "primer_nombre_dueno": primer_nombre_dueno
            })

            print(f"-> Registrado N° {num_historico} (Código: {codigo}) | "
                  f"Primer nombre del dueño (split): {primer_nombre_dueno} | "
                  f"Total activas: {contador_total}")

def mostrar():
    if not mascotas:
        print("No hay mascotas registradas actualmente.")
        return

    print("\n--- A) LISTAS PARALELAS ---")
    for i in range(len(nombres)):
        print(f"[{i}] Código: {registros_combinados[i]['codigo']} | Mascota: {nombres[i].upper():10s} | Especie: {especies[i]:8s} | Dueño: {duenos[i]}")

    print("\n--- B) MATRIZ BIDIMENSIONAL ---")
    print(f"  | {'NOMBRE':12s} | {'ESPECIE':10s} | {'DUEÑO':16s} |")
    print("  " + "-" * 47)
    anchos = [12, 10, 16]
    for fila in range(len(mascotas)):
        print("  |", end="")
        for col in range(len(mascotas[fila])):
            print(f" {mascotas[fila][col]:{anchos[col]}s} |", end="")
        print()

    print("\n--- C) ESTRUCTURA COMBINADA ---")
    for reg in registros_combinados:
        print(f"  Código: {reg['codigo']} | Nombre: {reg['nombre']} | "
              f"Especie: {reg['especie']} | Dueño: {reg['dueno']}")

def buscar():
    if not mascotas:
        print("No hay registros para buscar.")
        return

    termino = limpiar_texto(input("Ingrese el nombre, especie o dueño a buscar: "))
    if termino == "":
        print("Error: Debes escribir un término de búsqueda.")
        return

    encontrado = False

    print(f"\nResultados de búsqueda para '{termino}':")
    for i in range(len(nombres)):
        pos_nombre = nombres[i].lower().find(termino.lower())
        pos_especie = especies[i].lower().find(termino.lower())
        pos_dueno = duenos[i].lower().find(termino.lower())

        if pos_nombre != -1 or pos_especie != -1 or pos_dueno != -1:
            reg = registros_combinados[i]
            print(f"  - [{i}] Código: {reg['codigo']} | Nombre: {reg['nombre']} | "
                  f"Especie: {reg['especie']} | Dueño: {reg['dueno']}")
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

            if nuevo_nombre == "" and nueva_especie == "" and nuevo_dueno == "":
                print("No escribiste ningún cambio. El registro sigue igual.")
                return

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
                registros_combinados[pos]["dueno"] = nuevo_dueno
                registros_combinados[pos]["primer_nombre_dueno"] = nuevo_dueno.split(" ")[0]

            reg = registros_combinados[pos]
            reg["codigo"] = generar_codigo_mascota(reg["nombre"], reg["especie"], reg["numero"])

            print("¡Registro modificado correctamente!")
            print(f"Nuevo código: {reg['codigo']} | Nombre: {reg['nombre']} | "
                  f"Especie: {reg['especie']} | Dueño: {reg['dueno']}")
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
    texto = input("\nPosición(es) a eliminar (si son varias sepáralas con coma, ej. 0,2,3): ")
    try:
        posiciones = []
        for parte in texto.split(","):
            pos = int(parte.strip())
            if pos < 0 or pos >= len(nombres):
                print(f"Error: La posición {pos} está fuera de rango. No se eliminó nada.")
                return
            if pos not in posiciones:
                posiciones.append(pos)
    except ValueError:
        print("Error: Debes ingresar números enteros separados por coma.")
        return

    posiciones.sort(reverse=True)
    for pos in posiciones:
        eliminado = nombres.pop(pos)
        especies.pop(pos)
        duenos.pop(pos)
        mascotas.pop(pos)
        registros_combinados.pop(pos)
        contador_total = decrementar(contador_total)
        print(f"¡Mascota '{eliminado}' eliminada!")
    print(f"Total activas: {contador_total}")

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
            if nombres[j].lower() > nombres[j + 1].lower():
                intercambiar_registros(j, j + 1)

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
            if especies[j].lower() < especies[min_id].lower():
                min_id = j
        if min_id != i:
            intercambiar_registros(i, min_id)

    print("\n-> Lista ordenada alfabéticamente por Especie: ")
    mostrar()

def main():
    opcion = ""
    while opcion != "8":
        mostrar_menu()
        opcion = input("Elige una opción (1-8): ").strip()

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
            print("Saliendo del sistema...")
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main() 
