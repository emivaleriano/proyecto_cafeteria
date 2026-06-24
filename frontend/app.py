from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
import os

from flask import Flask
from flask_mail import Mail
from datetime import timedelta
from frontend.routes.admin_routes import admin_front_bp
from frontend.routes.publico_routes import publico_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "clave-local-desarrollo")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["API_BASE_URL"] = os.environ.get("API_BASE_URL")

# Configuración de Flask-Mail (SMTP)
app.config["MAIL_SERVER"]         = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"]           = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"]        = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USE_SSL"]        = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
app.config["MAIL_USERNAME"]       = os.environ.get("MAIL_USERNAME") or None
app.config["MAIL_PASSWORD"]       = os.environ.get("MAIL_PASSWORD") or None
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME", ""))

mail = Mail(app)

app.register_blueprint(admin_front_bp)
app.register_blueprint(publico_bp)

if __name__ == "__main__":
    app.run(debug=True, port=3000)