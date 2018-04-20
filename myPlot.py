#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 01:25:02 2018

@author: Jet
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import multiNodeLearning


# !!! TODO

class myPlot(self,nodes):
    def __init__(self):

        ########################################################################
        #############################plot session###############################
        
        txPackets = [ ]
        
        
        ############### 1 cumulativeCollisions ##################
        plt.figure(1)
        #plt.hold()
        legendInfo = [ ]
        for n in range(0,numNodes):
            plt.plot(cumulativeCollisions[:,n])      # <<<<
        #    if isinstance(nodes[n],dsaNode):
        #        legendInfo = 'Node %d (DSA)'%{n}
            if isinstance(nodes[n],hoppingNode):
                legendInfo.append( 'Node %d (Hopping)'%(n) )
            elif isinstance(nodes[n],mdpNode):
                legendInfo.append( 'Node %d (MDP)'%(n) )
            elif isinstance(nodes[n],dsaNode):
                legendInfo.append( 'Node %d (DSA)'%(n) )
            elif isinstance(nodes[n],dqnNode):
                legendInfo.append( 'Node %d (DQN)'%(n) )
            else:
                legendInfo.append( 'Node %d (Legacy)'%(n) )
            
            txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T , axis=0).T ) )
        plt.legend(legendInfo)
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Collisions')
        plt.title( 'Cumulative Collisions Per Node')                      
        plt.show()
                    
                
        ############### 2 cumulativeReward ##################
        plt.figure(2)
        #plt.hold()  #deprecate
        #c = 1
        legendInfo = [ ]
        for n in range(0,numNodes):
            if isinstance(nodes[n],mdpNode):
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (MDP)'%(n) )
            elif isinstance(nodes[n],dqnNode):
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN)'%(n) )
        if legendInfo:
            plt.legend(legendInfo)
            plt.xlabel('Step Number')
            plt.ylabel('Cumulative Reward')
            plt.title( 'Cumulative Reward Per Node')   
        plt.show()             
                
        #np.ceil
        ############### 3 Actions #################################
        plt.figure(3)
        split = np.ceil(numNodes / 2)    
        for n in range(0,numNodes):
            if n <= split:
                plt.subplot(split,2,n+1)
            else:
                plt.subplot(split,2,n+1)
                
            if isinstance(nodes,mdpNode):
                offset = 1
            else:
                offset = 0
            plt.plot( np.maximum(nodes[n].actionHistInd-1 , np.zeros(numSteps)),'bo' )
            plt.ylim(0,numChans+2)
            plt.xlabel('Step Number')
            plt.ylabel('Action Number')
            
            if   isinstance(nodes[n],legacyNode):
                titleLabel = 'Action Taken by Node %d (Legacy)'%(n)
            elif isinstance(nodes[n],hoppingNode):
                titleLabel = 'Action Taken by Node %d (Hopping)'%(n)
            elif isinstance(nodes[n],dsaNode):
                titleLabel = 'Action Taken by Node %d (DSA)'%(n)
            elif isinstance(nodes[n],mdpNode):
                titleLabel = 'Action Taken by Node %d (MDP)'%(n)
            else:
                titleLabel = 'Action Taken by Node %d (DQN)'%(n)   # no dsa
            plt.title(titleLabel)
        
            
        
        ############### 4 Packet Error Rate  #################################
        timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,1,numNodes )  
        txPackets = np.array(txPackets).T
        PER =  cumulativeCollisions / txPackets
        PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots
            
        plt.figure(4)
        legendInfo = [ ]
        for i in range(numNodes):
            if isinstance(nodes[i],mdpNode):
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (MDP)'%(i) )
            elif isinstance(nodes[i],dsaNode):
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DSA)'%(i) )
            elif isinstance(nodes[i],dqnNode):
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN)'%(i) )
            else:
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (legacy)'%(i) )
        plt.legend(legendInfo)
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Packet Error Rate')
        plt.title( 'Cumulative Packet Error Rate')                      
        plt.show()        
                
        
        ############### 5 Packet Loss Rate  #################################
        plt.figure(5)
        legendInfo = [ ]
        for i in range(numNodes):
            if isinstance(nodes[i],mdpNode):
                plt.semilogy( PLR[:,i] )
                legendInfo.append( 'Node %d (MDP)'%(i) )
            elif isinstance(nodes[i],dqnNode):
                plt.semilogy( PLR[:,i] )
                legendInfo.append( 'Node %d (DQN)'%(i) )
        if not legendInfo:
            plt.xlabel('Step Number')
            plt.ylabel('Cumulative Packet Loss Rate')
            plt.title( 'Cumulative Packet Loss Rate')                      
            plt.show() 
            
        
        ############### END OF PLOT  ################################# 