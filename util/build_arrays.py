from pdb import set_trace as st
import numpy as np
import scipy.sparse as sp

def build_diag_matrix( diag, offdiag, N ):

    AAA = diag * np.eye( N ) + offdiag * ( np.ones( (N,N) ) - np.eye( N ) )
    
    return AAA

def build_diag_constraints( N ):
    
    # diag elements
    row_diag = []
    for i in range(N):
        row_ = np.zeros( (N,N) )
        row_[i,i] = 1
        if i==N-1:
            row_[0,0] = -1
        else:
            row_[i+1,i+1] = -1
            
        row_diag.append( np.ravel( row_ ) )
        
    diag_constraints = np.vstack( row_diag )
    
    # upper triangular elements
    row_upp = []
    for i in range(N-1):
        for j in range(i+1,N):
            row_ = np.zeros( (N,N) )
            row_[i,j] = 1
            
            if i==N-2:
                row_[1,0] = -1
            else:
                if j==N-1: #upon reaching the end of row
                    row_[i+1,i+2] = -1
                else:
                    row_[i,j+1] = -1
                    
            row_upp.append( np.ravel( row_ ) )
    
    upp_constraints = np.vstack( row_upp )
    
    
    # lower triangular elements
    row_low = []
    for i in range(1,N):
        for j in range(i):
            row_ = np.zeros( (N,N) )
            row_[i,j] = 1
            
            if i==N-1:
                if j==N-2:
                    row_[0,1] = -1
                else:
                    row_[i,j+1] = -1
            else:
                if j==i-1: #upon reaching the end of row
                    row_[i+1,0] = -1
                else:
                    row_[i,j+1] = -1
                
            row_low.append( np.ravel( row_ ) )
    
    low_constraints = np.vstack( row_low )
    
    
    return np.vstack( (row_diag, row_upp, row_low) ).astype(np.float)
    
    
    
    
    
    
    
    
    
