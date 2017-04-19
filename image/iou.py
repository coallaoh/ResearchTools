__author__ = 'joon'

import numpy as np


def compute_iou(a, b, ig=None, return_type='iou'):
    if ig is not None:
        loc = (1 - ig).astype(np.bool)
    else:
        loc = np.ones(a.shape, dtype=np.bool)
    anb = a & b
    aub = a | b
    if return_type == 'iou':
        return float(anb[loc].sum()) / aub[loc].sum()
    elif return_type == 'iol':
        return float(anb[loc].sum()) / a[loc].sum()
    elif return_type == 'ior':
        return float(anb[loc].sum()) / b[loc].sum()
    else:
        raise NotImplementedError


if __name__ == "__main__":
    iou = compute_iou(np.array([[1,0],[1,1]],dtype=np.bool),
                     np.array([[0,1],[1,1]],dtype=np.bool))
    print(iou)

