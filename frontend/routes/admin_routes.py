from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
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
    service_cambiar_contrasenia,
    service_obtener_plato,
    service_obtener_servicio,
    cambiar_info_local,
    obtener_info_local,
    obtener_franjas_horarias,
    cambiar_franjas_horarias,
    service_obtener_reservas,
    service_actualizar_reservas_vencidas,
    service_cambiar_estado_plato
    )

import json
from frontend.utils.admin import requiere_sesion

admin_front_bp = Blueprint("admin", __name__, template_folder="../templates")


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
@requiere_sesion
def cambiar_contrasenia():

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

@admin_front_bp.route("/inicio/config", methods=["GET", "POST"])
@requiere_sesion
def config_local():
    if request.method =="GET":
        datos, error = obtener_info_local()
        if error:
            return render_template(url_for("admin.configuracion.html", error=error))
        return render_template("admin/configuracion.html", datos=datos)
    datos= {
        "nombre" : request.form.get("nombre"),
        "direccion" : request.form.get("direccion"),
        "telefono" : request.form.get("telefono"),
        "email" : request.form.get("email"),
        "capacidad" : request.form.get("capacidad"),
    }
    datos, error = cambiar_info_local(datos, session["admin_token"])

    return redirect(url_for("admin.dashboard"))


@admin_front_bp.route("/inicio/franjas", methods=["GET", "POST"])
@requiere_sesion
def franjas_horarias():
    if request.method == "GET":
        franjas, error = obtener_franjas_horarias()
        if error:
            return render_template("admin/franjas_horarias.html", error=error, franjas=[])
        return render_template("admin/franjas_horarias.html", franjas=franjas)

    franjas = json.loads(request.form.get("franjas_json", "[]"))
    datos, error = cambiar_franjas_horarias(franjas, session["admin_token"])

    if error:
        return render_template("admin/franjas_horarias.html", error=error, franjas=franjas)

    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/dashboard")
@requiere_sesion
def dashboard():
    token = session.get("admin_token")

    pagina = int(request.args.get("pagina", 1))
    orden = request.args.get("orden", "asc")
    estados = request.args.getlist("estado")

    datos, error = obtener_dashboard(token, pagina, orden, estados)
    reservas_data = datos.get("reservas", {})

    if error:
        datos = {"stats": {}, "reservas": [], "platos": [], "servicios": []}

    return render_template("admin/dashboard.html",
        stats = datos.get("stats", {}),
        reservas=reservas_data.get("reservas", []),
        total_paginas=reservas_data.get("total_paginas", 1),
        platos = datos.get("platos", []),
        servicios = datos.get("servicios", []),
        pagina=pagina,
        orden=orden,
        estados=estados
    )

@admin_front_bp.route("/dashboard/reservas")
@requiere_sesion
def dashboard_reservas():
    token = session.get("admin_token")

    pagina = int(request.args.get("pagina", 1))
    orden = request.args.get("orden", "asc")
    estados = request.args.getlist("estado")

    reservas, error = service_obtener_reservas(token, pagina, orden, estados)
    if error:
        return render_template("admin/dashboard.html", error=error), 500
        # return jsonify({"error": error}), 500
    return jsonify(reservas)
# ------- Platos

@admin_front_bp.route("/platos/nuevo", methods=["GET", "POST"])
@requiere_sesion
def crear_plato():

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
@requiere_sesion
def editar_plato(id):
    if request.method == "GET":
        plato, error = service_obtener_plato(id, session["admin_token"])
        if error:
            return render_template("error.html", mensaje=error), 503
        return render_template("admin/plato_form.html", plato=plato) # pasa el plato para mostrar los datos en el modo edicion
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
@requiere_sesion
def eliminar_plato(id):
    service_eliminar_plato(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/menu/<int:id>/estado")
@requiere_sesion
def cambiar_estado_plato(id):
    service_cambiar_estado_plato(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))



# ------------- Servicios

@admin_front_bp.route("/servicios/nuevo", methods=["GET", "POST"])
@requiere_sesion
def crear_servicio():
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
@requiere_sesion
def editar_servicio(id):
    if request.method == "GET":
        servicio, error = service_obtener_servicio(id, session["admin_token"])
        if error:
            return render_template("error.html", mensaje=error), 503
        return render_template("admin/servicio_form.html", servicio=servicio) # pasa el servicio para mostrar los datos en el modo edicion

    datos = {
        "nombre":      request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "activo":      request.form.get("activo") == "on",
    }
    service_editar_servicio(id, datos, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/servicios/<int:id>/eliminar", methods=["POST"])
@requiere_sesion
def eliminar_servicio(id):
    service_eliminar_servicio(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/servicios/<int:id>/estado")
@requiere_sesion
def cambiar_estado_servicio(id):
    service_cambiar_estado_servicio(id, session["admin_token"])
    return redirect(url_for("admin.dashboard"))



# ----------- Reservas
@admin_front_bp.route("/reservas/<int:id>", methods=["GET"])
@requiere_sesion
def reserva_detalle(id):
    reserva, error = service_obtener_reserva(id, session["admin_token"])
    return render_template("admin/reserva_detalle.html", reserva=reserva)

@admin_front_bp.route("/reservas/<int:id>/actualizar", methods=["POST"])
@requiere_sesion
def actualizar_estado_reserva(id):
    estado = request.form.get("estado")
    service_actualizar_reserva(id, estado)
    return redirect(url_for("admin.dashboard"))

@admin_front_bp.route("/reservas/actualizar-vencidas", methods=["POST"])
@requiere_sesion
def actualizar_reservas_vencidas():
    token = session.get("admin_token")
    service_actualizar_reservas_vencidas(token)

    return redirect(url_for("admin.dashboard"))
