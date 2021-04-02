#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:14:38 2019

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
    sql=("select geo_loc_name, count(geo_loc_name),bioproject_center  from " +x+ " group by geo_loc_name WHERE collection_date  ;")
    print(sql)
    numrows= cursor.execute("select geo_loc_name, count(geo_loc_name),bioproject_center  from " +x+ " group by geo_loc_name ;")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    rows =cursor.fetchall()#fetch all rows at once
    print(tabulate(rows, headers=["geo_loc_name","count"], tablefmt='psql')) 
    df_sample = pd.DataFrame(rows) 
    df_sample.columns=["geo_loc_name","count","bioproject_center"]
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

list_bugs=["Klebsiella_ast_us"]
list_gloc=[]
for x in list_bugs:
    print(x)
    sql=("select geo_loc_name, count(geo_loc_name) from " +x+ " group by geo_loc_name;")
    print(sql)
    numrows= cursor.execute("select geo_loc_name, count(geo_loc_name)  from " +x+ " group by geo_loc_name;")
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
gloc_df = gloc_df.groupby(['Location']).sum()
gloc_df = gloc_df.reset_index()


gloc_df['state']=gloc_df['Location'].map(lstd) #the location needs to be mapped to state codes for klebsiella or other new drugs too
#%% 

#%%

list_gloc=df_sample["geo_loc_name"].tolist()
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
        
df_sample["geo_loc_name"]=list_gloc
df_sample["geo_loc_name"]=df_sample['geo_loc_name'].str.strip()
df_sample["geo_loc_name"]=df_sample['geo_loc_name'].str.strip()#needed twice because some have double spaces
df_sample=df_sample.replace(to_replace ="USA", value ="Ohio")
df_sample=df_sample.replace(to_replace ="OH", value ="Ohio")
df_sample=df_sample.replace(to_replace ="NY", value ="New York")
df_sample=df_sample.replace(to_replace ="Bethesa", value ="Maryland")
df_sample=df_sample.replace(to_replace ="MA", value ="Maryland")
df_sample=df_sample.replace(to_replace ="CA", value ="California")
df_sample=df_sample.replace(to_replace ="MN", value ="Minnesota")
df_sample=df_sample.replace(to_replace ="Boston", value ="Massachusetts")

#%% 



#%%
df_sample.to_excel("/Users/jha/Documents/spring2020/bioproject.xlsx")
#%%

#%%

df_sample = pd.read_excel('/Users/jha/Documents/spring2020/bioproject.xlsx', sheet_name='Sheet1')
df_sample=df_sample.drop(["count"], axis=1)
list_sample=list(df_sample.itertuples(index=False, name=None))
#list_family=list(df_family)
sample_dict=dict(list_sample)
gloc_df['bioproject_center']=gloc_df['Location'].map(sample_dict)

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
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')




gloc_df['text'] = gloc_df['Location'].astype(str) + '<br>' + \
         + (gloc_df['bioproject_center']).astype(str) #+'<br>' +  ' Listeria ' + (gloc_df['listeria_percent']/100).astype(str) + '<br>' + \
        #'Campylobacter ' + (gloc_df['campylobacter_percent']/100).astype(str) +'<br>' + ' Ecoli ' + (gloc_df['ecoli_percent']/100).astype(str) 
data = [go.Choropleth(colorscale ='reds',autocolorscale = False,locations = gloc_df['state'],z = gloc_df['Klebsiella_ast_us'].astype(float),locationmode = 'USA-states',
                      text = gloc_df['text'],
                      marker = go.choropleth.Marker(line = go.choropleth.marker.Line(color="black",width = 2
                                      )),
    colorbar = go.choropleth.ColorBar(
        title = "number of samples ")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Samples tested for Klebsiella to anitimicrobials '),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)                                                  

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig,filename='state_bioproject_plot1')

#fig.save(filename='state_plot')





#colorscale = scl,

#%%
































































































#this one is for plotting more than one bug in the same map 
#%%  
gloc_df["total_samples"]= gloc_df.fillna(0)["salfinal"]#+ gloc_df.fillna(0)["Ecolifinal"]+gloc_df.fillna(0)["LSTRfinal"]+gloc_df.fillna(0)["CMPBast"]
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






#run this code snippet just once to create the final table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
gloc_df.to_sql(name='locationofbugs', con=cnx, if_exists = 'replace', index=False)
print("we are at line 244 in code")



#%%
#%%
numrows= cursor.execute("SELECT antibiotics FROM ECS ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows=cursor.fetchall()#fetch all rows at once
df=pd.DataFrame(rows)
list_drugs=df[0].tolist()
#%%
#getting the lat lon for the US states 
#%%

import pandas as pd              
file_path='/Users/jha/Documents/Fall2019/statelatlong.csv'
latlon_df = pd.read_csv(file_path)
latlon_df.head()       
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
latlon_df.to_sql(name='latlon_states', con=cnx, if_exists = 'replace', index=False)
print("your table is written in the database")

#%%


#before running this snippet initialize df_ec at the top
#%%

for drugs in list_drugs:
    print (drugs)
    try:
        sql=("select geo_loc_name, count(geo_loc_name) from Ecolifinal where"+drugs+ " = 'S' group by geo_loc_name;")
        #print(sql)
        numrows= cursor.execute("select geo_loc_name, count(geo_loc_name) from Ecolifinal where " + drugs + "= 'S' group by geo_loc_name;")
        print("Selected %s rows" %numrows)
        print("Selected %s rows " %cursor.rowcount)
        rows=(cursor.fetchall())#fetch all rows at once
    
        print(tabulate(rows, headers=['geo_loc','count'], tablefmt='psql'))
        lst=list(rows)#fetch all rows at once
        lstd=dict(lst) 
        print(lstd)
        
        df_ec[drugs] = df_ec['geo_loc'].map(lstd)
    except:
        pass




#%%
        
#%%
list_gloc=df_ec["geo_loc"].tolist()
for row in list_gloc:
    loc=list_gloc.index(row)
    row1=row.split(":")[-1]
    list_gloc.remove(row)
    list_gloc.insert(loc,row1)
#        row= row.split(":")[-1]
print ("the string has been split")
df_ec["geo_loc"]=list_gloc
df_ec["geo_loc"]=df_ec['geo_loc'].str.strip()
df_ec = df_ec.groupby('geo_loc').sum()
df_ec=df_ec.reset_index() 


#%%


#%%
location_list=["Latitude","Longitude"]
for item in location_list:
    sql=("select State, "+item+" from latlon_states;")
    numrows= cursor.execute("select State, "+item+" from latlon_states;")
    print("Selected %s rows" %numrows)
    print("Selected %s rows " %cursor.rowcount)
    rows=(cursor.fetchall())#fetch all rows at once
    
    print(tabulate(rows, headers=['geo_loc','l'], tablefmt='psql'))
    lst=list(rows)#fetch all rows at once
    lstd=dict(lst) 
#print(lstd)
    df_ec[item] = df_ec['geo_loc'].map(lstd)
#%%

# this is for streptomycin to geo _loc
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



df_ec["streptomycin"]=df_ec.fillna(0)["streptomycin"]
df_ec['text'] = df_ec['geo_loc'].astype(str) + '<br>' + \
        'streptomycin' + df_ec['streptomycin'].astype(str) 
data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = df_ec['geo_loc'],
    z = df_ec['streptomycin'].astype(float),
    locationmode = 'USA-states',
    text = df_ec['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(0,0,0)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "in integers")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'number of ecoli samples susceptible to streptomycin from 2015 to 2017 '
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


#for streptomycin colors dont signify anything
#%%
import plotly.graph_objects as go

import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
#df.head()
df_ec_sorted=df_ec.sort_values('streptomycin',ascending=False)
df_ec_sorted['text'] = df_ec_sorted['geo_loc'] +'<br>percentage'+(df_ec['streptomycin']).astype(str)+'%'
limits = [(0,10),(10,20),(20,30),(30,40),(40,54)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 5

fig = go.Figure()


for i in range(len(limits)):
    lim = limits[i]
    print(lim)
    df_sub = df_ec_sorted[lim[0]:lim[1]]
    df_sub.head()
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['Longitude'],
        lat = df_sub['Latitude'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['streptomycin']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))


fig.update_layout(
        title_text = 'resistant streptomycin',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        )
    )

fig.show()
plotly.offline.plot(fig) #creates the plot offline

#%%



#%%
import plotly.graph_objects as go

import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
#df.head()
#df_ecT= df_ec.T
#df_ecT=df_ecT.reset_index()
#df_ecT.columns=df_ecT.iloc[0]
#df_ecT=df_ecT.drop(df_ecT.index[0])
#df_ecT=df_ecT.reset_index()
#df_ecT=df_ecT.drop(["index"],axis=1)
df_ecT['text'] = df_ecT['geo_loc'] +'<br>percentage'+(df_ecT['MD']).astype(str)+'%'
limits = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9)]
colors = ["royalblue","crimson","lightseagreen","orange","darkgreen","chocolate","red","pink","darkviolet"]
cities = []
scale = 5

fig = go.Figure()


for i in range(len(limits)):
    lim = limits[i]
    print(lim)
    df_sub = df_ecT[lim[0]:lim[1]]
    df_sub.head()
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['Longitude'],
        lat = df_sub['Latitude'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['MD']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))


fig.update_layout(
        title_text = 'susceptibility in Maryland ',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        )
    )

fig.show()
plotly.offline.plot(fig) #creates the plot offline


#%%




#run this code snippet just once to create the final table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_ec.to_sql(name='location_ECS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 244 in code")



#%%












#%%
#list_bugs=["salfinal","Ecolifinal","LSTRfinal"]
#try:
#    for bugs in list_bugs:
#        print(bugs)
#        for drugs in list_drugs:
#            print(drugs)
#            sql=("select geo_loc_name, count(geo_loc_name) from " +bugs+ " where " +drugs+ " = 'S';")
#            print(sql)
#            numrows= cursor.execute("select geo_loc_name, count(geo_loc_name) from " +bugs+ " where " +drugs+ " = 'S';")
#            print("Selected %s rows" %numrows)
#            print("Selected %s rows " %cursor.rowcount)
#            rows=(cursor.fetchall())#fetch all rows at once
#    
#            print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))    
#            #df_map = pd.DataFrame(rows)
#except:
#    pass




#%%




# this is for the samples to geo_location    
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



