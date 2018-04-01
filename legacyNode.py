#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:16:16 2018

@author: Jet
"""

import numpy as np

class legacyNode(radioNode):
    
    def __init__(self, numChans, numSteps, txProb):
        self.actions                  = zeros(1,numChans)
        self.actions(randi(numChans)) = 1
        self.numActions               = size(self.actions,1)
        self.actionTally              = zeros(1,numChans+1)
        self.actionHist               = zeros(numSteps,numChans)
        self.actionHistInd            = zeros(1,numSteps)
        self.txProbability            = txProb
    
    def getAction(self,stepNum):
        if rand <= self.txProbability:
            action = self.actions;  # %  self.actions = zeros(1,numChans);
        else
            action = zeros(1,length(self.actions));

            
        self.actionHist(stepNum,:) = action;
        if ~sum(action):
            self.actionHistInd(stepNum) = 0;
        else
            self.actionHistInd(stepNum) = find(action == 1) + 1;
          
            
        if ~sum(action)
            self.actionTally(1) = self.actionTally(1) + 1;
        else
            self.actionTally(2:end) = self.actionTally(2:end) + action;
          