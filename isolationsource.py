#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:40:52 2020

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
numrows= cursor.execute("SELECT isolation_source FROM Escherichia_MergedF")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%


#splitting the collection_date column values into separate columns to get a separate column for date 
#%%
#df = pd.DataFrame(rows)
list_rows=[item for t in rows for item in t] 
list_epi=[]
for index,item in enumerate(list_rows):
    #print(item)
    if 'beef'in item:
        print ("it was beef")
        list_rows[index]= "beef/beefproduct"
    elif 'farm' in item :
        print("it was farm")
    
    else:
       list_rows[index]= "clinical" 
       print("it was clinical")

#%%
       
       


#%%
df = pd.DataFrame(list_rows,columns=['isolate_epi_type']) 
df['isolationsource']= pd.DataFrame(rows)   
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df.to_sql(name='isolationsource_es', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")

#%%      




#best way to read table from sql
#%%
import pandas as pd
numrows= cursor.execute("Describe Escherichia_isolateepi")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
dfz= pd.DataFrame(rows)

listz=list(dfz[0])
numrows_k= cursor.execute("Select * from Escherichia_isolateepi")
print("Selected %s rows" %numrows_k)
print("Selected %s rows " %cursor.rowcount)
rows_k =cursor.fetchall()#fetch all rows at once
df_kleb= pd.DataFrame(rows_k)
df_kleb.columns= listz

#%%


#%%
import pandas as pd
numrows= cursor.execute("Describe Escherichia_nov_astt")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
df_col_name= pd.DataFrame(rows)
list_col_name=list(df_col_name[0])

del list_col_name[0]
del list_col_name[0]


#%%

#df_crosstab=pd.crosstab(df_kleb.isolate_epi_type, df_kleb.cefoxitin, margins=True, margins_name="total samples" , normalize= 'all').round(4)*100
#df_crosstab=df_crosstab.T
#df_crosstab.to_excel('escherichia_isolation_astphenotypes_crosstab.xlsx')  

    
df_crosstab=pd.crosstab(df_kleb.isolate_epi_type, df_kleb.cefoxitin,df_kleb.Collection_year, margins=True, margins_name="total samples")

 

#%%

#for getting all the antimicrobials
#%%
 #def crosstab_all(df_kleb,list_col_name):
 appended_data=[]
for k in list_col_name:
    try:
        xdf=pd.crosstab(df_kleb["isolate_epi_type"],df_kleb[k], margins=True, margins_name="Out of total samples")
        xdf["Antimicrobial"] = k
        print('xdf',xdf)
        print('') # for spacing
        appended_data.append(xdf)
       
             
    except:
        print("not found")
        continue
appended_data = pd.concat(appended_data, sort= False) 
appended_data.loc[appended_data['Antimicrobial'].duplicated(), 'Antimicrobial'] = np.nan
#%%




#for only those antimicrobials which were tested for more than one epitypes
#%%
 #def crosstab_all(df_kleb,list_col_name):
 appended_data=[]
for k in list_col_name:
    try:
        xdf=pd.crosstab(df_kleb["isolate_epi_type"],df_kleb[k], margins=True, margins_name="All Samples Combined")
        xdf["Antimicrobial"] = k
        print('xdf',xdf)
        print('') # for spacing
        if len(xdf.index) >2:
            appended_data.append(xdf)
        else:
            print("only one epitype tested")
             
    except:
        print("not found")
        continue
appended_data= pd.concat(appended_data, sort= False) 

#%%


#%%

df_family = pd.read_excel('/Users/jha/Documents/spring2020/ecoli_antimicrobial_class.xlsx', sheet_name='Sheet1')
df_family_mod= df_family
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_family=list(df_family.itertuples(index=False, name=None))
#list_family=list(df_family)
family_dict=dict(list_family)

appended_data['Antimicrobial_class']=appended_data['Antimicrobial'].map(family_dict)
appended_data = appended_data.reset_index()

appended_data= (appended_data.groupby(['Antimicrobial_class', 'Antimicrobial','isolate_epi_type']).sum())
appended_data = appended_data.reset_index()
appended_data.loc[appended_data['Antimicrobial'].duplicated(), 'Antimicrobial'] = np.nan
appended_data.loc[appended_data['Antimicrobial_class'].duplicated(), 'Antimicrobial_class'] = np.nan
appended_data = appended_data.set_index(['Antimicrobial_class', 'Antimicrobial'])


#cols=["isolate_epi_type","S","R","I"]
#appended_data =appended_data[cols]

#%%

#for only those antimicrobials which were tested for more than one epitypes
#%%
 #def crosstab_all(df_kleb,list_col_name):
 appended_data_P=[]
for k in list_col_name:
    try:
        xdf=pd.crosstab(df_kleb["isolate_epi_type"],df_kleb[k], margins=True, margins_name="All Samples Combined", normalize="index").round(4)*100
        xdf["Antimicrobial"] = k
        print('xdf',xdf)
        print('') # for spacing
        if len(xdf.index) >2:
            appended_data_P.append(xdf)
        else:
            print("only one epitype tested")
             
    except:
        print("not found")
        continue
appended_data_P= pd.concat(appended_data_P, sort= False) 

#%%


#to merge the appended tables to get frequency and percentage in the same table
#%%

appended_data_P=appended_data_P.rename(columns = {"S": "%Susceptible", 
                                  "R":"%Resistant", 
                                  "I": "%Intermediate"})
appended_data=appended_data.reset_index()
appended_data=appended_data.reset_index()
appended_data_P=appended_data_P.reset_index()
appended_data_P=appended_data_P.reset_index()
appended_dict = dict(zip(appended_data.index, appended_data.S))
appended_data_P["Susceptible"]=appended_data_P['index'].map(appended_dict)

appended_dict = dict(zip(appended_data.index, appended_data.R))
appended_data_P["Resistant"]=appended_data_P['index'].map(appended_dict)

appended_dict = dict(zip(appended_data.index, appended_data.I))
appended_data_P["Intermediate"]=appended_data_P['index'].map(appended_dict)

appended_data_P=appended_data_P.drop("index", axis=1)
appended_data=appended_data.drop("index", axis=1)
#appended_data = appended_data.set_index(['Collection_year'])

#%%


#%%

df_family = pd.read_excel('/Users/jha/Documents/spring2020/ecoli_antimicrobial_class.xlsx', sheet_name='Sheet1')
df_family_mod= df_family
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_family=list(df_family.itertuples(index=False, name=None))
#list_family=list(df_family)
family_dict=dict(list_family)

appended_data_P['Antimicrobial_class']=appended_data_P['Antimicrobial'].map(family_dict)


appended_data_P= (appended_data_P.groupby(['Antimicrobial_class', 'Antimicrobial','isolate_epi_type']).sum())
appended_data_P = appended_data_P.reset_index()
appended_data_P.loc[appended_data_P['Antimicrobial'].duplicated(), 'Antimicrobial'] = np.nan
appended_data_P.loc[appended_data_P['Antimicrobial_class'].duplicated(), 'Antimicrobial_class'] = np.nan
appended_data_P = appended_data_P.set_index(['Antimicrobial_class', 'Antimicrobial'])


cols=["isolate_epi_type","%Susceptible","Susceptible","%Resistant","Resistant","%Intermediate","Intermediate"]
appended_data_P =appended_data_P[cols]

#%%








#%%
import pandas as pd
from openpyxl import load_workbook
path=  "/Users/jha/escherichia_isolation_antimicrobial_crosstab.xlsx"


book = load_workbook(path)
writer = pd.ExcelWriter(path, engine = 'openpyxl')
writer.book = book


appended_data_P.to_excel(writer, sheet_name="iso-byindex_freq_Per")
writer.save()
writer.close()
    
#%%