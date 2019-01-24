from puzzels import Simple
from GPSARSA.gpsarsa import GPSARSA
import numpy as np
from GPSARSA.Epsilon_greedy import epsilon_greedy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

size  = 10
puzz = Simple(size, 2)

S = np.zeros(shape=(2,size*size))
for i in range(size):
    for j in range(size):
        n = i*10 + j
        S[0][n] = j
        S[1][n] = i

S = np.array(S)

start = [0,0]
x= start[0]
y= start[1]
G = GPSARSA(0.2,0.000000005,1,[x, y], -1, constant_white_noise=100)
G.iterate([x,y], -1)

for i in range(10):
    start = [0,0]
    x= start[0]
    y= start[1]

    R = -1
    steps = 0
    while R != 5:
        R = puzz.reward(x,y)

        next_actions = puzz.next_action(x,y)
        new_state = epsilon_greedy(G, next_actions, 0.2, puzz)


        x = new_state//10
        y = new_state%10

        steps += 1

        G.iterate([x,y], puzz.reward(x, y))

    print(steps)
mean = puzz.action_into_puzzle(G)
optimal = puzz.action_into_puzzle_max(G)
var = puzz.var_into_puzzle(G)
print(len(G.D))
print(mean)
print(optimal)
print(var)
#PLOTTING
fig = plt.figure()
ax = fig.gca(projection='3d')


X = np.array([i for i in range(10)])
xlen = len(X)
Y = np.array([i for i in range(10)])
ylen = len(Y)

X, Y = np.meshgrid(X, Y)


colortuple = ('y', 'b')
colors = np.empty(X.shape, dtype=str)
for y in range(ylen):
    for x in range(xlen):
        colors[x, y] = colortuple[(x + y) % len(colortuple)]

# Plot the surface with face colors taken from the array we made.
surf = ax.plot_surface(X, Y, mean.T, facecolors=colors, linewidth=0)

# Customize the z axis.

ax.w_zaxis.set_major_locator(LinearLocator(6))
plt.title("GPSARASA Value function Map for a grid with path and 5 0 -1 reward")
plt.xlabel("x")
plt.ylabel('y')


#plt.savefig("GP_SARAS_-1_0_reward.png")

print("D_len = ", G.D_len)
plt.show()


start = [0,0]
x= start[0]
y= start[1]
R = -1
steps = 0

while R != 5:
    R = puzz.reward(x,y)
    next_actions = puzz.next_action(x,y)
    new_state = epsilon_greedy(G, next_actions, 0.7, puzz)


    x = new_state//10
    y = new_state%10


    steps += 1




print(steps)

