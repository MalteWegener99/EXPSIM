import numpy as np
import pandas as pd
from scipy.integrate import simps

# Constants
V = 0.0030229 # Volume
s = 1.397/2 # half span
c = 0.165 # MAC
t = 0.1582*c # thickness = 15.82% of chord

# import Cp data
df = pd.read_csv('CP.dat', sep='\s+', header=3)
_array = df.to_numpy()
x  = _array[:,0]
y  = _array[:,1]
Cp = _array[:,2]

# Eliminate bottom profile
elim = np.where(y<0)[0][0]
x  = x[0:elim][::-1]*c # non-dimensional, LE->TE
y  = y[0:elim][::-1]*c # non-dimensional, LE->TE
Cp = Cp[0:elim][::-1] # LE->TE

'''Calculations'''
kap1 = V/(2*s*c*t) 

dx   = np.diff(x)
dy   = np.diff(y)
dydx = dy/dx

Cp_cen = (Cp[1:] + Cp[0:-1])/2 # central value of Cp
x_cen  = (x[1:] + x[0:-1])/2 # central value of x
xc_cen = x_cen/c # central value of x/c
y_cen  =  (y[1:] + y[0:-1])/2 # central value of y
_int = y_cen/c*np.sqrt(1-Cp_cen)*np.sqrt(1+dydx*dydx)
Lam  = 16/np.pi*simps(_int,xc_cen) 

K1 = np.sqrt(np.pi**3)/16*Lam/t*c/kap1