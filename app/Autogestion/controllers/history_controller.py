# -*- coding: utf-8 -*-
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

