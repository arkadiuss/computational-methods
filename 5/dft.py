import numpy as np


def dft(x):
    n = len(x)
    z = 1j
    eps = np.cos(2*np.pi/n) + np.sin(2*np.pi/n)*z
    F = [[eps**(j*k) for k in range(n)] for j in range(n)]
    F = np.array(F)
    return F @ x


def idft(x):
    n = len(x)
    return np.conj(dft(np.conj(x)))/n


x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
print(dft(x))
print(idft(dft(x)))