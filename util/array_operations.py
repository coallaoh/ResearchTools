from pdb import set_trace as st
import numpy as np

def unique_rows(aaa):
    aaa = np.ascontiguousarray(aaa)
    unique_aaa = np.unique( aaa.view( [('', aaa.dtype)] * aaa.shape[1] ) )
    return unique_aaa.view(aaa.dtype).reshape(( unique_aaa.shape[0], aaa.shape[1] ))


