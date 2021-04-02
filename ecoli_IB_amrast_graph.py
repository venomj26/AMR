#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:06:49 2020

creating and AMR AST correlation graph

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

#writing data table into an excel file
#%%
import pandas as pd
numrows= cursor.execute("Describe EcoliIBisodatlocMerge")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
dfz= pd.DataFrame(rows)

listz=list(dfz[0])
numrows_k= cursor.execute("Select * from EcoliIBisodatlocMerge")
print("Selected %s rows" %numrows_k)
print("Selected %s rows " %cursor.rowcount)
rows_k =cursor.fetchall()#fetch all rows at once
df_kleb= pd.DataFrame(rows_k)
df_kleb.columns= listz
#df_kleb.to_excel("EcoliIBIsomerged.xlsx")
#%%




#%%
import pandas as pd
numrows= cursor.execute("Describe Ecoli_IB_amr")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
df_col_name_amr= pd.DataFrame(rows)
list_col_name_amr=df_col_name_amr[0].to_list()

del list_col_name_amr[0]
del list_col_name_amr[0] 


#%%


#%%
import pandas as pd
numrows= cursor.execute("Describe Ecoli_IB_AST ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
df_col_name_ast= pd.DataFrame(rows)
list_col_name_ast=df_col_name_ast[0].to_list()

del list_col_name_ast[0]
del list_col_name_ast[0]


#%%

#not used
#%%
list_col_name_amr_mod=list_col_name_amr
list_col_name_ast_mod=list_col_name_ast
list_col_name_amr_mod.append('Isolate')
list_col_name_ast_mod.append('Isolate')
df_amr=df_kleb[list_col_name_amr_mod]
df_ast=df_kleb[list_col_name_ast_mod]

#%%

#%%
df_impgenes = pd.read_excel('/Users/jha/important_genes.xlsx', sheet_name='Sheet1')
list_impgenes=df_impgenes["AMR_Gene"].to_list()
#%%



#%%
try:
    appended_data=[]
    for k in list_col_names_ast:
        try:
            xdf_crosstab=pd.crosstab(df_kleb["Isolate"],df_kleb[k])
            xdf_crosstab["AMR_gene"] = k
            print('xdf',xdf_crosstab)
            print('') # for spacing
            if len(xdf_crosstab.index) >3:
                appended_data.append(xdf_crosstab)
            else:
                print("only one epitype tested")
                 
        except:
            print("not found")
            continue
    appended_data= pd.concat(appended_data, sort= False) 
    appended_data=appended_data.drop("missing")
    appended_data=appended_data.drop("")
    #appended_data_P=appended_data_P.drop("DD", axis=1)
except:
    print("some error in gene",k)




#%%
#for AST value count
#%%
    
df_astvc=appended_data["Antimicrobial"].value_counts()
df_astvc=df_astvc.reset_index()
df_astvc=df_astvc.drop(df_astvc.index[0])
df_astvc.columns=["Antimicrobial","total_Samples_tested"]
list_astvc=list(df_astvc.itertuples(index=False, name=None))
#list_family=list(df_family)
astvc_dict=dict(list_astvc)
#%%

#for AMR genes value count
#%%
    
df_genevc=appended_data["AMR_gene"].value_counts()
df_genevc=df_genevc.reset_index()
#df_genevc=df_genevc.drop(df_genevc.index[0])
df_genevc.columns=["AMR_gene","total_Samples_tested"]
list_genevc=list(df_genevc.itertuples(index=False, name=None))
#list_family=list(df_family)
genevc_dict=dict(list_genevc)
#%%
  
    
#for all AST : this is required so that only resistant antimicrobials can be included
#%%
appended_data= appended_data.drop(["ND","SDD","S","DNE"], axis=1)
appended_data["Non-Susceptible"]= appended_data.sum(axis=1)
appended_data= appended_data.drop(["I","R"], axis=1)

#%%
# for AST
#%%
appended_data['Non-Susceptible'] = appended_data['Non-Susceptible'].replace(0, np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Non-Susceptible'])
#%%


#for AST
#%%
df_ast=appended_data.reset_index()
df_ast=df_ast.drop(["Non-Susceptible"],axis=1)

df_ast['Antimicrobial'] = df_ast['Antimicrobial'].replace('amr_VALUE', np.nan)
df_ast = df_ast.dropna(axis=0, subset=['Antimicrobial'])
#df_ast= df_ast.groupby(['Isolate'])
#df_amr=df_amr.reset_index()
#df_amr.to_excel("amrcrosstab.xlsx")

#%%%

#this is incase the antimicrobial class column is not needed in the finat df_ast (this has not been used in this current graph)
#%%
df_family = pd.read_excel('/Users/jha/Documents/spring2020/ecoli_antimicrobial_class.xlsx', sheet_name='Sheet1')
df_family_mod= df_family
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_family=list(df_family.itertuples(index=False, name=None))
#list_family=list(df_family)
family_dict=dict(list_family)
df_astcol=df_ast[["Antimicrobial"]].copy().drop_duplicates()
df_astcol.columns=["AMR_Gene"]
df_astcol['Antimicrobial_class']=df_astcol ['AMR_Gene'].map(family_dict)
df_astcol=df_astcol.sort_values("Antimicrobial_class")
col=[]
col=df_astcol["AMR_Gene"].to_list()
#%%
#this is being used to map the antimicrobial class to the df_ast dataframe so that the pivot table can be grouped by the antimicrobial family
#%%
df_family = pd.read_excel('/Users/jha/Documents/spring2020/ecoli_antimicrobial_class.xlsx', sheet_name='Sheet1')
df_family_mod= df_family
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_family=list(df_family.itertuples(index=False, name=None))
#list_family=list(df_family)
family_dict=dict(list_family)
df_ast['Antimicrobial_class']=df_ast ['Antimicrobial'].map(family_dict)
df_ast=df_ast.sort_values("Antimicrobial_class")
#col=[]
#col=df_astcol["AMR_Gene"].to_list()
#%%


#for all genes

#%%
#appended_data= appended_data.drop(["HMM","MISTRANSLATION","PARTIAL","POINT","PARTIAL_END_OF_CONTIG","COMPLETE","DNE"], axis=1)
appended_data2= appended_data.drop(["MISTRANSLATION","PARTIAL","POINT","PARTIAL_END_OF_CONTIG","COMPLETE"], axis=1) #for imp 45 genes
df_amr=appended_data2.reset_index()
df_amr['AMR_gene'] = df_amr['AMR_gene'].replace('VALUE', np.nan)
df_amr = df_amr.dropna(axis=0, subset=['AMR_gene'])
#%%
#%%

#df_amrast is merged on df_AMR so it will have as many rows as df_AMR (genes)
#%%

df_amrast=df_ast.merge(df_amr,left_on="Isolate",right_on="Isolate")
#%%


#%%

df = pd.pivot_table(df_amrast,index=["Isolate"],columns=["Antimicrobial"],values=["AMR_gene"],aggfunc=','.join, fill_value= 'None' )
#df.to_excel("amrast_45.xlsx")
#%%
#df_amrast2 is merged on df_AST so it will have as many rows as df_AST (antimicrobials)
#%%
df_amrast2=df_amr.merge(df_ast,left_on="Isolate",right_on="Isolate")
df2 = pd.pivot_table(df_amrast2,index=["Isolate"],columns=["AMR_gene"],values=["Antimicrobial"],aggfunc=','.join, fill_value= 'None' )
#df2.to_excel("amrast2`_45.xlsx")
#%%

#%%

df3 = pd.pivot_table(df_amrast2,index=["AMR_gene"],columns=["Antimicrobial_class","Antimicrobial"],values=["Isolate"],aggfunc='count', fill_value= 'None' )
#df3.to_excel("amrast3``_41gene`.xlsx")
#%%
#Calculating the percentage out of the total sample
#%%
df3=df3.T
df3=df3.reset_index()
df3=df3.replace('None',np.nan)
df3['total_tested_samples']=df3['Antimicrobial'].map(astvc_dict)
#
df3.loc[:,"aac(3)-IId":"uhpT_E350Q"] = df3.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(df3["total_tested_samples"], axis=0)#divinding by last column
df3=df3.drop('total_tested_samples',axis=1)
df3=df3.groupby(['level_0','Antimicrobial_class','Antimicrobial']).sum()

#%%

#%%
df3=df3.groupby(['level_0','Antimicrobial_class','Antimicrobial']).sum()
df3=df3*100
df3=df3.T
df3.to_excel("amrast8888.xlsx")

#%%


#%%

df3 = pd.pivot_table(df_amrast2,index=["Antimicrobial_class","Antimicrobial"],columns=["AMR_gene"],values=["Isolate"],aggfunc='count', fill_value= 'None' )
#df3.to_excel("amrast3``_41gene`.xlsx")
#%%

#Calculating the percentage out of the total sample for 41 genes (NOT DONE/INCOMPLETE)
#%%
df3.columns = df3.columns.droplevel(0)
df3=df3.T
df3=df3.reset_index()
df3['total_tested_samples']=df3['AMR_gene'].map(genevc_dict)
df3=df3.set_index("AMR_gene")
df3=df3.T
#df3=df3.reset_index()
##df3=df3.drop('Antimicrobial_class',axis=1)
df3=df3.replace('None',np.nan)
df3.loc[:,"aac(3)-IId":] = df3.loc[:,"aac(3)-IId":].div(df3.iloc[-1]["total_tested_samples":])# dividing by last row
df3=df3*100
df3=df3.T
df3=df3.round(2)
df3.to_excel("amrast8888gene.xlsx")
##df3=df3.groupby(['level_0','Antimicrobial_class','Antimicrobial']).sum()

#%%



#%%

df4 = pd.pivot_table(df_amrast2,index=["Isolate"],columns=["AMR_gene"],values=["Antimicrobial_class"],aggfunc=lambda x: len(x.unique()), fill_value= 'None' )
df4.to_excel("test1.xlsx")

#%%


#%%
df5 = pd.read_excel('/Users/jha/Documents/fall2020/data/resistance_mechanism.xlsx', sheet_name='Sheet1')
list_mech=list(df5.itertuples(index=False, name=None))
mech_dict=dict(list_mech)
df5=df_amrast2
df5['resistance_mech']=df5['AMR_gene'].map(mech_dict)
df6 = pd.pivot_table(df5,index=["AMR_gene"],columns=["resistance_mech"],values=["Isolate"],aggfunc=lambda x: len(x.unique()), fill_value= 'None' )
df6.to_excel("df6.xlsx")

#%%


#%%

#df7 = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["Collection_year_range"],values=["Gene_frequency"],aggfunc=lambda x: len(x.unique()), fill_value=0 )
df7= pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["Collection_year_range"],values=["Isolate"],aggfunc='count', fill_value=0)
df7=df7.T
df7=df7.reset_index()
df7=df7.drop('level_0',axis=1)
df7=df7.T
df7=df7.reset_index()
df7.columns=df7.iloc[0]
df7=df7.drop(df7.index[0])
df7.rename(columns={ df7.columns[0]: "AMR_gene" }, inplace = True)
df7['total_tested_samples']=df7['AMR_gene'].map(genevc_dict)
#df7=df7.replace( np.nan,0)

df7.loc[:,"1970-79":"before 1970"] = df7.loc[:,"1970-79":"before 1970"].div(df7["total_tested_samples"], axis=0)# dividing by last row
df7=df7.set_index("AMR_gene")
df7=df7*100
df7=df7.round(2)
df7=df7.reset_index()
df7.to_excel("genedate.xlsx")

#%%

#%%
isoyear_dict = dict(zip(df_kleb.Isolate, df_kleb.cd_year))
df_amrast2['cd_year']=df_amrast2['Isolate'].map(isoyear_dict)
astyear_dict = dict(zip(appended_datata.Isolate, appended_datata.Collection_year_range))
df_amrast2['Collection_year_range']=df_amrast2['Isolate'].map(astyear_dict)
df_amrast2["Antimicrobial_class"].value_counts()
dfast=pd.pivot_table(df_amrast2,index=["Antimicrobial_class","Antimicrobial"],columns=["cd_year"],values=["Isolate"],aggfunc=lambda x: len(x.unique()), fill_value=0)
dfast=dfast.reset_index()
dfast['total_tested_samples']=dfast['Antimicrobial'].map(astvc_dict)
dfast=dfast.groupby(["Antimicrobial_class"]).sum()
dfast.to_excel("ASTbasic.xlsx")
#%%



#adding the resistance mechanism column to the appeneded datata table for antimicrobial analysis
#%%
df5 = pd.read_excel('/Users/jha/Documents/fall2020/data/resistance_mechanism.xlsx', sheet_name='Sheet1')
list_mech=list(df5.itertuples(index=False, name=None))
mech_dict=dict(list_mech)
dfcAM = pd.read_excel('/Users/jha/count_antimicrobial.xlsx', sheet_name='Sheet2')
list_countAM=list(dfcAM.itertuples(index=False, name=None))
countAM_dict=dict(list_countAM)

appended_datata['resistance_mech']=appended_datata['Antimicrobial'].map(mech_dict)

#%%

#%%

appended_datata['Antimicrobial_class']=appended_datata ['Antimicrobial'].map(family_dict)

#%%
#%%
ydf=pd.crosstab((df_kleb["Isolate"],df_kleb["AST_phenotypes"]),df_kleb["epi_host"])
ydf.to_excel("ydf.xlsx")
#%%

#%%

#df_am= (appended_datata.groupby(['AMR_am','epi_host']).sum())
#df_am= (appended_datata.groupby(['epi_host','AMR_am']).sum())
amtable = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["samplehost"],values=["Isolate"],aggfunc='count', fill_value=0)
amtable=amtable.reset_index()
amtable.columns=amtable.columns.droplevel(0)
amtable.rename(columns={ amtable.columns[0]: "Antimicrobial" }, inplace = True)
amtable['Total_isolate_tested']=amtable ['Antimicrobial'].map(countAM_dict)

amtable.loc[:,"Environment":"Meat/Meatproduct"] = amtable.loc[:,"Environment":"Meat/Meatproduct"].div(amtable["Total_isolate_tested"], axis=0)#divinding by last column
amtable=amtable.set_index("Antimicrobial")
amtable=amtable*100
amtable=amtable.round(2)
amtable=amtable.reset_index()

amtable['Antimicrobial_class']=amtable ['Antimicrobial'].map(family_dict)

#df_am.to_excel("amanalysis'.xlsx")
amtable.to_excel("amanalysis'.xlsx")
#%%

#%%

#df_am= (appended_datata.groupby(['AMR_am','epi_host']).sum())
#df_am= (appended_datata.groupby(['epi_host','AMR_am']).sum())
amtable = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["epi_host"],values=["Isolate"],aggfunc='count', fill_value=0)
amtable=amtable.reset_index()
amtable.columns=amtable.columns.droplevel(0)
amtable.rename(columns={ amtable.columns[0]: "Antimicrobial" }, inplace = True)
amtable["total isolates non-susceptible"]=amtable["Antimicrobial"].map(amnumber_dict)

amtable.loc[:,"Environment":] = amtable.loc[:,"Environment":].div(amtable["total isolates non-susceptible"], axis=0)#divinding by last column
amtable=amtable.set_index("Antimicrobial")
amtable=amtable*100
amtable=amtable.round(2)
#df_am.to_excel("amanalysis'.xlsx")
amtable.to_excel("amanalysis'''.xlsx")
#%%

#%%


amtable = pd.pivot_table(appended_data,index=["Antimicrobial"],columns=["epi_type"],values=["Isolate"],aggfunc='count', fill_value=0)
amtable=amtable.reset_index()
amtable.columns=amtable.columns.droplevel(0)
amtable.rename(columns={ amtable.columns[0]: "Antimicrobial" }, inplace = True)
amtable["total isolates non-susceptible"]=amtable["Antimicrobial"].map(amnumber_dict)

amtable.loc[:,"Clinical":"Food"] = amtable.loc[:,"Clinical":"Food"].div(amtable["total isolates non-susceptible"], axis=0)#divinding by last column
amtable=amtable.set_index("Antimicrobial")

amtable=amtable*100
amtable=amtable.round(2)
#df_am.to_excel("amanalysis'.xlsx")
amtable.to_excel("amanalysis''.xlsx")
#%%



#this makes the table for variation in amr genes over each year. DO NOT EDIT THIS !!
#%%

dfx = pd.pivot_table(df_amrast2,index=["AMR_gene"],columns=["Antimicrobial_class"],values=["Isolate"],aggfunc='count', fill_value=0)
dfx.columns = dfx.columns.droplevel(0)
dfx=dfx.reset_index()
dfx=dfx.T
dfx=dfx.reset_index()
dfx.columns=dfx.iloc[0]
dfx=dfx.drop(dfx.index[0])
#df=df.drop(df.index[6]) #only used for collection date to remove the before 1950 row
#df=df[::-1] #reverses the order of rows in a dataframe specially needed for AMR gene
#df.to_excel("geneyear.xlsx")

#%%


#%%

# libraries and data
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Make a data frame
#df has been made in the above snippet
 
# Initialize the figure
#plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('cividis')
p=45
# multiple line plot
num=0
for column in dfx.drop('AMR_gene', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(4,10, num)
 
#    # plot every groups, but discreet
#    for v in dfx.drop('AMR_gene', axis=1):
#        plt.plot( dfx[v],dfx['AMR_gene'], marker='', color='grey', linewidth=0.6, alpha=0.3)
# 
    # Plot the lineplot
    plt.plot( dfx[column],dfx['AMR_gene'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
    # Same limits for everybody!
    plt.xlim(0,500)
    plt.ylim(0,20)
 
    # Not ticks everywhere
    if num in range(32) :
        plt.tick_params(labelbottom=False,labelsize = 8)
    if num not in [1,11,21,31] :
        plt.tick_params(labelleft=False,labelsize = 8)
    if num == 31:
        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
 
    # Add title
    plt.title(column, loc='left', fontsize=9, fontweight=60, color='green',pad= 3)
 
# general title
plt.suptitle("Variation of AMR genes in antimicrobials", fontsize=10, fontweight=10, color='black', style='italic', y=0.95)
 
## Axis title
#plt.text(45, 45, 'Time')
#plt.text(45, 0, 'Frequency',  rotation='vertical')

#plt.setp(axs[-1, :], xlabel='x axis label')
#plt.setp(axs[:, 0], ylabel='y axis label')


plt.show()
#plt.savefig('foo.png')
#%%
