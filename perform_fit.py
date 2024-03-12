""" 
    perform_fit.py 

        1. 
        2. 
        3. 
""" 

import os 
import sys 
import argparse
import json 
import numpy as np 

"""
def load_pdf(detec_type="LS"): 
    if detec_type == "WC": 

    elif detec_type == "LS": 
    
    return 




def calc_llh(e_data, pdf):
    llh = 0.

    for e in e_data: 
        llh += np.log()  

    llh = -llh 
    return llh 




def add_smear_syst(pdf): 

    return pdf, -llh 



def add_shift_syst(pdf): 
"""



if __name__ == "__main__":
    print("start an extended unbinned maximum likelihood fitting...")

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", type=str, 
                        default="config.json", help="config file")
    parser.add_argument("-t", "--fittype", dest="fittype", type=str, 
                        default="asimov", help="fitting type (Asimov or another data)")
    args = parser.parse_args()
    

    ## load experimental settings 
    config_file = open(args.config, "r")
    configs = json.load(config_file)

    use_wc = configs["use_wc"]
    if use_wc: 
        wc_volume = configs["WC"]["volume"]
        wc_livetime = configs["WC"]["livetime"]
        wc_atmo_nu_cc_syst = np.array([configs["WC"]["atmo_nu_cc"]["scale_syst"],
                                       configs["WC"]["atmo_nu_cc"]["shift_syst"],
                                       configs["WC"]["atmo_nu_cc"]["smear_syst"]]) 
        wc_atmo_nu_nc_syst = np.array([configs["WC"]["atmo_nu_nc"]["scale_syst"],
                                       configs["WC"]["atmo_nu_nc"]["shift_syst"],
                                       configs["WC"]["atmo_nu_nc"]["smear_syst"]]) 
        wc_spall_syst = np.array([configs["WC"]["spall"]["scale_syst"],
                                  configs["WC"]["spall"]["shift_syst"],
                                  configs["WC"]["spall"]["smear_syst"]]) 

    use_ls = configs["use_ls"]
    if use_ls: 
        ls_volume = configs["LS"]["volume"]
        ls_livetime = configs["LS"]["livetime"]
        ls_atmo_nu_cc_syst = np.array([configs["LS"]["atmo_nu_cc"]["scale_syst"],
                                       configs["LS"]["atmo_nu_cc"]["shift_syst"],
                                       configs["LS"]["atmo_nu_cc"]["smear_syst"]]) 
        ls_atmo_nu_nc_syst = np.array([configs["LS"]["atmo_nu_nc"]["scale_syst"],
                                       configs["LS"]["atmo_nu_nc"]["shift_syst"],
                                       configs["LS"]["atmo_nu_nc"]["smear_syst"]]) 
        ls_spall_syst = np.array([configs["LS"]["spall"]["scale_syst"],
                                  configs["LS"]["spall"]["shift_syst"],
                                  configs["LS"]["spall"]["smear_syst"]]) 
        ls_fastn_syst = np.array([configs["LS"]["fastn"]["scale_syst"],
                                  configs["LS"]["fastn"]["shift_syst"],
                                  configs["LS"]["fastn"]["smear_syst"]]) 




    # 1.1) get nominal signal based on input DSNB flux, IBD xsec, and signal efficiency: N_j for sig 
    # 1.2) get nominal backgrounds with scaling based on configs (volume, livetime): N_j for bkg 
    # 2.1) normalize signal distribution to get PDF: PDF_j for sig 
    # 2.2) normalize each background distribution to get PDFs: PDF_j for bkg 
    # 3. 



    ## load PDFs 
    if use_ls: 






"""
    
    ## load dataset 
    e_data = np.array([12.3, 24.8, 8.6])


    ## load nominal predictions 
    n_sig = 
    n_spall = 
    n_mupi = 
    n_nc = 
    n_decaye = 
    n_nuecc = 


    ## load signal and background PDFs
    pdf_spall = np.array() 
    pdf_mupi = np.array() 
    pdf_nc = np.array() 
    pdf_decaye = np.array() 
    pdf_nuecc = np.array() 


    ## load systematic uncertainties 
    scale 
    smear 
    shift 
    syst_sets = scale * smear * shit 


    ## perform llh calculation 
    n_sig = [] 
    llh = [] 

    for syst_sets:  # scale of sig/bkg, pdf syst 
        f_sig = 1.1 
        n_spall = 
        n_mupi = 
        n_nc = 
        n_decaye = 
        n_nuecc = 

        add_smear_syst(pdf)

        add_shift_syst(pdf)

        llh_tmp = calc_llh(e_data, pdf)
        llh.append(llh)
        nsig.append() 

    n_sig = np.array(n_sig, dtype=float)
    llh = np.array(llh, dtype=float)


    ## save results 


"""



