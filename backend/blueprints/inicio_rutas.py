from backend.repositories import inicio
from flask import Blueprint, request
from backend.utils.respuestas import (
    HTTP_OK_CODE, HTTP_INTERNAL_ERROR_CODE,
    crear_respuesta_exito, crear_error
)
from backend.repositories.inicio import (
    get_franjas_horarias,
    get_resenas_publicas,
    get_reserva_para_resena,
    get_resena_por_reserva,
    insertar_resena,
)
from backend.utils.validadores import validar_estrellas, validar_comentario

def _timedelta_a_str(td):
    '''Convierte un objeto timedelta a una cadena en formato "HH:MM"'''
    if hasattr(td, "seconds"):
        total = int(td.total_seconds())
        h, m = divmod(total // 60, 60)
        return f"{h:02d}:{m:02d}"
    return str(td)[:5]
 
DIAS = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo",
}

'''/inicio: Devuelve la informacion general del local'''
@inicio.route("/inicio", methods=["GET"])
def get_inicio():
    try:
        franjas = get_franjas_horarias()
 
        horarios = [
            {
                "id_franja":        f["id_franja"],
                "dia":              DIAS.get(f["dia_semana"], f["dia_semana"]),
                "hora_apertura":    _timedelta_a_str(f["hora_apertura"]),
                "hora_cierre":      _timedelta_a_str(f["hora_cierre"]),
                "capacidad_maxima": f["capacidad_maxima"],
            }
            for f in franjas
        ]
        data = {
            "nombre":    "La Brasa — Cocina de Fuego",
            "direccion": "Av. Santa Fe 1234, Palermo, Buenos Aires",
            "telefono":  "+54 11 4987-6543",
            "email":     "hola@labrasa.com.ar",
            "servicios_disponibles": [
                "Acceso para personas con discapacidad",
                "Estacionamiento",
                "Opciones veganas",
                "Sin TACC",
            ],
            "horarios": horarios,
        }
 
        return crear_respuesta_exito(
            datos=data,
            mensaje="Información del local obtenida correctamente",
            codigo=HTTP_OK_CODE,
        )
 
    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al obtener información del local",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE
    
