def etapa_1_manipulacion_cadenas():
    print("=" * 65)
    print("1. MANIPULACIÓN DE CADENAS DE CARACTERES")
    print("=" * 65)

    texto = "Python facilita el procesamiento de cadenas de texto en programación"
    print(f"Texto original:\n  '{texto}'\n")

    subcadena_1 = texto[0:6]
    subcadena_2 = texto[19:32]
    print(f"a) Subcadena obtenida [0:6]   : '{subcadena_1}'")
    print(f"   Subcadena obtenida [19:32] : '{subcadena_2}'\n")

    palabra_buscar = "cadenas"
    posicion = texto.find(palabra_buscar)
    print(f"b) Búsqueda('{palabra_buscar}'):")
    if posicion != -1:
        print(f"   La palabra '{palabra_buscar}' inicia en la posición (índice): {posicion}\n")
    else:
        print(f"   La palabra '{palabra_buscar}' no se encontró.\n")

    texto_reemplazado = texto.replace("programación", "el laboratorio")
    print("c) Reemplazo('programación', 'el laboratorio'):")
    print(f"   '{texto_reemplazado}'\n")

    partes = texto.split(" ")
    print("d) Texto separado en palabras(' '):")
    print(f"   {partes}")
    print(f"   Total de palabras obtenidas: {len(partes)}\n")

def etapa_2_listas_paralelas():
    print("=" * 65)
    print("2. BÚSQUEDA EN DOS LISTAS PARALELAS (NOMBRES Y EDADES)")
    print("=" * 65)

    nombres = ["Ana", "Carlos", "Lucía", "Mateo", "Valeria"]
    edades = [20, 22, 19, 21, 23]

    print("Listado de elementos en las listas paralelas: ")
    for i in range(len(nombres)):
        print(f"  Índice [{i}] -> Nombre: {nombres[i]:8s} | Edad: {edades[i]} años")

    nombre_buscado = input("\nIngrese el nombre de la persona a buscar: ").strip()

    encontrado = False
    for i in range(len(nombres)):
        if nombres[i].lower() == nombre_buscado.lower():
            print(f"Resultado: {nombres[i]} se encuentra en la posición [{i}] y tiene {edades[i]} años.\n")
            encontrado = True
            break

    if not encontrado:
        print(f"Resultado: No se encontró a '{nombre_buscado}' en la lista.\n")

def etapa_3_estructura_combinada():
    print("=" * 65)
    print("3. ESTRUCTURA COMBINADA (LISTA DE DICCIONARIOS), BÚSQUEDA Y ORDEN")
    print("=" * 65)

    usuarios = [
        {"nombre": "Diego Vargas", "email": "diego.vargas@correo.pe", "ciudad": "Cajamarca"},
        {"nombre": "Ana Torres", "email": "ana.torres@correo.pe", "ciudad": "Lima"},
        {"nombre": "Luis Mendoza", "email": "luis.mendoza@correo.pe", "ciudad": "Cajamarca"},
        {"nombre": "Camila Ríos", "email": "camila.rios@correo.pe", "ciudad": "Trujillo"},
        {"nombre": "Fernando Díaz", "email": "fernando.diaz@correo.pe", "ciudad": "Cajamarca"},
    ]

    print("Listado inicial de la estructura combinada (usuarios): ")
    for idx, u in enumerate(usuarios):
        print(f"  [{idx}] Nombre: {u['nombre']:14s} | Email: {u['email']:24s} | Ciudad: {u['ciudad']}")

    ciudad_buscar = input("\nIngrese la ciudad a buscar: ").strip()
    coincidencias = [u for u in usuarios if u["ciudad"].lower() == ciudad_buscar.lower()]

    print(f"\nCoincidencias encontradas en la ciudad de '{ciudad_buscar}' ({len(coincidencias)}):")
    if coincidencias:
        for u in coincidencias:
            print(f"  - {u['nombre']} ({u['email']}) - Ciudad: {u['ciudad']}")
    else:
        print("  No se encontraron usuarios en esa ciudad.")

    nombres_ordenados = sorted([u["nombre"] for u in usuarios])
    usuarios_ordenados = sorted(usuarios, key=lambda x: x["nombre"])

    print("\nNombres de usuarios ordenados alfabéticamente (A-Z): ")
    print(f"  {nombres_ordenados}")

    print("\nEstructura completa ordenada alfabéticamente por nombre: ")
    for u in usuarios_ordenados:
        print(f"  - {u['nombre']:14s} | Email: {u['email']:24s} | Ciudad: {u['ciudad']}")

if __name__ == "__main__":
    etapa_1_manipulacion_cadenas()
    etapa_2_listas_paralelas()
    etapa_3_estructura_combinada()