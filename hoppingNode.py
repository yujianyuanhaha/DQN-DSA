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
    hopRate = [ ]   #must, else error
    hopPattern = [ ]
    hopIndex = 0  # TODO we start from zero
    def __init__(self, numChans, numSteps, HoppingChanIndex):
 #       self.actions       = np.zeros((2,numChans) )      # TODO # matrix than vector, fix than random
#        self.actions[1,2]  = 1   # actions(sequence, channel)
    #    self.actions[2,4]  = 1
    #    self.actions[3,6]  = 1
    #    self.actions[4,8]  = 1
    #    self.actions[5,10] = 1  #TODO
        
        self.numActions    = len(HoppingChanIndex)  # damn, to
        self.actions       = np.zeros((self.numActions,numChans) )
        for i in range(self.numActions):
            self.actions[i,HoppingChanIndex[i]] = 1
            
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        
        self.hopRate       = 1    # hop rate, the freq it decide to hop next channel
#        self.hopPattern    = np.array( [0,1])   # we hop only two here #TODO
        self.hopPattern    = HoppingChanIndex
        
    def  getAction(self,stepNum):
        if not np.fmod(stepNum,self.hopRate):
            self.hopIndex +=  1
            if self.hopIndex >= len(self.hopPattern):
                self.hopIndex = 0  # roll over, what if fully understand at once
        action = self.actions[self.hopIndex,:]
        
        self.actionHist[stepNum,:] = action

        self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1
        
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[1] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        
        # easy  -- same for DSA, adv
        return action
        
               