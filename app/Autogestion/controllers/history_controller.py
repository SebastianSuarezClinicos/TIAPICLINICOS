# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023
Last Modified on Tue Jan 2 2024
@author: Sebastian Suarez
'''
# imports libraries
from fastapi import HTTPException
from decouple import config
import httpx
from datetime import datetime

# db
from db.client_graph import get_access_token

# Models
from app.Autogestion.models.history_model import historyModel


from app.Autogestion.services.token_User import create_access_token, get_user_current

# Environment variables
site = config('SITE_RESERVA_CITAS')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_REPORTE_DE_CITAS_SAN_MARTIN')

# CONTROLLER
async def history_controller(token: str):
    try:
        if token is None:
            raise HTTPException(
                status_code=401,
                detail="Token is missing",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token_decode = get_user_current(token)
        # db access token
        token_db = await get_access_token()

        # Parameters
        tidentificacion = token_decode.get("Tidentidad")
        nidentificacion = int(token_decode.get("Nidentidad"))
        sede = "SAN MARTIN"
        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token_db}"}

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

                return {"history": extracted_data}
            else:
                return {"error": "Formato de respuesta inesperado", "response_text": response.text}

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")
