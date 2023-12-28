# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.space_available_controller import space_available_controller

router = APIRouter(prefix='/space_available')

@router.post('/')
async def space_available_router():
    # Ruta para obtener la disponibilidad de citas
    return await space_available_controller()
