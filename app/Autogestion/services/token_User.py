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
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError


# Creación de token de acceso ---------------------------------------------------------------->
# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Creación de token
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_current(token: str):
    try:
        # Intenta decodificar el token JWT usando la clave secreta y el algoritmo especificado.
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})

        # Extrae el número de identificación del token decodificado.
        identification_number = token_decode.get("Nidentidad")

        # Si el número de identificación no está presente, levanta una excepción HTTP.
        if identification_number is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except ExpiredSignatureError:
        # Caso específico para cuando el token ha expirado.
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except DecodeError:
        # Caso específico para cuando el token está malformado.
        raise HTTPException(
            status_code=401,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError as e:
        # Caso general para otros errores relacionados con JWT.
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from e

    # Devuelve el token decodificado si no hay errores.
    return token_decode