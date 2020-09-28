# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:10:16 2020

@author: Gebruiker

A class that has the storage for the model. It contains doors and pools, and
files located on the pools.
"""

import classes.pool as pool
import classes.door as door

class Storage:
    
    def __init__(self, npools,ndoors):
        
        self.pools = [pool.Pool() for i in range(npools)]
        self.filled = 0
        self.files = []
        self.doors = [door.Door(self) for i in range(ndoors)]
        self.currenttraffic = []