bibliography sum up of the Deep Reinforcement Learning on Dynamic Channel Access Project.

# General Survey


* [Luong, Nguyen Cong, et al. "Applications of Deep Reinforcement Learning in Communications and Networking: A Survey." arXiv preprint arXiv:1810.07862 (2018).](https://arxiv.org/pdf/1810.07862.pdf)
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:iEhzRRZvQrYJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9CVAnWnMKdFrlWDUeGix1vFg0KC1ZJI&scisf=4&ct=citation&cd=-1&hl=en)
    * []
    * (+) cover many other work besides dynamic channel access, such as rate control, cache, offload and security
    * (+) cover pratical details such as multi-agent


# Classic Method

# Recent peer's work



* [Lu, Xiaozhen, Liang Xiao, and Canhuang Dai. "UAV-Aided 5G Communications with Deep Reinforcement Learning Against Jamming." arXiv preprint arXiv:1805.06628 (2018).](https://arxiv.org/pdf/1805.06628.pdf)
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:9V72XjAHCxgJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9CXHajwPLTyO54Ziru6khCZdceCUXcY&scisf=4&ct=citation&cd=-1&hl=en)
    * []
    * (+) apply **Tranfer Learning** to fast initial CNN
    * (+) claim to convergecast in 200 steps.
    * (-) lack technic details

# DQN Family & Dr. Silver work
Method  | Author | Afflicate | comment  | Bibtex | paper | abbreviation   
------------ | ------------- | ------------- | -------------| -------------| -------------| -------------
DQN | Mnih | Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:uiYh7C2joKwJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ev86XyGckKO1SwAJ-aFRN3_NsYro-n&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1312.5602.pdf)  | [mnih2015human]     
Double DQN |Van Hasselt | Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:Fn1meBxKdgMJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9ExiUYQZTnQhj968rfYoJBkvRNwBpO_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/download/12389/11847)  | [van2016deep]    
Prioritized DQN | Tom Schaul| Google DeepMind |- | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:xQqjDYKSnJUJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Eb7fqdkvFv0fT_Y5_Ym3D2v_AiTftD&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.05952)  | [schaul2015prioritized]    
Dueling DQN | Wang, Ziyu | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.06581)  | [wang2015dueling]   
Asynchronous DQN | Mnih | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:YW9AmGuXrcgJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E13K68hY-5jd1K3HO1n_Ja33FF-_l0&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1511.06581)  | mnih2016asynchronous]   
Distributional DQN | Marc G. Bellemare | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:mXZqOSjsZegJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E26dJsbarff-6SQqK-IojcJj4OIiJk&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1707.06887)  | [wang2015dueling]   
Noisy Nets DQL | Meire Fortunato | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1706.10295)  | [wang2015dueling]   
Rainbow DQN | Matteo Hessel | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:AKnVTHmGxq0J:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9Ec88MyvOfMNM4O7Uq2eh9TE-l-jbT_&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1710.02298.pdf)  | [hessel2017rainbow]   
Deep Deterministic Policy Gradient (DDPG) |David Silver | Google DeepMind | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:M5PDD9OWLCAJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E5NnoOBgVXowmnWaKFWhRHnXfLNlka&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](http://proceedings.mlr.press/v32/silver14.pdf)  | [silver2014deterministic]   
Distributed Proximal Policy Optimization (DPPO)  |John Schulman | OpenAI | - | [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:apL6FsUh-SQJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9E6CfJM9_46O33fqRFqs76J5z8YGcBU&scisf=4&ct=citation&cd=-1&hl=en)   | [paper](https://arxiv.org/pdf/1707.06347.pdf)  | [schulman2017proximal]   


# POMDP
* DRNQ - [Deep Recurrent Q-Learning for Partially Observable MDPs](https://arxiv.org/pdf/1507.06527.pdf) - by Matthew Hausknecht, UTA, Jul 2015 .
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:8OHjZ0rzTZYJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9HSsKVkzhePmb0bDaO_aZXjYKKBihUS&scisf=4&ct=citation&cd=-1&hl=en)
    * [hausknecht2015deep]



* POMCP - [Monte-Carlo planning in large POMDPs](http://papers.nips.cc/paper/4031-monte-carlo-planning-in-large-pomdps.pdf) - by David Silver, MIT, 2010.    
    * [BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:VavDmV-qsioJ:scholar.google.com/&output=citation&scisig=AAGBfm0AAAAAW9HTSwdqmPPetj8N2rSAF-rNza0apO8x&scisf=4&ct=citation&cd=-1&hl=en)
    * [silver2010monte]