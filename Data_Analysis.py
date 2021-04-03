# -*- coding: utf-8 -*-

#Imports

import os
import pandas as pd
import numpy as np
import re


#%%

pd.set_option('display.max_columns', 10)


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401//Data//')
os.chdir(wd)

#Load the Data
data=pd.read_excel('Data_out.xlsx')

data=data.rename(columns={'Not Remote-OHE':'NotRemoteOHE', 'Remote-OHE':'RemoteOHE',
                          'Temporarily remote-OHE':'TempRemoteOHE'})

#%%

def jobsRemoteValPercent(groupby_in, df_in):
    """
    Calculates the total number of jobs and the percentages of jobs that are remote given a groupby
    
    groupby_in: The categories of the data to groupby
    df_in: The dataframe loaded from Data_out.xlsx. 
    """
    
    calc=df_in.groupby(groupby_in).sum()
    
    calc['AllRemote']=calc['RemoteOHE']+calc['TempRemoteOHE']
    calc['Total_jobs']=calc['RemoteOHE']+calc['TempRemoteOHE']+calc['NotRemoteOHE']
    
    
    calc['Percent_Remote']= calc['RemoteOHE']/calc['Total_jobs']*100
    calc['Percent_Temp']= calc['TempRemoteOHE']/calc['Total_jobs']*100
    calc['Percent_NotRemote']= calc['NotRemoteOHE']/calc['Total_jobs']*100
    calc['Percent_AllRemote']= calc['AllRemote']/calc['Total_jobs']*100
    
    #Only keep the jobs columns - the groupbys are still hidden in the index
    out=calc.filter(['Total_jobs','Percent_Remote','Percent_Temp', 'Percent_NotRemote', 'NotRemoteOHE', 'RemoteOHE',
           'TempRemoteOHE', 'AllRemote', 'Percent_AllRemote'])
    #Reset the groupbys
    out.reset_index(inplace=True)

    return out


x=jobsRemoteValPercent(['CategoryStr'], data)




















#%%
# Useful for looking at wage/star value by remote status
df_in =data.copy()
groupby_in = ['SearchState']
agg_outs={'Stars':'mean', 'Midrange':'mean'}


#def inspectByRemote()

df_in['All_Remote']= df_in['RemoteOHE']+df_in['TempRemoteOHE']

if 'Remote' not in groupby_in:
    groupby_in=groupby_in+['Remote']

calc=df_in.groupby(groupby_in).agg(agg_outs)
calc=calc.reset_index()






























