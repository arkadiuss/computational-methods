import imageio
import numpy as np

im = imageio.imread('LENNA.JPG')

u, s, v = np.linalg.svd(im, full_matrices=False)
Ar = np.zeros((len(u), len(v)))
for i in range(50):
    Ar += s[i] * np.outer(u.T[i], v[i])

imageio.imwrite('picture_out.png', Ar)