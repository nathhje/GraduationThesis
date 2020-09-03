# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:12:03 2020

@author: Gebruiker
"""

class Job:
    
    def __init__(self,door,thetype,filename,size):
        
        self.thetype = thetype
        self.filename = filename
        self.size = size
        self.door = door
        self.speed = 0
        self.loadspeed = 0
        self.loaded = 0
        self.inmemory = 0
        self.complete = 0
        self.pool = 0
        self.requesttime = 0
        
        if self.thetype == "read":
            self.startRead()
            
        if self.thetype == "write":
            self.startWrite()
            
        if self.thetype == "delete":
            self.startDelete
            
    def startRead(self):
        self.pool, self.speed, self.loadspeed = self.door.locatePool(self.filename)
        
    def startWrite(self):
        self.pool,self.speed = self.door.getPool(self.size,self.filename)
        
        
    def startDelete(self):
        self.pool = self.door.deletePool(self.filename)
        
    def Continue(self):
        
        if self.thetype == "write":
            self.writeContinue()
            
        if self.thetype == "read":
            self.readContinue()
            
        if self.thetype == "delete":
            self.deleteContinue()
        
    
    def writeContinue(self):
        
        if self.requesttime < 1:
            self.requesttime += 0.1
            
        else:
            self.complete += self.speed
            self.pool.memo.filled += self.speed
            if self.complete > self.size:
                self.End()
                
    def readContinue(self):
        
        if self.requesttime < 1:
            self.requesttime += 0.1
            
        else:
            if self.loaded < self.size:
                self.loaded += self.loadspeed
                self.inmemory += self.loadspeed
                self.pool.memo.readused += self.loadspeed
            
            if self.inmemory > self.speed:
                self.inmemory -= self.speed
                self.pool.memo.readused -= self.speed
            else:
                self.pool.memo.readused -= self.inmemory
                self.inmemory = 0
                
            if self.loaded > self.size and self.inmemory == 0:
                self.End()
                
    def deleteContinue(self):
        
        if self.requesttime < 1:
            self.requesttime += 0.1
            
        else:
            self.requesttime += 0.1
            
            greenlight = self.door.checkDelete(self.pool)
            
            if greenlight == True or self.requesttime > 3:
                self.pool.files.remove(self.filename)
                self.End(self)
                
    def End(self):
        
        self.door.closeJob(self)