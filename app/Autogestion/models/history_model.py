
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

# Import libraries
from pydantic import BaseModel


# Classes
class historyModel(BaseModel):
    tipodeidentificacion: str
    numerodeidentificacion: str