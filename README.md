README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018  

-------------------------------------------------------------------------
# Related Files:
1. The [Result Demo of DQN-DCA](https://drive.google.com/open?id=1Tl5y8Ov_P_Fwqt1SpoRLuaAqaTlG20mImVx5o15VUsY) of Google Slides, 
and figure come from VT Google Folder [qdnFig](https://drive.google.com/open?id=1hQxplvCs_hSfgr9rrJ-rywutUkHWwnxP) of .png .pdf 
figure autosave by python, notice we SEPERATE figure from github to avoid too frequent update git folder.
2. The [technic report](https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB) and 
the [latex folder](https://drive.google.com/open?id=1GeqjxzAroWrWHcM8LnwumbAo0h-ZYItX).
3. A backup of Chris(Dr. Headley) MDP codes of [MDP solver](https://drive.google.com/open?id=1rddetimeRR8MECEsv0KRfdV1uLvd-4ZQ).




# Overview  
This project work around applying **deep Q network**[1] in **dynamic channel access**.
It validate the performance of intelligent node acess channel without information exchange 
with other nodes(legacy, hopping, intermittent, dsa etc). It mainly concerns about convergency speed
 and scale issues.  
To be exact, we look into following aspects:  
1. coexsitence with other type of nodes
⋅⋅* legacy
⋅⋅* legacy with tx prob
⋅⋅* hopping
⋅⋅* intermittent
⋅⋅* dsa (able to wait)
⋅⋅* mdp 
⋅⋅* dqn
2. learn to wait
3. learn to occupy more than one channels
4. learn to avoid hidden nodes
5. learn to utilize spatial reuse (exposed nodes)
6. select good channels (when several channel available, some low quality channel bring low reward).  
The inspiration comes from SC2 competition, and some papers[2][3] have start some work around it.  
  
The project transfer Chris's code of MDP-DCA Matlab simulator as the starter with MDP python solver[4], and then adapot DQN python solver[5].  
Another repository[6] maintain by Yue would merge soon, and [7] is the technical report.  

# Reference:  
[1] Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning." Nature 518.7540 (2015): 529-533.  
[2] Wang, Shangxing, et al. "Deep Reinforcement Learning for Dynamic Multichannel Access in Wireless Networks." IEEE Transactions on Cognitive Communications and Networking (2018)  
[3] Yu, Yiding, Taotao Wang, and Soung Chang Liew. "Deep-Reinforcement Learning Multiple Access for Heterogeneous Wireless Networks." arXiv preprint arXiv:1712.00162 (2017).  
[4] https://github.com/sawcordwell/pymdptoolbox  
[5] https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5_Deep_Q_Network   
[7] https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB  



--------------------------------------------------------------------------
# Configuration  
We run codes on **Spyder** GUI under Anaconda, tensorflow is required as well as related tensorboard setup.  
For batch test, we run codes on ARC VT.   


--------------------------------------------------------------------------
# How to run the codes?  
Paramter all configurable at header part of **multiNodeLearning.py** OR **setup.config** file 
in terminal run:  
```
python multiNodeLearning.py
```
:sunglasses:






--------------------------------------------------------------------------