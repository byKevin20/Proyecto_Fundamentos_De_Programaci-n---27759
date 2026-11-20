entregas = [
    {"codigo": "EST01", "archivo": "tarea1_final.pdf", "intentos": 1, "puntaje": 18, "obs": "A tiempo"},
    {"codigo": "EST02", "archivo": "laboratorio_v2.py", "intentos": 2, "puntaje": 15, "obs": "Corregido"},
    {"codigo": "EST03", "archivo": "proyecto_final.zip", "intentos": 1, "puntaje": 20, "obs": "Excelente"},
    {"codigo": "EST04", "archivo": "informe_borrador.docx", "intentos": 3, "puntaje": 12, "obs": "Incompleto"},
    {"codigo": "EST05", "archivo": "practica_v2_final.py", "intentos": 2, "puntaje": 17, "obs": "Buen trabajo"},
    {"codigo": "EST06", "archivo": "ejercicios_tema7.pdf", "intentos": 1, "puntaje": 16, "obs": "A tiempo"},
    {"codigo": "EST07", "archivo": "entrega_final.docx", "intentos": 1, "puntaje": 19, "obs": "Destacado"},
    {"codigo": "EST08", "archivo": "codigo_base_v2.py", "intentos": 2, "puntaje": 14, "obs": "Revisar lógica"}
]

def pedir_texto_no_vacio(mensaje):
    """Valida que el usuario no ingrese una búsqueda vacía."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("-> Error: El dato no puede estar vacío. Intente de nuevo.")

def pedir_entero_positivo(mensaje):
    """Valida que el número ingresado sea un entero mayor o igual a 0."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            return int(entrada)
        print("-> Error: Ingrese un número entero válido (sin negativos ni letras).")

def sumar_puntajes_recursivo(lista, indice=0):
    """Calcula la sumatoria de puntajes de la lista de entregas de forma recursiva."""
    if indice >= len(lista):
        return 0
    return lista[indice]["puntaje"] + sumar_puntajes_recursivo(lista, indice + 1)

def buscar_estudiante_recursivo(lista, codigo_buscado, indice=0):
    """Busca un código de estudiante en la lista avanzando posición por posición."""
    if indice >= len(lista):
        return None
    if lista[indice]["codigo"].upper() == codigo_buscado.upper():
        return lista[indice]
    return buscar_estudiante_recursivo(lista, codigo_buscado, indice + 1)

def contar_archivos_palabra_recursivo(lista, palabra_clave, indice=0):
    """Cuenta cuántos nombres de archivo contienen una palabra clave (ej. 'final' o 'v2')."""
    if indice >= len(lista):
        return 0
    coincidencia = 1 if palabra_clave.lower() in lista[indice]["archivo"].lower() else 0
    return coincidencia + contar_archivos_palabra_recursivo(lista, palabra_clave, indice + 1)

def factorial_recursivo(n):
    """Calcula el factorial de un número natural n (n!)."""
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)

def potencia_recursiva(base, exponente):
    """Calcula la potencia de una base elevada a un exponente entero positivo."""
    if exponente == 0:
        return 1
    return base * potencia_recursiva(base, exponente - 1)

def sumar_puntajes_iterativo(lista):
    """Calcula la sumatoria de puntajes usando un ciclo for tradicional."""
    total = 0
    for entrega in lista:
        total += entrega["puntaje"]
    return total

def buscar_estudiante_iterativo(lista, codigo_buscado):
    """Busca un estudiante usando un ciclo for."""
    for entrega in lista:
        if entrega["codigo"].upper() == codigo_buscado.upper():
            return entrega
    return None

def contar_archivos_palabra_iterativo(lista, palabra_clave):
    """Cuenta archivos que contienen la palabra clave usando un ciclo for."""
    contador = 0
    for entrega in lista:
        if palabra_clave.lower() in entrega["archivo"].lower():
            contador += 1
    return contador

def mostrar_entregas(lista):
    print("\n--- LISTADO DE ENTREGAS DIGITALES REGISTRADAS ---")
    print(f"{'Código':<8} | {'Nombre de Archivo':<23} | {'Intentos':<8} | {'Puntaje':<7} | {'Observación'}")
    print("-" * 75)
    for e in lista:
        print(f"{e['codigo']:<8} | {e['archivo']:<23} | {e['intentos']:<8} | {e['puntaje']:<7} | {e['obs']}")

def menu():
    while True:
        print("\n=== SISTEMA DE ANÁLISIS DE ENTREGAS DIGITALES ===")
        print("1. Mostrar las 8 entregas registradas")
        print("2. Calcular sumatoria de puntajes")
        print("3. Buscar entrega por código de estudiante")
        print("4. Contar archivos con palabra clave final o v2")
        print("5. Probar funciones simples: Factorial y Potencia")
        print("6. Salir")
        
        opcion = pedir_texto_no_vacio("Seleccione una opción (1-6): ")

        if opcion == "1":
            mostrar_entregas(entregas)
        elif opcion == "2":
            suma_rec = sumar_puntajes_recursivo(entregas)
            suma_ite = sumar_puntajes_iterativo(entregas)
            print(f"\n-> Sumatoria de puntajes (Recursiva): {suma_rec}")
            print(f"-> Sumatoria de puntajes (Iterativa): {suma_ite}")
            print(f"-> Promedio del grupo: {suma_rec / len(entregas):.2f}")
        elif opcion == "3":
            codigo = pedir_texto_no_vacio("Ingrese el código del estudiante a buscar (ej. EST03): ")
            resultado = buscar_estudiante_recursivo(entregas, codigo)
            if resultado is not None:
                print(f"-> Encontrado: Archivo='{resultado['archivo']}' | Puntaje={resultado['puntaje']} | Obs='{resultado['obs']}'")
            else:
                print("-> Resultado: No se encontró ningún estudiante con ese código.")
        elif opcion == "4":
            palabra = pedir_texto_no_vacio("Ingrese la palabra clave a buscar en los archivos (ej. final o v2): ")
            total_rec = contar_archivos_palabra_recursivo(entregas, palabra)
            total_ite = contar_archivos_palabra_iterativo(entregas, palabra)
            print(f"-> Archivos que contienen '{palabra}' (Recursivo): {total_rec}")
            print(f"-> Archivos que contienen '{palabra}' (Iterativo): {total_ite}")
        elif opcion == "5":
            print("\n--- Prueba de Factorial y Potencia ---")
            num = pedir_entero_positivo("Ingrese un número entero para calcular su factorial: ")
            print(f"-> Factorial de {num}! = {factorial_recursivo(num)}")
            base = pedir_entero_positivo("Ingrese la base para la potencia: ")
            exp = pedir_entero_positivo("Ingrese el exponente: ")
            print(f"-> Potencia de {base}^{exp} = {potencia_recursiva(base, exp)}")
        elif opcion == "6":
            print("Cerrando el programa...")
            break
        else:
            print("-> Opción no válida. Elija del 1 al 6.")

if __name__ == "__main__":
    menu()