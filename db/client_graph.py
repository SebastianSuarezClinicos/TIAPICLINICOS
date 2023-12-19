# Imports libraries
from fastapi import HTTPException
from decouple import config
import httpx



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
            response.raise_for_status
            token = response.json()['access_token']


    except httpx.RequestException as e:
        HTTPException(status_code=response.status_code,
                    message=f'Error en la solicitud HTTP {e}')

    except httpx.HTTPError as e:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")
    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al analizar JSON: {e}")

    return token
