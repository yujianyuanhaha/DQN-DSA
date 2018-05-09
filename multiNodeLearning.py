#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:54:27 2018

@author: Jet

jianyuan@vt.edu

April,2018

The main script to run

---------------------------
Github url:
       https://github.com/yujianyuanhaha/DQN-DSA 




---------------------------
File Achitecture:

    multiNodeLearning.py -- network.config
                         -- myFunction.py
                         -- legacyNode.py
                         -- hoppingNode.py
                         -- imNode.py
                         -- dsaNode.py
                         -- mdpNode.py      -- mdp.py
                         -- dqnNode.py      -- dqn.py
                                            -- dqnDouble.py
                                            -- dqnPriReplay.py
                                            -- dqnDuel.py 
                         
                         -- stateSpaceCreate.py
                         -- scenario.py
                     
----------------------------                     
Main Configuration:  
1. assignment of array "nodeTypes"  "legacyChanList"  "hoppingChanList"
                        



"""


import numpy as np
import math

from stateSpaceCreate import stateSpaceCreate
#from radioNode   import radioNode
from legacyNode  import legacyNode
from mdpNode     import mdpNode
from hoppingNode import hoppingNode
from dqnNode     import dqnNode   #
from dsaNode     import dsaNode 
from imNode     import imNode 

from scenario    import scenario
import matplotlib.pyplot as plt
import time
import random
from myFunction import channelAssignment, myPlot,\
     myPlotCollision, myPlotReward, myPlotAction,\
     myPlotOccupiedEnd, myPlotOccupiedAll,\
     myPlotPER, myPlotPLR
     





# for unknown reason, terminal of Spyder would keep the old tensorflow neural network data
# when change numChans(related to neural network), REMEMBER TO SHUT OFF AND OPEN A NEW terminal
# it would not happen in raw terminal 

################################################################
#######################     Network Setup & Simulation Parameters  ############

# recommend to load configuration from "setup.config" file


#numSteps = 30000
#numChans = 4 
#ChannelAssignType = 'typeIn'  

#nodeTypes = np.array( [0 ,1 ,0 ,5])
#legacyChanList = [0,1]
#hoppingChanList = [ [2,3]]

import ConfigParser
import json
Config = ConfigParser.ConfigParser()
Config.read("setup.config")     
numSteps          =  json.loads( Config.get('Networks', 'numSteps'))                  
numChans          =  json.loads( Config.get('Networks', 'numChans'))  
ChannelAssignType =  Config.get('Networks', 'ChannelAssignType')    
nodeTypes         =  np.asarray(  json.loads(Config.get('Networks', 'nodeTypes')))

legacyChanList    =  json.loads(Config.get('Networks', 'legacyChanList'))  
txProbability     =  json.loads(Config.get('Networks', 'txProbability'))  
hoppingChanList   =  json.loads(Config.get('Networks', 'hoppingChanList'))
hopRate           =  json.loads( Config.get('Networks', 'hopRate'))  
hoppingWidth      =  json.loads( Config.get('Networks', 'hoppingWidth'))  
imChanList        =  json.loads(Config.get('Networks', 'imChanList')) 
imDutyCircleList  =  json.loads(Config.get('Networks', 'imDutyCircleList')) 

#nodeTypes = np.array( [0,0,0,0,
#                       0,0,1,1,
#                       2,2,3,3,
#                       5,5,5,5] )                    
#legacyChanList = [3,4,5,6,8,9]
#hoppingChanList = [ [11,12],[12,13]]  
         
print nodeTypes                 
numNodes = len(nodeTypes)

hiddenDuplexCollision = np.zeros((numNodes,numNodes))
#hiddenDuplexCollision[2,3] = 1
#hiddenDuplexCollision[3,2] = 1

exposedSpatialReuse = np.zeros((numNodes,numNodes))
#exposedSpatialReuse[3,4] = 1
#exposedSpatialReuse[4,3] = 1

#if len(hiddenNodes) < numNodes:
#    hiddenNodes = np.concatenate( ( hiddenNodes,\
#                                   np.zeros(numNodes-len(hiddenNodes)) ), axis=0)

isWait = False  #default no imNode
if any(nodeTypes==2) and len(nodeTypes) > numChans:
    isWait = True
    print "learn to occupy imNode"
# if need to learn imNode, enable isWait to change rewards 
    
# The type of each node 
# 0 - Legacy (Dumb) Node 
# 1 - Hopping Node
# 2 - Intermittent Node/ im Node
# 3 - DSA node (just avoids)  
# 4 - MDP Node
# 5 - a. DQN Node
# 6 - b. DQN-DoubleQ
# 7 - c. DQN-PriReplay
# 8 - d. DQN-Duel     
# 6 - Adv. MDP Node

# the order does not matter for dsa, dqn, mdp make action
# we even allow several DSA coexsit
                                
################################################################
################################################################
if ChannelAssignType == 'random':
    legacyChanList, imChanList, hoppingChanList, utilization =\
        channelAssignment(nodeTypes, hoppingWidth, numChans)
elif ChannelAssignType == 'case1':
    "0-2 legacy,0-2 hopping"
    legacyChanList = [0,1,2,3]
    hoppingChanList = [ [2,3],[3,2]]
elif ChannelAssignType == 'case2':
    "0-4 legacy, 0-3 hopping"
    legacyChanList = [0,1,2,3]
    hoppingChanList = [ [4,5,6],[5,6,4],[6,5,4]]
else:
    pass



# Initializing Nodes, Observable States, and Possible Actions
nodes =  []
states = stateSpaceCreate(numChans)
numStates = np.shape(states)[0]
CountLegacyChanIndex = 0
CountHoppingChanIndex = 0
CountIm = 0
##################### Construct diff Type of Nodes #######################################
for k in range(0,numNodes):
    if   nodeTypes[k] == 0:
        t = legacyNode(numChans,numSteps, txProbability[CountLegacyChanIndex], legacyChanList[CountLegacyChanIndex]) 
        CountLegacyChanIndex += 1               
    elif nodeTypes[k] == 1:
        t = hoppingNode(numChans,numSteps,hoppingChanList[CountHoppingChanIndex],hopRate)
        CountHoppingChanIndex += 1
    elif nodeTypes[k] == 2:
        t = imNode(numChans,numSteps,imDutyCircleList[CountIm], imChanList[CountIm])
        CountIm += 1
    elif nodeTypes[k] == 3:
        t = dsaNode(numChans,numSteps,txProbability)    
    elif nodeTypes[k] == 4:
        t = mdpNode(numChans,states,numSteps)   
    elif nodeTypes[k] >= 5 and nodeTypes[k] <= 8:
        t = dqnNode(numChans,states,numSteps, nodeTypes[k])      # dqnNode
    else:
        pass
    t.hiddenDuplexCollision = hiddenDuplexCollision[k]
    t.exposedSpatialReuse   = exposedSpatialReuse[k]

    nodes.append(t)
        
#nodes[2].goodChans = np.array( [0,0,0,1] )        
#nodes[1].goodChans = np.array( [0,1,1,0] )          
#nodes[2].goodChans = np.array( [0,0,1,1] ) 
    
      
simulationScenario = scenario(numSteps,'fixed',3)  

# Vector and Matrix Initializations
actions              = np.zeros((numNodes,numChans))
collisions           = np.zeros(numNodes)
collisionTally       = np.zeros((numNodes,numNodes))  #TODO
collisionHist        = np.zeros((numSteps,numNodes))
cumulativeCollisions = np.zeros((numSteps,numNodes)) 


mdpLearnTime = np.zeros(numSteps)
dqnLearnTime = np.zeros(numSteps)
##################### MAIN LOOP BEGIN ############################################
tic = time.time()
ticMdpAction = [ ]
ticDqnAction = [ ]
print "Starting Main Loop"

legacyNodeIndicies = []
for n in range(0,numNodes):
    if isinstance(nodes[n],legacyNode):
        legacyNodeIndicies.append(n)
        
if (simulationScenario.scenarioType != 'fixed') and legacyNodeIndicies:
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies)  


learnProbHist = [ ]

#countLearnHist = np.zeros(numSteps);
observedStates = np.zeros((numNodes,numChans))
for s in range(0,numSteps):
    
    #Determination of next action for each node
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode):
            ticDqnAction  = time.time()
            observation = observedStates[n,:]
            actions[n,:], actionScalar = nodes[n].getAction(s, observation)  ###########
#            if not np.sum(actions[n,:] ):
#                print "dqnNode WAIT"
            tocDqnAction  = time.time()
        elif isinstance(nodes[n],mdpNode):
            ticMdpAction  = time.time()
            actions[n,:] = nodes[n].getAction(s)
            tocMdpAction  = time.time()
        else:    
            actions[n,:] = nodes[n].getAction(s)
        assert not any(np.isnan(actions[n,:])), "ERROR! action is Nan"


    if simulationScenario.scenarioType != 'fixed':
         simulationScenario.updateScenario(nodes,legacyNodeIndicies, s)

    # Determining observations, collisions, rewards, and policies (where applicable)
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if n != nn:
                # case 1, duplex collision
                if nodes[nn].hiddenDuplexCollision[n]:
                    if  np.sum( actions[n,:] + actions[nn,:])> 1:
                        collisions[n]         = 1
                        collisionTally[n,nn] += 1
                        observedStates[n,:]   = np.ones(numChans)   # all illegal 
                        # think duplex col node as "full channel user", only have to is wait
                       # print "duplex collision"                                  
                else:
                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)   # partial obseravtion
                        
                # case 2, same channel collision                        
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
                  and not nodes[nn].exposedSpatialReuse[n]:    # if nodes[nn].exposedSpatialReuse[n] == 0
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                      
                    
        if isinstance(nodes[n],dsaNode):
            nodes[n].updateState(observedStates[n,:],s)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],s,isWait)
            nodes[n].updateTrans(observedStates[n,:],s)
            if not math.fmod(s,nodes[n].policyAdjustRate):
                nodes[n].updatePolicy(s)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n],s, isWait)
            observation_ = observedStates[n,:]  # update already # full already
            done = True            
            nodes[n].storeTransition(observation, actionScalar, 
                 reward, observation_)
            if s > 200 and s % 5 == 0:    # step 2 trade in more computation for better performance
                nodes[n].learn()
                learnProbHist.append( nodes[n].dqn_.exploreProb)
            tocDqnLearn = time.time()
            # original  action -> step() -> observation_, reward, done
            # 1. action -> collisions
            # 2. collisions -> getReward() -> observation_, reward, done
    collisionHist[s,:]        = collisions
    cumulativeCollisions[s,:] = collisions
    if s != 0:
        cumulativeCollisions[s,:] +=  cumulativeCollisions[s-1,:]
    
    if ticMdpAction:
        mdpLearnTime[s] = tocMdpAction - ticMdpAction + tocMdpLearn - ticMdpLearn
    if ticDqnAction:
        dqnLearnTime[s] = tocDqnAction - ticDqnAction + tocDqnLearn - ticDqnLearn
          
print "End Main Loop"
toc =  time.time()
print "--- %s seconds ---" %(toc - tic)


##################### PLOT ############################################ 
import os
if not os.path.exists('../dqnFig'):
    os.makedirs('../dqnFig') 
    
#myPlot(nodes, numChans, numSteps, learnProbHist,cumulativeCollisions)
myPlotProb(learnProbHist)
txPackets = myPlotCollision(nodes, cumulativeCollisions)
myPlotReward(nodes, cumulativeCollisions)
myPlotAction(nodes, numChans)    
myPlotOccupiedEnd(nodes, numChans, plotPeriod = 100)
myPlotOccupiedAll(nodes, numChans)
PLR = myPlotPER(nodes, numSteps, txPackets, cumulativeCollisions)    
myPlotPLR(nodes, PLR)    
    
    
    
