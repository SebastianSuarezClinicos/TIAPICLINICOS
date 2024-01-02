""" # -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

# imports libraries
from fastapi import HTTPException
from decouple import config
import httpx
from datetime import datetime


# Imports
# db
from db.client_graph import get_access_token
# Models
from app.Autogestion.models.history_model import historyModel

# Environment variables
site = config('SITE_RESERVA_CITAS')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_REPORTE_DE_CITAS_SAN_MARTIN')

# CONTROLLER
async def history_controller(history: historyModel):
    try:
        # db access token
        token = await get_access_token()

        # Parameters
        tidentificacion = history.tipodeidentificacion
        nidentificacion = int(history.numerodeidentificacion)
        sede = "SAN MARTIN"
        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token}"}

        filter_query = {
            '$filter': f"fields/NumeroIdentificacion eq '{nidentificacion}' and fields/TipoIdentificacion eq '{tidentificacion}'",
            '$expand': "fields"
        }

        # HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status()
            users_data = response.json()

            if users_data and users_data.get("value", []):
                extracted_data = []
                for user in users_data["value"]:
                    # Formatear la fecha
                    fecha_inicio_cita_str = user["fields"]["FechaInicioCita"]
                    fecha_inicio_cita = datetime.strptime(fecha_inicio_cita_str, "%Y-%m-%dT%H:%M:%S%z")
                    fecha_inicio_cita_formateada = fecha_inicio_cita.strftime("%Y-%m-%d %H:%M")

                    user_info = {
                        "ID": user["id"],
                        "FechaInicioCita": fecha_inicio_cita_formateada,
                        "Servicio": user["fields"]["Servicio"],
                        "Estado": user["fields"]["Contacto"],
                        "Sede": sede,
                        "PersonaAsigna": user["fields"].get("PersonaqueAsigna_x003a_", ""),
                    }
                    extracted_data.append(user_info)

                return {"users": extracted_data}
            else:
                return {"error": "Formato de respuesta inesperado", "response_text": response.text}

    # Excepción de la respuesta JSON
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

"""
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
Last Modified on Tue Jan 2 2024
@author: Sebastian Suarez
'''

# Importaciones necesarias
from fastapi import HTTPException
from decouple import config
import httpx
from datetime import datetime

# Importaciones para manejar el token
from app.Autogestion.services.token_User import create_access_token, get_user_current
from db.client_graph import get_access_token

# Variables de entorno
site = config('SITE_RESERVA_CITAS')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_REPORTE_DE_CITAS_SAN_MARTIN')

# CONTROLADOR
async def history_controller(token: str):
    try:
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Token is missing",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Decodificar y validar el token
        token_decode = get_user_current(token)

        # Extraer la información del usuario del token
        tidentificacion = token_decode.get("Tidentidad")
        nidentificacion = token_decode.get("Nidentidad")
        sede = "SAN MARTIN"

        # Obtener el token de acceso para la solicitud HTTP
        token_db = await get_access_token()

        # Configuración de la URL y los headers
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token_db}"}

        filter_query = {
            '$filter': f"fields/NumeroIdentificacion eq '{nidentificacion}' and fields/TipoIdentificacion eq '{tidentificacion}'",
            '$expand': "fields"
        }

        # Realizar la solicitud HTTP
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status()
            users_data = response.json()

        # Procesar y devolver los datos
        if users_data.get("value", []):
            extracted_data = [process_user_data(user, sede) for user in users_data["value"]]
            return {"users": extracted_data}
        else:
            return {"error": "No se encontraron usuarios", "response_text": response.text}

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en la respuesta HTTP: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")

def process_user_data(user, sede):
    # Formatear la fecha
    fecha_inicio_cita_str = user["fields"]["FechaInicioCita"]
    fecha_inicio_cita = datetime.strptime(fecha_inicio_cita_str, "%Y-%m-%dT%H:%M:%S%z")
    fecha_inicio_cita_formateada = fecha_inicio_cita.strftime("%Y-%m-%d %H:%M")

    return {
        "ID": user["id"],
        "FechaInicioCita": fecha_inicio_cita_formateada,
        "Servicio": user["fields"]["Servicio"],
        "Estado": user["fields"]["Contacto"],
        "Sede": sede,
        "PersonaAsigna": user["fields"].get("PersonaqueAsigna_x003a_", "No definido"),
    }
