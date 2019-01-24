import numpy as np



def epsilon_greedy(GPSARSA, next_actions, epsilon, reward):

    next_action_value =  np.array([GPSARSA.iterate([i//10, i%10], reward[i], with_update=False)[0][0] for i in next_actions])


    x = np.random.binomial(n=1, p= epsilon, size=1)

    if x[0] == 1:
        ans =  next_actions[np.argmax(next_action_value)]

        return ans
    else:
        return next_actions[np.random.randint(len(next_action_value))]



