from backend.db import obtener_conexion
import uuid


def validar_disponibilidad(id_franja_horaria, cantidad_personas):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT capacidad_max, capacidad_ocupada
            FROM franjas_horarias
            WHERE id = %s AND disponible = true
            """,
            (id_franja_horaria,)
        )

        franja = cursor.fetchone()

        if not franja:
            return False

        disponible = (
            franja["capacidad_ocupada"] + cantidad_personas
            <= franja["capacidad_max"]
        )

        return disponible

    finally:
        cursor.close()
        conn.close()

def obtener_usuario_por_email(email):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()
        
def crear_usuario(nombre, email, telefono):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, email, telefono)

            VALUES (%s, %s, %s)
            """,
            (nombre, email, telefono)
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()
        
        
def crear_reserva(
    id_usuario,
    id_franja,
    fecha_hora,
    cantidad_personas,
    alergias,
    servicios,
    observaciones,
    estado,
    qr
):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            INSERT INTO reservas
            (
                id_usuario,
                id_franja,
                fecha_hora,
                cantidad_personas,
                alergias,
                servicios,
                observaciones,
                estado,
                qr
            )

            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                id_usuario,
                id_franja,
                fecha_hora,
                cantidad_personas,
                alergias,
                servicios,
                observaciones,
                estado,
                qr
            )
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()
        
def obtener_franja(id_franja):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT * FROM franjas_horarias
            WHERE id_franja = %s
            """,
            (id_franja,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()
        
def actualizar_capacidad_ocupada(id_franja, nueva_capacidad):

    conn = obtener_conexion()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE franjas_horarias
            SET capacidad_ocupada = %s
            WHERE id_franja = %s
            """,
            (nueva_capacidad, id_franja)
        )

        conn.commit()

    finally:
        cursor.close()
        conn.close()

def obtener_reserva(id_reserva):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT *
            FROM reservas
            WHERE id = %s
            """,
            (id_reserva,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def cancelar_reserva(id_reserva):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT cantidad_personas, id_franja_horaria, estado
            FROM reservas
            WHERE id = %s
            """,
            (id_reserva,)
        )

        reserva = cursor.fetchone()

        if not reserva:
            return {
                "error": "Reserva no encontrada"
            }

        if reserva["estado"] == "cancelada":
            return {
                "error": "La reserva ya fue cancelada"
            }

        cursor.execute(
            """
            UPDATE reservas
            SET estado = 'cancelada'
            WHERE id = %s
            """,
            (id_reserva,)
        )

        cursor.execute(
            """
            UPDATE franjas_horarias
            SET capacidad_ocupada = capacidad_ocupada - %s
            WHERE id = %s
            """,
            (
                reserva["cantidad_personas"],
                reserva["id_franja_horaria"]
            )
        )

        conn.commit()

        return {
            "mensaje": "Reserva cancelada correctamente"
        }

    finally:
        cursor.close()
        conn.close()