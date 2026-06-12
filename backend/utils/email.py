import os
import smtplib
import qrcode
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5001")


def generar_imagen_qr(texto_qr):
    """
    Genera un QR en memoria y lo devuelve como bytes PNG.
    """
    img = qrcode.make(texto_qr)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def enviar_confirmacion_reserva(email_destino, nombre, reserva):
    """
    Envía el email de confirmación con el QR adjunto y el botón de cancelar.

    Args:
        email_destino (str): Email del usuario.
        nombre (str): Nombre del usuario.
        reserva (dict): Datos de la reserva (id_reserva, fecha_hora, cantidad_personas, qr).
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        # Si no hay credenciales configuradas, no falla — solo avisa
        print("[EMAIL] Variables SMTP_USER / SMTP_PASSWORD no configuradas. Email no enviado.")
        return

    id_reserva = reserva["id_reserva"]
    fecha_hora = reserva.get("fecha_hora", "")
    cantidad = reserva.get("cantidad_personas", "")
    codigo_qr = reserva["qr"]

    url_cancelar = f"{FRONTEND_BASE_URL}/reservar/{id_reserva}/cancelar"

    # Genera la imagen QR
    imagen_qr_bytes = generar_imagen_qr(codigo_qr)
    imagen_qr_b64 = base64.b64encode(imagen_qr_bytes).decode("utf-8")

    # Arma el mensaje MIME
    msg = MIMEMultipart("related")
    msg["Subject"] = f"Confirmación de reserva #{id_reserva} - Cafetería"
    msg["From"] = SMTP_USER
    msg["To"] = email_destino

    # Cuerpo HTML con el QR embebido (cid:qr_image)
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto;">
        <h2 style="color: #c0392b;">¡Reserva confirmada, {nombre}!</h2>
        <p>Tu reserva fue registrada exitosamente. Presentá el código QR al llegar al local.</p>

        <table style="border-collapse: collapse; width: 100%; margin-bottom: 16px;">
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Número de reserva</td>
            <td style="padding: 8px; border: 1px solid #ddd;">#{id_reserva}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Fecha y horario</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{fecha_hora}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Cantidad de personas</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{cantidad}</td>
          </tr>
        </table>

        <div style="text-align: center; margin: 24px 0;">
          <img src="cid:qr_image" alt="Código QR de tu reserva"
               style="width: 200px; height: 200px; border: 2px solid #eee; padding: 8px;" />
          <p style="font-size: 12px; color: #888;">Código: {codigo_qr}</p>
        </div>

        <hr style="border: none; border-top: 1px solid #eee;">

        <p style="margin-top: 24px;">
          ¿No podés asistir? Podés cancelar tu reserva haciendo clic en el botón de abajo.
        </p>

        <div style="text-align: center; margin: 16px 0;">
          <a href="{url_cancelar}"
             style="background-color: #c0392b; color: white; padding: 12px 28px;
                    text-decoration: none; border-radius: 6px; font-size: 15px;
                    display: inline-block;">
            Cancelar reserva
          </a>
        </div>

        <p style="font-size: 12px; color: #aaa; margin-top: 32px;">
          Si no realizaste esta reserva, podés ignorar este mensaje.<br>
          Cafetería — {FRONTEND_BASE_URL}
        </p>
      </body>
    </html>
    """

    parte_html = MIMEText(html, "html")
    msg.attach(parte_html)

    # Adjunta el QR como imagen inline
    imagen_mime = MIMEImage(imagen_qr_bytes, _subtype="png")
    imagen_mime.add_header("Content-ID", "<qr_image>")
    imagen_mime.add_header("Content-Disposition", "inline", filename="qr_reserva.png")
    msg.attach(imagen_mime)

    # Envía el mail
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.login(SMTP_USER, SMTP_PASSWORD)
            servidor.sendmail(SMTP_USER, email_destino, msg.as_string())
        print(f"[EMAIL] Confirmación enviada a {email_destino}")
    except smtplib.SMTPException as e:
        # No queremos que un fallo de email rompa la reserva
        print(f"[EMAIL] Error al enviar email: {e}")