"""
    aaa

"""

import numpy as np 

datadir = ../../data

# will consider enu_max and enu_min...



#####

def resample_data_linear(x_new, x_old, y_old):  
    """
        x, y sampling should be linear. 
        x is often neutrino energy. 
    """

    y_new = []

    for x in x_new:
        if x < np.min(x_old):
            y_tmp = y_old[0]
        elif x > np.max(x_old):
            y_tmp = y_old[-1]
        else:
            j = 0
            for i in range(len(x_old)-1):
                if x >= x_old[i] and x < x_old[i+1]:
                    j = i
                    break
            y_tmp = y_old[j] + (y_old[j+1] - y_old[j]) / (x_old[j+1] - x_old[j]) * (x - x_old[j])

        y_new.append(y_tmp)

    y_new = np.array(y_new, dtype=float)
    return y_new


#####

def load_ibd_xsec(finname=f"{datadir}/ibd_strumia2003.dat", enu_used):

    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    xsec = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0]))
        xsec = np.append(xsec, float(idata[1]))

    xsec *= 1.0e-41  # cm^2
    xsec = resample_data_linear(enu_used, enu, xsec)
    return xsec


#####

def load_dsnb_flux(finname=f"{datadir}/dsnb_ashida2023.dat", enu_used):

    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    flux = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0]))
        flux = np.append(flx, float(idata[1]))

    flux = resample_data_linear(enu_used, enu, flux)
    return flux


#####

def load_sig_eff(finname, enu_used): 
    """
        prompt energy is common in both SK and JUNO files?? 
    """

    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    eff = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0])+0.789)  # prompt energy --> neutrino energy in IBD 
        eff = np.append(eff, float(idata[1]))

    eff = resample_data_linear(enu_used, enu, eff)
    return eff


#####

def load_bkg(finname, enu_used): 
    """
        prompt energy is common in both SK and JUNO files?? 
    """

    fin = open(finname, "r")
    data = fin.readlines()
    bkg_type_num = len(data[0].split()) - 1  # first column for energy 

    enu = np.array([])
    bkg = [[] for i in range(bkg_type_num)]

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0])+0.789)  # prompt energy --> neutrino energy in IBD 
        
        for j in range(bkg_type_num): 
            bkg[j].append(float(idata[j+1]))

    bkg = np.array(bkg, dtype=float)
    for i in range(bkg_type_num): 
        bkg[i] = resample_data_linear(enu_used, enu, bkg[i])

    return bkg 











