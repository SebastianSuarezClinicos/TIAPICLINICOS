# -*- coding: utf-8 -*-
'''
Created on Mon Dec 20 2023

@author: Sebastian Suarez
'''

from pydantic import BaseModel

class UpdateListModel(BaseModel):
    ingreso: str
    item_id: str
