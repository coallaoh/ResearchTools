import numpy as np


def is_quadratic(num):
    return np.sqrt(float(num)).is_integer()


def matrix_argmax(mat):
    return np.unravel_index(mat.argmax(), mat.shape)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def inv_sigmoid(x, envelop=np.Inf):
    assert (envelop > 0)
    return np.maximum(np.minimum(np.log(x / (1 - x)), envelop), -envelop)


def linear_transform_01(A):
    max_A = np.max(A).astype(np.float)
    min_A = np.min(A).astype(np.float)
    return (A - min_A) / (max_A - min(A))


def Jsoftmax(w, t=1.0, axis=0):
    w = np.array(w)  # n, c, h, w
    ndim = len(w.shape)
    w_sh = np.array(w.shape)
    w_sh[axis] = 1
    reshapedim = np.array([1] * ndim, dtype=np.int)
    reshapedim[axis] = w.shape[axis]

    w_max = np.amax(w, axis=axis, keepdims=True)
    w -= np.tile(w_max, reshapedim)  # to avoid numerical issues (exploding exp)

    e = np.exp(np.array(w) / t)
    Z = np.sum(e, axis=axis, keepdims=True)

    out = e / np.tile(Z, reshapedim)
    return out


def proj_lp(v, xi, p):
    if np.linalg.norm(v.reshape(-1), p) > xi:
        if p == np.inf:
            v_projected = np.sign(v) * np.minimum(np.abs(v), xi)
        elif p == 2:
            v_projected = v / np.linalg.norm(v.reshape(-1)) * xi
        else:
            raise
        return v_projected
    else:
        return v


def compute_percentiles(x, thres=0.25):
    x = np.array(x)
    p = np.sort(x.reshape(-1))
    N = float(x.size)
    low_n, upp_n = int(thres * N), int((1 - thres) * N)
    return p[low_n], p[upp_n]
