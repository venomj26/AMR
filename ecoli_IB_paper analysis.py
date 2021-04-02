#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:13:22 2020
Epigenetic type anaysis of Ecoli

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



#%%
df_impgenes = pd.read_excel('/Users/jha/important_genes.xlsx', sheet_name='Sheet1')
list_impgenes=df_impgenes["AMR_Gene"].to_list()
#%%



#%%
try:
    appended_data=[]
    for k in list_col_name_ast:
        try:
            xdf_crosstab=pd.crosstab(df_kleb["Isolate"],df_kleb[k])
            xdf_crosstab["Antimicrobial"] = k
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
    
#%%
try:
    appended_data=[]
    for k in list_impgenes:
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
    
    
    
#for sample value count
#%%
    
df_samplevc=df_kleb["samplehost"].value_counts()
df_samplevc=df_samplevc.reset_index()
df_samplevc=df_samplevc.drop(df_samplevc.index[0])
df_samplevc.columns=["samplehost","total_Samples_tested"]
list_samplevc=list(df_samplevc.itertuples(index=False, name=None))
#list_family=list(df_family)
samplevc_dict=dict(list_samplevc)
#%%

#for sample value count
#%%
    
df_epivc=df_kleb["epi_host"].value_counts()
df_epivc=df_epivc.reset_index()
df_epivc.columns=["epi_host","total_samples_tested"]
list_epivc=list(df_epivc.itertuples(index=False, name=None))
#list_family=list(df_family)
epivc_dict=dict(list_epivc)
#%%

#for 41 genes
#%%
#appended_data= appended_data.drop(["DNE"], axis=1)
appended_data = appended_data.replace(np.nan, 0)      
appended_data["Gene_frequency"]= appended_data.sum(axis=1)
appended_data= appended_data.drop(["MISTRANSLATION","PARTIAL","POINT","PARTIAL_END_OF_CONTIG","COMPLETE"], axis=1)
#%%
#for all genes
#%%
appended_data= appended_data.drop(["DNE"], axis=1)
appended_data = appended_data.replace( np.nan, 0) 
appended_data["Gene_frequency"]= appended_data.sum(axis=1)
appended_data= appended_data.drop(["HMM","MISTRANSLATION","PARTIAL","POINT","PARTIAL_END_OF_CONTIG","COMPLETE"], axis=1)
#%%
    
#for all AST : this is required so that only resistant antimicrobials can be included
#%%
appended_data= appended_data.drop(["ND","SDD","S","DNE"], axis=1)
appended_data = appended_data.replace(np.nan, 0)  
appended_data["Non-Susceptible"]= appended_data.sum(axis=1)
appended_data= appended_data.drop(["I","R"], axis=1)

#%%
# for AST: this deletes all samples with no ast values
#%%
appended_data['Non-Susceptible'] = appended_data['Non-Susceptible'].replace(0, np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Non-Susceptible'])
#%%


#for df_AST: this deletes all samples with no ast values
#%%
df_ast=appended_data.reset_index()
df_ast=df_ast.drop(["Non-Susceptible"],axis=1)

df_ast['Antimicrobial'] = df_ast['Antimicrobial'].replace('amr_VALUE', np.nan)
df_ast = df_ast.dropna(axis=0, subset=['Antimicrobial'])
#df_ast= df_ast.groupby(['Isolate'])
#df_amr=df_amr.reset_index()
#df_amr.to_excel("amrcrosstab.xlsx")

#%%%
#this is being used to map the antimicrobial class to the df_ast dataframe so that the pivot table can be grouped by the antimicrobial family
#%%
df_family = pd.read_excel('/Users/jha/Documents/spring2020/ecoli_antimicrobial_class.xlsx', sheet_name='Sheet1')
df_family_mod= df_family
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_family=list(df_family.itertuples(index=False, name=None))
#list_family=list(df_family)
family_dict=dict(list_family)

#%%
#%%
df_ast['Antimicrobial_class']=df_ast ['Antimicrobial'].map(family_dict)
df_ast=df_ast.sort_values("Antimicrobial_class")
#col=[]
#col=df_astcol["AMR_Gene"].to_list()
#%%

#for both all purposes
#%%



appended_data = appended_data.reset_index()
isoyear_dict = dict(zip(df_kleb.Isolate, df_kleb.cd_year))
appended_data['CD_year']=appended_data['Isolate'].map(isoyear_dict)
isostate_dict = dict(zip(df_kleb.Isolate, df_kleb.state_loc))
appended_data['State']=appended_data['Isolate'].map(isostate_dict)
isoepi_dict = dict(zip(df_kleb.Isolate, df_kleb.epi_host))
#appended_data['epi_host']=appended_data['Isolate'].map(isoepi_dict)
isosamp_dict = dict(zip(df_kleb.Isolate, df_kleb.samplehost))
appended_data['samplehost']=appended_data['Isolate'].map(isosamp_dict)
isoepitype_dict = dict(zip(df_kleb.Isolate, df_kleb.epi_type))
#appended_data['epi_type']=appended_data['Isolate'].map(isoepitype_dict)
#appended_data['Antimicrobial_class']=appended_data ['Antimicrobial'].map(family_dict)
isoloc_dict = dict(zip(df_kleb.Isolate, df_kleb.state_loc))
appended_data['state_loc']=appended_data['Isolate'].map(isoloc_dict)
#appended_data= (appended_data.groupby(['Isolate','AMR_gene']).sum())

#cols=["PARTIAL","PARTIAL_END_OF_CONTIG","COMPLETE","Out of total samples"]
#appended_data =appended_data[cols]
# 

#%%


#%%
import numpy as np
#appended_data=appended_data.reset_index()
appended_data['CD_year'] = appended_data['CD_year'].replace('Missing', np.nan) 
#appended_data['cd_year'] = appended_data['cd_year'].replace('Out of total samples', np.nan)#use this line only for temporal analysis
appended_data = appended_data.dropna(axis=0, subset=['CD_year']) #this line only for temporal analysis
appended_data['CD_year'] = appended_data['CD_year'].astype('datetime64[ns]')
#%%
#%%

appended_data["cd_decade"]=((appended_data["CD_year"].dt.year//10)*10)
appended_data= appended_data.drop(["CD_year"], axis=1)


#%%
#%%
df_dec = pd.read_excel('/Users/jha/Documents/spring2020/data/ecoli_IB/decaderange.xlsx', sheet_name='Sheet1')
list_dec=list(df_dec.itertuples(index=False, name=None))
dec_dict=dict(list_dec)

appended_data['Collection_year_range']=appended_data['cd_decade'].map(dec_dict)
#%%
#%%
appended_data= appended_data.drop(["cd_decade"], axis=1)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('2020-29', np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Collection_year_range'])

#%%

#%%
appended_data_ref=appended_data
#%%

#%%
appended_data=appended_data_ref
#%%
#%%
appended_data_ref_ast=appended_data
#%%


#%%
appended_datata['samplehost'] = appended_datata['samplehost'].replace('unknown', np.nan)
appended_datata = appended_datata.dropna(axis=0, subset=['samplehost'])

#%%


#%%
appended_datata['epi_host'] = appended_datata['epi_host'].replace('unknown', np.nan)
appended_datata = appended_datata.dropna(axis=0, subset=['epi_host'])

#%%
#for only sample host
#%%

dfsh = pd.pivot_table(appended_datata,index=["samplehost"],columns=["AMR_gene"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
#dfsh.to_excel("samplehost.xlsx")


#%%

#%%

dfsh = pd.pivot_table(appended_datata,index=["epi_host"],columns=["AMR_gene"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "epi_host" }, inplace = True)
dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("epi_host")
#dfsh=dfsh*100
#%%
#%%
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
##dfsh=dfsh.T
dfsh.to_excel("epi_host1.xlsx")


#%%



#%%

dfsh = pd.pivot_table(appended_datata,index=["Collection_year_range"],columns=["epi_host"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
dfsh.to_excel("collectionyear_epihostt.xlsx")


#%%


#%%
#%%

dfsh = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["epi_host"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
dfsh.to_excel("antimicrobial_epi.xlsx")


#%%


#%%

dfsh = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
dfsh.to_excel("antimicrobial_sample.xlsx")


#%%
#%%

dfsh = pd.pivot_table(appended_datata,index=["Antimicrobial_class"],columns=["epi_host"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
dfsh.to_excel("antimicrobialclass_epi.xlsx")


#%%
#%%

dfsh = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["epi_host"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "Antimicrobial" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
dfsh['Antimicrobial_class']=dfsh ['Antimicrobial'].map(family_dict)
dfsh=dfsh.groupby(['Antimicrobial_class','Antimicrobial']).sum()
dfsh.to_excel("antimicrobialclass_epi.xlsx")


#%%
#%%

dfsh = pd.pivot_table(df_kleb,index=["epi_host"],columns=["state_loc"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "State" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()

dfsh.to_excel("location_samplehostt.xlsx")



#%%
#%%

dfsh = pd.pivot_table(appended_data,index=["samplehost"],columns=["state_loc"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "State" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()

dfsh.to_excel("location_samplehostt.xlsx")



#%%
#%%
#%%

dfsh = pd.pivot_table(appended_data,index=["AMR_gene"],columns=["State"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "AMR_gene" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()

#dfsh.to_excel("location_samplehostt.xlsx")



#%%

#%%
appended_data=xdf_crosstab

appended_data=appended_data.reset_index()
appended_data['CD_year']=appended_data['Isolate'].map(isoyear_dict)
isoloc_dict = dict(zip(df_kleb.Isolate, df_kleb.state_loc))
appended_data['state_loc']=appended_data['Isolate'].map(isoloc_dict)
#%%



#%%
import numpy as np
#appended_data=appended_data.reset_index()
appended_data['CD_year'] = appended_data['CD_year'].replace('Missing', np.nan) 
#appended_data['cd_year'] = appended_data['cd_year'].replace('Out of total samples', np.nan)#use this line only for temporal analysis
appended_data = appended_data.dropna(axis=0, subset=['CD_year']) #this line only for temporal analysis
appended_data['CD_year'] = appended_data['CD_year'].astype('datetime64[ns]')
#%%
#%%

appended_data["cd_decade"]=((appended_data["CD_year"].dt.year//10)*10)
appended_data= appended_data.drop(["CD_year"], axis=1)


#%%
#%%
df_dec = pd.read_excel('/Users/jha/Documents/spring2020/data/ecoli_IB/decaderange.xlsx', sheet_name='Sheet1')
list_dec=list(df_dec.itertuples(index=False, name=None))
dec_dict=dict(list_dec)

appended_data['Collection_year_range']=appended_data['cd_decade'].map(dec_dict)
#%%
#%%
appended_data= appended_data.drop(["cd_decade"], axis=1)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('2020-29', np.nan)
#appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('2000-09', np.nan)
#appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1990-99', np.nan)
#appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1980-89', np.nan)
#appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1970-79', np.nan)
#appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('before 1970', np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Collection_year_range'])

#%%

#%%

dfsh = pd.pivot_table(appended_data,index=["Collection_year_range","Food"],columns=["state_loc"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
#dfsh=dfsh.T
#dfsh=dfsh.reset_index()
#dfsh=dfsh.drop("level_0",axis=1)
#dfsh=dfsh.T
#dfsh=dfsh.reset_index()
#dfsh.columns=dfsh.iloc[0]
#dfsh=dfsh.drop(dfsh.index[0])
#dfsh.rename(columns={ dfsh.columns[0]: "State" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['epi_host'].map(epivc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()

dfsh.to_excel("location_samplehostt.xlsx")



#%%



#%%

dfsh = pd.pivot_table(appended_data,index=["AMR_gene","State"],columns=["Collection_year_range"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.drop("before 1970",axis=1)
dfsh.rename(columns={ dfsh.columns[0]: "AMR_gene" }, inplace = True)
#dfsh=dfsh.T
ax = dfsh.plot.barh()
#%%
#forstate_temporal
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
for column in dfsh.drop('AMR_gene', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(4,10, num)
 
#    # plot every groups, but discreet
#    for v in dfx.drop('AMR_gene', axis=1):
#        plt.plot( dfx[v],dfx['AMR_gene'], marker='', color='grey', linewidth=0.6, alpha=0.3)
# 
    # Plot the lineplot
    plt.plot( dfsh[column],dfsh['AMR_gene'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
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
    plt.title(column, loc='left', fontsize=9, fontweight=60, color='green',pad= -7)
 
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

#original
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
for column in dfsh.drop('AMR_gene', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(4,10, num)
 
#    # plot every groups, but discreet
#    for v in dfx.drop('AMR_gene', axis=1):
#        plt.plot( dfx[v],dfx['AMR_gene'], marker='', color='grey', linewidth=0.6, alpha=0.3)
# 
    # Plot the lineplot
    plt.plot( dfsh[column],dfsh['AMR_gene'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
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
    plt.title(column, loc='left', fontsize=9, fontweight=60, color='green',pad= -7)
 
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



#this makes the table for variation in amr genes over each year. DO NOT EDIT THIS !!
#%%

dfx = pd.pivot_table(appended_datata,index=["samplehost"],columns=["AMR_gene"],values=["Isolate"],aggfunc='count', fill_value=0)
dfx.columns = dfx.columns.droplevel(0)
dfx1=dfx.astype(float)# this is required to convert the data type of dfx from object to strin. correlation works on float datatype only
dfx1=dfx1.reset_index()
dfx1['samplehost'] = dfx1['samplehost'].replace('unknown', np.nan)#use this line only for temporal analysis
dfx1 = dfx1.dropna(axis=0, subset=['samplehost'])
dfx1=dfx1.set_index('samplehost')
#df=df.drop(df.index[6]) #only used for collection date to remove the before 1950 row
#df=df[::-1] #reverses the order of rows in a dataframe specially needed for AMR gene
#df.to_excel("geneyear.xlsx")

#%%


#correlation matrix
#%%
               
data = {'A': [45,37,42,35,39,22],
        'B': [38,31,26,28,33,22],
        'C': [10,15,17,21,12,22]
        }

df = pd.DataFrame(data,columns=['A','B','C'])
#dfx1=dfx.astype(float)# this is required to convert the data type of dfx from object to strin. correlation works on float datatype only
##dfx=dfx.drop("AMR_gene", axis=1)
corrMatrix=dfx1.corr(method= 'pearson')



#%%


#Cross correlation matrix
#%%

from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a mask for the upper triangle
mask = np.zeros_like(corrMatrix, dtype=np.bool)
mask[np.triu_indices_from(mask,1)] = True #the k=1 value in the triu function helps to retain the main diagonal in the correlation matrix
#mask = np.triu(np.zeros_like(corrMatrix, dtype=np.bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(200, 20, as_cmap=True) #not used intead spectral is being used

# Draw the heatmap with the mask and correct aspect ratio
ax=sns.heatmap(corrMatrix,mask= mask,  cmap='Spectral', vmax=1, vmin=-1,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#ax.invert_yaxis()
#ax.invert_xaxis()
plt.title("cross-correlation matrix of AMR genes of Ecoli grouped by samplehosts in the created AMR database")






#%%


#for only sample host
#%%

dfsh = pd.pivot_table(df_kleb,columns=["samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
#dfsh.to_excel("samplehost.xlsx")


#%%


#%%
from scipy.stats import chi2_contingency
chi=chi2_contingency(dfx1)
print(a,b,c)


#%%

#%%
import scipy.stats as ss
def cramers_v(confusion_matrix):
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))

#%%
    
#%%
   
matrix=cramers_v(dfx1)

#%%


#this makes the table for variation in amr genes over each year. DO NOT EDIT THIS !!
#%%

dfy = pd.pivot_table(appended_datata,index=["CD_year"],columns=["AMR_gene"],values=["Isolate"],aggfunc='count', fill_value=0)
dfy.columns = dfy.columns.droplevel(0)
dfy1=dfy.astype(float)# this is required to convert the data type of dfx from object to strin. correlation works on float datatype only
dfy1=dfy1.reset_index()
dfy1['CD_year'] = dfy1['CD_year'].replace('unknown', np.nan)#use this line only for temporal analysis
dfy1 = dfy1.dropna(axis=0, subset=['CD_year'])
dfy1=dfy1.set_index('CD_year')
#df=df.drop(df.index[6]) #only used for collection date to remove the before 1950 row
#df=df[::-1] #reverses the order of rows in a dataframe specially needed for AMR gene
#df.to_excel("geneyear.xlsx")

#%%

#%%

corrMatrix=dfy1.corr(method= 'pearson')
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a mask for the upper triangle
mask = np.zeros_like(corrMatrix, dtype=np.bool)
mask[np.triu_indices_from(mask,1)] = True #the k=1 value in the triu function helps to retain the main diagonal in the correlation matrix
#mask = np.triu(np.zeros_like(corrMatrix, dtype=np.bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(200, 20, as_cmap=True) #not used intead spectral is being used

# Draw the heatmap with the mask and correct aspect ratio
ax=sns.heatmap(corrMatrix,mask= mask,  cmap='Spectral', vmax=1, vmin=-1,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#ax.invert_yaxis()
#ax.invert_xaxis()
plt.title("cross-correlation matrix of AMR genes of Ecoli grouped by collection year in the created AMR database")



#%%

#%%

from scipy.stats import chi2_contingency
import numpy as np


data_encoded=dfx1

def cramers_V(var1,var2) :
  crosstab =np.array(pd.crosstab(var1,var2, rownames=None, colnames=None)) # Cross table building
  stat = chi2_contingency(crosstab)[0] # Keeping of the test statistic of the Chi2 test
  obs = np.sum(crosstab) # Number of observations
  mini = min(crosstab.shape)-1 # Take the minimum value between the columns and the rows of the cross table
  return (stat/(obs*mini))

rows=[]

for var1 in data_encoded:
  col = []
  for var2 in data_encoded :
    cramers =cramers_V(data_encoded[var1], data_encoded[var2]) # Cramer's V test
    col.append(round(cramers,2)) # Keeping of the rounded value of the Cramer's V  
  rows.append(col)
  
cramers_results = np.array(rows)
df = pd.DataFrame(cramers_results, columns = data_encoded.columns, index =data_encoded.columns)





#%%


#%%

import seaborn as sns
import matplotlib.pyplot as plt



mask = np.zeros_like(df, dtype=np.bool)
mask[np.triu_indices_from(mask,1)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))


with sns.axes_style("white"):
  ax = sns.heatmap(df, mask=mask,vmin=0., vmax=1,cmap='Spectral', square=True)

plt.show()



#%%

#%%
import pandas as pd
numrows= cursor.execute("select * from isolation_source_ecoli_IB group by samplehost;")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(rows)
bs=pd.DataFrame(rows)
bs.to_excel("dictionary_isolation source_exanple.xlsx")
#%%



#this is being used to map the antimicrobial resistance mechanism to the appended_data dataframe so that the pivot table can be grouped by the antimicrobial resistance mechanism
#%%
df_resmech = pd.read_excel('/Users/jha/Documents/fall2020/data/resistance_mechanism.xlsx', sheet_name='Sheet1')
df_resmech_mod= df_resmech
#df_family=df_family.drop(["Intrinsicly_resistant","Antimicrobial_class","Antimicrobial_mod"], axis=1)
list_resmech=list(df_resmech.itertuples(index=False, name=None))
#list_family=list(df_family)
resmech_dict=dict(list_resmech)


appended_data['res_mech']=appended_data['AMR_gene'].map(resmech_dict)

#%%

#resistance mechanism analysis
#%%

dfsh = pd.pivot_table(appended_data,index=["AMR_gene"],columns=["res_mech"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh.rename(columns={ dfsh.columns[0]: "samplehost" }, inplace = True)
#dfsh['Total_isolate_tested']=dfsh ['samplehost'].map(samplevc_dict)
#dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"] = dfsh.loc[:,"aac(3)-IId":"uhpT_E350Q"].div(dfsh["Total_isolate_tested"], axis=0)# dividing by last row
#dfsh=dfsh.set_index("samplehost")
#dfsh=dfsh*100
#dfsh=dfsh.round(2)
#dfsh=dfsh.reset_index()
#dfsh.to_excel("antimicrobial_sample.xlsx")


#%%


#this section is being used to remove the unknown values and also just use the most recent decade values for samplehost/loc
#%%



#this snippet is being used to delete all date ranges other than the last decade
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('2000-09', np.nan)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1990-99', np.nan)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1980-89', np.nan)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('1970-79', np.nan)
appended_data['Collection_year_range'] = appended_data['Collection_year_range'].replace('before 1970', np.nan)

appended_data = appended_data.dropna(axis=0, subset=['Collection_year_range'])
#%%

#%%

appended_data['samplehost'] = appended_data['samplehost'].replace('unknown', np.nan)
appended_data['state_loc'] = appended_data['state_loc'].replace('Unknown', np.nan)
appended_data = appended_data.dropna(axis=0, subset=['state_loc','samplehost'])

#%%



#%%



dfsh = pd.pivot_table(appended_data,index=["state_loc","samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)

dfsh=dfsh.reset_index()
#dfsh['AMR_gene'] = dfsh['AMR_gene'].replace('acrF', np.nan)
#dfsh['AMR_gene'] = dfsh['AMR_gene'].replace('mdtM', np.nan)
#dfsh['AMR_gene'] = dfsh['AMR_gene'].replace('blaEC', np.nan)
#dfsh = dfsh.dropna(axis=0)
dfsh["Total"]= dfsh.sum(axis=1) #adding a total column
dfsh1 = dfsh[dfsh['Total'] > 150] #subsetting the table dfsh1 from dfsh where total number of genes from each sample host is less than 150

#dfsh1.to_excel("location_samplehost_gene.xlsx")
#%%

#%%
dfsh1=dfsh1.drop("Total",axis=1)

#%%
#%%
dfsh1=dfsh1.T
dfsh1.columns=dfsh1.iloc[0]
dfsh1=dfsh1.drop(dfsh1.index[0])
dfsh1=dfsh1.reset_index()
dfsh1=dfsh1.drop("level_0",axis=1)
dfsh1=dfsh1.T
dfsh1.columns=dfsh1.iloc[0]
dfsh1=dfsh1.drop(dfsh1.index[0])
dfsh1.rename(columns={ dfsh1.columns[0]: "gene" }, inplace = True)
dfsh1=dfsh1.T
dfsh1=dfsh1.reset_index()
dfsh1=dfsh1.T
dfsh1=dfsh1.reset_index()
dfsh1.columns=dfsh1.iloc[0]
dfsh1=dfsh1.drop(dfsh1.index[0])
#dfsh1['AMR_g'] = dfsh1[['state_loc', 'gene'].agg('/'.join, axis=1)
#dfsh1=dfsh1.reset_index()

#%%

#%%
dfsh1["ag"]=dfsh1.samplehost.astype(str).str.cat(dfsh1.AMR_gene.astype(str), sep=',')
#dfsh1=dfsh1.drop(["state_loc","gene"],axis=1)
#%%



#%%
numrows= cursor.execute("Select name,latitude,longitude,abv from geo_states")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
st_df = pd.DataFrame(rows)
st_df.columns=["name","lat","lon","abv"]
#%%

#%%
LL_dict = dict(zip(st_df.name, st_df.lat))
dfsh1['Lat']=dfsh1['state_loc'].map(LL_dict)
LL_dict = dict(zip(st_df.name, st_df.lon))
dfsh1['Lon']=dfsh1['state_loc'].map(LL_dict)
abv_dict = dict(zip(st_df.name, st_df.abv))
dfsh1['state_abv']=dfsh1['state_loc'].map(abv_dict)

#%%
#%%
import plotly.express as px
df=dfsh1
df = df.sort_values('Isolate', ascending=False)
fig = px.scatter_geo(df, locationmode="USA-states",
                     locations="state_abv",
                     color="samplehost", # which column to use to set the color of markers
                     hover_name="state_loc", # column added to hover information
                     size="Isolate", # size of markers
                     projection="albers usa")
fig.show(renderer="browser")
fig.write_html("/Users/jha/Documents/fall2020/data/state_sh_2010_gene.html")
#%%
#plotly example file
#%%
import plotly.express as px
df_ex = px.data.gapminder().query("year == 2007")
fig = px.scatter_geo(df_ex, locations="iso_alpha",
                     color="continent", # which column to use to set the color of markers
                     hover_name="country", # column added to hover information
                     size="pop", # size of markers
                     projection="natural earth")
fig.show()
#%%

#%%
import plotly.graph_objects as go

import pandas as pd

df_ex = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
df_ex['text'] = df_ex['airport'] + '' + df_ex['city'] + ', ' + df_ex['state'] + '' + 'Arrivals: ' + df_ex['cnt'].astype(str)

fig = go.Figure(data=go.Scattergeo(
        lon = df_ex['long'],
        lat = df_ex['lat'],
        text = df_ex['text'],
        mode = 'markers',
        marker_color = df_ex['cnt'],
        ))

fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo_scope='usa',
    )
fig.show()

#%%
#%%
import plotly.graph_objects as go

import pandas as pd

df = dfsh1

fig = go.Figure(data=go.Scattergeo(
        lon = df['Lon'],
        lat = df['Lat'],
       # size=df['Total']/0.25,
        #text = df['text'],
        mode = 'markers',
        marker_color = df['Isolate'],
        ))

fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo_scope='usa',
    )
fig.show()

#%%


#state-2010-AST result-sh
#%%
dfash = pd.pivot_table(appended_data,index=["state_loc","samplehost","Antimicrobial_class"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfash=dfash.replace('None',0)
#%%

#%%
dfash=dfash.reset_index()
LL_dict = dict(zip(st_df.name, st_df.lat))
dfash['Lat']=dfash['state_loc'].map(LL_dict)
LL_dict = dict(zip(st_df.name, st_df.lon))
dfash['Lon']=dfash['state_loc'].map(LL_dict)
abv_dict = dict(zip(st_df.name, st_df.abv))
dfash['state_abv']=dfash['state_loc'].map(abv_dict)

#%%

#%%
import plotly.express as px
df=dfash
df = df.sort_values('Isolate', ascending=False)
fig = px.scatter_geo(df, locationmode="USA-states",
                     locations="state_abv",
                     color="samplehost", # which column to use to set the color of markers
                     hover_name="state_loc", # column added to hover information
                     size="Isolate", # size of markers
                     projection="albers usa")
fig.show(renderer="browser")
fig.write_html("/Users/jha/Documents/fall2020/data/state_sh_2010_ast.html")
#%%

#%%



#special case for analysis without the three most common genes
#%%

appended_data['AMR_gene'] = appended_data['AMR_gene'].replace('acrF', np.nan)
appended_data['AMR_gene'] = appended_data['AMR_gene'].replace('mdtM', np.nan)
appended_data['AMR_gene'] = appended_data['AMR_gene'].replace('blaEC', np.nan)
appended_data = appended_data.dropna(axis=0)
#%%
#%%



dfsh = pd.pivot_table(appended_data,index=["AMR_gene","state_loc"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)


dfsh["Total"]= dfsh.sum(axis=1)
dfsh1 = dfsh[dfsh['Total'] > 100]

#dfsh.to_excel("gene_loc_only.xlsx")
#%%


#%%
dfsh=dfsh.reset_index()
dfsh=dfsh.T
dfsh=dfsh.reset_index()
dfsh=dfsh.drop("level_0",axis=1)
dfsh=dfsh.T
dfsh.columns=dfsh.iloc[0]
dfsh=dfsh.drop(dfsh.index[0])
dfsh=dfsh.drop(["unknown"], axis=1)
#%%

#
#%%
#%%
dfsh1=dfsh1.reset_index()
LL_dict = dict(zip(st_df.name, st_df.lat))
dfsh1['Lat']=dfsh1['state_loc'].map(LL_dict)
LL_dict = dict(zip(st_df.name, st_df.lon))
dfsh1['Lon']=dfsh1['state_loc'].map(LL_dict)
abv_dict = dict(zip(st_df.name, st_df.abv))
dfsh1['state_abv']=dfsh1['state_loc'].map(abv_dict)

#%%
#%%
import plotly.express as px
df=dfsh1
df = df.sort_values('Isolate', ascending=False)
fig = px.scatter_geo(df, locationmode="USA-states",
                     locations="state_abv",
                     color="AMR_gene", # which column to use to set the color of markers
                     hover_name="state_loc", # column added to hover information
                     size="Isolate", # size of markers
                     projection="albers usa")
fig.show(renderer="browser")
fig.write_html("/Users/jha/Documents/fall2020/data/state_sh_2010_gene.html")
#%%

#for analysis without theunknown and lafayette
#%%

appended_data['state_loc'] = appended_data['state_loc'].replace('Unknown', np.nan)
appended_data['state_loc'] = appended_data['state_loc'].replace('Lafayette', np.nan)
#appended_data['AMR_gene'] = appended_data['AMR_gene'].replace('blaEC', np.nan)
appended_data = appended_data.dropna(axis=0)
#%%




#%%



dfgene = pd.pivot_table(appended_data,index=["state_loc","AMR_gene","samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfsh=dfsh.replace('None',0)

#dfgene.to_excel("gene_loc_host_only.xlsx")
dfgene = dfgene[dfgene['Isolate'] > 10] #(for testing purpose of all genes comment this line)


#%%

#%%
#%%
dfgene=dfgene.reset_index()
LL_dict = dict(zip(st_df.name, st_df.lat))
dfgene['Lat']=dfgene['state_loc'].map(LL_dict)
LL_dict = dict(zip(st_df.name, st_df.lon))
dfgene['Lon']=dfgene['state_loc'].map(LL_dict)
abv_dict = dict(zip(st_df.name, st_df.abv))
dfgene['state_abv']=dfgene['state_loc'].map(abv_dict)

#%%

#%%
import plotly.express as px
df=dfgene
df = df.sort_values('Isolate', ascending=False)
fig = px.scatter_geo(df, locationmode="USA-states",
                     locations="state_abv",
                     color="AMR_gene", # which column to use to set the color of markers
                     hover_name="AMR_gene", # column added to hover information
                     size="Isolate", # size of markers
                     projection="albers usa")
fig.show(renderer="browser")
fig.write_html("/Users/jha/Documents/fall2020/data/gene_loc_sh.html")
#%%

#do not change it copy and edit
#location and amr gene
#%%



dfgene = pd.pivot_table(appended_data,index=["state_loc"],columns=["AMR_gene"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfgene=dfgene.replace('None',0)

#dfgene.to_excel("gene_loc_host_only.xlsx")
dfgene = dfgene[dfgene['Isolate'] > 10] #(for testing purpose of all genes comment this line)


#%%
#do not change it copy and edit
#important table with info about the number of states from which amr gene was isolated and their corresponding sample host
#%%



dfgenex = pd.pivot_table(appended_data,index=["AMR_gene"],columns=["samplehost"],values=["state_loc"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfgenex=dfgenex.replace('None',0)

#dfgene.to_excel("gene_loc_host_only.xlsx")
#dfgenex = dfgenex[dfgenex['Isolate'] > 10] #(for testing purpose of all genes comment this line)


#%%

#do not change it copy and edit
#%%



dfgenez = pd.pivot_table(appended_data,index=["AMR_gene","state_loc","samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
dfgenez=dfgenez.replace('None',0)

#dfgene.to_excel("gene_loc_host_only.xlsx")
dfgenez = dfgenez[dfgenez['Isolate'] > 50] #(for testing purpose of all genes comment this line)


#%%

#this
#%%
appended_data=appended_data.reset_index()
isoast_dict = dict(zip(appended_data.Isolate, appended_data.Antimicrobial))
appended_data_ref['antimicrobial']=appended_data['Isolate'].map(isoast_dict)
#%%


#or this]
#%%
appended_data=appended_data.reset_index()
isoamr_dict = dict(zip(appended_data.Isolate, appended_data.AMR_gene))
appended_data_ref_ast['AMR_gene']=appended_data['Isolate'].map(isoamr_dict)


#%%

#for analysis without theunknown and lafayette
#%%

appended_data_ref_ast['state_loc'] = appended_data_ref_ast['state_loc'].replace('Unknown', np.nan)
appended_data_ref_ast['state_loc'] = appended_data_ref_ast['state_loc'].replace('Lafayette', np.nan)
#appended_data_ref_ast['AMR_gene'] = appended_data_ref_ast['AMR_gene'].replace('blaEC', np.nan)
appended_data_ref_ast = appended_data_ref_ast.dropna(axis=0)
#%%

#%%

dfrajini = pd.pivot_table(appended_data_ref_ast,index=["Antimicrobial","state_loc","samplehost"],columns=["AMR_gene","res_mech"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
appended_data['res_mech']=appended_data['AMR_gene'].map(resmech_dict)
dfrajini=dfrajini.replace('None',0)
dfrajini.to_excel("dfrajini.xlsx")
#%%


#%%
appended_data['res_mech']=appended_data['AMR_gene'].map(resmech_dict)
dfrajini = pd.pivot_table(appended_data,index=["res_mech","AMR_gene","CD_year"],columns=["state_loc","samplehost"],values=["Isolate"],aggfunc=pd.Series.nunique, fill_value= 'None' )
appended_data['res_mech']=appended_data['AMR_gene'].map(resmech_dict)
dfrajini=dfrajini.replace('None',0)
dfrajini.to_excel("dfrajini_resmech``.xlsx")
#%%




#%%
df_amc = pd.read_excel('/Users/jha/Documents/fall2020/data/Gene_AMC.xlsx', sheet_name='Sheet1')
list_amc=list(df_amc.itertuples(index=False, name=None))
amc_dict=dict(list_amc)
appended_data=appended_data.reset_index()

appended_data['AMC']=appended_data['AMR_gene'].map(amc_dict)

isoamc_dict = dict(zip(appended_data.Isolate, appended_data.AMC))

#%%

#%%
appended_data=appended_data.reset_index()
appended_data["AMC"]=appended_data["Isolate"].map(isoamc_dict)


#%%


#%%

dfAMC = pd.pivot_table(appended_data,index=["Isolate","Antimicrobial_class","Antimicrobial"],columns=["AMC"],values=["Non-Susceptible"],aggfunc='count', fill_value= 'None' )
#appended_data['res_mech']=appended_data['AMR_gene'].map(resmech_dict)
dfAMC=dfAMC.replace('None',0)
dfAMC.to_excel("dfAMC.xlsx")
#%%