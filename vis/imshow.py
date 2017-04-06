__author__ = 'joon'

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow as pim


def fpim(data, fig_no=1, alpha=1., cmap=None, clim=None):
    plt.figure(fig_no)
    if cmap:
        if clim:
            pim(data, cmap=cmap, clim=clim)
        else:
            pim(data, cmap=cmap)
    else:
        if clim:
            pim(data, clim=clim)
        else:
            pim(data)
    plt.pause(0.001)
    return


def vis_seg(im, seg, figno=18, alpha=.5, cmap='nipy_spectral', clim=(0, 30), both=True):
    if both:
        fig = plt.figure(figno)
        ax = fig.add_subplot(2, 1, 1)
        ax.imshow(seg, cmap=cmap, clim=clim)
        ax = fig.add_subplot(2, 1, 2)
        ax.imshow(im)
        ax.imshow(seg, alpha=alpha, cmap=cmap, clim=clim)
    else:
        plt.figure(figno)
        pim(im)
        pim(seg, alpha=alpha, cmap=cmap, clim=clim)

    plt.pause(.1)

    return
