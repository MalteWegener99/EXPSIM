import itertools
import numpy as np
import sklearn.linear_model as lr
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 13})

#Load the fucktwat data
data = pd.read_csv("datapoints-unpowered.csv")
V = np.array(data["V"])
dr = -1*np.array(data["dr"],dtype=np.float64)
J = np.array(data["J"])
al = np.array(data["a"])
ac = np.array(data["ac"])
bt = np.array(data["b"])
bc = np.array(data["bc"])
data["Cn"] = -data["Cn"]


def derivatives_20_Cn():
    filt = (V == 20) & (bc<8)
    print("Re=$2.3\cdot10^5$")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr)])
    a = lr.LinearRegression(fit_intercept=False)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    return a

def derivatives_40_Cn():
    filt = (V == 40)
    print("Re=$4.6\cdot10^5$")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr)])
    a = lr.LinearRegression(fit_intercept=False)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    return a

def derivatives_20_Cp():
    filt = (V == 20) & (bc<8)
    print("Re=$2.3\cdot10^5$")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr)])
    a = lr.LinearRegression(fit_intercept=False)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    return a

def derivatives_40_Cp():
    filt = (V == 40)
    print("Re=$4.6\cdot10^5$")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr)])
    a = lr.LinearRegression(fit_intercept=False)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    return a

def show_nonlinearity_tobeta():
    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (ac == 2)
    filta5 = (ac == 5)

    #Show for Cn
    plt.clf()
    plt.scatter(bt[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=5$",facecolors='none')

    plt.scatter(bt[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\beta$")
    plt.ylabel("$C_N$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCNbeta-unp")

    plt.clf()
    plt.scatter(bt[filt20&filta2],data["Cp"][filt20&filta2],marker="o",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt20&filta5],data["Cp"][filt20&filta5],marker="s",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=5$",facecolors='none')

    plt.scatter(bt[filt40&filta2],data["Cp"][filt40&filta2],marker="v",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt40&filta5],data["Cp"][filt40&filta5],marker="^",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\beta$")
    plt.ylabel("$C_{L'}$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCpbeta-unp")

def show_nonlinearity_toal():
    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (bc == 2)
    filta5 = (bc == 5)

    #Show for Cn
    plt.clf()
    plt.scatter(al[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\beta=2$",facecolors='none')
    plt.scatter(al[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\beta=5$",facecolors='none')

    plt.scatter(al[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\beta=2$",facecolors='none')
    plt.scatter(al[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\alpha$")
    plt.ylabel("$C_N$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCNal-unp")

    plt.clf()
    plt.scatter(al[filt20&filta2],data["Cp"][filt20&filta2],marker="o",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\beta=2$",facecolors='none')
    plt.scatter(al[filt20&filta5],data["Cp"][filt20&filta5],marker="s",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\beta=5$",facecolors='none')

    plt.scatter(al[filt40&filta2],data["Cp"][filt40&filta2],marker="v",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\beta=2$",facecolors='none')
    plt.scatter(al[filt40&filta5],data["Cp"][filt40&filta5],marker="^",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\alpha$")
    plt.ylabel("$C_{L'}$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCpal-unp")

def plot_fit_Cn():
    alpha = [2,5]
    drs = [0,5,10]
    C = 0.15
    betas = np.linspace(0,10)
    plt.clf()
    for a, d in itertools.product(alpha,drs):
        aa = np.full_like(betas,np.radians(a))
        dd = np.full_like(betas,np.radians(a))
        cc = np.full_like(betas,C)
        m = np.array([aa,np.radians(betas),dd,cc])
        plt.plot(betas, Cn2.predict(m.T), "--k")
        plt.plot(betas, Cn4.predict(m.T), "--", c="gray")

    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (al == 2)
    filta5 = (al == 5)

    #Show for Cn
    plt.scatter(bt[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"Re=$2.3\cdot10^5$, $\alpha=5$",facecolors='none')

    plt.scatter(bt[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"Re=$4.6\cdot10^5$, $\alpha=5$",facecolors='none')

    plt.show()

def make_tables(C2, C4):
    de = [r"\alpha",r"\beta",r"\delta_r",r"C_T"]
    unit = ["[1/rad]","[1/rad]","[1/rad]","[-]"]
    for i in range(C2.coef_.shape[0]):
        print("$C_{{X_{{{}}}}}$ {} & {:.4f} & {:.4f} \\\\".format(de[i],unit[i],C2.coef_[i],C4.coef_[i]))

    print()
    print()
    print()


Cn2 = derivatives_20_Cn()
Cn4 = derivatives_40_Cn()
Cp2 = derivatives_20_Cp()
Cp4 = derivatives_40_Cp()
show_nonlinearity_tobeta()
show_nonlinearity_toal()

make_tables(Cn2,Cn4)
make_tables(Cp2,Cp4)

# plot_fit_Cn()


exit()
filt1 = (V == 40) &  (J == 1.7)
plt.scatter(bt[filt1],(data["Cn"])[filt1],c=dr[filt1],label="40",marker="v")
filt2 = (V == 20) & (J == 1.7)
plt.scatter(bt[filt2],(data["Cn"])[filt2],c=dr[filt2],label="20",marker="x")
plt.legend()
plt.show()
