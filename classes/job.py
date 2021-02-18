# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:12:03 2020

@author: Gebruiker

This file contains the job class. It initiates a read, write or delete file
and asks its associated door for location information. The Continue() function
progresses the job one timestep. When the job is done, it is deleted from the 
list of active jobs.
"""

import random

import classes.file as file

class Job:
    
    def __init__(self,door,thetype):
        
        self.id = -5
        self.thetype = thetype
        self.filename = 0
        self.size = 0
        self.door = door
        self.speed = 0
        self.loadspeed = 0
        self.inmemory = 0
        self.complete = 0
        self.disc = 0
        self.requesttime = 0
        self.speedhistory = []
        self.time = []
        self.ended = False
        self.sourcejob = thetype
        
        self.futureStart()
        
    def randomStart(self):
        
        if self.thetype == "read":
            self.startRead()
            
        if self.thetype == "write":
            self.startWrite()
            
        if self.thetype == "delete":
            self.startDelete()
    
    def futureStart(self):
        #print(self.thetype)
        self.size = self.thetype['size']
        
        self.filename = file.File(self.thetype)
        self.disc = self.thetype['domain']
        
        if self.thetype['isWrite']=='read':
            self.speed, self.loadspeed = self.door.readSpeed(self.disc)
        elif self.thetype['isWrite']=='write':
            self.speed = self.door.writeSpeed(self.disc)
            
        self.thetype = self.thetype['isWrite']
        
        self.disc.activejobs.append(self)
            
    def startRead(self):
        
        self.filename, self.disc, self.speed, self.loadspeed = self.door.locatedisc()
        self.size = self.filename.size
        
        #self.disc.activejobs.append(self)
        
    def startWrite(self):
        
        self.size = random.random()*10000.
        self.filename = file.File(self.size)
        self.disc,self.speed = self.door.getdisc(self.size,self.filename)
        
        #self.disc.activejobs.append(self)
        
    def startDelete(self):
        self.filename, self.disc = self.door.deletedisc()
        
        #self.disc.activejobs.append(self)
        
    def Continue(self):
        
        if self.thetype == "write":
            self.writeContinue()
            
        if self.thetype == "read":
            self.readContinue()
            
        if self.thetype == "delete":
            self.deleteContinue()
        
    
    def writeContinue(self):
        
        memo = self.disc.memo
        
        if memo.blocked == False:
            self.complete += self.speed
            self.disc.memo.filled += self.speed
        if self.complete > self.size:
            self.disc.memo.filled -= self.complete - self.size
            self.End()
                
    def readContinue(self):
        
        memo = self.disc.memo
            
        if self.complete < self.size and memo.blocked == False:
            self.complete += self.loadspeed
            self.inmemory += self.loadspeed
            self.disc.memo.readused += self.loadspeed
            
        if self.inmemory > self.speed:
            self.inmemory -= self.speed
            memo.readused -= self.speed
        else:
            memo.readused -= self.inmemory
            self.inmemory = 0
                
        if self.complete > self.size and self.inmemory == 0:
            self.End()
                
    def deleteContinue(self):
           
        self.requesttime += 0.1
            
        greenlight = self.door.checkDelete(self.disc)
            
        if greenlight == True or self.requesttime > 3:
            self.disc.files.remove(self.filename)
            self.End()
                
    def End(self):
        
        self.door.closeJob(self)
        self.ended = True