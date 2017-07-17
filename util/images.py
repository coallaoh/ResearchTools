from PIL import Image
import numpy as np
import time


def load_image_PIL(imname):
    for iii in range(10):
        try:
            im = np.asarray(Image.open(
                imname
            ))
            return im
        except IOError:
            print ('failed to load image %s: attempt %d / 10' % (imname, iii + 1))
            time.sleep(10)

    raise IOError
