# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import pymysql
db = pymysql.connect("localhost","root","Sukhoi@90","myamr")
cursor =db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Connected") 


#%%

#%%
#
# Create table as per requirement
sql = """CREATE TABLE IF NOT EXISTS Klebsiella(
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
   `#label` BLOB,
   `FDA_lab_id` BLOB,
   `HHS_region` BLOB,   
   `LibraryLayout` BLOB,   
   `PFGE_PrimaryEnzyme_pattern` BLOB,    
   `PFGE_SecondaryEnzyme_pattern` BLOB,  
   `Platform`  BLOB,  
   `Run`  BLOB,  
   `asm_acc` BLOB,   
   `asm_level` BLOB,   
   `asm_stats_contig_n50` BLOB,   
   `asm_stats_length_bp` BLOB,   
   `asm_stats_n_contig` VARCHAR(10) DEFAULT NULL,  
   `assembly_method`   VARCHAR(10) DEFAULT NULL, 
   `attribute_package`  VARCHAR(10) DEFAULT NULL,  
   `bioproject_acc`    VARCHAR(10) DEFAULT NULL,
   `bioproject_center` VARCHAR(10) DEFAULT NULL,   
   `biosample_acc`   VARCHAR(10) DEFAULT NULL, 
   `collected_by`   VARCHAR(10) DEFAULT NULL, 
   `collection_date` VARCHAR(10) DEFAULT NULL,
   `epi_type` VARCHAR(10) DEFAULT NULL,
   `fullasm_id`  VARCHAR(10) DEFAULT NULL,  
   `geo_loc_name` VARCHAR(10) DEFAULT NULL,   
   `host` VARCHAR(10) DEFAULT NULL,  
   `host_disease` VARCHAR(10) DEFAULT NULL,    
   `isolation_source` LONGTEXT DEFAULT NULL,    
   `lat_lon` VARCHAR(10) DEFAULT NULL,    
   `outbreak` VARCHAR(10) DEFAULT NULL,  
   `sample_name` VARCHAR(10) DEFAULT NULL,    
   `scientific_name` VARCHAR(10) DEFAULT NULL,    
   `serovar` VARCHAR(10) DEFAULT NULL,    
   `species_taxid` VARCHAR(10) DEFAULT NULL,    
   `sra_center` VARCHAR(10) DEFAULT NULL,    
   `sra_release_date` VARCHAR(10) DEFAULT NULL,
   `strain` VARCHAR(10) DEFAULT NULL,    
   `target_acc` VARCHAR(10) DEFAULT NULL,    
   `target_creation_date` VARCHAR(10) DEFAULT NULL,    
   `tax-id` VARCHAR(10) DEFAULT NULL,    
   `wgs_acc_prefix` VARCHAR(10) DEFAULT NULL,    
   `wgs_master_acc` VARCHAR(10) DEFAULT NULL,    
   `minsame` VARCHAR(10) DEFAULT NULL,    
   `mindiff` VARCHAR(10) DEFAULT NULL,    
   `number_drugs_resistant` VARCHAR(10) DEFAULT NULL,    
   `number_drugs_intermediate` VARCHAR(10) DEFAULT NULL,    
   `number_drugs_susceptible` VARCHAR(10) DEFAULT NULL,   
   `number_drugs_tested` VARCHAR(10) DEFAULT NULL,    
   `number_amr_genes` VARCHAR(10) DEFAULT NULL,    
   `AST_phenotypes` LONGTEXT DEFAULT NULL,   
   `AMR_genotypes` LONGTEXT DEFAULT NULL)"""

cursor.execute(sql)


#%%

#%%

with open('/Users/jha/Documents/Summer2019/Neisseria/PDG000000032.53/PDG000000032.53.amr.metadata.tsv .csv', newline='') as csvfile:
        amr_data = csv.reader(csvfile) 
        table_name = 'nessy'
        for row, line in enumerate (amr_data):
            if row == 0 :
                #print("The outer loop is printing the heading at line 92", line)
                #print("The row number for enumerate header at line 93",row)
                #print("printing each header element at line 94", line)
                header_list = list(line)
                #header_string = ',' .join(header_list)
                header_string = '"{0}"'.format('", "'.join(header_list))
                print("string is ", header_string)
                sql_insert = 'CREATE TABLE IF NOT EXISTS ' + table_name + '( ' + '` VARCHAR (10) NOT NULL,`'.join(header_list) + "\n"+ '` VARCHAR (255) NOT NULL) '
                print(sql_insert)
                cursor.execute(sql_insert)
                print("one line was written")









#%%










#%%


esql = """LOAD DATA INFILE '/Users/jha/Documents/Summer2019/Salmonella2/PDG000000002.1637/PDG000000002.1637.amr.metadata.tsv'
                      INTO TABLE Salmonella
                      FIELDS TERMINATED BY '\t' 
                      ENCLOSED BY '"'
                      LINES TERMINATED BY '\n'
                      IGNORE 1 ROWS;"""
cursor.execute(esql)
db.commit()
print("The table has been uploaded")
#%%



#%%
#import glob 
##import pandas as pd
#path = r'/Users/jha/Documents/Salmonella'
##df = pd.concat([pd.read_csv(f, encoding='latin1') for f in glob.glob('data*.csv'), ignore_index=True])
#file_name = glob.glob(path +"/*")
#for name in file_name:
#    file1= glob.glob(name + "/*.csv")
#    #print("file is",file1)
#    for f in file1: 
#        if "amr" in f.lower():
#            print ("file_name",f)
#            esql = """LOAD DATA INFILE 'f'
#                      INTO TABLE Salmonella 
#                      FIELDS TERMINATED BY ',' 
#                      ENCLOSED BY '"'
#                      LINES TERMINATED BY '\n'
#                      IGNORE 1 ROWS;"""
#            cursor.execute(esql)

#cursor.commit()
print("DATABASE version : %s" % data)
db.close()





#%%
import pymysql
db = pymysql.connect("localhost","root","Sukhoi@90","myamr")
cursor =db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Connected") 


#%%

#%%
#
# Create table as per requirement
sql = """CREATE TABLE IF NOT EXISTS Ecoli_IB(
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
   `#label` VARCHAR (255) DEFAULT NULL,
   `FDA_lab_id` VARCHAR (255) DEFAULT NULL,
   `HHS_region` VARCHAR (255) DEFAULT NULL,   
   `LibraryLayout` VARCHAR (255) DEFAULT NULL,   
   `PFGE_PrimaryEnzyme_pattern` VARCHAR (255) DEFAULT NULL,    
   `PFGE_SecondaryEnzyme_pattern` VARCHAR (255) DEFAULT NULL,  
   `Platform`  VARCHAR (255) DEFAULT NULL,  
   `Run`  VARCHAR (255) DEFAULT NULL,  
   `asm_acc` VARCHAR (255) DEFAULT NULL,   
   `asm_level` VARCHAR (255) DEFAULT NULL,   
   `asm_stats_contig_n50` VARCHAR (255) DEFAULT NULL,   
   `asm_stats_length_bp` VARCHAR (255) DEFAULT NULL,   
   `asm_stats_n_contig` VARCHAR(255) DEFAULT NULL,  
   `assembly_method`   VARCHAR(255) DEFAULT NULL, 
   `attribute_package`  VARCHAR(255) DEFAULT NULL,  
   `bioproject_acc`    VARCHAR(255) DEFAULT NULL,
   `bioproject_center` VARCHAR(255) DEFAULT NULL,   
   `biosample_acc`   VARCHAR(255) DEFAULT NULL, 
   `collected_by`   VARCHAR(255) DEFAULT NULL, 
   `collection_date` VARCHAR(255) DEFAULT NULL,
   `epi_type` VARCHAR(255) DEFAULT NULL,
   `fullasm_id`  VARCHAR(255) DEFAULT NULL,  
   `geo_loc_name` VARCHAR(255) DEFAULT NULL,   
   `host` VARCHAR(255) DEFAULT NULL,  
   `host_disease` VARCHAR(255) DEFAULT NULL,    
   `isolation_source` LONGTEXT DEFAULT NULL,    
   `lat_lon` VARCHAR(255) DEFAULT NULL,    
   `outbreak` VARCHAR(255) DEFAULT NULL,  
   `sample_name` VARCHAR(255) DEFAULT NULL,    
   `scientific_name` VARCHAR(255) DEFAULT NULL,    
   `serovar` VARCHAR(255) DEFAULT NULL,    
   `species_taxid` VARCHAR(255) DEFAULT NULL,    
   `sra_center` VARCHAR(255) DEFAULT NULL,    
   `sra_release_date` VARCHAR(255) DEFAULT NULL,
   `strain` VARCHAR(255) DEFAULT NULL,    
   `target_acc` VARCHAR(255) DEFAULT NULL,    
   `target_creation_date` VARCHAR(255) DEFAULT NULL,    
   `tax-id` VARCHAR(255) DEFAULT NULL,    
   `wgs_acc_prefix` VARCHAR(255) DEFAULT NULL,    
   `wgs_master_acc` VARCHAR(255) DEFAULT NULL,    
   `minsame` VARCHAR(255) DEFAULT NULL,    
   `mindiff` VARCHAR(255) DEFAULT NULL,    
   `number_drugs_resistant` VARCHAR(255) DEFAULT NULL,    
   `number_drugs_intermediate` VARCHAR(255) DEFAULT NULL,    
   `number_drugs_susceptible` VARCHAR(255) DEFAULT NULL,   
   `number_drugs_tested` VARCHAR(255) DEFAULT NULL,    
   `number_amr_genes` VARCHAR(255) DEFAULT NULL,    
   `AST_phenotypes` LONGTEXT DEFAULT NULL,   
   `AMR_genotypes` LONGTEXT DEFAULT NULL,
   `number_stress_genes` LONGTEXT DEFAULT NULL,
   `stress_genotypes` LONGTEXT DEFAULT NULL,
   `number_virulence_genes` LONGTEXT DEFAULT NULL,
   `virulence_genotype` LONGTEXT DEFAULT NULL,
   `amrfinder_version` LONGTEXT DEFAULT NULL,
   `refgene_db_version` LONGTEXT DEFAULT NULL,
   `amrfinder_analysis_type` LONGTEXT DEFAULT NULL,
   `amrfinder_applied` LONGTEXT DEFAULT NULL)"""

cursor.execute(sql)


#%%



#%%
sql ="""CREATE TABLE IF NOT EXISTS EcoliIB(
     `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Organism_Group` VARCHAR (255) DEFAULT NULL,
    `Strain` VARCHAR (255) DEFAULT NULL,
    `Serovar` VARCHAR (255) DEFAULT NULL,
    `Isolate` VARCHAR (255) DEFAULT NULL,
    `Create_Date` VARCHAR (255) DEFAULT NULL,	
    `Location` VARCHAR (255) DEFAULT NULL,
    `Isolation_Source` VARCHAR (255) DEFAULT NULL,
    `Isolation_type` VARCHAR (255) DEFAULT NULL,	
    `Host` VARCHAR (255) DEFAULT NULL,
    `SNP_cluster` VARCHAR (255) DEFAULT NULL, 
    `Min-same` VARCHAR (255) DEFAULT NULL,
    `Min-diff` VARCHAR (255) DEFAULT NULL,
    `BioSample` VARCHAR (255) DEFAULT NULL,	
    `Assembly` VARCHAR (255) DEFAULT NULL,
    `AMR_genotypes` VARCHAR (255) DEFAULT NULL,	
    `K-mer_group` VARCHAR (255) DEFAULT NULL,
    `Scientific_name` VARCHAR (255) DEFAULT NULL,
    `AST_phenotypes` VARCHAR (255) DEFAULT NULL,
    `Virulence_genotypes` VARCHAR (255) DEFAULT NULL,
    `Stress_genotypes` VARCHAR (255) DEFAULT NULL,
    `AMRFinderPlus_version` VARCHAR (255) DEFAULT NULL,
    `PD_Ref_Gene_Catalog_version` VARCHAR (255) DEFAULT NULL,
    `AMRFinderPlus_analysis_type` VARCHAR (255) DEFAULT NULL,	
    `BioProject` VARCHAR (255) DEFAULT NULL,
    `Collected_by` VARCHAR (255) DEFAULT NULL,	
    `Collection_Date` VARCHAR (255) DEFAULT NULL,	
    `Lat/Lon` VARCHAR (255) DEFAULT NULL,
    `N50` VARCHAR (255) DEFAULT NULL,
    `Length` VARCHAR (255) DEFAULT NULL,	
    `Contigs` VARCHAR (255) DEFAULT NULL,
    `Library_Layout` VARCHAR (255) DEFAULT NULL,	
    `Platform` VARCHAR (255) DEFAULT NULL,	
    `Run` VARCHAR (255) DEFAULT NULL,
    `SRA_Center` VARCHAR (255) DEFAULT NULL,	
    `SRA_Release_Date` VARCHAR (255) DEFAULT NULL,	
    `Species_TaxID` VARCHAR (255) DEFAULT NULL,	
    `Outbreak` VARCHAR (255) DEFAULT NULL,		
    `Host_Disease` VARCHAR (255) DEFAULT NULL,	
    `Level` VARCHAR (255) DEFAULT NULL,	
    `Method` VARCHAR (255) DEFAULT NULL,	
    `PFGE_Primary_Enzyme_Pattern` VARCHAR (255) DEFAULT NULL,
    `PFGE_Secondary_Enzyme_Pattern` VARCHAR (255) DEFAULT NULL,	
    `TaxID` VARCHAR (255) DEFAULT NULL,
    `WGS_Prefix` VARCHAR (255) DEFAULT NULL,
    `WGS_Accession` VARCHAR (255) DEFAULT NULL)"""	
cursor.execute(sql)
#%%


#%%
esql = """LOAD DATA INFILE '/Users/jha/Documents/spring2020/data/ecoli_IB/Pathogen.tsv'
                      INTO TABLE Ecoli_IB_AMR
                      FIELDS TERMINATED BY '\t' 
                      ENCLOSED BY '"'
                      LINES TERMINATED BY '\n'
                      IGNORE 1 ROWS
                      ;"""
cursor.execute(esql)
#%%

#%%



sql ="""CREATE TABLE `Ecoli_IB_AMR` (
	`AMR_genotypes` BLOB,
    `aac(3)-VIa` BLOB,
    `blaPSE` BLOB,
    `tet(G)` BLOB,
    `blaCMY-154` BLOB,
    `blaSHV-30` BLOB,
    `tet(K)` BLOB,
    `aac(2')-IIa` BLOB,
    `blaKPC-18` BLOB,
    `nfsA_Q44STOP` BLOB,
    `parE_E460D` BLOB,
    `catA1` BLOB,
    `parE_L416F` BLOB,
    `lnu(C)` BLOB,
    `soxR_G121D` BLOB,
    `cmlA5` BLOB,
    `blaCTX-M-115` BLOB,
    `parE_I355T` BLOB,
    `blaSHV-1` BLOB,
    `aac(6')-Ib3` BLOB,
    `qnrB1` BLOB,
    `blaKPC-2` BLOB,
    `blaTEM-34` BLOB,
    `arr-3` BLOB,
    `mef(B)` BLOB,
    `qnrS13` BLOB,
    `floR` BLOB,
    `ant(3'')-Ia` BLOB,
    `fosA8` BLOB,
    `ere(D)` BLOB,
    `aadA16` BLOB,
    `aph(3')-IIIa` BLOB,
    `parC_A108V` BLOB,
    `aph(6)-Id` BLOB,
    `aac(6')-Il` BLOB,
    `blaCTX-M-8` BLOB,
    `fos` BLOB,
    `blaKPC` BLOB,
    `aadA22` BLOB,
    `tet(H)` BLOB,
    `erm(42)` BLOB,
    `dfrA23` BLOB,
    `blaTEM-148` BLOB,
    `nfsA_R203L` BLOB,
    `blaTEM-210` BLOB,
    `blaOXA-1` BLOB,
    `blaROB` BLOB,
    `parC_A56T` BLOB,
    `dfrA12` BLOB,
    `tet(A)` BLOB,
    `erm(G)` BLOB,
    `qnrD` BLOB,
    `gyrA_D87Y` BLOB,
    `rmtE1` BLOB,
    `tet(E)` BLOB,
    `rpoB_Q513L` BLOB,
    `blaFOX-5` BLOB,
    `parC_E84A` BLOB,
    `abc-f` BLOB,
    `qnrA` BLOB,
    `blaACT` BLOB,
    `fosA7.5` BLOB,
    `ere(A)` BLOB,
    `blaSHV-2A` BLOB,
    `blaTEM-181` BLOB,
    `aadA3` BLOB,
    `gyrA_D87H` BLOB,
    `sul3` BLOB,
    `blaCTX-M-104` BLOB,
    `tet(D)` BLOB,
    `mef(C)` BLOB,
    `aac(3)-Ib` BLOB,
    `aac(6')-Ib4` BLOB,
    `dfrA36` BLOB,
    `blaTEM-10` BLOB,
    `qnrS2` BLOB,
    `dfrA32` BLOB,
    `fosA3` BLOB,
    `16S_C1192T` BLOB,
    `dfrA10` BLOB,
    `soxR_R20H` BLOB,
    `ant(3'')` BLOB,
    `dfrA8` BLOB,
    `dfrA7` BLOB,
    `blaCTX-M-2` BLOB,
    `blaLAP` BLOB,
    `tet(X)` BLOB,
    `emrD` BLOB,
    `aadA12` BLOB,
    `parE_D475E` BLOB,
    `aph(3')-VI` BLOB,
    `nfsA_R15C` BLOB,
    `aac(3)-IIa` BLOB,
    `mph(B)` BLOB,
    `aac(6')-Ib-cr` BLOB,
    `qnrB` BLOB,
    `qepA7` BLOB,
    `blaTEM` BLOB,
    `blaSHV-12` BLOB,
    `aadD1` BLOB,
    `cyaA_S352T` BLOB,
    `bleO` BLOB,
    `blaCMY-7` BLOB,
    `aac(6')` BLOB,
    `aac(6')-Ib` BLOB,
    `blaZ` BLOB,
    `tet(41)` BLOB,
    `aph(3')-Ib` BLOB,
    `tet` BLOB,
    `blaHER-3` BLOB,
    `qnrS11` BLOB,
    `dfrA21` BLOB,
    `blaCTX-M-216` BLOB,
    `dfrA27` BLOB,
    `catB3` BLOB,
    `parC_E84G` BLOB,
    `aadA8` BLOB,
    `16S_A794G` BLOB,
    `blaTEM-1` BLOB,
    `aac(6')-Ib'` BLOB,
    `blaOXA-10` BLOB,
    `dfrB4` BLOB,
    `qnrA1` BLOB,
    `gyrB_D426N` BLOB,
    `dfrA17` BLOB,
    `folP_F28L` BLOB,
    `blaTEM-52` BLOB,
    `aadA4` BLOB,
    `folP_P64L` BLOB,
    `parE_I464F` BLOB,
    `blaCTX-M` BLOB,
    `rpoB_S531F` BLOB,
    `dfrA3` BLOB,
    `blaTEM-169` BLOB,
    `ant(2'')-Ia` BLOB,
    `qnrD1` BLOB,
    `qnrB2` BLOB,
    `floR2` BLOB,
    `rmtC` BLOB,
    `rpoB_V146F` BLOB,
    `ampC_T-14TGT` BLOB,
    `ere(B)` BLOB,
    `lnu(A)` BLOB,
    `catB11` BLOB,
    `aac(6')-Ib-cr5` BLOB,
    `parE_S458T` BLOB,
    `tet(C)` BLOB,
    `aac(6')-33` BLOB,
    `blaCARB-2` BLOB,
    `msr(E)` BLOB,
    `blaNDM-9` BLOB,
    `blaTEM-171` BLOB,
    `gyrA_G81C` BLOB,
    `blaTEM-190` BLOB,
    `blaTEM-156` BLOB,
    `erm(F)` BLOB,
    `aac(3)-IVa` BLOB,
    `ble` BLOB,
    `blaSRT` BLOB,
    `aph(3')-I` BLOB,
    `blaOXA-2` BLOB,
    `acrB_R620C` BLOB,
    `aph(3')-IIa` BLOB,
    `aadA31` BLOB,
    `blaCTX-M-65` BLOB,
    `marR_R94H` BLOB,
    `blaDHA-1` BLOB,
    `dfrA34` BLOB,
    `parC_A108T` BLOB,
    `marR_R77L` BLOB,
    `blaTEM-84` BLOB,
    `blaCMY-6` BLOB,
    `parE_D476N` BLOB,
    `dfrA16` BLOB,
    `aac(3)-I` BLOB,
    `aadA15` BLOB,
    `ampC_G-15GG` BLOB,
    `catB8` BLOB,
    `aph(6)-Ic` BLOB,
    `aph(4)-Ia` BLOB,
    `basR_G53E` BLOB,
    `blaNDM` BLOB,
    `arr-2` BLOB,
    `aadA1` BLOB,
    `soxS_A12S` BLOB,
    `blaNDM-5` BLOB,
    `blaOXA-244` BLOB,
    `blaVEB` BLOB,
    `blaLAP-2` BLOB,
    `folP_P64S` BLOB,
    `mph(E)` BLOB,
    `blaCMY-4` BLOB,
    `qepA1` BLOB,
    `blaNDM-4` BLOB,
    `parC_E84V` BLOB,
    `blaCTX-M-55` BLOB,
    `blaCTX-M-32` BLOB,
    `blaNDM-1` BLOB,
    `dfrA15` BLOB,
    `acrR_R45C` BLOB,
    `dfrA` BLOB,
    `aac(3)-IId` BLOB,
    `blaIMP-27` BLOB,
    `blaR1` BLOB,
    `qnrB77` BLOB,
    `blaTEM-207` BLOB,
    `oqxA` BLOB,
    `uhpT_E350Q` BLOB,
    `aadA5` BLOB,
    `sdeB` BLOB,
    `blaLAP-1` BLOB,
    `ampC_C-42T` BLOB,
    `blaCMY-44` BLOB,
    `blaTEM-168` BLOB,
    `aadA6` BLOB,
    `pmrB_L10P` BLOB,
    `pmrB_E121K` BLOB,
    `parC_S80I` BLOB,
    `gyrA_D87N` BLOB,
    `qnrB7` BLOB,
    `dfrA19` BLOB,
    `qxB` BLOB,
    `pmrB_C84Y` BLOB,
    `qepA4` BLOB,
    `mcr-10.1` BLOB,
    `erm(B)` BLOB,
    `parC_E84K` BLOB,
    `blaTEM-35` BLOB,
    `parC_S80R` BLOB,
    `armA` BLOB,
    `nfsA_S33R` BLOB,
    `aadS` BLOB,
    `cmlA4` BLOB,
    `uhpA_G97D` BLOB,
    `lnu(G)` BLOB,
    `blaCTX-M-134` BLOB,
    `dfrA5` BLOB,
    `ble-Sh` BLOB,
    `rmtB1` BLOB,
    `aph(3')-II` BLOB,
    `aac(3)` BLOB,
    `blaTEM-19` BLOB,
    `blaCTX-M-1` BLOB,
    `blaEC` BLOB,
    `cmlA1` BLOB,
    `tet(M)` BLOB,
    `blaCMY-59` BLOB,
    `23S_T2609C` BLOB,
    `lnu(AN2)` BLOB,
    `ampC` BLOB,
    `blaCTX-M-27` BLOB,
    `rpoB_I572L` BLOB,
    `ampC_C-11T` BLOB,
    `aadA25` BLOB,
    `dfrA14` BLOB,
    `qnrS1` BLOB,
    `blaCTX-M-3` BLOB,
    `blaCMY-2` BLOB,
    `ampC_T-32A` BLOB,
    `qepA8` BLOB,
    `smfY` BLOB,
    `mph(A)` BLOB,
    `nfsA_R133S` BLOB,
    `blaNDM-27` BLOB,
    `mcr-1` BLOB,
    `nfsA_R203C` BLOB,
    `gyrA_S83A` BLOB,
    `qnrB4` BLOB,
    `dfrA24` BLOB,
    `qnrS` BLOB,
    `blaOXA-9` BLOB,
    `tet(Q)` BLOB,
    `blaCTX-M-9` BLOB,
    `ptsI_V25I` BLOB,
    `blaNDM-7` BLOB,
    `blaOXA` BLOB,
    `blaHER` BLOB,
    `blaTEM-54` BLOB,
    `parE_S458A` BLOB,
    `blaCTX-M-98` BLOB,
    `blaTEM-214` BLOB,
    `gyrA_S83L` BLOB,
    `aac(3)-IV` BLOB,
    `pmrB_V161G` BLOB,
    `nfsA_G131D` BLOB,
    `blaOXA-48` BLOB,
    `blaCTX-M-14` BLOB,
    `blaEC-5` BLOB,
    `blaTEM-33` BLOB,
    `parE_I529L` BLOB,
    `aac(3)-IIe` BLOB,
    `gyrA_D87G` BLOB,
    `blaSHV-7` BLOB,
    `qnrE` BLOB,
    `cmlA6` BLOB,
    `fosA5` BLOB,
    `blaCTX-M-24` BLOB,
    `fosA7` BLOB,
    `aadA13` BLOB,
    `blaTEM-12` BLOB,
    `23S_G2032A` BLOB,
    `mdtM` BLOB,
    `catA2` BLOB,
    `blaCMY-42` BLOB,
    `sul2` BLOB,
    `blaGES-5` BLOB,
    `aphA16` BLOB,
    `pmrB_T156M` BLOB,
    `blaTEM-176` BLOB,
    `blaSHV-2` BLOB,
    `parE_L445H` BLOB,
    `dfrA1` BLOB,
    `blaI` BLOB,
    `ompF_G141D` BLOB,
    `mph(G)` BLOB,
    `blaTEM-30` BLOB,
    `dfrA26` BLOB,
    `dfrA25` BLOB,
    `acrF` BLOB,
    `gyrA_S83V` BLOB,
    `aac(6')-IIc` BLOB,
    `fosA` BLOB,
    `blaTEM-57` BLOB,
    `aadA2` BLOB,
    `blaSHV` BLOB,
    `mcr-9.1` BLOB,
    `blaVIM-1` BLOB,
    `blaCTX-M-15` BLOB,
    `blaTEM-40` BLOB,
    `parE_E460K` BLOB,
    `blaKPC-3` BLOB,
    `16S_G527T` BLOB,
    `aadA7` BLOB,
    `blaTEM-116` BLOB,
    `blaOXA-181` BLOB,
    `dfr7` BLOB,
    `blaKPC-4` BLOB,
    `rpoB_I572F` BLOB,
    `tet(Y)` BLOB,
    `mcr-9` BLOB,
    `blaCMY-141` BLOB,
    `blaCMY` BLOB,
    `sul1` BLOB,
    `fabI_F203L` BLOB,
    `blaSCO-1` BLOB,
    `mcr-1.1` BLOB,
    `blaSHV-11` BLOB,
    `sat2` BLOB,
    `mph_3` BLOB,
    `arr` BLOB,
    `aph(3')-Ia` BLOB,
    `qnrB6` BLOB,
    `aph(3'')-Ib` BLOB,
    `bla` BLOB,
    `blaSHV-5` BLOB,
    `parC_S57T` BLOB,
    `cmlA` BLOB,
    `aac(3)-II` BLOB,
    `catA3` BLOB,
    `lnu(F)` BLOB,
    `tet(B)` BLOB,
    `blaTEM-135` BLOB,
    `gyrA_S83W` BLOB,
    `sdeY` BLOB,
    `fosA4` BLOB,
    `qnrB19` BLOB,
    `marR_S3N` BLOB)"""
cursor.execute(sql)
#cursor.commit()

#%%