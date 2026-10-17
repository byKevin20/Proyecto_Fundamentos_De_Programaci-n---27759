def etapa_1_listas_unidimensionales():
    print("=" * 65)
    print("ETAPA 1: EXPLORACIÓN DE LISTAS UNIDIMENSIONALES")
    print("=" * 65)

    numeros = [15, 42, 8, 23, 67, 4, 91, 33, 50, 19]
    print(f"Lista inicial (10 enteros): {numeros}\n")

    print("Recorrido de elementos: ")
    for indice, valor in enumerate(numeros):
        print(f"  Posición [{indice}] (Elemento #{indice + 1}): {valor}")

    nuevo_valor = int(input("\nIngrese el nuevo valor para el tercer elemento (posición 2): "))
    valor_anterior = numeros[2]
    numeros[2] = nuevo_valor
    print(f"Tercer elemento modificado ({valor_anterior} -> {numeros[2]}).")
    print(f"Lista actualizada: {numeros}")

    buscado = int(input("\nIngrese un número entero a buscar en la lista: "))
    encontrado = False
    posicion_encontrada = -1
    for i in range(len(numeros)):
        if numeros[i] == buscado:
            encontrado = True
            posicion_encontrada = i
            break

    if encontrado:
        print(f"Resultado: El número {buscado} Si existe en la lista (índice {posicion_encontrada}).\n")
    else:
        print(f"Resultado: El número {buscado} No existe en la lista.\n")

def etapa_2_listas_bidimensionales():
    print("=" * 65)
    print("ETAPA 2: USO DE LISTAS/ARREGLOS BIDIMENSIONALES (MATRIZ 3x3)")
    print("=" * 65)

    matriz = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    print("Ingrese los valores enteros para la matriz de 3x3:")
    for fila in range(3):
        for col in range(3):
            matriz[fila][col] = int(input(f"  Elemento [{fila}][{col}]: "))

    print("\nMatriz 3x3:")
    suma_total = 0
    for fila in range(3):
        print("  |", end="")
        for col in range(3):
            valor = matriz[fila][col]
            suma_total += valor
            print(f"{valor:5d}", end=" ")
        print("|")

    print(f"\nSuma total de todos los elementos de la matriz: {suma_total}\n")

def etapa_3_operaciones_listas_dinamicas():
    print("=" * 65)
    print("ETAPA 3: MENÚ DE OPERACIONES SOBRE UNA LISTA DINÁMICA")
    print("=" * 65)

    lista_dinamica = [10, 20, 30, 40]
    print(f"Lista dinámica inicial: {lista_dinamica}")

    while True:
        print("\n--- MENÚ DE OPERACIONES ---")
        print("1. Insertar un elemento al final")
        print("2. Eliminar un elemento por posición")
        print("3. Buscar un valor y mostrar su posición")
        print("4. Mostrar la lista actualizada")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            nuevo = int(input("Ingrese el valor entero a insertar al final: "))
            lista_dinamica.append(nuevo)
            print(f"-> Elemento {nuevo} insertado correctamente.")

        elif opcion == "2":
            if not lista_dinamica:
                print("-> La lista está vacía; no se puede eliminar.")
            else:
                pos = int(input(f"Ingrese la posición a eliminar (0 a {len(lista_dinamica) - 1}): "))
                if 0 <= pos < len(lista_dinamica):
                    eliminado = lista_dinamica.pop(pos)
                    print(f"-> Elemento {eliminado} en la posición [{pos}] eliminado.")
                else:
                    print("-> Error: Posición fuera de rango.")

        elif opcion == "3":
            valor_buscar = int(input("Ingrese el valor a buscar: "))
            if valor_buscar in lista_dinamica:
                pos = lista_dinamica.index(valor_buscar)
                print(f"-> El valor {valor_buscar} se encuentra en la posición (índice) [{pos}].")
            else:
                print(f"-> El valor {valor_buscar} no se encuentra en la lista.")

        elif opcion == "4":
            print(f"-> Lista actualizada: {lista_dinamica}")

        elif opcion == "5":
            print("-> Saliendo del menú de operaciones.\n")
            break
        else:
            print("-> Opción no válida. Intente nuevamente.")

def ordenamiento_burbuja(lista_original):
    lista = lista_original.copy()
    n = len(lista)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparaciones += 1
            if lista[j] > lista[j + 1]:
                temp = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temp
                intercambios += 1

    return lista, comparaciones, intercambios

def ordenamiento_seleccion(lista_original):
    lista = lista_original.copy()
    n = len(lista)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):
        indice_minimo = i
        for j in range(i + 1, n):
            comparaciones += 1
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j

        if indice_minimo != i:
            temp = lista[i]
            lista[i] = lista[indice_minimo]
            lista[indice_minimo] = temp
            intercambios += 1

    return lista, comparaciones, intercambios

def etapa_4_algoritmos_ordenamiento():
    print("=" * 65)
    print("ETAPA 4: APLICACIÓN DE ALGORITMOS DE ORDENAMIENTO")
    print("=" * 65)

    datos_desordenados = [64, 25, 12, 22, 11, 90, 34, 7, 48, 19]

    print("Algoritmo de Ordenamiento Burbuja: ")
    print(f"  Lista ANTES de ordenar : {datos_desordenados}")
    ordenada_burbuja, comp_b, int_b = ordenamiento_burbuja(datos_desordenados)
    print(f"  Lista DESPUÉS de ordenar: {ordenada_burbuja}")
    print(f"  Comparaciones: {comp_b} | Intercambios: {int_b}\n")

    print("Algoritmo de Ordenamiento por Selección: ")
    print(f"  Lista ANTES de ordenar : {datos_desordenados}")
    ordenada_seleccion, comp_s, int_s = ordenamiento_seleccion(datos_desordenados)
    print(f"  Lista DESPUÉS de ordenar: {ordenada_seleccion}")
    print(f"  Comparaciones: {comp_s} | Intercambios: {int_s}\n")

    print("Comparación de ambos algoritmos: ")
    print(f"  ¿Ambos producen el mismo resultado ordenado?: {ordenada_burbuja == ordenada_seleccion}")
    print(f"  Diferencia de intercambios (Burbuja y Selección): {int_b} y {int_s} "
          f"(Selección realizó {int_b - int_s} intercambios menos).")

if __name__ == "__main__":
    etapa_1_listas_unidimensionales()
    etapa_2_listas_bidimensionales()
    etapa_3_operaciones_listas_dinamicas()
    etapa_4_algoritmos_ordenamiento()