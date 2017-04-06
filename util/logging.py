import time
import os
from ios import save_to_cache


def log_experiments(control, locdir):
    timetoken = time.strftime('%Y%m%d%H%M%S')
    logdata = dict(
        timetoken=timetoken,
        control=control,
    )

    loc = os.path.join(locdir, timetoken)
    print('saving control log to....... %s' % loc)

    save_to_cache(logdata, loc)
    return


def leave_timestamp(dirname, control):
    timetoken = time.strftime('%Y%m%d%H%M%S')
    save_to_cache(control, os.path.join(dirname, timetoken + '.pkl'))

    return
