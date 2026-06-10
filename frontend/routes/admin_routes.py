from flask import Blueprint, render_template, request, redirect, url_for, session
from frontend.services.admin_service import (
    login_admin,
    service_actualizar_reserva,
    service_cambiar_estado_servicio,
    service_crear_plato,
    service_crear_servicio,
    service_editar_plato,
    service_editar_servicio,
    service_eliminar_servicio,
    service_eliminar_plato,
    service_obtener_reserva,
    obtener_dashboard,
    service_cambiar_contrasenia
    )


admin_front_bp = Blueprint("admin", __name__, template_folder="../templates")


def requiere_sesion():
    if not session.get("admin_token"):
        return redirect(url_for("admin.login"))


@admin_front_bp.route("/login", methods=["GET", "POST"])
def login():
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



@admin_front_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_front_bp.route("/nueva_clave", methods=["GET", "POST"])
def cambiar_contrasenia():
    sesion = requiere_sesion()
    if sesion:
        return sesion

    if request.method == "POST":
        contra_actual    = request.form.get("contra_actual")
        nueva_contra     = request.form.get("nueva_contra")
        confirmar_contra = request.form.get("confirmar_contra")

        datos, error = service_cambiar_contrasenia(
            contra_actual, nueva_contra, confirmar_contra,
            session["admin_token"]
        )

        if error:
            return render_template("admin/cambiar_contrasenia.html", error=error) #si hay un error renderiza la misma con el error

        return redirect(url_for("admin.dashboard")) # si sale bien vuelve al dash

    return render_template("admin/cambiar_contrasenia.html")# get

@admin_front_bp.route("/dashboard")
def dashboard():
    if not session.get("admin_token"):
        return redirect(url_for("admin.login"))

    token = session.get("admin_token")
    datos, error = obtener_dashboard(token)

    print("ERROR:", error)
    print("DATOS:", datos)

    if error:
        datos = {"stats": {}, "reservas": [], "platos": [], "servicios": []}

    return render_template("admin/dashboard.html",
        stats = datos.get("stats", {}),
        reservas = datos.get("reservas", []),
        platos = datos.get("platos", []),
        servicios = datos.get("servicios", [])
    )

# ------- Platos

@admin_front_bp.route("/platos/nuevo", methods=["GET", "POST"])
def crear_plato():
    sesion = requiere_sesion()
    if sesion:
        return sesion

    if request.method == "GET":
        return render_template("admin/plato_form.html")
    datos = {
        "nombre":      request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "precio":      request.form.get("precio"),
        "categoria":   request.form.get("categoria"),
        "imagen":      request.form.get("imagen"),
        "tags":        [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()],
    }
    service_crear_plato(datos, session["admin_token"])
    return redirect(url_for("admin.dashboard"))


@admin_front_bp.route("/platos/<int:id>/editar", methods=["GET", "POST"])
def editar_plato(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    if request.method == "GET":
        return render_template("admin/plato_form.html")
    datos = {
        "nombre":      request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "precio":      request.form.get("precio"),
        "categoria":   request.form.get("categoria"),
        "imagen":      request.form.get("imagen"),
        "tags":        [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()],
    }
    service_editar_plato(id, datos, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/platos/<int:id>/eliminar", methods=["POST"])
def eliminar_plato(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    service_eliminar_plato(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

# ------------- Servicios

@admin_front_bp.route("/servicios/nuevo", methods=["GET", "POST"])
def crear_servicio():
    sesion = requiere_sesion()
    if sesion:
        return sesion

    if request.method == "GET":
        return render_template("admin/servicio_form.html")
    datos = {
        "nombre":      request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "activo":      True,
    }
    service_crear_servicio(datos, session["admin_token"])
    return redirect(url_for("admin.dashboard"))


@admin_front_bp.route("/servicios/<int:id>/editar", methods=["GET", "POST"])
def editar_servicio(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    if request.method == "GET":
        return render_template("admin/servicio_form.html")
    datos = {
        "nombre":      request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "activo":      request.form.get("activo") == "on",
    }
    service_editar_servicio(id, datos, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/servicios/<int:id>/eliminar", methods=["POST"])
def eliminar_servicio(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    service_eliminar_servicio(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/servicios/<int:id>/estado")
def cambiar_estado_servicio(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    service_cambiar_estado_servicio(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))



# ----------- Reservas
@admin_front_bp.route("/reservas/<int:id>", methods=["GET"])
def reserva_detalle(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    reserva, error = service_obtener_reserva(id, session["admin_token"])
    print("RESERVA:", reserva)
    return render_template("admin/reserva_detalle.html", reserva=reserva)

@admin_front_bp.route("/reservas/<int:id>/actualizar", methods=["POST"])
def actualizar_estado_reserva(id):
    sesion = requiere_sesion()
    if sesion:
        return sesion

    estado = request.form.get("estado")
    service_actualizar_reserva(id, estado, session["admin_token"])
    return redirect(url_for("admin.dashboard"))
