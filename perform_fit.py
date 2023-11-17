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


def calc_llh(e_data, pdf):
    llh = 0.

    for e in e_data: 
        llh += np.log()  

    llh = -llh 
    return llh 




def add_smear_syst(): 


def add_shift_syst(): 



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--fittype", dest="fittype", type=str, 
                        default="asimov", help="fitting type --Asimov or another data")
    args = parser.parse_args()
    
    print("start unbinned maximum likelihood fitting...")

    
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





