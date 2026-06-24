from datetime import datetime

from backend.db import obtener_conexion
from backend.utils.formatos import formatear_reserva

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

        return cursor.fetchall()

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


def obtener_todas_reservas(pagina=1, max=10, estados=None, orden="asc"):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        offset = (pagina - 1) * max
        filtros = []
        valores = []

        if estados:
            placeholders = ", ".join(["%s"] * len(estados)) # [%s, %s, %s]
            filtros.append(f"r.estado IN ({placeholders})")
            valores.extend(estados)

        where = f"WHERE {' AND '.join(filtros)}" if filtros else "" # and r.estado in [...]
        direccion = "ASC" if orden == "asc" else "DESC"

        cursor.execute(f"""
            SELECT r.*, u.nombre, u.email, u.telefono
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            {where}
            ORDER BY r.fecha_hora {direccion}
            LIMIT %s OFFSET %s
        """, valores + [max, offset])
        reservas = [formatear_reserva(r) for r in cursor.fetchall()]

        cursor.execute(f"""
            SELECT COUNT(*) as total
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            {where}
        """, valores)
        total = cursor.fetchone()["total"]

        return {
            "reservas": reservas,
            "total": total,
            "pagina": pagina,
            "max": max,
            "total_paginas": -(-total // max) # menos para el redondeo
        }
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

def actualizar_no_completadas():
    """
    Actualiza a 'No Completada' todas las reservas que ya pasaron y que
    no fueron canceladas o completadas.

    """
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            UPDATE reservas
            SET estado = 'No Completada'
            WHERE fecha_hora < %s
            AND estado NOT IN ('Completada', 'Cancelada', 'No Completada')
        """, (datetime.now(),))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
