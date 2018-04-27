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
    imDutyPeriod      = 100
    
    def __init__(self, numChans, numSteps, imDutyCircle, imChanIndex):
        self.actions                  = np.zeros(numChans)   # missing ()
        self.actions[ imChanIndex ] = 1
        self.numActions               = np.size(self.actions,0)   # get size; as smiliar as possible  # WARNING
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.imDutyCircle            = imDutyCircle

    
    def getAction(self, stepNum):             
        
        if self.imDutyCircleCount <= self.imDutyCircle * self.imDutyPeriod:
            action = self.actions  
        else:
            action = np.zeros(len(self.actions))   # do nothing rather than choose channel 0            
            if self.imDutyCircleCount >= self.imDutyPeriod:
                self.imDutyCircleCount = 0
        self.imDutyCircleCount += 1
            
        self.actionHist[stepNum,:] = action;  # same synax with matlab   # replace () []
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1    #find
          
            
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        return action
          