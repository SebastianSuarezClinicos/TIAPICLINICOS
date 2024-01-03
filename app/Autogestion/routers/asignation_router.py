# -*- coding: utf-8 -*-
'''
Created on Mon Jan 2 2024
@author: Sebastian Suarez
'''

from fastapi import APIRouter, Depends, HTTPException, Header, status
from app.Autogestion.models.asignation_model import AsignationModel
from app.Autogestion.controllers.asignation_controller import asignation_controller
from app.Autogestion.services.token_User import get_user_current

# Crear un nuevo router para las rutas relacionadas con la asignación
router = APIRouter(prefix='/asignation-schedule')

@router.post("/",
            summary="Asignar una cita",
            response_description="Resultado de la asignación",
            response_model=dict)
async def asignar_cita(asignation_data: AsignationModel, authorization: str = Header(None),):
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó un token de autorización"
        )
        # Llama al controlador para procesar la asignación de la cita
        result = await asignation_controller(asignation_data, authorization)
        return result
    except HTTPException as http_exc:
        # Propagar excepciones HTTP tal como se reciben
        raise http_exc
    except Exception as e:
        # Manejar cualquier otra excepción como un error interno del servidor
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal Server Error: {e}")


"""Descomentar para probar disponibilidad
from app.Autogestion.controllers.asignation_controller import check_availability_controller

# Creación del router para la ruta /check_availability
router = APIRouter(prefix='/check_availability')

# Definición de la ruta GET en /check_availability
@router.get('/{id_registro}')
async def check_availability_router(id_registro: int):
    #Llamar ruta para validarsi sigue Disponible la agenda
    return await check_availability_controller(id_registro)

"""