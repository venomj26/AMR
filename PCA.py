#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:31:09 2019

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

#%%

import numpy as np  
import matplotlib.pyplot as plt
import pandas as pd
file_name = '/Users/jha/Documents/Fall2019/iris.data'
df = pd.read_csv(file_name, sep=',',header=None)
df.head(n=10)

numrows= cursor.execute("SELECT * FROM salfinal ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print("I am doing the thing")
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))


df_amr = pd.DataFrame(rows)
print("I am still doing this thing")
#%%

#%%
class_label = pd.DataFrame(df_amr.iloc[:,-1])
class_label.columns = ['label']
df_amr = df_amr.iloc[:, :-1]
df_amr.head(n=10)
#%%


#%%
df_amr = df_amr.sub(df_amr.mean(axis=0), axis=1)
df_amr_mat = np.asmatrix(df_amr)
sigma = np.cov(df_amr_mat.T)


eigVals, eigVec = np.linalg.eig(sigma)


sorted_index = eigVals.argsort()[::-1] 
eigVals = eigVals[sorted_index]
eigVec = eigVec[:,sorted_index]


eigVec = eigVec[:,:2]
transformed = df_amr_mat.dot(eigVec)


#horizontally stack transformed data set with class label.
final_df = np.hstack((transformed, class_label))
#convert the numpy array to data frame
final_df = pd.DataFrame(final_df)
#define the column names
final_df.columns = ['x','y','label']

#%%






#%%

groups = final_df.groupby('label')
figure, axes = plt.subplots()
axes.margins(0.05)
for name, group in groups:
    axes.plot(group.x, group.y, marker='o', linestyle='', ms=6, label=name)
    axes.set_title("PCA on pca_a.txt")
axes.legend()
plt.xlabel("principal component 1")
plt.ylabel("principal component 2")
plt.show()











#%%