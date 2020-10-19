# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:10:16 2020

@author: Gebruiker

A class that has the storage for the model. It contains doors and discs, and
files located on the discs.
"""

import classes.disc as disc
import classes.door as door

class Storage:
    
    def __init__(self, ndiscs,ndoors):
        
        self.discs = [disc.Disc() for i in range(ndiscs)]
        self.filled = 0
        self.files = []
        self.doors = [door.Door(self) for i in range(ndoors)]
        self.currenttraffic = []
        self.futurelist = []