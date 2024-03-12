""" 
    prepare.py 

        1. Get nominal signal (N_sig) based on input DSNB flux, IBD xsec, and signal efficiency, 
           and normalize signal distribution to get signal PDF (P_sig). 

        2. Get nominal backgrounds (N_bkg) with weighting based on detector size and livetime, 
           and normalize each background distribution to get background PDF (P_bkg).

        3. Prepare Asimov dataset based on nominal background distributions. 

        4. Save all above in numpy files. 


      written by Dr. Yosuke Ashida (University of Utah) 
""" 

import os 
import sys 
import argparse
import json 
import numpy as np 



def load_ibd_xsec(finname="./data/ibd_strumia2003.dat"): 
    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    xsec = np.array([])
    epos = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0]))
        xsec = np.append(xsec, float(idata[1]))
        epos = np.append(epos, float(idata[2]))

    xsec *= 1.0e-41  # cm^2

    return enu, xsec



def resample_quantity(enu_aft, enu_bfr, quan_bfr):
    quan = []

    for enu in enu_aft:
        if enu < np.min(enu_bfr):
            quan_tmp = quan_bfr[0]
        elif enu > np.max(enu_bfr):
            quan_tmp = quan_bfr[-1]
        else:
            j = 0
            for i in range(len(enu_bfr)-1):
                if enu >= enu_bfr[i] and enu < enu_bfr[i+1]:
                    j = i
                    break

            quan_tmp = quan_bfr[j] + (quan_bfr[j+1]-quan_bfr[j])/(enu_bfr[j+1]-enu_bfr[j]) * (enu-enu_bfr[j])

        quan.append(quan_tmp)

    quan = np.array(quan, dtype=float)

    return quan



def load_dsnb_flux(finname="./data/dsnb_horiuchi2009.dat"): 
    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    flx = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0]))
        flx = np.append(flx, float(idata[1]))

    return enu, flx



def load_sig_eff(finname="./data/sigeff_juno_fv1.dat"): 
    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    eff = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0])+0.789)  # prompt energy --> neutrino energy in IBD 
        eff = np.append(eff, float(idata[1]))

    return enu, eff



def load_bkg_ls(volume, livetime, finname="./data/bkg_juno_fv1.dat"): 
    fin = open(finname, "r")
    data = fin.readlines()

    enu = np.array([])
    fastn = np.array([])
    atmo_nu_cc = np.array([])
    atmo_nu_nc_11C = np.array([])
    atmo_nu_nc_others = np.array([])

    for i, idata in enumerate(data):
        idata = idata.split()
        enu = np.append(enu, float(idata[0])+0.789)  # prompt energy --> neutrino energy in IBD 
        fastn = np.append(fastn, float(idata[1]))
        atmo_nu_cc = np.append(atmo_nu_cc, float(idata[2]))
        atmo_nu_nc_11C = np.append(atmo_nu_nc_11C, float(idata[3]))
        atmo_nu_nc_others = np.append(atmo_nu_nc_others, float(idata[4]))

    wgt = (volume/14.7) * (livetime/10.0)
    fastn *= wgt 
    atmo_nu_cc *= wgt 
    atmo_nu_nc_11C *= wgt 
    atmo_nu_nc_others *= wgt

    return enu, fastn, atmo_nu_cc, atmo_nu_nc_11C, atmo_nu_nc_others



def create_asimov_dataset(enu, cum, n_evt): 
    data_uniform = np.random.uniform(low=0.0, high=1.0, size=n_evt)
    data_asimov = [] 

    index = 0 
    for data in data_uniform: 
        for i in range(len(cum[:-1])): 
            if data >= cum[i] and data < cum[i+1]: 
                index = i 
                break 

        data_asimov.append(np.random.uniform(low=enu[index], high=enu[index+1], size=1))
    
    data_asimov = np.array(data_asimov, dtype=float)

    return data_asimov



if __name__ == "__main__":
    print("start an extended unbinned maximum likelihood fitting...")

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", type=str, 
                        default="config.json", help="config file")
    parser.add_argument("-t", "--fittype", dest="fittype", type=str, 
                        default="asimov", help="fitting type (Asimov or another data)")
    args = parser.parse_args()
    

    ## load DSNB flux & IBD cross section 
    enu_dsnb, flx_dsnb = load_dsnb_flux()  # MeV, MeV^{-1}s^{-1}cm^{-2}
    enu_tmp, xsec_tmp = load_ibd_xsec()  # MeV, cm^2 
    xsec_ibd = resample_quantity(enu_dsnb, enu_tmp, xsec_tmp)


    ## load experimental settings 
    config_file = open(args.config, "r")
    configs = json.load(config_file)


    ## WC 
    use_wc = configs["use_wc"]
    if use_wc: 
        wc_volume = configs["WC"]["volume"]
        wc_livetime = configs["WC"]["livetime"]


    ## LS 
    use_ls = configs["use_ls"]
    if use_ls: 
        enu_min_ls = 11.789; enu_max_ls = 30.789

        ls_volume = configs["LS"]["volume"]  # kton 
        ls_np = ls_volume * 7.15e+31 
        ls_livetime = configs["LS"]["livetime"]  # yr 

        # signal 
        enu_tmp, sigeff_tmp = load_sig_eff()
        sigeff_ls = resample_quantity(enu_dsnb, enu_tmp, sigeff_tmp)
        
        sig_ls = ls_np * (ls_livetime*3.15576e+7) * xsec_ibd[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))] \
                                                  * flx_dsnb[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))] \
                                                  * sigeff_ls[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))]  # MeV^{-1}

        d_enu_dsnb = np.diff(enu_dsnb[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))])
        n_sig_ls = np.sum(sig_ls[:-1] * d_enu_dsnb)
        pdf_sig_ls = sig_ls/np.sum(sig_ls[:-1])  # normalize
        pdf_sig_ls[-1] = -1

        # background 
        enu_tmp, fastn_tmp, atmo_nu_cc_tmp, atmo_nu_nc_11C_tmp, atmo_nu_nc_others_tmp = load_bkg_ls(ls_volume, ls_livetime) 
        
        fastn_ls = resample_quantity(enu_dsnb, enu_tmp, fastn_tmp)
        fastn_ls = fastn_ls[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))]  # MeV^{-1}
        n_fastn_ls = np.sum(fastn_ls[:-1])
        pdf_fastn_ls = fastn_ls/n_fastn_ls  # normalize
        pdf_fastn_ls[-1] = -1
        
        atmo_nu_cc_ls = resample_quantity(enu_dsnb, enu_tmp, atmo_nu_cc_tmp)
        atmo_nu_cc_ls = atmo_nu_cc_ls[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))]  # MeV^{-1}
        n_atmo_nu_cc_ls = np.sum(atmo_nu_cc_ls[:-1])
        pdf_atmo_nu_cc_ls = atmo_nu_cc_ls/n_atmo_nu_cc_ls  # normalize
        pdf_atmo_nu_cc_ls[-1] = -1
        
        atmo_nu_nc_11C_ls = resample_quantity(enu_dsnb, enu_tmp, atmo_nu_nc_11C_tmp)
        atmo_nu_nc_11C_ls = atmo_nu_nc_11C_ls[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))]  # MeV^{-1}
        n_atmo_nu_nc_11C_ls = np.sum(atmo_nu_nc_11C_ls[:-1])
        pdf_atmo_nu_nc_11C_ls = atmo_nu_nc_11C_ls/n_atmo_nu_nc_11C_ls  # normalize
        pdf_atmo_nu_nc_11C_ls[-1] = -1
        
        atmo_nu_nc_others_ls = resample_quantity(enu_dsnb, enu_tmp, atmo_nu_nc_others_tmp)
        atmo_nu_nc_others_ls = atmo_nu_nc_others_ls[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))]  # MeV^{-1}
        n_atmo_nu_nc_others_ls = np.sum(atmo_nu_nc_others_ls[:-1])
        pdf_atmo_nu_nc_others_ls = atmo_nu_nc_others_ls/n_atmo_nu_nc_others_ls  # normalize
        pdf_atmo_nu_nc_others_ls[-1] = -1

        # Asimov 
        bkg_tot_ls = fastn_ls + atmo_nu_cc_ls + atmo_nu_nc_11C_ls + atmo_nu_nc_others_ls  # MeV^{-1} 
        n_bkg_tot_ls = np.sum(bkg_tot_ls[:-1])
        pdf_bkg_tot_ls = bkg_tot_ls/n_bkg_tot_ls
        pdf_bkg_tot_ls[-1] = -1
        cum_bkg_tot_ls = np.cumsum(pdf_bkg_tot_ls) 

        #asimov_set_ls = create_asimov_dataset(enu_dsnb[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))], cum_bkg_tot_ls, int(n_bkg_tot_ls)*100)
        asimov_set_ls = create_asimov_dataset(enu_dsnb[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))], cum_bkg_tot_ls, int(n_bkg_tot_ls))


    ## save into numpy files 
    np.savez("./data/arr_enu", enu=enu_dsnb[np.where((enu_dsnb>=enu_min_ls) & (enu_dsnb<enu_max_ls))])

    n_arr_ls = np.array([n_sig_ls, n_fastn_ls, n_atmo_nu_cc_ls, n_atmo_nu_nc_11C_ls, n_atmo_nu_nc_others_ls])
    np.savez("./data/arr_n_ls", n_arr_ls=n_arr_ls)
    np.savez("./data/arr_pdf_ls", pdf_sig_ls=pdf_sig_ls, 
                                  pdf_fastn_ls=pdf_fastn_ls, 
                                  pdf_atmo_nu_cc_ls=pdf_atmo_nu_cc_ls, 
                                  pdf_atmo_nu_nc_11C_ls=pdf_atmo_nu_nc_11C_ls, 
                                  pdf_atmo_nu_nc_others_ls=pdf_atmo_nu_nc_others_ls)
    np.savez("./data/arr_asimov_ls", asimov_set_ls=asimov_set_ls)








    




