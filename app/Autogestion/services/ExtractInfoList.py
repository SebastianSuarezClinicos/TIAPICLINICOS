# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

import httpx
from pydantic import BaseModel

from db.client_graph import get_access_token

class historyModel(BaseModel):
    tipodeidentificacion: str
    numerodeidentificacion: int

async def history_controller(history: historyModel):
    try:
        list_id = '3e83ea1c-2b7d-4376-853b-809e82bce79b'

        token = await get_access_token()

        list_info_url = f'https://graph.microsoft.com/v1.0/sites/root/lists/{list_id}'

        headers = {"Authorization": f"Bearer {token}"}

        response = httpx.get(list_info_url, headers=headers)
        print(list_id)
        if response.status_code == 200:
            list_info = response.json()

            site_id = list_info['parentReference']['siteId']
            subsite_id = list_info['parentReference']['webId']

            print(f'Site ID: {site_id}')
            print(f'Subsite ID: {subsite_id}')
            print(list_id)
        else:
            print(f'Error al obtener información de la lista: {response.status_code} - {response.text}', print(list_id))

    except Exception as e:
        print(f"Error en el controlador: {e}")
