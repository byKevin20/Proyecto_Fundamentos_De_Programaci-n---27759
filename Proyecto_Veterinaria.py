nombres = [] 
especies = [] 
duenos = [] 
mascotas = [] 

contador_total = 0

def mostrar_menu():
    print("\n--- VETERINARIA REGISTRO ---")
    print("1. Registrar")
    print("2. Mostrar todos")
    print("3. Buscar")
    print("4. Modificar")
    print("5. Eliminar")
    print("6. Ordenar por (nombre)")
    print("7. Ordenar por (especie)")
    print("8. Salir")

def limpiar_texto(texto):
    return texto.strip().title()

def agregar_a_listas(lista_n, lista_e, lista_d, nombre, especie, dueno):
    lista_n.append(nombre)
    lista_e.append(especie)
    lista_d.append(dueno)

def incrementar(numero):
    numero = numero + 1
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
        cantidad = int(input("¿Cuántas mascotas registrar? "))
    except ValueError:
        print("Error: Debes escribir un número")
        return
    for i in range(cantidad): 
        print(f"\nMascota {i+1}")
        nombre = limpiar_texto(input("Nombre: "))
        especie = limpiar_texto(input("Especie: "))
        dueno = limpiar_texto(input("Dueño: "))

        if nombre == "" or dueno == "":
            print("Error: Nombre y dueño obligatorios")
        else:
            agregar_a_listas(nombres, especies, duenos, nombre, especie, dueno)
            mascotas.append([nombre, especie, dueno])

            contador_total = incrementar(contador_total)
            print(f"Registrado N° {mi_contador()} - Total: {contador_total}")

def mostrar():
    if not mascotas:
        print("No hay registros")
        return
    print("\n--- LISTA ---")
    for i in range(len(mascotas)): 
        print(f"{i}: {nombres[i].upper()} -> {especies[i]} | Dueño: {duenos[i]} | {mascotas[i]}")

def buscar():
    buscar_nombre = limpiar_texto(input("Buscar nombre: "))
    encontrado = False
    for i in range(len(nombres)):
        if nombres[i].lower().startswith(buscar_nombre.lower()):
            print(f"Encontrado en pos {i}: {mascotas[i]}")
            encontrado = True
    if not encontrado:
        print("No encontrado")

def modificar():
    mostrar()
    try:
        pos = int(input("Posición a modificar: "))
        if 0 <= pos < len(nombres):
            nuevo = limpiar_texto(input("Nuevo nombre: "))
            nombres[pos] = nuevo
            mascotas[pos][0] = nuevo 
            print("Modificado!")
        else:
            print("Posición inválida")
    except ValueError:
        print("Debe ser número")

def eliminar():
    mostrar()
    try:
        pos = int(input("Posición a eliminar: "))
        if 0 <= pos < len(nombres):
            del nombres[pos]
            del especies[pos]
            del duenos[pos]
            del mascotas[pos]
            print("Eliminado!")
        else:
            print("Posición inválida")
    except ValueError:
        print("Debe ser número")

def ordenar_nombre():
    n = len(nombres)
    for i in range(n):
        for j in range(n - 1 - i):
            if nombres[j] > nombres[j+1]:
                nombres[j], nombres[j+1] = nombres[j+1], nombres[j]
                especies[j], especies[j+1] = especies[j+1], especies[j]
                duenos[j], duenos[j+1] = duenos[j+1], duenos[j]
                mascotas[j], mascotas[j+1] = mascotas[j+1], mascotas[j]
    print("Ordenado por (nombre): ")
    mostrar()

def ordenar_especie():
    n = len(especies)
    for i in range(n):
        min_id = i
        for j in range(i+1, n):
            if especies[j] < especies[min_id]:
                min_id = j
        nombres[i], nombres[min_id] = nombres[min_id], nombres[i]
        especies[i], especies[min_id] = especies[min_id], especies[i]
        duenos[i], duenos[min_id] = duenos[min_id], duenos[i]
        mascotas[i], mascotas[min_id] = mascotas[min_id], mascotas[i]
    print("Ordenado por (especie): ")
    mostrar()

def main():
    opcion = ""
    while opcion!= "8": 
        mostrar_menu()
        opcion = input("Elige: ")

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
            print("Saliendo...")
        else:
            print("Opción inválida")

main()