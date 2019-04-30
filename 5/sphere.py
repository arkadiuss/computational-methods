from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_zlabel('z')
ax.set_xlabel('x')
ax.set_ylabel('y')


def show(A):
    xdata = list(map(lambda x: x[0], A))
    ydata = list(map(lambda x: x[1], A))
    zdata = list(map(lambda x: x[2], A))
    ax.scatter(xdata, ydata, zdata)
    plt.show()


def create_eclipse():
    B = []
    for s in np.arange(0, 2*np.pi, 0.05):
        for t in np.arange(0, np.pi, 0.05):
            B.append([math.cos(s)*math.sin(t), math.sin(s)*math.sin(t), math.cos(t)])
    return np.array(B)


def transform(B):
    A = np.random.random((3, 3))
    u, s, v = np.linalg.svd(A)
    print(s)
    return u, s, v


def show_sv(v, B):
    show(B @ np.transpose(v))


def show_ssv(s, v, B):
    print(B @ (s @ np.transpose(v)))


def show_susv(u, s, v, B):
    print(B @ (u @ s @ v))


B = create_eclipse()
u, s, v = transform(B)
show_sv(v, B)
show_ssv(s, v, B)
show_susv(u, s, v, B)
