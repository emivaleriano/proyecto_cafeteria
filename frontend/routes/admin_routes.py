from flask import Blueprint, render_template, request, redirect, url_for, session
from frontend.services.admin_service import login_admin, obtener_dashboard

admin_front_bp = Blueprint("admin", __name__, template_folder="../templates")


@admin_front_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_token"): #si ya tiene sesion no muestra el login
        return redirect(url_for("admin.dashboard"))

    if request.method == "GET":
        return render_template("admin/login.html", datos={})

    # post
    usuario     = request.form.get("usuario", "").strip()
    contrasenia = request.form.get("contrasenia", "")

    datos, error = login_admin(usuario, contrasenia)

    if error:
        return render_template("admin/login.html", error=error), 401

    session["admin_token"] = datos.get("access_token")
    session.permanent = True

    return redirect(url_for("admin.dashboard"))


@admin_front_bp.route("/dashboard")
def dashboard():
    if not session.get("admin_token"):
        return redirect(url_for("admin.login"))

    token = session.get("admin_token")
    datos, error = obtener_dashboard(token)

    if error:
        datos = {"stats": {}, "reservas": [], "platos": [], "servicios": []}

    return render_template("admin/dashboard.html",
        stats = datos.get("stats", {}),
        reservas = datos.get("reservas", []),
        platos = datos.get("platos", []),
        servicios = datos.get("servicios", [])
    )


@admin_front_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))
