# -*- coding: utf-8 -*-


import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from datetime import date
from datetime import timedelta

pd.set_option('display.max_columns', 10)


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401')
os.chdir(wd)


today = date.today()+ + timedelta(days=1)

#%%

def make_url(title_str, city_str, radius=10):
    """
    Creates an indeed job search url based on input variables
    
    title_str: The job title to search for, as string
    city_str: The name of the city to search for, as string
    radius: The radius around the city to search
    """
    
    title_str=title_str.replace(' ', '+')
    city_str=city_str.replace(' ', '+')
    
    url='https://www.indeed.com/jobs?as_and='+title_str+'&radius='+str(radius)+'&l='+city_str+'&fromage=15&limit=50&filter=0&psf=advsrch&forceLocation=1&from=advancedsearch'
    
    return url
    
#page_url = make_url('system admin', 'Seattle', radius=10)





def search_page_downloader(page_url):
    """
    Download all the jobs in the search page, extract all needed tags from the miniature posting
    Downloads all jobs and returns a dataframe with all information
    
    page_url: The search URL created with make_url
    """
    
    #Download the page
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    #Isolate the job search result cards
    results =soup.find_all('div', {'class':'jobsearch-SerpJobCard unifiedRow row result'})
    
    #Data collection list
    data=[]
    
    #For each result, extract all desired information
    for result in results:
        
        try: #This will always find a job title, unless there were no postings for that search
            job_title = result.find('h2').find('a')['title']
        except:
            job_title = 'ERROR'
            
        if job_title == 'ERROR':
            print(f'ERROR with:\n {page_url}')
            continue # Catches the error and quits the loop
        
        try:
            stars=result.find('span', {'class':'ratingsContent'}).get_text().strip()
        except:
            stars=np.nan
        try:
            company = result.find('span', {'class':'company'}).get_text().strip()
        except:
            company = 'ERROR'
            
        if company == 'ERROR':
            print(f'ERROR with:\n {page_url}')
            continue # Catches the error and quits the loop
        try:
            location = result.find('div', {'class':'recJobLoc'})['data-rc-loc'].strip()
        except:
            location = 'ERROR'
            
        if location == 'ERROR':
            print(f'ERROR with:\n {page_url}')
            continue # Catches the error and quits the loop
        try:
            wage=result.find('span', {'class':'salaryText'}).get_text().strip()
        except:
            wage='Unknown'
         
        try:    
            remote=result.find('span', {'class':'remote'}).get_text().strip()   
        except:
            remote='Not Remote'
            
        #Aggregate the extracted variables
        data.append(pd.Series(data={'Title':job_title, 'Company':company, 'Stars':stars, 'Location':location, 'Wage':wage, 'Remote':remote}))

    #Aggrigate all postings and return
    data=pd.DataFrame(data)
    
    return data

#x=search_page_downloader(page_url)
#%%


cities= pd.read_excel('.//Data//Job_Titles.xlsx', )
cities=cities[~cities.State.isin([' American Samoa', ' Guam', ' Northern Mariana Islands', ' Puerto Rico', ' Virgin Islands (U.S.)'])]
cities.reset_index(drop=True, inplace=True)





job_collect=[]

for i in range(cities.shape[0]):
    
    page_url=make_url('Data Scientist', cities.MostPopulous[i], radius=10)
    x=search_page_downloader(page_url)
    
    x.insert(column='SearchCity', loc=0, value=cities.MostPopulous[i])
    x.insert(column='SearchState', loc=0, value=cities.State[i])
    
    job_collect.append(x)
    
    time.sleep(np.random.random_sample()*3)

job_collect_df=pd.concat(job_collect)






#%%
#Import the modified jobs excel data file

jobs= pd.read_excel('.//Data//Modified_Jobs2.xlsx', )
jobs.rename(columns={0:'Category', 1:"JobTitle"}, inplace=True)


job_collect=[]

for i in range(jobs.shape[0]):
    
    page_url=make_url(jobs.JobTitle[i], 'Seattle', radius=10)
    x=search_page_downloader(page_url)
    
    x.insert(column='SearchTitle', loc=0, value=jobs.JobTitle[i])
    x.insert(column='Category', loc=0, value=jobs.Category[i])
    
    job_collect.append(x)
    
    time.sleep(np.random.random_sample()*3)

job_collect_df=pd.concat(job_collect)


#%%

cities= pd.read_excel('.//Data//Job_Titles.xlsx', )
cities=cities[~cities.State.isin([' American Samoa', ' Guam', ' Northern Mariana Islands', ' Puerto Rico', ' Virgin Islands (U.S.)'])]
cities.reset_index(drop=True, inplace=True)


jobs= pd.read_excel('.//Data//Modified_Jobs2.xlsx', )
jobs.rename(columns={0:'Category', 1:"JobTitle"}, inplace=True)





for k in range(0,cities.shape[0]):

    
    city=cities['Third Most'][k]
    state=cities.State[k]
    job_collect=[]
    
    if city is np.nan:
        continue
    
    print(f'\n\nNow working on {city}, {state}.\n\n')
    
    for i in tqdm(range(jobs.shape[0])):
        
        page_url=make_url(jobs.JobTitle[i], city, radius=10)
        x=search_page_downloader(page_url)
        
        x.insert(column='SearchTitle', loc=0, value=jobs.JobTitle[i])
        x.insert(column='Category', loc=0, value=jobs.Category[i])
        x.insert(column='SearchCity', loc=0, value=city)
        x.insert(column='SearchState', loc=0, value=state)
        
        
        job_collect.append(x)
        
        #Sleep to reduce rates of captcha
        time.sleep(np.random.random_sample()*6)
    
    
    #End of the State, save the result in case of crash or captcha
    job_collect_df=pd.concat(job_collect)
    job_collect_df.to_csv('.//Data//'+state+' '+str(today)+'.csv')
    
    print('\n\n\nWaiting........\n\n\n')
    time.sleep(np.random.random_sample()*14)
