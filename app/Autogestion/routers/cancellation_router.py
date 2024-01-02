# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status
from app.Autogestion.controllers.cancellation_controller import cancellation_controller
from app.Autogestion.models.cancellation_model import cancellationModel

# Creación del router para la ruta /appointment-cancellation
router = APIRouter(prefix='/appointment-cancellation')

# Definición de la ruta POST en /appointment-cancellation
@router.post('/', summary="Cancelar Cita", response_description="Resultado de la cancelación de la cita")
async def cancellation_router(cancellation_data: cancellationModel):
    try:
    #Llamar ruta para cancelar la cita asignada previamente
        return await cancellation_controller(cancellation_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar la cita: {e}"
        )
