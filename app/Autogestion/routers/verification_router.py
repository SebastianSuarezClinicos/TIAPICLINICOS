# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, Header, Response, status
import re
from app.Autogestion.controllers.verification_controller import send_verification_code_route, verify_code
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.models.verification_model import VerificationModel

router = APIRouter(prefix='/verification')

@router.post('/send-code', summary="Enviar código de verificación", response_description="Resultado del envío")
async def send_verification_code_route_wrapper(login_data: verificationModel):
    # Ruta para enviar el código de verificación
    try:
        return await send_verification_code_route(login_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post('/verify-code', summary="Verificar código", response_description="Resultado de la verificación")
async def verify_code_wrapper(
    response: Response,
    verification_data: VerificationModel,
    authorization: str = Header(None),
):
    # Ruta para verificar el código ingresado
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó un token de autorización"
        )

    verify_code_response = await verify_code(verification_data, authorization)
    # Establecer la cookie con el token JWT
    response.set_cookie(key="access_token", value=verify_code_response["token"], httponly=True, secure=True, path="http://localhost:3000/autoAgendamiento", samesite='None', max_age=1800)
    return ("Verificacion exitosa", verify_code_response["history_result"])


