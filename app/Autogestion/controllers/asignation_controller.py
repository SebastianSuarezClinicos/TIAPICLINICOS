# -*- coding: utf-8 -*-
'''
Created on Mon Jan 2 2024
@author: Sebastian Suarez
'''

# Imports
from fastapi import HTTPException, Request
import httpx
from decouple import config

# Importar modelos y otros módulos necesarios
from app.Autogestion.models.asignation_model import AsignationModel, checkAvailabilityModel
from db.client_graph import get_access_token
from app.Autogestion.services.token_User import get_user_current

# Configuración de variables de entorno
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_RUTH_YURANYS_ARMENTA_POLO')

# Controlador para asignar una cita
async def asignation_controller(asignation_data: AsignationModel,
    request: Request):
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Cookie is missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        #print("Prueba",token)

        # Decodificar y validar el token
        token_decode = get_user_current(token)
        #print(token_decode)
        # Verificar disponibilidad de la cita
        availability = await check_availability_controller(checkAvailabilityModel(id_registro=asignation_data.Id))
        #print(availability)
        # Si la agenda está disponible
        if availability == "Disponible":
            # Obtener token de acceso para la API de Microsoft Graph
            token_db = await get_access_token()

            Nombredelpaciente= asignation_data.nombre.upper()
            #print(Nombredelpaciente)
            # Preparar URL y headers para la solicitud PATCH
            URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items/{asignation_data.Id}'
            headers = {"Authorization": f"Bearer {token_db}"}

            # Preparar datos para actualizar la cita
            update_data = {
            "fields":{
                "EstadodelaCita": "Asignada",
                "Identificaci_x00f3_n": token_decode.get("Nidentidad"),
                "Nombredelpaciente": Nombredelpaciente,
                "Modalidadinicial":asignation_data.modalidad.upper(),
                "Modalidad":asignation_data.modalidad.upper(),
                "UsuarioAsigna": "AUTOAGENDAMIENTO",
                "CorreoPersonaAsigna": token_decode.get("Correo")
                }
            }

            # Realizar solicitud PATCH para actualizar la cita
            async with httpx.AsyncClient() as client:
                response = await client.patch(URL, json=update_data, headers=headers)
                response.raise_for_status()
            return {"message": "Cita asignada con éxito"}#, "Response": response.json()

        # Si la agenda no está disponible
        else:
            return {"message": "La agenda NO está disponible"}

    # Manejar errores específicos relacionados con HTTP
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en la solicitud HTTP: {e}")

    # Manejar cualquier otro error
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la operación: {e}")

# Controlador para verificar disponibilidad de una cita
async def check_availability_controller(availability_data: checkAvailabilityModel):
    try:
        # Obtener token de acceso para la API de Microsoft Graph
        token = await get_access_token()

        # Preparar URL y headers para la solicitud GET
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items/{availability_data.id_registro}'
        headers = {"Authorization": f"Bearer {token}"}

        # Realizar solicitud GET para verificar la disponibilidad
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers)
            response.raise_for_status()
            data = response.json()

            estado_cita = data["fields"]["Estado_x0020_de_x0020_la_x0020_c"]
            # Determinar el estado de la cita
            if estado_cita != "Disponible":
                return "No Disponible"
            else:
                return "Disponible"

    # Manejar errores específicos de la solicitud HTTP
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    # Manejar errores específicos de la respuesta HTTP
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en la respuesta HTTP: {e}")

    # Manejar errores al analizar el JSON
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")


