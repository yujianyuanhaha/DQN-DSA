#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 02:57:37 2018

@author: Jet
"""

# functions
import numpy as np

# [~,stateIndex] = ismember(self.stateHist[stepNum-1,:], self.states,'rows') 
# TODO - the import issue
#def ismember(A,B):
#    length = np.shape(A)[0]
#    Locb = np.zeros(length)
#    for i in range(0,length):
#        for j in range(0, np.shape(B)[0]):
#            if all(A[i,:] == B[j,:]):
#                Locb[i]= j
#                break
#    return np.transpose( [Locb] )



def ismember(a,B):
    t = 0           
    for j in range(0, np.shape(B)[0]):
        if all(a == B[j,:]):
            t = j
            break
    return t

# if no match, return 0
# possible one line function    