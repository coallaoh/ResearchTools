import numpy as np


def random_crop(im, ratio=.1, return_coords=False):
    H = float(im.shape[0])
    W = float(im.shape[1])
    dH = H * ratio
    dW = W * ratio

    x0 = int(np.random.uniform(low=0, high=dH))
    x1 = int(np.random.uniform(low=H - dH, high=H))
    y0 = int(np.random.uniform(low=0, high=dW))
    y1 = int(np.random.uniform(low=W - dW, high=W))

    if return_coords:
        return im[x0:x1, y0:y1], dict(x0=x0, x1=x1, y0=y0, y1=y1)
    else:
        return im[x0:x1, y0:y1]


def random_translation(im, ratio=.1, return_coords=False):
    H = float(im.shape[0])
    W = float(im.shape[1])
    dH = H * ratio / 2
    dW = W * ratio / 2

    h = int(np.random.uniform(low=-dH, high=dH))
    w = int(np.random.uniform(low=-dW, high=dW))

    new_im = np.zeros_like(im)
    if h > 0:
        if w > 0:
            new_im[h:, w:] = im[:-h, :-w]
        elif w < 0:
            new_im[h:, :w] = im[:-h, -w:]
        else:
            new_im[h:, :] = im[:-h, :]
    elif h < 0:
        if w > 0:
            new_im[:h, w:] = im[-h:, :-w]
        elif w < 0:
            new_im[:h, :w] = im[-h:, -w:]
        else:
            new_im[:h, :] = im[-h:, :]
    else:
        if w > 0:
            new_im[:, w:] = im[:, :-w]
        elif w < 0:
            new_im[:, :w] = im[:, -w:]
        else:
            new_im[:, :] = im[:, :]

    if return_coords:
        return new_im, dict(h=h, w=w)
    else:
        return new_im
