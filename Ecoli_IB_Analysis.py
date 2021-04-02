#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 22:38:24 2020

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
dfj = pd.read_excel('/Users/jha/isolate1.xlsx', sheet_name='Sheet1')

#%%

#%%
df_j= (dfj.groupby(['AMR_gene','CD_year','samplehost','State']).sum())
df_j=df_j.reset_index()
df_j['CD_year'] = df_j['CD_year'].replace('2020', np.nan)#removing all values from 2020
df_j= df_j.dropna(axis=0, subset=['CD_year'])
#%%



#%%

import plotly.express as px
fig = px.scatter(df_j, x="CD_year", y="AMR_gene",
	         size="Gene_frequency", color="samplehost",
                 hover_name="AMR_gene",size_max=120, range_x=[1960,2030])
fig.show(renderer="browser")
#px.show()

#%%



#%%

import plotly.express as px
fig = px.scatter(df_j, x="AMR_gene", y="CD_year",
	         size="Gene_frequency", color="samplehost",
                 hover_name="AMR_gene",size_max=160,range_y=[1960,2030])
fig.show(renderer="browser")
#fig.write_html("/Users/jha/Documents/summer2020/data_ecoli_IB/graphs/temporal.html")
#px.show()

#%%


#%%
df_jstate=df_j
df_jstate['State'] = df_j['State'].replace('Unknown', np.nan)
df_jstate['State'] = df_j['State'].replace('Lafayette', np.nan)
df_jstate= df_jstate.dropna(axis=0, subset=['State'])
import plotly.express as px
fig = px.scatter(df_jstate, x="State", y="CD_year",
	         size="Gene_frequency", color="AMR_gene",
                 hover_name="AMR_gene",size_max=50)
fig.show(renderer="browser")
fig.write_html("/Users/jha/Documents/summer2020/data_ecoli_IB/graphs/state.html")
#px.show()

#%%

#%%
df_jstate.to_excel("graphstate.xlsx")
df_j.to_excel("graphtemporal.xlsx")
#%%

#%%




#%%
numrows= cursor.execute("Select name,latitude,longitude from geo_states")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
st_df = pd.DataFrame(rows)
st_df.columns=["name","lat","lon"]
#%%

#%%
LL_dict = dict(zip(st_df.name, st_df.lat))
df_jstate['Lat']=df_jstate['State'].map(LL_dict)
LL_dict = dict(zip(st_df.name, st_df.lon))
df_jstate['Lon']=df_jstate['State'].map(LL_dict)

#%%

import plotly.graph_objects as go
fig = go.Figure(go.Densitymapbox(lat=df_jstate.Latitude, lon=df_jstate.Longitude, z=df_jstate.Gene_frequency,      
                                 radius=10))
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
#%%



"""
Descriptive analysis of ECOLI isolate browser data

"""



#get the data from the Ecoli_merged table to make the dataframe for unique Samplehost
#%%
import pandas as pd
numrows= cursor.execute("Select epi_type from EcoliIBisodatlocmerge;")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
is_df = pd.DataFrame(rows)
is_df.columns=["epi"]
dflist=is_df['epi'].value_counts(normalize=True).round(4) * 100
dflist.to_excel("epi.xlsx")
#%%
#get the data from the Ecoli_merged table to make the dataframe for unique Samplehost
#%%
import pandas as pd
numrows= cursor.execute("Select samplehost from EcoliIBisodatlocmerge;")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
is_df = pd.DataFrame(rows)
is_df.columns=["epi"]
dflist=is_df['epi'].value_counts(normalize=True).round(4) * 100
dflist.to_excel("samplehost.xlsx")
#%%



#for all genes
#%%
 #def crosstab_all(df_kleb,list_col_name):
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


#for 45 genes
#%%
 #def crosstab_all(df_kleb,list_col_name):
#for j in list_col_name_amr:
try:
    appended_data=[]
    for k in list_impgenes :
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
        #continue
    

#%%

#for 41 genes
#%%
#appended_data= appended_data.drop(["DNE"], axis=1)
appended_data = appended_data.replace( np.nan, 0)      
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
#for all AMR
#%%
appended_data= appended_data.drop(["ND","SDD","S","DNE"], axis=1)
appended_data['R'] = appended_data['R'].replace( np.nan, 0)
appended_data['I'] = appended_data['I'].replace( np.nan, 0)
appended_data["Non-Susceptible"]= appended_data.sum(axis=1)
appended_data= appended_data.drop(["I","R"], axis=1)
#%%


# for AMR
#%%
appended_data['Non-Susceptible'] = appended_data['Non-Susceptible'].replace(0, np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Non-Susceptible'])
appended_data['Antimicrobial'] = appended_data['Antimicrobial'].replace('amr_VALUE', np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Antimicrobial'])

#%%

#TO calculate the number of samples tested for each antimicrobial
#%%
appended_data['Antimicrobial'] = appended_data['Antimicrobial'].replace('amr_VALUE', np.nan)
appended_data = appended_data.dropna(axis=0, subset=['Antimicrobial'])
appended_data= appended_data.drop(["ND","SDD"], axis=1)
appended_data['R'] = appended_data['R'].replace( np.nan, 0)
appended_data['I'] = appended_data['I'].replace( np.nan, 0)
appended_data["Non-Susceptible"]= appended_data["R"]+appended_data["I"]
appended_data= appended_data.drop(["I","R","DNE"], axis=1)
appended_data= appended_data.reset_index()
appended_data['S'] = appended_data['S'].replace(np.nan, 0)
appended_data['Non-Susceptible'] = appended_data['Non-Susceptible'].replace(np.nan,0)
count_antimicrobial = pd.pivot_table(appended_data,index=["Antimicrobial"],columns=["S","Non-Susceptible"],values=["Isolate"],aggfunc='count', fill_value=0)
count_antimicrobial.reset_index()
count_antimicrobial.to_excel("count_antimicrobial.xlsx")
#%%

#for both all purposes
#%%



appended_data = appended_data.reset_index()
isoyear_dict = dict(zip(df_kleb.Isolate, df_kleb.cd_year))
appended_data['CD_year']=appended_data['Isolate'].map(isoyear_dict)
isostate_dict = dict(zip(df_kleb.Isolate, df_kleb.state_loc))
appended_data['State']=appended_data['Isolate'].map(isostate_dict)
isoepi_dict = dict(zip(df_kleb.Isolate, df_kleb.epi_host))
appended_data['epi_host']=appended_data['Isolate'].map(isoepi_dict)
isosamp_dict = dict(zip(df_kleb.Isolate, df_kleb.samplehost))
appended_data['samplehost']=appended_data['Isolate'].map(isosamp_dict)
isoepitype_dict = dict(zip(df_kleb.Isolate, df_kleb.epi_type))
appended_data['epi_type']=appended_data['Isolate'].map(isoepitype_dict)

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
#appended_data = appended_data.dropna(axis=0, subset=['CD_year'])
appended_data['CD_year'] = appended_data['CD_year'].astype('datetime64[ns]')
#%%
#%%

appended_data["cd_decade"]=((appended_data["CD_year"].dt.year//10)*10)
appended_data= appended_data.drop(["CD_year"], axis=1)#this line only for temporal analysis


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
appended_datata=appended_data
#%%

#%%
appended_datata['samplehost'] = appended_datata['samplehost'].replace('unknown', np.nan)
appended_datata = appended_datata.dropna(axis=0, subset=['samplehost'])

#%%


#%%
appended_datata['epi_host'] = appended_datata['epi_host'].replace('unknown', np.nan)
appended_datata = appended_datata.dropna(axis=0, subset=['epi_host'])

#%%


#%%
#appended_datata['AMR_gene'] = appended_datata['AMR_gene'].replace('VALUE', np.nan)
#appended_datata = appended_datata.dropna(axis=0, subset=['AMR_gene'])

#%%

#%%

appended_datata= (appended_datata.groupby(['Collection_year_range','AMR_gene']).sum())
#appended_datata['percent'] = appended_datata.groupby(level=0).transform(lambda x: (x*100 / x.sum()).round(2))
#dflist=appended_data['epi'].value_counts(normalize=True).round(4) * 100
appended_datata=appended_datata.unstack(level=-1)
#%%

#%%

table = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["epi_host","Collection_year_range"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)


#table=table.sort_index(axis='columns', level='samplehost')
#%%

#for amr
#%%

#table = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["epi_host","Collection_year_range"],values=["Non-Susceptible"],aggfunc=np.sum, fill_value=0)


#table=table.sort_index(axis='columns', level='samplehost')
#%%


#%%
appended_data=appended_data.reset_index()
appended_data=appended_data.groupby(['epi_host']).sum()

#%%
#%%
#table.to_excel("isolatetest.xlsx")
#table.plot(x='AMR_gene',y='epi_host',kind='bar')
import seaborn as sns

sns.barplot(x='AMR_gene', y='Gene_frequency', hue='epi_host', data=appended_datata)
#%%

#%%

#df_gene= (appended_datata.groupby(['AMR_gene','epi_host']).sum())
df_gene= (appended_datata.groupby(['epi_host','AMR_gene']).sum())
genetable = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["epi_host"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)
df_gene.to_excel("geneanalysis'.xlsx")

#%%
#%%
genetable = pd.pivot_table(appended_datata,columns=["AMR_gene"],values=["Isolate"],aggfunc='count', fill_value=0)
genetable=genetable.T
genetable=genetable.reset_index()
genenumber_list=list(genetable.itertuples(index=False, name=None))
genenumber_dict=dict(genenumber_list)

#%%
#%%

#df_gene= (appended_datata.groupby(['AMR_gene','epi_host']).sum())
#df_gene= (appended_datata.groupby(['epi_host','AMR_gene']).sum())
genetable = pd.pivot_table(appended_datata,index=["Antimicrobial"],columns=["samplehost"],values=["Isolate"],aggfunc='count', fill_value=0)
genetable=genetable.reset_index()
genetable.columns=genetable.columns.droplevel(0)
genetable.rename(columns={ genetable.columns[0]: "AMR_gene" }, inplace = True)
genetable["total isolates identified with gene"]=genetable["AMR_gene"].map(genenumber_dict)

genetable.loc[:,"Animalfood":"unknown"] = genetable.loc[:,"Animalfood":"unknown"].div(genetable["total isolates identified with gene"], axis=0)#divinding by last column

#df_gene.to_excel("geneanalysis'.xlsx")
genetable.to_excel("geneanalysis'.xlsx")
#%%

#%%

#df_gene= (appended_datata.groupby(['AMR_gene','epi_host']).sum())
#df_gene= (appended_datata.groupby(['epi_host','AMR_gene']).sum())
genetable = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["epi_host"],values=["Isolate"],aggfunc='count', fill_value=0)
genetable=genetable.reset_index()
genetable.columns=genetable.columns.droplevel(0)
genetable.rename(columns={ genetable.columns[0]: "AMR_gene" }, inplace = True)
genetable["total isolates identified with gene"]=genetable["AMR_gene"].map(genenumber_dict)

genetable.loc[:,"Animal":"unknown"] = genetable.loc[:,"Animal":"unknown"].div(genetable["total isolates identified with gene"], axis=0)#divinding by last column

#df_gene.to_excel("geneanalysis'.xlsx")
genetable.to_excel("geneanalysis'.xlsx")
#%%

#%%


genetable = pd.pivot_table(appended_data,index=["AMR_gene"],columns=["epi_type"],values=["Isolate"],aggfunc='count', fill_value=0)
genetable=genetable.reset_index()
genetable.columns=genetable.columns.droplevel(0)
genetable.rename(columns={ genetable.columns[0]: "AMR_gene" }, inplace = True)
genetable["total isolates identified with gene"]=genetable["AMR_gene"].map(genenumber_dict)

genetable.loc[:,"Clinical":"Food"] = genetable.loc[:,"Clinical":"Food"].div(genetable["total isolates identified with gene"], axis=0)#divinding by last column

#df_gene.to_excel("geneanalysis'.xlsx")
genetable.to_excel("geneanalysis'.xlsx")
#%%












"""
GRAPHS
"""
#this makes the table for variation in amr genes over each year. DO NOT EDIT THIS !!
#%%

df = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["Collection_year_range"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)
df.columns = df.columns.droplevel(0)
df=df.reset_index()
df=df.T
df=df.reset_index()
df.columns=df.iloc[0]
df=df.drop(df.index[0])
df=df.drop(df.index[6]) #only used for collection date to remove the before 1950 row
df=df[::-1] #reverses the order of rows in a dataframe specially needed for AMR gene
#df.to_excel("isolatetest.xlsx")

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
for column in df.drop('AMR_gene', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(9,5, num)
 
    # plot every groups, but discreet
    for v in df.drop('AMR_gene', axis=1):
        plt.plot( df[v],df['AMR_gene'], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot( df[column],df['AMR_gene'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
    # Same limits for everybody!
    plt.xlim(0,20000)
    plt.ylim(0,7)
 
    # Not ticks everywhere
    if num in range(42) :
        plt.tick_params(labelbottom=False,labelsize = 8)
    if num not in [1,6,11,16,21,26,31,36,41,46] :
        plt.tick_params(labelleft=False,labelsize = 8)
    if num == 41:
        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
 
    # Add title
    plt.title(column, loc='left', fontsize=8, fontweight=4, color='saddlebrown',pad= -6)
 
# general title
plt.suptitle("Variation of AMR genes from 1960 to 2019", fontsize=10, fontweight=10, color='black', style='italic', y=0.95)
 
## Axis title
plt.text(45, 45, 'Time')
plt.text(45, 0, 'Frequency',  rotation='vertical')

#plt.setp(axs[-1, :], xlabel='x axis label')
#plt.setp(axs[:, 0], ylabel='y axis label')


plt.show()
#plt.savefig('foo.png')
#%%


#%%

df1=pd.DataFrame({'x': range(1,11), 'y1': np.random.randn(10), 'y2': np.random.randn(10)+range(1,11), 'y3': np.random.randn(10)+range(11,21), 'y4': np.random.randn(10)+range(6,16), 'y5': np.random.randn(10)+range(4,14)+(0,0,0,0,0,0,0,-3,-8,-6), 'y6': np.random.randn(10)+range(2,12), 'y7': np.random.randn(10)+range(5,15), 'y8': np.random.randn(10)+range(4,14), 'y9': np.random.randn(10)+range(4,14) })


#%%    
    
#this is used to make the df for gene frequency over the years yearly comparison   
#%%

df = pd.pivot_table(appended_datata,index=["AMR_gene"],columns=["Collection_year_range"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)
df.columns = df.columns.droplevel(0)
df=df.reset_index()
df=df.drop(['before 1950'], axis = 1)  #only used for collection date to remove the before 1950 row

df=df[::-1] #reverses the order of rows in a dataframe specially needed for AMR gene

#%%



#%%

# libraries and data
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# Make a data frame
#df has been made in the above snippet
 
# Initialize the figure
#plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('cividis')
p=6
# multiple line plot
num=0
for column in df.drop('AMR_gene', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(1,6, num)
 
    # plot every groups, but discreet
    for v in df.drop('AMR_gene', axis=1):
        plt.plot( df[v],df['AMR_gene'], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot( df[column],df['AMR_gene'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
    # Same limits for everybody!
    plt.xlim(0,20000)
    plt.ylim(0,45)
 
    # Not ticks everywhere
#    if num in range(42) :
#        plt.tick_params(labelbottom=False,labelsize = 8)
    if num not in [1] :
        plt.tick_params(labelleft=False,labelsize = 8)
    if num == 41:
        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
 
    # Add title
    plt.title(column, loc='left', fontsize=8, fontweight=4, color='saddlebrown',pad= -6)
 
# general title
plt.suptitle("Variation of AMR genes from 1960 to 2019 /n  A comparison by years", fontsize=10, fontweight=10, color='black', style='italic', y=0.95)
 
## Axis title
plt.text(20, -5, 'Frequency')
#plt.text(-45, 15, 'Genes',  rotation='vertical')

#plt.setp(axs[-1, :], xlabel='x axis label')
#plt.setp(axs[:, 0], ylabel='y axis label')


plt.show()
#plt.savefig('foo.png')
#%%

#%%
#df=(appended_datata.groupby(['samplehost','Collection_year_range'], as_index=False).sum())
df = pd.pivot_table(appended_datata,index=["samplehost"],columns=["Collection_year_range"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)
df=df.reset_index()
df=df.T
df.to_excel("temp.xlsx")
df=df.reset_index()
df.columns=df.iloc[0]
df=df.drop(df.index[0])
df=df.drop('samplehost',axis=1)
df=df.drop('unknown',axis=1)
df.rename(columns={ df.columns[0]: "samplehost" }, inplace = True)

df['samplehost'] = df['samplehost'].replace('before 1950', np.nan)
df=df.dropna(axis=0, subset=['samplehost'])
#%%

#%%

#%%

# libraries and data
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# Make a data frame
#df has been made in the above snippet
 
# Initialize the figure
#plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('cividis')
p=6
# multiple line plot
num=0
for column in df.drop('samplehost', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(7,2, num)
 
    # plot every groups, but discreet
    for v in df.drop('samplehost', axis=1):
        plt.plot( df[v],df['samplehost'], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot( df[column],df['samplehost'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
    # Same limits for everybody!
    plt.xlim(0,5000)
    plt.ylim(0,6)
 
    # Not ticks everywhere
    if num in range(13) :
        plt.tick_params(labelbottom=False,labelsize = 8)
    if num not in [1,3,5,7,9,11,13] :
        plt.tick_params(labelleft=False,labelsize = 8)
    if num == 13:
        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
 
    # Add title
    plt.title(column, loc='left', fontsize=8, fontweight=10, color='saddlebrown',pad= -6)
 
# general title
plt.suptitle("Variation of samplehost from 1960 to 2019", fontsize=10, fontweight=20, color='black', style='italic', y=0.95)
 
## Axis title
plt.text(40, -5, 'Frequency')
#plt.text(-45, 15, 'Genes',  rotation='vertical')

#plt.setp(axs[-1, :], xlabel='x axis label')
#plt.setp(axs[:, 0], ylabel='y axis label')


plt.show()
#plt.savefig('foo.png')
#%%


#%%
#df=(appended_datata.groupby(['samplehost','Collection_year_range'], as_index=False).sum())
df = pd.pivot_table(appended_datata,index=["epi_host"],columns=["AMR_gene"],values=["Gene_frequency"],aggfunc=np.sum, fill_value=0)
df=df.reset_index()
df=df.T
df.to_excel("temp.xlsx")
df=df.reset_index()
df.columns=df.iloc[0]
df=df.drop(df.index[0])
df=df.drop('epi_host',axis=1)
#df=df.drop('unknown',axis=1)
df.rename(columns={ df.columns[0]: "epi_host" }, inplace = True)
cols= ["epi_host","Homosapiens","Animals","Environment","Food"]
df.columns=cols
df=df.T
df=df.reset_index()
df.columns=df.iloc[0]
df=df.drop(df.index[0])
df=df[::-1] #reverses the order of rows in a dataframe
#
#df['samplehost'] = df['samplehost'].replace('before 1950', np.nan)
#df=df.dropna(axis=0, subset=['samplehost'])
#%%


#%%

# libraries and data
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# Make a data frame
#df has been made in the above snippet
 
# Initialize the figure
#plt.style.use('seaborn-darkgrid')
 
# create a color palette
palette = plt.get_cmap('cividis')
p=6
# multiple line plot
num=0
for column in df.drop('epi_host', axis=1): #accesing each column name
    num+=1
    num1=num
    # Find the right spot on the plot
    plt.subplot(9,5, num)
 
    # plot every groups, but discreet
    for v in df.drop('epi_host', axis=1):
        plt.plot( df[v],df['epi_host'], marker='', color='grey', linewidth=0.6, alpha=0.3)
 
    # Plot the lineplot
    plt.plot( df[column],df['epi_host'], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
    
    # Same limits for everybody!
    plt.xlim(0,1500)
    plt.ylim(0,4)
 
    # Not ticks everywhere
#    if num in range(13) :
#        plt.tick_params(labelbottom=False,labelsize = 8)
#    if num not in [1] :
#        plt.tick_params(labelleft=False,labelsize = 8)
#    if num == 13:
#        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
    if num in range(42) :
        plt.tick_params(labelbottom=False,labelsize = 8)
    if num not in [1,6,11,16,21,26,31,36,41,46] :
        plt.tick_params(labelleft=False,labelsize = 8)
    if num == 41:
        plt.tick_params(labelbottom=True,labelsize = 8)#this extra line had to be added because at the 41st plot both the ticks were blocking the function of the other
 
    # Add title
    plt.title(column, loc='left', fontsize=8, fontweight=10, color='saddlebrown',pad= -6)
 
# general title
plt.suptitle("Variation of frequency of amr genes in one health epigenetic types", fontsize=10, fontweight=20, color='black', style='italic', y=0.95)
 
## Axis title
plt.text(40, -5, 'Frequency')
#plt.text(-45, 15, 'Genes',  rotation='vertical')

#plt.setp(axs[-1, :], xlabel='x axis label')
#plt.setp(axs[:, 0], ylabel='y axis label')


plt.show()
#plt.savefig('foo.png')



#%%




