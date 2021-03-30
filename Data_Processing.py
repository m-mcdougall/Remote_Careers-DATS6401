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




#%%

#For the original files,a whitespace character was present in the file string

for file in os.listdir():
    if '\xa0' in file:
        if file.strip() in os.listdir():
            pass
        else:
            os.rename(file, file.strip())
        
        
#Load the files and concatinate
data=[]

for file in os.listdir():
    if '.csv' in file:
        data.append(pd.read_csv(file, index_col=0))
        
        
data=pd.concat(data)

data=data.reset_index(drop=True)

#%%

#Wage calculators



known_wage=data[data.Wage != 'Unknown']

#Seperate the wages into hourly pay and year
hourly = known_wage[known_wage.Wage.str.contains('hour')]
annual = known_wage[known_wage.Wage.str.contains('year')]
#%%

#===================

#Annual - Handle the ranges, 'Up to's and 'Starting at's

#===================

overall_annual=[]

#Annual Ranges
#---------------

#Contains a range
an_wage = annual[annual.Wage.str.contains(' - ')]
results=an_wage.Wage.str.extractall('([$](\d)+\,(\d)+)')[0].reset_index()


#Seperate the matches into the upper and lower bounds, reset index
match0=results[results.match==0].set_index(an_wage.index)
match1=results[results.match==1].set_index(an_wage.index)



#Extract the upper and lower values, and convert to int
results=pd.DataFrame(index=an_wage.index)
results['Lower'] = match0[0].str[1::].str.replace(',','').astype(int)
results['Upper'] = match1[0].str[1::].str.replace(',','').astype(int)

#Calculated midpoint in the range
results['Midrange'] = (results['Lower'] +results['Upper'] )/2

#Append to collector
overall_annual.append(results)
#%%

#Annual Up to
#---------------

#Up to a set value
an_wage = annual[annual.Wage.str.contains('Up to')]
results=an_wage.Wage.str.extract('([$](\d)+\,(\d)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the upper value, then estimate the lower and mid values
results['Upper'] = results[0].str[1::].str.replace(',','').astype(int)
results['Lower'] = results['Upper']*0.8
results['Midrange'] = results['Upper']*0.9

#Clean columns
results=results.drop(['index', 0], axis=1)

#Append to collector
overall_annual.append(results)

#%%

#Annual From
#---------------

#Up to a set value
an_wage = annual[annual.Wage.str.contains('From')]
results=an_wage.Wage.str.extract('([$](\d)+\,(\d)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the lower value, then estimate the upper and mid values
results['Lower'] = results[0].str[1::].str.replace(',','').astype(int)
results['Upper'] = results['Lower']*1.2
results['Midrange'] = results['Lower']*1.1

#Clean columns
results=results.drop(['index', 0], axis=1)

#Append to collector
overall_annual.append(results)


#%%

#Annual Remaining - Specifies the exact amount
#---------------

#These inputs are in the format: '$54,000 a year'

#Exclude all previously extracted, leaves us with the desired section
an_wage = annual[(~annual.Wage.str.contains('From'))&(~annual.Wage.str.contains('Up to'))&(~annual.Wage.str.contains(' - '))]

#Extract the exact wage
results=an_wage.Wage.str.extract('([$](\d)+\,(\d)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the lower value, then estimate the upper and mid values
results['Lower'] = results[0].str[1::].str.replace(',','').astype(int)
results['Upper'] = results['Lower']
results['Midrange'] = results['Lower']

#Clean columns
results=results.drop(['index', 0], axis=1)

#Append to collector
overall_annual.append(results)

#%%

#Concatinate the collected wages
annual_out=pd.concat(overall_annual)


#Join together the Annual data and the wage columns
annual=annual.reset_index()
annual_out=annual_out.reset_index()

all_annual_out = annual.merge(annual_out, on=['index'])

#%%

#===================

#Hourly - Handle the ranges, 'Up to's and 'Starting at's

#===================

overall_hourly=[]
hours_to_annual = 40 * 52 #Assumes 40h/week, 52 weeks/year


#Hourly Ranges
#---------------

#Contains a range
hour_wage = hourly[hourly.Wage.str.contains(' - ')]
results=hour_wage.Wage.str.extractall('([\$](\S)+)')[0].reset_index()


#Seperate the matches into the upper and lower bounds, reset index
match0=results[results.match==0].set_index(hour_wage.index)
match1=results[results.match==1].set_index(hour_wage.index)



#Extract the upper and lower values, and convert to int
results=pd.DataFrame(index=hour_wage.index)
results['Lower'] = match0[0].str[1::].str.replace(',','').astype(float)
results['Upper'] = match1[0].str[1::].str.replace(',','').astype(float)

#Calculated midpoint in the range
results['Midrange'] = (results['Lower'] +results['Upper'] )/2
results=results*hours_to_annual


#Append to collector
overall_hourly.append(results)


#%%


#Hourly Up to
#---------------

#Up to a set value
hour_wage = hourly[hourly.Wage.str.contains('Up to')]
results=hour_wage.Wage.str.extract('([$](\S)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the upper value, then estimate the lower and mid values
results['Upper'] = results[0].str[1::].str.replace(',','').astype(float)
results['Lower'] = results['Upper']*0.8
results['Midrange'] = results['Upper']*0.9

#Clean columns
results=results.drop(['index', 0], axis=1)
results=results*hours_to_annual

#Append to collector
overall_hourly.append(results)

#%%

#Hourly From
#---------------

#Up to a set value
hour_wage = hourly[hourly.Wage.str.contains('From')]
results=hour_wage.Wage.str.extract('([$](\S)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the lower value, then estimate the upper and mid values
results['Lower'] = results[0].str[1::].str.replace(',','').astype(float)
results['Upper'] = results['Lower']*1.2
results['Midrange'] = results['Lower']*1.1

#Clean columns
results=results.drop(['index', 0], axis=1)
results=results*hours_to_annual

#Append to collector
overall_hourly.append(results)


#%%

#Hourly Remaining - Specifies the exact amount
#---------------

#These inputs are in the format: '$54,000 a year'

#Exclude all previously extracted, leaves us with the desired section
hour_wage = hourly[(~hourly.Wage.str.contains('From'))&(~hourly.Wage.str.contains('Up to'))&(~hourly.Wage.str.contains(' - '))]

#Extract the exact wage
results=hour_wage.Wage.str.extract('([$](\S)+)')[0].reset_index()

#Set index to the original
results=results.set_index(results['index'])


#Extract the lower value, then estimate the upper and mid values
results['Lower'] = results[0].str[1::].str.replace(',','').astype(float)
results['Upper'] = results['Lower']
results['Midrange'] = results['Lower']

#Clean columns
results=results.drop(['index', 0], axis=1)
results=results*hours_to_annual

#Append to collector
overall_hourly.append(results)


#%%
#Join together the Hourly data and the wage columns

#Concatinate the collected wages
hourly_out=pd.concat(overall_hourly)


#Join together the Annual data and the wage columns
hourly=hourly.reset_index()
hourly_out=hourly_out.reset_index()

all_hourly_out = hourly.merge(hourly_out, on=['index'])


#%%

#===================

#All Wages - Join Annual and Hourly

#===================


data2=pd.concat([all_annual_out, all_hourly_out]).set_index(['index'])

data=data2.append(data[data.Wage == 'Unknown'])
#data=data2.fillna('Unknown')

data=data.sort_index(axis=0)


del [match0, match1, data2, results, known_wage, all_annual_out,all_hourly_out,
    an_wage, annual, annual_out, hour_wage, hourly, hourly_out, hours_to_annual,
    overall_annual, overall_hourly,]



#%%
#===================

#Add Region - Add a region by state

#===================


def create_regions():
    #Get a list of us state abbreviations
    runfile(os.path.abspath('..')+'//UsStateAbbreviations.py')
    
    #Define the regions and the component states
    regions={"Pacific":['WA', 'OR','CA','NV','AK','HI',],
             'Rocky_Mountains':['MT','ID','WY','UT','CO', 'AZ','NM',],
             'Midwest':['ND','SD','NE','KS','MN','IA','MO','WI','IL','MI','IN','OH'],
             'Southwest':['TX','OK', 'AR','LA',],
             'Southeast':['KY','TN','MS','AL','WV','VA','NC','SC','GA','FL',],
             'Northeast':['ME','NH','VT','NY','MA','RI','CT','PA','NJ','DE','MD','DC']}    
    
    
    #Flip the key:value pairs, to assign one region for each state
    region_flip={}
    for key in regions:
        for state in regions[key]:
            full_state = abbrev_us_state[state]
            region_flip[full_state]=key
        

    return region_flip

region_dict=create_regions()

data['SearchState']=data['SearchState'].str.strip()

data['Region']=data['SearchState'].replace(region_dict)

#%%


data.groupby(['Category']).agg({'Midrange':'mean', })
data.groupby(['SearchState']).agg({'Midrange':'mean', })
data.groupby(['Region']).agg({'Midrange':'mean', 'Midrange':'var',})




