import numpy as np
import matplotlib.pyplot as plt


P = [[-1 for i in range(10)] for j in range(10)]
P[5][8] = 5
P[7][2] = 5

P[1][1] = 0
P[2][2] = 0
P[3][2] = 0
P[4][2] = 0
P[5][2] = 0
P[6][2] = 0


fig, ax = plt.subplots()
im = ax.imshow(P)

for i in range(10):
    for j in range( 10):
        text = ax.text(j, i, P[i][ j],
                       ha="center", va="center", color="w")

ax.set_title("Map of the grid")
fig.tight_layout()
plt.show()


