# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:10:16 2020

@author: Gebruiker
"""

import classes.pool as pool
import classes.door as door

class Storage:
    
    def __init__(self, npools):
        
        self.pools = [pool.Pool() for i in range(npools)]
        self.filled = 0
        self.files = []
        self.doors = [door.Door(self) for i in range(self.ndoors)]
        self.currenttraffic = []