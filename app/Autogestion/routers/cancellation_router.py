# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter

from app.Autogestion.controllers.cancellation_controller import cancellation_controller
from app.Autogestion.models.cancellation_model import cancellationModel

# Creación del router para la ruta /appointment-cancellation
router = APIRouter(prefix='/appointment-cancellation')

# Definición de la ruta POST en /appointment-cancellation
@router.post('/')
async def cancellation_router(cancellationModel: cancellationModel):
    #Llamar ruta para cancelar la cita asignada previamente
    return await cancellation_controller(cancellationModel)

from fastapi import APIRouter

from app.Autogestion.controllers.cancellation_controller import cancellation_controller
from app.Autogestion.models.cancellation_model import cancellationModel

# Creación del router para la ruta /appointment-cancellation
router = APIRouter(prefix='/appointment-cancellation')

# Definición de la ruta POST en /appointment-cancellation
@router.post('/')
async def cancellation_router(cancellationModel: cancellationModel):
    #Llamar ruta para cancelar la cita asignada previamente
    return await cancellation_controller(cancellationModel)
