# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from decouple import config
from fastapi import HTTPException
import httpx

from db.client_graph import get_access_token

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id1 = config('LIST_AUTOAGENDAMIENTO_GESTION_ECOPETROL')

async def uptade_ingreso(updateModel):
    try:
        token = await get_access_token()

        endpoint_url = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items/{updateModel.item_id}'
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Datos a enviar en la solicitud
        item_data = {
            "fields": {
                "Ingreso": updateModel.ingreso
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(endpoint_url, json=item_data, headers=headers)
            response.raise_for_status()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        if hasattr(e, "response") and e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la respuesta HTTP: {e}")
        else:
            raise HTTPException(status_code=500, detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

    if response.status_code == 200:
        new_item_id = response.json().get("id")
        print("Datos actualizados en SharePoint con éxito. ID del registro:", new_item_id)
        return new_item_id
    else:
        print("Error al actualizar en SharePoint. Código de estado:", response.status_code, response.text)
        raise HTTPException(status_code=response.status_code, detail=response.text)
