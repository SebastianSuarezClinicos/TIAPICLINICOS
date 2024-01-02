
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, status
from app.Autogestion.controllers.update_list_controller import uptade_ingreso
from app.Autogestion.models.update_list_model import UpdateListModel

router = APIRouter(prefix='/update_ingreso')

@router.post('/', summary="Actualizar Ingreso", response_description="Resultado de la actualización")
async def update_list_router(updateModel: UpdateListModel):
    # Ruta para actualizar el campo ingreso en la lista
    try:
        return await uptade_ingreso(updateModel)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el ingreso: {e}"
        )

