
# coding: utf-8

# In[1]:
import numpy as np

class tools: 
    def createReward(Power_Sensing,threshold_r = 45):
        
        temp_r = np.array(Power_Sensing)
        p_max = temp_r.max()
 
        reward_estimated = (p_max - temp_r) / p_max * 100
        print('R_es is ' + str(reward_estimated))
        reward_estimated[reward_estimated < threshold_r] = 0
        print('afte R_es is ' + str(reward_estimated))
       
        return reward_estimated


# In[2]:


    def createObservation(Power_Sensing,threshold_obs = 45):
        
        observation = np.array(Power_Sensing)
        observation[observation <= threshold_obs] = 0
        observation[observation > threshold_obs] = 1
        
        return observation


# In[3]:


    def reversePower(powerValue,threshold_p = 45):
        
        if powerValue < threshold_p:
            reversedPower = 60 + int(np.random.rand() * 60 - 30)
        else:
            reversedPower = 20 + int(np.random.rand() * 45 - 10)
            
        return reversedPower





