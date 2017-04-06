import numpy as np


def mask2bbox(mask):
    x0 = np.where(mask)[0].min()
    x1 = np.where(mask)[0].max()
    y0 = np.where(mask)[1].min()
    y1 = np.where(mask)[1].max()

    return np.array([x0, x1, y0, y1])


def bbox_ratio(bbox, ratio=1.):
    x0, x1, y0, y1 = bbox.tolist()
    h = x1 - x0
    w = y1 - y0
    cx = float(x0 + x1) / 2
    cy = float(y0 + y1) / 2

    h_new = h * float(ratio)
    w_new = w * float(ratio)

    x0_new = np.round(cx - h_new / 2)
    x1_new = np.round(cx + h_new / 2)
    y0_new = np.round(cy - w_new / 2)
    y1_new = np.round(cy + w_new / 2)

    return np.array([x0_new, x1_new, y0_new, y1_new])


def carve_bbox_to_im(bbox, imshape):
    H, W = imshape

    x0, x1, y0, y1 = bbox.tolist()

    x0_new = max(x0, 0)
    x1_new = min(x1, H)
    y0_new = max(y0, 0)
    y1_new = min(y1, W)

    return np.array([x0_new, x1_new, y0_new, y1_new])


def bbox_area(bbox):
    return (bbox[1] - bbox[0]) * (bbox[3] - bbox[2])
