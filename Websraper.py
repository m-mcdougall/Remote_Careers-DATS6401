# -*- coding: utf-8 -*-


#Going to want to extract the date stolen, the location, if the lock was circumvented, and the bike ID (address)



import os
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import concurrent.futures as cf


pd.set_option('display.max_columns', 10)


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Remote_Careers-DATS6401')
os.chdir(wd)




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
    
    url='https://www.indeed.com/jobs?as_and='+title_str+'&radius='+str(radius)+'&l='+city_str+'&fromage=any&limit=50&sort=date&psf=advsrch&from=advancedsearch'
    
    return url
    
page_url = make_url('system admin', 'Seattle', radius=10)





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
        
        job_title = result.find('h2').find('a')['title']
        
        try:
            stars=result.find('span', {'class':'ratingsContent'}).get_text().strip()
        except:
            stars=np.nan
        
        company = result.find('span', {'class':'company'}).get_text().strip()
        
        location = result.find('div', {'class':'recJobLoc'})['data-rc-loc'].strip()
        
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

x=search_page_downloader(page_url)
#%%
