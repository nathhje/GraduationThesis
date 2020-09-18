# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:50:48 2020

@author: Gebruiker
"""

import classes.memory as memory

class Pool:
    
    def __init__(self):
        self.bandwith = 10.
        self.files = []
        self.space = 10000.
        self.filled = 0
        self.memo = memory.Memory(self)
        