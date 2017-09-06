from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np


def visualise_mat(M, fignum=1):
    plt.matshow(M, fignum=fignum, cmap=plt.cm.gray)
    plt.show()


def print_mat(M):
    sh = np.shape(M)
    for ind_x in range(sh[0]):
        for ind_y in range(sh[1]):
            print('%2.2f  ' % (M[ind_x, ind_y]), end="")
        print("\n", end="")


def visualise_time_series(V, fignum=1, title='plot', xlabel='x', ylabel='y'):
    plt.plot(V)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def histogram_array(V, n_bins=10, x_label='variable'):
    n, bins, patches = plt.hist(V, n_bins, normed=1, facecolor='blue', alpha=0.75)
    plt.xlabel(x_label)
    plt.ylabel('frequency')
    plt.grid(True)
    plt.show()
