import numpy as np
import matplotlib.pyplot as plt
import math

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
A = []
for s in np.arrange(0, 2*np.pi, 0.01):
    for t in np.arrange(0, np.pi, 0.01):
        A.append([math.cos(s)*math.sin(t), math.sin(s)*math.sin(t), math.cos(t)])

xdata = map(lambda x: x[0], A)
ydata = map(lambda x: x[1], A)
zdata = map(lambda x: x[2], A)
ax.scatter(xdata, ydata, zdata, c=zdata, cmap='Greens')
plt.show()