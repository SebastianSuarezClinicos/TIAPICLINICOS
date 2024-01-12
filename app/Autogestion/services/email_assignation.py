import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

def send_email_with_attachment(age, recipient_email, attachment_paths):
    # Cargar configuración desde variables de entorno
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))

    # Seleccionar el archivo .msg adecuado según la edad
    attachment_path = attachment_paths.get('adult' if age >= 18 else 'child', None)
    if not attachment_path:
        raise ValueError("No se encontró un archivo .msg adecuado para la edad dada.")

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Asunto del Correo"

    # Agregar el cuerpo del correo
    body = "Cuerpo del correo"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el archivo .msg
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
        message.attach(part)

    # Conectar al servidor SMTP y enviar el correo
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

# Rutas a los archivos .msg
attachment_paths = {
    'child': 'ruta_del_archivo_para_menores.msg',
    'adult': 'ruta_del_archivo_para_adultos.msg'
}

# Ejemplo de uso
try:
    send_email_with_attachment(20, "correo_destinatario@gmail.com", attachment_paths)
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar correo: {e}")
