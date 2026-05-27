from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from backend.utils.manejador_errores import registrar_manejadores


load_dotenv(Path(__file__).parent / ".env")

from backend.blueprints.admin_routes import admin_bp # noqa: E402
from backend.blueprints.servicios_routes import servicios_bp # noqa: E402


app = Flask(__name__)
registrar_manejadores(app)

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(servicios_bp, url_prefix="/servicios")


@app.route('/')
def home():
    return "API funcionando"

if __name__ == '__main__':

    app.run(debug=True, port= 5000)
