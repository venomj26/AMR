#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:55:47 2019

@author: jha
"""

import glob 
#import pandas as pd
path = r'/Users/jha/Documents/Salmonella'
#df = pd.concat([pd.read_csv(f, encoding='latin1') for f in glob.glob('data*.csv'), ignore_index=True])
file_name = glob.glob(path +"/*")
for name in file_name:
    file1= glob.glob(name + "/*.csv")
    #print("file is",file1)
    for f in file1: 
        if "amr" in f.lower():
            print ("file_name",f)