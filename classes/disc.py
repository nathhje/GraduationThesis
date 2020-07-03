# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:03:14 2020

@author: 
"""

import classes.block as block

class Disc:
    
    def __init__(self,nblocks):
        self.blocks = []
        self.blocks.append(block.Block())
        self.bandwith = 1