#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as cm

#%%
df_gsh = pd.read_excel('/Users/jhasneha/Documents/Spring2021/AMR/DATA _From_Jha/New Folder With Items 2/gene_samplehost.xlsx', sheet_name='Sheet1')
#df_gsh=df_gsh.drop(["acrF","blaEC","mdtM"], axis=1)
df_gshT=df_gsh.T
df_gshT.columns=df_gshT.iloc[0]
df_gshT=df_gshT.drop(df_gshT.index[0])

#df_gshT=df_gshT.reset_index()

# %%
#viridis = cm.get_cmap('viridis', 14)
ax=df_gshT.plot.bar(stacked=True)
plt.legend(bbox_to_anchor=(1,1), loc='upper left')
#plt.tight_layout()
#plt.axes()
#plt.show()

# %%
