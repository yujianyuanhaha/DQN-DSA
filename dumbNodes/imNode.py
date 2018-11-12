#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:16:16 2018

@author: Jet
"""

import numpy as np
import random
from radioNode import radioNode

class imNode(radioNode):
    
#    imDutyCircleCount = 0
#    imDutyPeriod      = 100
    
    def __init__(self, numChans, numSteps, imPeriod ,imDutyCircle, imChanIndex):
        self.actions                  = np.zeros(numChans)
        self.OFF                      = np.zeros(numChans)  
        self.actions[ imChanIndex ]   = 1
        self.ON                      = self.actions
         
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.imDutyPeriod             = imPeriod
        self.imDutyCircle             = imDutyCircle
        self.type                     = "im"
        self.hyperType                = "dumb" 
        "-- swith means when (the percentage of period) to make a flip"
        self.switch                   = np.zeros(len(self.imDutyCircle)+1)
        self.switch[0]                = 0                   
        for i in range(len(self.imDutyCircle)):
            self.switch[i+1] = self.imDutyCircle[i] * self.imDutyPeriod 

    
    def getAction(self, stepNum): 

#        mode = "dutyCycle"
        mode = "onOFF"
        onDuration = 5
        offDuration = 2
            
                    
        if stepNum > 0:
            if mode == "dutyCycle":
                if  stepNum % self.imDutyPeriod in self.switch:
                    # do the 'flip' when meet the switch point
                    if (self.actionHist[stepNum-1,:]).any():   # previous is ON
                        action = self.OFF
                    else:
                        action = self.ON
                else:
                    action = self.actionHist[stepNum-1,:]   
            elif mode == "onOFF":
                if stepNum % (onDuration + offDuration) < onDuration:
                    action = self.ON
                else:
                    action = self.OFF
                    
                
                    
        else:
            action = self.ON
            
            
        
        
#        self.imDutyCircleCount += 1
            
        self.actionHist[stepNum,:] = action
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1             
            
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        return action
          
    
# ToDo, write test unit    