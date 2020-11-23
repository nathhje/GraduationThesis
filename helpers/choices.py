# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:33:19 2020

@author: Gebruiker

There are different ways to choose what disc a file is written to.
randomChoice() chooses a random discs and only checks if there is 
enough space on it. mostSpace() chooses the disc with the most space 
free space.
"""

import random

def randomChoice(storage,size,defile):
    
    free = 0
    counter = 0
            
    while free < size and counter < 500:
        disc = random.choice(storage.discs)
        free = disc.space -disc.filled
        counter += 1
                
    if free > size:
            
        defile.disc = disc
        storage.files.append(defile)
        disc.files.append(defile)
        disc.filled += size
        storage.filled += size
        return disc
    else:
        mostSpace(storage,size,defile)

def mostSpace(storage,size,defile):
    
    thedisc = storage.discs[0]
    
    for i in range(1,len(storage.discs)):
        
        if storage.discs[i].filled < thedisc.filled:
            thedisc = storage.discs[i]
    
    free = thedisc.space -thedisc.filled
    
    if free > size:
        defile.disc = thedisc
        storage.files.append(defile)
        thedisc.files.append(defile)
        thedisc.filled += size
        storage.filled += size
        
        return thedisc
    else:
        print("error, file could not be saved")
        

def lowWorkload():
    
    return True

def aveWorkload():
    
    return True