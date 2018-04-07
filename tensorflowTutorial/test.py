import tensorflow as tf
import numpy as np
 
s_temp = tf.placeholder(tf.float32,[1,5],name = 's_temp')
 
with tf.Session() as sess:
    rand_array = np.zeros((1,5))
    print(sess.run(s_temp, feed_dict={s_temp: rand_array}))  # Will succeed.
   
print type(s_temp)
print type(tf.eval(s_temp))