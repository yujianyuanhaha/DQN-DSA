
# coding: utf-8

#


import numpy as np;
import tensorflow as tf;
from ToolBox import tools




class DeepQNetwork:
    def __init__(
           self,
           n_actions,  # int
           n_features, # num of channels, int
           learning_rate=0.01,
           reward_decay=0.9,
           lamda = 0.9,
           e_greedy=0.9,
           replace_target_iter=300,
           batch_size=32,
           e_greedy_increment=None,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.power = None # input   1*n_features
        self.observation = None # input from power  1*n_features
        self.reward_estimated = None # input from power  1*n_features
        self.lr = learning_rate
        self.gamma = reward_decay # discount factor
        self.lamda = lamda # eligible trace factor
        self.epsilon_max = e_greedy     # epsilon max value
        self.replace_target_iter = replace_target_iter  # num of steps that updating target-net's parameters
        self.memory_size = 300  #  size of memory box 
        self.batch_size = batch_size    # batch size
        self.epsilon_increment = e_greedy_increment 
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max # epsilon_greedy algorithm

        # record training times and decide when to update target-network 
        self.learn_step_counter = 0

        # initialize memory box [s, a, trace , r, s_]  size = n_features[1 * 2^#C vector] + #action[0~#C] + #reward[0~100] + trace +  n_features 
        self.memory = np.zeros((self.memory_size, n_features*2 + 3)) 
        self.memory_elig_trace = np.zeros((1,2**n_features))

        # build [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection(tf.global_variables, scope='target_net')
        e_params = tf.get_collection(tf.global_variables, scope='eval_net')

        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)] # updatge each layers' parameters


        self.sess = tf.Session()


        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []  




# Build Network
# There are two networks: Evaluate-Network and Target-Network
# Evaluate Network: Updating parameters in each step
# Target-Network: Updating parameters after several steps
#  E_N and T_N can be seen as an approximated Function
    def _build_net(self):
    
    # Build Evaluate-Network:
    # This Network has 3 layers 
    # s,q_t,r,a,trace are tensor
        self.s = tf.placeholder(tf.float32,[None,self.n_features],name = 'state') # receive observation 
        #self.q_target = tf.placeholder(tf.float32,[None,self.n_actions],name = 'Q_target') # receive Q_target
        self.r = tf.placeholder(tf.float32, [None, ], name='r')  # input Reward(memory + estiamted)
        self.a = tf.placeholder(tf.int32, [None, ], name='a')  # input Action
        self.elig_trace = tf.placeholder(tf.float32,[None, ], name='elig_trace')  # trace
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name = 's_') # receive observation_next
    
      
        
        w_initializer, b_initializer = tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
        
        with tf.variable_scope('eval_net'):

            e1 = tf.layers.dense(self.s, 20, tf.nn.relu, kernel_initializer=w_initializer,
                                 bias_initializer=b_initializer, name='e1')
            e2 = tf.layers.dense(e1, 30, tf.nn.relu, kernel_initializer=w_initializer,
                                 bias_initializer=b_initializer, name='e2')
            self.q_eval = tf.layers.dense(e2, self.n_actions, kernel_initializer=w_initializer,
                                          bias_initializer=b_initializer, name='q')

        
    
    # Build Target-Network:
    # This Network has same architecture 
    
    
        with tf.variable_scope('target_net'):
            t1 = tf.layers.dense(self.s_, 20, tf.nn.relu, kernel_initializer=w_initializer,
                                 bias_initializer=b_initializer, name='t1')
            t2 = tf.layers.dense(t1, 30, tf.nn.relu, kernel_initializer=w_initializer,
                                 bias_initializer=b_initializer, name='t2')
            self.q_next = tf.layers.dense(t2, self.n_actions, kernel_initializer=w_initializer,
                                          bias_initializer=b_initializer, name='t3')
        
            
            
        with tf.variable_scope('q_target'):
            q_target = self.r + self.gamma * tf.reduce_max(self.q_next, axis=1, name='Qmax_s_') * self.elig_trace
            self.q_target = tf.stop_gradient(q_target)
        
        with tf.variable_scope('q_eval'):
            a_indices = tf.stack([tf.range(tf.shape(self.a)[0], dtype=tf.int32), self.a], axis=1)
        # something will happen here
            self.q_eval_wrt_a = tf.gather_nd(params=self.q_eval, indices=a_indices)    # shape=(None, )
            
        with tf.variable_scope('loss'):
        #self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval_wrt_a, name='TD_error'))
        
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)




    def store_transition(self,s, a, r, s_, method = 0,threshold_distance = 0):
        if not hasattr(self, 'memory_counter'): # check whether self has 'memory_counter'
            self.memory_counter = 0

    # stock method
        if method == 0:
            
            transition = np.zeros((1,self.n_features*2 + 3))
        
        #store eligibility trace
            if (1 in self.observation):  # observation should be np.array
                temp_loc = np.where(self.observation==1)
                for i in range(len(temp_loc)):
                    temp_sum = 2**temp_loc[i]

                index_state = temp_sum.sum()
                temp_elig_trace = self.gamma * self.lamda * self.memory_elig_trace[0,index_state] + 1
                self.memory_elig_trace[0,index_state] = temp_elig_trace 
           
            else:
                temp_elig_trace = self.gamma * self.lamda * self.memory_elig_trace[0,0] + 1
                self.memory_elig_trace[0,0] = temp_elig_trace

            transition[0,:self.n_features] = s
            transition[0,self.n_features] = a
            transition[0,self.n_features+1] = r
            transition[0,self.n_features+2] = temp_elig_trace
            transition[0,-self.n_features:] = s_

    # because memory's size is fixed, so the new sample will replace the oldest one.
            index = self.memory_counter % self.memory_size
            self.memory[index, :] = transition 

            self.memory_counter += 1
        
        else:
        # Norm-2 method
            threshold__distance = 3
        




    def choose_action(self):
    # transform observation vector to observation matrix to satify tensorflow
    # epsilon greedy algorithm

    #temp_observation = self.observation[np.newaxis, :]
        temp_observation = self.observation.copy()

        if np.random.uniform() < self.epsilon:
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: temp_observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)   
        return action





    def learn(self):
    
    # After replace_target_iter steps, we will update target-net's parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op) # self.sess.run(_replace_target_parameters())
            print('\ntarget_parameters _replaced\n')
        
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size,size = self.batch_size,replace = False) # pick batch from memory, without replacement
        else:
            sample_index = np.random.choice(self.memory_counter,size = self.batch_size)
        batch_memory = self.memory[sample_index,:]
    # add some guess samples
        temp_guess = self.addEstimatedSample()
        batch_memory = np.vstack((batch_memory,temp_guess))
    
    
        _, cost = self.sess.run(
            [self._train_op, self.loss],
            feed_dict={
            ###  recall the structure of memory  [s_n_features,action,reward,trace,s_next_n_feature]
                self.s: batch_memory[:, :self.n_features],
                self.a: batch_memory[:, self.n_features],
                self.r: batch_memory[:, self.n_features + 1],
                self.elig_trace: batch_memory[:, self.n_features + 2],
                self.s_: batch_memory[:, -self.n_features:],
        })

        self.cost_his.append(cost)


    # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1




    def addEstimatedSample(self):
         if (1 in self.observation):  # s should be np.array
             temp_loc = np.where(self.observation==1)
             for i in range(len(temp_loc)):
                 temp_sum = 2**temp_loc[i]
             index_state = temp_sum.sum()
         else:
             index_state = 0
         trace = self.memory_elig_trace[0,index_state]
         trunk = int(np.ceil(self.n_features/3))
         r_temp = np.sort(self.reward_estimated)
         select = r_temp[0,-trunk:]
         temp_memory = np.zeros((trunk, self.n_features*2 + 3))
         s = (self.observation.reshape(1,self.n_features)).copy()
         for i in range(trunk):
             index = np.where(self.reward_estimated == select[i])
             temp_index = index[1][0]
             a = temp_index + 1
             r = select[i]
             s_ = (self.observation[:]).reshape(1,self.n_features)
             s_[0,temp_index] = 1

             temp_memory[i,:self.n_features] = s 
             temp_memory[i,self.n_features] = a
             temp_memory[i,self.n_features + 1] = r
             temp_memory[i,self.n_features + 2] = trace
             temp_memory[i,-self.n_features:] = s_
 
             s_[0,index] = 0
     
         return temp_memory




    def measureRandO(self,power):
        self.power = power
        observation = tools.createObservation(self.power,threshold_obs = 45)
        observation.reshape(1,self.n_features)
        reward_estimated = tools.createReward(self.power,threshold_r = 45)
        reward_estimated.reshape(1,self.n_features)
        self.observation = observation # np.array (n_features,0)
        self.reward_estimated = reward_estimated #np.array (n_features,0)
        return observation





    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

