from backend.repositories.inicio_repository import get_franjas_horarias, get_resenas_publicas, get_reserva_para_resena, get_resena_por_reserva, insertar_resena
from backend.services.servicios_service import obtener_servicios_activos
from backend.utils.validadores import validar_estrellas, validar_comentario

DIAS = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo",
}


def _timedelta_a_str(td):
    """Convierte un objeto timedelta a una cadena en formato 'HH:MM'"""
    if hasattr(td, "seconds"):
        total = int(td.total_seconds())
        h, m = divmod(total // 60, 60)
        return f"{h:02d}:{m:02d}"
    return str(td)[:5]


def obtener_info_local():
    """Devuelve los datos generales del local junto con horarios y servicios activos"""
    franjas = get_franjas_horarias()
    servicios = obtener_servicios_activos()
    nombres_servicios = [s["nombre"] for s in servicios]

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

    return {
        "nombre":    "La Brasa — Cocina de Fuego",
        "direccion": "Av. Santa Fe 1234, Palermo, Buenos Aires",
        "telefono":  "+54 11 4987-6543",
        "email":     "hola@labrasa.com.ar",
        "servicios_disponibles": nombres_servicios,
        "horarios": horarios,
    }


def obtener_resenas():
    """Devuelve las reseñas públicas con la fecha formateada"""
    resenas = get_resenas_publicas()
    for r in resenas:
        if r.get("fecha"):
            r["fecha"] = r["fecha"].strftime("%Y-%m-%d %H:%M:%S")
    return resenas


def crear_resena(id_reserva, estrellas, comentario):
    """
    Valida y persiste una nueva reseña para una reserva completada.
    Lanza ValueError con un mensaje descriptivo ante cualquier problema de negocio.
    Retorna el id de la reseña creada.
    """
    validar_estrellas(estrellas)
    validar_comentario(comentario)

    reserva = get_reserva_para_resena(id_reserva)
    if not reserva:
        raise LookupError("La reserva no existe")

    if reserva["estado"] != "Completada":
        raise ValueError("Solo se pueden reseñar reservas con estado 'Completada'")

    if get_resena_por_reserva(id_reserva):
        raise ValueError("Ya existe una reseña para esta reserva")

    return insertar_resena(
        id_reserva=id_reserva,
        estrellas=estrellas,
        comentario=comentario.strip(),
    )