#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:54:27 2018

@author: Jet

jianyuan@vt.edu

April,2018

This is the main script to run

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
from learningNodes.drqnNode     import drqnNode   #
from learningNodes.acNode      import acNode
from learningNodes.ddpgNode    import ddpgNode 

from scenario    import scenario
import matplotlib.pyplot as plt
import time

from myFunction import myPlotProb,\
      myPlotCollision, myPlotReward, myPlotAction,\
     myPlotOccupiedEnd, myPlotOccupiedAll,\
     myPlotPER, myPlotPLR, myPlotThroughput, myPlotCost, \
     noise, updateStack, partialPad, partialObserve, \
     update, myCalculatePER, myGetTxPackets, partialObserveAction, \
     myCalculatePFR, myPlotPFR, myPlotPCR, myPlotPAR, myPlotPFCAR
     







''' ===================================================================  '''
'''      Network Setup & Simulation Parameters                          '''
''' ===================================================================  '''

# recommend to load configuration from "setup.config" file

import ConfigParser
import json
import argparse

parser            = argparse.ArgumentParser(description='Load settings file')
parser.add_argument('--set', default="setup.cfg" , type=str, help='Specify the setting file name')
args              = vars(parser.parse_args())
Config            = ConfigParser.ConfigParser()
Config.read(args['set'])
  
numSteps          =  json.loads( Config.get('Global', 'numSteps'))                  
numChans          =  json.loads( Config.get('Global', 'numChans'))  
nodeTypes         =  np.asarray(  json.loads(Config.get('Global', 'nodeTypes')))
optimalTP         =  json.loads( Config.get('Global', 'optimalTP')) 


legacyChanList    =  json.loads(Config.get('legacyNode', 'legacyChanList')) 
 

hoppingChanList   =  json.loads(Config.get('hoppingNode', 'hoppingChanList'))
hopRate           =  json.loads( Config.get('hoppingNode', 'hopRate'))  
hoppingWidth      =  json.loads( Config.get('hoppingNode', 'hoppingWidth'))  
offSet            =  json.loads( Config.get('hoppingNode', 'offSet'))  

imPeriod          =  json.loads(Config.get('imNode', 'imPeriod')) 
imChanList        =  json.loads(Config.get('imNode', 'imChanList')) 
imDutyCircleList  =  json.loads(Config.get('imNode', 'imDutyCircleList')) 

poissonChanList   =  json.loads(Config.get('poissonNode', 'poissonChanList')) 
arrivalInterval   =  json.loads(Config.get('poissonNode', 'arrivalInterval')) 
serviceInterval   =  json.loads(Config.get('poissonNode', 'serviceInterval')) 

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

timeLearnStart    = 1000
absent            = 0

             
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

#isWait = False  #default no imNode
#if any(nodeTypes==2) and len(nodeTypes) > numChans:
#    isWait = True
#    print("learn to occupy imNode")




# Initializing Nodes, Observable States, and Possible Actions
nodes                 =  [ ]
if stackNum > 1:
    print "extra-memory MDP"
states                = stateSpaceCreate(numChans*stackNum)
#states                = stateSpaceCreate(numChans)

CountLegacyChanIndex  = 0
CountHoppingChanIndex = 0
CountIm               = 0
numDqn                = 0
dqnIndex              =  [ ]

''' ===================================================================  '''
'''          Construct different Type of Nodes                                '''
''' ===================================================================  '''

for k in range(0,numNodes):
    if   nodeTypes[k] == 0 or nodeTypes[k] == 'legacy':
        t = legacyNode(numChans,numSteps, legacyChanList[CountLegacyChanIndex]) 
        CountLegacyChanIndex += 1               
    elif nodeTypes[k] == 1  or nodeTypes[k] == 'hopping':
        t = hoppingNode(numChans,numSteps,hoppingChanList[CountHoppingChanIndex],hopRate,offSet[CountHoppingChanIndex])
        CountHoppingChanIndex += 1
    elif nodeTypes[k] == 2 or nodeTypes[k] == 'im':
        t = imNode(numChans,numSteps,imPeriod, imDutyCircleList[CountIm], imChanList[CountIm])
        CountIm += 1
    elif nodeTypes[k] == 3  or nodeTypes[k] == 'dsa':
        t = dsaNode(numChans,numSteps)    
    elif nodeTypes[k] == 4  or nodeTypes[k] == 'possion':
        t = poissonNode( numChans, numSteps, poissonChanList, arrivalInterval, serviceInterval)
    elif nodeTypes[k] == 5  or nodeTypes[k] == 'markovChain':
        t = markovChainNode( numChans, numSteps, mcChanList, alpha, beta)
    elif nodeTypes[k] == 10  or nodeTypes[k] == 'mdp':
        t = mdpNode(numChans,states,numSteps,'VI')   
    elif (nodeTypes[k] >= 11 and nodeTypes[k] <= 16)  \
         or (nodeTypes[k] >= 30 and nodeTypes[k] <= 33)  \
                    or nodeTypes[k] == 'dqn'          or nodeTypes[k] == 'dqnDouble' \
                    or nodeTypes[k] == 'dqnPriReplay' or nodeTypes[k] == 'dqnDuel'   \
                    or nodeTypes[k] == 'dqnRef'       or nodeTypes[k] == 'dpg'       \
                    or nodeTypes[k] == 'dqnPo'        or nodeTypes[k] == 'dqnPad'    \
                    or nodeTypes[k] == 'dqnStack':
#            or nodeTypes[k] in ['dqn', 'dqnDouble', 'dqnPriReplay', 'dqnDuel', 'dqnRef', \ 
#                       'dpg', 'dqnPo', 'dqnPad',  'dqnStack'  ]:
            
        t = dqnNode(numChans, numSteps, nodeTypes[k])     
        numDqn += 1
        dqnIndex.append(k)
        #        print "DQN node %s Parameters: learning_rate %s, reward_decay %s,\
        #                replace_target_iter %s, memory_size %s,\
        #                policyAdjustRate %s" %(k, t.dqn_.lr, t.dqn_.gamma,              
        #                    t.dqn_.replace_target_iter, t.dqn_.memory_size, t.policyAdjustRate )
    elif nodeTypes[k] == 17 or nodeTypes[k] == 'ac':
        t = acNode(numChans,states,numSteps) 
        numDqn += 1
        dqnIndex.append(k)
        
    elif nodeTypes[k] == 18 or nodeTypes[k] == 'ddpg':
        t = ddpgNode(numChans,states,numSteps)
        numDqn += 1
        dqnIndex.append(k)
        
    elif nodeTypes[k] == 34  or nodeTypes[k] == 'drqn':
        t = drqnNode(numChans,numSteps, poSeeNum)   
        numDqn += 1
        dqnIndex.append(k)
        
        

    else:
        pass
    t.hiddenDuplexCollision = hiddenDuplexCollision[k]
    t.exposedSpatialReuse   = exposedSpatialReuse[k]

    nodes.append(t)
    
print nodes

"-------- print ENTER to confirm the input--------------"
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
cumulativeAbsents    = np.zeros((numSteps,numNodes)) 


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
#observationS  = np.zeros( stackNum * poSeeNum)
#observationS_ = np.zeros( stackNum * poSeeNum)
observationS  = np.zeros( stackNum * numChans)
observationS_ = np.zeros( stackNum * numChans)

priorityS      = np.arange(numDqn)
indexPriority = np.zeros(numDqn)


for t in range(0,numSteps):
    ''' ===================================================================  '''
    '''    Determination of next action, states, and action for each node                       '''
    ''' ===================================================================  '''
    
    "random shuffle the priority of dqn nodes"
    np.random.shuffle(priorityS)
    for m in range(numDqn):
        nodes[dqnIndex[m]].priority =  priorityS[m]
        indexPriority[priorityS[m]] = dqnIndex[m]
#    print "indexPriority %s at step %s"%(indexPriority,t)
    
    '''------------------- get action ------------------------'''
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],drqnNode) or isinstance(nodes[n],acNode) or isinstance(nodes[n],ddpgNode):
            ticDqnAction  = time.time()
            temp = observedStates[n,:]
            
            "------ dqn primary get Action, while dqn sec pending ------"

            if n == indexPriority[0]:  # if higher priority
                if nodes[n].type == 'dqn' or nodes[n].type == 'dpg' or nodes[n].type == 'ac' \
                    or nodes[n].type == 'dqnDouble' or nodes[n].type == 'dqnDuel' \
                    or nodes[n].type == 'dqnPriReplay' or nodes[n].type == 'dqnRef':
                    observation                = temp                    
                    actions[n,:], actionScalar = nodes[n].getAction(t, observation)
                elif nodes[n].type == 'dqnPo':
                    observationPo              = partialObserve( temp, t, poStepNum, poSeeNum)
                    actions[n,:], actionScalar = nodes[n].getAction(t, observationPo)
                elif nodes[n].type == 'dqnPad':
                    observationPd                = partialPad( temp, t, poStepNum, poBlockNum, padValue)
                    actions[n,:], actionScalar = nodes[n].getAction(t, observationPd)                
                elif nodes[n].type == 'dqnStack' or nodes[n].type == 'dpgStack':
#                    temp2                      = partialObserve( temp, t, poStepNum, poSeeNum)
                    temp2                      = partialObserveAction( temp, t, poStepNum, poSeeNum,actions[n,:])
                    # extra-memory DQN, no block
#                    temp2 = temp
                    observationS               = updateStack(observationS, temp2)
                    actions[n,:], actionScalar = nodes[n].getAction(t, observationS)
                elif nodes[n].type == 'drqn':
#                    observationPo              = partialObserveAction( temp, t, poStepNum, poSeeNum, actions[n,:])
                    observationPo = temp
                    actions[n,:], actionScalar = nodes[n].getAction(t, observationPo)
                else:
                    print "error dqn type"

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

    '''-------- update states and other dqn make action ----------------------'''    
    collisions, absent, collisionTally, observedStates = \
                    update(nodes, numChans, actions, collisions, collisionTally, absent)

    for m in range(1,numDqn):
        l = indexPriority[m].astype(int)
        # update
        temp = observedStates[l,:]
            
        if nodes[l].type == 'dqn' or nodes[l].type == 'dpg' or nodes[l].type == 'ac' \
            or nodes[l].type == 'dqnDouble' or nodes[l].type == 'dqnDuel' \
            or nodes[l].type == 'dqnPriReplay' or nodes[l].type == 'dqnRef':
        
            observation                = temp                    
            actions[l,:], actionScalar = nodes[l].getAction(t, observation)
        elif nodes[l].type == 'dqnPo':
            observationPo              = partialObserve( temp, t, poStepNum, poSeeNum)
            actions[l,:], actionScalar = nodes[l].getAction(t, observationPo)
        elif nodes[l].type == 'dqnPad':
            observationPd                = partialPad( temp, t, poStepNum, poBlockNum, padValue)
            actions[l,:], actionScalar = nodes[l].getAction(t, observationPd)                
        elif nodes[l].type == 'dqnStack' or nodes[l].type == 'dpgStack':
            temp2                      = partialObserveAction( temp, t, poStepNum, poSeeNum, actions[l,:])
#            temp2 = temp
            observationS               = updateStack(observationS, temp2)
            actions[l,:], actionScalar = nodes[l].getAction(t, observationS)
        elif nodes[l].type == 'drqn':
#            observationPo              = partialObserveAction( temp, t, poStepNum, poSeeNum, actions[l,:])
            observationPo = temp
            actions[l,:], actionScalar = nodes[l].getAction(t, observationPo)
        else:
            print "error dqn type"
        
        collisions, absent, collisionTally, observedStates = \
            update(nodes, numChans, actions, collisions, collisionTally, absent)

    "notice NO FEEDBACK for wait, thus hard to define reward for wait, sometime it is right wait, sometimes NOT"
    
    ''' ===================================================================  '''
    ''' Determining rewards, and policies          '''
    ''' ===================================================================  '''
            
           

    for n in range(0,numNodes):
        if isinstance(nodes[n],dsaNode):
            nodes[n].updateState(observedStates[n,:],t)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],t)
            # additive noise to flip certain bit of observation
            temp = observedStates[n,:]
            
            # extra-meory
            observationS               = updateStack(observationS, temp)


            if  noiseErrorProb > 0:
                observedStates[n,:]  = noise(observedStates[n,:] , noiseErrorProb, noiseFlipNum)            
            if padEnable == 'True':
                observedStates[n,:] = partialPad(observedStates[n,:], t, poStepNum, poBlockNum, padValue)
  
            nodes[n].updateTrans(observationS,t)         # for extra-memoey             
#            nodes[n].updateTrans(observedStates[n,:],t)
            if t % nodes[n].policyAdjustRate == 0:
                nodes[n].updatePolicy(t)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode) or isinstance(nodes[n],ddpgNode) or isinstance(nodes[n],drqnNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n] ,t)
            temp = observedStates[n,:]  #  observation_

            if   nodes[n].type == 'dqnPo':
                observation_                = partialObserve( temp, t, poStepNum, poSeeNum)
                nodes[n].storeTransition(observationPo, actionScalar, 
                     reward, observation_)
            elif nodes[n].type == 'dqnPad':
                observation_                = partialPad( temp, t, poStepNum, poBlockNum, padValue)
                nodes[n].storeTransition(observationPd, actionScalar, 
                     reward, observation_)             
            elif nodes[n].type == 'dqnStack' or nodes[n].type == 'dpgStack':
                temp2 = partialObserveAction( temp, t, poStepNum, poSeeNum,actions[n,:])
#                temp2 = temp
                observationS_               = updateStack(observationS, temp2)
                nodes[n].storeTransition(observationS, actionScalar, 
                     reward, observationS_) 
            elif   nodes[n].type == 'drqn':
#                observation_                = partialObserveAction( temp, t, poStepNum, poSeeNum, actions[n,:])
                observation_ = temp
                nodes[n].storeTransition(observationPo, actionScalar, 
                     reward, observation_, t)         ########################
            elif nodes[n].type == 'dqn' or nodes[n].type == 'dpg':
                observation_ = temp
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)
                

            if  noiseErrorProb > 0:           
                observation_  = noise(observation_ , noiseErrorProb, noiseFlipNum)

            done = True  
            if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],drqnNode):
                if t >timeLearnStart:
                    if t % nodes[n].policyAdjustRate == 0:    
                        nodes[n].learn()
                    
                learnProbHist.append( nodes[n].dqn_.exploreProb)
                    
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
        
    absents                = np.zeros(numNodes)
    absents[dqnIndex[0]]   = absent    # todo uniform vs efficiency
    cumulativeAbsents[t,:] = absents
    
    
    if ticMdpAction:
        mdpLearnTime[t] = tocMdpAction - ticMdpAction + tocMdpLearn - ticMdpLearn
    if ticDqnAction:
        dqnLearnTime[t] = tocDqnAction - ticDqnAction + tocDqnLearn - ticDqnLearn
        
    " show compeleted "
    if t == numSteps * 0.1:
        print( "  10% completed--------------------")
        toc =  time.time()
        print( "--- cost %s seconds ---" %(toc - tic))
        
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.2:
        print( "  20% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.3:
        print( "  30% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.4:
        print( "  40% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.5:
        print( "  50% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.6:
        print ("  60% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.7:
        print( "  70% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.8:
        print( "  80% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    elif t == numSteps * 0.9:
        print( "  90% completed--------------------")
#        PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  myGetTxPackets(nodes,cumulativeCollisions), 
#                                  cumulativeCollisions)
#        print "Packet Error Rate: %s"%(PER[t-1]*100)
#        print "Packet Loss  Rate: %s"%(PLR[t-1]*100)
    
print( " 100% completed--------------------")
txPackets = myGetTxPackets(nodes,cumulativeCollisions)
#PER, PLR = myCalculatePER(nodes, numSteps, 
#                                  txPackets, 
#                                  cumulativeCollisions)
PFR,PCR, PAR = myCalculatePFR(nodes,numSteps, cumulativeCollisions, cumulativeAbsents)
print "Packet Fail       Rate: %s"%(PFR[t-1]*100)   
print "Packet Collision  Rate: %s"%(PCR[t-1]*100)  
print "Packet Absent     Rate: %s"%(PAR[t-1]*100)   
   
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
plt.figure(1)
myPlotCollision(nodes, cumulativeCollisions)
plt.figure(2)
myPlotReward(nodes, cumulativeCollisions)
#plt.figure(4)
#myPlotAction(nodes, numChans) 
plt.figure(3)   
myPlotOccupiedEnd(nodes, numChans, plotPeriod = 100)
plt.figure(4)
myPlotOccupiedAll(nodes, numChans)
#plt.figure(5)
#myPlotPER(nodes, PER) 
#plt.figure(6)   
#myPlotPLR(nodes, PLR)
#plt.figure(9)   
#myPlotThroughput(nodes, cumulativeCollisions, txPackets, optimalTP, numSteps)
#plt.figure(10)
#myPlotCost(nodes)
#plt.figure(5)
#myPlotPFR(nodes,PFR)
#plt.figure(6)
#myPlotPCR(nodes,PCR)
#plt.figure(7)
#myPlotPAR(nodes,PAR)
plt.figure(5)
myPlotPFCAR(dqnIndex[0],PFR, PCR, PAR)
