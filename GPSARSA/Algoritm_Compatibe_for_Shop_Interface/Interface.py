
import numpy as np

#give two vectores one representing the location and another representing the attributes
def state_representation(location_array, attrbute_array, alpha = 0.1, beta= 0.01):

    return alpha*np.array(location_array) + beta*np.array(attrbute_array)

def state_creation(States, Adjacent_State, new_state):

    distance_array = np.array(States)- np.array(new_state)
    euclidian_array = np.array([np.dot(distance_array[j], distance_array[j]) for j in range(len(x)) ])
    s = np.argsort(euclidian_array)
    for k in range(3):
        States.append(new_state)
        Adjacent_State[-1][k] = States[s[k]]

    r= np.random.randint(0, len(States)-1)
    Adjacent_State[-1][-1] = States[s[r]]


