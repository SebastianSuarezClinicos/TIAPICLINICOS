# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status
from fastapi import Response

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


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logout exitoso"}
