import numpy as np


z = 1j


def dft(x):
    n = len(x)
    eps = np.cos(2 * np.pi / n) + np.sin(2 * np.pi / n) * z
    F = [[eps**(j*k) for k in range(n)] for j in range(n)]
    F = np.array(F)
    return F @ x


def idft(x):
    n = len(x)
    return np.conj(dft(np.conj(x)))/n


def fft(x):
    n = len(x)
    if n == 1:
        return np.array([x[0]])
    eps = np.cos(2 * np.pi / n) + np.sin(2 * np.pi / n) * z
    E = np.diag([eps**i for i in range(int(n/2))])
    p = np.array([i for i in range(n) if i % 2 == 0])
    p = np.concatenate([p,
            np.array([i for i in range(n) if i % 2 == 1])])
    P = np.zeros((n,n))
    for i in range(n):
        P[i][int(p[i])] = 1

    p = np.array([x[i] for i in range(n) if i % 2 == 0])
    p2 = np.array([x[i] for i in range(n) if i % 2 == 1])

    F = np.vstack([
        np.hstack([fft(p), E @ fft(p2)]),
        np.hstack([fft(p), -E @ fft(p2)])
    ])

    return F @ P


def ifft(x):
    n = len(x)
    return np.conj(fft(np.conj(x)) @ x)/n


x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
print(ifft(fft(x)))