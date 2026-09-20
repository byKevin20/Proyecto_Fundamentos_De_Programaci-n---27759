# Prueba de rama y pull request
# Comentario de prueba -Abraham
# Comentario de prueba -Jhostym

# Funcionalidad

def mostrar_menu():
    print("\n===================================")
    print("       SOPORTE ACADÉMICO")
    print("===================================")
    print("1. Registrar solicitud")
    print("2. Mostrar solicitudes")
    print("3. Ejecutar pruebas")
    print("4. Salir")
    print("===================================")
 
 
# ------------------------------------------------------------
# FUNCIÓN CON RETORNO:
# ------------------------------------------------------------
def validar_texto(texto):
    return texto.strip() != ""
 
 
# ------------------------------------------------------------
# FUNCIÓN CON RETORNO:
# valida el código del estudiante
def validar_codigo(codigo, longitud):
    codigo = codigo.strip().upper()
 
    if codigo == "":
        return False
 
    if len(codigo) != longitud:
        return False
 
    if codigo[0] != "N":
        return False
 
    if not codigo[1:].isdigit():
        return False
 
    return True
 
 
# ------------------------------------------------------------
# FUNCIÓN CON RETORNO:
# valida que el tipo de consulta sea permitido
# ------------------------------------------------------------
def validar_tipo_consulta(tipo):
    tipos_validos = [
        "matrícula",
        "matricula",   # también se acepta sin tilde
        "pagos",
        "constancia",
        "plataforma",
        "otro"
    ]
 
    return tipo.strip().lower() in tipos_validos
 
 
# FUNCIÓN CON RETORNO:
# asigna la prioridad según el tipo de consulta
# matrícula, pagos y plataforma -> Alta
# los demás                     -> Baja
def asignar_prioridad(tipo_consulta):
    tipo_consulta = tipo_consulta.strip().lower()
 
    if (tipo_consulta == "matrícula" or tipo_consulta == "matricula"
            or tipo_consulta == "pagos" or tipo_consulta == "plataforma"):
        return "Alta"
    else:
        return "Baja"
 
 
# ------------------------------------------------------------
# FUNCIÓN SIN RETORNO:
# muestra el resumen de una solicitud
# ------------------------------------------------------------
def mostrar_resumen(solicitud):
    print("\n-----------------------------------")
    print("       RESUMEN DE SOLICITUD")
    print("-----------------------------------")
    print("Código:", solicitud["codigo"])
    print("Nombre:", solicitud["nombre"])
    print("Tipo de consulta:", solicitud["tipo"])
    print("Descripción:", solicitud["descripcion"])
    print("Prioridad:", solicitud["prioridad"])
    print("-----------------------------------")
 
 
# ------------------------------------------------------------
# FUNCIÓN CON RETORNO:
# registra una nueva solicitud
# ------------------------------------------------------------
def registrar_solicitud():
    print("\n===== REGISTRAR SOLICITUD =====")
 
    longitud_codigo = 9
 
    # Contadores de intentos con datos incorrectos (variables locales)
    errores_codigo = 0
    errores_nombre = 0
    errores_tipo = 0
    errores_descripcion = 0
 
    # Solicitar código
    while True:
        codigo = input("Ingrese código de estudiante (ejemplo: N00333800): ")
 
        if validar_codigo(codigo, longitud_codigo):
            break
        else:
            print("Error: código de estudiante no válido.")
            print("Debe empezar con N seguido de", longitud_codigo - 1, "números.")
            errores_codigo = errores_codigo + 1
 
    # Solicitar nombre
    while True:
        nombre = input("Ingrese nombre del estudiante: ")
 
        if validar_texto(nombre):
            break
        else:
            print("Error: el nombre no puede estar vacío.")
            errores_nombre = errores_nombre + 1
 
    # Solicitar tipo de consulta
    while True:
        print("\nTipos de consulta disponibles:")
        print("1. matrícula")
        print("2. pagos")
        print("3. constancia")
        print("4. plataforma")
        print("5. otro")
 
        tipo = input("Ingrese el tipo de consulta: ")
 
        if validar_tipo_consulta(tipo):
            tipo = tipo.strip().lower()
            break
        else:
            print("Error: el tipo de consulta no es válido.")
            errores_tipo = errores_tipo + 1
 
    # Solicitar descripción
    while True:
        descripcion = input("Ingrese una descripción breve: ")
 
        if validar_texto(descripcion):
            break
        else:
            print("Error: la descripción no puede estar vacía.")
            errores_descripcion = errores_descripcion + 1
 
    # Asignar prioridad
    prioridad = asignar_prioridad(tipo)
 
    # Crear la solicitud
    solicitud = {
        "codigo": codigo.strip().upper(),
        "nombre": nombre.strip(),
        "tipo": tipo,
        "descripcion": descripcion.strip(),
        "prioridad": prioridad,
        "errores_codigo": errores_codigo,
        "errores_nombre": errores_nombre,
        "errores_tipo": errores_tipo,
        "errores_descripcion": errores_descripcion
    }
 
    return solicitud
 
 
# ------------------------------------------------------------
# FUNCIÓN SIN RETORNO:
# ------------------------------------------------------------
def mostrar_solicitudes(solicitudes):
 
    if len(solicitudes) == 0:
        print("\nNo hay solicitudes registradas.")
        return
 
    print("\n===================================")
    print("     SOLICITUDES REGISTRADAS")
    print("===================================")
 
    for numero, solicitud in enumerate(solicitudes, start=1):
        print("\nSolicitud N.º", numero)
        mostrar_resumen(solicitud)
 
 
# ------------------------------------------------------------
# FUNCIÓN SIN RETORNO:
# ------------------------------------------------------------
def ejecutar_pruebas(solicitudes):
    print("\n===== PRUEBAS =====")
 
    if len(solicitudes) == 0:
        print("No hay solicitudes registradas para probar.")
        print("Registre al menos una solicitud (opción 1) y vuelva a intentar.")
        return
 
    # Longitud del código, igual a la definida en registrar_solicitud
    longitud_codigo = 9
 
    total = 0
    aprobadas = 0
 
    # Se prueban los datos de cada estudiante registrado
    for numero, solicitud in enumerate(solicitudes, start=1):
 
        print("\n-----------------------------------")
        print("Solicitud N.º", numero, "-", solicitud["codigo"], "-", solicitud["nombre"])
        print("-----------------------------------")
 
        # Prueba 1: código de estudiante válido
        codigo_ok = validar_codigo(solicitud["codigo"], longitud_codigo)
        errores = solicitud["errores_codigo"]
        total = total + 1
 
        print("Prueba 1: código válido (N + 8 números)")
        print("  Dato:", solicitud["codigo"])
        if errores > 0:
            print("  Intentos con datos incorrectos:", errores)
        if codigo_ok == True and errores == 0:
            print("  Resultado: Sin problemas en los datos")
            aprobadas = aprobadas + 1
        else:
            print("  Resultado: Hay problemas en los datos")
 
        # Prueba 2: datos no vacíos (nombre y descripción)
        nombre_ok = validar_texto(solicitud["nombre"])
        descripcion_ok = validar_texto(solicitud["descripcion"])
        errores = solicitud["errores_nombre"] + solicitud["errores_descripcion"]
        total = total + 1
 
        print("Prueba 2: datos no vacíos (nombre y descripción)")
        print("  Dato:", solicitud["nombre"], "|", solicitud["descripcion"])
        if errores > 0:
            print("  Intentos con datos incorrectos:", errores)
        if nombre_ok == True and descripcion_ok == True and errores == 0:
            print("  Resultado: Sin problemas en los datos")
            aprobadas = aprobadas + 1
        else:
            print("  Resultado: Hay problemas en los datos")
 
        # Prueba 3: tipo de consulta válido
        tipo_ok = validar_tipo_consulta(solicitud["tipo"])
        errores = solicitud["errores_tipo"]
        total = total + 1
 
        print("Prueba 3: tipo de consulta válido")
        print("  Dato:", solicitud["tipo"])
        if errores > 0:
            print("  Intentos con datos incorrectos:", errores)
        if tipo_ok == True and errores == 0:
            print("  Resultado: Sin problemas en los datos")
            aprobadas = aprobadas + 1
        else:
            print("  Resultado: Hay problemas en los datos")
 
        # Prueba 4: prioridad (alta o baja según el tipo de consulta)
        tipo = solicitud["tipo"]
        if (tipo == "matrícula" or tipo == "matricula"
                or tipo == "pagos" or tipo == "plataforma"):
            esperada = "Alta"
        else:
            esperada = "Baja"
        obtenida = solicitud["prioridad"]
        total = total + 1
 
        print("Prueba 4: prioridad", esperada.lower())
        print("  Dato: tipo =", tipo)
        print("  Prioridad asignada:", obtenida)
        if obtenida == esperada:
            print("  Resultado: Sin problemas en los datos")
            aprobadas = aprobadas + 1
        else:
            print("  Resultado: Hay problemas en los datos")
 
    print("\n===================================")
    print("Estudiantes probados:", len(solicitudes))
    print("Pruebas sin problemas:", aprobadas, "de", total)
    print("===================================")
 
 
# PROGRAMA PRINCIPAL
def main():
 
    # Variable utilizada en el programa principal
    solicitudes = []
 
    print("===================================")
    print("  SISTEMA DE SOPORTE ACADÉMICO")
    print("===================================")
 
    while True:
 
        mostrar_menu()
 
        opcion = input("Seleccione una opción: ")
 
        if opcion == "1":
 
            solicitud = registrar_solicitud()
 
            # Se agrega la solicitud a la lista
            solicitudes.append(solicitud)
 
            print("\nSolicitud registrada correctamente.")
            mostrar_resumen(solicitud)
 
        elif opcion == "2":
 
            mostrar_solicitudes(solicitudes)
 
        elif opcion == "3":
 
            ejecutar_pruebas(solicitudes)
 
        elif opcion == "4":
 
            print("\nPrograma finalizado.")
            print("Total de solicitudes registradas:", len(solicitudes))
            break
 
        else:
 
            print("\nError: opción no válida.")
            print("Seleccione 1, 2, 3 o 4.")
 
 
# EJECUTAR EL PROGRAMA
if __name__ == "__main__":
    main() 