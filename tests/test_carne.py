import math 
import numpy as np 

from carne import carne
from carne import utils


enu = np.linspace(50, 0, 50)  # MeV 

xsec = utils.load_ibd_xsec(enu)  # cm^2
flux = utils.load_dsnb_flux(enu)  # cm^-2 s^-1 MeV^-1




