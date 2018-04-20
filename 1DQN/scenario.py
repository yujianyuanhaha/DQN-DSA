#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:06:32 2018

@author: Jet
"""
import math

class scenario:
    numSteps = [ ]
    scenarioType = [ ]
    numIntervals = [ ]
    intervalSize = [ ]
    
    def __init__(self,numSteps,scenarioType,numIntervals):
        self.numSteps     = numSteps
        self.numIntervals = numIntervals
        self.scenarioType = scenarioType
        self.intervalSize = numSteps/numIntervals
        
    def initializeScenario(self,nodes,indicies):
        numNodes = len(indicies)   
        for i in range(0,numNodes):
            nodes[indicies(i)-1].txProbability = 0   # how to get access to node
            # notice -1 or not, to be debugged

    def updateScenario(self,nodes, indicies, steptime):
        numNodes = len(indicies)          
        if self.scenarioType == 'ncorn':
            currentInterval = math.floor(steptime/self.intervalSize)
            if steptime > self.numSteps * (self.numIntervals-1) / self.numIntervals:
                currentInterval = self.numIntervals                    
            for i in range(0,numNodes):
                nodes[indicies(i)-1].txProbability = currentInterval/self.numIntervals        # -j ??                       
        elif self.scenarioType   == 'fixed':   #% nothing in fixed
            pass # todo                    
        else: 
            print "scenario.Type is unknown"