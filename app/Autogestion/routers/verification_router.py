# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023

@author:Sebastian Suarez
'''
from fastapi import APIRouter
from app.Autogestion.controllers.verification_controller import send_verification_code_route, verify_code
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.models.verification_model import VerificationModel

router = APIRouter(prefix='/verification')

@router.post('/send-code')
async def send_verification_code_route_wrapper(login_data: verificationModel):
    return await send_verification_code_route(login_data)

@router.post('/verify-code')
async def verify_code_wrapper(verification_data: VerificationModel, login_data: verificationModel):
    return await verify_code(verification_data, login_data)
