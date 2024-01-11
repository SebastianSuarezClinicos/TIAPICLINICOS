# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023
@author: Sebastian Suarez
'''
from pydantic import BaseModel

class AsignationModel(BaseModel):
    Id: int
    modalidad: str
    nombre: str


class checkAvailabilityModel(BaseModel):
    id_registro: int
