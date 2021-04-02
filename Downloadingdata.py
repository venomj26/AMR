#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:16:49 2019

@author: jha
"""

# coding: utf-8

#%%


import ftplib
import os
from ftplib import error_perm
ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
ftp.login()
ftp.cwd("/pathogen/Results/Candida_auris")
# list files with ftplib
file_list = ftp.nlst()

#print(file_list)
for f in file_list: 
    #print (f)
    try:
             
        if 'pdg000000067' in f.lower() :
            print(f)
            try :
                storetodir='/Users/jha/Documents/Summer2019/Candida_auris/'+f
                print(storetodir)
                os.mkdir(storetodir)
                os.chdir(storetodir)
            except :
                print('Failed. Invalid directory?')
                
            ftp.cwd("/pathogen/Results/Candida_auris/" +f+"/Metadata")
            file_list = ftp.nlst()
            print(file_list)
            for f1 in file_list:
                if "pdg000000067" in f1.lower() and any(f1.endswith(ext) for ext in ['tsv']):
                    # download file sending "RETR <name of file>" command
                    # open(f, "w").write is executed after RETR suceeds and returns file binary data
                    ftp.retrbinary("RETR {}".format(f1), open(f1, "wb").write)
                    print("downloaded {}".format('f1'))
        else :
            print("exit")

        if 'pdg000000067' in f.lower():
            ftp.cwd("/pathogen/Results/Candida_auris/" +f+"/AMR")
            file_list = ftp.nlst()
            print(file_list)
            for f1 in file_list:
                if "pdg000000067" in f1.lower() and any(f1.endswith(ext) for ext in ['tsv']):
                    # download file sending "RETR <name of file>" command
                    # open(f, "w").write is executed after RETR suceeds and returns file binary data
                    ftp.retrbinary("RETR {}".format(f1), open(f1, "wb").write)
                    print("downloaded {}".format('f1'))
    except ftplib.error_perm as e:
        print("AMR does not exist")
        
              
        
ftp.quit()
    
#%%
