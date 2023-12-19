# -*- coding: utf-8 -*-
'''
Created on Mon Dec 19 2023

@author:Sebastian Suarez
'''

from decouple import config
import requests
from datetime import datetime

from db.client_graph import get_access_token



async def write_list(access_token, correo, nombres, apellidos, tipo_identificacion, numero_identificacion, ingreso):
    try:
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M") #
        token = await get_access_token()
        # Environment variables
        site = config('SITE_AGENDAMIENTO_ECOPETROL')
        sub_site = config('SUBSITE_MEGAS_BULEVAR')
        list_id1 = "1e2054e0-650c-4a95-8203-0ae78b6ee2af"#config('LIST_AUTOAGENDAMIENTO_CITAS_ECOPETROL')
        print(list_id1)
        endpoint_url =f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items'
        headers = {"Authorization": f"Bearer {token}"}

        # Datos a enviar en la solicitud
        item_data = {

                "FechaHoraActual": fecha_hora_actual,
                "Correo": correo,
                "Nombres": nombres,
                "Apellidos": apellidos,
                "TipoIdentificacion": tipo_identificacion,
                "NumeroIdentificacion": numero_identificacion,
                "Ingreso": ingreso

        }
        #return item_data, site, sub_site, list_id, access_token, token

        response = requests.post(endpoint_url, json=item_data, headers=headers)

        if response.status_code == 201:
            new_item_id = response.json().get("id")
            print("Datos escritos en SharePoint con éxito. ID del registro:", new_item_id, item_data)
            return ("Datos escritos en SharePoint con éxito. ID del registro:", new_item_id, item_data)
        else:
            print("Error al escribir en SharePoint. Código de estado:", response.status_code)
            return ("Error al escribir en SharePoint. Código de estado:", response.status_code, response.text, list_id1)

    except Exception as e:
        print("Error durante la operación:", e)
        return ("Error durante la operación:", e)
