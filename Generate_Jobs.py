# -*- coding: utf-8 -*-
#%%

import os
import pandas as pd


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401//Data//')
os.chdir(wd)


#Load the full list of Occupations and OccupationCategories
x=pd.read_excel('Job_Titles.xlsx', sheet_name='Attempt')

#Collector 
collect=[]

#Parse the columns into a condensed form
for i in range(x.shape[0]):
    this_row=x.iloc[i,:].dropna()
    
    if this_row.shape[0] == 2:
        collect.append(this_row.values)
    elif this_row.shape[0] >= 3:
        collect.append(this_row.values[-2::])
    else:
        pass
    

#Collapse the collector
collect2 = pd.DataFrame(collect) 
collect2 = collect2.drop_duplicates(subset=1)
collect2[0]=collect2[0].str[0:2]


#%%

# Sample the condensed list of Occupations
# Sample each 4 times without replacement
data = []
for category in collect2[0].unique():
    
    this_cat=collect2[collect2[0] == category]
    
    this_cat=this_cat.sample(n=4, random_state=42)
    data.append(this_cat)

data=pd.concat(data)

#Export sampled Occupations
data.to_excel('Modified_Jobs.xlsx', index=False)