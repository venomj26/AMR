






























##

import h5py
import numpy as np
f=h5py.File('/Users/jha/Documents/Spring2021/jha_shadowproject/simSeries_1/simState.mat')
list_f=list(f.keys())
simstate = f['simState']  
print("simstate prints",simstate,list_f)
simstate=f.get('simState')
data=np.array('simState')
#simstate1=f.get('smiState/
#data1_simstate=

