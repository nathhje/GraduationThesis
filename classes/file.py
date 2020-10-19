# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:42:51 2020

@author: Gebruiker

A file class that can be saved on a disc.
"""

class File:
    
    def __init__(self,size):
        self.size = size
        self.disc = False