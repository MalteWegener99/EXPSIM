import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.integrate import quad

HTdat  = pd.read_csv('naca64.dat', sep = '\s+', header = None)
HTdat  = HTdat.to_numpy()
HTdatx = HTdat[:,0]
HTdaty = HTdat[:,1]
c      = 0.149
elim   = np.where(HTdaty<0)[0][0]
HTdatx = HTdatx[0:elim-1]*c # non-dimensional, LE->TE
HTdaty = HTdaty[0:elim-1]*c # non-dimensional, LE->TE

fHTdat   = interp1d(HTdatx, HTdaty, kind='quadratic')
halfarea = quad(fHTdat, HTdatx[0], HTdatx[-1])[0]
fullarea = halfarea*2 

bHT = 0.576
VHT= bHT*fullarea