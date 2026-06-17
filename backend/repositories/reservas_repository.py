from backend.db import obtener_conexion
import json

DIAS = {
    "Monday": "Lun", "Tuesday": "Mar", "Wednesday": "Mie",
    "Thursday": "Jue", "Friday": "Vie", "Saturday": "Sab", "Sunday": "Dom"
}
def formatear_reserva(reserva):
    if reserva:
        reserva["servicios"] = json.loads(reserva["servicios"] or "[]")
        if reserva["fecha_hora"]:
            fecha = reserva["fecha_hora"]
            reserva["fecha_hora"] = f"{DIAS[fecha.strftime('%A')]} {fecha.strftime('%d/%m/%Y %H:%M')}"
    return reserva

def obtener_usuario_por_email(email):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE email = %s
            """,
            (email,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def crear_usuario(nombre, email, telefono):

    conn = obtener_conexion()
    cursor = conn.cursor()

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


def obtener_franja_por_dia(dia_semana):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:

        cursor.execute(
            """
            SELECT *
            FROM franjas_horarias
            WHERE dia_semana = %s
            """,
            (dia_semana,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def obtener_personas_reservadas(fecha):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT COALESCE(SUM(cantidad_personas), 0) AS total
            FROM reservas
            WHERE fecha_hora = %s
            AND estado <> 'Cancelada'
            """,
            (fecha,)
        )

        resultado = cursor.fetchone()
        return resultado["total"]

    finally:
        cursor.close()
        conn.close()


def crear_reserva(
    id_usuario,
    fecha_hora,
    cantidad_personas,
    servicios,
    observaciones,
    estado,
    qr
):

    conn = obtener_conexion()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO reservas
            (
                id_usuario,
                fecha_hora,
                cantidad_personas,
                servicios,
                observaciones,
                estado,
                qr
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                id_usuario,
                fecha_hora,
                cantidad_personas,
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


def obtener_reserva(id_reserva):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT r.*, u.nombre, u.email, u.telefono
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            WHERE r.id_reserva = %s
            """,
            (id_reserva,)
        )

        return formatear_reserva(cursor.fetchone())

    finally:
        cursor.close()
        conn.close()


def cancelar_reserva(id_reserva):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT *
            FROM reservas
            WHERE id_reserva = %s
            """,
            (id_reserva,)
        )

        reserva = cursor.fetchone()

        if not reserva:
            return {"error": "Reserva no encontrada"}

        if reserva["estado"] == "Cancelada":
            return {"error": "La reserva ya fue cancelada"}

        cursor.execute(
            """
            UPDATE reservas
            SET estado = 'Cancelada'
            WHERE id_reserva = %s
            """,
            (id_reserva,)
        )

        conn.commit()

        return {
            "mensaje": "Reserva cancelada correctamente"
        }

    finally:
        cursor.close()
        conn.close()

def obtener_todas_reservas():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.*, u.nombre, u.email, u.telefono
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora DESC
        """)
        return [formatear_reserva(r) for r in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

def actualizar_estado_reserva(id_reserva, estado):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,)
        )
        reserva = cursor.fetchone()
        if not reserva:
            return {"error": "Reserva no encontrada"}
        cursor.execute(
            "UPDATE reservas SET estado = %s WHERE id_reserva = %s",
            (estado, id_reserva)
        )
        conn.commit()
        return {"mensaje": "Estado actualizado correctamente"}
    finally:
        cursor.close()
        conn.close()

def obtener_reserva_por_token(token):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.*, u.nombre, u.email, u.telefono
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            WHERE r.qr = %s
        """, (token,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
