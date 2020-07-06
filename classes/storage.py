# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:10:16 2020

@author: Gebruiker
"""

import classes.disc as disc

class Storage:
    
    def __init__(self, ndiscs):
        
        self.nblocks = 2
        self.discs = []
        self.discs.append(disc.Disc(self.nblocks))