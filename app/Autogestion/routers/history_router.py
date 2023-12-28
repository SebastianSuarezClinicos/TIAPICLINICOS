# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.history_controller import history_controller
from app.Autogestion.models.history_model import historyModel

# Creación del router para la ruta /history
router = APIRouter(prefix='/history')

# Definición de la ruta POST en /history
@router.post('/')
async def history_router(history: historyModel):
    #Ruta para obtener el historial de citas del paciente
    return await history_controller(history)
