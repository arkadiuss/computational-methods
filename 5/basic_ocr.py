import imageio
import numpy as np
from numpy.fft import fft2, ifft2


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


im = rgb2gray(imageio.imread('galia.jpg'))

wz = rgb2gray(imageio.imread('galie_e.png'))


#im = 255 - im
#wz = 255 - wz

wz_g = np.zeros(im.shape)
wz_g[:wz.shape[1], :wz.shape[0]] = np.rot90(wz)
res = np.real(ifft2(fft2(im) * fft2(wz_g)))
maxi = np.amax(res)
mini = np.amin(res)
res = res/(maxi-mini)
for i in range(len(res)):
    for j in range(len(res[i])):
        res[i][j] = 1 if res[i][j] > 0.95 else 0
imageio.imwrite('picture_out.png', res)
#print(im, wz)