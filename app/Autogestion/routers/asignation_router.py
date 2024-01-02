# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.asignation_controller import check_availability_controller

# Creación del router para la ruta /check_availability
router = APIRouter(prefix='/check_availability')

# Definición de la ruta GET en /check_availability
@router.get('/{id_registro}')
async def check_availability_router(id_registro: int):
    #Llamar ruta para validarsi sigue Disponible la agenda
    return await check_availability_controller(id_registro)
