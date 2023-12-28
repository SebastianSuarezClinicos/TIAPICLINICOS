
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023

@author: Sebastian Suarez
'''

# Imports
from fastapi import HTTPException
from decouple import config
import httpx
from app.Autogestion.models.cancellation_model import cancellationModel

# db
from db.client_graph import get_access_token
# Models

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_RUTH_YURANYS_ARMENTA_POLO')

# CONTROLLER
async def cancellation_controller(cancellationModel: cancellationModel):
    try:
        # db access token
        token = await get_access_token()

        # Parameters
        idRegistro = cancellationModel.id_registro

        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items/{idRegistro}'
        headers = {"Authorization": f"Bearer {token}"}

        filter_query = {'$filter': f"fields/Title eq 'SALUD OCUPACIONAL' ",
                        "$expand": "fields"}

        estadoCita = {
            "fields":{"EstadodelaCita": "Cancelada"}
            }

        # HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.patch(URL, headers=headers, json=estadoCita)#, params=filter_query validacion adicional 
            response.raise_for_status()

            updated_response = await client.get(URL, headers=headers, params=filter_query)
            updated_response.raise_for_status()
            updated_data = updated_response.json()

        #Respuesta
        return {
            "Mensaje": f"Estado de la cita del registro {idRegistro} fue actualizado a {estadoCita['EstadodelaCita']}",#
            "Datos actualizados": updated_data
        }

    # Excepción de la respuesta JSON
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")
