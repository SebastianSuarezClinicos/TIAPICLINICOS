# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from decouple import config
from fastapi import HTTPException
import httpx

from db.client_graph import get_access_token

# Variables de entorno
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id1 = config('LIST_AUTOAGENDAMIENTO_GESTION_ECOPETROL')

# Función para actualizar el campo "Ingreso" en un elemento de la lista de SharePoint
async def uptade_ingreso(updateModel):
    try:
        # Obtiene el token de acceso
        token = await get_access_token()

        # Construye la URL del punto final de la API de Microsoft Graph para actualizar un elemento específico
        endpoint_url = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items/{updateModel.item_id}'
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Datos a enviar en la solicitud
        item_data = {
            "fields": {
                "Ingreso": updateModel.ingreso
            }
        }

        # Realiza una solicitud PATCH para actualizar el campo "Ingreso" en el elemento específico de la lista
        async with httpx.AsyncClient() as client:
            response = await client.patch(endpoint_url, json=item_data, headers=headers)
            response.raise_for_status()

    # Manejo de excepciones para posibles errores en la solicitud y respuesta HTTP
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        if hasattr(e, "response") and e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la respuesta HTTP: {e}")
        else:
            raise HTTPException(status_code=500, detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

    # Manejo de la respuesta y posibles errores
    if response.status_code == 200:
        new_item_id = response.json().get("id")
        #print("Datos actualizados en SharePoint con éxito. ID del registro:", new_item_id)
        return ("Datos actualizados en SharePoint con éxito. ID del registro:", new_item_id)
    else:
        #print("Error al actualizar en SharePoint. Código de estado:", response.status_code, response.text)
        raise HTTPException(status_code=response.status_code, detail=response.text)
