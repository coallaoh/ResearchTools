import numpy as np
from mask_box import bbox_area, mask2bbox


def compute_cc(mask, minarea=5 ** 2):
    mask_cc = []
    import skimage.morphology as skimorph

    labels = skimorph.label(mask, connectivity=2)
    for n in np.unique(labels):
        if n == 0: continue
        mask_indiv = labels == n
        if mask_indiv.sum() < minarea: continue
        if bbox_area(mask2bbox(mask_indiv)) == 0: print('        ...zero area!!'); continue
        mask_cc.append(mask_indiv)

    print('    Found %d connected components in mask' % (len(mask_cc)))

    return mask_cc
