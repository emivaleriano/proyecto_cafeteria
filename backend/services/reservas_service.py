from backend.repositories.reservas_repository import (
    obtener_usuario_por_email,
    crear_usuario,
    crear_reserva,
    obtener_franja_por_dia,
    obtener_personas_reservadas,
    obtener_reserva,
    cancelar_reserva,
    obtener_todas_reservas,
    actualizar_estado_reserva
)

from backend.utils.validadores import (
    validar_id,
    validar_texto,
    validar_email,
    validar_entero_positivo
)

from datetime import datetime
import uuid
import json

def crear_nueva_reserva(data):

    nombre = validar_texto(data.get("nombre"), "nombre")
    email = validar_email(data.get("email"))
    telefono = validar_texto(data.get("telefono"), "telefono")

    cantidad_personas = validar_entero_positivo(
        data.get("cantidad_personas"),
        "cantidad_personas"
    )

    fecha_hora = data.get("fecha_hora")

    fecha_obj = datetime.fromisoformat(fecha_hora)

    dia_semana = fecha_obj.weekday()

    franja = obtener_franja_por_dia(dia_semana)

    if not franja:
        return {
            "error": "No existe una franja horaria para ese día"
        }

    personas_reservadas = obtener_personas_reservadas(
        fecha_obj.date()
    )

    if (
        personas_reservadas + cantidad_personas
        > franja["capacidad_maxima"]
    ):
        return {
            "error": "No hay disponibilidad para esa fecha"
        }

    usuario = obtener_usuario_por_email(email)

    if not usuario:

        id_usuario = crear_usuario(
            nombre,
            email,
            telefono
        )

    else:

        id_usuario = usuario["id_usuario"]

    qr = str(uuid.uuid4())
    alergias_json  = json.dumps(data.get("alergias", []))
    servicios_json = json.dumps(data.get("servicios", []))


    id_reserva = crear_reserva(
        id_usuario,
        fecha_hora,
        cantidad_personas,
        alergias_json,
        servicios_json,
        data.get("observaciones"),
        "Pendiente",
        qr
    )

    return {
        "id_reserva": id_reserva,
        "qr": qr
    }




def data_obtener_reserva(id_reserva):

    id_reserva = validar_id(id_reserva)

    return obtener_reserva(id_reserva)


def data_cancelar_reserva(id_reserva):

    id_reserva = validar_id(id_reserva)

    return cancelar_reserva(id_reserva)

def data_obtener_todas_reservas():
    return obtener_todas_reservas()

def data_actualizar_estado_reserva(id_reserva, estado):
    id_reserva = validar_id(id_reserva)
    ESTADOS_VALIDOS = {"Pendiente", "Confirmada", "Cancelada", "Completada"}
    if estado not in ESTADOS_VALIDOS:
        return {"error": f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"}
    return actualizar_estado_reserva(id_reserva, estado)
