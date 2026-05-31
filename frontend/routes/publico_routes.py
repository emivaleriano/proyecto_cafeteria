from flask import Blueprint, render_template, request, redirect, url_for
from frontend.services.publico_service import (
    get_inicio,
    get_menu,
    get_reviews,
    post_review,
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
