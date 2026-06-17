from flask import jsonify
from werkzeug.exceptions import HTTPException

def registrar_manejadores(app):
    """Registra manejadores globales de errores HTTP."""

    # --- Excepciones de Python →  HTTP ---

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": "Solicitud incorrecta", "detalle": str(e)}), 400

    @app.errorhandler(KeyError)
    def handle_key_error(e):
        return jsonify({"error": "Conflicto", "detalle": str(e)}), 409

    @app.errorhandler(LookupError)
    def handle_lookup_error(e):
        return jsonify({"error": "Recurso no encontrado", "detalle": str(e)}), 404

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.exception(e)  # imprime el traceback completo en consola
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500


    # --- HTTP
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Solicitud incorrecta", "detalle": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso no encontrado", "detalle": str(e)}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.name, "detalle": e.description}), e.code
