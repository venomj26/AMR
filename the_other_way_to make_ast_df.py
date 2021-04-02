#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:56:57 2019

@author: jha
"""
#%%
import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

#%%


#%%
import csv
import mysql.connector as mariadb
from tabulate import tabulate


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
numrows= cursor.execute("SELECT AST_phenotypes FROM Salmonellatest GROUP BY AST_phenotypes")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
for row in rows:
    for col in rows:
        print("%s,"%col)
    print("\n")
    
#%%    
    
    
    
#%%   
numrows= cursor.execute("SELECT AST_phenotypes, AMR_genotypes FROM Salmonellatest WHERE LENGTH(AST_phenotypes) >24 LIMIT 2 ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(tabulate(rows, headers=['AST_phenotype', 'AMR_genotype'], tablefmt='psql'))  
#%%


#creating a table where all AST_phenotypes have values 
#%%
new_table= cursor.execute("CREATE TABLE IF NOT EXISTS salamr AS SELECT * FROM Salmonellatest WHERE LENGTH(AST_phenotypes) >20")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once


#%%

#check to see if the new table has all datas
#%%
import pandas as pd
numrows= cursor.execute("SELECT AST_phenotypes FROM sal_ast ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%

#splitting the AST_phenotype column values into separate columns of the table 
#%%
df = pd.DataFrame(rows)
#print ("the pandas dataframe ",df
       
df.columns=["AST_phenotypes"]
df.head()
split_df= df['AST_phenotypes'].str.split(',', expand= True)
split_df.head()
#split_df = split_df.drop(split_df.columns[[23]], axis=1) 

#%%
#we are making the column names for the AST dataframes 
#%%
split_df_list=[]
split_df_list = split_df.values.tolist()
flat_list_sd = []
for sublist in split_df_list:
    for item in sublist:
        flat_list_sd.append(item)

#print ("ATline {0} in code split_df has been converted to a list{1}".format(lineno(),flat_list_sd))
split_flsd=[]
for element in flat_list_sd:
    if element != None:
        split_flsd.append(element.split('=', 1)[0]) 
#print ("ATline {0} in code split_df has been converted to a list".format(lineno()))
print("the list of all elements in split_df", split_flsd)
header_set=set(split_flsd)
header_list_AST=list(header_set)

print("at line 87 in code the list of header values are ")



#%%

#%%

#df_AST= pd.DataFrame(columns = header_list_AST)
import re
for name in header_list_AST:
    print(name)
    #name=[]
    for item in flat_list_sd:
        if item is not None and name in item:
            print("the code is at line 125")
#                    print ("the column name at line 124 of code is", item,name1)
            name.append(item)
#                    print ("at line 121 in code \n", "writing the table into AST dataframe ")
#                    #print("at line 127 in code the item name is ", item)
#                    #var = var+1
#        
            print("at line 132",item)

#%%

#the list of antibiotics is populated by the R and S values forming an array. (the result is a list of lists called
#list_list_AST)
#%%
            
def extractDigits(lst): 
    return list(map(lambda el:[el], lst)) 
list_list_AST= extractDigits(header_list_AST)
for x in list_list_AST:
    #print(x)
    for item in flat_list_sd:
        if item is not None and x[0] in item:
            x.append(item)
            #print("printing if equal",x)
        #print("printing table item",item)
    #print ("printing x",x)   
        
        
#%%



#we are using regex to remove the anitibiotic name(ex: ampicillin=R and retain the "R" for each column= DONE)
#%%
for col in list_list_AST:
   # print ("col",col)
    for row in col:
        print("the row is",row)
        if "=" in row:
            #print("row", row)
            loc=col.index(row)
            row1=row.split("=")[-1]
            col.remove(row)
            col.insert(loc,row1)
           # print ("the row has been split to ",row)
            








#%%

#%%
df_AST= pd.DataFrame(list_list_AST)       
df_ASTT=df_AST.T

         
            
#%%

#%%
df_ASTT.columns = df_ASTT.iloc[0] #grab the first row for the header

df_ASTT=df_ASTT.drop([0])# drops the first row which is a header row from dataframe but this also changes the index of the dataframe
df_ASTT=df_ASTT.reset_index()# the change of index in the previous command causes error in the concatenation of the other dataframe
df_ASTT= df_ASTT.drop(columns=['index'])# so reset is used to create a new index and the old index is deleted 
df_ASTT = pd.concat([df,df_ASTT], axis=1, join_axes=[df.index]) 


#%%


#%%
from sqlalchemy import create_engine
import pandas as pd
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#df3.to_sql(name='salall', con=cnx, if_exists = 'replace', index=False)
df_sal_ast= pd.read_sql('sal_ast',cnx)

#%%



#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_ASTT.to_sql(name='salastt', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")

#%%

#%%

numrows= cursor.execute("SELECT * FROM salastt LEFT JOIN sal_ast ON salastt.AST_phenotypes=sal_ast.AST_phenotypes  UNION SELECT * FROM salastt RIGHT JOIN sal_ast ON salastt.AST_phenotypes=sal_ast.AST_phenotypes;")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))    
dffinal = pd.DataFrame(rows) 

#%%



#%%
header_astt=[]
header_astt= list(df_ASTT.columns)
header_sal_ast=[]
header_sal_ast= list(df_sal_ast.columns)
header_final=[]
header_final=header_astt+header_sal_ast
dffinal.columns=header_final
dffinal=dffinal.drop(dffinal.columns[[0]], axis=1)







#%%

#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
dffinal.to_sql(name='salfinal', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")



#%%



#%%
df_AB=df_AST
df_AB= df_AB.T
df_AB.columns= df_AB.iloc[0]
df_AB=df_AB.drop([0])
df_AB=df_AB.reset_index()
df_AB=df_AB.drop(columns=["index"])

#%%





#%%
count=0
for row in df_AB:
    try:
        sql_insert = 'SELECT count('+ row +') FROM salfinal WHERE ' +row +'= "S" ;'
        print (sql_insert)
        numrows= cursor.execute(sql_insert)
        rows =cursor.fetchall()#fetch all rows at once
        print(tabulate(rows, headers=['count'], tablefmt='psql'))    
    #dffinal = pd.DataFrame(rows) 
    except:
        pass
    
    


#%%


#%%
chunk=[]
chunk1=[]
for row in df_AB.columns:
    try:
        print(row)
        #print(df_AB[row].value_counts().index.to_list())
        #df_plot=(df_AB[row].value_counts().index.to_list())
        
        #df_plot=pd.merge((df_AB[row].value_counts().to_frame()), on )
        #print(df_AB[row].value_counts().to_frame())
        #df_plot= df.append(df_AB[row].value_counts(), ignore_index=True)
        #print("line 312")
        
        print(df_AB[row].value_counts().reset_index())
        df5=df_AB[row].value_counts().reset_index()
        val=df5.loc[df5['index'] == "S"]
        val=val.T
        val=val.reset_index()
        val=val.drop([0])
        print("before saving to list)")
        chunk1.append(val.values.tolist())
        #val.columns=['antibiotic','number_of_S']
        
        
        
        
        #df=pd.DataFrame('antibiotics': val[])
    #    print("yes",val)
        #chunk= [df5.columns.values.tolist()] + df5.values.tolist()
    #    df_plot_C=pd.concat(series5)
    except:
        pass
    

    
#%%
        
    
#%%
list_chunk=[]       
for x in chunk1:
            print(x)
            for y in x:
                print(y)
                list_chunk.append(y)    
    
    
#%%
        
#%%
        
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
df_plot= pd.DataFrame(list_chunk)
df_plot.columns=['antibiotics','number_of_S']
df_plot['percent_S'] = ((df_plot['number_of_S']/1272)*100) 
                           
#print()
ax = df_plot.plot.bar(x='antibiotics', y='number_of_S', rot=90,legend=False,    # Turn the Legend off
        width=0.75,      # Set bar width as 75% of space available
        figsize=(15,6),  # Set size of plot in inches
        colormap='summer')
for index,data in enumerate(df_plot['percent_S']):
    plt.text(x=index , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=5))
#plt.plot(x,y)
#plt.show()




#%%

















