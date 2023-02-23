#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 19:27:02 2023

@author: meaganpatrick
"""
#download packages
import pandas as pd
import urllib.request
import http.cookiejar
import time
import os
import re
import calendar

#we only want to download the halt incident lists for now,
#so filter the urls to include only those which have halt incident lists. 

#create/define download directory (should have been created in n1_geturls.py)
download_dir = "downloads/halt/"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

#first, import the csv created in step (1) with all of the urls. 
urldf=pd.read_csv('downloads/reporturls.csv')

halt=urldf[urldf['fullurl'].str.contains("halt-incident-list")].reset_index()
halt=halt[['urlnames','fullurl']]

#create new columns for the months so that you can sort by month and year, extracting
#from the text in the url. 
halt['year']=halt['urlnames'].str.split('-').str[-1]
halt['month']=halt['urlnames'].str.split('-').str[-2]

month_dict = {
    'january': '01',
    'february': '02',
    'march': '03',
    'april': '04',
    'may': '05',
    'june': '06',
    'july': '07',
    'august': '08',
    'september': '09',
    'october': '10',
    'november': '11',
    'december': '12'
}

halt['monthnum']=halt['month'].map(month_dict)
halt['year_month']=halt['year']+'.'+halt['monthnum']

print('Number of halt incident reports:',len(halt))
print('Reports from months:',halt['year_month'].sort_values())

#check that the number of reports is as expected. Reports started in April 2022. 
#calculate number of months since start
date_range = pd.date_range(start='2022-04-01', end=pd.Timestamp.today(), freq='M')
num_months = len(date_range)

#calculate number of reports 
num_reports=len(halt)

# check if num_reports is equal to num_months
if num_reports == num_months:
    print("The number of reports is adequate.")
elif num_reports>num_months:
    print("There are too many reports")
else:
    print("There are too few reports")

#Using the URLs, Download all of the Halt Incident Reports 
cookie_jar = http.cookiejar.CookieJar()

# Set the cookie jar in the request
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Iterate through each URL in the specified column
for url in halt['fullurl']:
    # Wait for a few seconds before making the next request
    time.sleep(5)

    # Set a custom User-Agent and Referer header
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    #req.add_header("Referer", "doccs.ny.gov")

    # Send the request with the cookie jar
    response = opener.open(req)
    content = response.read()

    # Download the file
    filename = url.split("/")[-1]
    if not filename.endswith(".pdf"):
        filename = filename + ".pdf"
    filepath = os.path.join(download_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    print(f"Downloaded {filename}")