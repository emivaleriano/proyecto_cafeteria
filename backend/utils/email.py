"""Envío de emails usando Flask-Mail + templates Jinja2.

Los templates viven en frontend/templates/email/:
  - _base.html               : layout con estilos inline, header y footer comunes
  - confirmacion_reserva.html: confirmación de reserva con QR adjunto inline
  - check_in_completado.html : agradecimiento post check-in con link de reseña
"""
import os
import qrcode
import io
import logging
from pathlib import Path
from email.mime.image import MIMEImage
from flask_mail import Mail, Message
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")

_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "frontend" / "templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=True)


def _renderizar(template_path: str, **contexto) -> str:
    contexto.setdefault("frontend_base_url", FRONTEND_BASE_URL)
    return _jinja_env.get_template(template_path).render(**contexto)


def _generar_imagen_qr(texto_qr: str) -> bytes:
    img = qrcode.make(texto_qr)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def enviar_confirmacion_reserva(email_destino: str, nombre: str, reserva: dict, app) -> None:
    id_reserva = reserva["id_reserva"]
    fecha_hora = reserva.get("fecha_hora", "")
    cantidad   = reserva.get("cantidad_personas", "")
    codigo_qr  = reserva["qr"]

    url_cancelar    = f"{FRONTEND_BASE_URL}/reservar/{id_reserva}/cancelar"
    url_qr          = f"{FRONTEND_BASE_URL}/check-in/{codigo_qr}"
    imagen_qr_bytes = _generar_imagen_qr(url_qr)

    html = _renderizar(
        "email/confirmacion_reserva.html",
        nombre=nombre,
        id_reserva=id_reserva,
        fecha_hora=fecha_hora,
        cantidad_personas=cantidad,
        codigo_qr=codigo_qr,
        url_cancelar=url_cancelar,
    )

    with app.app_context():
        mensaje = Message(
            subject=f"Confirmación de reserva #{id_reserva} - Cafetería",
            recipients=[email_destino],
            html=html,
        )
        mensaje.attach(
            filename="qr_reserva.png",
            content_type="image/png",
            data=imagen_qr_bytes,
            disposition="inline",
            headers={"Content-ID": "<qr_image>"},
        )
        Mail(app).send(mensaje)
    logger.info(f"Email de confirmación de reserva #{id_reserva} enviado a {email_destino}")


def enviar_email_check_in(email_destino: str, nombre: str, id_reserva: int, link_resena: str, app) -> None:
    html = _renderizar(
        "email/check_in_completado.html",
        nombre=nombre,
        id_reserva=id_reserva,
        link_resena=link_resena,
    )

    with app.app_context():
        mensaje = Message(
            subject="¡Gracias por tu visita! Dejanos tu reseña — Cafetería",
            recipients=[email_destino],
            html=html,
        )
        Mail(app).send(mensaje)
    logger.info(f"Email de check-in enviado a {email_destino}")