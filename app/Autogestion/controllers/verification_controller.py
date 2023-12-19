# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023

@author:Sebastian Suarez
'''
from fastapi import HTTPException
from app.Autogestion.models.verification_model import VerificationModel
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.services.email_service import send_verification_code
from datetime import datetime, timedelta

# Almacenamiento en memoria para códigos de verificación (solo para ejemplo)
stored_verification_codes = {}

async def send_verification_code_route(verification_data: verificationModel):
    email = verification_data.correo
    verification_code = await send_verification_code(email)

    expiration_time = datetime.utcnow() + timedelta(minutes=5)

    # Almacenar código de verificación y tiempo de expiración como un diccionario
    stored_verification_codes[email] = {"code": verification_code, "expiration_time": expiration_time}
    print(stored_verification_codes)

    return {"message": f"Código de verificación enviado: {verification_code}"}

async def verify_code(verification_data: VerificationModel, login_data: verificationModel):
    email = login_data.correo
    stored_code_data = stored_verification_codes.get(email)

    if not stored_code_data:
        raise HTTPException(status_code=400, detail="Código de verificación no encontrado")

    stored_code = stored_code_data["code"]
    expiration_time = stored_code_data["expiration_time"]

    if datetime.utcnow() > expiration_time:
        raise HTTPException(status_code=400, detail="Código de verificación expirado")

    entered_code = verification_data.codigo

    if entered_code == stored_code:
        del stored_verification_codes[email]
        return {"message": "Código verificado exitosamente"}
    else:
        return {"message": "Código incorrecto"}
