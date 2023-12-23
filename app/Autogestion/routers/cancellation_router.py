# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023

@author: Sebastian Suarez
'''

from fastapi import APIRouter
from app.Autogestion.controllers.cancellation_controller import cancellation_controller
from app.Autogestion.models.cancellation_model import cancellationModel

router = APIRouter(prefix='/appointment-cancellation')

@router.post('/')
async def cancellation_router(cancellationModel: cancellationModel):
    return await cancellation_controller(cancellationModel)