import numpy as np


def debug_show_time_elapsed(times):
    for i, t in enumerate(times[:-1]):
        print("Block %d took %1.5f sec" % (i, times[i + 1] - t))
