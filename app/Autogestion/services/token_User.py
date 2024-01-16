# -*- coding: utf-8 -*-
'''
Created on Mon Dec 27 2023

@author: Sebastian Suarez
'''

# imports libraries
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from jwt import DecodeError, ExpiredSignatureError


# Creación de token de acceso ---------------------------------------------------------------->
# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Creación de token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Validar token
def get_user_current(token: str):
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="No se ha proporcionado una cookie de autenticación",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})

        if 'user_info' in token_decode:
            token_decode = token_decode.get("user_info")

        identification_number = token_decode.get("Nidentidad")

        if identification_number is None:
            raise HTTPException(
                status_code=401,
                detail="El token es válido pero falta el número de identidad",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except DecodeError:
        raise HTTPException(
            status_code=401,
            detail="Error al decodificar el token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Error en la validación del token JWT",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token_decode
