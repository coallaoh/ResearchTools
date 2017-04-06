from pdb import set_trace as st
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow, show
from skimage.morphology import square, dilation, erosion
import time
import scipy
import cv2

np.random.seed(1574)


def dilate_polygon(poly, rate):
    if isinstance(poly, list):
        poly_np = np.array(poly).reshape((-1, 2))
    else:
        poly_np = poly.reshape((-1, 2))
    X = poly_np[:, 0]
    Y = poly_np[:, 1]
    C_X = np.mean(X)
    C_Y = np.mean(Y)

    X_new = (X - C_X) * rate + C_X
    Y_new = (Y - C_Y) * rate + C_Y

    poly_new = np.hstack((X_new.reshape((-1, 1)), Y_new.reshape((-1, 1))))
    return poly_new.reshape(-1).tolist()


def polygon_mask_on_image(img_obj, mask_poly, cat=None, where='FG', dilate_rate=1, all_instances=False):
    if not mask_poly:
        return img_obj
    # img = Image.new('L', (width, height), 0)
    img_pil = Image.fromarray(img_obj, mode=None)

    # print ('WARNING: Only picking first class in the annotation for masking')
    if cat is None:
        n_obj = len(mask_poly)
        success = False
        while not success:
            choice = np.random.choice(range(n_obj), size=1, replace=False)[0]
            try:
                seg = mask_poly[choice]['segmentation'][0]  # pick the first instance
                success = True
            except:
                awefjliajgaa = 1 + 1
    else:
        seg = []
        for idx in range(len(mask_poly)):
            if mask_poly[idx]['category_id'] == cat['id']:
                if all_instances:
                    try:
                        seg.append(mask_poly[idx]['segmentation'][0])
                    except:
                        awefjliajgaa = 1 + 1
                else:
                    seg = mask_poly[idx]['segmentation'][0]  # pick only the first instance of the given category
                    break

    if dilate_rate != 1:
        if all_instances:
            seg = [dilate_polygon(sg, dilate_rate) for sg in seg]
        else:
            seg = dilate_polygon(seg, dilate_rate)
    # poly = np.array(seg)  # .reshape((2,-1))

    d = ImageDraw.Draw(img_pil)

    if all_instances:
        for sg in seg:
            d.polygon(sg, outline=0, fill=0)
    else:
        d.polygon(seg, outline=0, fill=0)

    mask = np.array(img_pil)

    if where == 'FG':
        return mask
    elif where == 'BG':
        return img_obj - mask
    else:
        raise Exception('choose either FG or BG mask')


def skimage_opencv_dilation(white_pixels, dilation_rate=1., USE_RESIZE_TRICK=False, opencv=False):
    area = new_area = white_pixels.sum().astype(np.float)
    new_white_pixels = white_pixels
    target_area = target_area_ = (dilation_rate ** 2) * area
    C = 1
    TOL = 1
    ITER = 0
    start_time = time.time()

    x1 = 1
    x2 = 1 + int(np.sqrt(area) * np.abs(dilation_rate - 1) * C)
    width = np.floor(float(x1 + x2) / 2).astype(np.int)

    if dilation_rate > 1:
        resize_trick = target_area > 5000 and USE_RESIZE_TRICK
        resize_factor = np.sqrt(5000 / target_area)
    else:
        resize_trick = (area - target_area) > 1000 and USE_RESIZE_TRICK
        resize_factor = np.sqrt(1000 / area)

    if resize_trick:
        im_size = white_pixels.shape
        white_pixels = scipy.misc.imresize(white_pixels, resize_factor, interp='bilinear')
        target_area *= resize_factor ** 2
        x2 = 1 + int(np.sqrt(white_pixels.sum().astype(np.float)) * np.abs(dilation_rate - 1) * C)
        width = np.floor(float(x1 + x2) / 2).astype(np.int)

    if dilation_rate > 1:
        while (x2 - x1 > TOL):
            ITER += 1
            if opencv:
                new_white_pixels = cv2.dilate(white_pixels, square(width), iterations=1)
            else:
                new_white_pixels = dilation(white_pixels, square(width))
            new_area = new_white_pixels.sum().astype(np.float)
            if new_area > target_area:
                x2 = width
            else:
                x1 = width
            width = np.floor(float(x1 + x2) / 2).astype(np.int)

    else:
        while (x2 - x1 > TOL):
            ITER += 1
            if opencv:
                new_white_pixels = cv2.erode(white_pixels, square(width), iterations=1)
            else:
                new_white_pixels = erosion(white_pixels, square(width))
            new_area = new_white_pixels.sum().astype(np.float)
            if new_area > target_area:
                x1 = width
            else:
                x2 = width
            width = np.floor(float(x1 + x2) / 2).astype(np.int)

    if resize_trick:
        new_white_pixels = scipy.misc.imresize(new_white_pixels, im_size, interp='bilinear')
        new_area = new_white_pixels.sum().astype(np.float)
        target_area = target_area_

    end_time = time.time()
    if False:
        print ('        =======================')
        print ('        Iterations:    %d' % ITER)
        print ('        Resize trick?  %d' % resize_trick)
        print ('        Time taken:    %2.1f' % (end_time - start_time))
        print ('        Original area: %3.1f' % area)
        print ('        New area:      %3.1f' % new_area)
        print ('        Ratio:         %1.2f' % (float(new_area) / area))
        print ('        Target ratio:  %1.2f' % (dilation_rate ** 2))
        print (' ')
        print ('        Init:          %d, %d' % (1, 1 + int(np.sqrt(area) * np.abs(dilation_rate - 1) * C)))
        print ('        Final:         %d' % (width))
    return new_white_pixels


def skimage_opencv_dilation_incremental(white_pixels, dilation_rate=1., USE_RESIZE_TRICK=False, opencv=False):
    area = new_area = previous_area = white_pixels.sum().astype(np.float)
    new_white_pixels = previous_white_pixels = white_pixels
    target_area = (dilation_rate ** 2) * area
    ITER = 0
    # if target_area-area>50000:
    #     width = 100
    # elif target_area-area>10000:
    #     width = 20
    # else:
    width = 3

    start_time = time.time()

    if dilation_rate > 1:
        while (new_area < target_area and ITER < 1000):
            previous_area = new_area
            previous_white_pixels = new_white_pixels
            ITER += 1
            if opencv:
                new_white_pixels = cv2.dilate(new_white_pixels, square(width), iterations=1)
            else:
                new_white_pixels = dilation(new_white_pixels, square(width))
            new_area = new_white_pixels.sum().astype(np.float)

    else:
        while (new_area > target_area and ITER < 1000):
            previous_area = new_area
            previous_white_pixels = new_white_pixels
            ITER += 1
            if opencv:
                new_white_pixels = cv2.erode(new_white_pixels, square(width), iterations=1)
            else:
                new_white_pixels = erosion(new_white_pixels, square(width))
            new_area = new_white_pixels.sum().astype(np.float)

    if np.abs(target_area - previous_area) < np.abs(target_area - new_area):
        new_white_pixels = previous_white_pixels
        new_area = previous_area

    end_time = time.time()
    if False:
        print ('        =======================')
        print ('        Iterations:    %d' % ITER)
        print ('        Time taken:    %2.1f' % (end_time - start_time))
        print ('        Original area: %3.1f' % area)
        print ('        New area:      %3.1f' % new_area)
        print ('        Ratio:         %1.2f' % (float(new_area) / area))
        print ('        Target ratio:  %1.2f' % (dilation_rate ** 2))
        print (' ')
    return new_white_pixels


def polygon_mask_on_image_skimage(im, mask_poly, cat=None, where='FG', dilate_rate=1, all_instances=False):
    if not mask_poly:
        return im

    # print ('WARNING: Only picking first class in the annotation for masking')
    if cat is None:
        n_obj = len(mask_poly)
        success = False
        while not success:
            choice = np.random.choice(range(n_obj), size=1, replace=False)[0]
            try:
                seg = mask_poly[choice]['segmentation'][0]  # pick the first instance
                success = True
            except:
                awefjliajgaa = 1 + 1
    else:
        seg = []
        for idx in range(len(mask_poly)):
            if mask_poly[idx]['category_id'] == cat['id']:
                if all_instances:
                    try:
                        seg.append(mask_poly[idx]['segmentation'][0])
                    except:
                        awefjliajgaa = 1 + 1
                else:
                    seg = mask_poly[idx]['segmentation'][0]  # pick only the first instance of the given category
                    break

    if all_instances:
        dilated_mask = np.zeros(im.shape[:2], dtype=np.uint8)
        for sg in seg:
            shadow = np.ones(im.shape[:2], dtype=np.uint8)
            shadow_pil = Image.fromarray(shadow, mode=None)
            d = ImageDraw.Draw(shadow_pil)
            d.polygon(sg, outline=0, fill=0)
            shadow_mask = np.array(shadow_pil)
            dilated_mask_ = skimage_opencv_dilation(1 - shadow_mask, dilate_rate)
            dilated_mask = dilated_mask + dilated_mask_
        dilated_mask = np.minimum(dilated_mask, 1)

    else:
        shadow = np.ones(im.shape[:2], dtype=np.uint8)
        shadow_pil = Image.fromarray(shadow, mode=None)
        d = ImageDraw.Draw(shadow_pil)
        d.polygon(seg, outline=0, fill=0)
        seg = dilate_polygon(seg, dilate_rate)
        shadow_mask = np.array(shadow_pil)
        dilated_mask = skimage_opencv_dilation(1 - shadow_mask, dilate_rate)

    if where == 'FG':
        return np.multiply(np.dstack([1 - dilated_mask] * 3), im)

    elif where == 'BG':
        return np.multiply(np.dstack([dilated_mask] * 3), im)
    else:
        raise Exception('choose either FG or BG mask')


def polygon_mask_on_image_opencv(im, mask_poly, cat=None, where='FG', dilate_rate=1, all_instances=False,
                                 incremental=False):
    if not mask_poly:
        return im

    # print ('WARNING: Only picking first class in the annotation for masking')
    if cat is None:
        n_obj = len(mask_poly)
        success = False
        while not success:
            choice = np.random.choice(range(n_obj), size=1, replace=False)[0]
            try:
                seg = mask_poly[choice]['segmentation'][0]  # pick the first instance
                success = True
            except:
                awefjliajgaa = 1 + 1
    else:
        seg = []
        for idx in range(len(mask_poly)):
            if mask_poly[idx]['category_id'] == cat['id']:
                if all_instances:
                    try:
                        seg.append(mask_poly[idx]['segmentation'][0])
                    except:
                        awefjliajgaa = 1 + 1
                else:
                    seg = mask_poly[idx]['segmentation'][0]  # pick only the first instance of the given category
                    break

    if all_instances:
        dilated_mask = np.zeros(im.shape[:2], dtype=np.uint8)
        for sg in seg:
            shadow = np.ones(im.shape[:2], dtype=np.uint8)
            shadow_pil = Image.fromarray(shadow, mode=None)
            d = ImageDraw.Draw(shadow_pil)
            d.polygon(sg, outline=0, fill=0)
            shadow_mask = np.array(shadow_pil)
            if incremental:
                dilated_mask_ = skimage_opencv_dilation_incremental(1 - shadow_mask, dilate_rate, opencv=True)
            else:
                dilated_mask_ = skimage_opencv_dilation(1 - shadow_mask, dilate_rate, opencv=True)
            dilated_mask = dilated_mask + dilated_mask_
        dilated_mask = np.minimum(dilated_mask, 1)

    else:
        shadow = np.ones(im.shape[:2], dtype=np.uint8)
        shadow_pil = Image.fromarray(shadow, mode=None)
        d = ImageDraw.Draw(shadow_pil)
        d.polygon(seg, outline=0, fill=0)
        seg = dilate_polygon(seg, dilate_rate)
        shadow_mask = np.array(shadow_pil)
        if incremental:
            dilated_mask = skimage_opencv_dilation_incremental(1 - shadow_mask, dilate_rate, opencv=True)
        else:
            dilated_mask = skimage_opencv_dilation(1 - shadow_mask, dilate_rate, opencv=True)

    if where == 'FG':
        return np.multiply(np.dstack([1 - dilated_mask] * 3), im)

    elif where == 'BG':
        return np.multiply(np.dstack([dilated_mask] * 3), im)
    else:
        raise Exception('choose either FG or BG mask')
