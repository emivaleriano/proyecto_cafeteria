from backend.repositories.reservas_repository import (
    obtener_usuario_por_email,
    crear_usuario,
    crear_reserva,
    obtener_franja,
    actualizar_capacidad_ocupada
)

import uuid

def crear_nueva_reserva(data):

    usuario = obtener_usuario_por_email(data["email"])

    if not usuario:

        id_usuario = crear_usuario(
            data["nombre"],
            data["email"],
            data["telefono"]
        )

    else:
        id_usuario = usuario["id_usuario"]

    franja = obtener_franja(data["id_franja"])

    if not franja:
        raise ValueError("La franja horaria no existe")

    ocupada = franja["capacidad_ocupada"]
    maxima = franja["capacidad_maxima"]

    if ocupada + data["cantidad_personas"] > maxima:
        raise ValueError("No hay disponibilidad")

    nueva_capacidad = ocupada + data["cantidad_personas"]

    actualizar_capacidad_ocupada(
        data["id_franja"],
        nueva_capacidad
    )

    qr = str(uuid.uuid4())

    id_reserva = crear_reserva(
        id_usuario,
        data["id_franja"],
        data["fecha_hora"],
        data["cantidad_personas"],
        data.get("alergias"),
        data.get("servicios"),
        data.get("observaciones"),
        "Pendiente",
        qr
    )

    return {
        "id_reserva": id_reserva,
        "qr": qr
    }
    

def data_obtener_reserva(id_reserva):

    reserva = obtener_reserva(id_reserva)

    if not reserva:
        raise LookupError("No existe una reserva con ese ID")

    return reserva


def data_cancelar_reserva(id_reserva):

    reserva = obtener_reserva(id_reserva)

    if not reserva:
        raise LookupError("No existe una reserva con ese ID")

    return cancelar_reserva(id_reserva)