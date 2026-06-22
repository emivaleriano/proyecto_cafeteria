from backend.repositories.reservas_repository import (
    obtener_usuario_por_email,
    crear_usuario,
    crear_reserva,
    obtener_franja_por_dia,
    obtener_personas_reservadas,
    obtener_reserva,
    cancelar_reserva,
    obtener_todas_reservas,
    actualizar_estado_reserva,
    obtener_reserva_por_token,
    actualizar_no_completadas
)
from backend.repositories.inicio_repository import get_capacidad_maxima
from backend.repositories.servicios_repository import obtener_servicios
from backend.utils.validadores import (
    validar_id,
    validar_texto,
    validar_email,
    validar_entero_positivo
)
from backend.utils.formatos import formatear_reserva
from datetime import datetime
import uuid
import json

from backend.utils.email import enviar_confirmacion_reserva

def crear_nueva_reserva(data):

    nombre = validar_texto(data.get("nombre"), "nombre")
    email = validar_email(data.get("email"))
    telefono = validar_texto(data.get("telefono"), "telefono")

    cantidad_personas = validar_entero_positivo(
        data.get("cantidad_personas"),
        "cantidad_personas"
    )

    fecha_hora = data.get("fecha_hora")
    try:
        fecha_obj = datetime.fromisoformat(fecha_hora)
    except (TypeError, ValueError):
        raise ValueError("La fecha y hora ingresadas no son válidas.")

    if fecha_obj < datetime.now():
        raise ValueError("No se puede reservar para una fecha pasada.")


    dia_semana = fecha_obj.isoweekday() % 7 # Domingo = 0, Lunes = 1

    franja = obtener_franja_por_dia(dia_semana)
    capacidad_maxima = get_capacidad_maxima()

    if not franja:
        raise ValueError("No existe una fecha horaria para ese dia")


    personas_reservadas = obtener_personas_reservadas(fecha_obj)

    if (personas_reservadas + cantidad_personas > capacidad_maxima):
        raise ValueError("No hay disponibilidad para esa cantidad de personas ")


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

    servicios_json = json.dumps(data.get("servicios", []))

    id_reserva = crear_reserva(
        id_usuario,
        fecha_hora,
        cantidad_personas,
        servicios_json,
        data.get("observaciones"),
        "Pendiente",
        qr
    )

# Envía email de confirmación con el QR
    enviar_confirmacion_reserva(
        email_destino=email,
        nombre=nombre,
        reserva={
            "id_reserva": id_reserva,
            "fecha_hora": fecha_hora,
            "cantidad_personas": cantidad_personas,
            "qr": qr,
        }
    )

    return {
        "id_reserva": id_reserva,
        "qr": qr
    }



def data_obtener_reserva(id_reserva):

    id_reserva = validar_id(id_reserva)
    reserva = obtener_reserva(id_reserva)

    todos = obtener_servicios() #obtiene todos los servicios para no hacer una consulta
    reserva["servicios"] = [
        s["nombre"] for s in todos
        if str(s["id_servicio"]) in [str(id) for id in reserva["servicios"]] #si el id coincide con los servicios de la reserva
    ]

    print(reserva)
    return reserva


def data_cancelar_reserva(id_reserva):

    id_reserva = validar_id(id_reserva)

    return cancelar_reserva(id_reserva)



def data_obtener_todas_reservas(pagina, max, estados, orden):
    return obtener_todas_reservas(pagina, max, estados, orden)

def data_actualizar_estado_reserva(id_reserva, estado):
    id_reserva = validar_id(id_reserva)
    ESTADOS_VALIDOS = {"Pendiente", "Confirmada", "Cancelada", "Completada", "No Completada"}
    if estado not in ESTADOS_VALIDOS:
        return {"error": f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"}
    return actualizar_estado_reserva(id_reserva, estado)

def data_check_in(token):
    reserva = obtener_reserva_por_token(token)
    if not reserva:
        return {"error": "Reserva no encontrada"}
    if reserva["estado"] == "Cancelada":
        return {"error": "La reserva fue cancelada"}
    if reserva["estado"] == "Completada":
        return {"error": "La reserva ya fue completada"}

    hoy = datetime.now().date()
    fecha_reserva = reserva["fecha_hora"].date()
    if fecha_reserva != hoy:
        return {"error": "El QR solo es válido el día de la reserva"}

    todos = obtener_servicios() #obtiene todos los servicios para no hacer una consulta
    ids = json.loads(reserva["servicios"] or "[]")
    reserva["servicios"] = [
        s["nombre"] for s in todos
        if str(s["id_servicio"]) in [str(id) for id in ids]
    ]
    return formatear_reserva(reserva)

def data_actualizar_reservas_vencidas():
    return actualizar_no_completadas()
