# -*- coding: utf-8 -*-
'''
Created on Mon Dec 19 2023

@author: Sebastian Suarez
'''

from decouple import config
import httpx
from datetime import datetime

from db.client_graph import get_access_token
from fastapi import HTTPException

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id1 = config('LIST_AUTOAGENDAMIENTO_GESTION_ECOPETROL')

async def write_list(correo, nombres, apellidos, tipo_identificacion, numero_identificacion, ingreso):
    try:
        fecha_hora_actual = datetime.utcnow().isoformat()+"Z"
        numero_identificacion = int(numero_identificacion)
        token = await get_access_token()

        endpoint_url = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items'
        headers = {"Authorization": f"Bearer {token}"}

        # Datos a enviar en la solicitud
        item_data = {
            "fields": {
                "Fecha": fecha_hora_actual,
                "Login": correo,
                "Nombres": nombres,
                "Apellido": apellidos,
                "TipoIdentificacion": tipo_identificacion,
                "NoIdentificacion": numero_identificacion,
                "Ingreso": ingreso
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint_url, json=item_data, headers=headers)
            response.raise_for_status()

        # MANEJO RESPUESTA Y POSIBLES ERRORES
        if response.status_code == 201:
            item_id = response.json().get("id")
            return {"Ingreso": ingreso, "Registro": item_id}

        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error al escribir en SharePoint. Código de estado: {response.status_code}")

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        if hasattr(e, "response") and e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la respuesta HTTP: {e}")
        else:
            raise HTTPException(status_code=500, detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")
