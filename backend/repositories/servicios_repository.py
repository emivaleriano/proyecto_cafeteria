from backend.db import obtener_conexion

def obtener_servicios():
    """Obtiene todos los servicios"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_servicio, nombre, descripcion, activo from servicios"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obtener_servicios_activos():
    """Obtiene todos los servicios activos"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_servicio, nombre, descripcion from servicios where activo = 1"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obtener_servicio_bd(id):
    """Devuelve un servicio especifico a partir de su id"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_servicio, nombre, descripcion, activo FROM servicios WHERE id_servicio = %s", (id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def obtener_servicio_por_nombre(nombre):
    """Obtiene los servicios con un nombre especifico"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_servicio, nombre, descripcion, activo from servicios where nombre = %s", (nombre,)
            )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def agregar_servicio_bd(nombre, descripcion, activo):
    """agrega un servicio nuevo en la base de datos"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO servicios (nombre, descripcion, activo) values (%s, %s, %s)",(nombre, descripcion, activo)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def eliminar_servicio_bd(id):
    """ Elimina un servicio a partir de su id"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM servicios WHERE id_servicio = %s", (id,)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def modificar_servicio_bd(id, nombre, descripcion, activo):
    """Modifica todos los datos de un servicio"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE servicios SET nombre = %s, descripcion = %s, activo=%s WHERE id_servicio = %s",(nombre, descripcion, activo, id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def activar_desactivar_servicio_bd(id, activo):
    """Cambia el estado del un servicio especifico"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE servicios SET activo = %s WHERE id_servicio = %s", (activo, id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
