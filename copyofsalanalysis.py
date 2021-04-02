#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:39:20 2019

@author: jha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:56:57 2019

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


    
    
    



#creating a table where all AST_phenotypes have values 
#%%
new_table= cursor.execute("CREATE TABLE IF NOT EXISTS salamr AS SELECT * FROM Salmonellatest WHERE LENGTH(AST_phenotypes) >20")
print("Selected %s rows" %new_table)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))

#%%



#get the data from the ast table to make the dataframe 
#%%
import pandas as pd
numrows= cursor.execute("SELECT AST_phenotypes FROM sal_ast ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%

#%%
import pandas as pd
numrows= cursor.execute("Select * from salastt limit 20 ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
df=pd.DataFrame(rows)
#df.columns=("Scientific_names", "AST_Phenotypes")
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
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

##%%
#
##df_AST= pd.DataFrame(columns = header_list_AST)
#import re
#for name in header_list_AST:
#    print(name)
#    #name=[]
#    for item in flat_list_sd:
#        if item is not None and name in item:
#            print("the code is at line 125")
##                    print ("the column name at line 124 of code is", item,name1)
#            name.append(item)
##                    print ("at line 121 in code \n", "writing the table into AST dataframe ")
##                    #print("at line 127 in code the item name is ", item)
##                    #var = var+1
##        
#            print("at line 132",item)
#
##%%

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
        #print("the row is",row)
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

cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#df3.to_sql(name='salall', con=cnx, if_exists = 'replace', index=False)
df_sal_ast= pd.read_sql('sal_ast',cnx)

#%%



##%%
#from sqlalchemy import create_engine
#cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#df_ASTT.to_sql(name='salastt', con=cnx, if_exists = 'replace', index=False)
#print("we are at line 186 in code")
#
##%%
#
##%%
#
#numrows= cursor.execute("SELECT * FROM salastt LEFT JOIN sal_ast ON salastt.AST_phenotypes=sal_ast.AST_phenotypes  UNION SELECT * FROM salastt RIGHT JOIN sal_ast ON salastt.AST_phenotypes=sal_ast.AST_phenotypes")
#print("Selected %s rows" %numrows)
#print("Selected %s rows " %cursor.rowcount)
#rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))    
##dffinal = pd.DataFrame(rows) 
#
##%%
#
#
#
##%%
#header_astt=[]
#header_astt= list(df_ASTT.columns)
#header_sal_ast=[]
#header_sal_ast= list(df_sal_ast.columns)
#header_final=[]
#header_final=header_astt+header_sal_ast
#header_final = [s.replace('#label', 'Label') for s in header_final]
#dffinal.columns=header_final
#dffinal=dffinal.drop(dffinal.columns[[0]], axis=1)
#
#
#
#
#
#
#
##%%

##%%
#from sqlalchemy import create_engine
#cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#dffinal.to_sql(name='salfinal', con=cnx, if_exists = 'replace', index=False)
#print("we are at line 186 in code")
#
#
#
##%%



#%%
df_AB=df_AST
df_AB= df_AB.T
df_AB.columns= df_AB.iloc[0]
df_AB=df_AB.drop([0])
df_AB=df_AB.reset_index()
df_AB=df_AB.drop(columns=["index"])

#%%


#writing the ASTphenotype for each drug into sql
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#df_AB.to_sql(name='SLAST', con=cnx, if_exists = 'replace', index=False)
print("we are at line 244 in code")


df_AB= pd.read_sql('SLAST',cnx)

#%%









##%%
#count=0
#for row in df_AB:
#    try:
#        sql_insert = 'SELECT count('+ row +') FROM salfinal WHERE ' +row +'= "S" ;'
#        print (sql_insert)
#        numrows= cursor.execute(sql_insert)
#        rows =cursor.fetchall()#fetch all rows at once
#        print(tabulate(rows, headers=['count'], tablefmt='psql'))    
#    #dffinal = pd.DataFrame(rows) 
#    except:
#        pass
#    
#    
#
#
##%%


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
        val=df5.loc[df5['index'] != "S"]
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
df_plotSNS= pd.DataFrame(list_chunk)

df_plotSNS.columns=["antibiotics","R","I","ND"]
df_plotSNS["non_susceptible"]=df_plotSNS.fillna(0)["R"]+df_plotSNS.fillna(0)["I"] # this line is needed to make non susceptible column by adding R and I columns 
#df_plot.columns=['antibiotics','number_of_S']
#df_plotSNS['percent_nonS'] = ((df_plotSNS['non_susceptible']/1272)*100) 
#df_plotSNS.percent_nonS=df_plotSNS.percent_nonS.round(2)
#                           
##print()
#%%                
                

#Cross-correlation matrix for antibiotics 
#%%
import numpy as np
import sys
cross_df= df_AB
ecdrugs=[]
ecdrugs=cross_df.columns.tolist()
eclist=[]
ec_list=[]
w=len(ecdrugs)
ecmatrix=[[0 for x in range(w)] for y in range(w)]
countx=0

for x in ecdrugs:
    print ("the element in i axis is",x)
    county=0
    try:
        sql1=("SELECT COUNT("+ x +") FROM SLAST WHERE "+ x +"='R' or "+ x +"='I'")
        numrows= cursor.execute("SELECT COUNT("+x+") FROM SLAST WHERE "+x+"='R' or " + x + "='I'")
        print ("the query is",sql1)
        print("Selected %s rows" %numrows)
        print("Selected %s rows " %cursor.rowcount)
        rowx =cursor.fetchall()#fetch all rows at once
            #print(rows)
        for tup in rowx:
            for elex in tup:
                print (elex)
    except:
        print("there is something wrong at line 399")
        continue
        
    #try:
    for y in ecdrugs:
        try:
            print("the element in j axis is", y)
            
            sql=("SELECT COUNT(" + y + ") FROM SLAST where ( " + x + "='R' or " + x + "='I') and ( "+ y + "='I' or " + y + "='R')")
            numrows= cursor.execute("SELECT COUNT(" + y + ") FROM SLAST where ( " + x + "='R' or " + x + "='I') and ( "+ y + "='I' or " + y + "='R')")
            print(sql)
            print("Selected %s rows" %numrows)
            print("Selected %s rows " %cursor.rowcount)
            rows =cursor.fetchall()#fetch all rows at once
            #print(rows)
            for tup in rows:
                for ele in tup:
                    print (ele)
            print(tabulate(rows, headers=[ "count" ], tablefmt='psql'))
            print ("the count for y is: ",county)
            print("the count for x is : ", countx)
            #ecmatrix[countx][county]= rows\
            
            value=ele/elex
            print("the probability of resistance of %s when the sample is already resistant to %s is %s"%( y,x,value)  )
            ecmatrix[countx][county]=round(value,2)
            #print("the matrix is: " ,ecmatrix)
            county= county+1
            
            
            
            
        except:
            print("there is something wrong at line 425")
            continue
    countx=countx+1       




#%%

#editing the matrix to look like the cross correlation matrix
#%%
    
cross_df=pd.DataFrame(ecmatrix)
#cross_df.drop()
#cross_df=cross_df.reset_index()
new_col=[]
cross_df.columns=ecdrugs
cross_df = cross_df.loc[:, (cross_df != 0).any(axis=0)]# used to delete columns 
new_col= cross_df.columns.values.tolist()
cross_df=cross_df.T
cross_df = cross_df.loc[:, (cross_df != 0).any(axis=0)]# used to delete columns 
cross_df.columns=new_col

#cross_df=cross_df.T
#
#%%


#Cross correlation matrix
#%%

from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a large random dataset
#rs = np.random.RandomState(33)
#d = pd.DataFrame(data=rs.normal(size=(100, 26)),
#                columns=list(ascii_letters[26:]))

# Compute the correlation matrix
#corr = d.corr()
corr=cross_df
# Generate a mask for the upper triangle
#mask = np.zeros_like(corr, dtype=np.bool)
#mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


plt.title("Salmonella")







#%%


































 
#%%
#df_plotSNS_sorted=df_plotSNS.sort_values('percent_nonS',ascending=False)
#ax = df_plotSNS_sorted.plot.bar(x='antibiotics', y='percent_nonS', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotSNS_sorted['percent_nonS']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of Salmonella samples found non-Susceptible to antibiotics (1272 samples)")
#plt.ylabel("percentage of nonS")
#plt.plot(x,y)
#plt.show()
#



#%%               
                
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotSNS.to_sql(name='SNS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%               
                



#for graphing the susceptible microbes
#%%
        
chunk2=[]
chunk3=[]
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
        df6=df_AB[row].value_counts().reset_index()
        val=df6.loc[df6['index'] == "S"]
        val=val.T
        val=val.reset_index()
        val=val.drop([0])
        print("before saving to list)")
        chunk3.append(val.values.tolist())
        #val.columns=['antibiotic','number_of_S']
        
        
        
        
        
        #df=pd.DataFrame('antibiotics': val[])
    #    print("yes",val)
        #chunk= [df5.columns.values.tolist()] + df5.values.tolist()
    #    df_plot_C=pd.concat(series5)
    except:
        pass   
    
    
    
    
    
    
#%%
    
    

    
#%%
list_chunkS=[]       
for x in chunk3:
            print(x)
            for y in x:
                print(y)
                list_chunkS.append(y)    
    
    
#%%
        
#%%
        
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
df_plotSS= pd.DataFrame(list_chunkS)

df_plotSS.columns=["antibiotics","Susceptible"]
#df_plotSS['percent_S'] = ((df_plotSS['Susceptible']/1272)*100) 
#df_plotSS.percent_S=df_plotSS.percent_S.round(2)
#                           
##print()
#%%


#%%
#df_plotSS_sorted=df_plotSS.sort_values('percent_S',ascending=False)
#ax = df_plotSS_sorted.plot.bar(x='antibiotics', y='percent_S', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotSS_sorted['percent_S']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of Salmonella samples found Susceptible to antibiotics(1272 samples)")
#plt.ylabel("percentage of S")
#plt.plot(x,y)
#plt.show()
#
#


#%%


#%%

df_plotSS_dict=df_plotSS.set_index('antibiotics')['Susceptible'].to_dict()

df_plotSNS['Susceptible'] = df_plotSNS['antibiotics'].map(df_plotSS_dict)
df_plotSNS["Total_Samples"]=df_plotSNS.fillna(0)["Susceptible"]+ df_plotSNS.fillna(0)["non_susceptible"]

df_plotSNS['percent_S'] = ((df_plotSNS['Susceptible']/df_plotSNS["Total_Samples"])*100) 


df_plotSNS['percent_nonS'] = ((df_plotSNS['non_susceptible']/df_plotSNS["Total_Samples"])*100) 





#%%


#%%
df_plotSNS_sorted=df_plotSNS.sort_values('percent_S',ascending=False)
df_plotSNS_sorted.percent_nonS=df_plotSNS.percent_S.round(0)
df_plotSNS_sorted.percent_nonS=df_plotSNS.percent_nonS.round(0)


#%%





#%%

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

r=[]
r= list(df_plotSNS_sorted["antibiotics"])
bars1=[]

bars1= list(df_plotSNS_sorted.fillna(0)["percent_nonS"])

bars2=[]

bars2=list(df_plotSNS_sorted.fillna(0)["percent_S"])
p1=plt.bar(r, bars1, color='#b5ffb9', edgecolor='white', width=1,label="Susceptible")
# Create green bars (middle), on top of the firs ones
p2=plt.bar(r, bars2, bottom=bars1, color='#f9bc86', edgecolor='white', width=1,label="non-Susceptible")
plt.xticks(r,rotation=90)
plt.xlabel("antibiotics")
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
plt.title("Percentage of Salmonella samples tested ( 1272 samples)")
plt.ylabel("percentage")

rects1 = p1.patches
labels1 = ["%d" % i for i in (df_plotSNS_sorted.fillna(0)["Susceptible"])]
for rect, label in zip(rects1, labels1):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="black", fontsize=8,fontweight="bold")


rects2 = p2.patches
labels2 = ["%d" % i for i in df_plotSNS_sorted.fillna(0)["non_susceptible"]]
for rect, label in zip(rects2, labels2):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., 100-height, label,ha='center', va='top',color="blue", fontsize=8,fontweight="bold")


rects1 = p1.patches
labels3 = ["%d" % i for i in df_plotSNS_sorted.fillna(0)["Total_Samples"]]
for rect, label in zip(rects2, labels3):
    height=41
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="maroon", fontsize=8,fontweight="bold")



plt.show()





#%%





#%%

#writing the list of drugs into an excel file for classification

# import xlsxwriter module 
import xlsxwriter 
  
workbook = xlsxwriter.Workbook('Salmonella.xlsx') 
worksheet = workbook.add_worksheet() 
  
# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 0
column = 0
  
content = header_list_AST
  
# iterating through content list 
for item in content : 
  
    # write operation perform 
    worksheet.write(row, column, item) 
  
    # incrementing the value of row by one 
    # with each iteratons. 
    row += 1
      
workbook.close() 











#%%





#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotSS.to_sql(name='SS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%



    
    
#%%   
list_bugs=["salfinal","Ecolifinal","LSTRfinal","CMPBast"]
list_gloc=[]
for x in list_bugs:
    print(x)
    sql=("select geo_loc_name, count(geo_loc_name) from " +x+ " group by geo_loc_name;")
    print(sql)
    numrows= cursor.execute("select geo_loc_name, count(geo_loc_name) from " +x+ " group by geo_loc_name;")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    rows =cursor.fetchall()#fetch all rows at once
    print(tabulate(rows, headers=["geo_loc_name","count"], tablefmt='psql')) 
    df_sample = pd.DataFrame(rows) 
    df_sample.columns=["geo_loc_name","number_of_Sal_samples"]
    list_loc=[]
    list_loc=df_sample["geo_loc_name"].tolist()
    for index in list_loc:
        list_gloc.append(index)
list_gloc=list(set(list_gloc))
gloc_df=pd.DataFrame()
gloc_df["Location"]=list_gloc    
    
#%%

#%%

list_bugs=["salfinal","Ecolifinal","LSTRfinal","CMPBast"]
list_gloc=[]
for x in list_bugs:
    print(x)
    sql=("select geo_loc_name, count(geo_loc_name) from " +x+ " group by geo_loc_name;")
    print(sql)
    numrows= cursor.execute("select geo_loc_name, count(geo_loc_name) from " +x+ " group by geo_loc_name;")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    lst=list(cursor.fetchall())#fetch all rows at once
    lstd=dict(lst) 

    gloc_df[x] = gloc_df['Location'].map(lstd)





#%%

#%%


#%%



#%%


list_gloc=gloc_df["Location"].tolist()
for row in list_gloc:
    loc=list_gloc.index(row)
    row1=row.split(":")[-1]
    list_gloc.remove(row)
    list_gloc.insert(loc,row1)
#        row= row.split(":")[-1]
    print (row) 
gloc_df["Location"]=list_gloc
#%% 

#%%  
gloc_df["total_samples"]= gloc_df.fillna(0)["salfinal"]+ gloc_df.fillna(0)["Ecolifinal"]+gloc_df.fillna(0)["LSTRfinal"]+gloc_df.fillna(0)["CMPBast"]
gloc_df["salmonella_percent"]=gloc_df.fillna(0)["salfinal"]/gloc_df.fillna(0)["total_samples"]*100
gloc_df["listeria_percent"]=gloc_df.fillna(0)["LSTRfinal"]/gloc_df.fillna(0)["total_samples"]*100
gloc_df["ecoli_percent"]=gloc_df.fillna(0)["Ecolifinal"]/gloc_df.fillna(0)["total_samples"]*100
gloc_df["campylobacter_percent"]=gloc_df.fillna(0)["CMPBast"]/gloc_df.fillna(0)["total_samples"]*100
gloc_df.salmonella_percent=gloc_df.salmonella_percent.round(0)
gloc_df.listeria_percent=gloc_df.listeria_percent.round(0)
gloc_df.ecoli_percent=gloc_df.ecoli_percent.round(0)
gloc_df.campylobacter_percent=gloc_df.campylobacter_percent.round(0)
#for col in df_sample.columns:
#    df[col] = df[col].astype(str)
#%%


#%%  
import plotly
import plotly.graph_objs as go  
scl = [
    [0.0, 'rgb(242,240,247)'],
    [0.2, 'rgb(218,218,235)'],
    [0.4, 'rgb(188,189,220)'],
    [0.6, 'rgb(158,154,200)'],
    [0.8, 'rgb(117,107,177)'],
    [1.0, 'rgb(84,39,143)']
]
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')




gloc_df['text'] = gloc_df['Location'].astype(str) + '<br>' + \
        'salmonella ' + gloc_df['salmonella_percent'].astype(str) +'<br>' +  ' Listeria ' + gloc_df['listeria_percent'].astype(str) + '<br>' + \
        'Campylobacter ' + gloc_df['campylobacter_percent'].astype(str) +'<br>' + ' Ecoli ' + gloc_df['ecoli_percent'].astype(str) 
data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = gloc_df['Location'],
    z = gloc_df['total_samples'].astype(float),
    locationmode = 'USA-states',
    text = gloc_df['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "in integers")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'number of samples collected and tested for Salmonella to anitibiotics over the years '
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig)
















#%%
    
#%%    
scl = [
    [0.0, 'rgb(242,240,247)'],
    [0.2, 'rgb(218,218,235)'],
    [0.4, 'rgb(188,189,220)'],
    [0.6, 'rgb(158,154,200)'],
    [0.8, 'rgb(117,107,177)'],
    [1.0, 'rgb(84,39,143)']
]
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')




df_sample['text'] =  df_sample['location'].astype(str) + '<br>' + \
    'number_of_samples ' + df_sample['count'].astype(str) 

data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = df_sample['location'],
    z = df_sample['count'].astype(float),
    locationmode = 'USA-states',
    text = df_sample['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "in integers")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'number of samples collected and tested for amr to anitibiotics over the years '
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig)
















#%%

#chechk for offline connection of plotly plot
#%%
import plotly
import plotly.graph_objs as go

plotly.offline.plot({
    "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": go.Layout(title="hello world")
}, auto_open=True)

#%%



#test code for plotly check
#%%
import plotly
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

for col in df.columns:
    df[col] = df[col].astype(str)

scl = [
    [0.0, 'rgb(242,240,247)'],
    [0.2, 'rgb(218,218,235)'],
    [0.4, 'rgb(188,189,220)'],
    [0.6, 'rgb(158,154,200)'],
    [0.8, 'rgb(117,107,177)'],
    [1.0, 'rgb(84,39,143)']
]

df['text'] = df['state'] + '<br>' + \
    'Beef ' + df['beef'] + ' Dairy ' + df['dairy'] + '<br>' + \
    'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
    'Wheat ' + df['wheat'] + ' Corn ' + df['corn']

data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = df['code'],
    z = df['total exports'].astype(float),
    locationmode = 'USA-states',
    text = df['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "Millions USD")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = '2011 US Agriculture Exports by State<br>(Hover for breakdown)'
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = 'd3-cloropleth-map')

#%%




#%%
import copy
dict_of_dfs = []
df_list=[]
for item in header_list_AST:
    try:
        print(item)
        sql_query='SELECT geo_loc_name,count(geo_loc_name) FROM salfinal WHERE ' +item +'= "R" GROUP BY geo_loc_name ;'
        print (sql_query)
        num_rows=cursor.execute(sql_query)
        print("Selected %s rows" %numrows)
        print("Selected %s rows " %cursor.rowcount)
        rows =cursor.fetchall()#fetch all rows at once
        print(tabulate(rows, headers=["geo_loc_name","count"], tablefmt='psql')) 
        df_geo=pd.DataFrame(rows)
        df_list=list(df_geo)
        print("at line 547 in code a list should be made)" )
        dict_of_dfs=list.append(df_list)
    except:
        pass



#%%
        
#%%
dict_of_dfs   
    
    
#%%