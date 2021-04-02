#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:14:22 2019

@author: jha
"""
#%%
import csv
import mysql.connector as mariadb
#try:
amrdb= mariadb.connect(
    host="localhost",
    user="jhasneha",
    passwd="sukhoi@90",
    database ="myamr"
    )
cursor= amrdb.cursor(buffered=True)
cursor.execute("SELECT VERSION()")
    
    
#%%   

#changing the "#label" to label
#%%
import pandas
import numpy as np
import os
path= '/Users/jha/Documents/Summer2019/Candida_auris'
#for root, dirs, files in os.walk(path, topdown=False):
dirlist= os.listdir(path)

for name in dirlist:
    if 'PDG' in name:
        path_new=os.path.join(path,name)
        # print (path_new)
        dirlist1= os.listdir(path_new)
        for name in dirlist1:
            if name.endswith (".tsv") and 'amr' in name:
                pathnew1=os.path.join(path_new,name)
                #pathnew11= os.path.join(pathnew1,)
                print(pathnew1)
                df = pandas.read_csv(pathnew1, sep='\t')
                #df.head()
                #df=df.dropna()
                #df= df.rename(columns=({'#label':'label'}))
                #df= df.replace('NULL', np.nan)
                df.columns=["label","HHS_region","LibraryLayout","PFGE_PrimaryEnzyme_pattern","PFGE_SecondaryEnzyme_pattern","Platform	Run	asm_acc	asm_level","asm_stats_contig_n50	","asm_stats_length_bp","	asm_stats_n_contig","assembly_method	attribute_package","bioproject_acc","bioproject_center","biosample_acc","collected_by","collection_date","fullasm_id","geo_loc_name","host",	"host_disease","isolation_source","lat_lon",	"outbreak","sample_name","scientific_name","serovar","species_taxid","sra_center	","sra_release_date","strain	","target_acc","target_creation_date","tax-id","wgs_acc_prefix","wgs_master_acc","minsame","mindiff","number_drugs_resistant","number_drugs_intermediate","number_drugs_susceptible","number_drugs_tested","number_amr_genes","AST_phenotypes","AMR_genotypes","FDA_lab_id","epi_type"]
                print (columns)
        
                with open(pathnew1, "w") as f:
                    df.to_csv(pathnew1, index= False, sep="\t" )
#                    
#
#            
           






#%%







   
#%% 
try:                 
    with open('/Users/jha/Documents/Summer2019/Salmonella2/PDG000000002.1080/PDG000000002.1080.amr.metadata.tsv .csv', newline='') as csvfile:
        amr_data = csv.reader(csvfile)  
        table_name = 'Salmonella'
        for row, line in enumerate (amr_data):
            if row == 0 :
                #print("The outer loop is printing the heading at line 92", line)
                #print("The row number for enumerate header at line 93",row)
                #print("printing each header element at line 94", line)
                header_list = list(line)
                #header_string = ',' .join(header_list)
                header_string = '"{0}"'.format('", "'.join(header_list))
                print("string is ", header_string)
                
            else:
                #print("The outer loop is printing the table rows at line 100", line)
                #print("The row number for enumerate data at line 101",row)
                #print("printing each header element", line)
                try:
                    table_list = list(line)
                #table_string = ',' .join(table_list)
                    table_string = '"{0}"'.format('", "'.join(table_list))
                #print("string is ", table_string)
                
                #sql_insert=("INSERT INTO Ecoli (%s) VALUES (%s)",(header_string,table_string))
                #sql_insert=("INSERT INTO Salmonella1 ({header_string}) VALUES ({table_string})")
                #print(f"INSERT INTO Salmonella1 (%s) VALUES (%s)")
                #print(f"INSERT INTO Ecoli ({header_string}) VALUES ({table_string})" + "\n")
                    sql_insert = 'INSERT INTO ' + table_name + '( ' + ','.join(header_list) + "\n"+ ') VALUES (' + ','.join(map('"{0}"'.format, table_list))+ "\n"+')'
                    print(sql_insert)
                    cursor.execute(sql_insert)
                    print("one line was written")
                
                #amrdb.commit()
                #breakcollection_date
                #cursor.close() 
                #cursor.execute(sql_insert,[header_string], [table_string])
                #print("query looks like", cursor.execute)

                except:
                    print("column mismatch error")
                    #continue
                    
                
#amrdb.commit()           
                #amrdb.close()              
                
                
                
                
#                for header in index_in_header:
#                    str = ','.join(header)
#                    print ("the header is",str)
#                    break
                
#            header =0
#            for index_in_row in row:
#                print ("Printing one row",index_in_row)
#                
                #if index ==0:
                    #print (row[index])
                #if colname == 0:
                    
            
        

except mariadb.Error as err:
    print("something went wrong :{}".format(err))
    pass


#%%
                
                
#%%

cursor = amrdb.cursor(buffered=True)
filename = "/Users/jha/Documents/Summer2019/Ecoli2/PDG000000004.854/PDG000000004.854.amr.metadata.tsv"
cursor.execute("""LOAD DATA LOCAL INFILE %s
               INTO TABLE Salmonella1 
               FIELDS TERMINATED BY ',' 
               ENCLOSED BY '\"' 
               LINES TERMINATED BY '\n' 
               IGNORE 1 ROWS;""" ,filename)

amrdb.commit()
#%%                
                
#%%                
cursor.execute("""INSERT INTO Salmonella(
             `#label`  ,
             HHS_region   ,
             LibraryLayout   ,
             PFGE_PrimaryEnzyme_pattern   , 
             PFGE_SecondaryEnzyme_pattern   ,
             Platform   ,    
             Run   ,    
             asm_acc   ,    
             asm_level   ,    
             asm_stats_contig_n50   , 
             asm_stats_length_bp   ,  
             asm_stats_n_contig   ,   
             assembly_method   ,    
             attribute_package   ,    
             bioproject_acc   ,    
             bioproject_center   ,    
             biosample_acc   ,    
             collected_by   ,    
             collection_date   ,    
             fullasm_id   ,    
             geo_loc_name   ,    
             host   ,    
             host_disease   ,    
             isolation_source   ,    
             lat_lon   ,    
             outbreak   ,    
             sample_name   ,    
             scientific_name   ,    
             serovar   ,    
             species_taxid   ,    
             sra_center   ,    
             sra_release_date   ,
             strain   ,    
             target_acc   ,    
             target_creation_date   ,    
             `tax-id`   ,    
             wgs_acc_prefix   ,    
             wgs_master_acc   ,    
             minsame   ,    
             mindiff   ,
             number_drugs_resistant   ,    
             number_drugs_intermediate   ,    
             number_drugs_susceptible   ,    
             number_drugs_tested   ,    
             number_amr_genes   ,
             AST_phenotypes,    
             AMR_genotypes )
            VALUES("%s" , "%s", "%s","%s" , 
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" , 
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" , 
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" , 
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" ,
                   "%s", "%s","%s" , "%s")""",
                   row)
#close the connection to the database.
mydb.commit()
cursor.close()
print ("Done")
#%%