"""Envío de emails usando Flask-Mail + templates Jinja2.

Cada email tiene su template en frontend/templates/email/:
  - _base.html               : layout con estilos inline, header y footer comunes
  - confirmacion_reserva.html: confirmación de reserva con QR adjunto inline
  - check_in_completado.html : agradecimiento post check-in con link de reseña
"""
import os
import qrcode
import io
import logging

from flask import render_template, current_app
from flask_mail import Mail, Message

logger = logging.getLogger(__name__)

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")


def _enviar(asunto: str, destinatario: str, template_base: str, contexto: dict) -> None:
    """Renderiza el template HTML y envía el email."""
    contexto.setdefault("frontend_base_url", FRONTEND_BASE_URL)
    cuerpo_html = render_template(f"email/{template_base}.html", **contexto)

    mensaje = Message(
        subject=asunto,
        recipients=[destinatario],
        html=cuerpo_html,
    )

    mail = Mail(current_app)
    mail.send(mensaje)
    logger.info(f"Email '{asunto}' enviado a {destinatario} (template: {template_base})")


def _generar_imagen_qr(texto_qr: str) -> bytes:
    img = qrcode.make(texto_qr)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def enviar_confirmacion_reserva(email_destino: str, nombre: str, reserva: dict) -> None:
    id_reserva = reserva["id_reserva"]
    fecha_hora = reserva.get("fecha_hora", "")
    cantidad   = reserva.get("cantidad_personas", "")
    codigo_qr  = reserva["qr"]

    url_cancelar    = f"{FRONTEND_BASE_URL}/reservar/{id_reserva}/cancelar"
    url_qr          = f"{FRONTEND_BASE_URL}/check-in/{codigo_qr}"
    imagen_qr_bytes = _generar_imagen_qr(url_qr)

    contexto = {
        "nombre":            nombre,
        "id_reserva":        id_reserva,
        "fecha_hora":        fecha_hora,
        "cantidad_personas": cantidad,
        "codigo_qr":         codigo_qr,
        "url_cancelar":      url_cancelar,
        "frontend_base_url": FRONTEND_BASE_URL,
    }
    cuerpo_html = render_template("email/confirmacion_reserva.html", **contexto)

    mensaje = Message(
        subject=f"Confirmación de reserva #{id_reserva} - Cafetería",
        recipients=[email_destino],
        html=cuerpo_html,
    )
    mensaje.attach(
        filename="qr_reserva.png",
        content_type="image/png",
        data=imagen_qr_bytes,
        disposition="inline",
        headers={"Content-ID": "<qr_image>"},
    )

    mail = Mail(current_app)
    mail.send(mensaje)
    logger.info(f"Email de confirmación de reserva #{id_reserva} enviado a {email_destino}")


def enviar_email_check_in(email_destino: str, nombre: str, id_reserva: int, link_resena: str) -> None:
    _enviar(
        asunto="¡Gracias por tu visita! Dejanos tu reseña — Cafetería",
        destinatario=email_destino,
        template_base="check_in_completado",
        contexto={
            "nombre":      nombre,
            "id_reserva":  id_reserva,
            "link_resena": link_resena,
        },
    )

def enviar_email_edicion_resena(email_destino: str, nombre: str, id_resena: int, link_edicion_resena: str) -> None:
    _enviar(
        asunto="¡Gracias por tu comentario!",
        destinatario=email_destino,
        template_base="edicion_resena",
        contexto={
            "nombre": nombre,
            "id_resena": id_resena,
            "link_edicion_resena": link_edicion_resena,
        },
    )
