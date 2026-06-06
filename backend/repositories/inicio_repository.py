from backend.db import obtener_conexion


def get_franjas_horarias():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_franja, dia_semana, hora_apertura, hora_cierre, capacidad_maxima
        FROM franjas_horarias
        ORDER BY dia_semana ASC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def get_resenas_publicas():
    """Devuelve una lista de reseñas publicadas a nombre del usuario"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.id_resena,
            u.nombre  AS nombre_usuario,
            r.estrellas,
            r.comentario,
            r.fecha
        FROM resenas r
        JOIN reservas  res ON r.id_reserva   = res.id_reserva
        JOIN usuarios  u   ON res.id_usuario  = u.id_usuario
        ORDER BY r.fecha DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def get_reserva_para_resena(id_reserva):
    """Devuelve el estado de una reserva para validar si puede escribir una reseña"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_reserva, estado
        FROM reservas
        WHERE id_reserva = %s
    """, (id_reserva,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado


def get_resena_por_reserva(id_reserva):
    """Verifica si ya existe una reseña para una reserva dada"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_resena
        FROM resenas
        WHERE id_reserva = %s
    """, (id_reserva,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado


def insertar_resena(id_reserva, estrellas, comentario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO resenas (id_reserva, estrellas, comentario)
        VALUES (%s, %s, %s)
    """, (id_reserva, estrellas, comentario))
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return nuevo_id