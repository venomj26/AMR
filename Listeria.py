#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:39:20 2019

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
new_table= cursor.execute("CREATE TABLE IF NOT EXISTS klebsiellaast AS SELECT * FROM Klebsiella WHERE AST_phenotypes LIKE '%=%'")
print("Selected %s rows" %new_table)
print("Selected %s rows " %cursor.rowcount)
#rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))

#%%



#get the data from the ast table to make the dataframe 
#%%
import pandas as pd
numrows= cursor.execute("SELECT AST_phenotypes FROM Klebsiellaast ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
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
##                    print("at line 127 in code the item name is ", item)
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
    print(x)
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
            #print ("the row has been split to ",row)
            
print("the rows have been split")







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
#from sqlalchemy import create_engine
#
#cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
##df3.to_sql(name='salall', con=cnx, if_exists = 'replace', index=False)
#df_sal_ast= pd.read_sql('LSTRast',cnx)

#%%


#run this code only once to create the astt table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_ASTT.to_sql(name='Klebsiellaastt', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")

#%%

#%%

numrows= cursor.execute("SELECT * FROM Klebsiellaastt LEFT JOIN Klebsiellaast ON Klebsiellaastt.AST_phenotypes=Klebsiellaast.AST_phenotypes  UNION SELECT * FROM Klebsiellaastt RIGHT JOIN Klebsiellaast ON Klebsiellaastt.AST_phenotypes=Klebsiellaast.AST_phenotypes")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))    
dffinal = pd.DataFrame(rows) 

#%%



#%%
header_astt=[]
header_astt= list(df_ASTT.columns)
header_sal_ast=[]
header_sal_ast= list(df_sal_ast.columns)
header_final=[]
header_final=header_astt+header_sal_ast
header_final = [s.replace('#label', 'Label') for s in header_final]
dffinal.columns=header_final
dffinal=dffinal.drop(dffinal.columns[[0]], axis=1)







#%%



#run this code snippet just once to create the final table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
dffinal.to_sql(name='Klebsiellafinal', con=cnx, if_exists = 'replace', index=False)
print("we are at line 244 in code")



#%%



#%%
df_AB=df_AST
df_AB= df_AB.T
df_AB.columns= df_AB.iloc[0]
df_AB=df_AB.drop([0])
df_AB=df_AB.reset_index()
df_AB=df_AB.drop(columns=["index"])

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
df_plotLNS= pd.DataFrame(list_chunk)

df_plotLNS.columns=["antibiotics","R","I","ND"]
df_plotLNS["non_susceptible"]=df_plotLNS.fillna(0)["R"]+df_plotLNS.fillna(0)["I"] # this line is needed to make non susceptible column by adding R and I columns 
#df_plot.columns=['antibiotics','number_of_S']
#df_plotLNS['percent_nonS'] = ((df_plotLNS['non_susceptible']/118)*100) 
#df_plotLNS.percent_nonS=df_plotLNS.percent_nonS.round(2)
#                           
##print()
#%%                

#writing the ASTphenotype for each drug into sql
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_AB.to_sql(name='cbnew_ast', con=cnx, if_exists = 'replace', index=False)
print("we have written the ast table for listeria in sql ")




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
    for y in ecdrugs:
        try:
            print("the element in j axis is", y)
            sql1=("SELECT COUNT(" + y + ") FROM cbnew_ast where ( " + x + "='R' or " + x + "='I') and ( "+ y + "='I' or " + y + "='R')")
            numrows= cursor.execute("SELECT COUNT(" + y + ") FROM cbnew_ast where ( " + x + "='R' or " + x + "='I') and ( "+ y + "='I' or " + y + "='R')")
            print ("the query is",sql1)
            print("Selected %s rows" %numrows)
            print("Selected %s rows " %cursor.rowcount)
            rowx =cursor.fetchall()#fetch all rows at once
            #print(rows)
            for tup in rowx:
                for elex in tup:
                    print (elex)
                    
            
            sql=("SELECT COUNT(" + y + ") FROM cbnew_ast where ( " + x + "='R' or " + x + "='I' or "+ x + "= 'S') and ( "+ y + "='I' or " + y + "='R' or "+ y + "= 'S')")
            numrows= cursor.execute("SELECT COUNT(" + y + ") FROM cbnew_ast where ( " + x + "='R' or " + x + "='I'or "+ x + "= 'S') and ( "+ y + "='I' or " + y + "='R' or "+ y + "= 'S')")
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
            value=elex/ele
            print("the probability of resistance of %s when the sample is already resistant to %s is %s"%( y,x,value)  )
            ecmatrix[countx][county]=round(value,2)
            #print("the matrix is: " ,ecmatrix)
            county= county+1
            
            
            
            
        except:
            print("there is something wrong at line 425")
            continue
    countx=countx+1       




#%%
    
    
    
    
    
#cross corelation matrix #2 using percentage of the samples tested for 
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
        sqlx_den=("SELECT COUNT("+ x +") FROM Klebsiella_ast WHERE "+ x +" <> 'NULL'")
        print ("the query is",sqlx_den)
        numrowsx_den= cursor.execute("SELECT COUNT("+ x +") FROM Klebsiella_ast WHERE "+ x +" <> 'NULL'")
        print("Selected %s rows" %numrowsx_den)
        print("Selected %s rows " %cursor.rowcount)
        rowx_den =cursor.fetchall()
        for tup in rowx_den:
            for elex_den in tup:
                print ("the total number of samples tested for the drug",elex_den)
            #print(rows)
        sqlx_num=("SELECT COUNT("+ x +") FROM Klebsiella_ast WHERE "+ x +"='R' or "+ x +"='I'")
        print ("the query is",sqlx_num)
        numrowsx_num= cursor.execute("SELECT COUNT("+x+") FROM Klebsiella_ast WHERE "+x+"='R' or " + x + "='I'")
        print("Selected %s rows" %numrowsx_num)
        print("Selected %s rows " %cursor.rowcount)
        rowx_num =cursor.fetchall()#fetch all rows at once
        print("the out put of select count query for x is ", rowx_num)
        for tup in rowx_num:
            for elex_num in tup:
                print ("the number of samples resistant to the drug",elex_num)
        
        
    except:
        print("there is something wrong at line 399")
        continue
        
    #try:
    for y in ecdrugs:
        try:
            print("the element in j axis is", y)
            #county= county+1
            sqly_num=("SELECT COUNT(" + y + ") FROM Klebsiella_ast where " + y + "='I' or " + y + "='R'")
            numrowsy_num= cursor.execute("SELECT COUNT(" + y + ") FROM Klebsiella_ast where " + y + "='I' or " + y + "='R'")
            print("the query is",sqly_num)
            print("Selected %s rows" %numrowsy_num)
            print("Selected %s rows " %cursor.rowcount)
            rowsy_num =cursor.fetchall()#fetch all rows at once
            #print(rows)
            for tup in rowsy_num:
                for eley_num in tup:
                    print (eley_num)
            print(tabulate(rowsy_num, headers=[ "count" ], tablefmt='psql'))
            
            
            sqly_den=("SELECT COUNT("+ x +") FROM Klebsiella_ast WHERE <> 'NULL'")
            numrowsy_den= cursor.execute("SELECT COUNT("+ y +") FROM Klebsiella_ast WHERE "+ y +"  <> 'NULL'")
            print("the query is",sqly_den)
            print("Selected %s rows" %numrowsy_den)
            print("Selected %s rows " %cursor.rowcount)
            rowsy_den =cursor.fetchall()#fetch all rows at once
            #print(rows)
            for tup in rowsy_den:
                for eley_den in tup:
                    print (eley_den)
            value=(elex_num + eley_num)/(elex_den + eley_den)
            print("the percentage of resistance of %s and %s is %s"%( y,x,value)  )
            ecmatrix[countx][county]=round(value,2)
            print("the matrix is: " ,countx,county)
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
f, ax = plt.subplots(figsize=(25, 25))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.1, cbar_kws={"shrink": 0.5})



plt.title("Klebsiella")






#%%








































#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotLNS.to_sql(name='LNS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%



                

#%%
#df_plotLNS_sorted=df_plotLNS.sort_values('percent_nonS',ascending=False)
#ax = df_plotLNS_sorted.plot.bar(x='antibiotics', y='percent_nonS', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotLNS_sorted['percent_nonS']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of cbnew samples found non Susceptible to antibiotics (118 samples)")
#plt.ylabel("percentage of nonS")
#plt.plot(x,y)
#plt.show()




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
df_plotLS= pd.DataFrame(list_chunkS)

df_plotLS.columns=["antibiotics","Susceptible"]
#df_plotLS['percent_S'] = ((df_plotLS['Susceptible']/118)*100) 
#df_plotLS.percent_S=df_plotLS.percent_S.round(2)
##                           
##print()
#%%


#%%

#df_plotLS_sorted=df_plotLS.sort_values('percent_S',ascending=False)
#ax = df_plotLS_sorted.plot.bar(x='antibiotics', y='percent_S', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotLS_sorted['percent_S']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of Listeria samples found Susceptible to antibiotics (118 samples)")
#plt.ylabel("percentage of S")
#plt.plot(x,y)
#plt.show()





#%%


#making the table with each percentage non-susceptible is non-susceptible/(susceptible+non_susceptible) same for susceptible

#%%

df_plotLS_dict=df_plotLS.set_index('antibiotics')['Susceptible'].to_dict()

df_plotLNS['Susceptible'] = df_plotLNS['antibiotics'].map(df_plotLS_dict)
df_plotLNS["Total_Samples"]=df_plotLNS.fillna(0)["Susceptible"]+ df_plotLNS.fillna(0)["non_susceptible"]

df_plotLNS['percent_S'] = ((df_plotLNS['Susceptible']/df_plotLNS["Total_Samples"])*100) 


df_plotLNS['percent_nonS'] = ((df_plotLNS['non_susceptible']/df_plotLNS["Total_Samples"])*100) 





#%%


#%%
df_plotLNS_sorted=df_plotLNS.sort_values('percent_S',ascending=False)
df_plotLNS_sorted.percent_nonS=df_plotLNS.percent_S.round(0)
df_plotLNS_sorted.percent_nonS=df_plotLNS.percent_nonS.round(0)


#%%





#%%

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import matplotlib.patches as mpatches
r=[]
r= list(df_plotLNS_sorted["antibiotics"])
bars1=[]

bars1= list(df_plotLNS_sorted.fillna(0)["percent_nonS"])

bars2=[]

bars2=list(df_plotLNS_sorted.fillna(0)["percent_S"])
p1=plt.bar(r, bars1, color='#b5ffb9', edgecolor='white', width=1,label="Susceptible")
# Create green bars (middle), on top of the firs ones
p2=plt.bar(r, bars2, bottom=bars1, color='#f9bc86', edgecolor='white', width=1,label="non-Susceptible")
plt.xticks(r,rotation=90)
plt.xlabel("antibiotics")
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
plt.title("Percentage of Listeria samples tested ( samples)")
plt.ylabel("percentage")

rects1 = p1.patches
labels1 = ["%d" % i for i in (df_plotLNS_sorted.fillna(0)["Susceptible"])]
for rect, label in zip(rects1, labels1):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="black", fontsize=8,fontweight="bold")


rects2 = p2.patches
labels2 = ["%d" % i for i in df_plotLNS_sorted.fillna(0)["non_susceptible"]]
for rect, label in zip(rects2, labels2):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., 100-height, label,ha='center', va='top',color="blue", fontsize=8,fontweight="bold")


rects1 = p1.patches
labels3 = ["%d" % i for i in df_plotLNS_sorted.fillna(0)["Total_Samples"]]
for rect, label in zip(rects2, labels3):
    height=45
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="maroon", fontsize=8,fontweight="bold")


plt.show()





#%%





#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotLS.to_sql(name='LS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%


#%%
import pandas as pd
numrows= cursor.execute("Describe Klebsiella ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
dfz= pd.DataFrame(rows)

listz=list(dfz[0])
numrows_k= cursor.execute("Select * from Klebsiellaast")
print("Selected %s rows" %numrows_k)
print("Selected %s rows " %cursor.rowcount)
rows_k =cursor.fetchall()#fetch all rows at once
df_kleb= pd.DataFrame(rows_k)
df_kleb.columns= listz

#%%

#%%
#import os
#
#outname = 'klebsiella.csv'
#
#outdir = '/Users/jha/Documents/Fall2019'
#if not os.path.exists(outdir):
#    os.mkdir(outdir)
#
#fullname = os.path.join(outdir, outname)    


df_kleb.to_excel("klebsiella_ASTfull.xlsx")


#%%




#%%

#writing the list of drugs into an excel file for classification

# import xlsxwriter module 
import xlsxwriter 
  
workbook = xlsxwriter.Workbook('klebsiella_full.xlsx') 
worksheet = workbook.add_worksheet() 
  
# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 0
column = 0
  
content = df_kleb
  
# iterating through content list 
for item in content : 
  
    # write operation perform 
    worksheet.write(row, column, item) 
  
    # incrementing the value of row by one 
    # with each iteratons. 
    row += 1
      
workbook.close() 











#%%