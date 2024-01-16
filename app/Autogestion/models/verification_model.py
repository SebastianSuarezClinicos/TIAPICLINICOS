# -*- coding: utf-8 -*-
'''
Created on Mon Dec 18 2023

@author:Sebastian Suarez
'''
from pydantic import BaseModel

class VerificationModel(BaseModel):
    codigo: str
    token: str
