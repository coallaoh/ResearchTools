__author__ = 'joon'

import numpy as np
import thread

def apply_async_wrapper(func, *args):
    try:
        return func(*args)
    except Exception as e:
        return e


class Sum:
    def __init__(self, shape, type=np.int):
        self.value = np.zeros(shape, dtype=type)  # this is the initialization of the sum
        self.lock = thread.allocate_lock()
        self.count = 0

    def add(self, value):
        if type(value) == TypeError:
            raise Exception("Error occurred inside parallel loop")
        elif type(value) == IOError:
            raise Exception("Loading failed:" + value.filename)

        self.count += 1
        self.lock.acquire()  # lock so sum is correct if two processes return at same time
        self.value += value  # the actual summation
        self.lock.release()

