# -*- coding: utf-8 -*-


import os
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', 10)


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401//Data//')
os.chdir(wd)




#%%



for file in os.listdir():
    if '\xa0' in file:
        if file.strip() in os.listdir():
            pass
        else:
            os.rename(file, file.strip())
        
        
#%%

data=[]

for file in os.listdir():
    if '.csv' in file:
        data.append(pd.read_csv(file))
        
        
data=pd.concat(data)

#%%


data.Remote.value_counts()

#%%

data.groupby('Category').Remote.value_counts()