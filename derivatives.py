import numpy as np
import sklearn.linear_model as lr
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

#Load the fucktwat data
data = pd.read_csv("datapoints.csv")
V = np.array(data["V"])
dr = np.array(data["dr"],dtype=np.float64)
Ct = np.array(data["CT"])
J = np.array(data["J"])
al = np.array(data["a"])
bt = np.array(data["b"])

filt = (V == 20)
plt.scatter(J[filt],Ct[filt],marker="v")
filt = (V == 40)
plt.scatter(J[filt],Ct[filt],marker="x")
plt.show()

def derivatives_20_Cn():
    filt = (V == 20) & (bt<8)
    print("V=20")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([al,bt,dr,Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    print("Cn_CT:",a.coef_[3])

def derivatives_40_Cn():
    filt = (V == 40)
    print("V=40")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([al,bt,dr,Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    print("Cn_CT:",a.coef_[3])

def derivatives_20_Cp():
    filt = (V == 20) & (bt<8)
    print("V=20")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([al,bt,dr,Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    print("Cp_CT:",a.coef_[3])

def derivatives_40_Cp():
    filt = (V == 40)
    print("V=40")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([al,bt,dr,Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    print("Cp_CT:",a.coef_[3])

derivatives_20_Cn()
derivatives_40_Cn()
derivatives_20_Cp()
derivatives_40_Cp()
exit()
filt1 = (V == 40) &  (J == 1.7)
plt.scatter(bt[filt1],(data["Cn"])[filt1],c=dr[filt1],label="40",marker="v")
filt2 = (V == 20) & (J == 1.7)
plt.scatter(bt[filt2],(data["Cn"])[filt2],c=dr[filt2],label="20",marker="x")
plt.legend()
plt.show()
