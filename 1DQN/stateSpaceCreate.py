#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 11:59:54 2018

@author: Jet

Matlab code
*********************************
function states = stateSpaceCreate(numChans)
    for dec = 0:2^(numChans)-1
        binStr = dec2bin(dec,numChans);
        %     dec2bin(D,N) produces a binary representation with at least N bits.
        % Example dec2bin(23) returns '10111'
        
        binVect = zeros(1,numChans);
        for k = 1:numChans
            binVect(k) = str2double(binStr(k));
        end

        states(dec+1,:) = binVect;
    end
end
********************************
first python starter
less print or comment out; more debug; more robust
INSTANT NOTE
1. decimal to bin
    bin()
2. numpy zeros()
    numpy.zeros(shape, dtype=float, order='C') 
3.  np.r_ / np.c_
    concatenate matrix or array 
    e.g np.r_['0,2',  [ [1,2,3],[4,5,6] ],  [7,8,9]]
    we get array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])   ## why not matrix 


********************************

"""
import numpy as np

def stateSpaceCreate(numChans):
    states = [ np.zeros( numChans ) ]
    for dec in range(1, 2**(numChans)):
        binStr = bin(dec)
        binStr = binStr[2:].zfill(numChans)   #OR format(binStr, 'b') to emit '0b'
        binVect = np.zeros( numChans )
        for k in range(0, numChans):
           binVect[k] = float(binStr[k]);  # emit '0b', start from 3rd one
        states = np.concatenate((states, [binVect]), axis=0)   # damn [ ]  tricky stuff       
    return states   

if __name__ == '__main__':
    states = stateSpaceCreate(4)
#    print states        