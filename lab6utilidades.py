def pedir_dato_no_vacio(mensaje):
    """Pide un dato por teclado y valida que el usuario no lo deje en blanco."""
    while True:
        dato = input(mensaje).strip()
        if dato != "":
            return dato
        print("-> Error: Este campo no puede quedar vacío. Intente de nuevo.")

def buscar_equipo_por_codigo(lista_equipos, codigo_buscado):
    """Busca un equipo por su código y lo devuelve si existe, o None si no existe."""
    codigo_limpio = codigo_buscado.strip().upper()
    for equipo in lista_equipos:
        if equipo["codigo"] == codigo_limpio:
            return equipo
    return None