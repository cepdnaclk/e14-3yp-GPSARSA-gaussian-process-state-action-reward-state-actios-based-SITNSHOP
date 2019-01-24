from GPSARSA.gpsarsa import GPSARSA
from GPSARSA.Epsilon_greedy import epsilon_greedy

#This must run all the time

G =  GPSARSA(0.2,0.000000005,1,[0, 0], -1, constant_white_noise=100)

while(1):




    #GIVE THE STATES FROM THE ADJACENT STAES matrix in interface
    next_actions = []
    reward = [] #Array of rewards corresponding to each state
    new_state = epsilon_greedy(G, next_actions, 0.2, reward)

    #RUN THE FUNCTION THAT GIVES A REWARD WHEN APPLIED new_state_reward=  fun(state
    new_state_reward = 0
    G.iterate(new_state, new_state_reward)

    #GIVE THE NEW STATE TO THE USER AS THE NEXT SUGESSION
    



