from flask import Blueprint, render_template, request, redirect, url_for
from frontend.services.publico_service import (
    get_inicio,
    get_menu,
    get_reviews,
    post_review,
    get_datos_reserva,
    post_reserva,
    get_reserva,
    post_cancelar_reserva,
)

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


@publico_bp.route("/reviews/crear", methods=["GET", "POST"])
def crear_review():
    if request.method == "GET":
        return render_template("crear_review.html", datos={}, error=None)

    id_reserva = request.form.get("id_reserva", "").strip()
    estrellas  = request.form.get("estrellas")
    comentario = request.form.get("comentario", "").strip()

    datos, error = post_review(id_reserva, estrellas, comentario)

    if error:
        return render_template("crear_review.html", datos={}, error=error)

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

    return render_template("confirmacion.html", reserva=reserva, datos=datos)


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
    return redirect(url_for("publico.inicio"))