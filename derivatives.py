import numpy as np
import sklearn.linear_model as lr
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

data = pd.read_csv("datapoints.csv")
V = np.array(data["V"])
dr = np.array(data["dr"])
Ct = np.array(data["CT"])
al = np.array(data["a"])
bt = np.array(data["b"])
filt = (V == 20) & (bt<8)
print(sum(filt))
indep = np.array([al,bt,dr,Ct])
a = lr.LinearRegression(fit_intercept=True)
a.fit((indep.T)[filt,:], (data["Cn"])[filt])
print(a.score((indep.T)[filt,:], (data["Cn"])[filt]))
print(a.coef_)
# print("Cnbeta:", a.coef_[1])
# print("Cndr:", a.coef_[2])
# print("CnJ:", a.coef_[3])
# print("Cnalpha:", a.coef_[0])

filt1 = (V == 40) & (al==5)
plt.plot(bt[filt1],(data["Cn"])[filt1],"s",label="40")
filt2 = (filt) & (al==5)
plt.plot(bt[filt2],(data["Cn"])[filt2],"v",label="20")
plt.legend()
plt.show()
