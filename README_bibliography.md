README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018
------------------------------------------------------------------------------------------------------------------------------------

Bibliography sum up of the Deep Reinforcement Learning on Dynamic Channel Access Project.


# Related Files
* [bibliography.bib]() for conference or journal writing.
* [ Illustration Graphs]() for conference or journal writing.
* [ Equations, Algorithms & Tables]() for conference or journal writing.





# General Survey
* [Arulkumaran, Kai, et al. "A brief survey of deep reinforcement learning." arXiv preprint arXiv:1708.05866 (2017).](https://arxiv.org/pdf/1708.05866)

* [Luong, Nguyen Cong, et al. "Applications of Deep Reinforcement Learning in Communications and Networking: A Survey." arXiv preprint arXiv:1810.07862 (2018).](https://arxiv.org/pdf/1810.07862.pdf)
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:iEhzRRZvQrYJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9CVAnWnMKdFrlWDUeGix1vFg0KC1ZJI&scisf=4&ct=citation&cd=-1&hl=en)
    * [luong2018applications]
    * (+) cover many other work besides dynamic channel access, such as __rate control__, __cache__, offload and security, part of them could be our further work.
    * (+) cover pratical details such as __multi-agent__
* [Chen, Mingzhe, et al. "Machine learning for wireless networks with artificial intelligence: A tutorial on neural networks." arXiv preprint arXiv:1710.02913 (2017).](https://arxiv.org/pdf/1710.02913.pdf)
    * list __liquid state machine__ / __echo state machine__
    * (-) skip DQN

# Classic Method
## myopic
* [Zhao, Qing, Bhaskar Krishnamachari, and Keqin Liu. "On myopic sensing for multi-channel opportunistic access: structure, optimality, and performance." IEEE Transactions on Wireless Communications 7.12 (2008).](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4723352)  
        * (+) achieve 66.7% rate when coexist with __stochastic channel__, the Gilber-Elliot/ 2-state Makov Chain Model. 
        * (-) limited, work for small scale channel case. 
        * [zhao2008myopic] 
## MDP
* [Zhang, Yalin, et al. "Model free dynamic sensing order selection for imperfect sensing multichannel cognitive radio networks: A Q-learning approach." Communication Systems (ICCS), 2014 IEEE International Conference on. IEEE, 2014.](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7024826)
    * (+) imprefect sensing analyze
    * (+) Q-learning
    * (-) sense-tx procedure is not real learning


# Recent peer's work

* [Wang, Shangxing, et al. "Deep reinforcement learning for dynamic multichannel access in wireless networks." IEEE Transactions on Cognitive Communications and Networking (2018).](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8303773)
    * __first journal__, IEEE TRANSACTIONS ON COGNITIVE COMMUNICATIONS AND NETWORKING, VOL. 4, NO. 2, JUNE 2018, First paper __apply DQN on channel access__
    * USC
    * [wang2018deep]



* [Yu, Yiding, Taotao Wang, and Soung Chang Liew. "Deep-reinforcement learning multiple access for heterogeneous wireless networks." 2018 IEEE International Conference on Communications (ICC). IEEE, 2018.](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8422168)
    * Time slot aceess
    * [yu2017deep]

* [Tsiligkaridis, Theodoros, and David Romero. "Accelerated Reinforcement Learning Algorithms with Nonparametric Function Approximation for Opportunistic Spectrum Access." arXiv preprint arXiv:1706.04546 (2017).](https://arxiv.org/pdf/1706.04546)
    * MIT 
    * (+)reduce state space in a math way, rather than neural network
    * [tsiligkaridis2017accelerated]
* [Naparstek, Oshri, and Kobi Cohen. "Deep multi-user reinforcement learning for dynamic spectrum access in multichannel wireless networks." arXiv preprint arXiv 1704 (2017).](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8254101)
    * (+) first handle __multi-agent learning__, first implement __DRQN in LSTM__, where author treat _distribute observation as the partial observation_. 
    * [30 page version](https://arxiv.org/pdf/1704.02613.pdf)
    * [naparstek2017deep]

---
After July 2018

* [Lu, Xiaozhen, Liang Xiao, and Canhuang Dai. "UAV-Aided 5G Communications with Deep Reinforcement Learning Against Jamming." arXiv preprint arXiv:1805.06628 (2018).](https://arxiv.org/pdf/1805.06628.pdf)
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:9V72XjAHCxgJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9CXHajwPLTyO54Ziru6khCZdceCUXcY&scisf=4&ct=citation&cd=-1&hl=en)
    * [lu2018uav]
    * (+) apply **Tranfer Learning** to fast initial CNN
    * (+) claim to convergecast in 200 steps.
    * (-) lack technic details

* [Wang, Leye, et al. "Cell Selection with Deep Reinforcement Learning in Sparse Mobile Crowdsensing." arXiv preprint arXiv:1804.07047 (2018).](https://arxiv.org/pdf/1804.07047.pdf) 
    * [wang2018cell]
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:XWTN3jWWLNoJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9H0jrnscHn0KWRuwE2rNlvI982Sdsaz&scisf=4&ct=citation&cd=-1&hl=en)
    * (+) apply DRQN to solver partial observation
    * (+) transfer learning

# DQN Family & Dr. Silver work

## Sutton TextBook
* Sutton, Richard S., Andrew G. Barto, and Francis Bach. Reinforcement learning: An introduction. MIT press, 1998.
* [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:sGQzs-IYknYJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9H5bq_slhoZVa-gm3j94rQ4c_ICkusT&scisf=4&ct=citation&cd=-1&hl=en)


## DQN Family
Method  | Author | Afflicate | comment  | Bibtex | paper | abbreviation  |  openSource   
------------ | ------------- | ------------- | -------------| -------------| -------------| -------------| -------------
 DQN | Mnih | Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:uiYh7C2joKwJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ev86XyGckKO1SwAJ-aFRN3_NsYro-n&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1312.5602.pdf)  | [mnih2015human]   | [DQN](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5_Deep_Q_Network)  
Double DQN |Van Hasselt | Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:Fn1meBxKdgMJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9ExiUYQZTnQhj968rfYoJBkvRNwBpO_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/download/12389/11847)  | [van2016deep]  |  [Double DQN](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5.1_Double_DQN)    
Prioritized DQN | Tom Schaul| Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:xQqjDYKSnJUJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Eb7fqdkvFv0fT_Y5_Ym3D2v_AiTftD&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.05952)  | [schaul2015prioritized]    |  [Pri DQN](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5.2_Prioritized_Replay_DQN)    
Dueling DQN | Wang, Ziyu | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.06581)  | [wang2015dueling]   |  [Duel DQN](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5.3_Dueling_DQN)    
Asynchronous DQN | Mnih | Google DeepMind | Asynchronous Advantage Actor Critic (A3C) + RNN with continuous action space | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:YW9AmGuXrcgJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E13K68hY-5jd1K3HO1n_Ja33FF-_l0&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.06581)  | mnih2016asynchronous]  |  [Asyn DQN](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents10_A3C)     
 Distributional DQN | Marc G. Bellemare | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:mXZqOSjsZegJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E26dJsbarff-6SQqK-IojcJj4OIiJk&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1707.06887)  | [wang2015dueling]   
Noisy Nets DQL | Meire Fortunato | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1706.10295)  | [wang2015dueling]   
Rainbow DQN | Matteo Hessel | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1710.02298.pdf)  | [hessel2017rainbow]   
Deep Deterministic Policy Gradient (DDPG) |David Silver | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:M5PDD9OWLCAJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E5NnoOBgVXowmnWaKFWhRHnXfLNlka&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](http://proceedings.mlr.press/v32/silver14.pdf)  | [silver2014deterministic]   |  [DDPG](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/9_Deep_Deterministic_Policy_Gradient_DDPG)    
Distributed Proximal Policy Optimization (DPPO)  |John Schulman | OpenAI | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:apL6FsUh-SQJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E6CfJM9_46O33fqRFqs76J5z8YGcBU&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1707.06347.pdf)  | [schulman2017proximal]   |  [DDPO](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/12_Proximal_Policy_Optimization)    


## POMDP
* DRNQ - [Deep Recurrent Q-Learning for Partially Observable MDPs](https://arxiv.org/pdf/1507.06527.pdf) - by Matthew Hausknecht, UTA, Jul 2015 .
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:8OHjZ0rzTZYJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9HSsKVkzhePmb0bDaO_aZXjYKKBihUS&scisf=4&ct=citation&cd=-1&hl=en)
    * [hausknecht2015deep]



* POMCP - [Monte-Carlo planning in large POMDPs](http://papers.nips.cc/paper/4031-monte-carlo-planning-in-large-pomdps.pdf) - by David Silver, MIT, 2010.    
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:VavDmV-qsioJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9HTSwdqmPPetj8N2rSAF-rNza0apO8x&scisf=4&ct=citation&cd=-1&hl=en)
    * [silver2010monte]

# How to cite a Github open source
1. [morvan's github](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow) for DQN famlily
```
@misc{Mofan2013,
  author = {Mofan Zhou},
  title = {Reinforcement-learning-with-tensorflow},
  year = {2016},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow}},
  commit = {81fea33905c7f81719ec031eab51c68225eb7cce}
}
```


* [how to make your codes citable](https://guides.github.com/activities/citable-code/)