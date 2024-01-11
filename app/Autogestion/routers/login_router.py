# -*- coding: utf-8 -*-
'''
Created on [Fecha de Creación]
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import re

from app.Autogestion.models.login_model import loginModel
from app.Autogestion.controllers.login_controller import login_controller

router = APIRouter(prefix='/Autoagendamiento')

def validar_correo(correo: str) -> bool:
    patron_gmail = re.compile(r'^[a-zA-Z0-9_.+-]+@clinicos\.com\.co$')
    return patron_gmail.match(correo) is not None

@router.post('/Login', summary="Iniciar Sesión", response_description="Resultado del inicio de sesión")
async def login_router(login: loginModel):
    if not validar_correo(login.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo no válido"
        )
    return await login_controller(login)

"""
# -*- coding: utf-8 -*-
'''
Created on [Fecha de Creación]
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status, Response
import re

from app.Autogestion.models.login_model import loginModel
from app.Autogestion.controllers.login_controller import login_controller

router = APIRouter(prefix='/login')

def validar_correo(correo: str) -> bool:
    patron_gmail = re.compile(r'^[a-zA-Z0-9_.+-]+@clinicos\.com\.co$')
    return patron_gmail.match(correo) is not None

@router.post('/', summary="Iniciar Sesión", response_description="Resultado del inicio de sesión")
async def login_router(response: Response, login: loginModel):
    if not validar_correo(login.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo no válido"
        )

    login_response = await login_controller(login)
    if isinstance(login_response, str):
        # En caso de que la respuesta sea un mensaje de error en forma de cadena
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=login_response
        )

    # Establecer la cookie con el token JWT
    response.set_cookie(key="access_token", value=login_response["token"], httponly=True, samesite='Lax')

    return {"message": "Login exitoso"}
 """