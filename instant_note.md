#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:12:55 2018

@author: Jet
"""
--------------------------------------------------------------------------------
Headline
1. BE IN LAB 10am-1am 5pm-7pm breaks
2. less turnover time


--------------------------------------------------------------------------------
A. ToDoList
1. Week
[x] Code Run Fri 
[x] Draft Report Fri
[ ] 

#Wed - GlobelComm Due XXX
#Mon - slides w/ full figure XXXX

2. Day


Thur
[ ] - debug multiple DQN node
[ ] - scale up



Tue
[ ] - debug


Mon - [ ] dsa Node debug
    - [ ] intermittent node design 



----------------------------------------------
Sat - [x] run through DQN
    - [x] vs DQN
    - [ ] flexiable nodeType List
    - [ ] *DQN tricks, double Q, policy, priotity
    - [ ] *intermitent node

--------------------------------------------------------------------------------
B. Logs



Sun
[] - DQN learn hopping, detail metric
[] - the spectrum period of MDP? wrong conclusion, seems MDP has lower baseline of compution



Mon
1. DSA avoid legacy, but not hopping

days are easier
1. more reflection about workflow, coding style, understanding of DQN, writing and some others

[X]. detail running time
[X]. exp episolon e-geedy to reduce random 
    - perfect
    - full API for different decay
2. flexiable nodeType, init pattern, capacity check <
3. 8+ channel
4. refine code, input/output, wrap plot, multiple run
[X]. auto save & naming figure
6. tensorboard setoff
5. DSA node
6. hidden node/expose node
[ ]. learn to WAIT (NOT EASY JOB)
8. DQN tricks
9. ARC steup


1. test MDP if explorePorb type matters
    - tiny, perf seems better a little bit, do it later

--------------------------------------------------------------------------------
C. Debug

1. the dsa bug
    full understand other code, step by step
    final - '(array([], dtype=int64),)' is mistake as 'False', but programmes take it for 'True'
    use '(array([], dtype=int64),) == True' instead




1. DQN random[FIXED]
    - the observedState never change, same of MDP
    - output converge at action 3, right answer, why plot wrong?
    - go and see coolisionHist, doubt epsilion 90% too high
    - fixed XD
        
2. interminent node not doing right

3. learn step 5 -> 0 

4. channel utility

5. the multiple DQN bug


 

--------------------------------------------------------------------------------
D. Miscellaneous
[X]. How to tell computing time in each time slot?
    - hard to tell
2. Wil legacy with txProb work?
    - Yes, it did work for 0.9 or 0.5
    - for 0.5, it GIVE UP
    - bug so far,all 0 does not mean choose channel 0(ToDo)
2. intermittent Node
3. even 2 MDP, 2 legacy, the performance of MDP is not the same? always the former better? (ToDo)

4. the setup "always choose the first of available channel", the order matter if dsa choose before dqn
however, we need to remove the assumption.


---------------------------------------------------------------
E. Findings
1. MDP is "influence" by hopping, it would hopping to occupy several channels even there is a full channel.




