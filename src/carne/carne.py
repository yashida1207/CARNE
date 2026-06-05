"""
    aaa

"""

import math
import numpy as np
import utils


##### Template class 

class MyClass:

    def __init__(self, value):
        self.value = value

    def do_something(self):
        return self.value * 2


#####

class wc: 
    
    def __init__(self, size, runyear, enu, dsnb_model): 

        self.size = size 
        nproton = size * 6.67e+31

        self.runyear = runyear
        runtime = runyear * 3.15576e+7  # yr --> sec 

        xsec = utils.load_ibd_xsec(enu_used=enu)   # cm^2
        flux = utils.load_dsnb_flux(finname=dsnb_model, enu_used=enu)  # cm^-2 s^-1 MeV^-1
        sigeff = utils.load_sigeff(finname="sig_eff_sk4_fv_2970day.dat", enu_used=enu)
        bkg = utils.load_bkg(finname="bkg_event_sk4_fv_2970day.dat", enu_used=enu) * 0.5  # 0.5 for 2 MeV binning in SK-IV (???) 





### below should probably be separated as functions because of potential change on a user side 

        d_enu = np.diff(enu)

        sig = nproton * runtime * xsec * flux * sigeff  # MeV^-1
        self.sig = sig 
        nsig = np.sum(sig[:-1] * d_enu)
        self.nsig = nsig 

        bkg = bkg * (volume/22.5) * (livetime/8.13)  # MeV^-1
        self.bkg = bkg
        nbkg = np.array([])
        for ibkg in bkg: 
            nbkg = np.append(nbkg, np.sum(ibkg[:-1] * d_enu))
        self.nbkg = nbkg  

        pdfsig = sig/np.sum(sig[:-1]); pdfsig[-1] = np.nan 
        self.pdfsig = pdfsig

        pdfbkg = np.array([]) 
        for ibkg in bkg:
            pdfbkg = np.append(pdfbkg, ibkg/np.sum(ibkg[:-1])); pdfbkg[-1] = np.nan 
        self.pdfbkg = pdfbkg





        self.register_evt("sig", sig)
        self.set_syst("sig", 0.2)
        self.register_evt("bkg", bkg)
        self.set_syst("bkg", 0.2)


    def create_pdf(self): 



    def register_evt(self): 
        
        # ... calculate nsig and nbkg from loaded data 
        # ... make PDFs from calculated/loaded sig and bkg distributions 

        self.nsig = nsig 
        self.nbkg = nbkg 


    def set_syst(self, ntype, syst): 
        
        if ntype == "sig": 
            self.nsig_syst = syst 
        elif ntype == "bkg": 
            self.nbkg_syst = syst 


    def create_toy(self, ntoy, mode): 
        
        return toy





def calc_likelihood(toy): 

    return loglikeli, teststat





