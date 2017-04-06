__author__ = 'joon'

import numpy as np


def bw_to_rgb(I):
    I_new = np.zeros((I.shape[0], I.shape[1], 3), dtype='uint8')
    I_new[:, :, 0] = I.copy()
    I_new[:, :, 1] = I.copy()
    I_new[:, :, 2] = I.copy()
    return I_new
