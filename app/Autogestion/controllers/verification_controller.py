
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 19 2023

@author: Sebastian Suarez
'''

from decouple import config
from fastapi import HTTPException
from jose import jwt
from app.Autogestion.models.verification_model import VerificationModel
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.services.email_service import send_verification_code
from datetime import datetime, timedelta

# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM =  config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Creación de token
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Almacenamiento en memoria para códigos de verificación (solo para ejemplo)
stored_verification_codes = {}

async def send_verification_code_route(verification_data: verificationModel):
    email = verification_data.correo
    verification_code = await send_verification_code(email)

    expiration_time = datetime.utcnow() + timedelta(minutes=5)


    stored_verification_codes[email] = {"code": verification_code, "expiration_time": expiration_time, "attempts": 0}
    print(stored_verification_codes)

    access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
    code_token = create_access_token(data={"Código de verificación enviado": verification_code}, expires_delta=access_token_expires)


    return {"token": code_token}


async def verify_code(verification_data: VerificationModel, login_data: verificationModel):
    email = login_data.correo
    stored_code_data = stored_verification_codes.get(email)

    if not stored_code_data:
        raise HTTPException(status_code=400, detail="Código de verificación no encontrado")

    expiration_time = stored_code_data["expiration_time"]

    if datetime.utcnow() > expiration_time:
        raise HTTPException(status_code=400, detail="El código de verificación ha expirado")

    stored_code = stored_code_data["code"]
    entered_code = verification_data.codigo

    if entered_code == stored_code:
        del stored_verification_codes[email]
        return {"message": "Código verificado exitosamente"}
    else:
        attempts = stored_code_data["attempts"]
        attempts += 1
        stored_verification_codes[email]["attempts"] = attempts

        max_attempts = 3
        if attempts >= max_attempts:
            del stored_verification_codes[email]
            raise HTTPException(status_code=400, detail="Se ha superado el límite de intentos, por favor solicite un nuevo código.")
        else:
            raise HTTPException(status_code=400, detail="Código incorrecto, por favor inténtelo de nuevo.")
