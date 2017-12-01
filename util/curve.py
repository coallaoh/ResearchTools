__author__ = "joon"

from util.ios import save_to_cache, load_from_cache


class TrainCurve(object):
    def __init__(self, *args):
        self.curves = dict(zip(args, [[] for _ in range(len(args))]))

    def save(self, loc):
        save_to_cache(self.curves, loc)

    def load(self, loc):
        self.curves = load_from_cache(loc)
