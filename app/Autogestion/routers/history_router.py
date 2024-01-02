# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.Autogestion.controllers.history_controller import history_controller
from app.Autogestion.models.history_model import historyModel

# Creación del router para la ruta /history
router = APIRouter(prefix='/history')

# Configuración del esquema de autenticación OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definición de la ruta POST en /history
@router.post('/')
async def history_router(history: historyModel, token: str = Depends(oauth2_scheme)):
    # Verificar si el token está presente
    if not token:
        raise HTTPException(status_code=401, detail="No se proporcionó un token de autorización")

    # Ruta para obtener el historial de citas del paciente
    return await history_controller(history, token)
