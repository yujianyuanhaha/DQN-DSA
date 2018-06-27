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

    multiNodeLearning.py -- setup.config
                         -- myFunction.py
                         -- legacyNode.py
                         -- hoppingNode.py
                         -- imNode.py
                         -- dsaNode.py
                         -- poissonNode.py
                         
                         -- mdpNode.py      -- mdp.py
                         
                         -- dqnNode.py      -- dqn.py
                                            -- dqnDouble.py
                                            -- dqnPriReplay.py
                                            -- dqnDuel.py 
                                            -- dqnR.py
                                            -- dpq.py 
                                            
                         -- acNode.py       -- actor.py                         
                                            -- critic.py
                                            
                         -- ddpgNode.py     -- ddpg.py
                                            
                                            
                         -- stateSpaceCreate.py
                         -- scenario.py
                     
----------------------------                     
Main Configuration:  
1. assignment of array "nodeTypes"  "legacyChanList"  "hoppingChanList"
2. description seen in setup.config file
                        






"""


import numpy as np
import math
import random

from stateSpaceCreate import stateSpaceCreate
#from radioNode   import radioNode
from dumbNodes.legacyNode  import legacyNode
from dumbNodes.hoppingNode import hoppingNode
from dumbNodes.imNode      import imNode 
from dumbNodes.dsaNode     import dsaNode 
from dumbNodes.poissonNode import poissonNode

from learningNodes.mdpNode     import mdpNode
from learningNodes.dqnNode     import dqnNode   #
from learningNodes.acNode      import acNode
#from learningNodes.ddpgNode    import ddpgNode 

from scenario    import scenario
import matplotlib.pyplot as plt
import time

from myFunction import channelAssignment, \
     myPlotProb,\
     myPlotCollision, myPlotReward, myPlotAction,\
     myPlotOccupiedEnd, myPlotOccupiedAll,\
     myPlotPER, myPlotPLR, myPlotCost
     





# for unknown reason, terminal of Spyder would keep the old tensorflow neural network data
# when change numChans(related to neural network), REMEMBER TO SHUT OFF AND OPEN A NEW terminal
# it would not happen in raw terminal 

###############################################################################
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
numSteps          =  json.loads( Config.get('Global', 'numSteps'))                  
numChans          =  json.loads( Config.get('Global', 'numChans'))  
ChannelAssignType =  Config.get('Global', 'ChannelAssignType')    
nodeTypes         =  np.asarray(  json.loads(Config.get('Global', 'nodeTypes')))


legacyChanList    =  json.loads(Config.get('legacyNode', 'legacyChanList')) 
txProbability     =  json.loads(Config.get('legacyNode', 'txProbability'))  

hoppingChanList   =  json.loads(Config.get('hoppingNode', 'hoppingChanList'))
hopRate           =  json.loads( Config.get('hoppingNode', 'hopRate'))  
hoppingWidth      =  json.loads( Config.get('hoppingNode', 'hoppingWidth'))  

imPeriod          =  json.loads(Config.get('imNode', 'imPeriod')) 
imChanList        =  json.loads(Config.get('imNode', 'imChanList')) 
imDutyCircleList  =  json.loads(Config.get('imNode', 'imDutyCircleList')) 

poissonChanList   =  json.loads(Config.get('poissonNode', 'poissonChanList')) 
arrivalRate       =  json.loads(Config.get('poissonNode', 'arrivalRate')) 
serviceRate       =  json.loads(Config.get('poissonNode', 'serviceRate')) 

#nodeTypes = np.array( [0,0,0,0,
#                       0,0,1,1,
#                       2,2,3,3,
#                       5,5,5,5] )                    
#legacyChanList = [3,4,5,6,8,9]
#hoppingChanList = [ [11,12],[12,13]]  
             
numNodes = len(nodeTypes)
print "nodeType list: %s"%nodeTypes
print "num of channel: %s        num of nodes: %s"%(numChans, numNodes)

noiseErrorProb = 0.00
noiseFlipNum = 1
if noiseErrorProb > 0.00:
    print "Additive Noise Enabled with Flip Num %s"%noiseFlipNum

PartialObservation = 'False'
poBlockNum = 2
poStepNum = 3
if PartialObservation == 'True':
    print "rollOver Partial Observation Enabled with Blocked Num %s and Step Num %s "%(poBlockNum, poStepNum)


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
    print("learn to occupy imNode")
    

   
    
# if need to learn imNode, enable isWait to change rewards 


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
CountLegacyChanIndex = 0
CountHoppingChanIndex = 0
CountIm = 0
##################### Construct diff Type of Nodes #######################################
for k in range(0,numNodes):
    if   nodeTypes[k] == 0 or nodeTypes[k] == 'legacy':
        t = legacyNode(numChans,numSteps, txProbability[CountLegacyChanIndex], legacyChanList[CountLegacyChanIndex]) 
        CountLegacyChanIndex += 1               
    elif nodeTypes[k] == 1  or nodeTypes[k] == 'hopping':
        t = hoppingNode(numChans,numSteps,hoppingChanList[CountHoppingChanIndex],hopRate)
        CountHoppingChanIndex += 1
    elif nodeTypes[k] == 2 or nodeTypes[k] == 'im':
        t = imNode(numChans,numSteps,imPeriod, imDutyCircleList[CountIm], imChanList[CountIm])
        CountIm += 1
    elif nodeTypes[k] == 3  or nodeTypes[k] == 'dsa':
        t = dsaNode(numChans,numSteps,txProbability)    
    elif nodeTypes[k] == 4  or nodeTypes[k] == 'possion':
        t = poissonNode( numChans, numSteps, poissonChanList, arrivalRate, serviceRate)
    elif nodeTypes[k] == 10:
        t = mdpNode(numChans,states,numSteps)   
    elif (nodeTypes[k] >= 11 and nodeTypes[k] <= 16) \
                    or nodeTypes[k] == 'dqn'          or nodeTypes[k] == 'dqnDouble' \
                    or nodeTypes[k] == 'dqnPriReplay' or nodeTypes[k] == 'dqnDuel'   \
                    or nodeTypes[k] == 'dqnRef'       or nodeTypes[k] == 'dpg':
                    
        t = dqnNode(numChans,states,numSteps, nodeTypes[k])      
        # dqnNode, temporary asyn
        t.policyAdjustRate = random.randint(5, 9)
#        t.policyAdjustRate = 5
#        print "DQN node %s Parameters: learning_rate %s, reward_decay %s,\
#                replace_target_iter %s, memory_size %s,\
#                policyAdjustRate %s" %(k, t.dqn_.lr, t.dqn_.gamma,              
#                    t.dqn_.replace_target_iter, t.dqn_.memory_size, t.policyAdjustRate )
    elif nodeTypes[k] == 17 or nodeTypes[k] == 'ac':
        t = acNode(numChans,states,numSteps) 
        
    #ßelif nodeTypes[k] == 18 or nodeTypes[k] == 'ddpg':
    #    t = ddpgNode(numChans,states,numSteps)     
        

    else:
        pass
    t.hiddenDuplexCollision = hiddenDuplexCollision[k]
    t.exposedSpatialReuse   = exposedSpatialReuse[k]

    nodes.append(t)
    
print nodes

#confirmKey = raw_input("If setting is ready, press ENTER to continue, any other key to abort ... ") 
#assert confirmKey == '', "setting wrong, programs abort :("
        
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
print("--- Starting Main Loop ---")

legacyNodeIndicies = []
for n in range(0,numNodes):
    if isinstance(nodes[n],legacyNode):
        legacyNodeIndicies.append(n)
        
if (simulationScenario.scenarioType != 'fixed') and legacyNodeIndicies:
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies)  


learnProbHist = [ ]

#countLearnHist = np.zeros(numSteps);
observedStates = np.zeros((numNodes,numChans))






for t in range(0,numSteps):
    
    ################ Determination of next action for each node ##############
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode): #or isinstance(nodes[n],ddpgNode) :
            ticDqnAction  = time.time()
            observation = observedStates[n,:]
            actions[n,:], actionScalar = nodes[n].getAction(t, observation)  ###########
#            if not np.sum(actions[n,:] ):
#                print "dqnNode WAIT"
            tocDqnAction  = time.time()
        elif isinstance(nodes[n],mdpNode):
            ticMdpAction  = time.time()
            actions[n,:] = nodes[n].getAction(t)
            tocMdpAction  = time.time()
        else:    
            actions[n,:] = nodes[n].getAction(t)
        assert not any(np.isnan(actions[n,:])), "ERROR! action is Nan"


    if simulationScenario.scenarioType != 'fixed':
         simulationScenario.updateScenario(nodes,legacyNodeIndicies, t)

    ################# Determining observations, collisions, rewards, and policies (where applicable)
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if nn != n:
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
            nodes[n].updateState(observedStates[n,:],t)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],t,isWait)
            # additive noise to flip certain bit of observation
            temp = observedStates[n,:]
            if random.random() < noiseErrorProb:
                for k in range(noiseFlipNum):   # 0, 1
                    ind =  random.randint(0, numChans-1)
                    temp[ind] = 1- temp[ind]
            observedStates[n,:] = temp
            # yes, it did effect on performance under e.g. [0,1,2,4]
            
            if PartialObservation == 'rollOver':
                rollInd = t * poStepNum % numChans
                for i in range(poBlockNum):
                    temp[(rollInd+i)%numChans] = 0       
            observedStates[n,:] = temp
            # 20% PER, unbearable    
                        
            nodes[n].updateTrans(observedStates[n,:],t)
            if t % nodes[n].policyAdjustRate == 0:
                nodes[n].updatePolicy(t)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode) :
                                       # or isinstance(nodes[n],ddpgNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n] ,t, isWait)
            observation_ = observedStates[n,:]  # update already # full already
            # additive noise to observation_
            if random.random() < noiseErrorProb:
                for k in range(noiseFlipNum):
                    ind =  random.randint(0, numChans-1)
                    observation_[ind] = 1- observation_[ind]
            observedStates[n,:] = observation_                        
            # Todo - rolling partially observation            
            # mdp seems for robust under same noise
            # Conclusion - robust to certain level of additive noise, e.g under [0,1,2,5]
            
            temp = observedStates[n,:]
            if PartialObservation == 'True':
                rollInd = int( math.fmod(t, numChans))
                for i in range(poBlockNum):
                    temp[(rollInd+i)%numChans] = 0
            observedStates[n,:] = temp
            observation_ = observedStates[n,:]
            # better than MDP, more rubost to partial observation
            
            done = True  
            if isinstance(nodes[n],dqnNode):
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)
                if t % nodes[n].policyAdjustRate == 0:    
                    nodes[n].learn()
                    
            elif isinstance(nodes[n],acNode):
                 nodes[n].learn(observation, actionScalar, 
                     reward, observation_)
                 
#            elif isinstance(nodes[n],ddpgNode):
#                 nodes[n].storeTransition(observation, actionScalar, 
#                 reward, observation_)
#                 if nodes[n].ddpg_.pointer > nodes[n].ddpg_.MEMORY_CAPACITY:
#                     nodes[n].var *= .9995    # decay the action randomness
#                     nodes[n].ddpg_.learn()
                 
            else:
                pass
                    
 #               learnProbHist.append( nodes[n].dqn_.exploreProb)
            tocDqnLearn = time.time()
            # original  action -> step() -> observation_, reward, done
            # 1. action -> collisions
            # 2. collisions -> getReward() -> observation_, reward, done
    collisionHist[t,:]        = collisions
    cumulativeCollisions[t,:] = collisions
    if t != 0:
        cumulativeCollisions[t,:] +=  cumulativeCollisions[t-1,:]
    
    if ticMdpAction:
        mdpLearnTime[t] = tocMdpAction - ticMdpAction + tocMdpLearn - ticMdpLearn
    if ticDqnAction:
        dqnLearnTime[t] = tocDqnAction - ticDqnAction + tocDqnLearn - ticDqnLearn
        
    # show compeleted
    if t == numSteps * 0.1:
        print( "  10% completed")
        toc =  time.time()
        print( "--- cost %s seconds ---" %(toc - tic))        
    elif t == numSteps * 0.2:
        print( "  20% completed")
    elif t == numSteps * 0.3:
        print( "  30% completed")
    elif t == numSteps * 0.4:
        print( "  40% completed")
    elif t == numSteps * 0.5:
        print( "  50% completed")
    elif t == numSteps * 0.6:
        print ("  60% completed")
    elif t == numSteps * 0.7:
        print( "  70% completed")
    elif t == numSteps * 0.8:
        print( "  80% completed")
    elif t == numSteps * 0.9:
        print( "  90% completed")
    
print( " 100% completed"  )        
print( "--- End Main Loop--- ")
toc =  time.time()
print( "--- Totally %s seconds ---" %(toc - tic))






##################### PLOT ############################################ 
import os
if not os.path.exists('../dqnFig'):
   os.makedirs('../dqnFig') 
        
plt.figure(1)
myPlotProb(learnProbHist)
plt.figure(2)
txPackets = myPlotCollision(nodes, cumulativeCollisions)
plt.figure(3)
myPlotReward(nodes, cumulativeCollisions)
plt.figure(4)
myPlotAction(nodes, numChans) 
plt.figure(5)   
myPlotOccupiedEnd(nodes, numChans, plotPeriod = 100)
plt.figure(6)
myPlotOccupiedAll(nodes, numChans)
plt.figure(7)
PER, PLR = myPlotPER(nodes, numSteps, txPackets, cumulativeCollisions) 
plt.figure(8)   
myPlotPLR(nodes, PLR)
plt.figure(9)
myPlotCost(nodes)

print "Packet Error Rate: %s"%(PER[numSteps-1]*100)
    