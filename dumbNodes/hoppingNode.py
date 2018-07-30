#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:05:07 2018

@author: Jet
"""

import numpy as np
import random
from radioNode import radioNode


class hoppingNode(radioNode):
    hopRate = [ ]  
    hopPattern = [ ]
    hopIndex = 0  
    def __init__(self, numChans, numSteps, HoppingChanIndex, hopRate):
        
        self.numActions    = len(HoppingChanIndex)  
        self.actions       = np.zeros((self.numActions,numChans) )
        for i in range(self.numActions):
            self.actions[i,HoppingChanIndex[i]] = 1
            
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        
        self.hopRate       = hopRate  # hop rate, the freq it decide to hop next channel
        self.hopPattern    = HoppingChanIndex
        
        self.type = "hopping"
        
    def  getAction(self,stepNum):
        if not np.fmod(stepNum,self.hopRate):
            self.hopIndex +=  1
            if self.hopIndex >= len(self.hopPattern):
                self.hopIndex = 0  # roll over
                
        action = self.actions[self.hopIndex,:]
        
        self.actionHist[stepNum,:] = action

        self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1
        
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[1] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        
        return action
        
               