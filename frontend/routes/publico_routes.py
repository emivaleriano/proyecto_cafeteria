from flask import Blueprint, render_template, request, redirect, url_for
import qrcode
import io
import base64
from frontend.services.publico_service import (
    get_inicio,
    get_menu,
    get_reviews,
    post_review,
    get_datos_reserva,
    post_reserva,
    get_reserva,
    post_cancelar_reserva,
    get_check_in
)
from frontend.services.admin_service import service_actualizar_reserva
from frontend.utils.tokens import verificar_token_resena
import os
publico_bp = Blueprint("publico", __name__)


@publico_bp.route("/")
@publico_bp.route("/inicio")
def inicio():
    datos, error = get_inicio()
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("index.html", datos=datos)


@publico_bp.route("/menu")
def menu():
    productos, error = get_menu()
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("menu.html", productos=productos)


@publico_bp.route("/reviews")
def reviews():
    lista, error = get_reviews()
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("reviews.html", reviews=lista)


@publico_bp.route("/reviews/<token>", methods=["GET", "POST"])
def crear_review(token):
    id_reserva, error = verificar_token_resena(token)
    if error:
        return render_template("error.html", mensaje=error), 403

    if request.method == "GET":
        return render_template("crear_review.html", datos={}, error=None, token=token)

    estrellas  = request.form.get("estrellas")
    comentario = request.form.get("comentario", "").strip()

    if not estrellas:
        return render_template("crear_review.html", datos={}, error="Seleccioná una valoración.", token=token)


    datos, error = post_review(id_reserva, int(estrellas), comentario)

    if error:
        return render_template("crear_review.html", datos={}, error=error, token=token)

    return redirect(url_for("publico.reviews"))



@publico_bp.route("/reservar", methods=["GET", "POST"])
def crear_reserva():
    if request.method == "GET":
        datos, error = get_datos_reserva()
        if error:
            return render_template("error.html", mensaje=error), 503
        return render_template("crear_reserva.html", **datos) #pasa el diccionario a argumentos con nombre

    datos, error = post_reserva(request.form)
    if error:
        form_datos, _ = get_datos_reserva()
        return render_template("crear_reserva.html", **(form_datos or {}), error=error)

    return redirect(url_for(
        "publico.confirmacion_reserva",
        id_reserva=datos.get("id_reserva"),
        qr=datos.get("qr"),
    ))


@publico_bp.route("/reservar/confirmacion/<int:id_reserva>")
def confirmacion_reserva(id_reserva):
    reserva, error = get_reserva(id_reserva)
    if error:
        return render_template("error.html", mensaje=error), 503

    datos, error = get_inicio()
    if error:
        return render_template("error.html", mensaje=error), 503

    # Genera la imagen QR en base64 para mostrar en la página
    base_url = os.getenv("FRONTEND_BASE_URL")
    url_qr = f"{base_url}/check-in/{reserva['qr']}"

    img = qrcode.make(url_qr)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_b64 = base64.b64encode(buffer.read()).decode("utf-8")
    qr_data_url = f"data:image/png;base64,{qr_b64}"

    return render_template("confirmacion.html", reserva=reserva, datos=datos, qr_img=qr_data_url)


@publico_bp.route("/reservar/<int:id_reserva>/cancelar", methods=["GET"])
def confirmar_cancelacion(id_reserva):
    """Página de confirmación antes de cancelar (link del email llega acá)."""
    reserva, error = get_reserva(id_reserva)
    if error:
        return render_template("cancelar_reserva.html", reserva=None, error=error)
    return render_template("cancelar_reserva.html", reserva=reserva, error=None)


@publico_bp.route("/reservar/<int:id_reserva>/cancelar", methods=["POST"])
def cancelar_reserva(id_reserva):
    _, error = post_cancelar_reserva(id_reserva)
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("reserva_cancelada.html")


@publico_bp.route("/check-in/<string:token>", methods=["GET"])
def check_in(token):
    reserva, error = get_check_in(token)
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("check_in.html", reserva=reserva)


@publico_bp.route("/check-in/<string:token>", methods=["POST"])
def confirmar_check_in(token):
    reserva, error = get_check_in(token)
    if error:
        return render_template("error.html", mensaje=error), 503
    _, error = service_actualizar_reserva(reserva["id_reserva"], "Completada")
    if error:
        return render_template("error.html", mensaje=error), 503
    return render_template("check_in.html", reserva=reserva, completada=True)

"""
Para generar el mail:
from utils.tokens import generar_token_resena

token = generar_token_resena(id_reserva)
link  = url_for("publico.crear_review", token=token, _external=True) # el external true es para que genere la URL completa
# usas link en el cuerpo del mail
# usar siempre id_reserva, no id solo
"""
