import json
DIAS = {
    "Monday": "Lun", "Tuesday": "Mar", "Wednesday": "Mie",
    "Thursday": "Jue", "Friday": "Vie", "Saturday": "Sab", "Sunday": "Dom"
}

def formatear_reserva(reserva):
    if reserva:
        if isinstance(reserva["servicios"], str):
            reserva["servicios"] = json.loads(reserva["servicios"] or "[]")
        if reserva["fecha_hora"]:
            fecha = reserva["fecha_hora"]
            reserva["fecha_hora"] = f"{DIAS[fecha.strftime('%A')]} {fecha.strftime('%d/%m/%Y %H:%M')}"
    return reserva
