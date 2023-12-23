# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.history_controller import history_controller
from app.Autogestion.models.history_model import historyModel

router = APIRouter(prefix='/history')

@router.post('/')
async def history_router(history: historyModel):
    return await history_controller(history)
