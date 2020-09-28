# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:50:48 2020

@author: Gebruiker

The Pool class contains a list of files it contains and also has a memory that
files are temporarily saved in on there way to going to the client or going to
disc.
"""

import classes.memory as memory

class Pool:
    
    def __init__(self):
        self.bandwith = 10.
        self.files = []
        self.space = 10000.
        self.filled = 0
        self.memo = memory.Memory(self)
        
        self.flushing = []