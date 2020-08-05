# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:33:19 2020

@author: Gebruiker
"""

import random

import classes.file as file

def randomChoice(model,size):
    
    free = 0
    counter = 0
            
    while free < size and counter < 50:
        disc = random.choice(model.storage.discs)
        block = random.choice(disc.blocks)
        free = block.storage - block.filled
        counter += 1
                
    if free > size:
            
        defile = file.File(size, block)
        model.storage.files.append(defile)
        disc.files.append(defile)
        block.files.append(defile)
        block.filled += size
        disc.filled += size
        model.storage.filled += size
    else:
        print("error, file could not be saved")

def mostSpace(model,size):
    
    theDisc = model.storage.discs[0]
    
    for i in range(1,len(model.storage.discs)):
        
        if model.storage.discs[i].filled < theDisc.filled:
            theDisc = model.storage.discs[i]
            
    theBlock = theDisc.blocks[0]
    
    for i in range(1,len(theDisc.blocks)):
        
        if theDisc.blocks[i].filled < theBlock.filled:
            theBlock = theDisc.blocks[i]
            
    
    
    free = theBlock.storage -theBlock.filled
    
    '''
    counter = 0
    while free < size and counter < 50:
        block = random.choice(theDisc.blocks)
        free = block.storage - block.filled
        counter += 1
    '''
    if free > size:
        defile = file.File(size,theBlock)
        model.storage.files.append(defile)
        theDisc.files.append(defile)
        theBlock.files.append(defile)
        theBlock.filled += size
        theDisc.filled += size
        model.storage.filled += size
    else:
        print("error, file could not be saved")
        

def lowWorkload():
    
    return True

def aveWorkload():
    
    return True