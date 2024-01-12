""" # -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.Autogestion.controllers.history_controller import history_controller
from app.Autogestion.models.history_model import historyModel


# Creación del router para la ruta /history
router = APIRouter(prefix='/Autoagendamiento')


# Configuración del esquema de autenticación OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definición de la ruta POST en /history
@router.post('/History', summary="Obtener Historial de Citas", response_description="Historial de citas del paciente")
async def history_router(token: str = Depends(oauth2_scheme)):
    # Verificar si el token está presente
    if not token:
        raise HTTPException(status_code=401, detail="No se proporcionó un token de autorización")

    # Ruta para obtener el historial de citas del paciente
    return await history_controller(token)

"""
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from app.Autogestion.controllers.history_controller import history_controller

# Creación del router para la ruta /history
router = APIRouter(prefix='/Autoagendamiento')

# Configuración del esquema de autenticación OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definición de la ruta POST en /history
@router.post('/History', summary="Obtener Historial de Citas", response_description="Historial de citas del paciente")
async def history_router(authorization: str = Header(None)):
    # Extraer el token del encabezado Authorization
    if not authorization:
        raise HTTPException(status_code=401, detail="No se proporcionó un token de autorización")

    # Asumiendo que el token viene con el prefijo "Bearer", se debe quitar este prefijo.
    token = authorization.split(" ")[1] if len(authorization.split(" ")) > 1 else None
    if not token:
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    # Ruta para obtener el historial de citas del paciente
    return await history_controller(token)
