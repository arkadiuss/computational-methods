import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt

MAX_ITERS = 1000
EPS = 1e-6


def normalize(A):
    return A/np.linalg.norm(A)


def power_method(A):
    v = normalize(np.random.random(A.shape[0]))
    l = 3
    pl = -1
    i = 0
    while abs(l - pl) > EPS:
        pl = l
        w = A@v
        v = normalize(w)
        l = np.transpose(v)@A@v
        i = i + 1

    #print(l, v, np.linalg.eig(A))
    return i


def rev_method(A):
    v = normalize(np.random.random(A.shape[0]))
    mi = 3
    lu, piv = linalg.lu_factor(A - mi*np.identity(A.shape[0]))
    l = 3
    pl = -1
    i = 0
    while abs(l - pl) > EPS:
        pl = l
        w = linalg.lu_solve((lu, piv), v)
        v = normalize(w)
        l = np.transpose(v)@A@v
        i = i + 1

    #print(l, v, np.linalg.eig(A))
    return i


def ray(A):
    v = normalize(np.random.random(A.shape[0]))
    pl = -1
    l = 3
    i = 0
    while abs(l - pl) > EPS:
        pl = l
        w = np.linalg.solve(A - l*np.identity(A.shape[0]), v)
        v = normalize(w)
        l = np.transpose(v)@A@v
        i = i + 1

    #print(l, v, np.linalg.eig(A))
    return i

iters = []
ip = []
irp = []
iray = []

for i in range(5, 1000):
    if i%100 == 0:
        print(i)
    A = np.random.random((i, i))
    A = A@np.transpose(A)
    iters.append(i)
    ip.append(power_method(A))
    irp.append(rev_method(A))
    iray.append(ray(A))


plt.plot(iters, ip, iters, irp, iters, iray)
plt.show()