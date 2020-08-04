# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:07:35 2020

@author: Gebruiker
"""

class Block:
    
    def __init__(self,disc):
        
        self.storage = 1
        self.filled = 0
        self.pdisc = disc
        self.files = []