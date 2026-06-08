from backend .db import obtener_conexion

def obtener_valor_unico(consulta, parametros=()):
    """
    Ejecuta una consulta que devuelve un solo valor y lo retorna. Si no hay resultados, devuelve 0.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        resultado = cursor.fetchone()
        if resultado is None:
            return 0
        else:
            return resultado[0]
    finally:
        cursor.close()
        conexion.close()


def contar_total_reservas():
    """
    Devuelve el total de reservas
    """
    consulta = "SELECT COUNT(*) FROM reservas"
    return obtener_valor_unico(consulta)

def contar_reservas_hoy():
    """Devuelve la cantidad de reservas para el dia de hoy"""
    consulta = """
        SELECT COUNT(*) FROM reservas WHERE estado != 'Cancelada' AND DATE(fecha_hora) = CURDATE()
        """
    return obtener_valor_unico(consulta)

def contar_cancelaciones():
    """Devuelve la cantidad total de reservas canceladas.
    """
    consulta = """
        SELECT COUNT(*) FROM reservas WHERE estado = 'Cancelada'
        """
    return obtener_valor_unico(consulta)

def contar_total_resenas():
    """
    Devuelve la cantidad total de reseñas.
    """
    consulta = """
        SELECT COUNT(*) FROM resenas
        """
    return obtener_valor_unico(consulta)

def obtener_todas_reservas():
    """
    Devuelve todas las reservas con los datos:
    - id_reserva
    - nombre del cliente
    - fecha y hota
    - cantidad de personas
    - estado
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT
            reservas.id_reserva,
            usuarios.nombre,
            reservas.fecha_hora,
            reservas.cantidad_personas,
            reservas.estado
        FROM reservas
        JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
        ORDER BY reservas.fecha_hora DESC
        """)
        return cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()
