#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 09:23:13 2020

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

#this is for multiple microbes and their location in the same dataframe
#%%   
list_bugs=["Klebsiella_ast_us"]
list_gloc=[]
for x in list_bugs:
    print(x)
    sql=("select count(`#label`), collection_date, geo_loc_name from " +x+ " where collection_date like '%2015%' group by geo_loc_name")
    print(sql)
    numrows= cursor.execute("select count(`#label`), collection_date, geo_loc_name from " +x+ " where collection_date like '%2015%' group by geo_loc_name")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    rows =cursor.fetchall()#fetch all rows at once
    print(tabulate(rows, headers=["count","collection_date","geo_loc_name"], tablefmt='psql')) 
    df_sample = pd.DataFrame(rows) 
    df_sample.columns=["count","collection_date","geo_loc_name"]
    list_loc=[]
    list_loc=df_sample["geo_loc_name"].tolist()
    for index in list_loc:
        list_gloc.append(index)
list_gloc=list(set(list_gloc))
gloc_df=pd.DataFrame()
gloc_df["Location"]=list_gloc 
df_ec=pd.DataFrame()
df_ec["geo_loc"]= list_gloc   

    
#%%

#%%





##when you want to make is sophesticated like subplots
##%%
#ist_bugs=["Klebsiella_ast_us"]
#list_gloc=[]
#for x in list_bugs:
#    print(x)
#    sql=("select collection_date from " +x+ " group by collection_date")
#    print(sql)
#    numrows= cursor.execute("select collection_date from " +x+ " group by collection_date")
#    print("Selected %s rows" %numrows)
#    print("Selected %s rows " %cursor.rowcount)
#    rows =cursor.fetchall()#fetch all rows at once
#    print(tabulate(rows, headers=["count","collection_date","geo_loc_name"], tablefmt='psql')) 
#    df_year = pd.DataFrame(rows) 
#    df_year.columns=["collection_date"]
#try:
#    df_year=pd.to_datetime(df_year['collection_date'])
#    df_year= df_year['collection_date'].dt.year
#    
#except:
#    pass
#
##%%



#%%
list_bugs=["Klebsiella_ast_us"]
list_gloc=[]
for x in list_bugs:
    print(x)
    sql=("select geo_loc_name , count(`#label`)from " +x+ " where collection_date like '%2015%' group by geo_loc_name")
    print(sql)
    numrows= cursor.execute("select geo_loc_name , count(`#label`) from " +x+ " where collection_date like '%2015%' group by geo_loc_name")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    lst=list(cursor.fetchall())#fetch all rows at once
    lstd=dict(lst) 

    gloc_df[x] = gloc_df['Location'].map(lstd)





#%%




#%%
sql=("select state,City from latlon_states")
print(sql)
numrows= cursor.execute("select City,State from latlon_states")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
lst=list(cursor.fetchall())#fetch all rows at once 
lstd=dict(lst) 

#%%




#%%


list_gloc=gloc_df["Location"].tolist()
for row in list_gloc:
    if row is not None:
        
        loc=list_gloc.index(row)
        row1=row.split(":")[-1]
        list_gloc.remove(row)
        list_gloc.insert(loc,row1)
        print (row) 
for row in list_gloc:
    if row is not None:
        
        loc=list_gloc.index(row)
        row1=row.split(", ")[-1]
        list_gloc.remove(row)
        list_gloc.insert(loc,row1)
        print (row)
        
gloc_df["Location"]=list_gloc
gloc_df["Location"]=gloc_df['Location'].str.strip()
gloc_df["Location"]=gloc_df['Location'].str.strip()#needed twice because some have double spaces
gloc_df=gloc_df.replace(to_replace ="USA", value ="Ohio")
gloc_df=gloc_df.replace(to_replace ="OH", value ="Ohio")
gloc_df=gloc_df.replace(to_replace ="NY", value ="New York")
gloc_df=gloc_df.replace(to_replace ="Bethesa", value ="Maryland")
gloc_df=gloc_df.replace(to_replace ="MA", value ="Maryland")
gloc_df=gloc_df.replace(to_replace ="CA", value ="California")
gloc_df=gloc_df.replace(to_replace ="MN", value ="Minnesota")
gloc_df=gloc_df.replace(to_replace ="Boston", value ="Massachusetts")
gloc_df=gloc_df.replace(to_replace ="Boston, MA", value ="Massachusetts")

#gloc_df = gloc_df.groupby(['Location']).sum()
#gloc_df = gloc_df.reset_index()


gloc_df['state']=gloc_df['Location'].map(lstd) #the location needs to be mapped to state codes for klebsiella or other new drugs too
#%% 





#%%  
import plotly
import plotly.graph_objs as go  
#scl = [
#    [0.0, 'rgb(242,240,247)'],
#    [0.2, 'rgb(218,218,235)'],
#    [0.4, 'rgb(188,189,220)'],
#    [0.6, 'rgb(158,154,200)'],
#    [0.8, 'rgb(117,107,177)'],
#    [1.0, 'rgb(84,39,143)']
#]
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2015_us_ag_exports.csv')




gloc_df['text'] = gloc_df['Location'].astype(str) #+ '<br>' + \
        # + (gloc_df['bioproject_center']).astype(str) #+'<br>' +  ' Listeria ' + (gloc_df['listeria_percent']/100).astype(str) + '<br>' + \
        #'Campylobacter ' + (gloc_df['campylobacter_percent']/100).astype(str) +'<br>' + ' Ecoli ' + (gloc_df['ecoli_percent']/100).astype(str) 
data = [go.Choropleth(colorscale ='reds',autocolorscale = False,locations = gloc_df['state'],z = gloc_df['Klebsiella_ast_us'].astype(float),locationmode = 'USA-states',
                      text = gloc_df['text'],
                      marker = go.choropleth.Marker(line = go.choropleth.marker.Line(color="black",width = 2
                                      )),
    colorbar = go.choropleth.ColorBar(
        title = "number of samples")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Samples tested for Klebsiella to anitimicrobials in 2015 '),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)                                                  

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig,filename='state_bioproject2015_plot')

#fig.save(filename='state_plot')





#colorscale = scl,

#%%