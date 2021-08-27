# Remote_Careers-DATS6401
An analysis into the rising prevalence of remote work opportunities arising during the 2020 Covid-19 Pandemic
Full visualization webpage [https://m-mcdougall.github.io/Remote_Careers-DATS6401/]

## Data Sources

Occupational categories and sample occupations were taken from the Bureau of Labor and Statistics' Standard Occupational Classification System Structure Manual [https://www.bls.gov/soc/2018/soc_2018_manual.pdf]  
All Job postings taken from Indeed.com [https://www.indeed.com/]  

## Running the Code

To generate the data for yourself, run the scripts in the following order:  
1. Generate_Jobs.py  
  -Creates the excel sheet of sample positions  
  -Open the resulting file, and process the positions to be more searchable  
2. Webscraper.py  
  -Runs the webscraper to download the job postings  
  -Note: this will take a substantial amount of time, as the requests need to be spaced out to avoid alerting Indeed's bot detector.  
3. Data_Processing.py  
  -Processes the data, adding wages and regions  


### Templates

Bootstrap Grayscale template [https://startbootstrap.com/theme/grayscale]
