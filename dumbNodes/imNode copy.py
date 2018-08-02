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
    
    imDutyCircleCount = 0
#    imDutyPeriod      = 100
    
    def __init__(self, numChans, numSteps, imPeriod ,imDutyCircle, imChanIndex):
        self.actions                  = np.zeros(numChans)  
        self.actions[ imChanIndex ] = 1
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.imDutyPeriod             = imPeriod
        self.imDutyCircle             = imDutyCircle
        self.type = "im"

    
    def getAction(self, stepNum):             
        
        if self.imDutyCircleCount <= self.imDutyCircle * self.imDutyPeriod:
            action = self.actions  
        else:
            action = np.zeros(len(self.actions))   # choose channel 0            
            if self.imDutyCircleCount >= self.imDutyPeriod:
                self.imDutyCircleCount = 0
        self.imDutyCircleCount += 1
            
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
          