import os
from pdb import set_trace as st

try:
    import cPickle as pickle
except ImportError:
    import pickle

# https://github.com/ShaoqingRen/faster_rcnn/blob/master/utils/mkdir_if_missing.m

def mkdir_if_missing(dirname):
    if os.path.isdir(dirname):
        return
    else:
        try:
            os.mkdir(dirname)
        except OSError:
            split_dirname = dirname.split('/')
            subdirectory = ''
            start = True
            for name in split_dirname[:-1]:
                if start:
                    subdirectory = name
                    start = False
                else:
                    subdirectory = subdirectory + '/' + name
            mkdir_if_missing(subdirectory)
            os.mkdir(dirname)
            return


def save_to_cache(variable, cachename):
    mkdir_if_missing(os.path.split(cachename)[0])
    fp = open(cachename, 'wb')
    pickle.dump(variable, fp)


def load_from_cache(cachename):
    fp = open(cachename, 'rb')
    return pickle.load(fp)
