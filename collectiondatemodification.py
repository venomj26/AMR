#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:29:53 2020

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
numrows= cursor.execute("SELECT collection_date FROM EscherichiaMergedUS")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%


#splitting the collection_date column values into separate columns to get a separate column for date 
#%%
df = pd.DataFrame(rows)
#print ("the pandas dataframe ",df
#df=df.reset_index()      
df.columns=["collection_date"]
df.head()
df['collectiondate']=df['collection_date']
df=df.set_index('collectiondate')
split_df= df['collection_date'].str.split('-', expand= True)

split_df.head()
#split_dfT=split_df.T
#split_df = split_df.drop(split_df.columns[[23]], axis=1) 

#%%

#%%


split_df.columns=['Collection_year','a','b']
split_df= split_df.drop(['a','b'], axis=1)
split_df= split_df.reset_index()



#%%


#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
split_df.to_sql(name='collectiondates_es', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")

#%%


#%%
import pandas as pd
numrows= cursor.execute("CREATE TABLE IF NOT EXISTS EscherichiaUSM AS SELECT * FROM collectiondates_escherichia INNER JOIN EscherichiaMergedUS ON collectiondates_escherichia.collectiondate = EscherichiaMergedUS.collection_date")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%

