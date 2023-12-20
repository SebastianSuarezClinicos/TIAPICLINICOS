# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.update_list_controller import uptade_ingreso
from app.Autogestion.models.update_list_model import UpdateListModel

router = APIRouter(prefix='/update_ingreso')

@router.post('/')
async def update_list_router(updateModel: UpdateListModel):
    return await uptade_ingreso(updateModel)
