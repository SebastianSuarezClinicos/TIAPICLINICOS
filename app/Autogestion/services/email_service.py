# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023

@author:Sebastian Suarez
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from decouple import config
from datetime import datetime, timedelta

# Diccionario para almacenar códigos de verificación con tiempo de expiración
verification_codes = {}

async def send_verification_code(email: str):
    verification_code = secrets.token_hex(2)

    # Tiempo de expiración (5 minutos en este caso)
    expiration_time = datetime.utcnow() + timedelta(minutes=5)

    # Almacenar código de verificación con tiempo de expiración
    verification_codes[email] = {"code": verification_code, "expiration_time": expiration_time}

    smtp_host = config("SMTP_HOST")
    smtp_port = config("SMTP_PORT", default=587, cast=int)
    smtp_user = config("SMTP_USER")
    smtp_password = config("SMTP_PASSWORD")
    sender_email = config("SENDER_EMAIL")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Código de verificación"

    # Deshabilitar la respuesta al correo electrónico
    message["Reply-To"] = "noreply@example.com"

    # Cuerpo del mensaje en formato HTML con estilos y colores
    body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                justify-content: center;
                align-items: center;
                height: 37vh;
            }}
            .container {{
                text-align: center;
                background-color: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 215, 0.5);
            }}
            h1 {{
                color: #333;
            }}
            p {{
                font-size: 18px;
                color: #555;
            }}
            strong {{
                color: #1e90ff;
            }}
            em {{
                font-style: italic;
                color: #777;
            }}
            .disclaimer {{
                font-size: 12px;
                color: #777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Código de Verificación</h1>
            <p>Tu código de verificación es: <strong>{verification_code}</strong></p>
            <p>Este código expirará en 5 minutos.</p>
            <p><em>Este correo no puede ser respondido. Por favor, no responda a esta dirección de correo electrónico.</em></p>
            <p class="disclaimer">Este mensaje y cualquier archivo es considerado confidencial y podría contener información privilegiada y/o reservada de Clínicos IPS, para el uso exclusivo de su destinatario. Si llegó a usted por error, le agradecemos eliminarlo e informar al remitente, absteniéndose de divulgarlo en cualquier forma. En caso contrario, podría ser objeto de sanciones acorde a la ley. Las opiniones contenidas en este mensaje y sus adjuntos no necesariamente coinciden con las posiciones institucionales de Clínicos IPS.</p>
        </div>
    </body>
    </html>
    """
    phone_number = "+573502414696"
    # Adjuntar el cuerpo del mensaje al mensaje principal
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, email, message.as_string())

    return verification_code
