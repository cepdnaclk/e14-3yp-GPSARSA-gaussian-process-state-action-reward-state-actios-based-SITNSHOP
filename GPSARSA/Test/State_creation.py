import numpy as np
import matplotlib.pyplot as plt
import csv

X1 = []
Y1 = []

X2 = []
Y2 = []

X3 = []
Y3 = []


for i in range(1000):
    x = np.random.random()
    y = np.random.random()

    if (x-0.3)**2 + (y-0.2)**2 < 0.02:
        X1.append(x)
        Y1.append(y)

    if (x-0.32)**2 + (y-0.4)**2 < 0.01:
        X2.append(x)
        Y2.append(y)

    if (x-0.5)**2 + (y-0.4)**2 < 0.04:
        X3.append(x)
        Y3.append(y)


with open("states.csv", 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(X1)
    thewriter.writerow(Y1)
    thewriter.writerow(X2)
    thewriter.writerow(Y2)
    thewriter.writerow(X3)
    thewriter.writerow(Y3)

fig = plt.figure()

plt.scatter(X1,Y1, c="RED")
plt.scatter(X2,Y2, c= "GREEN")
plt.scatter(X3,Y3, c= "BLUE")
plt.legend(("Area1", "Area2", "Area3"))
plt.title("States in different Geographical Locations with different active radius")
plt.savefig("State.png")

