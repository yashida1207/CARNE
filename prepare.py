""" 
    prepare.py 

        1. 
        2. 
        3. 
""" 

import os 
import sys 
import argparse

import numpy as np 




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--fittype", dest="fittype", type=str, 
                        default="asimov", help="fitting type --Asimov or another data")
    args = parser.parse_args()
    
    print("start unbinned maximum likelihood fitting...")


# 1. get nominal numbers of signal and backgrounds based on detector & livetime settings 
# 2. create signal and background PDFs  
# 3. prepare systematics list  

