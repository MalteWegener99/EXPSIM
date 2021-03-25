import itertools
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

def derivatives_20_Cn():
    filt = (V == 20) & (bt<8) & (Ct > 0.02)
    print("V=20")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr),Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    print("Cn_CT:",a.coef_[3])
    return a

def derivatives_40_Cn():
    filt = (V == 40)
    print("V=40")
    print("Calculating yaw stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr),Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cn"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cn"])[filt]))
    print("Cn_beta:",a.coef_[1])
    print("Cn_alpha:",a.coef_[0])
    print("Cn_dr:",a.coef_[2])
    print("Cn_CT:",a.coef_[3])
    return a

def derivatives_20_Cp():
    filt = (V == 20) & (bt<8) & (Ct > 0.02)
    print("V=20")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr),Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    # print("Cp_CT:",a.coef_[3])
    return a

def derivatives_40_Cp():
    filt = (V == 40)
    print("V=40")
    print("Calculating Roll stability derivatives from",sum(filt), "Datapoints")
    indep = np.array([np.radians(al),np.radians(bt),np.radians(dr),Ct])
    a = lr.LinearRegression(fit_intercept=True)
    a.fit((indep.T)[filt,:], (data["Cp"])[filt])
    print("Score of fit:",a.score((indep.T)[filt,:], (data["Cp"])[filt]))
    print("Cp_beta:",a.coef_[1])
    print("Cp_alpha:",a.coef_[0])
    print("Cp_dr:",a.coef_[2])
    # print("Cp_CT:",a.coef_[3])
    return a

def show_nonlinearity_tobeta():
    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (al == 2)
    filta5 = (al == 5)

    #Show for Cn
    plt.clf()
    plt.scatter(bt[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\alpha=5$",facecolors='none')

    plt.scatter(bt[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\alpha=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\beta$")
    plt.ylabel("$C_N$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCNbeta")

    plt.clf()
    plt.scatter(bt[filt20&filta2],data["Cp"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt20&filta5],data["Cp"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\alpha=5$",facecolors='none')

    plt.scatter(bt[filt40&filta2],data["Cp"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\alpha=2$",facecolors='none')
    plt.scatter(bt[filt40&filta5],data["Cp"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\alpha=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\beta$")
    plt.ylabel("$C_P$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCpbeta")

def show_nonlinearity_toCt():
    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (bt == 2)
    filta5 = (bt == 5)

    #Show for Cn
    plt.clf()
    plt.scatter(Ct[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\beta=2$",facecolors='none')
    plt.scatter(Ct[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\beta=5$",facecolors='none')

    plt.scatter(Ct[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\beta=2$",facecolors='none')
    plt.scatter(Ct[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel("$C_T$")
    plt.ylabel("$C_N$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCNCt")

    plt.clf()
    plt.scatter(Ct[filt20&filta2],data["Cp"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\beta=2$",facecolors='none')
    plt.scatter(Ct[filt20&filta5],data["Cp"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\beta=5$",facecolors='none')

    plt.scatter(Ct[filt40&filta2],data["Cp"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\beta=2$",facecolors='none')
    plt.scatter(Ct[filt40&filta5],data["Cp"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel("$C_T$")
    plt.ylabel("$C_P$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCpCt")

def show_nonlinearity_toal():
    filt20 = (V == 20)
    filt40 = (V == 40)
    filta2 = (bt == 2) & (Ct > 0.02)
    filta5 = (bt == 5) & (Ct > 0.02)

    #Show for Cn
    plt.clf()
    plt.scatter(al[filt20&filta2],data["Cn"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\beta=2$",facecolors='none')
    plt.scatter(al[filt20&filta5],data["Cn"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\beta=5$",facecolors='none')

    plt.scatter(al[filt40&filta2],data["Cn"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\beta=2$",facecolors='none')
    plt.scatter(al[filt40&filta5],data["Cn"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\alpha$")
    plt.ylabel("$C_N$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCNal")

    plt.clf()
    plt.scatter(al[filt20&filta2],data["Cp"][filt20&filta2],marker="o",edgecolors="k",label=r"V=20, $\beta=2$",facecolors='none')
    plt.scatter(al[filt20&filta5],data["Cp"][filt20&filta5],marker="s",edgecolors="k",label=r"V=20, $\beta=5$",facecolors='none')

    plt.scatter(al[filt40&filta2],data["Cp"][filt40&filta2],marker="v",edgecolors="gray",label=r"V=40, $\beta=2$",facecolors='none')
    plt.scatter(al[filt40&filta5],data["Cp"][filt40&filta5],marker="^",edgecolors="gray",label=r"V=40, $\beta=5$",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\alpha$")
    plt.ylabel("$C_P$")
    plt.tight_layout()
    plt.savefig("Images/nonlinCpal")

def show_CT_J():
    plt.clf()
    filt20 = (V == 20)
    filt40 = (V == 40)
    plt.clf()
    plt.scatter(J[filt20],Ct[filt20],marker="o",edgecolors="k",label=r"V=20",facecolors='none')
    plt.scatter(J[filt40],Ct[filt40],marker="o",edgecolors="gray",label=r"V=400",facecolors='none')
    plt.legend()
    plt.grid()
    plt.xlabel("$J$")
    plt.ylabel("$C_T$")
    plt.tight_layout()
    plt.savefig("Images/Ctj")

def plot_fit_Cn():
    alpha = [2,5]
    drs = [0,5,10]
    betas = np.linspace(0,10)
    for a, d in itertools.product(alpha,drs):
        pass

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
show_nonlinearity_toCt()
show_nonlinearity_toal()
show_CT_J()

make_tables(Cn2,Cn4)
make_tables(Cp2,Cp4)


exit()
filt1 = (V == 40) &  (J == 1.7)
plt.scatter(bt[filt1],(data["Cn"])[filt1],c=dr[filt1],label="40",marker="v")
filt2 = (V == 20) & (J == 1.7)
plt.scatter(bt[filt2],(data["Cn"])[filt2],c=dr[filt2],label="20",marker="x")
plt.legend()
plt.show()
