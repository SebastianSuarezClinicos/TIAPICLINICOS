# -*- coding: utf-8 -*-
'''
#Created on Mon Dec 22 2023

#@author: Sebastian Suarez
'''

# Imports
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from decouple import config
import httpx

# db
from db.client_graph import get_access_token

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_RUTH_YURANYS_ARMENTA_POLO')

# CONTROLLER
async def space_available_controller():
    try:
        # db access token
        token = await get_access_token()

        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token}"}

        filter_query = {'$filter': f"fields/Title eq 'SALUD OCUPACIONAL' ",
                        "$expand": "fields"}

        # HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status()
            data = response.json().get("value", [])

        result_data = {}
        count = 0

        fecha_hora_actual_utc = datetime.now(timezone.utc)
        offset_colombia = -5
        fecha_hora_actual_colombia = fecha_hora_actual_utc + timedelta(hours=offset_colombia)
        fecha_hora_actual_str = fecha_hora_actual_colombia.strftime("%Y-%m-%d %H:%M")

        for data_item in data:
            count += 1
            # Validar el estado de la cita
            estado_cita = data_item["fields"]["Estado_x0020_de_x0020_la_x0020_c"]
            if estado_cita != "Disponible":
                count -= 1
                continue

            # Formatear las fechas
            fecha_inicial_cita_str = data_item["fields"]["FechayHorainicialdedisponibilida"]
            fecha_inicial_cita = datetime.strptime(fecha_inicial_cita_str, "%Y-%m-%dT%H:%M:%S%z")
            fecha_inicial_cita_formateada = (fecha_inicial_cita + timedelta(hours=offset_colombia)).strftime("%Y-%m-%d %H:%M")

            fecha_final_cita_str = data_item["fields"]["FechayHorafinaldedisponibilidad"]
            fecha_final_cita = datetime.strptime(fecha_final_cita_str, "%Y-%m-%dT%H:%M:%S%z")
            fecha_final_cita_formateada = (fecha_final_cita + timedelta(hours=offset_colombia)).strftime("%Y-%m-%d %H:%M")

            # Validar si la fecha y hora actual son mayores a la fecha inicial
            if fecha_hora_actual_str > fecha_inicial_cita_formateada:
                count -= 1
                continue

            usuario_asigna = data_item["fields"].get("UsuarioAsigna", None)

            user_data = {
                "Id_Registro": data_item["fields"]["id"],
                "Estado_de_la_Cita": estado_cita,
                "Fecha_y_Hora_Inicial": fecha_inicial_cita_formateada,
                "Fecha_y_Hora_Final": fecha_final_cita_formateada,
                "Nombre_del_Profesional": data_item["fields"]["Title"],
                "Responsable_del_Agendamiento": usuario_asigna if usuario_asigna is not None else "No Asignado",
                "Sede": "SAN MARTÍN",
            }

            result_data[count] = user_data

        return {"Cupos disponibles": result_data}

    # Excepción de la respuesta JSON
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")
