# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023

@author: Sebastian Suarez
'''

# verification_router.py
from fastapi import APIRouter
from app.Autogestion.controllers.verification_controller import send_verification_code_route, verify_code
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.models.verification_model import VerificationModel
from fastapi import Header

router = APIRouter(prefix='/verification')

@router.post('/send-code')
async def send_verification_code_route_wrapper(login_data: verificationModel):
    # Ruta para enviar el código de verificación
    return await send_verification_code_route(login_data)

@router.post('/verify-code/{item_id}')
async def verify_code_wrapper(
    verification_data: VerificationModel,
    login_data: verificationModel,
    item_id: str,
    authorization: str = Header(...),
):
    # Ruta para verificar el código ingresado
    return await verify_code(verification_data, login_data, item_id, authorization)
