from backend.repositories import inicio_repository
from flask import Blueprint, request
from backend.utils.respuestas import (
    HTTP_OK_CODE, HTTP_INTERNAL_ERROR_CODE,
    crear_respuesta_exito, crear_error
)
from backend.repositories.inicio_repository import (
    get_franjas_horarias,
    get_resenas_publicas,
    get_reserva_para_resena,
    get_resena_por_reserva,
    insertar_resena,
)
from backend.utils.validadores import validar_estrellas, validar_comentario

inicio_bp = Blueprint("inicio", __name__)

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
@inicio_bp.route("/inicio", methods=["GET"])
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
        '''Datos estaticos del local,'''
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
    
'''/reviews: Devuelve las reseñas publicadas'''
@inicio_bp.route("/reviews", methods=["GET"])
def get_reviews():
    try:
        resenas = get_resenas_publicas()

        for r in resenas:
            if r.get("fecha"):
                r["fecha"] = r["fecha"].strftime("%Y-%m-%d %H:%M:%S")
 
        return crear_respuesta_exito(
            datos=resenas,
            mensaje="Reseñas obtenidas correctamente",
            codigo=HTTP_OK_CODE,
        )
 
    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al obtener reseñas",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE
    
'''/reservas/<id_reserva>/review: Permite publicar una reseña para una reserva completada'''
@inicio_bp.route("/reservas/<int:id_reserva>/review", methods=["POST"])
def post_review(id_reserva):
    try:
        body = request.get_json(silent=True)
        if not body:
            return crear_error(400, "Body inválido", "Se esperaba JSON"), 400
        
        estrellas  = body.get("estrellas")
        comentario = body.get("comentario")
        '''Valida formato de los datos'''
        try:
            validar_estrellas(estrellas)
            validar_comentario(comentario)
        except ValueError as ve:
            return crear_error(400, "Datos inválidos", str(ve)), 400
        
        '''Verifica que la reserva exista'''
        reserva = get_reserva_para_resena(id_reserva)
        if not reserva:
            return crear_error(404, "No encontrada", "La reserva no existe"), 404
        
        '''Verifica que el estado de la reserva sea completada'''
        if reserva["estado"] != "Completada":
            return crear_error(
                400, "Estado inválido",
                "Solo se pueden reseñar reservas con estado 'Completada'"
            ), 400
        
        '''Verifica que no haya una reseña previa para esta reserva'''
        if get_resena_por_reserva(id_reserva):
            return crear_error(
                409, "Duplicado", "Ya existe una reseña para esta reserva"
            ), 409
        
        nuevo_id = insertar_resena(
            id_reserva=id_reserva,
            estrellas=estrellas,
            comentario=comentario.strip(),
        )
 
        return crear_respuesta_exito(
            datos={"id_resena": nuevo_id},
            mensaje="Reseña creada exitosamente",
            codigo=201,
        )
 
    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al crear la reseña",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE