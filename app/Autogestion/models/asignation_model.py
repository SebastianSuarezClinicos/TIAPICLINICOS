
# -*- coding: utf-8 -*-
'''
#Created on Mon Dec 22 2023

#@author: Sebastian Suarez
'''
from pydantic import BaseModel

class asignationModel(BaseModel):
    id_registro: int
    tipodeidentificacion: str
    numerodeidentificacion: str
    correo: str

class checkAvailabilityModel(BaseModel):
    id_registro: int