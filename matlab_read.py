#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 00:43:09 2021

@author: jha
"""

#%%
from fastkml import kml

with open('US41.kml') as myfile:
    doc=myfile.read()
k = kml.KML()
k.from_string(doc)

outerFeature = list(k.features())
innerFeature = list(outerFeature[0].features())

placemarks = list(innerFeature[0].features())

for p in placemarks:
    coords = p.coordinates #this does not work


#%%
    
#load from matlab
#%%
import pandas as pd
import h5py
import scipy.io

f = h5py.File('/Users/jha/Documents/Spring2021/jha_shadowproject/Simulation_INDOT_RoadShadow_US41_Loc_1/simState.mat',
              'r')

hmat=pd.HDFStore('/Users/jha/Documents/Spring2021/jha_shadowproject/Simulation_INDOT_RoadShadow_US41_Loc_1/simState.mat',
              'r')

#mat = scipy.io.loadmat("/Users/jha/Documents/Spring2021/jha_shadowproject/Simulation_INDOT_RoadShadow_US41_Loc_1/simState.mat")
#f.keys()
#data = f.get('data/subs')
#data = np.array(data)  # For converting to a NumPy array
#print(data)
    
    
#%%
#%%
import h5py
f=h5py.File('/Users/jha/Documents/Spring2021/jha_shadowproject/Simulation_INDOT_RoadShadow_US41_Loc_1/simState.mat')
list_f=list(f.keys())
simstate = f['simState']  
print("simstate prints",simstate)
w=pd.DataFrame()
w=simstate['gridEles']
w=f.get('gridEles')
print("w is :", w)
df=numpy.array(simstate)
n1 = f.get('simState')
print("ni is:", n1)
#f[simstate['gridEles'][0, 0]].value
    
#%%
    
    
    
    
#%%
    
import h5py
f=h5py.File('/Users/jha/Documents/Spring2021/jha_shadowproject/simSeries_1/simState.mat')
list_f=list(f.keys())
simstate = f['simState']  
print("simstate prints",simstate)
data=np.array(simstate)
#w=simstate['gridEles']
#w=f.get('gridEles')
#print("w is :", w)
#df=numpy.array(simstate)
n1 = f.get('simstate/sunsetDatetimes')
n1.items()
#print("ni is:", n1)
#f[simstate['gridEles'][0, 0]].value
    
#%%


#%%
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon




#%%


#%%
data=np.array(simstate)

simstate=f.get('simConfigs')

data=np.array(simstate)

simstate=f.get('simState/gridLatLonPts')

data=np.array(simstate)

data=np.array(simstate)




#%%