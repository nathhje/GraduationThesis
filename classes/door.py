# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker
"""

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        
    def getPool(storage,size):
        choices.mostSpace(storage,size)