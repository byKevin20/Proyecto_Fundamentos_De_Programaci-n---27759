import pickle
import os

ARCHIVO_TXT = "contactos.txt"
ARCHIVO_BIN = "contactos.bin"

def pedir_contacto():
    print("\n--- Ingreso de Contacto ---")
    id_c = input("Ingrese el ID: ").strip()
    nombre = input("Ingrese el Nombre: ").strip()
    telefono = input("Ingrese el Teléfono: ").strip()
    return {"id": id_c, "nombre": nombre, "telefono": telefono}

def escribir_contactos_iniciales():
    print("\nCreación inicial del archivo de texto...")
    archivo = open(ARCHIVO_TXT, "w", encoding="utf-8")
    cantidad = int(input("¿Cuántos contactos iniciales desea registrar?: "))
    for _ in range(cantidad):
        c = pedir_contacto()
        linea = f"{c['id']},{c['nombre']},{c['telefono']}\n"
        archivo.write(linea)
    archivo.close() 
    print("-> Datos iniciales guardados y archivo cerrado correctamente.")

def leer_contactos_txt():
    print("\nLectura del archivo de texto línea por línea:")
    if not os.path.exists(ARCHIVO_TXT):
        print("-> El archivo aún no existe.")
        return
    
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        print(f"{'ID':<5} | {'Nombre':<15} | {'Teléfono':<12}")
        print("-" * 38)
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) == 3:
                print(f"{datos[0]:<5} | {datos[1]:<15} | {datos[2]:<12}")

def agregar_contacto_txt():
    print("\nAñadir nuevo registro al final del archivo...")
    c = pedir_contacto()
    with open(ARCHIVO_TXT, "a", encoding="utf-8") as archivo:
        archivo.write(f"{c['id']},{c['nombre']},{c['telefono']}\n")
    print("-> Nuevo contacto añadido.")

def procesar_contactos_txt():
    print("\nProcesamiento de datos (Conteo y Búsqueda):")
    if not os.path.exists(ARCHIVO_TXT):
        print("-> El archivo no existe.")
        return

    contactos = []
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            if len(partes) == 3:
                contactos.append({"id": partes[0], "nombre": partes[1], "telefono": partes[2]})

    print(f"-> Total de contactos registrados: {len(contactos)}")

    buscado = input("Ingrese el nombre del contacto a buscar: ").strip().lower()
    encontrados = [c for c in contactos if buscado in c["nombre"].lower()]

    if encontrados:
        print("-> Resultados encontrados:")
        for c in encontrados:
            print(f"   ID: {c['id']} | Nombre: {c['nombre']} | Teléfono: {c['telefono']}")
    else:
        print("-> No se encontró ningún contacto con ese nombre.")

def prueba_archivo_binario():
    print("\nRespaldo y recuperación en archivo binario (.bin):")
    lista_estructurada = []
    
    if os.path.exists(ARCHIVO_TXT):
        with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    lista_estructurada.append({
                        "id": int(partes[0]),
                        "nombre": partes[1],
                        "telefono": partes[2]
                    })

    with open(ARCHIVO_BIN, "wb") as bin_out:
        pickle.dump(lista_estructurada, bin_out)
    print(f"-> Estructura de datos guardada en '{ARCHIVO_BIN}'.")

    with open(ARCHIVO_BIN, "rb") as bin_in:
        datos_recuperados = pickle.load(bin_in)
    print("-> Estructura recuperada desde el archivo binario:")
    for registro in datos_recuperados:
        print("  ", registro)

def menu():
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE CONTACTOS ===")
        print("1. Crear archivo y registrar contactos iniciales")
        print("2. Leer y mostrar contactos línea por línea")
        print("3. Añadir un nuevo contacto")
        print("4. Procesar datos: Contar y buscar contacto")
        print("5. Guardar y leer estructura en archivo binario")
        print("6. Salir")
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            escribir_contactos_iniciales()
        elif opcion == "2":
            leer_contactos_txt()
        elif opcion == "3":
            agregar_contacto_txt()
        elif opcion == "4":
            procesar_contactos_txt()
        elif opcion == "5":
            prueba_archivo_binario()
        elif opcion == "6":
            print("Cerrando el programa...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()