#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:12:55 2018

@author: Jet
"""
--------------------------------------------------------------------------------
Head
1. BE IN LAB 10am-1am 5pm-7pm breaks
2. less turnover time


--------------------------------------------------------------------------------
A. ToDoList
1. Week
Wed - GlobelComm Due
Mon - slides w/ full figure

2. Day
Sat - [x] run through DQN
    - [x] vs DQN
    - [ ] flexiable nodeType List
    - [ ] *DQN tricks, double Q, policy, priotity
    - [ ] *intermitent node

--------------------------------------------------------------------------------
B. Logs
0. detail running time
1. exp episolon e-geedy to reduce random 
    - perfect
    - full API for different decay
2. flexiable nodeType, init pattern, capacity check <
3. 8+ channel
4. refine code, input/output, wrap plot, multiple run
5. auto save & naming figure
6. tensorboard setoff
5. DSA node
6. hidden node/expose node
7. learn to WAIT
8. DQN tricks
9. ARC steup


1. test MDP if explorePorb type matters
    - tiny, perf seems better a little bit, do it later





--------------------------------------------------------------------------------
C. Debug
1. DQN random[FIXED]
    - the observedState never change, same of MDP
    - output converge at action 3, right answer, why plot wrong?
    - go and see coolisionHist, doubt epsilion 90% too high
    - fixed XD
    
    
2. interminent node not doing right



--------------------------------------------------------------------------------
D. Miscellaneous
1. How to tell computing time in each time slot?
    - hard to tell
2. Wil legacy with txProb work?
    - Yes, it did work for 0.9 or 0.5
    - for 0.5, it GIVE UP
    - bug so far,all 0 does not mean choose channel 0(ToDo)
2. intermittent Node








