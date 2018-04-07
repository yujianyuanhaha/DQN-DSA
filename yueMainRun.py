# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:57:53 2018

@author: yuexu
"""

import numpy as np;
import tensorflow as tf;


from Comm_Env import Comm_env_test # communication test env 
from DQN_brain import DeepQNetwork

def run_Comm():
    step = 0    # control when to study
    for episode in range(1000): # 300 episodes
        # initalize Comm.env
        print('episode is ' + str(episode))
        power = env.reset(10)
        accumReward = 0
        done = False 
        print(power)
        #input("Press Enter to continue...")


        while True:
            
            

            observation = RL.measureRandO(power)
            #print('ob is ' + str(observation))
            
            # DQN 根据观测值选择行为
            action = RL.choose_action()
            print('action is ' + str(action))

            # 环境根据行为给出下一个 state, reward, 是否终止
            observation_, reward, done, accumReward = env.interact(action, accumReward, done)
            #print('o_' + str(observation_))
            print('r is ' + str(reward))
            print('acRe is' + str(accumReward))
            
            RL.store_transition(observation, action, reward, observation_)
            #print('storing end!')


            # 控制学习起始时间和频率 (先累积一些记忆再开始学习)
            if (step > 200) and (step % 5 == 0):
                RL.learn()
                print('Learning End!')

            # 将下一个 state_ 变为 下次循环的 state
            power = env.updateEnv(action)
            #print('Updating End!')

            # 如果终止, 就跳出循环

            
            print(done)
            if done:
                break
            step += 1   # 总步数
            print(step)
            #if step == 200:
                #print('200 !!!')
                #input("Press Enter to continue...")
                

    # end of timeslot
    print('Timeslot End!')

if __name__ == "__main__":
    env = Comm_env_test()
    RL = DeepQNetwork(11, 10,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,  # 每 200 步替换一次 target_net 的参数

                      )
    run_Comm()
    print('Over!')
    RL.plot_cost()  # 观看神经网络的误差曲线