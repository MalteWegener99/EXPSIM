import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from K1calc import K1
from HTvol import VHT
from scipy.io import savemat

'''General parameters'''
B    = 1.800 # WT breadth
H    = 1.250 # WT height
lf   = 0.3 # corner fillet length
C    = B*H - 2*lf*lf # WT cross-sectional area
BH   = B/H # windtunnel B-H ratio
S    =  0.2172 # wing area


'''Functions'''
K3dat = pd.read_csv('K3.csv', header=None)
K3dat = K3dat.to_numpy()
K3datx = K3dat[:,0]
K3daty = K3dat[:,1]
fK3 = interp1d(K3datx, K3daty, fill_value='extrapolate')

tau1dat = pd.read_csv('tau1.csv', header=None)
tau1dat = tau1dat.to_numpy()
tau1datx = tau1dat[:,0]
tau1daty = tau1dat[:,1]
ftau1 = interp1d(tau1datx, tau1daty, kind='quadratic',fill_value='extrapolate')

def functau1(bbB):
    return float(ftau1(bbB))

def epssb(Kone, tauone, vol):
    return Kone*tauone*vol/(C**(3/2))


"""SOLID BLOCKAGE"""
'''Wing'''
VW  = 0.0030229 # volume of wing  
tc  = 0.1582 # airfoil thickness ratio
bW  = 1.297 # span of wing - tip to tip
K1W = K1 # wing K1

bbBW  = 2*bW/B
tau1W = functau1(bbBW)

eps_sb_W = epssb(K1W,tau1W,VW)

'''Horizontal tailplane'''
bHT  = 0.576 # span horz tailplane
tcHT = 0.15 # t/c horz tailplane
# VHT is imported at the start of program

K1HTdat  = pd.read_csv('K1HT.csv', header=None) # NACA 64 series
K1HTdat  = K1HTdat.to_numpy()
K1HTdatx = K1HTdat[:,0]
K1HTdaty = K1HTdat[:,1]
fK1HT    = interp1d(K1HTdatx, K1HTdaty)
K1HT     = float(fK1HT(tcHT))

bbBHT  = 2*bHT/B
tau1HT = functau1(bbBHT)

eps_sb_HT = epssb(K1HT,tau1HT,VHT)

'''Vertical tailplane '''
bVT  = 0.258*2 # span vert tailplane - take into account mirrored span (so twice the height)
tcVT = 0.15 # t/c vert tailplane
VVT = 0.0003546

K1VTdat  = pd.read_csv('K1VT.csv', header=None) # NACA 4 digit
K1VTdat  = K1VTdat.to_numpy()
K1VTdatx = K1VTdat[:,0]
K1VTdaty = K1VTdat[:,1]
fK1VT    = interp1d(K1VTdatx, K1VTdaty, kind='quadratic')
K1VT     = float(fK1VT(tcVT))

crVT = 0.0642
ctVT = 0.0438
tr = crVT*tcVT
tt = ctVT*tcVT
tVT = (tr+tt)/2 
bbBVT  = 2*tVT/B # 2H is the breadth for mirrored windtunnel calculation
tau1VT = functau1(bbBVT)

eps_sb_VT = epssb(K1VT,tau1VT,VVT)

'''Fuselage'''
Vfuse   = 0.0160632
dfuse   = 0.14 # diameter of fuselage
bbBfuse = 2*dfuse/B
lenfuse =  0.96*bW # length of fuselage
dlfuse  = dfuse/lenfuse # diameter of fuselage

K3fuse   = float(fK3(dlfuse))
tau1fuse = functau1(bbBfuse)

eps_sb_fuse = epssb(K3fuse,tau1fuse,Vfuse)

'''Nacelle'''
Vnac   = (0.0024485 - VHT)/2 # ONE NACELLE
RnRp   = 0.28 # Rn/Rp
Rp     = 0.2031/2
Rnac   = Rp*RnRp
dnac   = 2*Rnac # diameter of nacelle
bbBnac = 2*dnac/B
lennac = 0.345 # length of nacelle
dlnac  = dnac/lennac  

K3nac   = float(fK3(dlnac))
tau1nac  = functau1(bbBnac)

eps_sb_nac = epssb(K3nac,tau1nac,Vnac)

'''Struts'''
# BHvert = 2*H/B # inverted fraction for vertical components - about the same as initial BH = 1.4
lenstrut  = 0.46*bW # Assume all struts have the same length
dlenstrut = 2*lenstrut # double the lenght for mirrored image
bbBstrut  = 2*dlenstrut/(2*H)
tau1strut = functau1(bbBstrut) 

""" WAKE BLOCKAGE """
ARW  = 8.98 # wing aspect ratio
e    = 1/(1.05+0.007*np.pi*ARW) # oswald eff factor

CD0_2  = 0.05535578
CD0_5  = 0.0660773
CD0_8  = 0.08187667
CD0_f  = interp1d([2,5,8],[CD0_2,CD0_5,CD0_8],'quadratic',fill_value='extrapolate')
CD0_10 = float(CD0_f(10))
CD0_0  = float(CD0_f(0))

# eps_wb_0_2  = S/4/C*CD0_2
# eps_wb_0_5  = S/4/C*CD0_5
# eps_wb_0_8  = S/4/C*CD0_8
# eps_wb_0_10 = S/4/C*CD0_10

CD0 = np.array([CD0_0, CD0_2, CD0_5, CD0_8, CD0_10])
eps_wb_0 = S/4/C*CD0

CDi = 0.032767



""" LIFT INTERFERENCE """

# constants
HB   = H/B # lambda
TRW  = 0.4 # wing taper ratio
qc   = 0.25*bW/ARW # 0.25c

# Import tail-off data
CLWdat   = pd.read_csv('TailOffData0.csv', header=0)
CLWdat   = CLWdat.to_numpy()
CLW_aoa  = CLWdat[:,0]
CLW_aos  = CLWdat[:,1]
CLW_Vinf = CLWdat[:,2]
CLW_CL   = CLWdat[:,3]
CLW_CD   = CLWdat[:,4]

# gather relevant data points corresponding to Vinf and AoA
Vinf = 20
aoa  = -3
aoa_ = []
CL_  = []
CD_  = []
for i in np.arange(len(CLW_aoa)):
    # if np.abs(aoa - CLW_aoa[i]) < 0.1 and np.abs(Vinf - CLW_Vinf[i]) < 0.1 and len(aoa_) < 20:
    if np.abs(Vinf - CLW_Vinf[i]) < 0.1 and len(aoa_) < 20:
    # if np.abs(aoa - CLW_aoa[i]) < 0.1 and np.abs(Vinf - CLW_Vinf[i]) < 0.1 and CLW_aos[i] >=2 and CLW_aos[i] <= 8:
        aoa_.append(CLW_aoa[i])
        CL_.append(CLW_CL[i])
        CD_.append(CLW_CD[i])
CL_ = np.array(CL_)
CL2_ = CL_*CL_
slope = (CD_[12] - CD_[5]) / (CL2_[12] - CL2_[5])
# plt.figure()        
# plt.plot(CL_*CL_, CD_)

CLWavg = np.mean(CL_)
    
# gathered values for C_L_W
CLW_m3 = np.mean([0.029, 0.01025]) # 0.029 for V=20
CLW_m1 = 0.2065
CLW_2  = 0.483725
CLW_5  = 0.7455
CLW_7  = np.mean([0.8935, 0.9081])
# array in order of increasing AoA
CLW = np.array([CLW_m3, CLW_m1, CLW_2, CLW_5, CLW_7])

'''Functions'''
bv5dat  = pd.read_csv('bv-5.csv', header=None)
bv5dat  = bv5dat.to_numpy()
bv5datx = bv5dat[:,0]
bv5daty = bv5dat[:,1]
bv5func = interp1d(bv5datx, bv5daty, 'quadratic')

bv25dat  = pd.read_csv('bv-25.csv', header=None)
bv25dat  = bv25dat.to_numpy()
bv25datx = bv25dat[:,0]
bv25daty = bv25dat[:,1]
bv25func = interp1d(bv25datx, bv25daty, 'quadratic')

bvW = (bv5func(ARW) + bv25func(ARW))/2 
be  = (bW + bvW)/2
k   = be/B
    
deltadat  = pd.read_csv('delta.csv', header=None)
deltadat  = deltadat.to_numpy()
deltadatx = deltadat[:,0]
deltadaty = deltadat[:,1]
deltafunc = interp1d(deltadatx, deltadaty, 'quadratic')
delta     = float(deltafunc(k))

delta_alfa_uw = delta*S/C*CLW
delta_CDW     = delta_alfa_uw*CLW

tau2dat  = pd.read_csv('tau2.csv', header=None)
tau2dat  = tau2dat.to_numpy()
tau2datx = tau2dat[:,0]
tau2daty = tau2dat[:,1]
tau2func = interp1d(tau2datx, tau2daty, 'quadratic', fill_value='extrapolate')
tau205c  = float(tau2func(qc))

delta_alfa_sc = tau205c*delta*S/C*CLW
delta_alfa = delta_alfa_uw + delta_alfa_sc

aoa_1 = []
CL_1  = []
for i in np.arange(len(CLW_aoa)):
    if np.abs(20 - CLW_Vinf[i]) < 0.1 and len(aoa_1) < 12:
        aoa_1.append(CLW_aoa[i])
        CL_1.append(CLW_CL[i])
CL_1  = np.array(CL_1)
aoa_1 = np.array(aoa_1)
CLalfa = np.mean((CL_1[1:] - CL_1[:-1])/1)

delta_CM_qc   = 1/8*delta_alfa_sc*CLalfa

"""DOWNWASH AT TAILPLANE"""
lt   = 0.535 # tail arm - assume cg = wing mac location 
ltB  = lt/B
ARt = 3.87

tau2lt         = float(tau2func(ltB))
dCLdalfat      = 0.1*ARW/(ARt+2)*0.8 # ASSUME qt/q = 1
dCMqcdalfat    = dCLdalfat * lt
delta_alfa_sct = delta*S/C*tau2lt
delta_alfa_t   = delta_alfa_uw + delta_alfa_sct

delta_CMqct    = dCMqcdalfat * delta_alfa_t 


"""SLIPSTREAM BLOCKAGE"""
# To be executed in matlab directly


"""Save as mat file"""
# matdict = {'eps_sb_fuse': eps_sb_fuse, 
#            'eps_sb_HT': eps_sb_HT,
#            'eps_sb_nac': eps_sb_nac,
#            'eps_sb_VT': eps_sb_VT,
#            'eps_sb_W': eps_sb_W,
#            'eps_wb_0': eps_wb_0,
#            'C': C,
#            'CD0': CD0,
#            'CDi': CDi,
#            'delta_CDW': delta_CDW,
#            'delta_CM_qc': delta_CM_qc,
#            'delta_CMqct': delta_CMqct}

eps_sb = eps_sb_fuse + eps_sb_HT + eps_sb_nac + eps_sb_VT + eps_sb_W
matdict = {'eps_sb': eps_sb,
           'eps_wb_0': eps_wb_0,
            'C': C,
            'S': S,
            'CD0': CD0,
            'CDi': CDi,
            'delta_alfa':delta_alfa,
            'delta_CDW': delta_CDW,
            'delta_CM_qc': delta_CM_qc,
            'delta_CMqct': delta_CMqct}
savemat("BCpara.mat", matdict)