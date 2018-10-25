# Why Experience Replay Matters
* [stackoverflow](https://datascience.stackexchange.com/questions/20535/what-is-experience-replay-and-what-are-its-benefits)    

    Advantages of experience replay:    

    More efficient use of previous experience, by learning with it multiple times. This is key when gaining real-world experience is costly, you can get full use of it. The Q-learning updates are incremental and do not converge quickly, so multiple passes with the same data is beneficial, especially when there is low variance in immediate outcomes (reward, next state) given the same state, action pair.   

    Better convergence behaviour when training a function approximator. Partly this is because the data is more like i.i.d. data assumed in most supervised learning convergence proofs.    

    Disadvantage of experience replay:  

    It is harder to use multi-step learning algorithms, such as Q(λ), which can be tuned to give better learning curves by balancing between bias (due to bootstrapping) and variance (due to delays and randomness in long-term outcomes). Multi-step DQN with experience-replay DQN is one of the extensions explored in the paper Rainbow: Combining Improvements in Deep Reinforcement Learning.    


* [Rainbow: Combining Improvements in Deep Reinforcement Learning by D. Silver](https://arxiv.org/pdf/1710.02298.pdf)    
     multi-step learning

     
* [A Deeper Look at Experience Replay by Sutton](https://arxiv.org/pdf/1712.01275.pdf)

* [The importance of experience replay databasecomposition in deep reinforcement learning](http://rll.berkeley.edu/deeprlworkshop/papers/database_composition.pdf)  
    1. increased efficiency. Experience replay helpsto increase the sample efficiency by allowing samples to be reused.    
    2. experience replay allows for mini-batch updates which helps the **computational efficiency**, especially when the training is performed on a GPU. 
    3.  improves the stability of theDDPG learning algorithm in several ways:   
        (a).  helps stabilize thelearning process is that it is used to break the temporal correlations of the neural network learningupdates. Without an experience database, the updates of (2), (3) would be based on subsequentexperience samples from the system. These samples are highly correlated since the state of thesystem does not change much between consecutive time-steps. For real-time control, this effectis even more pronounced with high sampling frequencies. Theproblem this poses to the learningprocess is that most mini-batch optimization algorithms are based on the assumption of independentand identically distributed data [1]. Learning from subsequent samples would **violate this i.i.d.**      
        (b). nsuringthat the experiences used to train the networks are not only based on the most recent policy


# Bib
1. Hessel, Matteo, et al. "Rainbow: Combining improvements in deep reinforcement learning." arXiv preprint arXiv:1710.02298 (2017).    
    ```
    @article{hessel2017rainbow,
    title={Rainbow: Combining improvements in deep reinforcement learning},
    author={Hessel, Matteo and Modayil, Joseph and Van Hasselt, Hado and Schaul, Tom and Ostrovski, Georg and Dabney, Will and Horgan, Dan and Piot, Bilal and Azar, Mohammad and Silver, David},
    journal={arXiv preprint arXiv:1710.02298},
    year={2017}
    }
    ```
2. Zhang, Shangtong, and Richard S. Sutton. "A Deeper Look at Experience Replay." arXiv preprint arXiv:1712.01275 (2017).   
    ```
        @article{zhang2017deeper,
        title={A Deeper Look at Experience Replay},
        author={Zhang, Shangtong and Sutton, Richard S},
        journal={arXiv preprint arXiv:1712.01275},
        year={2017}
        }
    ```
3. de Bruin, Tim, et al. "The importance of experience replay database composition in deep reinforcement learning." Deep Reinforcement Learning Workshop, NIPS. 2015.
```
    @inproceedings{de2015importance,
    title={The importance of experience replay database composition in deep reinforcement learning},
    author={de Bruin, Tim and Kober, Jens and Tuyls, Karl and Babu{\v{s}}ka, Robert},
    booktitle={Deep Reinforcement Learning Workshop, NIPS},
    year={2015}
}
```
