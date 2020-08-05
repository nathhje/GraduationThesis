# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker
"""

import random

import classes.storage as storage
import classes.file as file
import helpers.choices as choices

class Model:
    
    def __init__(self):
        
        self.ndiscs = 2
        
        self.storage = storage.Storage(self.ndiscs)
        
        self.setup()
    
    def setup(self):
        
        for i in range(random.randint(10,100)):
            size = random.random()/100.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        choices.mostSpace(self,size)
        
    
    def run(self):
        
        for i in range(1000):
            self.action()
            print(self.storage.discs[0].blocks[0].filled)
            print(self.storage.discs[0].filled)
            print(self.storage.filled)
            
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            self.read()
        elif rand<0.92:
            self.write()
        else:
            self.delete()
            
    def read(self):
        print("read")
        rfile = random.choice(self.storage.files)
        
    def write(self):
        print("write")
        size = random.random()/100.
        self.placeFile(size)
        
    def delete(self):
        print("delete")
        dfile = random.choice(self.storage.files)
        dfile.block.files.remove(dfile)
        dfile.block.pdisc.files.remove(dfile)
        self.storage.files.remove(dfile)
        dfile.block.filled -= dfile.size