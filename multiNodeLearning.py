#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:54:27 2018

@author: Jet
"""

import stateSpaceCreate
import numpy as np

# to be wrap in seperate files
def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
    else:
        print "Toc: start time not set"




# Simulation Parameters
numSteps = 30000
numChans = 4
nodeTypes = np.array( [2,2,2,3])
# The type of each node 
#0 - Legacy (Dumb) Node 
#1 - Hopping Node
#2 - MDP Node
#3 - DSA node (just avoids)         
#4 - Adv. MDP Node
legacyTxProb = 1
numNodes = len(nodeTypes)
hiddenNodes = np.array( [0,0,0,0])
exposedNodes = np.array( [0,0,0,0])

if len(hiddenNodes) < numNodes:
    hiddenNodes = np.concatenate( ( hiddenNodes,\
                                   np.zeros(numNodes-len(hiddenNodes)) ), axis=0)

# Initializing Nodes, Observable States, and Possible Actions
nodes =  []
for k in range(0,numNodes):
    if nodeType[k] == 0:
#        t = legacyNode(numChans,numSteps,legacyTxProb)
        pass
    elif nodeType[k] == 1:
#        t = hoppingNode(numChans,numSteps)
        pass
    elif nodeType[k] == 2:
#        t = mdpNode(numChans,states,numSteps)
        pass
    elif nodeType[k] == 3:
#        t = dsaNode(numChans,numSteps,legacyTxProb)
        pass
    else:
#        t = mdpNodeAdvanced(numChans,states,numSteps)
        pass
    t.hidden = hiddenNodes[k]
    t.exposed = exposedNodes[k] 
    nodes.append(t)
        
nodes[0].goodChans = np.array( [1,1,0,0] )        
nodes[1].goodChans = np.array( [0,1,1,0] )          
nodes[2].goodChans = np.array( [0,0,1,1] )    

simulationScenario = scenario(numSteps,'fixed',3)  

# Vector and Matrix Initializations
actions              = np.zeros(numNodes,numChans)
collisions           = np.zeros(1,numNodes)
collisionTally       = np.zeros(numNodes)
collisionHist        = np.zeros(numSteps,numNodes)
cumulativeCollisions = np.zeros(numSteps,numNodes) 

# Main Loops
toc
print "Starting Main Loop"