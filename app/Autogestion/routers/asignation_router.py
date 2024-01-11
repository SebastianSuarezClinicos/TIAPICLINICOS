# -*- coding: utf-8 -*-
'''
Created on Mon Jan 2 2024
@author: Sebastian Suarez
'''

from fastapi import APIRouter, HTTPException, Request, status
from app.Autogestion.models.asignation_model import AsignationModel
from app.Autogestion.controllers.asignation_controller import asignation_controller

# Crear un nuevo router para las rutas relacionadas con la asignación
router = APIRouter(prefix='/Autoagendamiento')

@router.post("/asignation-schedule",
            summary="Asignar una cita",
            response_description="Resultado de la asignación",
            response_model=dict)
async def asignar_cita(asignation_data: AsignationModel, request: Request):
    try:
        token = request.cookies.get('access_token')
        #print(token)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó un token de autorización"
        )
        # Llama al controlador para procesar la asignación de la cita
        result = await asignation_controller(asignation_data, request)
        return result
    except HTTPException as http_exc:
        # Propagar excepciones HTTP tal como se reciben
        raise http_exc
    except Exception as e:
        # Manejar cualquier otra excepción como un error interno del servidor
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal Server Error: {e}")
