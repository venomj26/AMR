#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 17:55:38 2020

@author: jha

"""

#%%
import csv
import mysql.connector as mariadb
from tabulate import tabulate
import pandas as pd

amrdb= mariadb.connect(
        host="localhost",
        user="root",
        passwd="Sukhoi@90",
        database ="myamr"
        )
cursor = amrdb.cursor(buffered=True) # else it fetches one row for everytime it is executed 
print("We are at line 31 we have connection, lets begin")

#%%


#get the data from the ast table to make the dataframe 
#%%
import pandas as pd
numrows= cursor.execute("SELECT `Lat/Lon` FROM EcoliIBisodatlocmerge group by `Lat/Lon` limit 10")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
df = pd.DataFrame(rows)
df.columns=["LL"]
#%%


#%%

from geopy.geocoders import Nominatim 
geolocator = Nominatim(user_agent="geoapiExercises") 
def city_state_country(coord): 
    location = geolocator.reverse(coord, exactly_one=True) 
    address = location.raw['address']
    state = address.get('state', '') 
    return  state 
list_ll=df["LL"].to_list()
list_l = ['0' if x is None else x for x in list_ll]
for i in list_l: 
    try:
        l=city_state_country(i)
        print(l,i)
        
        
    except:
        print("missing values")
        continue



#%%