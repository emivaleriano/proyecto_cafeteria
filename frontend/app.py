from flask import Flask
from datetime import timedelta
from frontend.routes.admin_routes import admin_front_bp
from frontend.routes.publico_routes import publico_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "clave-local-desarrollo")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["_base_url"] = os.environ.get("_base_url")
app.register_blueprint(admin_front_bp)
app.register_blueprint(publico_bp)



if __name__ == "__main__":
    app.run(debug=True, port=3000)
