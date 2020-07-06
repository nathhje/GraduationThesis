# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker
"""

import random

import classes.storage as storage

class Model:
    
    def __init__(self):
        
        ndiscs = 2
        
        self.storage = storage.Storage(ndiscs)
    
    def run(self):
        
        for i in range(1000):
            self.action()
            
    def action(self):
        
        rand = random.random()
        
        if rand<0.4:
            self.read()
        elif rand<0.8:
            self.write()
        else:
            self.delete()
            
    def read(self):
        print("hello")
        
    def write(self):
        print("world")
        
    def delete(self):
        print("slashn")