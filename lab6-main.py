from lab6utilidades import pedir_dato_no_vacio, buscar_equipo_por_codigo

def mostrar_menu():
    """Muestra las opciones del menú principal en consola."""
    print("\n=== SISTEMA DE PRÉSTAMOS LABTECH ===")
    print("1. Registrar nuevo equipo")
    print("2. Prestar un equipo")
    print("3. Devolver un equipo")
    print("4. Listar todos los equipos y su disponibilidad")
    print("5. Consultar cantidad de equipos disponibles por categoría")
    print("6. Salir")

def registrar_equipo(equipos):
    """Registra un nuevo equipo validando que los datos no estén vacíos ni el código repetido."""
    print("\n--- Registro de Nuevo Equipo ---")
    codigo = pedir_dato_no_vacio("Ingrese el código del equipo (ej. LAP02): ").upper()
    
    if buscar_equipo_por_codigo(equipos, codigo) is not None:
        print("-> Error: Ya existe un equipo registrado con ese código.")
        return

    nombre = pedir_dato_no_vacio("Ingrese el nombre del equipo: ")
    categoria = pedir_dato_no_vacio("Ingrese la categoría (Laptop, Mouse, Cable, Kit): ")

    nuevo_equipo = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "estado": "Disponible",
        "estudiante": "-",
        "fecha": "-"
    }
    equipos.append(nuevo_equipo)
    print(f"-> Equipo '{nombre}' ({codigo}) registrado correctamente como Disponible.")

def prestar_equipo(equipos):
    """Registra el préstamo de un equipo validando que exista y que esté disponible."""
    print("\n--- Préstamo de Equipo ---")
    codigo = pedir_dato_no_vacio("Ingrese el código del equipo a prestar: ").upper()
    
    equipo = buscar_equipo_por_codigo(equipos, codigo)
    if equipo is None:
        print("-> Error: El código de equipo no existe.")
        return

    if equipo["estado"] != "Disponible":
        print(f"-> Error: El equipo '{equipo['nombre']}' no está disponible (prestado a {equipo['estudiante']}).")
        return

    estudiante = pedir_dato_no_vacio("Nombre del estudiante: ")
    fecha = pedir_dato_no_vacio("Fecha del préstamo (dd/mm/aaaa): ")

    equipo["estado"] = "No disponible"
    equipo["estudiante"] = estudiante
    equipo["fecha"] = fecha
    print(f"-> Préstamo registrado: '{equipo['nombre']}' entregado a {estudiante} el {fecha}.")

def devolver_equipo(equipos):
    """Registra la devolución de un equipo prestado para que vuelva a estar disponible."""
    print("\n--- Devolución de Equipo ---")
    codigo = pedir_dato_no_vacio("Ingrese el código del equipo a devolver: ").upper()
    
    equipo = buscar_equipo_por_codigo(equipos, codigo)
    if equipo is None:
        print("-> Error: El código de equipo no existe.")
        return

    if equipo["estado"] == "Disponible":
        print("-> Aviso: Este equipo ya figura como Disponible en el laboratorio.")
        return

    equipo["estado"] = "Disponible"
    equipo["estudiante"] = "-"
    equipo["fecha"] = "-"
    print(f"-> Devolución exitosa: El equipo '{equipo['nombre']}' está Disponible nuevamente.")

def listar_disponibilidad(equipos):
    """Muestra en una tabla ordenada todos los equipos registrados y su estado actual."""
    print("\n--- Listado de Equipos LabTech ---")
    print(f"{'Código':<8} | {'Nombre':<18} | {'Categoría':<10} | {'Estado':<15} | {'Estudiante':<12} | {'Fecha'}")
    print("-" * 80)
    for eq in equipos:
        print(f"{eq['codigo']:<8} | {eq['nombre']:<18} | {eq['categoria']:<10} | {eq['estado']:<15} | {eq['estudiante']:<12} | {eq['fecha']}")

def consultar_disponibles_por_categoria(equipos):
    """Cuenta y muestra cuántos equipos están disponibles en una categoría específica."""
    print("\n--- Consulta por Categoría ---")
    categoria_buscada = pedir_dato_no_vacio("Ingrese la categoría a consultar (ej. Laptop, Mouse, Cable): ")
    
    contador = 0
    for eq in equipos:
        if eq["categoria"].lower() == categoria_buscada.lower() and eq["estado"] == "Disponible":
            contador += 1
            
    print(f"-> Cantidad de equipos disponibles en la categoría '{categoria_buscada}': {contador}")

def ejecutar_sistema():
    inventario_equipos = [
        {"codigo": "LAP01", "nombre": "Laptop Lenovo", "categoria": "Laptop", "estado": "Disponible", "estudiante": "-", "fecha": "-"},
        {"codigo": "MOU01", "nombre": "Mouse", "categoria": "Mouse", "estado": "Disponible", "estudiante": "-", "fecha": "-"},
        {"codigo": "HDM01", "nombre": "Cable HDMI", "categoria": "Cable", "estado": "Disponible", "estudiante": "-", "fecha": "-"}
    ]

    while True:
        mostrar_menu()
        opcion = pedir_dato_no_vacio("Seleccione una opción (1-6): ")

        if opcion == "1":
            registrar_equipo(inventario_equipos)
        elif opcion == "2":
            prestar_equipo(inventario_equipos)
        elif opcion == "3":
            devolver_equipo(inventario_equipos)
        elif opcion == "4":
            listar_disponibilidad(inventario_equipos)
        elif opcion == "5":
            consultar_disponibles_por_categoria(inventario_equipos)
        elif opcion == "6":
            print("Cerrando el sistema LabTech...")
            break
        else:
            print("-> Opción no válida. Elija un número del 1 al 6.")

if __name__ == "__main__":
    ejecutar_sistema()