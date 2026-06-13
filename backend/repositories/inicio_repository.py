from backend.db import obtener_conexion


def get_franjas_horarias():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_franja, dia_semana, hora_apertura, hora_cierre
        FROM franjas_horarias
        ORDER BY dia_semana, hora_apertura ASC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def reemplazar_franjas_horarias(franjas):
    """Borra las franjas existentes y las reemplaza por nuevas (en caso de que se agregue otra franja dentro de un dia)"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM franjas_horarias")
        for f in franjas:
            cursor.execute(
                "INSERT INTO franjas_horarias (dia_semana, hora_apertura, hora_cierre) values (%s, %s, %s)",
                (f["dia_semana"], f["hora_apertura"], f["hora_cierre"])
            )
            conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()

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

def get_info_local():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT nombre, direccion, telefono, email
        FROM info_local
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado

def get_capacidad_maxima():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT capacidad_maxima
        FROM info_local
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado

def update_info_local(nombre, direccion, telefono, email, capacidad):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
                   update info_local set nombre=%s, direccion=%s, telefono=%s,email=%s, capacidad_maxima=%s where id = 1""",
                   (nombre, direccion, telefono, email, capacidad))
    conexion.commit()
    cursor.close()
    conexion.close()
