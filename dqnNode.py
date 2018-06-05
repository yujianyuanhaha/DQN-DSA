#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 00:45:09 2018

@author: Jet
"""

from radioNode import radioNode
from myFunction import ismember   #
import random
import numpy as np
from dqn import dqn
import dqnDouble
import dqnPriReplay
import dqnDuel

class dqnNode(radioNode):
    goodChans     = [ ]    
    numStates     = [ ]
    states        = [ ]
    stateHist     = [ ]
    stateTally    = [ ]
    stateTrans    = [ ]
    avgStateTrans = [ ]
    
    discountFactor   = 0.9
    policyAdjustRate = 5         # Policy is adjusted at this step increment
    
            
    policy           = [ ] 
    policyHist       = [ ]        
    # [Not transmitting, Good Channel no Interference, Good Channel Interference, 
    # Bad Channel no Interference, Bad Channel Interference]
    rewards          = [-200, 100, -100, 50, -100]   
    # different duty cycle need different rewards   
    rewardHist       = [ ]
    rewardTally      = [ ]        
    rewardTrans      = [ ]
    cumulativeReward = [ ]
    
    def __init__(self,numChans,states,numSteps, dqnType):
        self.actions = np.zeros((numChans+1,numChans))
        for k in range(0,numChans):
            self.actions[k+1,k] = 1
        self.numChans      = numChans
        self.numActions    = np.shape(self.actions)[0]
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        
        self.goodChans     = np.ones(numChans)
        
        self.states        = states
        self.numStates     = np.shape(states)[0]
        
        self.stateHist     = np.zeros((numSteps,numChans))
        self.stateTally    = np.zeros(self.numStates)
      
        self.rewardHist    = np.zeros(numSteps)
        self.rewardTally   = np.zeros(numChans+1)
        self.cumulativeReward = np.zeros(numSteps)
        self.rewardTrans   = np.zeros((self.numActions, self.numStates,self.numStates) )
        
        self.exploreHist   = [ ]
        
        self.policy = np.zeros(numChans)
               
        self.n_actions     = numChans+1   
        self.n_features    = numChans 
        
        self.type = "raw"        
        if dqnType == 5 :
            self.dqn_ = dqn(
                            self,
                            self.n_actions, 
                            self.n_features,   
                            learning_rate=0.01,
                            reward_decay=0.9,
                            exploreDecayType = 'expo',
                            replace_target_iter=200,
                            memory_size=2000,
                            e_greedy_increment=True,
                            ) 
        elif dqnType == 6 :
            self.type = "double"
            self.dqn_ = dqnDouble.DoubleDQN(
                            self,
                            self.n_actions, 
                            self.n_features,   
                            learning_rate=0.005,
                            reward_decay=0.9,
                            exploreDecayType = 'expo',
                            replace_target_iter=200,
                            memory_size=2000,
                            e_greedy_increment=True,
                            double_q = True, 
                            )
        elif dqnType == 7 :
            self.type = "priReplay"
            self.dqn_ = dqnPriReplay.DQNPrioritizedReplay(
                            self,
                            self.n_actions, 
                            self.n_features,   
                            learning_rate=0.01,
                            reward_decay=0.9,
                            exploreDecayType = 'expo',
                            replace_target_iter=200,
                            memory_size=2000,
                            e_greedy_increment=True,
                            prioritized=True,  
                            ) 
        elif dqnType == 8 :
            self.type = "duel"
            self.dqn_ = dqnDuel.DuelingDQN(
                            self,
                            self.n_actions, 
                            self.n_features,   
                            learning_rate=0.01,
                            reward_decay=0.9,
                             exploreDecayType = 'expo',
                            replace_target_iter=200,
                            memory_size=2000,
                            e_greedy_increment=True,
                            dueling=True, 
                            ) 
        else:
                pass

        
    def getAction(self, stepNum ,observation):
        temp = self.dqn_.choose_action(observation) 
        # !!! new define, convert action from a int to a array
        action       = np.zeros(self.numChans) 
        if temp > 0:
            action[temp-1] = 1 
        
        self.actionHist[stepNum,:] = action                   
        if not np.sum(action):
            self.actionTally[0] +=    1
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1
            self.actionTally[1:] += action
        
        return action, temp  
    
    
    def getReward(self,collision,stepNum, isWait):
        
        if isWait == True:
             self.rewards  = [-50, 100, -200, 50, -100] 
        action = self.actionHist[stepNum,:]
        if not np.sum(action):
            reward = self.rewards[0]
            self.rewardTally[0] +=  reward
        else:
            if any(np.array(self.goodChans+action) > 1): 
                if collision == 1:
                    reward = self.rewards[2]
                else:
                    reward = self.rewards[1]             
            else:
                if collision == 1:
                    reward = self.rewards[4]
                else:
                    reward = self.rewards[3]   
 
            self.rewardTally[1:] += action * reward        
        self.rewardHist[stepNum] = reward   
        
        if stepNum == 0:
            self.cumulativeReward[stepNum] = reward
        else:
            self.cumulativeReward[stepNum] = self.cumulativeReward[stepNum-1] + reward
        return reward  
    
    
    def storeTransition(self, s, a, r, s_):
        self.dqn_.store_transition(s, a, r, s_)   
        
    def learn(self):
        self.dqn_.learn()

       
        
        
        