# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker
"""

import random

import classes.storage as storage
import classes.file as file

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
        
        free = 0
        counter = 0
            
        while free < size and counter < 50:
            disc = random.choice(self.storage.discs)
            block = random.choice(disc.blocks)
            free = block.storage - block.filled
            counter += 1
                
        if free > size:
            
            defile = file.File(size, block)
            self.storage.files.append(defile)
            disc.files.append(defile)
            block.files.append(defile)
            block.filled += size
    
    def run(self):
        
        for i in range(1000):
            self.action()
            print(self.storage.discs[0].blocks[0].filled)
            
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