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
        print("hello")
        
    def startWrite(self):
        self.pool, self.speed = self.door.getPool()
        
        
    def startDelete(self):
        print("world")
        
    def Continue(self):
        
        if self.requesttime < 1:
            self.requesttime += 0.1