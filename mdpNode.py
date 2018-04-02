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


class mdpNode(radioNode):
    goodChans     = [ ]    
    numStates     = [ ]
    states        = [ ]
    stateHist     = [ ]
    stateTally    = [ ]
    stateTrans    = [ ]
    avgStateTrans = [ ]
    
    discountFactor   = 0.9
    policyAdjustRate = 100         # Policy is adjusted at this step increment
    
    exploreProb      = [ ]                    # Current exploration probability
    exploreInit      = 1.0               # Initial exploration probability
    exploreDecay     = 0.1              # Percentage reduction in exploration chance per policy calculation
    exploreHist      = [ ]    
    exploreDecayType = 'perf'             # either 'expo', 'step' or 'perf'
    exploreWindow    = 500           # only used with 'step'
    exploreMin       = 0.01              # only used with 'step'    
    explorePerf      = 10               # only used with 'perf' 
    explorePerfWin   = 100           # triggers jump in explore prob to
                                    # 1 if reward is below this over 
                                    # last explorePerfWin epoch    
    policy           = [ ]
    policyHist       = [ ]        
    # [Not transmitting, Good Channel no Interference, Good Channel Interference, Bad Channel no Interference, Bad Channel Interference]
    rewards          = [-200, 100, -100, 50, -200]   # -j ??    
    rewardHist       = [ ]
    rewardTally      = [ ]        
    rewardTrans      = [ ]
    cumulativeReward = [ ]
    
    def __init__(self,numChans,states,numSteps):
        self.actions = np.zeros((numChans+1,numChans)
        for k in range(0,numChans):
            self.actions[k+1,k] = 1
            #for n in range(0,numNodes):        
        self.numActions    = np.shape(self.actions)
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        
        self.goodChans     = np.ones(numChans)
        
        self.states        = states
        self.numStates     = np.shape(states)
        
        self.stateHist     = np.zeros((numSteps,numChans))
        self.stateTally    = np.zeros(self.numStates)
        self.stateTrans    = np.zeros((self.numStates,self.numStates,self.numActions))
        self.stateTrans[:,0,:] = np.ones( (self.numStates,1,self.numActions) )
        self.avgStateTrans = np.zeros( (self.numStates,self.numStates,self.numActions))
        
        self.rewardHist    = np.zeros(numSteps)
        self.rewardTally   = np.zeros(numChans+1)
        self.cumulativeReward = np.zeros(numSteps)
        self.rewardTrans   = np.zeros((self.numStates,self.numStates,self.numActions) )
        
        self.exploreProb   = self.exploreInit
        self.exploreHist   = self.exploreProb
    

      
        
        
    def getAction(self,stepNum):
        if random.random( ) < self.exploreProb:
            action = self.actions[ random.randint(0, numActions-1) , :]              # randi
        else:
            # ismember()
            stateIndex = ismember(self.stateHist[stepNum-1,:], self.states)
            action = self.actions(self.policy[stateIndex],:)                # follow 'intelligient' policy  
            # notice traspose
        
        
        self.actionHist[stepNum,:] = action
                    
        if not np.sum(action):
            self.actionTally[0] +=    1
            self.actionHistInd[stepNum] = 1
        else:
            self.actionHistInd[stepNum] = np.where(action == 1) + 1
            self.actionTally[1:] += action           
        

        
    def getReward(self,collision,stepNum):
        action = self.actionHist[stepNum,:]
        if not np.sum(action):
            reward = self.rewards[0]
            #  rewards = [-200, 100, -100, 50, -200] 
            self.rewardTally[0] +=  reward
        else:
            if isempty(find(self.goodChans+action > 1, 1)):    # find the 1st of ...
                if collision == 1:
                    reward = self.rewards[4]
                else:
                    reward = self.rewards[3]
                
            else:
                if collision == 1:
                    reward = self.rewards[2]
                else:
                    reward = self.rewards[1]
                
                                         
            self.rewardTally[1:] += action*reward
        
        self.rewardHist[stepNum] = reward   
        
        if stepNum == 1:
            self.cumulativeReward[stepNum] = reward
        else:
            self.cumulativeReward[stepNum] = self.cumulativeReward[stepNum-1] + reward
        
        
        
    def updateTrans(self,observedState,stepNum):
        self.stateHist[stepNum,:] = observedState
            
        indB = ismember(self.stateHist[stepNum,:],self.states)
        self.stateTally[indB] += 1
        
        if stepNum > 1:
            indA = ismember(self.stateHist[stepNum-1,:], self.states)
            indC = ismember(self.actionHist[stepNum,:],  self.actions)
            
            self.stateTrans[indA,indB,indC]  +=  1
            self.rewardTrans[indA,indB,indC]  = self.rewardHist[stepNum]
            # why 3D stuff
            # state_i, state_j, action
        
        
    def updatePolicy(self,step):
        self.avgStateTrans = self.stateTrans
        for k in range(0,self.numStates):
            for kk = 1 in range(0,self.numActions):
                self.avgStateTrans[k,:,kk] = self.avgStateTrans[k,:,kk] / np.sum(self.avgStateTrans[k,:,kk])  # normalize                  
            
        
        self.avgStateTrans(isnan(self.avgStateTrans)) = 0    # isnan
        
        [~,self.policy] = mdp_policy_iteration(self.avgStateTrans,self.rewardTrans,self.discountFactor)
        self.policy = self.policy.'   # data type of policy 
        
        self.policyHist = [self.policyHist, self.policy]
        
        if self.exploreDecayType == 'expo':
            self.exploreProb = self.exploreInit*exp(-self.exploreDecay*np.shape(self.policyHist)[0])     
 
       elif self.exploreDecayType == 'step'
            if step > self.exploreWindow:
                self.exploreProb = self.exploreMin
            else:
                self.exploreProb = 1
                
        elif self.exploreDecayType == 'perf':
             self.exploreProb = self.exploreInit*exp(-self.exploreDecay*np.shape(self.policyHist)[0])     
             if (mean(self.rewardHist[step-self.explorePerfWin+1:step]) < self.explorePerf) & (self.exploreProb < 0.05)
                 self.exploreProb = 0.2 #self.exploreProb + self.explorePerfJump
                 
        else:
            error('exploreDecayType misdefined')
        
        self.exploreHist = [self.exploreHist, self.exploreProb]
        
        
        
        