# -*- coding: utf-8 -*-
#%%

import os
import pandas as pd


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401//Data//')
os.chdir(wd)



x=pd.read_excel('Job_Titles.xlsx', sheet_name='Attempt')

collect=[]

for i in range(x.shape[0]):
    this_row=x.iloc[i,:].dropna()
    
    if this_row.shape[0] == 2:
        collect.append(this_row.values)
    elif this_row.shape[0] >= 3:
        collect.append(this_row.values[-2::])
    else:
        pass
    


collect2 = pd.DataFrame(collect) 

collect2 = collect2.drop_duplicates(subset=1)
   
collect2[0]=collect2[0].str[0:2]


#%%
data = []
for category in collect2[0].unique():
    
    this_cat=collect2[collect2[0] == category]
    
    this_cat=this_cat.sample(n=4, random_state=42)
    data.append(this_cat)

data=pd.concat(data)

data.to_excel('Modified_Jobs.xlsx', index=False)