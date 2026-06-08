from backend.repositories.dashboard_repository import (
    contar_total_reservas,
    contar_reservas_hoy,
    contar_cancelaciones,
    contar_total_resenas,
    obtener_todas_reservas,
)

def obtener_stats():
    """
    Devuelve un diccionario con todas las estadisticas para el dashboard.
    """
    total_reservas = contar_total_reservas()
    reservas_hoy = contar_reservas_hoy()
    cancelaciones = contar_cancelaciones()
    total_resenas = contar_total_resenas()

    return {
        "total_reservas": total_reservas,
        "reservas_hoy": reservas_hoy,
        "cancelaciones": cancelaciones,
        "resenas": total_resenas,
    }

def obtener_reservas():
    """
    Devuele la lista de reservas para el dashboard.
    """
    return obtener_todas_reservas()
