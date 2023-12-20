from decouple import config
import requests
import asyncio
from fastapi import HTTPException
import httpx

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id1 = config('LIST_AUTOAGENDAMIENTO_GESTION_ECOPETROL')

# Function, access token from Microsoft Graph API
async def get_access_token():
    try:
        # Parameters
        data = {
            'client_id': config('CLIENT_ID'),
            'client_secret': config('CLIENT_SECRET'),
            'grant_type': 'client_credentials',
            'scope': 'https://graph.microsoft.com/.default'
        }

        # HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.post(config('AUTH_URL'), data=data)
            response.raise_for_status()
            token = response.json().get('access_token')

    except httpx.RequestException as e:
        raise HTTPException(status_code=response.status_code, detail=f'Error en la solicitud HTTP {e}')

    except httpx.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

    return token
nombres = "Pedro Pablo"
item_id = "149"
async def uptade_ingreso(ingreso, item_id, nombres):
    try:
        token = await get_access_token()

        endpoint_url = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items/{item_id}'
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Datos a enviar en la solicitud
        item_data = {
            "fields": {
                "Ingreso": ingreso,
                "Nombres": nombres
            }
        }

        response = requests.patch(endpoint_url, json=item_data, headers=headers)

        if response.status_code == 200:
            new_item_id = response.json().get("id")
            print("Datos actualizados en SharePoint con éxito. ID del registro:", new_item_id)
            return new_item_id
        else:
            print("Error al actualizar en SharePoint. Código de estado:", response.status_code, response.text)
            return ("Error al actualizar en SharePoint. Código de estado:", response.status_code, response.text)

    except Exception as e:
        print("Error durante la operación:", e)
        return ("Error durante la operación:", e)

async def main():
    ingreso = "No Exitoso"
    await uptade_ingreso(ingreso, item_id, nombres)

# Ejecutar el bucle de eventos de asyncio
asyncio.run(main())
