# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status
from app.Autogestion.controllers.space_available_controller import space_available_controller

router = APIRouter(prefix='/space_available')

@router.post('/', summary="Obtener Disponibilidad de Citas", response_description="Disponibilidad de citas")
async def space_available_router():
    # Ruta para obtener la disponibilidad de citas
    try:
        return await space_available_controller()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la disponibilidad de citas: {e}"
        )
