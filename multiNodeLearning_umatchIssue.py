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
----------------------------                     
Main Configuration:  
    seen in setup.config file
    
---------------------------
Notice:
    for unknown reason, terminal of Spyder would keep the old tensorflow neural network data
    when change numChans(related to neural network), REMEMBER TO SHUT OFF AND OPEN A NEW terminal
    it would not happen in raw terminal 

"""


import numpy as np
import math
import random

from stateSpaceCreate      import stateSpaceCreate
from dumbNodes.legacyNode  import legacyNode
from dumbNodes.hoppingNode import hoppingNode
from dumbNodes.imNode      import imNode 
from dumbNodes.dsaNode     import dsaNode 

from stochasticNodes.poissonNode import poissonNode
from stochasticNodes.markovChainNode import markovChainNode

from learningNodes.mdpNode     import mdpNode
from learningNodes.dqnNode     import dqnNode   #
from learningNodes.acNode      import acNode
from learningNodes.ddpgNode    import ddpgNode 

from scenario    import scenario
import matplotlib.pyplot as plt
import time

from myFunction import channelAssignment, \
     myPlotProb,\
     myPlotCollision, myPlotReward, myPlotAction,\
     myPlotOccupiedEnd, myPlotOccupiedAll,\
     myPlotPER, myPlotPLR, myPlotThroughput, myPlotCost, \
     noise, updateStack, partialPad, partialObserve
     







''' ===================================================================  '''
'''      Network Setup & Simulation Parameters                          '''
''' ===================================================================  '''

# recommend to load configuration from "setup.config" file

import ConfigParser
import json
import argparse

parser            = argparse.ArgumentParser(description='Load settings file')
parser.add_argument('--set', default="setup.config" , type=str, help='Specify the setting file name')
args              = vars(parser.parse_args())
Config            = ConfigParser.ConfigParser()
Config.read(args['set'])
  
numSteps          =  json.loads( Config.get('Global', 'numSteps'))                  
numChans          =  json.loads( Config.get('Global', 'numChans'))  
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

mcChanList        =  json.loads(Config.get('markovChainNode', 'mcChanList')) 
alpha             =  json.loads(Config.get('markovChainNode', 'alpha')) 
beta              =  json.loads(Config.get('markovChainNode', 'beta')) 


noiseErrorProb    =  json.loads(Config.get('noise', 'noiseErrorProb')) 
noiseFlipNum      =  json.loads(Config.get('noise', 'noiseFlipNum')) 

poBlockNum        =  json.loads(Config.get('partialObservation', 'poBlockNum')) 
poSeeNum          =  json.loads(Config.get('partialObservation', 'poSeeNum')) 
poStepNum         =  json.loads(Config.get('partialObservation', 'poStepNum')) 
padEnable         =  json.loads(Config.get('partialObservation', 'padEnable')) 
padValue          =  json.loads(Config.get('partialObservation', 'padValue')) 
stackNum          =  json.loads(Config.get('partialObservation', 'stackNum')) 
             
numNodes = len(nodeTypes)
print "nodeType list: %s"%nodeTypes
print "num of channel: %s        num of nodes: %s"%(numChans, numNodes)

if noiseErrorProb > 0.00:
    print "-------- Additive Noise Enabled -------------"
    print "--------- with Flip Num %s ------------------"%noiseFlipNum

if padEnable == 'True':
    print "----rollOver Partial Observation Padding Enabled --------"
    print "--------  with Blocked Num %s and Step Num %s ----------"%(poBlockNum, poStepNum)


hiddenDuplexCollision = np.zeros((numNodes,numNodes))
exposedSpatialReuse   = np.zeros((numNodes,numNodes))


#if len(hiddenNodes) < numNodes:
#    hiddenNodes = np.concatenate( ( hiddenNodes,\
#                                   np.zeros(numNodes-len(hiddenNodes)) ), axis=0)

isWait = False  #default no imNode
if any(nodeTypes==2) and len(nodeTypes) > numChans:
    isWait = True
    print("learn to occupy imNode")




# Initializing Nodes, Observable States, and Possible Actions
nodes                 =  [ ]
states                = stateSpaceCreate(numChans)
CountLegacyChanIndex  = 0
CountHoppingChanIndex = 0
CountIm               = 0
CountDqn              = 0

''' ===================================================================  '''
'''          Construct different Type of Nodes                                '''
''' ===================================================================  '''

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
    elif nodeTypes[k] == 5  or nodeTypes[k] == 'markovChain':
        t = markovChainNode( numChans, numSteps, mcChanList, alpha, beta)
    elif nodeTypes[k] == 10:
        t = mdpNode(numChans,states,numSteps,'PI')   
    elif (nodeTypes[k] >= 11 and nodeTypes[k] <= 16)  \
         or (nodeTypes[k] >= 30 and nodeTypes[k] <= 33)  \
                    or nodeTypes[k] == 'dqn'          or nodeTypes[k] == 'dqnDouble' \
                    or nodeTypes[k] == 'dqnPriReplay' or nodeTypes[k] == 'dqnDuel'   \
                    or nodeTypes[k] == 'dqnRef'       or nodeTypes[k] == 'dpg'       \
                    or nodeTypes[k] == 'dqnPo'        or nodeTypes[k] == 'dqnPad'    \
                    or nodeTypes[k] == 'dqnStack':
                    
        t = dqnNode(numChans,states,numSteps, nodeTypes[k])      
#       dqnNode, temporary asyn
#       t.policyAdjustRate = 5
        CountDqn += 1
        if CountDqn > 1:
            t.priority += 1
#        print "DQN node %s Parameters: learning_rate %s, reward_decay %s,\
#                replace_target_iter %s, memory_size %s,\
#                policyAdjustRate %s" %(k, t.dqn_.lr, t.dqn_.gamma,              
#                    t.dqn_.replace_target_iter, t.dqn_.memory_size, t.policyAdjustRate )
    elif nodeTypes[k] == 17 or nodeTypes[k] == 'ac':
        t = acNode(numChans,states,numSteps) 
        
    elif nodeTypes[k] == 18 or nodeTypes[k] == 'ddpg':
        t = ddpgNode(numChans,states,numSteps)     
        

    else:
        pass
    t.hiddenDuplexCollision = hiddenDuplexCollision[k]
    t.exposedSpatialReuse   = exposedSpatialReuse[k]

    nodes.append(t)
    
print nodes

confirmKey = raw_input("If setting is ready, press ENTER to continue, any other key to abort ... ") 
assert confirmKey == '', "setting wrong, programs abort :("
        
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

''' ===================================================================  '''
'''                 MAIN LOOP BEGIN                               '''
''' ===================================================================  '''

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

# for stack-DQN
observationS  = np.zeros( stackNum * poSeeNum)
observationS_ = np.zeros( stackNum * poSeeNum)


for t in range(0,numSteps):
    ''' ===================================================================  '''
    '''    Determination of next action for each node                       '''
    ''' ===================================================================  '''
    
    dqnPriObservation = 0
    dqnPriAction = 0
    
    '''=========== get action =============================================='''
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode) or isinstance(nodes[n],ddpgNode):
            ticDqnAction  = time.time()
            temp = observedStates[n,:]
            
            if   nodes[n].type == 'dqnPo':
                observation                = partialObserve( temp, t, poStepNum, poSeeNum)
                actions[n,:], actionScalar = nodes[n].getAction(t, observation)
            elif nodes[n].type == 'dqnPad':
                observation                = partialPad( temp, t, poStepNum, poBlockNum, padValue)
                actions[n,:], actionScalar = nodes[n].getAction(t, observation)                
            elif nodes[n].type == 'dqnStack' or nodes[n].type == 'dpgStack':
                temp2 = partialObserve( temp, t, poStepNum, poSeeNum)
                observationS               = updateStack(observationS, temp2)
                actions[n,:], actionScalar = nodes[n].getAction(t, observationS)
            else:
                "------ dqn primary get Action, while dqn sec pending ------"
                if nodes[n].priority:  # if higher priority
                    observation                = temp
                    
                    dqnPriObservation = observation
                    
#                    print "dqn primary observation %s"%(observation)
                    actions[n,:], actionScalar = nodes[n].getAction(t, observation)
                    
                    dqnPriAction = actions[n,:]
                    
#                    print "dqn primary make action %s"%(actionScalar)
#                    print "******dqn node %s make action*****"%(n)
                    # dqn2 action pending as WAIT, be overwritten later

             

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

    '---------------------- first update after dqn primary excute action -----------------------------------------'
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if nn != n:
                if any( np.array( actions[n,:] + actions[nn,:])> 1 ):
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)        
    '-----------------------------------------------------------------------------'
          
                    
                
                
#                # case 1, duplex collision
#                if nodes[nn].hiddenDuplexCollision[n]:
#                    if  np.sum( actions[n,:] + actions[nn,:])> 1:
#                        collisions[n]         = 1
#                        collisionTally[n,nn] += 1
#                        observedStates[n,:]   = np.ones(numChans)   # all illegal 
#                        # think duplex col node as "full channel user", only have to is wait
#                        # print "duplex collision"                                  
#                else:
#                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)   # partial obseravtion
#                        
#                # case 2, same channel collision                        
#                if np.sum(actions[n,:]) > 0 \
#                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
#                  and not nodes[nn].exposedSpatialReuse[n]:    # if nodes[nn].exposedSpatialReuse[n] == 0
#                    collisions[n]         = 1
#                    collisionTally[n,nn] += 1
                    
                    
                      
    "-------- after meta update for another observation, dqn1 make action; and then update collision --------" 
    for n in range(0,numNodes):
        if nodes[n].type == 'dqn':
            if nodes[n].priority == 0:
                
#                print "dqn sec observation %s"%(observedStates[n,:])
                
                "--- correct check, the gosh ---"
                if not np.array_equal( observedStates[n,:] , ( dqnPriObservation + dqnPriAction ) > 0):
                    print "unmatch at step %s"%(t)
                    
                 
                 
                
                observation = observedStates[n,:]
                actions[n,:], actionScalar = nodes[n].getAction(t, observation)
#                print "dqn sec make action %s"%(actionScalar)
            
    
    
    "-------- update again after dqn 2 ------- "
    
    
    
    '-----------------------------------------------------------------------------'
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if nn != n:
                if any( np.array( actions[n,:] + actions[nn,:])> 1 ):
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)
    '-----------------------------------------------------------------------------'
    
#    for n in range(0,numNodes):
#        collisions[n] = 0
#    
#   
#        for nn in range(0,numNodes):
#            if nn != n:
#                # case 1, duplex collision
#                if nodes[nn].hiddenDuplexCollision[n]:
#                    if  np.sum( actions[n,:] + actions[nn,:])> 1:
#                        collisions[n]         = 1
#                        collisionTally[n,nn] += 1
#                        observedStates[n,:]   = np.ones(numChans)   # all illegal 
#                        # think duplex col node as "full channel user", only have to is wait
#                        # print "duplex collision"                                  
#                else:
#                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)   # partial obseravtion
#                        
#                # case 2, same channel collision                        
#                if np.sum(actions[n,:]) > 0 \
#                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
#                  and not nodes[nn].exposedSpatialReuse[n]:    # if nodes[nn].exposedSpatialReuse[n] == 0
#                    collisions[n]         = 1
#                    collisionTally[n,nn] += 1
    "-------- update ends------- "
    
    
    
    ''' ===================================================================  '''
    ''' Determining observations, collisions, rewards, and policies          '''
    ''' ===================================================================  '''
            
           

    for n in range(0,numNodes):
        if isinstance(nodes[n],dsaNode):
            nodes[n].updateState(observedStates[n,:],t)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],t,isWait)
            # additive noise to flip certain bit of observation
            temp = observedStates[n,:]

            if  noiseErrorProb > 0:
                observedStates[n,:]  = noise(observedStates[n,:] , noiseErrorProb, noiseFlipNum)            
            if padEnable == 'True':
                observedStates[n,:] = partialPad(observedStates[n,:], t, poStepNum, poBlockNum, padValue)
  
                        
            nodes[n].updateTrans(observedStates[n,:],t)
            if t % nodes[n].policyAdjustRate == 0:
                nodes[n].updatePolicy(t)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode) or isinstance(nodes[n],ddpgNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n] ,t, isWait)
            temp = observedStates[n,:]  #  observation_

            if   nodes[n].type == 'dqnPo':
                observation_                = partialObserve( temp, t, poStepNum, poSeeNum)
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)
            elif nodes[n].type == 'dqnPad':
                observation_                = partialPad( temp, t, poStepNum, poBlockNum, padValue)
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)             
            elif nodes[n].type == 'dqnStack' or nodes[n].type == 'dpgStack':
                temp2 = partialObserve( temp, t, poStepNum, poSeeNum)
                observationS_               = updateStack(observationS, temp2)
                nodes[n].storeTransition(observationS, actionScalar, 
                     reward, observationS_) 
            else:
                "----- dqn1 should   ---- learn ---------"
                observation_ = temp
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)
                

            if  noiseErrorProb > 0:           
                observation_  = noise(observation_ , noiseErrorProb, noiseFlipNum)

            done = True  
            if isinstance(nodes[n],dqnNode):
                if t % nodes[n].policyAdjustRate == 0:    
                    nodes[n].learn()
#                learnProbHist.append( nodes[n].dqn_.exploreProb)
                    
            elif isinstance(nodes[n],acNode):
                 nodes[n].learn(observation, actionScalar, 
                     reward, observation_)
                 
            elif isinstance(nodes[n],ddpgNode):
                 nodes[n].storeTransition(observation, actionScalar, 
                 reward, observation_)
                 if nodes[n].ddpg_.pointer > nodes[n].ddpg_.MEMORY_CAPACITY:
                     nodes[n].var *= .9995    # decay the action randomness
                     nodes[n].ddpg_.learn()
                 
            else:
                pass
                    
                
            tocDqnLearn = time.time()

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





''' ===================================================================  '''
'''                             PLOT                                     '''
''' ===================================================================  '''

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
myPlotThroughput(nodes, PLR)
plt.figure(10)
#myPlotCost(nodes)

print "Packet Error Rate: %s"%(PER[numSteps-1]*100)
    