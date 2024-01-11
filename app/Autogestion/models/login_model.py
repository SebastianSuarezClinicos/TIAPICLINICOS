# -*- coding: utf-8 -*-
'''
Created on Mon Dec 22 2023
@author: Sebastian Suarez
'''

# Import libraries
from pydantic import BaseModel


# Classes
class loginModel(BaseModel):
  tipodeidentificacion: str
  numerodeidentificacion: str
  correo: str

class verificationModel(BaseModel):
  correo: str

