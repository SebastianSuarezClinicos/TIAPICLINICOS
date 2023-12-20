# -*- coding: utf-8 -*-
'''
Created on Mon Dec 19 2023

@author:Sebastian Suarez
'''

from decouple import config
import requests
from datetime import datetime, timedelta

from db.client_graph import get_access_token


# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id1 = config('LIST_AUTOAGENDAMIENTO_GESTION_ECOPETROL')

async def write_list(access_token, correo, nombres, apellidos, tipo_identificacion, numero_identificacion, ingreso):
    try:
        fecha_hora_actual = datetime.utcnow().isoformat()+"Z"
        numero_identificacion = int(numero_identificacion)
        token = await get_access_token()

        #print(list_id1)
        endpoint_url =f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items'
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
        #return item_data, site, sub_site, list_id, access_token, token

        response = requests.post(endpoint_url, json=item_data, headers=headers)

        if response.status_code == 201:
            item_id = response.json().get("id")
            #print("Datos escritos en SharePoint con éxito. ID del registro:", new_item_id, item_data)
            return (ingreso, item_id)
        else:
            print("Error al escribir en SharePoint. Código de estado:", response.status_code)
            return ("Error al escribir en SharePoint. Código de estado:", response.status_code, response.text,)

    except Exception as e:
        print("Error durante la operación:", e)
        return ("Error durante la operación:", e)

item_id = "2"
async def uptade_ingreso(ingreso, item_id):
    try:
        token = await get_access_token()

        endpoint_url =f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id1}/items'
        headers = {"Authorization": f"Bearer {token}"}

        # Datos a enviar en la solicitud
        item_data = {
            "fields": {
                "Ingreso": ingreso
            }
        }
        #return item_data, site, sub_site, list_id, access_token, token

        response = requests.patch(endpoint_url, json=item_data, headers=headers)

        if response.status_code == 201:
            new_item_id = response.json().get("id")
            #print("Datos escritos en SharePoint con éxito. ID del registro:", new_item_id, item_data)
            return (new_item_id)
        else:
            print("Error al escribir en SharePoint. Código de estado:", response.status_code)
            return ("Error al escribir en SharePoint. Código de estado:", response.status_code, response.text,)

    except Exception as e:
        print("Error durante la operación:", e)
        return ("Error durante la operación:", e)