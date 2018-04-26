#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 02:57:37 2018

@author: Jet
"""

# functions
import numpy as np

# [~,stateIndex] = ismember(self.stateHist[stepNum-1,:], self.states,'rows') 

def ismember(a,B):
    t = 0           
    for j in range(0, np.shape(B)[0]):
        if all(a == B[j,:]):
            t = j
            break
    return t

# if no match, return 0
# possible one line function    
    





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
        
        
        
        
def channelAssignment(nodeTypes, hoppingWidth, numChans):        
    # random assign channel or choose example set
    # hopping is kind of combination of imNode, legecy also a special kind of legacy   
    # first sort a copy of input NodeTye array, legacy/im first; hoppingNext
    nodeTypes_ = nodeTypes
    nodeTypes_.sort()
#    print nodeTypes_
    
    numNodes       = len(nodeTypes_)
    legacyNodeNum  = 0
    hoppingNodeNum = 0
    imNodeNum      = 0    
    availChanList = range(numChans)
    legacyChanList = [ ]
    imChanList = [ ]
  
    # Assign Legacy and Intermittent
    for k in range(0,numNodes):
        if   nodeTypes_[k] == 0:
            legacyNodeNum        += 1
            index = random.randint(0,len(availChanList)-1)
            legacyChanList.append(availChanList[index])
            del availChanList[index]
        elif nodeTypes_[k] == 1:
            hoppingNodeNum       += 1

        elif nodeTypes_[k] == 6:
            imNodeNum            += 1
            index = random.randint(0,len(availChanList)-1)
            imChanList.append(availChanList[index])
            del availChanList[index]
        else:
            print "nodeTypes from 0 - 6"
            
    assert len(hoppingWidth) == hoppingNodeNum, "hopWidth array does not match num of hop node"
    
    # if hoppingWidth include 2/ 3, also collision
            
    # capacity check
    occupiedHopping = 0
    for i in range(len(hoppingWidth)):
        occupiedHopping += 1.0/hoppingWidth[i]
    occupied = legacyNodeNum + imNodeNum + occupiedHopping
    utilization = occupied * 1.0/ numChans
    assert utilization <= 1, "capacity overflow"        
    
    hoppingChanList = []    
    for i in range(hoppingNodeNum):       
        temp = generateHopPattern(availChanList,hoppingWidth[i])
        if hoppingChanList != []:  # if not empty
            while not isCollisonFree(temp, hoppingChanList):
                temp = generateHopPattern(availChanList,hoppingWidth[i])
        hoppingChanList.append(temp)
    
    return legacyChanList, imChanList, hoppingChanList, utilization
    


import random    
def generateHopPattern(availChanList, hopWidth):
    availHopChanList = availChanList
    temp = []
    for l in range(0,hopWidth):
        index = random.randint(0,len(availHopChanList)-1)
        temp.append(availHopChanList[index])
        del availHopChanList[index]
    availChanList += temp   # unknow issue, need restore   
    return temp

    
import fractions  
def isCollisonFree(hopPattern, exsitHopChanList):
    tag = True
    for i in range( len(exsitHopChanList) ):
        temp = exsitHopChanList[i]
        a = len(hopPattern)
        b = len(temp)
        lcm = a*b/fractions.gcd(a,b)
        hopPattern_ = hopPattern * (lcm/a)
        temp_ = temp * (lcm/b)        
        for j in range(lcm):
            if temp_[j] == hopPattern_[j]:
                tag = False
                break
       # print "%s collide with %s"%(hopPattern, exsitHopChanList)
    return tag
        
####################### Test Unit ############################################
if __name__ == '__main__':
#    t = generateHopPattern([3,8,4,5], 2)
#    print t
#    t2 = isCollisonFree([2,3], [[1,4],[5,6,7]])  # True
#    print t2
#    t3 = isCollisonFree([2,3], [[1,4],[3,5,6]])  #False
#    print t3
#     t4 = isCollisonFree([1,2], [[3,2,1]])  #False
#     print t4
    
#    a,b,c,d = channelAssignment([0,0,6,1], [2],5)
#    print a,b,c,d  #0.7
#    a,b,c,d = channelAssignment([0,0,6,1,1], [2,2],5)
#    print a,b,c,d  #0.8
    a,b,c,d = channelAssignment([0,0,6,1,1], [3,3],8)
    # even-odd rule,  crazy
    print a,b,c,d  #5/6


