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

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_RUTH_YURANYS_ARMENTA_POLO')

# CONTROLLER
async def check_availability_controller(id_registro: int):
    try:
        # db access token
        token = await get_access_token()

        # Parameters
        idRegistro = id_registro

        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items/{idRegistro}'
        headers = {"Authorization": f"Bearer {token}"}

        # HTTP REQUEST PARA OBTENER EL ESTADO ACTUAL
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers)
            response.raise_for_status()
            data = response.json()

            # VALIDAR SI EL CAMPO 'estado' ESTA 'Disponible'
            estado = "Disponible" if data.get("fields", {}).get("estado", None) == "Asignada" else "Disponible"

        return estado

    # Excepción de la respuesta JSON
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

