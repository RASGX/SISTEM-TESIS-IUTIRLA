import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Configuración del servidor SMTP (ejemplo con Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CORREO_EMISOR = "tu_correo_biblioteca@gmail.com"  # Correo de la institución/sistema
PASSWORD_EMISOR = "tu_clave_de_aplicacion"       # Contraseña de aplicación generada

def enviar_tesis_por_correo(correo_destino: str, nombre_estudiante: str, titulo_tesis: str, ruta_pdf: str):
    # Crear la estructura del mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = CORREO_EMISOR
    mensaje["To"] = correo_destino
    mensaje["Subject"] = f"Entrega Digital de Tesis - {titulo_tesis}"

    cuerpo = f"""
    Hola {nombre_estudiante},

    Adjunto a este correo encontrarás el archivo digital en PDF de la tesis solicitada:
    "{titulo_tesis}".

    Saludos,
    Departamento de Archivo y Biblioteca IUTIRLA.
    """
    mensaje.attach(MIMEText(cuerpo, "plain"))

    # Adjuntar el archivo PDF si existe en la carpeta uploads/
    if os.path.exists(ruta_pdf):
        with open(ruta_pdf, "rb") as archivo:
            adjunto = MIMEApplication(archivo.read(), _subtype="pdf")
            adjunto.add_header("Content-Disposition", "attachment", filename=os.path.basename(ruta_pdf))
            mensaje.attach(adjunto)

    # Conexión al servidor SMTP para realizar el envío
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(CORREO_EMISOR, PASSWORD_EMISOR)
        server.send_message(mensaje)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False